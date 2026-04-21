"""Stage 4 (AGENT): Premium model for triage with tools.

Uses PydanticAI output_type for structured output (V1).
Routes to premium model for reasoning (V3).
"""

from typing import Literal

from pydantic import BaseModel, Field

from app.agent.classify import Classification

Severity = Literal["P0", "P1", "P2", "P3", "P4"]

_CLASSIFY_TO_SEVERITY: dict[str, Severity] = {
    "critical": "P0",
    "high": "P1",
    "medium": "P2",
    "low": "P3",
}


class TriageResult(BaseModel):
    """Structured triage output — enforced by PydanticAI output_type (V2 schema)."""

    severity: Severity
    affected_service: str
    root_cause_hypothesis: str
    confidence: float = Field(ge=0.0, le=1.0)
    mitigation_steps: list[str]
    relevant_files: list[str]


async def triage_incident(incident: dict[str, object], classification: Classification) -> TriageResult:
    """Triage incident using premium model with tool access.

    MVP: Rule-based stub. Phase 2 replaces this with a PydanticAI agent + fallback chain.
    """
    severity = _CLASSIFY_TO_SEVERITY.get(classification.severity, "P3")
    return TriageResult(
        severity=severity,
        affected_service=classification.category or "unknown",
        root_cause_hypothesis="Requires investigation",
        confidence=classification.confidence,
        mitigation_steps=[
            f"Investigate {classification.category} systems",
            "Check recent deployments",
            "Review monitoring dashboards",
        ],
        relevant_files=[],
    )
