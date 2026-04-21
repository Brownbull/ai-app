# 003 — Level 2: Structured Agent

**Your first real agent.** The output is guaranteed, the input is guarded, and failures don't crash the system.

---

## What Level 2 Looks Like

```mermaid
sequenceDiagram
    participant U as User
    participant API as API Server
    participant Guard as Input Guardrails
    participant LLM as LLM (with schema)
    participant FB as Fallback Chain

    U->>API: Submit incident
    API-->>U: 202 Accepted (processing in background)
    API->>Guard: Validate input (regex patterns)
    alt Input blocked
        Guard-->>API: Blocked (log violation)
        API->>API: Store rejection with reason
    else Input clean
        Guard-->>API: Passed
        API->>LLM: Triage request with enforced output schema
        LLM-->>API: Structured response
        alt Valid output
            API->>API: Store triage result
        else Invalid output
            API->>FB: Retry → Regex extract → Rule-based → Safe default
            FB-->>API: Usable output (always)
        end
    end
    API->>U: Result available (poll or webhook)
```

## Characteristics

| Capability | Level 2 Status |
|------------|---------------|
| Output format | Framework-enforced (PydanticAI / tool-use schema) |
| Error handling | Deterministic fallback chain — never returns empty |
| Input safety | Regex guardrails (10-15 compiled patterns, <5ms) |
| Tools | None or minimal lookup tools (2-4 deterministic) |
| Processing | Async — 202 Accepted, background task |
| Cost tracking | None yet |

## The Reliability Foundation

### Structured Output Enforcement

Two approaches, both effective:

```mermaid
flowchart TD
    subgraph "Approach 1: PydanticAI"
        PA1["Agent(model, output_type=TriageResult)"]
        PA1 --> PA2["Framework validates response<br/>against Pydantic model"]
        PA2 -->|Valid| PA3["Guaranteed schema"]
        PA2 -->|Invalid| PA4["Auto-retry (up to 2)"]
    end

    subgraph "Approach 2: Tool-Use Forcing"
        TU1["tools=[emit_triage with schema]"]
        TU1 --> TU2["tool_choice={type: tool,<br/>name: emit_triage}"]
        TU2 --> TU3["LLM MUST call this tool<br/>with valid arguments"]
        TU3 --> TU4["Response is always<br/>valid against schema"]
    end

    style PA3 fill:#cfc,stroke:#3c3,color:#333
    style TU4 fill:#cfc,stroke:#3c3,color:#333
```

**Who used what**:
- **PydanticAI approach**: #1 (cszdiego), #3 (AgentNOOB) — Gemini models
- **Tool-use forcing**: #2 (jjovalle99), #5 (Core Tech Expert) — Claude models

### The Fallback Chain

This is what separates Level 2 from Level 1. When structured output fails, the system degrades gracefully:

```mermaid
flowchart TD
    LLM["LLM Response"] --> V1{Framework<br/>validation?}
    V1 -->|Pass| OK["Valid result"]
    V1 -->|Fail| R1["Retry with same prompt<br/>(up to 2 retries)"]
    R1 --> V2{Retry<br/>succeeded?}
    V2 -->|Yes| OK
    V2 -->|No| R2["Regex JSON extraction<br/>(find first { to last })"]
    R2 --> V3{Valid<br/>JSON?}
    V3 -->|Yes| OK
    V3 -->|No| R3["Rule-based inference<br/>from keywords in text"]
    R3 --> V4{Could<br/>infer?}
    V4 -->|Yes| OK
    V4 -->|No| R4["Safe default<br/>team=SRE-Triage, severity=P3"]
    R4 --> OK

    style OK fill:#cfc,stroke:#3c3,color:#333
    style R4 fill:#fec,stroke:#c93,color:#333
```

**Critical rule**: NEVER return an empty result. NEVER crash. Every incident gets a usable triage, even if it's a conservative default routing to the generic SRE team.

### Input Guardrails

Pre-compiled regex patterns that run before any LLM call:

```mermaid
flowchart LR
    INPUT["User Input"] --> REG["Regex Guardrails<br/>(compiled, <5ms)"]
    REG -->|Clean| LLM["Proceed to LLM"]
    REG -->|Violation| LOG["Log: IP, timestamp,<br/>pattern matched<br/>(cap at 500 chars)"]
    LOG --> BLOCK["Block with<br/>safe error message"]

    style REG fill:#ffc,stroke:#cc3,color:#333
    style BLOCK fill:#fcc,stroke:#c33,color:#333
    style LLM fill:#cfc,stroke:#3c3,color:#333
```

**Patterns observed across finalists** (10-16 regex each):

| Category | Example Patterns |
|----------|-----------------|
| SQL injection | `DROP TABLE`, `UNION SELECT`, `; DELETE` |
| Code execution | `eval(`, `exec(`, `__import__` |
| Prompt injection | `ignore previous`, `system prompt`, `DAN` |
| Data exfiltration | `curl`, `wget`, base64 encoded URLs |
| Format manipulation | `<\|im_start\|>`, `[INST]`, `<system>` |

## Evidence from Finalists

### #3 AgentNOOB (Level 2)
- PydanticAI with `output_type=TriageResult`
- 13 compiled regex guardrail patterns
- Embedded knowledge base (Python dict) for service lookup
- Background processing via FastAPI BackgroundTasks

### #4 ARIA (Level 2)
- Gemini 2.0 Flash with structured output
- 16 regex guardrails including jailbreak detection
- 3-tier JSON extraction fallback
- Real integrations (Linear + Jira + Discord + SMTP)

## Level 2 Checklist

Before claiming Level 2:

- [ ] Output schema enforced by framework (not prompt instructions)
- [ ] Fallback chain: retry → regex extract → rule-based → safe default
- [ ] 10+ regex guardrail patterns compiled and tested
- [ ] Async processing (202 Accepted + background task)
- [ ] Guardrails run BEFORE any LLM call
- [ ] Violations logged with context (but content capped at 500 chars)
- [ ] No path where the system returns empty or crashes

## What Level 2 Is Missing

```mermaid
graph TB
    subgraph "Level 2 Has"
        H1["Structured output"]
        H2["Fallback chain"]
        H3["Input guardrails"]
        H4["Async processing"]
    end

    subgraph "Level 3 Adds"
        A1["Pre-built service map"]
        A2["Classification-driven search scoping"]
        A3["Evidence ranking + bounded context"]
        A4["Real integrations with graceful degradation"]
        A5["Cost tracking and model routing"]
        A6["Tool use with search discipline"]
    end

    H1 -.->|upgrade| A2
    H3 -.->|upgrade| A1
    H4 -.->|upgrade| A5

    style A1 fill:#cfc,stroke:#3c3,color:#333
    style A2 fill:#cfc,stroke:#3c3,color:#333
    style A3 fill:#cfc,stroke:#3c3,color:#333
    style A4 fill:#cfc,stroke:#3c3,color:#333
    style A5 fill:#cfc,stroke:#3c3,color:#333
    style A6 fill:#cfc,stroke:#3c3,color:#333
```

---

*Previous: [002 — Level 1: Prompt & Parse](002-level-1-prompt-and-parse.md) | Next: [004 — Level 3: Context-Engineered Agent](004-level-3-context-engineered.md)*
