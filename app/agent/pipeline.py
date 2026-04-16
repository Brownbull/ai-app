"""Triage pipeline — classify -> triage -> dispatch.

Follows Tier 9 agent checklist stages 2-6.
"""

import structlog

from app.agent.guardrails import check_input_safety
from app.agent.classify import classify_severity
from app.agent.triage import triage_incident
from app.integrations.dispatcher import dispatch_result

logger = structlog.get_logger()


async def run_triage_pipeline(incident_id: str, incident: dict[str, object]) -> dict[str, object]:
    """Run the full triage pipeline for an incident."""
    log = logger.bind(incident_id=incident_id)

    # Stage 2 (GUARDRAILS)
    safety = check_input_safety(str(incident["description"]))
    if not safety["safe"]:
        log.warning("input_blocked", reason=safety["reason"])
        return {"status": "blocked", "reason": safety["reason"]}

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
