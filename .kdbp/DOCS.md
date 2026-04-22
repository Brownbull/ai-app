# Documentation Tracking

# Maps source code patterns to documentation targets.
# Used by /gabe-commit CHECK 7 (doc drift).

## Agent App

| Source Pattern | Doc Target | Section | Priority |
|---|---|---|---|
| app/db/models.py | docs/architecture.md | Data Model | critical |
| app/db/config.py | docs/architecture.md | Data Model | high |
| app/db/repository.py | docs/architecture.md | Data Model | high |
| app/api/main.py | docs/architecture.md | API Endpoints | critical |
| app/agent/*.py | docs/AGENTS_USE.md | Agent Design | critical |
| app/agent/guardrails.py | docs/AGENTS_USE.md | Safety | high |
| app/agent/pipeline.py | docs/AGENTS_USE.md | Agent Design | critical |
| app/integrations/*.py | docs/architecture.md | Integrations | medium |
| alembic/versions/*.py | docs/architecture.md | Data Model | high |
| docker-compose.yml | README.md | Setup | medium |
| Dockerfile | README.md | Setup | medium |
| pyproject.toml | README.md | Setup | low |
| .env.example | README.md | Configuration | medium |
| Makefile | README.md | Setup | medium |
| Dockerfile | README.md | Setup | medium |
| frontend/Dockerfile | README.md | Setup | medium |
| frontend/nginx.conf | README.md | Setup | low |
| frontend/package.json | README.md | Setup | low |
| alembic.ini | docs/architecture.md | Data Model | low |
| alembic/env.py | docs/architecture.md | Data Model | low |
| tests/** | skip | | |
| .kdbp/** | skip | | |
| app/__init__.py | skip | | |
| frontend/vite.config.ts | skip | | |
| alembic/script.py.mako | skip | | |
| frontend/eslint.config.js | skip | | |
| frontend/index.html | skip | | |
| frontend/package-lock.json | skip | | |
| frontend/tsconfig*.json | skip | | |
| frontend/public/*.svg | skip | | |
| frontend/.gitignore | skip | | |
| uv.lock | skip | | |
| .gitignore | skip | | |

## Meta / Reference Docs

Docs not tracked against live code. Listed here as Doc Targets with a self-referential
source pattern so the orphaned-doc audit (Step A4) stops flagging them. These rows
will never fire under per-diff CHECK 7 — the source pattern is the doc itself, which
is a doc not a code file, so it's never touched by code diffs.

| Source Pattern | Doc Target | Section | Priority |
|---|---|---|---|
| docs/BUILD-GUIDE-V2.md | docs/BUILD-GUIDE-V2.md | - | low |
| docs/SCALING.md | docs/SCALING.md | - | low |
| app/agent/** | docs/architecture-patterns.md | - | low |
| docs/archive/** | docs/archive/BUILD-GUIDE-v1.md | - | low |
| docs/archive/gabe-teach-v2-dogfood.md | docs/archive/gabe-teach-v2-dogfood.md | - | low |
| docs/archive/gabe-teach-v2-patch.md | docs/archive/gabe-teach-v2-patch.md | - | low |
| docs/references/** | docs/references/agent-engineering/000-overview.md | - | low |
| docs/references/** | docs/references/agent-engineering/001-architecture-taxonomy.md | - | low |
| docs/references/** | docs/references/agent-engineering/002-level-1-prompt-and-parse.md | - | low |
| docs/references/** | docs/references/agent-engineering/003-level-2-structured-agent.md | - | low |
| docs/references/** | docs/references/agent-engineering/004-level-3-context-engineered.md | - | low |
| docs/references/** | docs/references/agent-engineering/005-level-4-production-pipeline.md | - | low |
| docs/references/** | docs/references/agent-engineering/006-level-5-autonomous-investigation.md | - | low |
| docs/references/** | docs/references/agent-engineering/007-beyond-level-5.md | - | low |
| docs/references/** | docs/references/agent-engineering/008-anti-patterns.md | - | low |
| docs/references/** | docs/references/agent-engineering/009-implementation-roadmap.md | - | low |