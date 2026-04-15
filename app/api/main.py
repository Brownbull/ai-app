"""FastAPI application — intake + stream endpoints."""

import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.pipeline import run_triage_pipeline

app = FastAPI(title="SRE Triage Agent", version="0.1.0")


class IncidentRequest(BaseModel):
    title: str
    description: str
    reporter_email: str
    attachments: list[str] = []


class IncidentResponse(BaseModel):
    incident_id: str
    status: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/incidents", status_code=202)
async def create_incident(request: IncidentRequest) -> IncidentResponse:
    """Stage 1 (INTAKE): Validate input, assign ID, return 202 Accepted."""
    incident_id = str(uuid.uuid4())[:8]
    await run_triage_pipeline(incident_id, request.model_dump())
    return IncidentResponse(incident_id=incident_id, status="processing")
