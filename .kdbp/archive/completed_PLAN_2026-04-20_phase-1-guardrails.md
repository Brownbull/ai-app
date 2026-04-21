# Active Plan

<!-- status: completed -->

## Goal

Phase 1 — Incident Submission + Guardrails (Level 2a): accept multipart incident submissions with file attachments, enforce expanded guardrails before any LLM call, and wire the React form end-to-end to the dashboard.

## Context

- **Maturity:** mvp
- **Domain:** SRE triage agent that classifies incidents, creates tickets, and notifies teams
- **Level:** 2a — guardrails before LLM ("every blocked injection = zero tokens wasted")
- **Created:** 2026-04-16
- **Last Updated:** 2026-04-17

## Phases

| # | Phase | Description | Complexity | Review | Commit | Push |
|---|-------|-------------|------------|--------|--------|------|
| 1 | Enhanced guardrails | Expand from 15 → ~25 patterns (role separators, token markers, SQL injection, code exec); return matched pattern names; input sanitization; 8000-char warning. | medium | ✅ | ✅ | ✅ |
| 2 | Multipart API + file upload | POST /api/incidents → multipart; MIME whitelist; 10MB cap; UUID filenames in `uploads/`; run guardrails on title+description; 202 Accepted + background task; optional `severity_hint`. | medium | ✅ | ✅ | ✅ |
| 3 | React IncidentForm | Replace SubmitPage placeholder with full form: title, description, email, severity hint, drag-drop file upload, client validation, success/error/loading states. | medium | ✅ | ✅ | ✅ |
| 4 | API client update | Add `submitIncident(data: FormData)` in `frontend/src/lib/api.ts` using multipart fetch (no Content-Type header). | low | ✅ | ✅ | ✅ |
| 5 | Tests + checkpoint | Backend tests (guardrails patterns, multipart happy/injection/oversize/bad-MIME paths, pipeline E2E); migrate fixtures to multipart; manual frontend verification of submit → dashboard flow. | medium | ✅ | ✅ | ✅ |

<!-- Review/Commit/Push auto-ticked by /gabe-review, /gabe-commit, /gabe-push -->
<!-- A phase is complete when all three columns are ✅ -->
<!-- Migrated from legacy Status column on 2026-04-16. All phases shipped to main. -->


## Current Phase

Phase 5: Tests + checkpoint — complete. All phases complete; ready to archive via `/gabe-plan` (complete) and start Phase 2 of the roadmap.

## Dependencies

- Phase 2 depends on Phase 1 (API consumes guardrails return value and formats 400 response with matched pattern names).
- Phase 3 depends on Phase 2 (form posts to the multipart endpoint).
- Phase 4 is consumed by Phase 3 (form uses the client helper).
- Phase 5 depends on Phases 1–4 (tests cover the full submission path end-to-end).

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| File storage in container is ephemeral | low | Acceptable for MVP; mount a volume later. |
| Multipart switch breaks existing JSON-fixture tests | medium | Budget ~50 lines of test-fixture migration to multipart. |
| No shadcn Form components available | low | Plain HTML + Tailwind is sufficient for a single form. |
| 202 vs 201 semantics (BUILD-GUIDE suggested 201) | low | 202 is correct for BackgroundTask async processing — documented in phase notes. |

## Scope

- 7 files modified: `app/agent/guardrails.py`, `app/agent/pipeline.py`, `app/api/main.py`, `tests/test_guardrails.py`, `tests/test_pipeline.py`, `frontend/src/pages/SubmitPage.tsx`, `frontend/src/lib/api.ts`.
- 1 new file: `tests/test_api.py` (multipart tests).
- ~300 lines across backend + frontend, including test-fixture migration.
- No new dependencies (`python-multipart` already in `pyproject.toml`).

## Checkpoint

```bash
# Submit normal incident → 202, persisted to DB
# Submit injection attempt → 400 with matched patterns
# Submit oversized file → 400
```

Frontend manual verification:
- Normal submission → 202, appears on Incidents page after background triage.
- Injection attempt → 400 with form error surfaced.
- Oversized file → client-side rejection.

## Notes

- Consolidated from the legacy `.kdbp/PLAN-PHASE-1.md` into the standard gabe-plan format on 2026-04-16 so only one active plan lives in `.kdbp/`.
- Original source defined 5 Steps; they map 1:1 to the 5 phases above.
- All phases shipped; plan remains active as the record of Phase 1 — run `/gabe-plan` and choose `[complete]` to archive when ready.

## Archived

- **Resolution:** completed
- **Date:** 2026-04-20
- **Reason:** All 5 phases shipped. Review/Commit/Push ticked across every row. Phase 1 goal achieved: multipart incident submission + expanded guardrails + React form wired end-to-end.