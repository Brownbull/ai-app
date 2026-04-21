# 007 — Beyond Level 5: Emerging Patterns

**The theoretical frontier.** No implementation in the analysis fully achieved Level 5, and these levels are extrapolations based on observable trends in agent research, multi-agent systems, and self-improving architectures. They are included because someone building agents should know where the field is heading — even if they shouldn't build for it today.

---

## The Extended Maturity Model

```mermaid
graph TB
    subgraph L7["Level 7: Self-Improving System"]
        L7D["Prompt/tool evolution<br/>Architecture self-modification<br/>Meta-learning across domains"]
    end
    subgraph L6["Level 6: Collaborative Multi-Agent"]
        L6D["Specialized agent teams<br/>Negotiation protocols<br/>Shared knowledge base<br/>Conflict resolution"]
    end
    subgraph L5["Level 5: Autonomous Investigation"]
        L5D["Active retrieval<br/>Self-correction<br/>Pattern extraction"]
    end
    subgraph "Observed in Hackathon (Levels 1-4)"
        L4["Level 4: Production Pipeline"]
        L3["Level 3: Context-Engineered"]
        L2["Level 2: Structured Agent"]
        L1["Level 1: Prompt & Parse"]
    end

    L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7

    style L1 fill:#fee,stroke:#c33,color:#333
    style L2 fill:#fec,stroke:#c93,color:#333
    style L3 fill:#ffc,stroke:#cc3,color:#333
    style L4 fill:#cfc,stroke:#3c3,color:#333
    style L5 fill:#ccf,stroke:#33c,color:#333
    style L6 fill:#ecf,stroke:#93c,color:#333
    style L7 fill:#fce,stroke:#c39,color:#333
```

## Level 6: Collaborative Multi-Agent System

Multiple specialized agents working together with explicit handoff protocols, shared state, and conflict resolution.

```mermaid
flowchart TD
    INC["Incident"] --> ORCH["Orchestrator"]

    ORCH --> TRIAGE_A["Triage Agent<br/>(Claude Sonnet)<br/>Deep code analysis"]
    ORCH --> INFRA_A["Infra Agent<br/>(cheap model)<br/>Log/metric correlation"]
    ORCH --> HISTORY_A["History Agent<br/>(cheap model)<br/>Past incident patterns"]

    TRIAGE_A -->|"hypothesis + evidence"| MERGE["Evidence Merger"]
    INFRA_A -->|"infrastructure context"| MERGE
    HISTORY_A -->|"historical patterns"| MERGE

    MERGE --> CONFLICT{Conflicting<br/>hypotheses?}
    CONFLICT -->|Yes| DEBATE["Debate Protocol:<br/>Each agent defends<br/>its hypothesis with evidence"]
    CONFLICT -->|No| CONSENSUS["Consensus result"]

    DEBATE --> JUDGE["Judge Agent<br/>Selects best-supported hypothesis"]
    JUDGE --> CONSENSUS

    CONSENSUS --> RESULT["Final triage<br/>with provenance chain"]

    style ORCH fill:#ffc,stroke:#cc3,color:#333
    style TRIAGE_A fill:#ccf,stroke:#33c,color:#333
    style INFRA_A fill:#cef,stroke:#39c,color:#333
    style HISTORY_A fill:#cfc,stroke:#3c3,color:#333
    style DEBATE fill:#fec,stroke:#c93,color:#333
```

### Key Capabilities

| Capability | What It Means |
|------------|--------------|
| **Specialized roles** | Each agent has domain expertise (code, infra, history) |
| **Parallel investigation** | Agents search simultaneously, reducing wall-clock time |
| **Shared knowledge base** | Findings from one agent available to all others |
| **Conflict resolution** | When hypotheses disagree, structured debate resolves it |
| **Provenance tracking** | Final result traces back to which agent contributed what |

### Why Not Just One Better Agent?

```mermaid
flowchart LR
    subgraph "Single Agent"
        SA["One agent, all tasks<br/>Sequential investigation<br/>One perspective<br/>Context window pressure"]
    end

    subgraph "Multi-Agent"
        MA["Specialized agents<br/>Parallel investigation<br/>Multiple perspectives<br/>Distributed context"]
    end

    SA -->|"When single context<br/>window is sufficient"| GOOD1["Good enough<br/>for most cases"]
    MA -->|"When investigation<br/>exceeds one context"| GOOD2["Required for<br/>complex incidents"]

    style GOOD1 fill:#cfc,stroke:#3c3,color:#333
    style GOOD2 fill:#ccf,stroke:#33c,color:#333
```

**Practical threshold**: Multi-agent becomes valuable when an investigation requires more context than a single agent can hold, or when different domain expertise is needed (code vs. infrastructure vs. business logic).

## Level 7: Self-Improving System

The agent system evolves its own capabilities based on outcomes.

```mermaid
flowchart TD
    subgraph "Operate"
        OP1["Handle incidents normally"]
        OP1 --> OP2["Record outcome:<br/>Was triage accurate?<br/>Was root cause confirmed?"]
    end

    subgraph "Learn"
        OP2 --> L1["Analyze outcome patterns"]
        L1 --> L2{"What failed?"}
        L2 -->|"Wrong service map"| L3A["Update service map<br/>with new dependency"]
        L2 -->|"Poor search strategy"| L3B["Add new search<br/>template for this error type"]
        L2 -->|"Missing tool"| L3C["Propose new tool<br/>for human approval"]
    end

    subgraph "Evolve"
        L3A --> E1["Updated system prompt"]
        L3B --> E1
        L3C --> E2["New tool (human-approved)"]
        E1 --> E3["A/B test against<br/>previous version"]
        E2 --> E3
        E3 --> E4{"Improvement<br/>confirmed?"}
        E4 -->|Yes| E5["Promote to production"]
        E4 -->|No| E6["Rollback, log lesson"]
    end

    E5 --> OP1
    E6 --> OP1

    style L1 fill:#ffc,stroke:#cc3,color:#333
    style E3 fill:#ccf,stroke:#33c,color:#333
    style E5 fill:#cfc,stroke:#3c3,color:#333
    style E6 fill:#fcc,stroke:#c33,color:#333
```

### Key Capabilities

| Capability | What It Means | Risk |
|------------|--------------|------|
| **Prompt evolution** | System prompt improves based on outcome data | Prompt drift, regression |
| **Tool creation** | Agent proposes new tools for recurring patterns | Requires human gate |
| **Service map updates** | Architecture knowledge auto-updates when code changes | Stale data, hallucination |
| **Strategy library** | Successful investigation strategies stored and reused | Overfitting to past patterns |
| **A/B testing** | New capabilities tested against baseline before promotion | Requires outcome metrics |

### The Human-in-the-Loop Boundary

```mermaid
flowchart LR
    subgraph "Agent Can Self-Modify"
        SM1["Search strategy selection"]
        SM2["Evidence ranking weights"]
        SM3["Confidence thresholds"]
    end

    subgraph "Requires Human Approval"
        HA1["New tools"]
        HA2["Service map changes"]
        HA3["Routing rules"]
        HA4["Security policy changes"]
    end

    style SM1 fill:#cfc,stroke:#3c3,color:#333
    style SM2 fill:#cfc,stroke:#3c3,color:#333
    style SM3 fill:#cfc,stroke:#3c3,color:#333
    style HA1 fill:#ffc,stroke:#cc3,color:#333
    style HA2 fill:#ffc,stroke:#cc3,color:#333
    style HA3 fill:#ffc,stroke:#cc3,color:#333
    style HA4 fill:#fcc,stroke:#c33,color:#333
```

## When to Aim Beyond Level 5

```mermaid
flowchart TD
    Q1{"Incident volume<br/>> 100/day?"} -->|No| STAY["Stay at Level 4-5<br/>Sufficient for most teams"]
    Q1 -->|Yes| Q2{"Incidents cross<br/>multiple domains?"}
    Q2 -->|No| L5["Level 5 is enough<br/>Single expert agent"]
    Q2 -->|Yes| Q3{"Human review<br/>bandwidth exhausted?"}
    Q3 -->|No| L6_LITE["Level 6 lite:<br/>parallel agents,<br/>human merges results"]
    Q3 -->|Yes| L6_FULL["Full Level 6:<br/>automated conflict<br/>resolution needed"]

    L6_FULL --> Q4{"Outcome data<br/>available for learning?"}
    Q4 -->|No| STOP["Collect outcome data first"]
    Q4 -->|Yes| L7["Level 7:<br/>Self-improving system"]

    style STAY fill:#cfc,stroke:#3c3,color:#333
    style L5 fill:#ccf,stroke:#33c,color:#333
    style L6_LITE fill:#ecf,stroke:#93c,color:#333
    style L6_FULL fill:#ecf,stroke:#93c,color:#333
    style L7 fill:#fce,stroke:#c39,color:#333
    style STOP fill:#fec,stroke:#c93,color:#333
```

## Caveats

1. **Levels 6-7 are extrapolations**, not observed implementations. They represent where the field is heading based on research patterns and multi-agent frameworks (LangGraph, CrewAI, AutoGen).

2. **Premature sophistication is an anti-pattern.** Most teams should aim for Level 3-4 and stay there until they have clear evidence that Level 5+ is needed. See [008-anti-patterns.md](008-anti-patterns.md).

3. **Self-improvement requires outcome data.** If you can't measure whether a triage was accurate (human closes the loop), you can't learn from it. Collect outcome data at Level 4 before attempting Level 7.

---

*Previous: [006 — Level 5: Autonomous Investigation](006-level-5-autonomous-investigation.md) | Next: [008 — Anti-Patterns](008-anti-patterns.md)*
