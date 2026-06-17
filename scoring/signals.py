"""Signal detection patterns for lead scoring.

Each signal is a (name, regex_pattern, points) tuple.
Patterns are case-insensitive by default.
"""

import re
from typing import Pattern

SignalDef = tuple[str, str, int]


def _compile(name: str, pattern: str, points: int) -> tuple[str, Pattern[str], int]:
    return (name, re.compile(pattern, re.IGNORECASE), points)


# ── Positive signals ──

POSITIVE_SIGNALS: list[tuple[str, Pattern[str], int]] = [
    _compile(
        "real_time_dsp",
        r"\b(?:c\+\+|rust)\b.*\b(?:dsp|real[\s-]?time|realtime)\b",
        5,
    ),
    _compile("plugin_format", r"\b(?:vst3|clap|ara2?|au|audio\s*unit)\b", 5),
    _compile(
        "ml_neural",
        r"\b(?:onnx|libtorch|mamba|ssm|state\s*space|neural|ml\s*inference|machine\s*learning)\b",
        8,
    ),
    _compile("rust_audio", r"\b(?:nih[\s-]?plug|clap[\s-]?rs|rust\s*audio|rust\s*plugin)\b", 6),
    _compile("reaper_work", r"\b(?:reaper|reascript|reascripts|lua\s*script|sws\s*extension|custom\s*action|daw\s*automation|reaak|reapack)\b", 5),
    _compile(
        "edge_inference",
        r"\b(?:on[\s-]?device|edge|cpu[\s-]?only|no\s*cloud|offline\s*inference)\b",
        5,
    ),
    _compile("low_latency", r"\b(?:low\s*latency|<5ms|<1ms|real[\s-]?time\s*constraint)\b", 4),
    _compile(
        "remote_pnw",
        r"\b(?:remote|vancouver|pacific\s*time|pst|pdt)\b",
        3,
    ),
]

# ── Negative signals ──

NEGATIVE_SIGNALS: list[tuple[str, Pattern[str], int]] = [
    _compile("below_floor", r"\$\s*\d{1,3}\s*(?:per\s*year|annually|annual)", -15),
    _compile("gui_only", r"\bprojucer\b.*\bgui\b(?!.*\b(?:dsp|audio|signal)\b)", -3),
    _compile("mac_only", r"\b(?:mac\s*only|macos\s*only|dante)\b", -10),
]

# ── Hard skip keywords (any match = SKIP immediately) ──

HARD_SKIP_KEYWORDS: list[str] = [
    "revenue share",
    "equity only",
    "profit share",
    "free work",
    "for exposure",
    "unpaid",
    "volunteer",
    "sweat equity",
]


def check_hard_skip(text: str) -> bool:
    """Return True if text matches any hard-skip keyword."""
    lower = text.lower()
    return any(kw in lower for kw in HARD_SKIP_KEYWORDS)


def extract_signals(
    text: str,
    signals: list[tuple[str, Pattern[str], int]],
) -> dict[str, int]:
    """Run regex patterns against text, return dict of matched signal -> points."""
    result: dict[str, int] = {}
    for name, pattern, points in signals:
        if pattern.search(text):
            result[name] = points
    return result