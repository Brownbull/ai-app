"""Stage 4 (AGENT): Premium model for triage with tools.

Uses PydanticAI output_type for structured output (V1).
Routes to premium model for reasoning (V3).
"""

from pydantic import BaseModel

from app.agent.classify import Classification


class TriageResult(BaseModel):
    """Structured triage output — enforced by PydanticAI output_type."""

    summary: str
    root_cause_hypothesis: str
    recommended_actions: list[str]
    affected_services: list[str]
    requires_escalation: bool


async def triage_incident(incident: dict[str, object], classification: Classification) -> TriageResult:
    """Triage incident using premium model with tool access.

    MVP: Rule-based. Production: PydanticAI agent with Claude Sonnet.
    """
    return TriageResult(
        summary=f"Incident: {incident['title']} classified as {classification.severity}",
        root_cause_hypothesis="Requires investigation",
        recommended_actions=[
            f"Investigate {classification.category} systems",
            "Check recent deployments",
            "Review monitoring dashboards",
        ],
        affected_services=["unknown"],
        requires_escalation=classification.severity in ("critical", "high"),
    )
