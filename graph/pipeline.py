"""Pipeline: search → dedup → score → route.

Uses direct async orchestration instead of LangGraph for reliability.
LangGraph wrapper provided for future graph-based extensions.
"""

import asyncio
from typing import Any

from graph.state import PipelineState
from leads.schema import Lead, LeadStatus
from leads.store import check_duplicate, upsert_lead
from search import run_tier1, run_tier2, run_tier3, run_tier4
from search.base import RawCandidate
from scoring.score import score_candidate


async def run_pipeline(niche: str, max_per_tier: int = 10) -> PipelineState:
    """Run full pipeline: search → dedup → score.

    Returns final PipelineState with all results.
    """
    state: PipelineState = {
        "niche": niche,
        "max_leads_per_tier": max_per_tier,
        "tier1_candidates": [],
        "tier2_candidates": [],
        "tier3_candidates": [],
        "tier4_candidates": [],
        "all_candidates": [],
        "deduped_candidates": [],
        "leads": [],
        "hot_leads": [],
        "warm_leads": [],
        "cold_leads": [],
        "skipped_leads": [],
        "errors": [],
    }

    # ── Phase 1: Search all tiers ──
    results = await asyncio.gather(
        run_tier1(niche),
        run_tier2(niche),
        run_tier3(niche),
        run_tier4(niche),
        return_exceptions=True,
    )

    tier_keys = ["tier1_candidates", "tier2_candidates", "tier3_candidates", "tier4_candidates"]
    all_candidates: list[RawCandidate] = []

    for key, result in zip(tier_keys, results):
        if isinstance(result, Exception):
            state["errors"].append(f"{key} failed: {result}")
            state[key] = []
        else:
            candidates = result[:max_per_tier]
            state[key] = candidates
            all_candidates.extend(candidates)

    state["all_candidates"] = all_candidates

    # ── Phase 2: Dedup ──
    deduped: list[RawCandidate] = []
    for c in all_candidates:
        temp = Lead(
            source=c.source,
            tier=c.tier,
            title=c.title,
            url=c.url,
            raw_text=c.raw_text or c.snippet,
            niche=niche,
        )
        dup_id = check_duplicate(temp)
        if dup_id is None:
            deduped.append(c)
    state["deduped_candidates"] = deduped

    # ── Phase 3: Score ──
    leads: list[Lead] = []
    hot: list[Lead] = []
    warm: list[Lead] = []
    cold: list[Lead] = []
    skipped: list[Lead] = []

    for c in deduped:
        lead = score_candidate(c, niche)
        leads.append(lead)
        if lead.verdict == "HOT":
            hot.append(lead)
        elif lead.verdict == "WARM":
            warm.append(lead)
        elif lead.verdict == "COLD":
            cold.append(lead)
        else:
            skipped.append(lead)

        try:
            upsert_lead(lead)
        except Exception:
            pass

    state["leads"] = leads
    state["hot_leads"] = hot
    state["warm_leads"] = warm
    state["cold_leads"] = cold
    state["skipped_leads"] = skipped

    return state


# ── LangGraph wrapper (kept for future graph extensions) ──

from langgraph.graph import StateGraph, START, END


def build_pipeline() -> StateGraph:
    """Build LangGraph pipeline (experimental — use run_pipeline for production)."""
    builder = StateGraph(PipelineState)
    builder.add_node("run_pipeline", _langgraph_wrapper)
    builder.add_edge(START, "run_pipeline")
    builder.add_edge("run_pipeline", END)
    return builder.compile()


async def _langgraph_wrapper(state: PipelineState) -> dict[str, Any]:
    """Adapter node that calls the real pipeline."""
    result = await run_pipeline(
        niche=state.get("niche", "plugin_dev"),
        max_per_tier=state.get("max_leads_per_tier", 10),
    )
    return dict(result)


# ── LangGraph node functions (for graph-based workflow) ──


async def search_all(state: PipelineState) -> dict[str, Any]:
    """LangGraph node: search all tiers for candidates."""
    result = await run_pipeline(
        niche=state.get("niche", "plugin_dev"),
        max_per_tier=state.get("max_leads_per_tier", 10),
    )
    return {
        "all_candidates": result.get("all_candidates", []),
        "tier1_candidates": result.get("tier1_candidates", []),
        "tier2_candidates": result.get("tier2_candidates", []),
        "tier3_candidates": result.get("tier3_candidates", []),
        "tier4_candidates": result.get("tier4_candidates", []),
        "errors": result.get("errors", []),
    }


def route_by_verdict(state: PipelineState) -> str:
    """LangGraph conditional edge: route by verdict."""
    if state.get("hot_leads"):
        return "hot_path"
    if state.get("warm_leads"):
        return "warm_path"
    return "cold_path"
