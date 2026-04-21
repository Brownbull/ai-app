# Deviations Log

<!-- Append-only. Logged by /gabe-execute when PLAN.md tasks vary from spec. -->
<!-- Types: scope-creep (extra change not in Scope), impl-variance (different than Description), risk-fired (Risks table item materialized), schema-interpretation (ambiguous spec resolved in-flight). -->

| Date | Phase | Task | Type | Note |
|------|-------|------|------|------|
| 2026-04-21 | 1 | T1 | schema-interpretation | PLAN.md said "keep existing fields" but BUILD-GUIDE-V2 canonical V2 spec + Phase 3b tier 4 safe default both require renamed fields (`affected_service` singular, `mitigation_steps` not `recommended_actions`, drop `summary`/`requires_escalation`). Resolved: used V2 canonical schema. Consequence: `app/agent/pipeline.py` log line needed `recommended_actions` → `mitigation_steps` rename (in-scope file, minor ripple). |
