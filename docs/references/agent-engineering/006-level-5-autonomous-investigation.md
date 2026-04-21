# 006 — Level 5: Autonomous Investigation

**The frontier.** The agent drives its own investigation strategy — planning what to search, adapting based on findings, and self-correcting when confidence is low. No finalist fully achieved this level. #9 (Team Omar) came closest.

---

## What Level 5 Looks Like

```mermaid
sequenceDiagram
    participant INC as Incident
    participant AGENT as Agent (Autonomous)
    participant TOOLS as Tool Suite
    participant VERIFY as Verification Loop

    INC->>AGENT: Incident + pre-classified context

    loop Investigation (max 8 iterations)
        AGENT->>AGENT: Plan next search action
        AGENT->>TOOLS: Execute planned search
        TOOLS-->>AGENT: Results
        AGENT->>AGENT: Analyze findings
        AGENT->>AGENT: Update hypothesis
        AGENT->>AGENT: Assess confidence

        alt Confidence >= threshold
            AGENT->>VERIFY: Submit hypothesis for verification
        else Low confidence + iterations remaining
            AGENT->>AGENT: Revise plan, search different angle
        end
    end

    VERIFY->>VERIFY: Cross-check evidence against hypothesis
    alt Verified
        VERIFY-->>INC: Confirmed root cause + evidence chain
    else Not verified
        VERIFY-->>INC: Best hypothesis + uncertainty markers
    end
```

## The Active Retrieval Pattern

Inspired by OpenAI Codex's approach to code understanding. The agent doesn't follow a fixed search sequence — it plans, executes, and adapts.

```mermaid
flowchart TD
    START["Incident + Context"] --> PLAN["PLAN<br/>What do I need to find?<br/>Which files might contain the answer?<br/>What search terms map to this error?"]

    PLAN --> SEARCH["SEARCH<br/>Execute planned searches<br/>(Grep, Glob, targeted queries)"]

    SEARCH --> INSPECT["INSPECT<br/>Read matched files<br/>Extract relevant code sections<br/>Note dependencies and imports"]

    INSPECT --> DIAGNOSE["DIAGNOSE<br/>Form root cause hypothesis<br/>Identify affected components<br/>Map blast radius"]

    DIAGNOSE --> ASSESS{Confidence<br/>assessment}

    ASSESS -->|"High (>= 0.8)"| EMIT["Emit triage result<br/>with evidence chain"]
    ASSESS -->|"Medium (0.6-0.8)"| REFINE["Refine: search adjacent<br/>files and dependencies"]
    ASSESS -->|"Low (< 0.6)"| REPLAN["Re-plan: different<br/>search strategy entirely"]

    REFINE --> SEARCH
    REPLAN --> PLAN

    REFINE -.->|"iteration count"| GUARD{Max iterations<br/>reached?}
    REPLAN -.->|"iteration count"| GUARD
    GUARD -->|Yes| FALLBACK["Emit best hypothesis<br/>+ flag for human review"]

    style PLAN fill:#ccf,stroke:#33c,color:#333
    style SEARCH fill:#cef,stroke:#39c,color:#333
    style INSPECT fill:#cfc,stroke:#3c3,color:#333
    style DIAGNOSE fill:#ffc,stroke:#cc3,color:#333
    style EMIT fill:#cfc,stroke:#3c3,color:#333
    style FALLBACK fill:#fec,stroke:#c93,color:#333
```

## Self-Correction Mechanism

Level 5 agents don't just report confidence — they act on it.

```mermaid
stateDiagram-v2
    [*] --> Investigating

    Investigating --> HighConfidence: confidence >= 0.8
    Investigating --> MediumConfidence: 0.6 <= confidence < 0.8
    Investigating --> LowConfidence: confidence < 0.6

    HighConfidence --> Emit: Submit with evidence
    MediumConfidence --> Refine: Search adjacent code
    LowConfidence --> Replan: New search strategy

    Refine --> Investigating: Re-assess
    Replan --> Investigating: Re-assess

    Investigating --> BudgetExhausted: max iterations hit
    BudgetExhausted --> HumanEscalation: Route to SRE-Triage

    Emit --> [*]
    HumanEscalation --> [*]
```

**Contrast with Level 3-4**: At those levels, the agent searches within a fixed scope and reports whatever it finds. At Level 5, the agent evaluates its own findings and changes strategy if they're insufficient.

## Investigation Budget Management

```mermaid
gantt
    title Tool Call Budget Over Time (Level 5 Agent)
    dateFormat X
    axisFormat %s

    section Iteration 1
    Plan search strategy       :a1, 0, 1
    Grep for error patterns    :a2, 1, 2
    Read 2 matched files       :a3, 2, 4
    Assess: confidence 0.4     :a4, 4, 5

    section Iteration 2 (replanned)
    Grep for dependency chain  :b1, 5, 6
    Read upstream service      :b2, 6, 7
    Read config file           :b3, 7, 8
    Assess: confidence 0.7     :b4, 8, 9

    section Iteration 3 (refined)
    Grep for recent changes    :c1, 9, 10
    Read changelog             :c2, 10, 11
    Assess: confidence 0.85    :c3, 11, 12
    Emit result                :c4, 12, 13
```

| Budget Type | Mechanism | Observed Limit |
|-------------|-----------|----------------|
| Iteration count | Counter in tool-use loop | max 8 (#11) |
| Tool call count | Hard limit per investigation | max 20 (#10) |
| File read limit | Max lines per file read | 500 lines (#10) |
| Time budget | Wall-clock timeout | 180s typical |

## Multi-Agent Collaboration (Emerging)

No finalist fully implemented this, but the architecture is visible in #9's approach:

```mermaid
flowchart TD
    ORCH["Orchestrator Agent"] --> PLAN_A["Planner Agent<br/>Decides investigation strategy"]
    ORCH --> SEARCH_A["Searcher Agent<br/>Executes code searches"]
    ORCH --> DIAG_A["Diagnostician Agent<br/>Analyzes evidence"]
    ORCH --> VERIFY_A["Verifier Agent<br/>Confirms/refutes hypothesis"]

    PLAN_A -->|search plan| SEARCH_A
    SEARCH_A -->|evidence| DIAG_A
    DIAG_A -->|hypothesis| VERIFY_A
    VERIFY_A -->|"confirmed/refuted"| ORCH

    ORCH -->|"if refuted"| PLAN_A

    style ORCH fill:#ffc,stroke:#cc3,color:#333
    style PLAN_A fill:#ccf,stroke:#33c,color:#333
    style SEARCH_A fill:#cef,stroke:#39c,color:#333
    style DIAG_A fill:#cfc,stroke:#3c3,color:#333
    style VERIFY_A fill:#fec,stroke:#c93,color:#333
```

**Handoff protocol**: Each agent's output becomes the next agent's input with explicit schema. The orchestrator manages iteration budget and decides when to stop.

## Learning from Past Incidents (Beyond Dedup)

Level 4 has deduplication (same incident = same triage). Level 5 extracts patterns:

```mermaid
flowchart TD
    subgraph "Level 4: Deduplication"
        D1["New incident"] --> D2{"Similar recent<br/>incident?"}
        D2 -->|Yes| D3["Inject prior triage<br/>as hypothesis"]
        D2 -->|No| D4["Fresh investigation"]
    end

    subgraph "Level 5: Pattern Extraction"
        P1["Completed triage"] --> P2["Extract pattern:<br/>error_type → root_cause → affected_service"]
        P2 --> P3["Store in pattern database"]
        P3 --> P4["Future incidents query patterns<br/>even outside time window"]
        P4 --> P5["Agent starts with relevant<br/>historical patterns, not just recent duplicates"]
    end

    style D3 fill:#fec,stroke:#c93,color:#333
    style P5 fill:#cfc,stroke:#3c3,color:#333
```

## Evidence from Finalists

### #9 Team Omar (Closest to Level 5)
- "Codex-inspired active retrieval": plan → search → inspect → diagnose → verify
- LangGraph with 13 nodes and checkpoint-based recovery
- If confidence low, regenerates hypothesis once (single retry)
- Full investigation history preserved in LangGraph checkpoints
- **Gap**: Single retry, not iterative refinement. No pattern extraction.

### #11 AgenticTulkuns (Partial Level 5)
- Tool-use loop with max 8 iterations
- Agent decides when to stop based on accumulated evidence
- **Gap**: No explicit confidence assessment or self-correction strategy

## Level 5 Checklist

- [ ] Agent plans its own investigation strategy (not following fixed search)
- [ ] Active retrieval: plan → search → inspect → diagnose → verify
- [ ] Confidence-driven self-correction (low = replan, medium = refine)
- [ ] Iteration budget with hard limits (max 8-20 tool calls)
- [ ] Investigation history preserved for audit
- [ ] Multi-agent handoff protocol (emerging, not required)
- [ ] Pattern extraction from completed triages (emerging)
- [ ] Time/cost budget management (wall-clock + token tracking)

## The Gap to Level 5

What makes Level 5 hard:

| Challenge | Why It's Hard |
|-----------|--------------|
| Unpredictable latency | Investigation length varies by incident complexity |
| Cost bounding | More iterations = more tokens = more cost |
| Quality assessment | Agent must judge its own work (meta-cognition) |
| Strategy diversity | Agent needs multiple search strategies to switch between |
| Termination criteria | When is "enough evidence" enough? |

---

*Previous: [005 — Level 4: Production Pipeline](005-level-4-production-pipeline.md) | Next: [007 — Beyond Level 5](007-beyond-level-5.md)*
