# Architecture Patterns

<!-- Project-level ledger of architecture concepts adopted in this codebase. -->
<!-- Auto-maintained by /gabe-teach arch (Step 9c.2). Human-editable. -->
<!-- Each section keyed by concept-id from ~/.claude/skills/gabe-arch/concepts/. -->

## async-background-processing (foundational · agent, web)

**Verified:** 2026-04-20 via /gabe-teach arch (score 1/2)
**Applied in:** G3 API Layer (T2)
**Why we use it:** Decouple client wait from server work — return 202, stream progress via SSE.

### Decisions around this pattern

- **2026-04-18 — D1: Guardrails enforced at the API boundary only, not inside `run_triage_pipeline`.** Cites BackgroundTask as the single-caller mechanism that justifies one-boundary enforcement.

## input-guardrails (foundational · agent, security)

**Verified:** 2026-04-21 via /gabe-teach arch (score 1/2)
**Applied in:** G1 Guardrails (T1)
**Why we use it:** Filter adversarial input before the model sees it — cheaper than filtering output, and names every blocked pattern for ops observability.

### Decisions around this pattern

- **2026-04-18 — D1: Guardrails enforced at the API boundary only, not inside `run_triage_pipeline`.** Same decision drives both this pattern and async-background-processing: one trust boundary, named rejection shape.

### Known limitations

- **Unversioned pattern set** — `app/agent/guardrails.py` has 25 named patterns but no version field on `_PATTERNS` or the SafetyResult. When pattern #26 ships, ops dashboards can't distinguish "new attack variant" from "we just deployed the pattern." Identified during /gabe-teach arch session 2026-04-21. Track remediation if observability dashboard lands (not a blocker until there's a dashboard consuming `matched_patterns`).
