# 004 — Level 3: Context-Engineered Agent

**The quality leap.** This is where agents stop guessing and start knowing. Context engineering — controlling exactly what information reaches the LLM and when — was the single biggest differentiator between good and great implementations.

---

## What Level 3 Looks Like

```mermaid
sequenceDiagram
    participant U as User
    participant API as API Server
    participant Guard as Guardrails
    participant Classify as Classifier
    participant Map as Service Map
    participant Agent as Triage Agent (tools)
    participant Int as Real Integrations

    U->>API: Submit incident
    API-->>U: 202 Accepted
    API->>Guard: Validate input
    Guard-->>API: Clean
    API->>Classify: Classify severity + service
    Classify->>Map: Look up service map (pre-built)
    Map-->>Classify: Affected paths, SLOs, team
    Classify-->>API: severity=P1, search_paths=[src/Payment/]

    API->>Agent: Triage with scoped context
    Note over Agent: Tools scoped to search_paths only
    Agent->>Agent: Grep("ConnectionPool", "src/Payment/")
    Agent->>Agent: Read("PaymentProcessor.cs", line 142)
    Agent-->>API: Root cause hypothesis + evidence

    API->>Int: Create ticket (Linear)
    API->>Int: Send alert (Slack)
    Int-->>API: Delivered
    API->>U: Result + ticket link
```

## The Three Pillars of Context Engineering

### Pillar 1: Static Context Injection (Build-Time)

Pre-compute codebase knowledge once. Inject as system prompt. Save 3-5 tool calls per incident.

```mermaid
flowchart LR
    subgraph "Docker Build Time"
        SCAN["Scan codebase"] --> GEN["Generate service_map.md"]
        GEN --> INJECT["Inject into system prompt"]
    end
    subgraph "Runtime (every incident)"
        INJECT --> AGENT["Agent starts with<br/>full architecture knowledge"]
        AGENT --> SAVE["Saves 3-5 tool calls<br/>~200-500 tokens once"]
    end

    style SCAN fill:#eee,stroke:#999,color:#333
    style GEN fill:#ffc,stroke:#cc3,color:#333
    style INJECT fill:#cfc,stroke:#3c3,color:#333
    style AGENT fill:#cfc,stroke:#3c3,color:#333
```

**Implementations**:
| Team | Method | Token Cost |
|------|--------|------------|
| #2 | `scripts/generate-eshop-map.sh` at Docker build | ~200 tokens |
| #3 | Python dict with SLOs + failure patterns + team mappings | ~300 tokens |
| #1 | Hardcoded service-keyword mapping + exception heuristics | ~150 tokens |

### Pillar 2: Classification-Driven Context Scoping

Cheap model classifies first. Output constrains expensive model's search space.

```mermaid
flowchart TD
    INC["Incident text"] --> CHEAP["Cheap Model<br/>(Mistral Medium, $0.40/M)"]
    CHEAP --> CLASS["Classification Output"]

    CLASS --> SEV["severity: P1"]
    CLASS --> SVC["affected_services:<br/>PaymentProcessor, Ordering.API"]
    CLASS --> PATHS["search_paths:<br/>src/PaymentProcessor/<br/>src/Ordering.API/"]

    PATHS --> CONSTRAINT["Hard constraint in triage prompt:<br/>'Search ONLY within these directories'"]
    CONSTRAINT --> EXPENSIVE["Expensive Model<br/>(Claude Sonnet, $3/M)"]

    subgraph "Without Scoping"
        W1["Agent explores entire codebase<br/>50+ tool calls<br/>3+ minutes<br/>$0.50+"]
    end

    subgraph "With Scoping"
        W2["Agent searches 2 directories<br/>~10 tool calls<br/>15-30 seconds<br/>$0.01-0.05"]
    end

    EXPENSIVE --> W2

    style W1 fill:#fcc,stroke:#c33,color:#333
    style W2 fill:#cfc,stroke:#3c3,color:#333
    style CHEAP fill:#cef,stroke:#39c,color:#333
    style EXPENSIVE fill:#ffc,stroke:#cc3,color:#333
```

**5x reduction** in both latency and cost. This is the highest-ROI technique observed.

### Pillar 3: Evidence Ranking & Bounded Context

Don't dump everything into the prompt. Rank evidence, pack the best into a bounded window.

```mermaid
flowchart TD
    GREP["Grep results<br/>(many matches)"] --> SCORE["Hybrid Scoring"]
    READ["File reads<br/>(code snippets)"] --> SCORE
    LOGS["Log entries<br/>(if available)"] --> SCORE

    SCORE --> RANK["Rank by relevance<br/>55% lexical (TF-IDF)<br/>45% dense (SVD 64-dim)"]
    RANK --> TOP["Take top-k results"]
    TOP --> PACK["Pack into bounded context<br/>(max 4000 tokens)"]
    PACK --> LLM["Send to LLM<br/>with only relevant evidence"]

    style SCORE fill:#ffc,stroke:#cc3,color:#333
    style PACK fill:#cfc,stroke:#3c3,color:#333
```

**Key insight from #5**: Used scikit-learn SVD (64-dim) + pgvector. No external embedding API. Zero dependency, fast, reproducible. For small corpora (<1000 docs), this outperforms complex embedding pipelines.

## Tool Use Discipline

Level 3 agents have tools — but with strict discipline.

### The Search Discipline: Grep-First, Read-Second

```mermaid
flowchart TD
    START["Need information"] --> Q1{Know what<br/>to search for?}
    Q1 -->|Yes| GREP["Grep for pattern<br/>in scoped directories"]
    Q1 -->|No| THINK["Re-examine classification<br/>and incident text"]
    THINK --> GREP

    GREP --> Q2{Found<br/>relevant matches?}
    Q2 -->|Yes| READ["Read ONLY matched files<br/>(max 5 per incident)"]
    Q2 -->|No| WIDEN["Widen search slightly<br/>(still within scope)"]
    WIDEN --> GREP

    READ --> ANALYZE["Analyze with evidence"]

    style GREP fill:#cfc,stroke:#3c3,color:#333
    style READ fill:#ffc,stroke:#cc3,color:#333
```

**Rules enforced by #2 finalist**:
1. ALWAYS Grep for patterns FIRST (never Read blind)
2. Read ONLY relevant files (maximum 5 per incident)
3. NEVER Glob an entire directory
4. Combined with search_paths constraint, max ~10 tool calls

### Tool Safety: Read-Only, Always

```mermaid
flowchart LR
    subgraph "Agent Scope (read-only)"
        T1["Grep"]
        T2["Read"]
        T3["Glob"]
    end
    subgraph "Deterministic Code (outside agent)"
        T4["Create ticket"]
        T5["Send notification"]
        T6["Update database"]
    end

    T1 -.->|"path scoped to /app/codebase"| SAFE["Path validation:<br/>os.path.realpath()"]
    T2 -.->|"path scoped to /app/codebase"| SAFE
    T3 -.->|"path scoped to /app/codebase"| SAFE

    style T1 fill:#cfc,stroke:#3c3,color:#333
    style T2 fill:#cfc,stroke:#3c3,color:#333
    style T3 fill:#cfc,stroke:#3c3,color:#333
    style T4 fill:#ffc,stroke:#cc3,color:#333
    style T5 fill:#ffc,stroke:#cc3,color:#333
    style T6 fill:#ffc,stroke:#cc3,color:#333
```

**Critical pattern**: Agent tools have ZERO side effects. All mutations happen in deterministic pipeline stages outside the agent loop.

## Real Integrations with Graceful Degradation

Level 3 wires real integrations but handles failure gracefully:

```mermaid
flowchart TD
    RESULT["Triage Result"] --> TICKET{"Create ticket<br/>(Linear API)"}
    TICKET -->|Success| TID["ticket_id: ENG-42"]
    TICKET -->|API down| MOCK["Log locally,<br/>queue for retry"]

    RESULT --> NOTIFY{"Send alert<br/>(Slack webhook)"}
    NOTIFY -->|Success| SENT["Delivered to #sre-alerts"]
    NOTIFY -->|Webhook error| LOG["Log, continue pipeline"]

    style TID fill:#cfc,stroke:#3c3,color:#333
    style SENT fill:#cfc,stroke:#3c3,color:#333
    style MOCK fill:#fec,stroke:#c93,color:#333
    style LOG fill:#fec,stroke:#c93,color:#333
```

**Pattern**: `if API_KEY present → real provider; else → mock silently`. Never crash because an integration is misconfigured.

## Evidence from Finalists

### #1 cszdiego (Level 3, Winner)
- Pre-built service-keyword mapping + exception heuristics
- PydanticAI with Gemini 2.5 Flash
- Real Jira + Slack + Gmail integrations
- SSE streaming for real-time progress
- Cost: ~$0.01-0.03/incident

### #2 jjovalle99 (Level 3-4, Most Innovative)
- `generate-eshop-map.sh` at Docker build time
- Classification-driven search path scoping (the key innovation)
- Grep-first/Read-second discipline
- 140 tests, 95% coverage
- Cost: $0.007/incident

## Level 3 Checklist

- [ ] Pre-built service map injected as system prompt (build-time)
- [ ] Classification drives search scope before expensive triage
- [ ] Agent tools scoped to specific directories (path validation)
- [ ] Grep-first, Read-second discipline enforced in prompt
- [ ] Tool call budget set (10-15 max)
- [ ] At least one real integration per category (ticket, message, email)
- [ ] Graceful degradation when integrations fail
- [ ] Evidence ranked before packing into LLM context
- [ ] Cost per incident tracked (even if just logged)

---

*Previous: [003 — Level 2: Structured Agent](003-level-2-structured-agent.md) | Next: [005 — Level 4: Production Pipeline](005-level-4-production-pipeline.md)*
