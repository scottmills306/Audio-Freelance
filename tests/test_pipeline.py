"""Tests for graph/pipeline.py — LangGraph pipeline integration."""

import pytest

from graph.state import PipelineState
from graph.pipeline import build_pipeline, search_all, route_by_verdict
from search.base import RawCandidate
from leads.schema import Lead


def test_pipeline_state_type():
    """PipelineState should accept all expected fields."""
    state: PipelineState = {
        "niche": "plugin_dev",
        "max_leads_per_tier": 5,
        "all_candidates": [],
        "deduped_candidates": [],
        "leads": [],
        "hot_leads": [],
        "warm_leads": [],
        "cold_leads": [],
        "skipped_leads": [],
        "errors": [],
    }
    assert state["niche"] == "plugin_dev"
    assert state["max_leads_per_tier"] == 5


def test_route_by_verdict_hot():
    state: PipelineState = {
        "hot_leads": [Lead(
            source="test", tier=1, title="Hot",
            url="https://x.com", raw_text="test", niche="plugin_dev",
            verdict="HOT",
        )],
        "warm_leads": [],
    }
    assert route_by_verdict(state) == "hot_path"


def test_route_by_verdict_warm():
    state: PipelineState = {
        "hot_leads": [],
        "warm_leads": [Lead(
            source="test", tier=1, title="Warm",
            url="https://x.com", raw_text="test", niche="plugin_dev",
            verdict="WARM",
        )],
    }
    assert route_by_verdict(state) == "warm_path"


def test_route_by_verdict_cold():
    state: PipelineState = {
        "hot_leads": [],
        "warm_leads": [],
        "cold_leads": [Lead(
            source="test", tier=1, title="Cold",
            url="https://x.com", raw_text="test", niche="plugin_dev",
            verdict="COLD",
        )],
    }
    assert route_by_verdict(state) == "cold_path"


@pytest.mark.asyncio
async def test_search_all_graceful():
    """search_all should gracefully handle no-op case (all APIs down)."""
    state: PipelineState = {
        "niche": "plugin_dev",
        "max_leads_per_tier": 2,
    }
    result = await search_all(state)
    assert isinstance(result, dict)
    assert "all_candidates" in result
    assert isinstance(result["all_candidates"], list)


@pytest.mark.asyncio
async def test_build_pipeline():
    """Pipeline graph should compile without error."""
    graph = build_pipeline()
    assert graph is not None
    # Graph should have the expected nodes
    assert hasattr(graph, "get_graph")
