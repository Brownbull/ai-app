"""PydanticAI triage agent — Level 2b structured-output enforcement.

Phase 2 scope: just the Agent instance. `output_type=TriageResult` is the
mechanical shape guarantee (V1 — Enforce Output Structure). `retries=2` is
PydanticAI's built-in tier 1 of the fallback chain; tiers 2–4 (regex
extract, rule-based, safe default) land in Phase 3a/3b via a wrapper in
this same module.

ANTHROPIC_API_KEY is read from the process environment by PydanticAI's
Anthropic provider. When unset, constructing the Agent is still fine —
the call site fails at run-time, which is the boundary the Phase 3 wrapper
will catch.
"""

from pydantic_ai import Agent

from app.agent.prompts import TRIAGE_SYSTEM_PROMPT
from app.agent.triage import TriageResult

# Model pin: exact Sonnet 4.6 id. Do not swap without updating PLAN.md + a
# measurement run (V4). Version drift in the model silently changes cost,
# latency, and calibration.
_TRIAGE_MODEL = "anthropic:claude-sonnet-4-6"

triage_agent: Agent[None, TriageResult] = Agent(
    _TRIAGE_MODEL,
    output_type=TriageResult,
    retries=2,
    system_prompt=TRIAGE_SYSTEM_PROMPT,
)
