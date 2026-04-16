"""Stage 3 (CLASSIFY): Cheap model for severity classification.

Uses PydanticAI output_type for structured output (V1).
Routes to cheap model (V3).
"""

from pydantic import BaseModel


class Classification(BaseModel):
    """Structured classification output — enforced by PydanticAI output_type."""

    severity: str  # critical, high, medium, low
    category: str  # infrastructure, application, security, performance, other
    confidence: float  # 0.0 to 1.0
    reasoning: str


async def classify_severity(incident: dict[str, object]) -> Classification:
    """Classify incident severity using cheap model.

    MVP: Rule-based fallback (step 4 in fallback chain).
    Production: PydanticAI agent with Gemini Flash.
    """
    title = str(incident.get("title", "")).lower()

    if any(word in title for word in ["down", "outage", "crash", "critical"]):
        severity = "critical"
    elif any(word in title for word in ["slow", "error", "fail"]):
        severity = "high"
    elif any(word in title for word in ["warning", "degraded"]):
        severity = "medium"
    else:
        severity = "low"

    return Classification(
        severity=severity,
        category="infrastructure",
        confidence=0.6,
        reasoning=f"Rule-based classification from title keywords: {severity}",
    )
