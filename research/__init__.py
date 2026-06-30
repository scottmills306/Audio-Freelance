"""Market research layer: opportunity signals, tech trends, pricing intelligence."""

from research.market import (
    MarketReport,
    MarketSignal,
    extract_pricing_benchmarks,
    extract_tech_trends,
    generate_report,
    run_market_scan,
)

__all__ = [
    "MarketSignal",
    "MarketReport",
    "run_market_scan",
    "extract_tech_trends",
    "extract_pricing_benchmarks",
    "generate_report",
]
