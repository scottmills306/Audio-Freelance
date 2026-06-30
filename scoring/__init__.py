"""Scoring layer: signal detection, lead scoring, Tier 4 fit-score."""

from scoring.fit_score import score_company_fit
from scoring.score import score_candidate
from scoring.signals import HARD_SKIP_KEYWORDS, NEGATIVE_SIGNALS, POSITIVE_SIGNALS

__all__ = [
    "score_candidate",
    "score_company_fit",
    "POSITIVE_SIGNALS",
    "NEGATIVE_SIGNALS",
    "HARD_SKIP_KEYWORDS",
]
