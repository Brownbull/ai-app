# 009 — Implementation Roadmap

**The practical guide.** If you're building an agent from scratch, implement these capabilities in this exact order. Each step builds on the previous. Skip nothing.

---

## The 10-Step Climb

```mermaid
flowchart TD
    S1["1. Structured Output<br/>(PydanticAI or tool-use forcing)"]
    S2["2. Deterministic Pipeline<br/>(Agent handles ONE stage)"]
    S3["3. Guardrails Before LLM<br/>(Regex + input validation)"]
    S4["4. Fallback Chain<br/>(Retry → extract → rule-based → default)"]
    S5["5. Context Engineering<br/>(Service map + classification scoping)"]
    S6["6. Real-Time Streaming<br/>(SSE/WebSocket for progress)"]
    S7["7. Multi-Model Routing<br/>(Cheap classify, expensive reason)"]
    S8["8. Observability<br/>(Traces + metrics + structured logs)"]
    S9["9. Deduplication<br/>(Temporal memory + hypothesis injection)"]
    S10["10. Active Retrieval<br/>(Plan-driven investigation, self-correction)"]

    S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9 --> S10

    S1 -.- L2["Level 2"]
    S2 -.- L2
    S3 -.- L2
    S4 -.- L2
    S5 -.- L3["Level 3"]
    S6 -.- L3
    S7 -.- L4["Level 4"]
    S8 -.- L4
    S9 -.- L4
    S10 -.- L5["Level 5"]

    style S1 fill:#fec,stroke:#c93,color:#333
    style S2 fill:#fec,stroke:#c93,color:#333
    style S3 fill:#fec,stroke:#c93,color:#333
    style S4 fill:#fec,stroke:#c93,color:#333
    style S5 fill:#ffc,stroke:#cc3,color:#333
    style S6 fill:#ffc,stroke:#cc3,color:#333
    style S7 fill:#cfc,stroke:#3c3,color:#333
    style S8 fill:#cfc,stroke:#3c3,color:#333
    style S9 fill:#cfc,stroke:#3c3,color:#333
    style S10 fill:#ccf,stroke:#33c,color:#333
    style L2 fill:#fec,stroke:#c93,color:#333
    style L3 fill:#ffc,stroke:#cc3,color:#333
    style L4 fill:#cfc,stroke:#3c3,color:#333
    style L5 fill:#ccf,stroke:#33c,color:#333
```

## Step-by-Step Detail

### Step 1: Structured Output (Foundation)

**What**: Use framework-level schema enforcement, not prompt instructions.
**Why**: Everything else depends on reliable, parseable output.
**Effort**: 2-3 hours

```mermaid
flowchart LR
    subgraph "Choose One"
        A["PydanticAI<br/>output_type=TriageResult<br/>Works with any provider"]
        B["Claude tool-use<br/>tool_choice={type:tool}<br/>Schema-enforced response"]
    end

    A --> OK["Guaranteed valid output"]
    B --> OK

    style OK fill:#cfc,stroke:#3c3,color:#333
```

### Step 2: Deterministic Pipeline

**What**: Agent handles ONE stage (triage). Everything else is code.
**Why**: Predictable behavior, easy debugging, clear boundaries.
**Effort**: 2-4 hours

```mermaid
flowchart LR
    CODE1["Validate<br/>(code)"] --> CODE2["Classify<br/>(code or cheap LLM)"]
    CODE2 --> AGENT["Triage<br/>(AGENT)"]
    AGENT --> CODE3["Ticket<br/>(code)"]
    CODE3 --> CODE4["Notify<br/>(code)"]

    style AGENT fill:#ffc,stroke:#cc3,color:#333
    style CODE1 fill:#eee,stroke:#999,color:#333
    style CODE2 fill:#eee,stroke:#999,color:#333
    style CODE3 fill:#eee,stroke:#999,color:#333
    style CODE4 fill:#eee,stroke:#999,color:#333
```

### Step 3: Guardrails Before LLM

**What**: Compiled regex patterns. Run before any token is consumed.
**Why**: Blocks injection attacks. <5ms cost. No reason to skip.
**Effort**: 1-2 hours

### Step 4: Fallback Chain

**What**: LLM fails → retry → regex extract → rule-based → safe default.
**Why**: 15% of LLM responses will fail validation. The chain catches them all.
**Effort**: 2-3 hours

### Step 5: Context Engineering

**What**: Pre-built service map + classification-driven scoping.
**Why**: This is where quality jumps. The LLM sees only relevant context.
**Effort**: 4-6 hours

```mermaid
flowchart TD
    BUILD["Docker build time"] --> MAP["Generate service_map.md<br/>(scan codebase structure)"]
    MAP --> INJECT["Inject as system prompt<br/>(~200-500 tokens)"]
    INJECT --> SAVE["Save 3-5 tool calls<br/>per incident"]

    CLASSIFY["Classify incident"] --> SCOPE["Output: search_paths"]
    SCOPE --> CONSTRAIN["Constrain agent tools<br/>to those directories only"]

    style MAP fill:#ffc,stroke:#cc3,color:#333
    style CONSTRAIN fill:#cfc,stroke:#3c3,color:#333
```

### Step 6: Real-Time Streaming

**What**: SSE/WebSocket events for pipeline progress.
**Why**: Makes the agent feel responsive. Dead air during processing kills demos.
**Effort**: 4-6 hours

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant API as Server

    API-->>U: SSE: {"stage": "moderation", "status": "started"}
    API-->>U: SSE: {"stage": "moderation", "status": "passed"}
    API-->>U: SSE: {"stage": "classification", "status": "started"}
    API-->>U: SSE: {"stage": "classification", "result": "P1, PaymentService"}
    API-->>U: SSE: {"stage": "triage", "status": "searching_code"}
    API-->>U: SSE: {"stage": "triage", "status": "analyzing_files"}
    API-->>U: SSE: {"stage": "triage", "status": "complete"}
    API-->>U: SSE: {"stage": "ticket", "result": "ENG-42 created"}
```

### Step 7: Multi-Model Routing

**What**: Cheap models for classification/safety, expensive for reasoning.
**Why**: This is where cost drops 10-14x.
**Effort**: 4-6 hours

### Step 8: Observability

**What**: Langfuse/Phoenix for LLM traces, Prometheus for metrics.
**Why**: Without traces, you can't debug why the agent made a decision.
**Effort**: 4-8 hours (instrument from day one — harder to add retroactively)

### Step 9: Deduplication

**What**: Compare against recent incidents, inject prior context as hypothesis.
**Why**: Reduces redundant investigation. Speeds up repeated incidents.
**Effort**: 2-4 hours

### Step 10: Active Retrieval

**What**: Agent plans investigation, adapts based on findings, self-corrects.
**Why**: Only needed when domain requires deep investigation.
**Effort**: 8-16 hours

## Effort Breakdown

```mermaid
pie title Implementation Effort by Level
    "Level 2 (Steps 1-4)" : 28
    "Level 3 (Steps 5-6)" : 40
    "Level 4 (Steps 7-9)" : 48
    "Level 5 (Step 10)" : 64
```

| Level | Steps | Estimated Hours | Cumulative |
|-------|-------|----------------|------------|
| Level 2 | 1-4 | 7-12h | 7-12h |
| Level 3 | 5-6 | 8-12h | 15-24h |
| Level 4 | 7-9 | 10-18h | 25-42h |
| Level 5 | 10 | 8-16h | 33-58h |

**Hackathon note**: In a 48-hour hackathon, a solo builder can realistically achieve Level 3 with parts of Level 4. Aim for Steps 1-6 + one real integration. That's the winning formula.

## Framework Comparison

Choose your framework based on what you're building:

```mermaid
flowchart TD
    Q1{"What are you<br/>building?"} --> Q2{"Need checkpoint<br/>recovery?"}
    Q2 -->|Yes| LG["LangGraph"]
    Q2 -->|No| Q3{"Using Claude<br/>exclusively?"}
    Q3 -->|Yes| Q4{"Need built-in<br/>file tools?"}
    Q4 -->|Yes| CSDK["Claude Agent SDK"]
    Q4 -->|No| RAW_C["Raw Anthropic SDK"]
    Q3 -->|No| Q5{"Need multi-provider<br/>support?"}
    Q5 -->|Yes| PAI["PydanticAI"]
    Q5 -->|No| RAW["Raw SDK for your provider"]

    style LG fill:#cfc,stroke:#3c3,color:#333
    style CSDK fill:#ccf,stroke:#33c,color:#333
    style RAW_C fill:#ffc,stroke:#cc3,color:#333
    style PAI fill:#cef,stroke:#39c,color:#333
    style RAW fill:#eee,stroke:#999,color:#333
```

| Framework | Best For | Structured Output | Tool Use | Checkpoint | Used By |
|-----------|---------|-------------------|----------|------------|---------|
| **PydanticAI** | Simple agents, any provider | Native (output_type) | @tool decorator | No | #1, #3 |
| **Claude Agent SDK** | Claude + file tools | Via output_format | Built-in Read/Grep/Glob | No | #2, Us |
| **LangGraph** | Complex multi-stage | Via tool-use | Custom nodes | Yes (DB) | #5, #9 |
| **Raw Anthropic SDK** | Fine-grained control | tool_choice + schema | Custom tools | Manual | #2, #5, #10 |
| **Raw Google GenAI** | Gemini + cheap inference | response_mime_type | Custom tools | No | #1, #4 |

**Notable absence**: No finalist used LangChain. PydanticAI and raw SDKs dominated. The trend is toward simpler, more explicit frameworks over heavy abstractions.

## The Minimum Viable Agent

If you have **4 hours**, build this:

```mermaid
flowchart LR
    IN["Input"] --> GUARD["Regex guardrails<br/>(10 patterns)"]
    GUARD --> LLM["PydanticAI agent<br/>(output_type enforced)"]
    LLM --> FB["Fallback chain<br/>(retry → default)"]
    FB --> OUT["Structured result"]

    style GUARD fill:#fec,stroke:#c93,color:#333
    style LLM fill:#ffc,stroke:#cc3,color:#333
    style FB fill:#cfc,stroke:#3c3,color:#333
```

This gets you to **Level 2** — a working agent with guaranteed output, basic safety, and graceful failure handling. Everything beyond this is optimization.

## The Winning Formula (48-Hour Hackathon)

```mermaid
gantt
    title Hackathon Implementation Order
    dateFormat HH
    axisFormat %H:00

    section Level 2 Foundation
    Structured output + fallback     :a1, 00, 04
    Guardrails + async processing    :a2, 04, 06

    section Level 3 Quality
    Service map + context scoping    :a3, 06, 10
    Tool discipline (Grep-first)     :a4, 10, 12

    section Real Integrations
    Linear + Slack + Resend (free)   :a5, 12, 16

    section SSE Streaming
    Pipeline progress events         :a6, 16, 20

    section Polish
    Seed data + demo prep            :a7, 20, 24
    Documentation with real numbers  :a8, 24, 26

    section Buffer
    Fix issues + edge cases          :a9, 26, 30
```

**Total: 30 hours of focused building.** Leaves 18 hours for sleep, meals, and debugging. This is the path the top finalists followed.

---

*Previous: [008 — Anti-Patterns](008-anti-patterns.md) | Start over: [000 — Overview](000-overview.md)*
