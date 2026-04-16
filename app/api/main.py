"""FastAPI application — intake + stream endpoints."""

import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from app.agent.pipeline import run_triage_pipeline
from app.db.config import close_db, init_db
from app.db.models import IncidentSeverity, IncidentStatus
from app.db.repository import create_incident, get_incident, list_incidents

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("starting", service="triagista")
    await init_db()
    yield
    await close_db()
    logger.info("shutdown", service="triagista")


app = FastAPI(title="Triagista — SRE Triage Agent", version="0.1.0", lifespan=lifespan)


class IncidentRequest(BaseModel):
    title: str
    description: str
    reporter_email: EmailStr
    attachments: list[str] = []


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
    request: IncidentRequest, background_tasks: BackgroundTasks
) -> IncidentResponse:
    """Submit an incident for triage. Returns 202, processes in background."""
    incident_id = uuid.uuid4().hex[:8]

    await create_incident(
        incident_id=incident_id,
        title=request.title,
        description=request.description,
        reporter_email=request.reporter_email,
        attachments=request.attachments or None,
    )

    background_tasks.add_task(
        _run_pipeline_background, incident_id, request.model_dump()
    )

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
