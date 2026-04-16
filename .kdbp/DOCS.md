# Documentation Tracking

# Maps source code patterns to documentation targets.
# Used by /gabe-commit CHECK 7 (doc drift).

## Agent App

| Source Pattern | Doc Target | Section | Priority |
|---|---|---|---|
| app/models/*.py | docs/architecture.md | Data Model | critical |
| app/schemas/*.py | docs/architecture.md | API Contracts | critical |
| app/api/*.py | docs/architecture.md | API Endpoints | high |
| app/agent/*.py | docs/AGENTS_USE.md | Agent Design | critical |
| app/agent/guardrails.py | docs/AGENTS_USE.md | Safety | high |
| app/integrations/*.py | docs/architecture.md | Integrations | medium |
| app/config.py | README.md | Configuration | medium |
| docker-compose.yml | README.md | Setup | medium |
| db/alembic/versions/*.py | docs/architecture.md | Data Model | high |
| tests/** | skip | | |
| .kdbp/** | skip | | |
