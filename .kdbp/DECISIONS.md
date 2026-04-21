# Architecture Decisions

| # | Date | Decision | Rationale | Alternatives Considered | Status | Review Trigger |
|---|------|----------|-----------|------------------------|--------|----------------|
| D1 | 2026-04-18 | Guardrails enforced at the API boundary only, not inside `run_triage_pipeline`. | Single caller today (`api/main.py` queues the pipeline via BackgroundTask). Duplicating the check in both places creates drift risk (two return shapes to keep in sync, dead-code rot in the unreachable branch, cognitive load — "which check is authoritative?"). Defense-in-depth is load-bearing across trust domains (firewall + OS + app auth), not within one Python process. Roadmap (BUILD-GUIDE-V2.md Phase 2–6) introduces no second caller of `run_triage_pipeline`: PydanticAI retries are intra-pipeline; SSE streaming still goes through the same API handler; multi-model routing is inside the pipeline. | Keep both (rejected: drift risk > zero benefit today). Move to pipeline only (rejected: API needs fast <5ms rejection before queueing a BackgroundTask). | active | When a second caller of `run_triage_pipeline` is added (retry worker, admin replay, cron reprocess, queue consumer). At that point MOVE the check from the API into the pipeline — don't duplicate. See PENDING D1-trigger. |

<!-- Status: active / superseded / revisit -->
<!-- BEHAVIOR.md constraints reference decision IDs: "All integrations mocked (ref D1)" -->
