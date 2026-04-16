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
| tests/** | skip | | |
| .kdbp/** | skip | | |