"""Scoring layer: signal detection, lead scoring, Tier 4 fit-score."""

from scoring.score import score_candidate
from scoring.signals import POSITIVE_SIGNALS, NEGATIVE_SIGNALS, HARD_SKIP_KEYWORDS
from scoring.fit_score import score_company_fit

__all__ = [
    "score_candidate",
    "score_company_fit",
    "POSITIVE_SIGNALS",
    "NEGATIVE_SIGNALS",
    "HARD_SKIP_KEYWORDS",
]