"""Main scoring pipeline: candidate → scored lead with verdict."""

import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from leads.schema import Lead, LeadStatus, Verdict, PREFERRED_NICHES
from search.base import RawCandidate
from scoring.signals import (
    check_hard_skip,
    extract_signals,
    POSITIVE_SIGNALS,
    NEGATIVE_SIGNALS,
)

# Lowered thresholds for real-world job market
_HOT_THRESHOLD = 10
_WARM_THRESHOLD = 5
_MIN_RATE_CAD = 3000
_HOURLY_FLOOR_CAD = 150


def _parse_budget(text: str) -> Optional[int]:
    patterns = [
        r"\$\s*((?:\d{4,10}|\d{1,3}(?:,\d{3})*))(?:\.\d{2})?\s*(?:cad|usd)?",
        r"(\d{4,5})\s*(?:cad|usd|dollars)",
        r"budget\s*(?:of\s*)?[:$]?\s*((?:\d{4,10}|\d{1,3}(?:,\d{3})*))",
        r"rate\s*(?:of\s*)?[:$]?\s*((?:\d{4,10}|\d{1,3}(?:,\d{3})*))",
        r"\b\$(\d{2,3}(?:,\d{3})*)\s*(?:/hr|/hour|\s*(?:per|an?)\s*hour)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = int(m.group(1).replace(",", ""))
            if val >= 100:
                return val
    return None


def score_candidate(
    candidate: RawCandidate,
    niche: str,
    min_rate: int = _MIN_RATE_CAD,
    hourly_floor: int = _HOURLY_FLOOR_CAD,
) -> Lead:
    combined_text = f"{candidate.title} {candidate.snippet} {candidate.raw_text}"

    # Step 1: Hard skip
    if check_hard_skip(combined_text):
        return Lead(
            source=candidate.source, tier=candidate.tier,
            title=candidate.title, company=candidate.company,
            url=candidate.url, raw_text=candidate.raw_text,
            niche=niche, signals={"hard_skip": -999},
            score=0, verdict="SKIP", status=LeadStatus.SKIPPED,
        )

    # Step 2: Extract signals
    signals: dict[str, int] = {}
    for name, points in extract_signals(combined_text, POSITIVE_SIGNALS).items():
        signals[name] = points
    for name, points in extract_signals(combined_text, NEGATIVE_SIGNALS).items():
        signals[name] = points

    # Step 3: Budget
    budget = _parse_budget(combined_text)
    if budget is not None:
        if budget >= min_rate:
            signals["budget_above_floor"] = 10
        else:
            signals["budget_below_floor"] = -15

    # Step 4: Verdict
    total = sum(signals.values())

    if total >= _HOT_THRESHOLD:
        verdict: Verdict = "HOT"
        status = LeadStatus.HOT
    elif total >= _WARM_THRESHOLD:
        verdict = "WARM"
        status = LeadStatus.WARM
    elif total > -500:
        verdict = "COLD"
        status = LeadStatus.COLD
    else:
        verdict = "SKIP"
        status = LeadStatus.SKIPPED

    return Lead(
        source=candidate.source, tier=candidate.tier,
        title=candidate.title, company=candidate.company,
        url=candidate.url, raw_text=candidate.raw_text,
        niche=niche, signals=signals, score=total,
        verdict=verdict, status=status,
    )
