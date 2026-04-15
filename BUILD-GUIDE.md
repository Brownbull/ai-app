# Triagista v2 — Build Guide

**What**: Rebuild the SRE triage agent from scratch using finalist-level agent engineering patterns.
**Where**: This repo (`202604-agentx`), after clearing old app code.
**How**: ECC workflow + Gabe Lens for concepts. Phase by phase, building not reading.
**Reference**: Finalist repos in `analysis/repos/` — open their code side-by-side while you build yours.

---

## Repo Cleanup (Before Starting)

### Keep
```
analysis/              ← All our research + finalist repos (reference implementations)
analysis/repos/        ← The 11 cloned finalist repos
docs/hackathon_context/← Hackathon requirements (what the agent should do)
codebase/              ← Solidus docs (target e-commerce codebase)
.kdbp/                 ← Values and behaviors (update before starting)
```

### Remove
```
app/                   ← Old naive agent code
templates/             ← Old HTMX templates
tests/                 ← Old tests
alembic/               ← Old migrations
.planning/             ← GSD planning artifacts
.venv/                 ← Old virtualenv
docker-compose.yml     ← Rebuild from scratch
Dockerfile             ← Rebuild from scratch
pyproject.toml         ← Rebuild from scratch
uv.lock                ← Rebuild from scratch
README.md              ← Will rewrite with evidence
AGENTS_USE.md          ← Will rewrite with evidence
SCALING.md             ← Will rewrite with evidence
QUICKGUIDE.md          ← Will rewrite with evidence
```

### Update CLAUDE.md
Rewrite to reflect v2 stack and approach. Remove GSD enforcement clause.

---

## Tech Stack (Decided, No Debate)

These choices are locked. No switching mid-build.

| Layer | Choice | Why (from finalist analysis) |
|-------|--------|-----|
| **Agent framework** | PydanticAI | 3 of top 5 finalists. Structured output built-in. Simple: model + tools + output_type. |
| **LLM — triage** | Claude Sonnet (Anthropic SDK) | Best at tool use + reasoning. Used by #2, #5, #10. |
| **LLM — classify** | Gemini 2.5 Flash (Google GenAI) | 40x cheaper than Sonnet. Used by #1, #3 for classification. |
| **Web framework** | FastAPI | Every finalist used it. Async, auto-docs, Pydantic integration. |
| **Database** | PostgreSQL 16 + SQLAlchemy 2.0 async | Standard. #1, #2, #5 used it. |
| **Frontend** | React 18 + Vite + TypeScript + Tailwind CSS | 8 of 11 finalists used React. Strengthens a weak point. SSE via fetch + ReadableStream. |
| **UI components** | shadcn/ui | Used by #2 (ranked 2nd). Dark theme, accessible, copy-paste components. |
| **Observability** | Langfuse (cloud free tier) | No self-hosting. Zero extra containers. |
| **Integrations** | Linear (GraphQL) + Slack (webhook) + Resend (email) | Free tiers. Real, not mocked. |
| **Docker** | 4 containers (backend + frontend + postgres + clone-solidus) | Frontend is multi-stage Nginx build. Still lean. |
| **Testing** | pytest + pytest-asyncio (backend), Vitest (frontend) | 80% coverage target. |

**Note on frontend**: React + Vite (not Next.js). Next.js adds SSR complexity you don't need for this project — the backend is FastAPI, the frontend is a pure SPA. React + Vite is what finalists #1, #4, #10, #11 used. Tailwind + shadcn/ui is what #2 used for the most polished UI. SSE streaming uses the `fetch()` + `ReadableStream` pattern from #2 (not EventSource, which only supports GET).

---

## The Build Phases

Each phase has:
- **What to build** — concrete deliverables
- **Reference** — specific finalist files to study while building
- **Concept** — what agent engineering principle you're learning
- **Checkpoint** — how to verify it works before moving on

### Phase 0A: Backend Scaffold (2 hours)

**What to build:**
- FastAPI app with health endpoint
- PostgreSQL with SQLAlchemy async + Alembic
- Incidents table (title, description, reporter_email, status, severity, attachments)
- Docker Compose (backend + postgres + clone-solidus)
- `pyproject.toml` with uv
- `.env.example`

**Reference:**
- `analysis/repos/03-agentnoob-pinpacho/src/main.py` — clean FastAPI entry point
- `analysis/repos/03-agentnoob-pinpacho/docker-compose.yml` — minimal 2-container setup
- `analysis/repos/01-solo-cszdiego/backend/app/db/` — SQLAlchemy async pattern

**Concept:** None — this is mechanical. Get the backend running fast.

**Checkpoint:**
```bash
docker compose up --build
curl http://localhost:8000/health  # → 200 OK
```

---

### Phase 0B: React Frontend Scaffold (3 hours)

**What to build:**
- React 18 + Vite + TypeScript project in `frontend/`
- Tailwind CSS 4 + shadcn/ui setup
- Dark theme (like finalists — SRE tools look better dark)
- Basic layout: sidebar nav + main content area
- Proxy API calls to FastAPI backend (Vite dev proxy or Nginx in Docker)
- Multi-stage Dockerfile: Node builder → Nginx alpine
- Add `frontend` service to docker-compose.yml

**Reference:**
- `analysis/repos/01-solo-cszdiego/frontend/` — React 18 + Vite + Tailwind, dark industrial theme
- `analysis/repos/02-team-solo-jjovalle99/frontend/` — Next.js 16 + shadcn/ui (study the component patterns, skip the Next.js parts)
- `analysis/repos/04-solo-aveleyraa/frontend/` — React 18 + Vite + custom CSS design system with CSS variables
- `analysis/repos/10-marylin-alarcon/frontend/` — React 19 + Vite + Tailwind (5 views)

**Concept: React project structure for agent UIs.** Study how the finalists structured their React apps. Common pattern: pages/ (routes), components/ (reusable), hooks/ (custom hooks like useIncidentStream), lib/ (API client). You're building a dashboard, not a consumer app — keep it simple.

**Dockerfile pattern (multi-stage):**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

**Checkpoint:**
```bash
docker compose up --build
# http://localhost:3000 → React app loads with dark theme
# http://localhost:3000 → proxied API calls reach FastAPI at :8000
```

---

### Phase 1: Incident Submission + Guardrails (4 hours)

**What to build:**
- POST /api/incidents (multipart: title, description, email, file upload)
- Guardrail scanner: 13+ regex patterns for injection detection, run BEFORE anything else
- File validation (MIME whitelist, 10MB cap)
- Return 201 with incident_id
- React: IncidentForm component (title, description, email, severity hint, file drag-drop upload)
- React: IncidentList component (dashboard showing all incidents with status badges)

**Reference:**
- `analysis/repos/03-agentnoob-pinpacho/src/api/routes.py` — clean route + BackgroundTask pattern
- `analysis/repos/03-agentnoob-pinpacho/src/middleware/guardrails.py` — 13 regex patterns
- `analysis/repos/01-solo-cszdiego/backend/app/services/guardrails.py` — 15 patterns + PII detection

**Concept: Guardrails before LLM.** Every token spent on a malicious input is wasted money. The finalists run regex patterns (<5ms) before any API call. If injection detected → HTTP 400, pipeline stops, no tokens consumed.

**Checkpoint:**
```bash
# Submit normal incident → 201
# Submit injection attempt → 400 with matched patterns
# Submit oversized file → 400
```

**Tests:** Write tests for guardrail patterns (injection caught, clean text passes, file validation).

---

### Phase 2: The PydanticAI Agent — Structured Output (4 hours)

**This is the most important phase.** This is where the v1 agent was naive and the finalists were strong.

**What to build:**
- PydanticAI agent with `output_type=TriageResult`
- TriageResult Pydantic model: severity, affected_service, root_cause_hypothesis, summary, mitigation_steps, confidence, relevant_files
- System prompt with Solidus architecture context (pre-built service map)
- Deterministic fallback chain: PydanticAI validation → retry (2x) → rule-based inference → safe default
- Agent uses Claude Sonnet for triage

**Reference (study these carefully — this is the core learning):**
- `analysis/repos/03-agentnoob-pinpacho/src/agent/triage_agent.py` — PydanticAI agent definition, output_type, tools, dependency injection
- `analysis/repos/01-solo-cszdiego/backend/app/agents/triage_agent.py` — PydanticAI + fallback to rule-based
- `analysis/repos/03-agentnoob-pinpacho/src/agent/prompts.py` — system prompt that dynamically injects service catalog

**Concept: Structured output enforcement.** v1 used prompt-based JSON parsing ("please return JSON"). v2 uses PydanticAI's `output_type` which mechanically enforces the schema. If the LLM returns something invalid, PydanticAI catches it and retries. If retries fail, the fallback chain kicks in. The user NEVER sees a blank or broken result.

```python
# The core pattern — this is what you're learning
from pydantic_ai import Agent
from pydantic import BaseModel

class TriageResult(BaseModel):
    severity: Literal["P0", "P1", "P2", "P3", "P4"]
    affected_service: str
    root_cause_hypothesis: str
    confidence: float  # 0.0-1.0
    mitigation_steps: list[str]
    relevant_files: list[str]

agent = Agent(
    model="anthropic:claude-sonnet-4-20250514",
    output_type=TriageResult,
    system_prompt=TRIAGE_SYSTEM_PROMPT,
    retries=2,
)
```

**Checkpoint:**
```bash
# Submit incident → get TriageResult JSON with all fields valid
# Submit vague incident → get result with low confidence + "SRE-Triage" routing
# Manually break LLM response (if possible) → fallback chain produces safe default
```

**Tests:** Test TriageResult validation (valid input passes, missing fields caught). Test fallback chain.

**Gabe Lens moment:** After building this, run `/gabe-lens` on "structured output enforcement" to crystallize the concept in your cognitive format. This is the #1 pattern you were missing.

---

### Phase 3: Context Engineering — Codebase Map + Search Discipline (4 hours)

**What to build:**
- Build-time script that scans Solidus codebase and generates `solidus-map.md` (service names, key files, endpoints, common failure patterns)
- Inject `solidus-map.md` into agent system prompt (~200-500 tokens)
- Agent tools: `grep_codebase(pattern)`, `read_file(path, max_lines=200)`, `list_directory(path)`
- Search discipline in system prompt: "Grep FIRST, then Read only relevant files (max 5)"
- `max_turns=15` budget on agent

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/scripts/generate-eshop-map.sh` — build-time service map generation
- `analysis/repos/02-team-solo-jjovalle99/backend/app/triage.py` — search discipline prompt + max_turns=15
- `analysis/repos/03-agentnoob-pinpacho/src/knowledge/ecommerce_context.py` — embedded service catalog with SLOs, failure patterns, team assignments
- `analysis/repos/11-agentic-tulkuns/app/services/triage.py` — tool-use loop with search_code, read_file, list_directory

**Concept: Context engineering.** Don't give the agent the entire codebase. Don't make it discover the architecture every time. Pre-compute a map, inject it once. Then constrain HOW it searches: grep first (narrow), read second (focused), max 5 files, max 15 turns. This cuts cost 5x and latency 3x compared to unconstrained tool use.

**Checkpoint:**
```bash
# Submit "checkout payment failure" → agent searches Solidus payment-related files
# Check Langfuse trace: tool calls < 15, relevant files found
# Agent output references actual Solidus file paths
```

**Tests:** Test codebase map generation. Test tool call boundaries (max_turns respected). Test that paths in output actually exist.

---

### Phase 4: Real Integrations with Graceful Degradation (3 hours)

**What to build:**
- Linear: Create issue via GraphQL API (free tier). Map severity P0→urgent, P1→high, etc.
- Slack: Send webhook to #sre-alerts with severity color-coded blocks
- Resend: Send HTML email to reporter (acknowledgment) and team (alert)
- Abstract base class for each integration → real impl + mock fallback
- If API key missing → skip silently, log warning, don't crash

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/linear.py` — raw httpx GraphQL, no SDK, retry with stamina
- `analysis/repos/02-team-solo-jjovalle99/backend/app/slack.py` — Block Kit with severity colors
- `analysis/repos/02-team-solo-jjovalle99/backend/app/email.py` — Resend SDK, HTML escaping
- `analysis/repos/04-solo-aveleyraa/backend/integrations/` — abstract TicketingService base class + mock + real

**Concept: Graceful degradation.** Every integration wrapped in try/except. Missing API key → mock fallback. API timeout → skip that notification, continue pipeline. The agent NEVER fails because Slack is down. Each integration is independently fenced.

**Checkpoint:**
```bash
# With API keys: Submit incident → real Linear ticket created, Slack message sent, email delivered
# Without API keys: Submit incident → pipeline completes, notifications logged as "skipped"
```

**Tests:** Test with mocked HTTP responses (httpx mock). Test graceful degradation (API key missing → skip).

---

### Phase 5: SSE Streaming — Show the Thinking (4 hours)

**What to build:**
- POST /api/incidents returns 202 Accepted immediately
- Triage runs in BackgroundTask
- GET /api/incidents/{id}/stream returns SSE event stream
- Events: `stage_start`, `stage_complete`, `tool_call`, `triage_result`, `error`, `done`
- Replay buffer: if browser connects late, replay all past events
- React: PipelineView component showing stages lighting up as events arrive
- React: custom `useIncidentStream` hook for SSE connection management

**Reference:**
- `analysis/repos/01-solo-cszdiego/backend/app/services/streaming.py` — asyncio.Queue + replay buffer (backend pattern)
- `analysis/repos/01-solo-cszdiego/backend/app/api/` — SSE endpoint with retry/reconnect
- `analysis/repos/02-team-solo-jjovalle99/frontend/src/hooks/use-incident-stream.ts` — **THE KEY FILE**: custom React hook for SSE on POST, handles abort, buffered events, reconnect
- `analysis/repos/02-team-solo-jjovalle99/frontend/src/components/pipeline-view.tsx` — stage-by-stage progress with collapsible triage report
- `analysis/repos/01-solo-cszdiego/frontend/src/pages/IncidentDetailPage.tsx` — live reasoning sidebar

**Concept: Stream the thinking.** The 10-30 seconds while the agent triages is the most interesting part of the demo — IF you show it. Without streaming, it's dead air. With streaming, users see: "Scanning guardrails... Loading Solidus context... Searching for payment modules... Found 3 relevant files... Generating triage..." This builds trust in the agent and is the #1 demo differentiator.

**React SSE pattern** (from #2 finalist — study `use-incident-stream.ts`):
```typescript
// Can't use EventSource (GET only). Use fetch + ReadableStream for POST + SSE:
const response = await fetch('/api/incidents', { method: 'POST', body: formData, signal });
const reader = response.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const text = decoder.decode(value);
  // Parse SSE events: "event: stage_complete\ndata: {...}\n\n"
  parseSSEEvents(text).forEach(event => dispatch(event));
}
```

**Checkpoint:**
```bash
# Submit incident → 202 → open detail page → watch stages light up in real-time
# Refresh page after triage complete → all stages shown (replay buffer works)
```

---

### Phase 6: Multi-Model Routing (3 hours)

**What to build:**
- Gemini 2.5 Flash for classification: severity + affected_service + search_paths
- Classification output constrains triage agent's search scope
- Claude Sonnet for deep triage (only searches directories from classification)
- Measure and log cost per incident (input tokens × price + output tokens × price)

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/classification.py` — Mistral Medium classification with search_paths output
- `analysis/repos/02-team-solo-jjovalle99/SCALING.md` — measured cost per incident ($0.007)
- `analysis/repos/03-agentnoob-pinpacho/src/utils/multimodal.py` — hybrid model routing (Flash 80%, Sonnet 20%)

**Concept: Route by task, not by user.** v1 offered 3 engines as user choices. v2 composes them automatically: cheap model classifies (severity, service, search paths) → expensive model triages (only within those search paths). The user never picks a model. The system optimizes cost automatically. Target: <$0.01/incident.

**Checkpoint:**
```bash
# Submit incident → Langfuse shows 2 LLM calls (classify + triage)
# Classification output includes search_paths
# Triage agent only searches within those paths
# Cost logged: should be ~$0.005-0.015
```

---

### Phase 7: Deduplication — Agent Memory (2 hours)

**What to build:**
- On new incident: compare title+description against open incidents from last 2 hours
- Similarity: SequenceMatcher on title + Jaccard on extracted services
- If >70% similar: inject prior triage as "unverified hypothesis" in agent prompt
- Agent must explicitly confirm or refute the prior hypothesis

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/dedup.py` — SequenceMatcher + Jaccard, 30-min window
- `analysis/repos/02-team-solo-jjovalle99/backend/app/prompts/` — prior context injection with guardrails ("TREAT AS UNVERIFIED")
- `analysis/repos/01-solo-cszdiego/backend/app/agents/triage_agent.py` — 48h window, cross-modal dedup

**Concept: Deduplication as memory.** This is the closest thing to "agent memory" in production SRE agents. Not a vector database — temporal comparison with hypothesis injection. The agent gets context from past incidents but is forced to verify, not blindly accept. This prevents both "I've never seen this before" AND "I'll just copy the last answer."

**Checkpoint:**
```bash
# Submit incident A about "payment timeout"
# Submit incident B about "checkout payment failing" 5 min later
# B's triage prompt includes A's result as "unverified hypothesis"
# B's output explicitly confirms or refutes A's root cause
```

---

### Phase 8: Observability + Testing + Evidence Docs (4 hours)

**What to build:**
- Langfuse cloud free tier: trace every pipeline stage (guardrail, classify, triage, dispatch, notify)
- Structured logging with incident_id context binding
- Prometheus-compatible /metrics endpoint (incidents_total, triage_duration, cost_per_incident)
- 80%+ test coverage with pytest
- Run 5 real incidents, capture traces, measure costs
- Write README, AGENTS_USE.md, SCALING.md with REAL numbers from those 5 runs

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/SCALING.md` — measured $0.007/incident, per-stage latency
- `analysis/repos/02-team-solo-jjovalle99/AGENTS_USE.md` — real trace hierarchy, real log output
- `analysis/repos/05-core-tech-expert/README.md` — Mermaid diagrams + requirement mapping

**Concept: Evidence-based documentation.** v1 docs were written from theory. v2 docs include actual Langfuse trace screenshots, measured cost per incident, real latency breakdowns. "I measured it" vs "I planned it."

**Checkpoint:**
```bash
pytest --cov=app --cov-report=term-missing  # → 80%+
# README contains real numbers
# AGENTS_USE.md contains real trace output
# SCALING.md contains measured capacity, not theoretical
```

---

## Phase Summary

| Phase | What | Hours | Key Learning |
|-------|------|-------|--------------|
| 0A | Backend Scaffold (FastAPI + DB + Docker) | 2 | Mechanical — get the API running |
| **0B** | **React Scaffold (Vite + Tailwind + shadcn/ui)** | **3** | **React project structure for agent UIs** |
| 1 | Submission + Guardrails + React Form | 4 | Guardrails before LLM + React form components |
| **2** | **PydanticAI Agent + Structured Output** | **4** | **The core: schema enforcement + fallback chain** |
| **3** | **Context Engineering + Search Discipline** | **4** | **Pre-built map + constrained tools** |
| 4 | Real Integrations + Graceful Degradation | 3 | Never crash because an API is down |
| **5** | **SSE Streaming + React PipelineView** | **5** | **useIncidentStream hook + live reasoning UI** |
| 6 | Multi-Model Routing | 3 | Route by task, measure cost |
| 7 | Deduplication as Memory | 2 | Temporal memory with hypothesis injection |
| 8 | Observability + Tests + Evidence Docs | 4 | Prove it with real numbers |
| **Total** | | **~34 hours** | |

Bold phases are the ones where the learning matters most. Those are where you should slow down, study the finalist code, and use `/gabe-lens` to crystallize the concept.

---

## How to Work Each Phase

```
1. Read this guide's phase description (2 min)
2. Open the referenced finalist file(s) side-by-side (5 min)
3. Study how they implemented it — trace the code path (10-15 min)
4. Build your version, referencing theirs (the actual work)
5. Hit the checkpoint (verify it works)
6. Write tests
7. If the concept is new: /gabe-lens [concept] to anchor understanding
8. Commit. Move to next phase.
```

**If you get stuck**: Don't switch to a different approach. Read the finalist implementation again. The answer is in their code, not in a new tool.

**If you get tempted to redesign**: Remember U4 — Stay in the Friction. The discomfort IS the learning. Push through.

---

## Commands You'll Use

| When | Command | Why |
|------|---------|-----|
| Project start | `/gabe-align init triagista-v2` | Set up KDBP for the new build |
| Concept is unclear | `/gabe-lens [concept]` | Translate concept to your cognitive format |
| Before scope change | `/gabe-assess [change]` | Prevent 8-hour detours |
| Before commit | Git commit (hook fires automatically) | Checkpoint evaluates values against diff |
| Before merge/push | `/gabe-review` | Catch quality issues + deferred items |
| When confused about tools | `/gabe-help` | Shows what to use in current situation |
