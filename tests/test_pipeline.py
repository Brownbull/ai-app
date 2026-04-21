"""Tests for the full triage pipeline.

Injection-blocking is enforced at the API boundary (see tests/test_api.py).
Do not duplicate that coverage here — the pipeline trusts its single caller.
"""

import pytest

from app.agent.pipeline import run_triage_pipeline


@pytest.mark.asyncio
async def test_pipeline_happy_path():
    result = await run_triage_pipeline("test-001", {
        "title": "Checkout failing with 500 error",
        "description": "Users report checkout page crashes",
        "reporter_email": "ops@example.com",
        "attachments": [],
    })
    assert result["status"] == "completed"
