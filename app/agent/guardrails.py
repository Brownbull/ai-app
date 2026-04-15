"""Stage 2 (GUARDRAILS): Pre-compiled regex patterns for prompt injection.

Follows agent-security.md rule 1: Pre-compiled regex patterns (<5ms, 15+ patterns).
"""

import re

INJECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+a", re.IGNORECASE),
    re.compile(r"system\s*prompt", re.IGNORECASE),
    re.compile(r"</?(system|user|assistant)>", re.IGNORECASE),
    re.compile(r"ADMIN\s*MODE", re.IGNORECASE),
    re.compile(r"override\s+(safety|security|rules)", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
    re.compile(r"pretend\s+you", re.IGNORECASE),
    re.compile(r"act\s+as\s+(if|a)", re.IGNORECASE),
    re.compile(r"forget\s+(everything|all)", re.IGNORECASE),
    re.compile(r"new\s+instructions?:", re.IGNORECASE),
    re.compile(r"disregard\s+(all|previous)", re.IGNORECASE),
    re.compile(r"bypass\s+(filter|safety|moderation)", re.IGNORECASE),
    re.compile(r"reveal\s+(your|the)\s+(prompt|instructions)", re.IGNORECASE),
    re.compile(r"what\s+is\s+your\s+system\s+prompt", re.IGNORECASE),
]


def check_input_safety(text: str) -> dict[str, object]:
    """Check text against injection patterns. Fail-closed: block on match."""
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            return {"safe": False, "reason": f"Input matched safety pattern: {pattern.pattern}"}
    return {"safe": True, "reason": None}
