"""Tier 4 company fit-score for outbound target qualification."""

import re
from typing import Optional

from search.base import RawCandidate


def score_company_fit(
    candidate: RawCandidate,
) -> int:
    """Score a company/startup candidate for cold-outbound fit.

    Returns a fit score (0-20+). Threshold: ≥10 → add to target list.
    """
    score = 0
    text = f"{candidate.title} {candidate.snippet} {candidate.raw_text}".lower()

    # Signal 1: Builds real-time audio product (+5)
    if re.search(
        r"\b(?:audio\s*plugin|daw|vst|clap|audio\s*engine|real[\s-]?time\s*audio|sound|music\s*prod)",
        text,
    ):
        score += 5

    # Signal 2: Needs ML/inference (+5)
    if re.search(
        r"\b(?:ml|machine\s*learning|ai|neural|inference|deep\s*learning|mamba|ssm|state\s*space)",
        text,
    ):
        score += 5

    # Signal 3: Small stage (≤~30 employees, recent funding, or no DSP team visible) (+5)
    if re.search(
        r"\b(?:seed|series\s*a|startup|small\s*team|\d+\s*employees?|founding|early\s*stage)",
        text,
    ):
        score += 5

    # Signal 4: Active public technical content (+3)
    if re.search(
        r"\b(?:engineering\s*blog|conference\s*talk|tech\s*blog|opensource|open[\s-]?source|github|technical\s*write)",
        text,
    ):
        score += 3

    return score