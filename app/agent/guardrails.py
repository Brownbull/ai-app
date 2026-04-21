"""Stage 2 (GUARDRAILS): Pre-compiled regex patterns for prompt injection.

Follows agent-security.md rule 1: Pre-compiled regex patterns (<5ms, 25 patterns).
"""

import re
from typing import TypedDict

# Each pattern is a (name, compiled_regex) tuple for logging matched pattern names.
_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # --- Original 15 patterns ---
    ("ignore_previous", re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE)),
    ("role_impersonation", re.compile(r"you\s+are\s+now\s+a", re.IGNORECASE)),
    ("system_prompt_probe", re.compile(r"system\s*prompt", re.IGNORECASE)),
    ("xml_role_tags", re.compile(r"</?(system|user|assistant)>", re.IGNORECASE)),
    ("admin_mode", re.compile(r"ADMIN\s*MODE", re.IGNORECASE)),
    ("override_safety", re.compile(r"override\s+(safety|security|rules)", re.IGNORECASE)),
    ("jailbreak", re.compile(r"jailbreak", re.IGNORECASE)),
    ("pretend", re.compile(r"pretend\s+you", re.IGNORECASE)),
    ("act_as", re.compile(r"act\s+as\s+(if|a)", re.IGNORECASE)),
    ("forget_all", re.compile(r"forget\s+(everything|all)", re.IGNORECASE)),
    ("new_instructions", re.compile(r"new\s+instructions?:", re.IGNORECASE)),
    ("disregard", re.compile(r"disregard\s+(all|previous)", re.IGNORECASE)),
    ("bypass_filter", re.compile(r"bypass\s+(filter|safety|moderation)", re.IGNORECASE)),
    ("reveal_prompt", re.compile(r"reveal\s+(your|the)\s+(prompt|instructions)", re.IGNORECASE)),
    ("ask_system_prompt", re.compile(r"what\s+is\s+your\s+system\s+prompt", re.IGNORECASE)),
    # --- Phase 1: role separators ---
    ("role_separator_human", re.compile(r"\n\nHuman:", re.IGNORECASE)),
    ("role_separator_assistant", re.compile(r"\n\nAssistant:", re.IGNORECASE)),
    # --- Phase 1: token markers ---
    ("token_marker_im", re.compile(r"<\|im_start\|>", re.IGNORECASE)),
    ("token_marker_system", re.compile(r"<\|system\|>", re.IGNORECASE)),
    ("token_marker_bracket", re.compile(r"\[SYSTEM\]", re.IGNORECASE)),
    # --- Phase 1: emphasis bypass ---
    ("emphasis_bypass", re.compile(r"IMPORTANT:\s*ignore", re.IGNORECASE)),
    # --- Phase 1: SQL injection ---
    ("sql_drop", re.compile(r";\s*DROP\s+TABLE", re.IGNORECASE)),
    ("sql_union", re.compile(r"UNION\s+SELECT", re.IGNORECASE)),
    # --- Phase 1: code execution ---
    # Require a string literal arg (single/double/triple quote) so we catch
    # *injection attempts* like `eval('rm -rf /')` but NOT legit SRE
    # incident reports that mention `eval() raised TypeError` in a stack trace.
    ("code_import", re.compile(r"""__import__\s*\(\s*['"]""", re.IGNORECASE)),
    ("code_eval", re.compile(r"""eval\s*\(\s*['"]""", re.IGNORECASE)),
    ("code_exec", re.compile(r"""exec\s*\(\s*['"]""", re.IGNORECASE)),
]

DESCRIPTION_MAX_CHARS = 8000


def _sanitize(text: str) -> str:
    """Strip control characters and collapse excessive newlines."""
    # Remove ASCII control chars except newline/tab
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Collapse 3+ consecutive newlines to 2
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


class SafetyResult(TypedDict):
    safe: bool
    matched: list[str]
    sanitized: str
    warning: str | None


def check_input_safety(text: str) -> SafetyResult:
    """Check text against injection patterns. Fail-closed: block on match.

    Length over DESCRIPTION_MAX_CHARS produces a warning but does NOT block.
    """
    sanitized = _sanitize(text)
    matched: list[str] = []
    for name, pattern in _PATTERNS:
        if pattern.search(sanitized):
            matched.append(name)

    warning: str | None = None
    if len(sanitized) > DESCRIPTION_MAX_CHARS:
        warning = f"Input exceeds {DESCRIPTION_MAX_CHARS} chars ({len(sanitized)}). Consider shortening."

    return SafetyResult(
        safe=len(matched) == 0,
        matched=matched,
        sanitized=sanitized,
        warning=warning,
    )
