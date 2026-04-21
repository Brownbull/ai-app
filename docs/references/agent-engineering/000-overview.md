# 000 — Agent Engineering Maturity Model: Overview

**Source**: Analysis of 12 SRE triage agents (11 finalists + 1 submission), AgentX Hackathon 2026
**Purpose**: A framework for evaluating and improving AI agent implementations
**Reading order**: Start here, then follow the level docs (002-006) in order

---

## What Is This?

The Agent Engineering Maturity Model is a 5-level framework distilled from analyzing 12 production-intent agent implementations. Each level represents a distinct leap in reliability, cost-efficiency, and autonomy.

The model is **additive** — each level builds on the previous. You don't skip levels; you climb them.

## The Staircase

```mermaid
graph TB
    subgraph L5["Level 5: Autonomous Investigation"]
        L5D["Active retrieval loops<br/>Self-correction on low confidence<br/>Multi-agent collaboration"]
    end
    subgraph L4["Level 4: Production Pipeline"]
        L4D["Multi-model staged pipeline<br/>Checkpoint & recovery<br/>Defense-in-depth security<br/>Comprehensive observability"]
    end
    subgraph L3["Level 3: Context-Engineered Agent"]
        L3D["Pre-built domain knowledge<br/>Classification-driven scoping<br/>Evidence ranking<br/>Cost tracking & model routing"]
    end
    subgraph L2["Level 2: Structured Agent"]
        L2D["Framework-enforced output<br/>Deterministic fallback chain<br/>Input guardrails (regex)<br/>Background processing (202)"]
    end
    subgraph L1["Level 1: Prompt & Parse"]
        L1D["Single LLM call<br/>Parse JSON from text<br/>No tools, no fallbacks"]
    end

    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5

    style L1 fill:#fee,stroke:#c33,color:#333
    style L2 fill:#fec,stroke:#c93,color:#333
    style L3 fill:#ffc,stroke:#cc3,color:#333
    style L4 fill:#cfc,stroke:#3c3,color:#333
    style L5 fill:#ccf,stroke:#33c,color:#333
```

## Where the Finalists Landed

```mermaid
graph LR
    subgraph "Level 1"
        N1["(No finalists)"]
    end
    subgraph "Level 2"
        F3["#3 AgentNOOB"]
        F4["#4 ARIA"]
    end
    subgraph "Level 3"
        F1["#1 cszdiego"]
        F8["#8 Penguin Alley"]
    end
    subgraph "Level 4"
        F2["#2 jjovalle99"]
        F5["#5 Core Tech"]
    end
    subgraph "Level 5 (partial)"
        F9["#9 Team Omar"]
    end

    style N1 fill:#fee,stroke:#c33,color:#999
    style F3 fill:#fec,stroke:#c93,color:#333
    style F4 fill:#fec,stroke:#c93,color:#333
    style F1 fill:#ffc,stroke:#cc3,color:#333
    style F8 fill:#ffc,stroke:#cc3,color:#333
    style F2 fill:#cfc,stroke:#3c3,color:#333
    style F5 fill:#cfc,stroke:#3c3,color:#333
    style F9 fill:#ccf,stroke:#33c,color:#333
```

**Key observation**: No finalist was at Level 1. The minimum bar for a competitive agent is Level 2. The winners operated at Level 3-4. No one fully achieved Level 5.

## The Capability Map

Each level introduces specific capabilities. Here's what unlocks at each stage:

```mermaid
mindmap
  root((Agent Maturity))
    Level 1
      Single LLM call
      Text parsing
      No error recovery
    Level 2
      Structured output
      Fallback chains
      Input guardrails
      Async processing
    Level 3
      Service maps
      Context scoping
      Tool discipline
      Real integrations
      Cost awareness
    Level 4
      Multi-model routing
      Staged context assembly
      Checkpoints
      5-layer security
      Full observability
      Temporal memory
    Level 5
      Plan-driven retrieval
      Self-correction loops
      Hypothesis verification
      Pattern extraction
```

## Document Map

| Doc | Title | What You'll Learn |
|-----|-------|-------------------|
| [001](001-architecture-taxonomy.md) | Architecture Taxonomy | The 4 architecture patterns and when to use each |
| [002](002-level-1-prompt-and-parse.md) | Level 1: Prompt & Parse | The baseline — what to move past quickly |
| [003](003-level-2-structured-agent.md) | Level 2: Structured Agent | Your first real agent — output enforcement + safety |
| [004](004-level-3-context-engineered.md) | Level 3: Context-Engineered | The quality leap — controlling what the LLM sees |
| [005](005-level-4-production-pipeline.md) | Level 4: Production Pipeline | Multi-model, multi-stage, production-grade |
| [006](006-level-5-autonomous-investigation.md) | Level 5: Autonomous Investigation | The frontier — agent-driven exploration |
| [007](007-beyond-level-5.md) | Beyond Level 5 | Emerging patterns not yet observed in production |
| [008](008-anti-patterns.md) | Anti-Patterns | What NOT to do — categorized by level |
| [009](009-implementation-roadmap.md) | Implementation Roadmap | Step-by-step guide to climbing the levels |

## How to Use This

**If you're building your first agent**: Read 001, then 002-003. Implement Level 2 before anything else.

**If you're improving an existing agent**: Find your current level, read the next level doc, and implement the capabilities in order.

**If you're evaluating agents**: Use the maturity model to score implementations. The level grid in each doc provides a checklist.

---

*Next: [001 — Architecture Taxonomy](001-architecture-taxonomy.md)*
