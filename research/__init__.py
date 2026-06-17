"""Market research layer: opportunity signals, tech trends, pricing intelligence."""

from research.market import (
    MarketSignal,
    MarketReport,
    run_market_scan,
    extract_tech_trends,
    extract_pricing_benchmarks,
    generate_report,
)

__all__ = [
    "MarketSignal",
    "MarketReport",
    "run_market_scan",
    "extract_tech_trends",
    "extract_pricing_benchmarks",
    "generate_report",
]
