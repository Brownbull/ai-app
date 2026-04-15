"""Tests for severity classification."""

import pytest

from app.agent.classify import classify_severity


@pytest.mark.asyncio
async def test_critical_classification():
    result = await classify_severity({"title": "Production database is down"})
    assert result.severity == "critical"


@pytest.mark.asyncio
async def test_high_classification():
    result = await classify_severity({"title": "API returning 500 errors on checkout"})
    assert result.severity == "high"


@pytest.mark.asyncio
async def test_medium_classification():
    result = await classify_severity({"title": "Performance warning on search page"})
    assert result.severity == "medium"


@pytest.mark.asyncio
async def test_low_classification():
    result = await classify_severity({"title": "Update documentation for API endpoints"})
    assert result.severity == "low"


@pytest.mark.asyncio
async def test_classification_output_structure():
    result = await classify_severity({"title": "Server crash"})
    assert hasattr(result, "severity")
    assert hasattr(result, "category")
    assert hasattr(result, "confidence")
    assert hasattr(result, "reasoning")
    assert 0.0 <= result.confidence <= 1.0
