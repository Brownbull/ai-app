# 001 — Architecture Taxonomy: 4 Patterns for Agent Systems

**Context**: Before discussing maturity levels, understand the 4 architecture patterns observed across 12 agent implementations. Architecture choice is independent of maturity level — you can implement any pattern at any level.

---

## The 4 Patterns at a Glance

```mermaid
graph TD
    subgraph "Pattern A: Single Agent + Deterministic Pipeline"
        A1[Input] --> A2[Guardrails]
        A2 --> A3[Classify]
        A3 --> A4["Agent(tools)"]
        A4 --> A5[Ticket]
        A5 --> A6[Notify]
        A6 --> A7[Resolve]
    end

    style A4 fill:#ffc,stroke:#cc3,color:#333
    style A1 fill:#eee,stroke:#999,color:#333
    style A2 fill:#eee,stroke:#999,color:#333
    style A3 fill:#eee,stroke:#999,color:#333
    style A5 fill:#eee,stroke:#999,color:#333
    style A6 fill:#eee,stroke:#999,color:#333
    style A7 fill:#eee,stroke:#999,color:#333
```

```mermaid
graph TD
    subgraph "Pattern B: Multi-Model Staged Pipeline"
        B1[Input] --> B2["Model 1<br/>Safety"]
        B2 --> B3["Model 2<br/>Classify"]
        B3 --> B4["Model 3<br/>Triage(tools)"]
        B4 --> B5[Ticket + Notify]
    end

    style B2 fill:#cef,stroke:#39c,color:#333
    style B3 fill:#fec,stroke:#c93,color:#333
    style B4 fill:#ffc,stroke:#cc3,color:#333
    style B5 fill:#eee,stroke:#999,color:#333
```

```mermaid
graph TD
    subgraph "Pattern C: LangGraph State Machine"
        C1[Input] --> C2[Node 1]
        C2 --> C3[Node 2]
        C3 --> C4[...]
        C4 --> C5[Node N]
        C3 -.->|checkpoint| CDB[(State DB)]
        C5 -.->|checkpoint| CDB
        C4 -.->|"human approval"| CH[Human]
        CH -.-> C4
    end

    style C2 fill:#cfc,stroke:#3c3,color:#333
    style C3 fill:#cfc,stroke:#3c3,color:#333
    style C4 fill:#cfc,stroke:#3c3,color:#333
    style C5 fill:#cfc,stroke:#3c3,color:#333
    style CDB fill:#fcf,stroke:#c3c,color:#333
```

```mermaid
graph TD
    subgraph "Pattern D: Tool-Use Loop"
        D1[Input] --> D2["Agent<br/>(system prompt + tools)"]
        D2 --> D3{Enough evidence?}
        D3 -->|No| D4[Search]
        D4 --> D5[Read]
        D5 --> D6[Analyze]
        D6 --> D2
        D3 -->|Yes| D7[Output]
    end

    style D2 fill:#ccf,stroke:#33c,color:#333
    style D3 fill:#ffc,stroke:#cc3,color:#333
    style D4 fill:#eee,stroke:#999,color:#333
    style D5 fill:#eee,stroke:#999,color:#333
    style D6 fill:#eee,stroke:#999,color:#333
```

## Who Used What

```mermaid
pie title Architecture Pattern Distribution (12 repos)
    "A: Single Agent" : 5
    "B: Multi-Model" : 2
    "C: LangGraph" : 2
    "D: Tool-Loop" : 2
    "Hybrid (A+D)" : 1
```

| Pattern | Teams | Notable Implementation |
|---------|-------|----------------------|
| **A** Single Agent | #1, #3, #4, #11, Us | #1 (PydanticAI + 202 Accepted + SSE) |
| **B** Multi-Model | #2, #8 | #2 (5 models, $0.007/incident) |
| **C** LangGraph | #5 (10 nodes), #9 (13 nodes) | #5 (DB transaction per stage) |
| **D** Tool-Loop | #11 (max 8 iter), #9 (active retrieval) | #9 (Codex-inspired plan-search-verify) |

## Decision Matrix

```mermaid
quadrantChart
    title Architecture Selection Guide
    x-axis Low Complexity --> High Complexity
    y-axis Low Adaptability --> High Adaptability
    quadrant-1 Research Agents
    quadrant-2 Enterprise Systems
    quadrant-3 MVPs & Hackathons
    quadrant-4 Production Services
    Pattern A - Single Agent: [0.25, 0.20]
    Pattern B - Multi-Model: [0.45, 0.25]
    Pattern C - LangGraph: [0.75, 0.55]
    Pattern D - Tool-Loop: [0.50, 0.80]
```

### When to Choose Each

| Factor | A: Single Agent | B: Multi-Model | C: LangGraph | D: Tool-Loop |
|--------|----------------|----------------|--------------|--------------|
| **Latency** | 5-15s | 10-30s | 15-60s | 30-180s |
| **Cost/incident** | $0.01-0.05 | $0.005-0.01 | $0.02-0.05 | $0.02-0.10 |
| **Complexity** | Low | Medium | High | Medium |
| **Predictability** | High | High | High | Low |
| **Adaptability** | Low | Low | Medium | High |
| **Best for** | MVP, hackathon | Production cost-opt | Enterprise audit | Research, deep analysis |

### The Decision Flowchart

```mermaid
flowchart TD
    START[What are you building?] --> Q1{Need checkpoint/<br/>recovery?}
    Q1 -->|Yes| C["Pattern C<br/>LangGraph State Machine"]
    Q1 -->|No| Q2{Agent must adapt<br/>investigation strategy?}
    Q2 -->|Yes| D["Pattern D<br/>Tool-Use Loop"]
    Q2 -->|No| Q3{Cost optimization<br/>critical?}
    Q3 -->|Yes| B["Pattern B<br/>Multi-Model Pipeline"]
    Q3 -->|No| A["Pattern A<br/>Single Agent + Pipeline"]

    style A fill:#ffc,stroke:#cc3,color:#333
    style B fill:#cef,stroke:#39c,color:#333
    style C fill:#cfc,stroke:#3c3,color:#333
    style D fill:#ccf,stroke:#33c,color:#333
```

## Key Insight

**Architecture choice is not maturity.** A Level 4 implementation with Pattern A (single agent) beats a Level 2 implementation with Pattern C (LangGraph). Don't reach for complex architectures to compensate for missing fundamentals. Start with Pattern A, add sophistication as needed.

The #1 finalist won with Pattern A. The #2 finalist was most innovative with Pattern B. Pattern C and D add value only when you need checkpoint recovery or autonomous investigation.

---

*Previous: [000 — Overview](000-overview.md) | Next: [002 — Level 1: Prompt & Parse](002-level-1-prompt-and-parse.md)*
