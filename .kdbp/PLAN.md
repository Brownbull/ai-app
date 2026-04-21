# Active Plan

<!-- status: active -->

## Goal

Phase 2 — PydanticAI Agent — Structured Output (Level 2b): replace rule-based triage stub with PydanticAI agent enforcing `output_type=TriageResult`, backed by a 4-tier deterministic fallback chain (validation+retry → regex JSON extract → rule-based inference → safe default). Claude Sonnet. This is where V1 (Enforce Output Structure) lives or dies.

## Context

- **Maturity:** mvp
- **Domain:** SRE triage agent that classifies incidents, creates tickets, and notifies teams
- **Level:** 2b — structured output enforcement + fallback chain ("never empty, never crash")
- **Created:** 2026-04-20
- **Last Updated:** 2026-04-21 (Phase 1 exec started)

## Phases

| # | Phase | Description | Complexity | Exec | Review | Commit | Push |
|---|-------|-------------|------------|------|--------|--------|------|
| 1 | Upgrade TriageResult schema | Align `app/agent/triage.py` TriageResult to V2 spec: `severity: Literal["P0","P1","P2","P3","P4"]`, add `confidence: float`, `relevant_files: list[str]`; keep existing fields. | low | 🔄 | ⬜ | ⬜ | ⬜ |
| 2 | PydanticAI triage agent | New `app/agent/triage_agent.py`: `Agent(model="anthropic:claude-sonnet-4-6", output_type=TriageResult, retries=2)`. System prompt in `app/agent/prompts.py` with static Solidus service-map stub (dynamic map = Phase 3). Env-var API key via existing settings. Add `pydantic-ai` to `pyproject.toml`. | medium | ⬜ | ⬜ | ⬜ | ⬜ |
| 3a | Fallback tier 2 — regex JSON extract | Wrapper catches PydanticAI validation exhaustion, runs `re.search(r'\{.*\}', text, re.DOTALL)` on last raw response, feeds to `TriageResult.model_validate_json`. Returns structured result if parse succeeds. | low | ⬜ | ⬜ | ⬜ | ⬜ |
| 3b | Fallback tier 3+4 — rule-based + safe default | Tier 3: current rule-based `triage_incident` logic promoted to wrapper fallback (keyword inference from title/description). Tier 4: hardcoded safe default — `severity=P3`, `affected_service="unknown"`, `root_cause_hypothesis="Requires investigation"`, `mitigation_steps=["Route to SRE-Triage team"]`, `confidence=0.0`. Never raises. | low | ⬜ | ⬜ | ⬜ | ⬜ |
| 4 | Wire into pipeline | `app/agent/pipeline.py`: replace direct `triage_incident` call with wrapper `run_triage(incident, classification)`. Log which tier fired via structlog `tier=1|2|3|4`. Classify stays rule-based (Phase 6 routes classify to cheap model). | low | ⬜ | ⬜ | ⬜ | ⬜ |
| 5 | Tests | `tests/test_triage_agent.py`: schema validation (valid Pydantic input passes, missing fields rejected). Fallback chain: mock agent raises `ValidationError` → tier 2 fires; mock returns malformed text with embedded JSON → tier 2 succeeds; mock returns plain English → tier 3 fires; mock raises exhaustively → tier 4 fires. E2E pipeline test with mocked agent. No real LLM calls in automated tests. | medium | ⬜ | ⬜ | ⬜ | ⬜ |
| 6 | Evidence run + measurement stub | One real call end-to-end (guarded behind `PYTEST_REAL_LLM=1` env flag); capture cost/latency/tokens via structlog; record numbers in phase notes + `docs/wells/2-llm-pipeline.md`. Groundwork for V4 full observability (Phase 8). | low | ⬜ | ⬜ | ⬜ | ⬜ |

<!-- Exec written by /gabe-execute: ⬜ not started, 🔄 in progress, ✅ complete -->
<!-- Review/Commit/Push auto-ticked by /gabe-review, /gabe-commit, /gabe-push -->
<!-- A phase is complete when all four columns are ✅ -->
<!-- /gabe-next routes to the next command based on column state -->

## Current Phase

Phase 1: Upgrade TriageResult schema

## Dependencies

- Phase 2 depends on Phase 1 (agent consumes new schema)
- Phase 3a depends on Phase 2 (wrapper catches agent exhaustion)
- Phase 3b depends on Phase 3a (chain tiers wire in order)
- Phase 4 depends on Phase 3b (pipeline calls the complete wrapper)
- Phase 5 depends on Phase 4 (tests exercise the wired path)
- Phase 6 depends on Phase 5 (real call only after tests green)

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| ANTHROPIC_API_KEY not configured → dev blocked | medium | Fallback chain always produces result; dev works without key until Phase 6 evidence run. |
| Cost runaway in test suite | medium | Mock agent in all automated tests; real call gated by `PYTEST_REAL_LLM=1` env flag. |
| TriageResult schema breaking change | low | MVP — no external consumers; frontend dashboard renders whatever shape; update fixtures in tests/ only. |
| Prompt injection via title/description | low | Guardrails enforce at API boundary (D1) — agent only sees vetted input. |
| PydanticAI version pin drift | low | Lock version in `pyproject.toml`; document pin in Notes. |
| Regex JSON extract greedy match swallows trailing garbage | low | Use non-greedy + validate via Pydantic; if fails, tier 3 catches it. Deterministic degradation. |

## Values Check

- **V1 — Enforce Output Structure** ✅ Core of this phase. PydanticAI `output_type` = mechanical enforcement; fallback chain guarantees valid shape even on LLM failure.
- **V2 — Stream Progress** — deferred to Phase 5 (SSE).
- **V3 — Route by Cost** — partial: triage uses premium Sonnet. Classify stays rule-based. Full V3 = Phase 6.
- **V4 — Measure Every Run** — groundwork in step 6 (single evidence run logs cost/latency/tokens). Full V4 = Phase 8.

## Scope

- **Modified:** `app/agent/triage.py` (schema), `app/agent/pipeline.py` (wire), `tests/test_pipeline.py` (update fixtures), `pyproject.toml` (add `pydantic-ai`)
- **New:** `app/agent/triage_agent.py` (agent + fallback wrapper), `app/agent/prompts.py` (system prompt + service-map stub), `tests/test_triage_agent.py`
- **~400 lines**
- **No schema migrations** (Phase 2 is in-process only; DB tables unchanged)

## Checkpoint

```bash
# 1. Normal incident → TriageResult JSON, severity P0-P4, all fields present
# 2. ANTHROPIC_API_KEY unset → tier 2/3/4 fires depending on what PydanticAI raises
# 3. Mocked malformed LLM response → tier 2 regex extract succeeds
# 4. Mocked plain-English response → tier 3 rule-based fires
# 5. Mocked exhaustive failure → tier 4 safe default returns P3 + SRE-Triage
# 6. PYTEST_REAL_LLM=1 single run → cost/latency/tokens logged
```

## References

- `docs/BUILD-GUIDE-V2.md` Phase 2 (lines 150-204) — canonical scope
- `docs/references/agent-engineering/003-level-2-structured-agent.md` — Level 2 characteristics + 4-tier fallback diagram
- `docs/references/agent-engineering/009-implementation-roadmap.md` — Step 1 (Structured Output) + Step 4 (Fallback Chain) of the 10-step climb
- `analysis/repos/03-agentnoob-pinpacho/src/agent/triage_agent.py` — PydanticAI agent, `output_type`, tools, DI (reference impl)
- `analysis/repos/01-solo-cszdiego/backend/app/agents/triage_agent.py` — PydanticAI + rule-based fallback (reference impl)
- `analysis/repos/03-agentnoob-pinpacho/src/agent/prompts.py` — system prompt with service catalog (reference impl)

## Notes

- 4-tier fallback chain is explicit per roadmap 009 + level-2 003: **never return empty, never crash**. Every incident gets usable triage.
- Safe default (tier 4): severity=P3, team=SRE-Triage. Conservative middle-ground routing.
- Classify stage stays rule-based this phase. V3 cost routing (Phase 6) swaps classify to cheap model (Gemini Flash or Haiku).
- Static service-map stub in system prompt is acceptable for Phase 2. Dynamic codebase-scan map = Phase 3.
- Evidence run is gated behind `PYTEST_REAL_LLM=1` so CI never burns tokens unintentionally.
- PydanticAI built-in `retries=2` counts as tier 1; wrapper handles tiers 2-4 after exhaustion.
