# AI App — SRE Triage Agent

MVP agent application following the Gabe Suite + KDBP stack.

## Architecture

Pattern A (Single Agent + Deterministic Pipeline) from arch-ref-lib Tier 9.

```
INTAKE → GUARDRAILS → CLASSIFY → TRIAGE → DISPATCH
  (API)   (regex)    (Gemini)   (Claude)  (Linear+Slack)
```

## Setup

Two supported paths: **Docker Compose** (recommended — matches prod-style deploy) or **local venv** (faster dev loop, bring your own Postgres).

### Docker Compose (full stack)

```bash
cp .env.example .env            # populate optional integration keys
make up                         # alias: docker compose up --build -d
make health                     # curl-probe /health on :8000
```

Spins up three services defined in [docker-compose.yml](docker-compose.yml):

- `db` — Postgres 16-alpine with health-gated start (`pg_isready`).
- `backend` — FastAPI image built from root [Dockerfile](Dockerfile). Entrypoint runs `alembic upgrade head` then `uvicorn` on port 8000. Non-root user, healthcheck every 30s.
- `frontend` — React build served by nginx (see [frontend/Dockerfile](frontend/Dockerfile) + [frontend/nginx.conf](frontend/nginx.conf)). Exposed on :3000.

`make down` stops; `make deploy` runs full `lint + types + test` gate before rebuilding.

### Local dev (venv)

```bash
uv sync --dev                   # deps from pyproject.toml + uv.lock
uv run alembic upgrade head     # requires DATABASE_URL to a reachable Postgres
uv run uvicorn app.api.main:app --reload
```

Quality gates via Makefile: `make lint` (ruff), `make types` (mypy strict), `make test` (pytest), `make check` (all three). Frontend deps in [frontend/package.json](frontend/package.json) — `cd frontend && npm install && npm run dev`.

## Configuration

Copy `.env.example` to `.env` and populate what you need. All integration keys are optional — the pipeline runs end-to-end with zero external services configured (mock ticket + mock notification, see [docs/architecture.md#Integrations](docs/architecture.md)).

| Variable | Required? | Purpose |
|---|---|---|
| `DATABASE_URL` | yes | Async PostgreSQL DSN. Default: `postgresql+asyncpg://triagista:triagista@localhost:5432/triagista`. |
| `ANTHROPIC_API_KEY` | prod | Claude Sonnet key for triage agent. Unset = agent fails at call time (caught by Phase 3 fallback chain). |
| `GOOGLE_API_KEY` | prod | Gemini Flash key for classification. Unset = classify step uses rule-based keyword fallback. |
| `LINEAR_API_KEY` | optional | Real Linear ticket creation. Unset = mock ticket id `MOCK-{incident_id}`. |
| `LINEAR_TEAM_ID` | optional | Required when `LINEAR_API_KEY` is set. |
| `SLACK_WEBHOOK_URL` | optional | Real Slack notification. Unset = logged `mock_notification` event. |
| `RESEND_API_KEY` / `RESEND_FROM_EMAIL` | optional | Email notifications via Resend. |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST` | optional | Observability. Host default: `https://cloud.langfuse.com`. |

Source: [.env.example](.env.example). All vars are read via `os.environ.get` at call sites — startup does not hard-fail on missing optional keys.

## KDBP

This project uses the KDBP knowledge system. See `.kdbp/` for:
- `VALUES.md` — project values (V1-V4)
- `BEHAVIOR.md` — project context and maturity level
- `DECISIONS.md` — architecture decisions
- `PENDING.md` — deferred items
- `LEDGER.md` — session checkpoint history
- `MAINTENANCE.md` — quarterly checklist
