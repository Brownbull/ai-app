# Triagista — Build Guide (From Scratch)

**What**: Build an SRE triage agent from scratch, climbing the Agent Engineering Maturity Model level by level.
**Where**: This repo (`ai-app`), building fresh.
**How**: Phase by phase. Each phase maps to a maturity level. Build, verify, learn.
**Reference**: Finalist repos at `/home/khujta/projects/hackathon/202604-agentx/analysis/repos/` — open their code side-by-side while you build.
**Analysis**: Maturity model docs at `/home/khujta/projects/hackathon/202604-agentx/analysis/agent-engineering/`
**Codebase**: Solidus e-commerce docs at `/home/khujta/projects/hackathon/202604-agentx/codebase/`

---

## Dual Purpose

This build has two goals:

1. **Learn agent engineering levels** — each phase introduces a maturity level capability (structured output, context engineering, multi-model routing, etc.). The BUILD-GUIDE maps directly to the [Agent Engineering Maturity Model](../hackathon/202604-agentx/analysis/agent-engineering/000-overview.md).

2. **Validate the suite and stack** — test whether KDBP + Gabe Suite + ECC workflow + the chosen tech stack (PydanticAI, FastAPI, React, etc.) work well for building agent applications. The [ROAST](../hackathon/202604-agentx/analysis/agent-engineering/ROAST-AGENT-ENGINEERING-TOOLING.md) identified gaps — this build reveals whether the fixes hold.

---

## Tech Stack (Locked)

| Layer | Choice | Why (from finalist analysis) |
|-------|--------|-----|
| **Agent framework** | PydanticAI | 3 of top 5 finalists. Structured output built-in. |
| **LLM — triage** | Claude Sonnet (Anthropic SDK) | Best at tool use + reasoning. |
| **LLM — classify** | Gemini 2.5 Flash (Google GenAI) | 40x cheaper than Sonnet. |
| **Web framework** | FastAPI | Every finalist used it. Async, auto-docs, Pydantic native. |
| **Database** | PostgreSQL 16 + SQLAlchemy 2.0 async | Standard. Top finalists used it. |
| **Frontend** | React 18 + Vite + TypeScript + Tailwind CSS | 8 of 11 finalists used React. |
| **UI components** | shadcn/ui | Dark theme, accessible, copy-paste. |
| **Observability** | Langfuse (cloud free tier) | No self-hosting. Zero extra containers. |
| **Integrations** | Linear (GraphQL) + Slack (webhook) + Resend (email) | Free tiers. Real, not mocked. |
| **Docker** | 4 containers (backend + frontend + postgres + clone-solidus) | Lean. |
| **Testing** | pytest + pytest-asyncio (backend), Vitest (frontend) | 80% coverage target. |

---

## Maturity Level Map

Each phase maps to a level from the [Agent Engineering Maturity Model](../hackathon/202604-agentx/analysis/agent-engineering/000-overview.md):

```
Phase 0A-0B  →  Scaffold (no level — mechanical setup)
Phase 1-2    →  Level 2: Structured Agent (output enforcement, guardrails, fallbacks)
Phase 3      →  Level 3: Context-Engineered (service map, tool discipline, scoping)
Phase 4-6    →  Level 4: Production Pipeline (multi-model, integrations, streaming, observability)
Phase 7      →  Level 4+: Temporal Memory (deduplication, hypothesis injection)
Phase 8      →  Level 4 Complete (evidence-based docs, real measurements)
```

---

## The Build Phases

Each phase has:
- **What to build** — concrete deliverables
- **Maturity level** — which level capability this teaches
- **Reference** — specific finalist files to study (paths relative to hackathon repo)
- **Checkpoint** — how to verify before moving on

### Phase 0A: Backend Scaffold

**What to build:**
- FastAPI app with health endpoint
- PostgreSQL with SQLAlchemy async + Alembic migrations
- Incidents table (id, title, description, reporter_email, status, severity, attachments, created_at, updated_at)
- Docker Compose (backend + postgres)
- `pyproject.toml` with uv
- `.env.example` with all required vars

**Starting point:** We have a FastAPI app skeleton with health endpoint, guardrails, rule-based classify/triage stubs, and basic tests. Phase 0A adds the database layer and Docker infrastructure that's missing.

**Reference:**
- `analysis/repos/03-agentnoob-pinpacho/src/main.py` — clean FastAPI entry point
- `analysis/repos/03-agentnoob-pinpacho/docker-compose.yml` — minimal 2-container setup
- `analysis/repos/01-solo-cszdiego/backend/app/db/` — SQLAlchemy async pattern

**Maturity level:** None — mechanical setup.

**Checkpoint:**
```bash
docker compose up --build
curl http://localhost:8000/health  # → 200 OK
# DB connected, migrations applied
```

---

### Phase 0B: React Frontend Scaffold

**What to build:**
- React 18 + Vite + TypeScript in `frontend/`
- Tailwind CSS 4 + shadcn/ui
- Dark theme
- Basic layout: sidebar nav + main content area
- Proxy API calls to FastAPI backend
- Multi-stage Dockerfile: Node builder → Nginx alpine
- Add `frontend` service to docker-compose.yml

**Reference:**
- `analysis/repos/01-solo-cszdiego/frontend/` — React 18 + Vite + Tailwind
- `analysis/repos/02-team-solo-jjovalle99/frontend/` — shadcn/ui component patterns
- `analysis/repos/10-marylin-alarcon/frontend/` — React 19 + Vite + Tailwind

**Maturity level:** None — mechanical setup.

**Checkpoint:**
```bash
docker compose up --build
# http://localhost:3000 → React app with dark theme
# API calls proxied to backend at :8000
```

---

### Phase 1: Incident Submission + Guardrails (Level 2a)

**What to build:**
- POST /api/incidents (multipart: title, description, email, file upload)
- Guardrail scanner: 13+ regex patterns for injection detection, run BEFORE anything
- File validation (MIME whitelist, 10MB cap)
- Return 201 with incident_id, persist to database
- React: IncidentForm component (title, description, email, severity hint, file drag-drop)
- React: IncidentList component (dashboard showing all incidents with status badges)

**Starting point:** We have guardrails (15 regex patterns) and tests. Phase 1 adds file upload, DB persistence, and the React components.

**Reference:**
- `analysis/repos/03-agentnoob-pinpacho/src/api/routes.py` — route + BackgroundTask pattern
- `analysis/repos/03-agentnoob-pinpacho/src/middleware/guardrails.py` — 13 regex patterns
- `analysis/repos/01-solo-cszdiego/backend/app/services/guardrails.py` — 15 patterns + PII detection

**Maturity level:** Level 2 — guardrails before LLM. Every token on a malicious input is wasted money.

**Concept:** _Guardrails before LLM._ Run regex patterns (<5ms) before any API call. Injection detected → HTTP 400, pipeline stops, zero tokens consumed.

**Checkpoint:**
```bash
# Submit normal incident → 201, persisted to DB
# Submit injection attempt → 400 with matched patterns
# Submit oversized file → 400
```

**Tests:** Guardrail patterns (injection caught, clean text passes, file validation).

---

### Phase 2: PydanticAI Agent — Structured Output (Level 2b)

**This is the most important phase.** This is the core Level 2 capability.

**What to build:**
- PydanticAI agent with `output_type=TriageResult`
- TriageResult: severity (P0-P4), affected_service, root_cause_hypothesis, summary, mitigation_steps, confidence (0-1), relevant_files
- System prompt with Solidus architecture context (pre-built service map)
- Deterministic fallback chain: PydanticAI validation → retry (2x) → rule-based inference → safe default
- Agent uses Claude Sonnet for triage

**Starting point:** We have a TriageResult model and rule-based stub. Phase 2 replaces the stub with a real PydanticAI agent.

**Reference:**
- `analysis/repos/03-agentnoob-pinpacho/src/agent/triage_agent.py` — PydanticAI agent, output_type, tools, DI
- `analysis/repos/01-solo-cszdiego/backend/app/agents/triage_agent.py` — PydanticAI + fallback to rule-based
- `analysis/repos/03-agentnoob-pinpacho/src/agent/prompts.py` — system prompt with service catalog
- `analysis/agent-engineering/003-level-2-structured-agent.md` — Level 2 characteristics

**Maturity level:** Level 2 — structured output enforcement + deterministic fallback chain.

**Concept:** _Structured output enforcement._ PydanticAI's `output_type` mechanically enforces the schema. If LLM returns invalid data, PydanticAI retries. If retries fail, fallback chain kicks in. User NEVER sees blank or broken result.

```python
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
# Submit incident → TriageResult JSON with all fields valid
# Submit vague incident → result with low confidence
# Fallback chain produces safe default when LLM fails
```

**Tests:** TriageResult validation, fallback chain.

**Values check:** V1 (Enforce Output Structure) — this is where V1 lives or dies.

---

### Phase 3: Context Engineering — Codebase Map + Search Discipline (Level 3)

**What to build:**
- Build-time script that scans Solidus codebase → generates `solidus-map.md`
- Inject `solidus-map.md` into agent system prompt (~200-500 tokens)
- Agent tools: `grep_codebase(pattern)`, `read_file(path, max_lines=200)`, `list_directory(path)`
- Search discipline in system prompt: "Grep FIRST, then Read only relevant files (max 5)"
- `max_turns=15` budget on agent

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/scripts/generate-eshop-map.sh` — build-time service map
- `analysis/repos/02-team-solo-jjovalle99/backend/app/triage.py` — search discipline + max_turns=15
- `analysis/repos/03-agentnoob-pinpacho/src/knowledge/ecommerce_context.py` — embedded service catalog
- `analysis/repos/11-agentic-tulkuns/app/services/triage.py` — tool-use loop
- `analysis/agent-engineering/004-level-3-context-engineered.md` — Level 3 characteristics

**Maturity level:** Level 3 — context engineering. The quality leap.

**Concept:** _Context engineering._ Don't give the agent the entire codebase. Pre-compute a map, inject once. Constrain HOW it searches: grep first, read second, max 5 files, max 15 turns. Cuts cost 5x and latency 3x.

**Checkpoint:**
```bash
# Submit "checkout payment failure" → agent searches payment-related files
# Tool calls < 15, relevant files found
# Agent output references actual Solidus file paths
```

**Tests:** Codebase map generation, tool call boundaries, paths exist.

---

### Phase 4: Real Integrations with Graceful Degradation (Level 4a)

**What to build:**
- Linear: Create issue via GraphQL API (free tier). Map severity P0→urgent, P1→high, etc.
- Slack: Send webhook to #sre-alerts with severity color-coded blocks
- Resend: Send HTML email to reporter + team
- Abstract base class per integration → real impl + mock fallback
- If API key missing → skip silently, log warning, don't crash

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/linear.py` — raw httpx GraphQL
- `analysis/repos/02-team-solo-jjovalle99/backend/app/slack.py` — Block Kit with severity colors
- `analysis/repos/02-team-solo-jjovalle99/backend/app/email.py` — Resend SDK
- `analysis/repos/04-solo-aveleyraa/backend/integrations/` — abstract TicketingService base class

**Maturity level:** Level 4 — production pipeline (graceful degradation).

**Concept:** _Graceful degradation._ Every integration wrapped in try/except. Missing API key → mock fallback. API timeout → skip. Agent NEVER fails because Slack is down.

**Checkpoint:**
```bash
# With API keys: incident → real Linear ticket, Slack message, email
# Without API keys: pipeline completes, notifications logged as "skipped"
```

**Tests:** Mocked HTTP responses, graceful degradation.

---

### Phase 5: SSE Streaming — Show the Thinking (Level 3b + Level 4b)

**What to build:**
- POST /api/incidents returns 202 Accepted immediately
- Triage runs in BackgroundTask
- GET /api/incidents/{id}/stream returns SSE event stream
- Events: `stage_start`, `stage_complete`, `tool_call`, `triage_result`, `error`, `done`
- Replay buffer: late connections see all past events
- React: PipelineView component with stages lighting up
- React: custom `useIncidentStream` hook for SSE

**Reference:**
- `analysis/repos/01-solo-cszdiego/backend/app/services/streaming.py` — asyncio.Queue + replay buffer
- `analysis/repos/02-team-solo-jjovalle99/frontend/src/hooks/use-incident-stream.ts` — SSE hook for POST
- `analysis/repos/02-team-solo-jjovalle99/frontend/src/components/pipeline-view.tsx` — stage progress UI
- `analysis/repos/01-solo-cszdiego/frontend/src/pages/IncidentDetailPage.tsx` — live reasoning sidebar

**Maturity level:** Level 3 (streaming) + Level 4 (production readiness).

**Concept:** _Stream the thinking._ The 10-30 seconds during triage IS the demo — if you show it. Without streaming, dead air. With streaming, users see: "Scanning guardrails... Loading context... Searching files... Generating triage..." Builds trust.

**SSE pattern** (from #2 finalist):
```typescript
const response = await fetch('/api/incidents', { method: 'POST', body: formData, signal });
const reader = response.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  parseSSEEvents(decoder.decode(value)).forEach(event => dispatch(event));
}
```

**Checkpoint:**
```bash
# Submit incident → 202 → detail page → stages light up in real-time
# Refresh after complete → all stages shown (replay buffer)
```

**Values check:** V2 (Stream Progress) — this is where V2 lives or dies.

---

### Phase 6: Multi-Model Routing (Level 4c)

**What to build:**
- Gemini 2.5 Flash for classification: severity + affected_service + search_paths
- Classification output constrains triage agent's search scope
- Claude Sonnet for deep triage (only searches classified directories)
- Measure and log cost per incident

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/classification.py` — classification with search_paths
- `analysis/repos/02-team-solo-jjovalle99/SCALING.md` — measured $0.007/incident
- `analysis/repos/03-agentnoob-pinpacho/src/utils/multimodal.py` — hybrid routing

**Maturity level:** Level 4 — multi-model routing. Production cost optimization.

**Concept:** _Route by task, not by user._ Cheap model classifies → expensive model triages within scoped paths. User never picks a model. Target: <$0.01/incident.

**Checkpoint:**
```bash
# Submit incident → 2 LLM calls visible (classify + triage)
# Classification includes search_paths
# Cost logged: ~$0.005-0.015
```

**Values check:** V3 (Route by Cost) — this is where V3 lives or dies.

---

### Phase 7: Deduplication — Agent Memory (Level 4d)

**What to build:**
- Compare new incident title+description against open incidents (last 2 hours)
- Similarity: SequenceMatcher on title + Jaccard on services
- If >70% similar: inject prior triage as "unverified hypothesis" in prompt
- Agent must confirm or refute the prior hypothesis

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/backend/app/dedup.py` — SequenceMatcher + Jaccard
- `analysis/repos/01-solo-cszdiego/backend/app/agents/triage_agent.py` — 48h window dedup

**Maturity level:** Level 4 — temporal memory.

**Concept:** _Deduplication as memory._ Not a vector database — temporal comparison + hypothesis injection. Agent gets context from past incidents but is forced to verify.

**Checkpoint:**
```bash
# Submit "payment timeout" → triaged
# Submit "checkout payment failing" 5 min later → includes prior hypothesis
# Second triage explicitly confirms or refutes first
```

---

### Phase 8: Observability + Testing + Evidence Docs (Level 4 Complete)

**What to build:**
- Langfuse cloud: trace every pipeline stage
- Structured logging with incident_id context binding
- /metrics endpoint (incidents_total, triage_duration, cost_per_incident)
- 80%+ test coverage with pytest
- Run 5 real incidents, capture traces, measure costs
- Write docs with REAL numbers

**Reference:**
- `analysis/repos/02-team-solo-jjovalle99/SCALING.md` — measured $0.007/incident
- `analysis/repos/02-team-solo-jjovalle99/AGENTS_USE.md` — real traces
- `analysis/repos/05-core-tech-expert/README.md` — Mermaid + requirement mapping

**Maturity level:** Level 4 complete — evidence-based documentation.

**Concept:** _Evidence-based documentation._ Docs include actual Langfuse traces, measured cost, real latency. "I measured it" vs "I planned it."

**Checkpoint:**
```bash
pytest --cov=app --cov-report=term-missing  # → 80%+
# README contains real numbers from real runs
```

**Values check:** V4 (Measure Every Run) — this is where V4 lives or dies.

---

## Phase Summary

| Phase | What | Maturity Level | Key Learning |
|-------|------|----------------|--------------|
| 0A | Backend Scaffold | — | Get API + DB running |
| 0B | React Frontend | — | SPA structure for agent UIs |
| 1 | Submission + Guardrails | **Level 2a** | Guardrails before LLM |
| **2** | **PydanticAI Agent** | **Level 2b** | **Schema enforcement + fallback chain** |
| **3** | **Context Engineering** | **Level 3** | **Pre-built map + constrained tools** |
| 4 | Integrations | Level 4a | Graceful degradation |
| **5** | **SSE Streaming** | **Level 3b/4b** | **Stream the thinking** |
| 6 | Multi-Model Routing | Level 4c | Route by task, measure cost |
| 7 | Dedup as Memory | Level 4d | Temporal memory + hypothesis injection |
| 8 | Observability + Docs | Level 4 ✓ | Prove it with real numbers |

Bold = phases where learning matters most. Slow down, study finalist code.

---

## How to Work Each Phase

```
1. Read this guide's phase description
2. Open the referenced finalist file(s) side-by-side
3. Study how they implemented it — trace the code path
4. Build your version, referencing theirs
5. Hit the checkpoint (verify it works)
6. Write tests
7. Commit. Move to next phase.
```

---

## Project Values Validation Matrix

Each value (V1-V4) is validated by a specific phase:

| Value | Phase | Validated When |
|-------|-------|----------------|
| V1 — Enforce Output Structure | Phase 2 | PydanticAI output_type works, fallback chain catches failures |
| V2 — Stream Progress | Phase 5 | SSE events flow, PipelineView lights up stages |
| V3 — Route by Cost | Phase 6 | Gemini classifies, Sonnet triages, cost < $0.01 |
| V4 — Measure Every Run | Phase 8 | Real numbers in docs from real runs |

---

## Reference Paths

All reference material lives in the hackathon repo:

```
/home/khujta/projects/hackathon/202604-agentx/
├── analysis/
│   ├── agent-engineering/     ← Maturity model (000-009), BUILD-GUIDE original
│   ├── repos/                 ← 13 finalist repos (code to study)
│   ├── hackathon/             ← Retrospective + finalist analysis
│   ├── ai-suite/              ← KDBP learnings, Gabe analysis
│   └── ai-stack/              ← Stack decisions
├── codebase/                  ← Solidus docs (target e-commerce)
└── docs/hackathon_context/    ← Original assignment + requirements
```
