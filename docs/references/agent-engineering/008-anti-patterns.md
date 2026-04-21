# 008 — Anti-Patterns: What NOT to Do

**Lessons from failure.** These anti-patterns were observed across the 12 implementations — some in the finalists, some in our own submission. Each is mapped to the maturity level where it becomes most dangerous.

---

## Anti-Pattern Map

```mermaid
flowchart TD
    subgraph "Level 1-2 Anti-Patterns"
        AP1["Hope-Based Parsing<br/>Trusting LLM to return valid JSON"]
        AP2["No Fallback Chain<br/>System crashes on invalid output"]
        AP3["No Input Validation<br/>Raw user text to LLM"]
    end

    subgraph "Level 2-3 Anti-Patterns"
        AP4["Claude For Everything<br/>Expensive model for cheap tasks"]
        AP5["User Picks The Model<br/>Exposing model choice to users"]
        AP6["RAG for Small Domains<br/>Vector DB for 5-10 services"]
    end

    subgraph "Level 3-4 Anti-Patterns"
        AP7["Self-Hosting Everything<br/>6 containers for observability"]
        AP8["Mock Everything<br/>All integrations mocked for demo"]
        AP9["Unbounded Investigation<br/>No max_turns, no scoping"]
    end

    subgraph "Level 5+ Anti-Patterns"
        AP10["Premature Multi-Agent<br/>Complexity before fundamentals"]
        AP11["Self-Modification Without Metrics<br/>Evolving without outcome data"]
    end

    style AP1 fill:#fcc,stroke:#c33,color:#333
    style AP2 fill:#fcc,stroke:#c33,color:#333
    style AP3 fill:#fcc,stroke:#c33,color:#333
    style AP4 fill:#fec,stroke:#c93,color:#333
    style AP5 fill:#fec,stroke:#c93,color:#333
    style AP6 fill:#fec,stroke:#c93,color:#333
    style AP7 fill:#ffc,stroke:#cc3,color:#333
    style AP8 fill:#ffc,stroke:#cc3,color:#333
    style AP9 fill:#ffc,stroke:#cc3,color:#333
    style AP10 fill:#ccf,stroke:#33c,color:#333
    style AP11 fill:#ccf,stroke:#33c,color:#333
```

## Detailed Anti-Patterns

### AP1: "Use Claude for Everything"

```mermaid
flowchart LR
    subgraph "Anti-Pattern"
        BAD["Sonnet for classify<br/>Sonnet for safety<br/>Sonnet for triage<br/>$0.10/incident"]
    end

    subgraph "Correct Pattern"
        GOOD["Mistral Mod for safety ($0)<br/>Mistral Med for classify ($0.001)<br/>Sonnet for triage ($0.006)<br/>$0.007/incident"]
    end

    BAD -->|"14x more expensive"| COMPARE["Same quality output<br/>for classification and safety"]

    style BAD fill:#fcc,stroke:#c33,color:#333
    style GOOD fill:#cfc,stroke:#3c3,color:#333
```

**Impact**: 14x cost difference for no quality gain on simple tasks.
**Fix**: Route by task complexity. Only use expensive models for reasoning-heavy tasks.
**Evidence**: #2 achieved $0.007/incident with 5 models. "Claude for everything" costs ~$0.10.

### AP2: "User Picks the Model"

```mermaid
flowchart TD
    subgraph "Anti-Pattern (our approach)"
        UI["User sees: Basic / Premium / Experimental"]
        UI --> Q["User asks: which one should I pick?"]
        Q --> WRONG["Wrong choice = bad results OR wasted cost"]
    end

    subgraph "Correct Pattern"
        AUTO["System automatically routes:<br/>Safety → free model<br/>Classify → cheap model<br/>Triage → expensive model"]
        AUTO --> RIGHT["Always optimal for the task"]
    end

    style WRONG fill:#fcc,stroke:#c33,color:#333
    style RIGHT fill:#cfc,stroke:#3c3,color:#333
```

**Impact**: Users don't know which model fits their incident. Results in either bad quality (cheap model for complex incident) or wasted cost (expensive model for simple classification).
**Fix**: Automatic model routing by task. The system decides, not the user.
**Evidence**: Our Triagista offered 3 engine choices. No finalist exposed model selection to users.

### AP3: "RAG for Small Domains"

```mermaid
flowchart LR
    subgraph "Anti-Pattern"
        RAG["Vector DB + embeddings<br/>For 5-10 services<br/>Complex infra, latency"]
    end

    subgraph "Correct Pattern"
        DICT["Python dictionary<br/>With fuzzy matching<br/>Instant, deterministic"]
    end

    RAG --> WASTE["Overkill: ~500ms latency<br/>for 5 lookups"]
    DICT --> FAST["<1ms, zero infrastructure"]

    style WASTE fill:#fcc,stroke:#c33,color:#333
    style FAST fill:#cfc,stroke:#3c3,color:#333
```

**Threshold**: RAG makes sense at 100+ documents. Below that, a dictionary with fuzzy matching is faster, simpler, and more reliable.
**Evidence**: #3 used a Python dict for service lookup. #5 used scikit-learn SVD (no external API) for its larger corpus.

### AP4: "Self-Hosting Everything"

```mermaid
flowchart TD
    subgraph "Anti-Pattern"
        SH["Docker Compose with:"]
        SH --> SH1["app"]
        SH --> SH2["postgres"]
        SH --> SH3["langfuse-web"]
        SH --> SH4["langfuse-worker"]
        SH --> SH5["langfuse-postgres"]
        SH --> SH6["langfuse-clickhouse"]
        SH --> SH7["langfuse-redis"]
        SH --> SH8["langfuse-minio"]
        SH1 --> TOTAL["8+ containers<br/>Slow startup<br/>Complex debugging"]
    end

    subgraph "Correct Pattern"
        LEAN["Docker Compose with:"]
        LEAN --> L1["app"]
        LEAN --> L2["postgres"]
        LEAN --> L3["(observability via cloud free tier)"]
        L1 --> FAST["3 containers<br/>Fast startup<br/>Simple debugging"]
    end

    style TOTAL fill:#fcc,stroke:#c33,color:#333
    style FAST fill:#cfc,stroke:#3c3,color:#333
```

**Impact**: 6 extra containers for observability when Langfuse Cloud free tier (500K obs/month) or Phoenix Cloud exists.
**Fix**: Use cloud-hosted free tiers for demos. Only self-host when data sovereignty requires it.
**Evidence**: Our submission ran 6+ containers. Winners ran 2-4 containers.

### AP5: "Mock Everything for Hackathon"

```mermaid
flowchart LR
    subgraph "Anti-Pattern"
        MOCK["All integrations mocked"]
        MOCK --> READS["Reads as: incomplete"]
        READS --> JUDGE["Judges see no real API flow"]
    end

    subgraph "Correct Pattern"
        REAL["Real integrations + graceful degradation"]
        REAL --> FLOW["Judges see real ticket created"]
        FLOW --> CRED["Massive demo credibility"]
    end

    MOCK -.->|"Setup time: 0h"| MOCK
    REAL -.->|"Setup time: 2-4h"| REAL

    style READS fill:#fcc,stroke:#c33,color:#333
    style CRED fill:#cfc,stroke:#3c3,color:#333
```

**Impact**: The #1 reason our submission didn't make the cut. Every top-5 finalist had real integrations.
**Fix**: Wire at least one real integration per category. Linear free tier + Slack webhook + Resend free tier = zero cost, 2-4 hours setup.
**Evidence**: Our submission had all-mocked integrations. This was a deliberate founding decision made on commit 1 and never challenged.

### AP6: "Unbounded Agent Investigation"

```mermaid
flowchart TD
    subgraph "Anti-Pattern"
        UB["Agent with Read/Grep/Glob<br/>No max_turns<br/>No directory scoping<br/>No search discipline"]
        UB --> GLOB["Glob /src/ → 500 files"]
        GLOB --> READ["Read random files"]
        READ --> MORE["Keep searching..."]
        MORE --> RESULT["50+ tool calls<br/>3+ minutes<br/>$0.50+ cost"]
    end

    subgraph "Correct Pattern"
        BD["Agent with scoped tools<br/>max_turns=15<br/>search_paths constrained<br/>Grep-first discipline"]
        BD --> SCOPE["Search 2 directories"]
        SCOPE --> FIND["~10 tool calls<br/>15-30 seconds<br/>$0.01-0.05"]
    end

    style RESULT fill:#fcc,stroke:#c33,color:#333
    style FIND fill:#cfc,stroke:#3c3,color:#333
```

**Impact**: 5x latency, 10x cost, often worse results (noise drowns signal).
**Fix**: Classify first → scope directories → enforce Grep-first → set max_turns budget.

## Anti-Pattern Severity by Maturity Level

```mermaid
graph TD
    subgraph "Building Level 2?"
        CRIT2["CRITICAL: No fallback chain<br/>CRITICAL: No input guardrails<br/>HIGH: Synchronous processing"]
    end

    subgraph "Building Level 3?"
        CRIT3["CRITICAL: Unbounded investigation<br/>HIGH: Claude for everything<br/>HIGH: All mocked integrations<br/>MEDIUM: No service map"]
    end

    subgraph "Building Level 4?"
        CRIT4["HIGH: Self-hosting everything<br/>HIGH: No observability<br/>MEDIUM: No deduplication<br/>MEDIUM: No confidence routing"]
    end

    subgraph "Building Level 5?"
        CRIT5["HIGH: No iteration budget<br/>HIGH: No termination criteria<br/>MEDIUM: Premature multi-agent"]
    end

    style CRIT2 fill:#fcc,stroke:#c33,color:#333
    style CRIT3 fill:#fec,stroke:#c93,color:#333
    style CRIT4 fill:#ffc,stroke:#cc3,color:#333
    style CRIT5 fill:#ccf,stroke:#33c,color:#333
```

## The Meta Anti-Pattern: Premature Sophistication

The biggest anti-pattern is not any single mistake — it's building Level 4-5 capabilities before Level 2-3 fundamentals are solid.

```mermaid
flowchart TD
    START["I want a great agent"] --> Q{"Do you have<br/>structured output<br/>+ fallback chain?"}
    Q -->|No| FIX["Fix Level 2 first.<br/>Nothing else matters<br/>until output is reliable."]
    Q -->|Yes| Q2{"Do you have<br/>context engineering<br/>+ tool discipline?"}
    Q2 -->|No| FIX2["Fix Level 3 first.<br/>Multi-model routing<br/>won't help if context<br/>is wrong."]
    Q2 -->|Yes| GO["Now consider<br/>Level 4-5 capabilities"]

    style FIX fill:#fcc,stroke:#c33,color:#333
    style FIX2 fill:#fec,stroke:#c93,color:#333
    style GO fill:#cfc,stroke:#3c3,color:#333
```

---

*Previous: [007 — Beyond Level 5](007-beyond-level-5.md) | Next: [009 — Implementation Roadmap](009-implementation-roadmap.md)*
