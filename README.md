# AI App — SRE Triage Agent

MVP agent application following the Gabe Suite + KDBP stack.

## Architecture

Pattern A (Single Agent + Deterministic Pipeline) from arch-ref-lib Tier 9.

```
INTAKE → GUARDRAILS → CLASSIFY → TRIAGE → DISPATCH
  (API)   (regex)    (Gemini)   (Claude)  (Linear+Slack)
```

## Setup

```bash
pip install -e ".[dev]"
pytest tests/
uvicorn app.api.main:app --reload
```

## KDBP

This project uses the KDBP knowledge system. See `.kdbp/` for:
- `VALUES.md` — project values (V1-V4)
- `BEHAVIOR.md` — project context and maturity level
- `DECISIONS.md` — architecture decisions
- `PENDING.md` — deferred items
- `LEDGER.md` — session checkpoint history
- `MAINTENANCE.md` — quarterly checklist
