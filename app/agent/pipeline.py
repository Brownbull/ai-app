"""Triage pipeline — classify -> triage -> dispatch.

Follows Tier 9 agent checklist stages 2-6.
"""

import structlog

from app.agent.classify import classify_severity
from app.agent.triage import triage_incident
from app.integrations.dispatcher import dispatch_result

logger = structlog.get_logger()


async def run_triage_pipeline(incident_id: str, incident: dict[str, object]) -> dict[str, object]:
    """Run the full triage pipeline for an incident.

    Guardrails are enforced at the API boundary (app/api/main.py) — the single
    caller today. If a second caller is added (retry worker, admin replay, queue
    consumer), MOVE the guardrail check from the API into this function rather
    than duplicating it in both places. See DECISIONS.md D1.
    """
    log = logger.bind(incident_id=incident_id)

    # Stage 3 (CLASSIFY)
    classification = await classify_severity(incident)
    log.info("classified", severity=classification.severity, category=classification.category)

    # Stage 4 (AGENT)
    triage_result = await triage_incident(incident, classification)
    log.info("triaged", actions=len(triage_result.recommended_actions))

    # Stage 6 (DISPATCH)
    dispatch = await dispatch_result(incident_id, triage_result)
    log.info("dispatched", ticket_id=dispatch.get("ticket_id"))

    return {"status": "completed", "classification": classification, "triage": triage_result}
