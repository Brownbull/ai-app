# 002 — Level 1: Prompt & Parse

**The baseline.** This is where everyone starts — and where you should leave quickly.

---

## What Level 1 Looks Like

```mermaid
sequenceDiagram
    participant U as User
    participant App as Application
    participant LLM as LLM API

    U->>App: Submit incident
    App->>LLM: "Triage this incident: {text}<br/>Return JSON with severity, service, root_cause"
    LLM-->>App: "Here's the analysis:\n```json\n{...}\n```"
    App->>App: Try to parse JSON from response text
    alt Parse succeeds
        App-->>U: Show triage result
    else Parse fails
        App-->>U: Error / empty result / crash
    end
```

## Characteristics

| Capability | Level 1 Status |
|------------|---------------|
| Output format | Hope the LLM returns valid JSON |
| Error handling | Crash or return empty on parse failure |
| Input safety | None — raw user text goes to LLM |
| Tools | None — LLM reasons from prompt text only |
| Processing | Synchronous — user waits for full response |
| Cost tracking | None |

## The Core Problem

```mermaid
flowchart LR
    INPUT["User text"] --> LLM["LLM Call"]
    LLM --> PARSE["Parse JSON<br/>from text"]
    PARSE -->|Success ~85%| OK["Result"]
    PARSE -->|Fail ~15%| CRASH["Crash / Error"]

    style CRASH fill:#fcc,stroke:#c33,color:#333
    style OK fill:#cfc,stroke:#3c3,color:#333
```

At Level 1, roughly **15% of responses** will fail to parse correctly. The LLM might:
- Wrap JSON in markdown code fences
- Add explanatory text before/after the JSON
- Return partially valid JSON (trailing commas, single quotes)
- Hallucinate field names not in your prompt
- Return a completely different structure than requested

There is no fallback. When parsing fails, the user gets nothing.

## Why Nobody Stayed Here

None of the 12 analyzed implementations operated at Level 1. Even the simplest submissions had at least:
- Some form of structured output enforcement
- Basic input validation
- Background processing

This level exists as a reference point — it's where a "make the LLM do it" prototype starts. The gap between Level 1 and Level 2 is the difference between a demo that works sometimes and one that works reliably.

## What Level 1 Is Missing

```mermaid
graph TB
    subgraph "Level 1 Has"
        H1["Single LLM call"]
        H2["Text prompt with instructions"]
        H3["JSON parsing attempt"]
    end

    subgraph "Level 2 Adds"
        A1["Framework-enforced output schema"]
        A2["Deterministic fallback chain"]
        A3["Input guardrails (regex)"]
        A4["Async processing (202 Accepted)"]
        A5["Validation on LLM response fields"]
    end

    H1 -.->|upgrade| A1
    H3 -.->|upgrade| A2
    H2 -.->|upgrade| A3

    style H1 fill:#fee,stroke:#c33,color:#333
    style H2 fill:#fee,stroke:#c33,color:#333
    style H3 fill:#fee,stroke:#c33,color:#333
    style A1 fill:#cfc,stroke:#3c3,color:#333
    style A2 fill:#cfc,stroke:#3c3,color:#333
    style A3 fill:#cfc,stroke:#3c3,color:#333
    style A4 fill:#cfc,stroke:#3c3,color:#333
    style A5 fill:#cfc,stroke:#3c3,color:#333
```

## The Upgrade Path

Moving from Level 1 to Level 2 requires 3 changes:

1. **Enforce output schema** — Use PydanticAI `output_type` or Claude's `tool_choice` with a schema. Stop hoping the LLM cooperates.

2. **Add a fallback chain** — When the schema validation fails, retry once, then extract JSON with regex, then fall back to rule-based defaults. Never crash.

3. **Add input guardrails** — Compile 10-15 regex patterns (SQL injection, prompt injection, code execution). Run before any LLM call. Cost: <5ms.

Estimated effort: **2-4 hours** for a competent developer with framework experience.

---

*Previous: [001 — Architecture Taxonomy](001-architecture-taxonomy.md) | Next: [003 — Level 2: Structured Agent](003-level-2-structured-agent.md)*
