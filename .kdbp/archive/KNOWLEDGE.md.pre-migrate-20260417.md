# Human Knowledge Map

<!-- Tracks what the human (operator/architect) understands about decisions made. -->
<!-- Populated and updated by /gabe-teach. -->
<!-- Goal: the human knows WHY/WHEN/WHERE, not HOW. Architect-level, not coder-level. -->

## Gravity Wells

<!-- Architectural sections of the app. Topics anchor to wells so knowledge builds a map, not a pile. -->
<!-- Defined: 2026-04-16 via /gabe-teach init-wells -->

| ID | Name | Description | Analogy | Folders | Topics |
|----|------|-------------|---------|---------|--------|
| G1 | Guardrails | Input validation + injection patterns before any LLM call | Bouncer checking IDs at the door before anyone talks to the oracle | `app/agent/guardrails.py` | 0 |
| G2 | LLM Pipeline | Classify → triage orchestration, structured output, routing | Dispatch office: reads the call, tags it, routes it to the right desk | `app/agent/pipeline.py`, `classify.py`, `triage.py` | 0 |
| G3 | API Layer | HTTP surface, multipart handling, background tasks | Reception desk: takes the package, hands a receipt, processes behind the counter | `app/api/` | 0 |
| G4 | Data Model | Persistence, schema, migrations | Filing cabinet with strict labels that survives the office moving buildings | `app/db/`, `app/models/`, `alembic/` | 0 |
| G5 | Integrations | Outbound adapters (Linear, Slack, email) | Translators, each fluent in one external service's dialect | `app/integrations/` | 0 |
| G6 | Frontend | React dashboard + submit form, API client | Storefront glass — what users see and touch; the warehouse is elsewhere | `frontend/src/` | 0 |

## Topic Classes

| Class | Question it answers | Source |
|-------|--------------------|--------|
| **WHY** | Why did we choose this approach? | commits, PLAN.md, DECISIONS.md |
| **WHEN** | When to apply / not apply this pattern? | repeated patterns across commits |
| **WHERE** | Why does this file live here? (static gravity well) | new files + project structure conventions |

## Status Lifecycle

| Status | Meaning | Re-surfaces? |
|--------|---------|--------------|
| `pending` | Detected from changes, not yet discussed | Yes, next /gabe-teach |
| `verified` | Human answered quiz correctly (score recorded) | No, unless stale |
| `skipped` | Human deferred this session | Yes, next /gabe-teach |
| `already-known` | Human claimed prior knowledge | No |
| `stale` | Verified >90 days ago | Yes, for refresh |

## Topics

| # | Class | Topic | Well | Status | Last Touched | Verified Date | Score | Source | Tags |
|---|-------|-------|------|--------|--------------|---------------|-------|--------|------|

<!-- Example rows:
| T1 | WHY | Tier A/B knowledge promotion | verified | 2026-04-15 | 2026-04-15 | 2/2 | abc1234 |
| T2 | WHEN | Route by task not by user (U6) | pending | 2026-04-16 | — | — | def5678 |
| T3 | WHERE | Why hooks live in hooks/ not scripts/ | already-known | 2026-04-16 | — | — | def5678 |
-->

## Sessions

<!-- Append-only log of /gabe-teach runs. -->

<!-- Example:
### 2026-04-15 — /gabe-teach (post-commit)
- Commits covered: abc1234
- Presented: T1, T2
- Verified: T1 (score 2/2)
- Skipped: T2 (human wanted to defer)
-->
