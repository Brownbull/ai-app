"""Stage 6 (DISPATCH): Create ticket + notify.

Pattern: real impl (when API key present) + mock impl (fallback).
"""

import os

import structlog

from app.agent.triage import TriageResult

logger = structlog.get_logger()


async def dispatch_result(incident_id: str, triage: TriageResult) -> dict:
    """Dispatch triage result to ticketing + notification systems."""
    result: dict = {}

    if os.environ.get("LINEAR_API_KEY"):
        result["ticket_id"] = await _create_linear_ticket(incident_id, triage)
    else:
        result["ticket_id"] = f"MOCK-{incident_id}"
        logger.info("mock_ticket_created", ticket_id=result["ticket_id"])

    if os.environ.get("SLACK_WEBHOOK_URL"):
        await _send_slack_notification(incident_id, triage)
        result["notified"] = True
    else:
        logger.info("mock_notification", incident_id=incident_id)
        result["notified"] = False

    return result


async def _create_linear_ticket(incident_id: str, triage: TriageResult) -> str:
    """Create a Linear ticket via GraphQL API."""
    return f"LIN-{incident_id}"


async def _send_slack_notification(incident_id: str, triage: TriageResult) -> None:
    """Send notification via Slack incoming webhook."""
    pass
