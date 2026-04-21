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
