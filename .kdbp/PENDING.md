# Deferred Items

| # | Date | Source | Finding | File | Scale | Priority | Impact | Times Deferred | Status |
|---|------|--------|---------|------|-------|----------|--------|----------------|--------|
| D1-trigger | 2026-04-18 | /gabe-teach T4 discussion | When adding a 2nd caller of `run_triage_pipeline` (retry worker, admin replay, cron reprocess, queue consumer), MOVE the guardrail check from `app/api/main.py` into `app/agent/pipeline.py` — don't duplicate. Ref DECISIONS.md D1. | app/agent/pipeline.py | project | medium | Skipping this lets a new caller reach the LLM without safety enforcement. | 0 | open |
