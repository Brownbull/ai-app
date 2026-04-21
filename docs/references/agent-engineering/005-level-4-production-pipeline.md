# 005 — Level 4: Production Pipeline

**Production-grade.** Multiple models, staged context assembly, defense-in-depth security, full observability, and temporal memory. This is where agent systems become enterprise-ready.

---

## What Level 4 Looks Like

```mermaid
sequenceDiagram
    participant U as User
    participant API as API Server
    participant M1 as Model 1 (Safety)
    participant M2 as Model 2 (Classify)
    participant M3 as Model 3 (Triage)
    participant OBS as Observability
    participant INT as Integrations

    U->>API: Submit incident
    API-->>U: 202 Accepted + SSE stream
    API->>OBS: Start trace (root span)

    API->>M1: Safety screening (free model)
    M1-->>API: Passed (420ms)
    API->>OBS: Span: moderation (passed)

    API->>M2: Classify severity + service (cheap model)
    M2-->>API: P1, PaymentProcessor, search_paths
    API->>OBS: Span: classification (P1)

    API->>M3: Deep triage with scoped tools (expensive model)
    Note over M3: 10 tool calls, evidence assembly
    M3-->>API: Root cause + confidence 0.87
    API->>OBS: Span: triage (confidence 0.87, 10 tools, 2341 tokens)

    alt Confidence >= 0.6
        API->>INT: Create ticket + notify team
    else Confidence < 0.6
        API->>INT: Route to SRE-Triage (human review)
    end

    API->>OBS: Close trace (total: 18s, cost: $0.007)
    API->>U: SSE: stage complete events throughout
```

## Multi-Model Routing

The defining feature of Level 4: different models for different tasks.

```mermaid
flowchart TD
    subgraph "Free Tier"
        M_SAFE["Mistral Moderation<br/>Safety screening<br/>$0.00/call"]
    end

    subgraph "Cheap Tier ($0.04-0.40/M)"
        M_CLASS["Mistral Medium<br/>Classification + severity"]
        M_STT["Voxtral Mini<br/>Speech-to-text"]
        M_VIS["Mistral Small<br/>Image analysis"]
    end

    subgraph "Expensive Tier ($3/M)"
        M_TRIAGE["Claude Sonnet<br/>Deep codebase triage<br/>with tool use"]
    end

    INPUT["Incident"] --> M_SAFE
    M_SAFE --> M_CLASS
    M_CLASS --> M_STT
    M_STT --> M_VIS
    M_VIS --> M_TRIAGE
    M_TRIAGE --> OUTPUT["Triage Result"]

    style M_SAFE fill:#cfc,stroke:#3c3,color:#333
    style M_CLASS fill:#ffc,stroke:#cc3,color:#333
    style M_STT fill:#ffc,stroke:#cc3,color:#333
    style M_VIS fill:#ffc,stroke:#cc3,color:#333
    style M_TRIAGE fill:#fcc,stroke:#c33,color:#333
```

### Cost Impact (Real Data)

```mermaid
graph LR
    subgraph "Single Model Approach"
        S1["Claude Sonnet for everything"]
        S1 --> SC["~$0.10/incident"]
    end

    subgraph "Multi-Model Approach"
        M1["5 specialized models"] 
        M1 --> MC["$0.007/incident"]
    end

    SC --> COMPARE["14x more expensive"]
    
    style SC fill:#fcc,stroke:#c33,color:#333
    style MC fill:#cfc,stroke:#3c3,color:#333
    style COMPARE fill:#ffc,stroke:#cc3,color:#333
```

| Task | Model | Cost/M tokens | % of Total Cost |
|------|-------|--------------|-----------------|
| Safety screening | Mistral Moderation | $0.00 | 0% |
| Classification | Mistral Medium | $0.40 | ~1% |
| Speech-to-text | Voxtral Mini | $0.04 | <1% |
| Image analysis | Mistral Small | $0.60 | ~1% |
| Deep triage | Claude Sonnet | $3.00 | **~98%** |

**Lesson**: The triage step dominates cost. Optimize everything else to be cheap or free. The 14x savings come from NOT using Sonnet for classification, safety, and extraction.

## Staged Context Assembly

Build context progressively — each stage's output improves the next stage's query.

```mermaid
flowchart TD
    subgraph "Stage 1: Extract Facts"
        S1["Parse incident text"]
        S1 --> F1["request_id: abc-123<br/>error_code: 500<br/>service: checkout"]
    end

    subgraph "Stage 2: Query Runtime"
        F1 --> S2["Query logs with facts"]
        S2 --> F2["Correlated log entries<br/>within ±5 min window"]
    end

    subgraph "Stage 3: Search Codebase"
        F1 --> S3A["Facts constrain search"]
        F2 --> S3B["Logs refine search"]
        S3A --> S3["Search relevant files"]
        S3B --> S3
        S3 --> F3["Ranked source files<br/>by combined score"]
    end

    subgraph "Stage 4: Generate Summary"
        F1 --> S4A[" "]
        F2 --> S4B[" "]
        F3 --> S4C[" "]
        S4A --> S4["Generate grounded hypothesis<br/>with citations from ALL evidence"]
        S4B --> S4
        S4C --> S4
    end

    style F1 fill:#cef,stroke:#39c,color:#333
    style F2 fill:#fec,stroke:#c93,color:#333
    style F3 fill:#ffc,stroke:#cc3,color:#333
    style S4 fill:#cfc,stroke:#3c3,color:#333
```

**Why staged assembly beats dump-everything**: If you throw incident text + all logs + all code at the LLM, you get noise. Each stage filters and refines, so the final LLM call sees only relevant, pre-ranked evidence.

## Defense-in-Depth Security (5 Layers)

```mermaid
flowchart TD
    INPUT["External Input"] --> L1

    subgraph L1["Layer 1: Dedicated Moderation"]
        L1D["Mistral Moderation (free)<br/>11-category classifier<br/>Fail-CLOSED on API error"]
    end

    L1 --> L2
    subgraph L2["Layer 2: Inline Guardrails"]
        L2D["Runs alongside classification<br/>Zero extra latency"]
    end

    L2 --> L3
    subgraph L3["Layer 3: Input Boundary Markers"]
        L3D["[USER_INPUT_START]...[USER_INPUT_END]<br/>Agent treats as data, not instructions"]
    end

    L3 --> L4
    subgraph L4["Layer 4: Path Restriction"]
        L4D["Tools scoped to specific directory<br/>os.path.realpath() validation"]
    end

    L4 --> L5
    subgraph L5["Layer 5: Webhook Verification"]
        L5D["HMAC-SHA256 signatures<br/>Reject timestamps >60s old<br/>Timing-safe comparison"]
    end

    style L1 fill:#fcc,stroke:#c33,color:#333
    style L2 fill:#fec,stroke:#c93,color:#333
    style L3 fill:#ffc,stroke:#cc3,color:#333
    style L4 fill:#cfc,stroke:#3c3,color:#333
    style L5 fill:#ccf,stroke:#33c,color:#333
```

**Fail-closed principle**: If the safety check itself fails (API timeout, error), block the input. Safety over availability for external-facing inputs.

## Comprehensive Observability

### Trace Hierarchy

```mermaid
flowchart TD
    ROOT["incident.pipeline<br/>(root span)"]

    ROOT --> MOD["pipeline.moderation<br/>mistral-moderation, passed: true"]
    ROOT --> CLS["pipeline.classification<br/>mistral-medium, severity: P1"]
    ROOT --> TRI["pipeline.triage<br/>claude-sonnet-4-6"]
    ROOT --> TKT["pipeline.ticket<br/>linear.create → ENG-42"]
    ROOT --> NTF["pipeline.notify"]

    TRI --> TG["tool.Grep<br/>ConnectionPool, src/Payment/"]
    TRI --> TR1["tool.Read<br/>PaymentProcessor.cs:142"]
    TRI --> TLLM["llm.call<br/>in:2341 tok, out:587 tok"]
    TRI --> TR2["tool.Read<br/>OrderService.cs:89"]

    NTF --> NS["slack.send<br/>#sre-alerts, delivered"]
    NTF --> NE["email.send<br/>team@..., delivered"]

    style ROOT fill:#ffc,stroke:#cc3,color:#333
    style TRI fill:#ccf,stroke:#33c,color:#333
```

### Three Pillars + Agent Extension

| Pillar | Standard | Agent-Specific Extension |
|--------|----------|--------------------------|
| **Logging** | JSON structured | Per-stage context binding (incident_id, severity, confidence) |
| **Metrics** | Request count, latency | Token usage, LLM call count, cost/incident, guardrail blocks |
| **Tracing** | HTTP request spans | Tool-call spans, LLM generation spans, evidence retrieval spans |
| **Reasoning** | — | Live reasoning steps via SSE for user visibility |

### Tooling

| Tool | Best For | Used By |
|------|----------|---------|
| **Arize Phoenix** | OpenTelemetry native, free, LLM-specific views | #2, #5 |
| **Langfuse** | LLM observability, prompt analytics, sessions | #1, #7, #10, #11 |
| **Prometheus** | Metrics, alerting, cost tracking | #3, #5 |
| **Jaeger** | Distributed traces, lightweight | #3, #9 |

## Temporal Memory (Deduplication)

```mermaid
flowchart TD
    NEW["New incident"] --> COMPARE{"Similar incident<br/>in last 30 min?"}
    COMPARE -->|"SequenceMatcher +<br/>Jaccard > 0.7"| INJECT["Inject prior triage as<br/>UNVERIFIED HYPOTHESIS"]
    COMPARE -->|No match| FRESH["Fresh investigation"]

    INJECT --> VERIFY["Agent MUST:<br/>1. Search codebase to confirm pattern<br/>2. State whether prior cause confirmed/ruled out"]
    VERIFY --> RESULT["Grounded result<br/>(confirmed or new hypothesis)"]

    style INJECT fill:#ffc,stroke:#cc3,color:#333
    style VERIFY fill:#cfc,stroke:#3c3,color:#333
```

**Critical guardrail**: Always label prior context as "unverified." Without this, agents blindly copy prior results (force-fit trap).

## Evidence from Finalists

### #2 jjovalle99 (Level 4, Most Cost-Efficient)
- 5 models in staged pipeline ($0.007/incident)
- Defense-in-depth: Mistral Moderation + inline guardrails + boundary markers + path restriction + HMAC webhooks
- Arize Phoenix traces with full tool-call spans
- SequenceMatcher + Jaccard deduplication (30-min window)
- 140 tests, 95% coverage

### #5 Core Tech Expert (Level 4, Most Enterprise)
- 10-stage LangGraph pipeline with DB transaction per stage
- Hybrid retrieval: TF-IDF + SVD (64-dim) on pgvector
- Arize Phoenix + Loki + Grafana + Prometheus
- Staged context assembly (facts → logs → code → summary)
- ClamAV malware scan + Tesseract OCR on uploads

## Level 4 Checklist

- [ ] Multiple models routed by task (cheap classify, expensive reason)
- [ ] Staged context assembly (progressive evidence building)
- [ ] Checkpoint & recovery for pipelines >30s
- [ ] Defense-in-depth security (3+ layers, fail-closed)
- [ ] Full observability: traces + metrics + structured logs
- [ ] Key trace attributes: incident_id, severity, confidence, tokens, cost
- [ ] Deduplication against recent incidents (temporal window)
- [ ] Prior context labeled as "unverified hypothesis"
- [ ] Confidence-based routing (low confidence → human escalation)
- [ ] Evidence-based documentation (real numbers from real runs)
- [ ] SSE/WebSocket streaming for real-time progress

---

*Previous: [004 — Level 3: Context-Engineered Agent](004-level-3-context-engineered.md) | Next: [006 — Level 5: Autonomous Investigation](006-level-5-autonomous-investigation.md)*
