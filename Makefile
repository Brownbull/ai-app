.PHONY: up down build test lint types check health logs clean deploy

# ── Local Dev ──────────────────────────────────────

up: ## Start all services (build if needed)
	docker compose up --build -d

down: ## Stop all services
	docker compose down

build: ## Rebuild without starting
	docker compose build

logs: ## Tail backend logs
	docker compose logs -f backend

health: ## Check backend health
	@curl -sf http://localhost:8000/health && echo " ✅" || echo " ❌"

# ── Quality ────────────────────────────────────────

test: ## Run pytest
	VIRTUAL_ENV= uv run pytest tests/ -v

lint: ## Run ruff linter
	VIRTUAL_ENV= uv run ruff check app/

types: ## Run mypy strict
	VIRTUAL_ENV= uv run mypy app/

check: lint types test ## Run all quality checks

# ── Deploy ─────────────────────────────────────────

deploy: check ## Build, verify, then deploy
	docker compose down
	docker compose up --build -d
	@echo "Waiting for backend..."
	@sleep 5
	@curl -sf http://localhost:8000/health && echo " ✅ Deploy OK" || echo " ❌ Deploy FAILED"

# ── Cleanup ────────────────────────────────────────

clean: ## Stop services and remove volumes
	docker compose down -v

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
