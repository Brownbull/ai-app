# Human Knowledge Map

<!-- Tracks what the human (operator/architect) understands about decisions made. -->
<!-- Populated and updated by /gabe-teach. -->
<!-- Goal: the human knows WHY/WHEN/WHERE, not HOW. Architect-level, not coder-level. -->

## Gravity Wells

<!-- Architectural sections of the app. Topics anchor to a primary well. -->
<!-- Soft cap: 7 wells (Miller's number). -->
<!-- A topic that spans wells gets one primary Well + `cross` in the Tags column. -->
<!-- G0 Uncategorized is a reserved fallback for orphan topics; /gabe-teach flags it. -->
<!-- Analogy column: one-liner (5-15 words) from gabe-lens. Makes each well graspable at a glance. -->
<!-- Paths column: comma-separated globs where this well's code lives (e.g., `app/api/**, tests/api/**`). Used by brief mode for health/last-commit signals. -->
<!-- Docs column: single path to this well's docs file (e.g., `docs/wells/3-api.md`). Empty = opt-out. -->
<!-- Defined: 2026-04-16 via /gabe-teach init-wells; migrated to canonical schema 2026-04-17 -->

| # | Name | Description | Analogy | Paths | Docs | Topics (verified / pending / total) |
|---|------|-------------|---------|-------|------|--------------------------------------|
| G1 | Guardrails | Input validation + injection patterns before any LLM call | Bouncer checking IDs at the door before anyone talks to the oracle | app/agent/guardrails.py, app/agent/triage.py | docs/wells/1-guardrails.md | (1 / 0 / 1) |
| G2 | LLM Pipeline | Classify → triage orchestration, structured output, routing | Dispatch office: reads the call, tags it, routes it to the right desk | app/agent/pipeline.py, app/agent/classify.py | docs/wells/2-llm-pipeline.md | (0 / 0 / 1 skipped) |
| G3 | API Layer | HTTP surface, multipart handling, background tasks | Reception desk: takes the package, hands a receipt, processes behind the counter | app/api/** | docs/wells/3-api-layer.md | (1 / 0 / 1) |
| G4 | Data Model | Persistence, schema, migrations | Filing cabinet with strict labels that survives the office moving buildings | app/db/**, app/models/**, alembic/** | docs/wells/4-data-model.md | (0 / 0 / 0) |
| G5 | Integrations | Outbound adapters (Linear, Slack, email) | Translators, each fluent in one external service's dialect | app/integrations/** | docs/wells/5-integrations.md | (0 / 0 / 0) |
| G6 | Frontend | React dashboard + submit form, API client | Storefront glass — what users see and touch; the warehouse is elsewhere | frontend/src/** | docs/wells/6-frontend.md | (1 / 0 / 1) |

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

| # | Well | Class | Topic | Status | Tags | ArchConcepts | Last Touched | Verified Date | Score | Source |
|---|------|-------|-------|--------|------|--------------|--------------|---------------|-------|--------|
| T1 | G1 | WHY | Why 15→25 patterns + return matched pattern names | verified |  | input-guardrails | 2026-04-17 | 2026-04-17 | 1/2 | working-tree: app/agent/guardrails.py |
| T2 | G3 | WHY | Why multipart + 202 Accepted + BackgroundTask | verified |  | async-background-processing | 2026-04-18 | 2026-04-18 | 2/2 | working-tree: app/api/main.py |
| T3 | G6 | WHY | Why duplicate guardrails client-side + typed SubmitState | verified |  |  | 2026-04-18 | 2026-04-18 | 2/2 | working-tree: frontend/src/pages/SubmitPage.tsx |
| T4 | G2 | WHY | Why guardrails also run inside the pipeline | skipped |  |  | 2026-04-18 | — | — | Lesson was speculative for current single-caller codebase. Decision recorded as D1; trigger logged in PENDING.md. Pipeline-side check removed. |

<!-- Example rows:
| T1 | G1 | WHY | Why guardrails run before the LLM | verified |  | 2026-04-17 | 2026-04-17 | 2/2 | a4c9e2f |
| T2 | G3 | WHY | Why 202 Accepted + BackgroundTask | pending |  | 2026-04-17 | — | — | b1d8e3a |
| T3 | G5 | WHY | Structured logging format choice | pending | cross | 2026-04-17 | — | — | c7f2a91 |
-->

## Sessions

<!-- Append-only log of /gabe-teach runs. Enriched with wells active + plan/phase reference. -->

### 2026-04-17 — /gabe-teach topics (pre-commit, working tree)
- Wells active: G1 Guardrails, G3 API Layer, G6 Frontend (candidates)
- Commits covered: none (uncommitted working tree — 8 files, ~600 insertions)
- Plan reference: Phase 1 — Incident Submission + Guardrails (Level 2a), Phase 5/5 complete
- Presented: T1, T2, T3
- Pending: T1 (0/2 — missed observability-via-names and list-preserves-all-matches)
- Docs appended: none (pending status)

### 2026-04-17 — /gabe-teach topics (T1 retry)
- Wells active: G1 Guardrails
- Retried: T1 after overnight gap
- Verified: T1 (1/2 — Q1 solid on data-shape/telemetry; Q2 missed on dict-vs-list tradeoff, corrected inline)
- Docs appended: T1 → docs/wells/1-guardrails.md

### 2026-04-18 — /gabe-teach topics (T2)
- Wells active: G3 API Layer
- Verified: T2 (2/2 — both the split-clocks force and the check-order reasoning landed)
- Docs appended: T2 → docs/wells/3-api-layer.md

### 2026-04-18 — /gabe-teach topics (T3)
- Wells active: G6 Frontend
- Verified: T3 (2/2 — client-as-UX-optimizer and make-illegal-states-unrepresentable both landed)
- Docs appended: T3 → docs/wells/6-frontend.md
- Milestone: all 3 Phase-1 pending topics now verified across G1/G3/G6

### 2026-04-20 — /gabe-teach arch show async-background-processing
- Concept: async-background-processing (foundational · agent + web)
- Score: 1/2 — verified (weak). Q1 exact (in-memory restart loses jobs). Q2 partial (conflated persistence with delivery channel; missed wasted-round-trips cost + volume threshold).
- Tag suggestion deferred: T2 strong match (score 6) but Topics table lacks ArchConcepts column. Manual schema add + tag pending.
- STATE.md / HISTORY.md updated. Step 9c.1 (well-doc append) skipped — no tagged topics. Step 9c.2 (architecture-patterns.md) prompt pending — file does not exist.

### 2026-04-18 — /gabe-teach topics (T4 → skipped, code removed)
- Wells active: G2 LLM Pipeline
- Presented T4 "Why guardrails also run inside the pipeline"; user caught that the pipeline-side check is redundant with the API-boundary check (single caller today).
- Roadmap audit (BUILD-GUIDE-V2.md Phase 2–6): no upcoming phase introduces a second caller of `run_triage_pipeline`.
- Outcome: T4 marked skipped (lesson was speculative). Pipeline-side guardrail code removed from `app/agent/pipeline.py`. Pipeline tests for injection blocking removed (coverage already lives in `tests/test_api.py`). Decision recorded as D1 with rationale + review trigger; PENDING.md D1-trigger logged for future-caller scenario.
- Lesson for future /gabe-teach runs: don't force speculative defense-in-depth through the 6-part template when the single-caller argument hasn't matured.

### 2026-04-21 — /gabe-teach arch next → input-guardrails
- Wells active: G1 Guardrails
- Concept: input-guardrails (foundational · agent, security) — picked via adjacency rule (agent momentum, alphabetical first among unverified foundationals).
- Verified: 1/2 (Q1 clean on "which pattern fired + homogenized response"; Q2 partial — user identified observability layer notices first, missed deploy-vs-attack correlation failure that versioning specifically prevents).
- Docs updated: docs/architecture-patterns.md (new input-guardrails section + Known limitation: unversioned pattern set).
- Arch state: input-guardrails added to ~/.claude/gabe-arch/STATE.md as verified (1/2) in ai-app.
- Tag applied: T1 "Why 15→25 patterns + return matched pattern names" tagged with `input-guardrails` ArchConcept (strong match: keywords + files + commit verbs all fire).

<!-- Example:
### 2026-04-17 — /gabe-teach topics (post-commit)
- Wells active: G1 Guardrails, G2 LLM Pipeline, G3 API Layer, G4 Frontend, G5 Observability
- Commits covered: a4c9e2f, b1d8e3a, c7f2a91
- Plan reference: .kdbp/PLAN.md — "Phase 1 Level 2a" (current phase 3 of 5)
- Presented: T1, T2, T3
- Verified: T1 (score 2/2)
- Skipped: T2
- Already-known: T3 (sanity-checked)
-->

## Storyline

<!-- Generated on demand by /gabe-teach story. Lossy analogy of what's been built and why. -->
<!-- Auto-refresh trigger: 3 new archived plans since last generation. Manual: /gabe-teach story refresh. -->

_Generated: 2026-04-21 (based on 1 archived plan — Phase 1 Level 2a — + active Phase 1 Level 2b + 3 verified topics + 1 skipped topic + D1)_

Imagine building an emergency-call dispatch center from scratch. First sprint (archived Phase 1, Level 2a — "Incident Submission + Guardrails"): install the front door and the bouncer. Every incident report — title, description, file attachment — passes a 25-pattern frisk at the API boundary before anyone dials the oracle. Multipart intake, 10MB file cap, magic-byte MIME verification (no more "this .png is actually a shell script"), and `EmailStr` validation restored after a regression almost slipped through. The React storefront wired to the same back door through a typed `ApiError` class. Injection attempts waste zero tokens.

Second sprint (active Phase 1, Level 2b — "PydanticAI Agent + Structured Output"): make the translator inside the building incapable of producing gibberish. Phases 1–2 of 6 have shipped. Phase 1 upgraded `TriageResult` to the V2 canonical shape — `Literal["P0"…"P4"]`, bounded `confidence: float`, `relevant_files: list[str]`. Phase 2 instantiated the real translator: `Agent(model="anthropic:claude-sonnet-4-6", output_type=TriageResult, retries=2)` landed in `app/agent/triage_agent.py`, with system prompt + static Solidus service-map stub in `app/agent/prompts.py`. Next phases (3a → 6) wire the 4-tier fallback chain — validation retry → regex-extract JSON from prose → rule-based inference → hardcoded "route to SRE-Triage at P3" — then thread it through the pipeline, cover it in tests, and burn one real token on an evidence run. Never empty. Never crashes.

One load-bearing thesis holds the whole building together: **mechanical enforcement beats prompt instructions at every layer that matters.** Guardrails at the API trust boundary (not inside the pipeline — D1 ruled out speculative defense-in-depth; T4 "Why guardrails also run inside the pipeline" was skipped for exactly this reason). Pydantic at the LLM output contract. TypeScript `ApiError` at the UI boundary. When you can't trust instructions, enforce shape instead.

Picture a 24-hour emergency clinic. A patient stumbles in at 2am with a bleeding story — "something broke in prod." Three things have to happen, in order, or the whole clinic fails: the bouncer at the door refuses people carrying weapons, the triage nurse writes a ticket and hands it off before the next patient arrives, and the waiting room display shows what's happening so the patient doesn't panic.

Phase 1 built that clinic. The bouncer is the guardrail: 25 pattern-name checks (not just "safe/unsafe" — named patterns, so ops can see *which* attack is heating up this week). The triage nurse is the API's `202 Accepted + BackgroundTask` — the form returns a ticket in 5ms so the HTTP connection doesn't hostage a 30-second LLM call. The waiting room is the React form with typed `SubmitState`, which literally cannot render "success" and "loading" at the same time; illegal states are unrepresentable.

The load-bearing belief, visible in D1: **catch problems at one boundary, cheaply, and prove what you caught**. When we briefly built defense-in-depth inside the pipeline (T4), we deleted it — duplication across a single trust domain isn't safety, it's drift.

Run `/gabe-teach story refresh` to regenerate after the next archived plan.
