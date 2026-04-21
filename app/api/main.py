"""FastAPI application — intake + stream endpoints."""

import asyncio
import json
import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, EmailStr, TypeAdapter, ValidationError

from app.agent.guardrails import check_input_safety
from app.agent.pipeline import run_triage_pipeline
from app.db.config import close_db, init_db
from app.db.models import IncidentSeverity, IncidentStatus
from app.db.repository import create_incident, get_incident, list_incidents

logger = structlog.get_logger()

UPLOADS_DIR = "uploads"
ALLOWED_MIMES = {"image/png", "image/jpeg", "text/plain", "application/json", "application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Magic-byte prefixes per declared MIME. `text/plain` and `application/json`
# have no fixed signature — validated by decoding attempt instead.
_MAGIC_BYTES: dict[str, bytes] = {
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
    "application/pdf": b"%PDF-",
}

_EMAIL_ADAPTER: TypeAdapter[EmailStr] = TypeAdapter(EmailStr)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("starting", service="triagista")
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    await init_db()
    yield
    await close_db()
    logger.info("shutdown", service="triagista")


app = FastAPI(title="Triagista — SRE Triage Agent", version="0.1.0", lifespan=lifespan)


class IncidentResponse(BaseModel):
    incident_id: str
    status: str


class IncidentDetail(BaseModel):
    id: str
    title: str
    description: str
    reporter_email: str
    status: str
    severity: str
    triage_result: dict[str, object] | None = None
    confidence: float | None = None
    cost_usd: float | None = None
    created_at: str
    updated_at: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


SEVERITY_MAP = {
    "critical": IncidentSeverity.P0,
    "high": IncidentSeverity.P1,
    "medium": IncidentSeverity.P2,
    "low": IncidentSeverity.P3,
}

VALID_SEVERITY_HINTS = {"P0", "P1", "P2", "P3", "P4", "auto-detect"}


def _verify_magic_bytes(declared_mime: str, content: bytes) -> bool:
    """Verify file content matches declared MIME. Trust-but-verify.

    PNG/JPEG/PDF: check magic-byte prefix. text/plain: must decode as UTF-8.
    application/json: must parse as JSON.
    """
    if declared_mime in _MAGIC_BYTES:
        return content.startswith(_MAGIC_BYTES[declared_mime])
    if declared_mime == "text/plain":
        try:
            content.decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False
    if declared_mime == "application/json":
        try:
            json.loads(content)
            return True
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False
    return False


def _write_file(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


async def _save_upload(file: UploadFile) -> str:
    """Validate and save an uploaded file. Returns the stored path.

    Validates client-declared MIME against actual file magic bytes — the
    Content-Type header is attacker-controlled in multipart form-data.
    """
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed. Accepted: {', '.join(sorted(ALLOWED_MIMES))}",
        )
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds {MAX_FILE_SIZE // (1024 * 1024)}MB limit",
        )
    if not _verify_magic_bytes(file.content_type, content):
        raise HTTPException(
            status_code=400,
            detail=f"File content does not match declared type '{file.content_type}'",
        )
    ext = os.path.splitext(file.filename or "file")[1] or ""
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOADS_DIR, filename)
    # Run blocking I/O off the event loop.
    await asyncio.to_thread(_write_file, path, content)
    return path


async def _run_pipeline_background(incident_id: str, incident_data: dict[str, object]) -> None:
    """Run triage pipeline and update DB with result."""
    try:
        from app.db.repository import update_incident as update

        await update(incident_id, status=IncidentStatus.triaging)
        result = await run_triage_pipeline(incident_id, incident_data)

        if result["status"] == "blocked":
            await update(incident_id, status=IncidentStatus.blocked)
        elif result["status"] == "completed":
            from app.agent.classify import Classification
            from app.agent.triage import TriageResult

            triage = result.get("triage")
            classification = result.get("classification")
            severity_key = (
                classification.severity
                if isinstance(classification, Classification)
                else ""
            )
            severity = SEVERITY_MAP.get(severity_key, IncidentSeverity.unknown)
            await update(
                incident_id,
                status=IncidentStatus.triaged,
                severity=severity,
                triage_result=(
                    triage.model_dump() if isinstance(triage, TriageResult) else None
                ),
            )
    except Exception:
        logger.exception("pipeline_failed", incident_id=incident_id)


@app.post("/api/incidents", status_code=202)
async def submit_incident(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    reporter_email: str = Form(...),
    severity_hint: str = Form("auto-detect"),
    files: list[UploadFile] = File(default=[]),
) -> IncidentResponse:
    """Submit an incident for triage (multipart form). Returns 202, processes in background."""
    # --- Validate reporter_email format (restored from prior EmailStr model) ---
    try:
        validated_email = _EMAIL_ADAPTER.validate_python(reporter_email)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid reporter_email format") from None

    # --- Guardrails: check title + description before anything else ---
    title_check = check_input_safety(title)
    desc_check = check_input_safety(description)
    all_matched = title_check["matched"] + desc_check["matched"]
    if all_matched:
        raise HTTPException(
            status_code=400,
            detail=f"Input blocked by guardrails: {', '.join(all_matched)}",
        )

    # Use sanitized text from guardrails
    clean_title = str(title_check["sanitized"])
    clean_description = str(desc_check["sanitized"])

    # Validate severity hint
    if severity_hint not in VALID_SEVERITY_HINTS:
        raise HTTPException(status_code=400, detail=f"Invalid severity_hint. Must be one of: {', '.join(sorted(VALID_SEVERITY_HINTS))}")

    # --- File uploads ---
    attachment_paths: list[str] = []
    for file in files:
        path = await _save_upload(file)
        attachment_paths.append(path)

    # --- Persist ---
    incident_id = uuid.uuid4().hex[:8]
    await create_incident(
        incident_id=incident_id,
        title=clean_title,
        description=clean_description,
        reporter_email=validated_email,
        attachments=attachment_paths or None,
    )

    incident_data: dict[str, object] = {
        "title": clean_title,
        "description": clean_description,
        "reporter_email": validated_email,
        "severity_hint": severity_hint,
        "attachments": attachment_paths,
    }
    background_tasks.add_task(_run_pipeline_background, incident_id, incident_data)

    return IncidentResponse(incident_id=incident_id, status="processing")


@app.get("/api/incidents")
async def get_incidents(
    status: IncidentStatus | None = None, limit: int = 50
) -> list[IncidentDetail]:
    """List incidents, optionally filtered by status."""
    incidents = await list_incidents(status=status, limit=limit)
    return [
        IncidentDetail(
            id=i.id,
            title=i.title,
            description=i.description,
            reporter_email=i.reporter_email,
            status=i.status.value,
            severity=i.severity.value,
            triage_result=i.triage_result,
            confidence=i.confidence,
            cost_usd=i.cost_usd,
            created_at=i.created_at.isoformat() if i.created_at else "",
            updated_at=i.updated_at.isoformat() if i.updated_at else "",
        )
        for i in incidents
    ]


@app.get("/api/incidents/{incident_id}")
async def get_incident_detail(incident_id: str) -> IncidentDetail:
    """Get a single incident by ID."""
    incident = await get_incident(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentDetail(
        id=incident.id,
        title=incident.title,
        description=incident.description,
        reporter_email=incident.reporter_email,
        status=incident.status.value,
        severity=incident.severity.value,
        triage_result=incident.triage_result,
        confidence=incident.confidence,
        cost_usd=incident.cost_usd,
        created_at=incident.created_at.isoformat() if incident.created_at else "",
        updated_at=incident.updated_at.isoformat() if incident.updated_at else "",
    )
