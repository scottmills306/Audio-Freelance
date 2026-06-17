"""Market intelligence: what's in demand, what people are paying, where the work is.

This module answers three questions:
  1. What are people actually paying developers to do?
  2. What technologies/skills are in demand right now?
  3. Where are the opportunity signals that aren't on job boards?

It searches across funding news, GitHub activity, product launches, tech trends,
and pricing data — then aggregates everything into a structured report.
"""

import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import httpx

from search.base import web_search, SearchResult


# ── Data types ──


@dataclass
class MarketSignal:
    """A single piece of market intelligence."""

    category: str  # funding | tech_trend | product_launch | pricing | hiring_signal
    source: str
    title: str
    url: str
    snippet: str
    relevance_score: int = 0  # 1-10
    tags: list[str] = field(default_factory=list)


@dataclass
class TechTrend:
    technology: str
    mention_count: int = 0
    contexts: list[str] = field(default_factory=list)
    direction: str = "neutral"  # rising | stable | declining


@dataclass
class PricingBenchmark:
    niche: str
    contract_range_min: int = 0
    contract_range_max: int = 0
    hourly_min: int = 0
    hourly_max: int = 0
    sample_count: int = 0
    sources: list[str] = field(default_factory=list)


@dataclass
class MarketReport:
    scanned_at: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )
    signals: list[MarketSignal] = field(default_factory=list)
    tech_trends: list[TechTrend] = field(default_factory=list)
    pricing_benchmarks: list[PricingBenchmark] = field(default_factory=list)
    hot_opportunities: list[str] = field(default_factory=list)
    summary: str = ""


# ── Intelligence-gathering queries ──


# 1. Funding & company activity (money raised = hiring soon)
FUNDING_QUERIES = [
    # Audio AI / music tech startups that raised
    '"audio AI" OR "music AI" OR "neural audio" raised OR funding OR series',
    '"audio startup" OR "music tech startup" raised OR funding OR "series" OR seed',
    # Plugin companies with new investment
    '"audio plugin" OR "VST" OR "CLAP" company funding OR acquisition OR raised',
    # Game audio middleware funding
    '"game audio" OR "audio middleware" OR "wwise" OR "fmod" funding OR acquisition',
    # YC / accelerator companies in audio
    'site:ycombinator.com companies audio OR music OR speech OR sound',
]

# 2. Technology trends & skills in demand
TREND_QUERIES = [
    # CLAP adoption
    '"CLAP plugin" OR "clap-audio" adoption OR "now supports" OR migrating OR "switching to" -discussion',
    # ARA adoption
    '"ARA 2" OR "ARA extension" OR "Audio Random Access" plugin OR DAW support',
    # Rust for audio
    '"nih-plug" OR "clap-rs" OR "rust audio" new release OR update OR shipped',
    # Mamba/SSM in audio
    '"mamba" OR "state space" OR "SSM" audio OR DSP OR music new OR benchmark OR release',
    # On-device ML inference
    '"on-device" OR "edge" OR "CPU-only" "audio" OR "DSP" OR "inference" model OR engine OR framework',
    # Neural audio codecs
    '"neural audio codec" OR "EnCodec" OR "SoundStream" OR "DAC" OR "descript audio codec"',
]

# 3. Product launches & new tools (opportunity = new product needs support/contractors)
LAUNCH_QUERIES = [
    # New audio plugins
    '"new audio plugin" OR "new VST" OR "new CLAP" release OR launched OR announced',
    # New DAW features / tools
    '"DAW" OR "audio workstation" new feature OR update OR release "beta" OR "shipped"',
    # Open source audio tools
    '"open source" audio OR DSP OR plugin new release OR "just shipped" OR launched',
    # AI music tools
    '"AI music" OR "AI audio" tool OR product OR app launch OR released OR announced',
    # REAPER related tools
    '"REAPER" extension OR theme OR script OR tool new release OR update OR shipped',
]

# 4. Pricing intelligence (what people are ACTUALLY paying)
PRICING_QUERIES = [
    # Contract rates from job posts
    '"audio DSP" OR "audio plugin" "budget" OR "rate" OR "$" contract OR freelance',
    '"REAPER" OR "reascript" OR "DAW" "budget" OR "rate" OR "$" contract OR freelance OR commission',
    '"rust audio" OR "nih-plug" "contract" OR "freelance" "$" OR "budget" OR "rate"',
    '"machine learning" audio OR music OR speech "contract" OR "freelance" "$" OR "rate"',
    # Freelance rate discussions
    '"freelance" OR "contract" "audio DSP" OR "plugin developer" rate OR "$" OR "charging" OR "per hour"',
]

# 5. Hiring signals (not job posts, but companies actively building audio teams)
HIRING_SIGNAL_QUERIES = [
    '"hiring" "audio engineer" OR "DSP engineer" OR "audio programmer" -intern -junior',
    '"looking for" OR "we need" "audio developer" OR "DSP developer" OR "plugin developer"',
    '"audio team" OR "DSP team" growing OR building OR expanding OR hiring',
    'site:linkedin.com "audio" OR "DSP" OR "plugin" "hiring" OR "job" -intern -volunteer',
]

# 6. GitHub activity (what's being built in audio open source)
GITHUB_TOPICS = [
    "audio", "dsp", "plugin", "clap", "vst", "reaper",
    "music-information-retrieval", "audio-processing", "neural-audio",
    "music-ai", "audio-engine", "real-time-audio",
]

# Technologies we track
TRACKED_TECHNOLOGIES = {
    "CLAP": r"\bCLAP\b|clap-audio|clap-\w+",
    "ARA": r"\bARA 2\b|Audio Random Access|ARA extension",
    "Mamba/SSM": r"\bmamba\b|state.?space|SSM\b",
    "Rust Audio": r"nih.?plug|clap.?rs|rust.*audio",
    "ONNX": r"\bONNX\b|onnxruntime|onnx.?runtime",
    "LibTorch": r"\bLibTorch\b|libtorch|pytorch.*cpp",
    "REAPER": r"\bREAPER\b|reascript|SWS\b|ReaPack",
    "Web Audio": r"Web.?Audio|Audio.?Worklet|WASM.*audio",
    "Neural Audio Codecs": r"EnCodec|SoundStream|DAC\b|neural.*codec",
    "Source Separation": r"source.?separ|stem.*separ|Demucs|spleeter",
    "FAUST": r"\bFAUST\b|faust.*audio|functional.*audio",
    "JUCE": r"\bJUCE\b|juce.*framework",
    "RTNeural": r"\bRTNeural\b|rt.?neural|real.?time.*neural",
    "MIR": r"music.?information.?retrieval|MIR\b|audio.*analysis.*ml",
}


# ── GitHub search ──


async def _github_trending() -> list[MarketSignal]:
    """Search GitHub for trending audio-related repos."""
    signals: list[MarketSignal] = []
    url = "https://api.github.com/search/repositories"
    headers = {}
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for topic in GITHUB_TOPICS:
        params = {
            "q": f"topic:{topic} stars:>50 pushed:>2025-01-01",
            "sort": "stars",
            "per_page": 5,
            "order": "desc",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                for item in resp.json().get("items", [])[:5]:
                    desc = (item.get("description") or "")[:300]
                    signals.append(
                        MarketSignal(
                            category="tech_trend",
                            source="github_trending",
                            title=item.get("full_name", ""),
                            url=item.get("html_url", ""),
                            snippet=desc,
                            relevance_score=min(10, max(1, int(item.get("stargazers_count", 0) / 100))),
                            tags=[topic, "open_source"],
                        )
                    )
        except Exception:
            continue

    return signals


# ── General search runners ──


async def _search_queries(
    queries: list[str],
    category: str,
    tag: str,
    max_per_query: int = 5,
) -> list[MarketSignal]:
    signals: list[MarketSignal] = []
    seen_urls: set[str] = set()

    for query in queries:
        try:
            results = await web_search(query, max_results=max_per_query)
            for r in results:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    signals.append(
                        MarketSignal(
                            category=category,
                            source=r.source_api,
                            title=r.title,
                            url=r.url,
                            snippet=r.snippet,
                            relevance_score=5,
                            tags=[tag],
                        )
                    )
        except Exception:
            continue

    return signals


# ── Technology trend extraction ──


def _extract_tech_mentions(text: str) -> dict[str, int]:
    """Count mentions of tracked technologies in text."""
    mentions: dict[str, int] = {}
    for name, pattern in TRACKED_TECHNOLOGIES.items():
        count = len(re.findall(pattern, text, re.IGNORECASE))
        if count > 0:
            mentions[name] = count
    return mentions


def extract_tech_trends(signals: list[MarketSignal]) -> list[TechTrend]:
    """Aggregate technology mentions across all signals to identify trends."""
    mention_counts: dict[str, int] = {}
    contexts: dict[str, list[str]] = {}

    for signal in signals:
        text = f"{signal.title} {signal.snippet}"
        mentions = _extract_tech_mentions(text)
        for tech, count in mentions.items():
            mention_counts[tech] = mention_counts.get(tech, 0) + count
            if tech not in contexts:
                contexts[tech] = []
            if len(contexts[tech]) < 3:
                contexts[tech].append(signal.title[:100])

    trends = []
    for tech, count in sorted(mention_counts.items(), key=lambda x: -x[1]):
        direction = "rising" if count >= 3 else "stable" if count >= 1 else "neutral"
        trends.append(
            TechTrend(
                technology=tech,
                mention_count=count,
                contexts=contexts.get(tech, []),
                direction=direction,
            )
        )

    return trends


# ── Pricing extraction ──


def _parse_rate(text: str) -> Optional[tuple[int, int]]:
    """Extract min/max rate from text. Returns (min, max) or None."""
    # Contract ranges: $3,000 - $5,000
    m = re.search(r"\$(\d[\d,]*)\s*(?:-|to)\s*\$?(\d[\d,]*)", text)
    if m:
        return (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", "")))

    # Single budget: Budget $5,000
    m = re.search(r"(?:budget|rate|total)\s*(?:of\s*)?[:$]?\s*\$?(\d[\d,]*)", text, re.IGNORECASE)
    if m:
        val = int(m.group(1).replace(",", ""))
        if val >= 500:
            return (val, val)

    # Hourly: $150/hr
    m = re.search(r"\$(\d{2,3})\s*(?:/hr|/hour|per hour)", text, re.IGNORECASE)
    if m:
        hr = int(m.group(1))
        return (hr * 20, hr * 80)  # convert hourly to contract range estimate

    return None


def extract_pricing_benchmarks(signals: list[MarketSignal]) -> list[PricingBenchmark]:
    """Extract pricing data from signals."""
    niches = {
        "plugin_dev": [],
        "reaper_scripts": [],
        "rust_audio": [],
        "audio_ml": [],
        "game_audio_dev": [],
    }
    niche_patterns = {
        "plugin_dev": r"\b(?:VST|CLAP|AU|AAX|audio.?plugin|DSP)\b",
        "reaper_scripts": r"\b(?:REAPER|reascript|lua.?script|DAW.?automation)\b",
        "rust_audio": r"\b(?:rust|nih.?plug|clap.?rs)\b.*\b(?:audio|DSP)\b",
        "audio_ml": r"\b(?:ML|machine.?learning|neural|ONNX|inference)\b.*\b(?:audio|DSP|speech)\b",
        "game_audio_dev": r"\b(?:game|wwise|FMOD)\b.*\b(?:audio|sound)\b",
    }

    for signal in signals:
        rate = _parse_rate(f"{signal.title} {signal.snippet}")
        if rate:
            for niche, pattern in niche_patterns.items():
                if re.search(pattern, signal.snippet, re.IGNORECASE):
                    niches[niche].append(rate)

    benchmarks = []
    for niche, rates in niches.items():
        if rates:
            mins = [r[0] for r in rates]
            maxs = [r[1] for r in rates]
            hours = []
            for r in rates:
                # If a rate pair looks like hourly * 20-80, reconstruct hourly est
                if r[1] > 0 and r[0] > 0 and r[1] / r[0] < 5:
                    hours.append(r[0] // 20)
                    hours.append(r[1] // 80)

            benchmarks.append(
                PricingBenchmark(
                    niche=niche,
                    contract_range_min=min(mins) if mins else 0,
                    contract_range_max=max(maxs) if maxs else 0,
                    hourly_min=min(hours) if hours else 0,
                    hourly_max=max(hours) if hours else 0,
                    sample_count=len(rates),
                    sources=list(set(s.url for s in signals if _parse_rate(f"{s.title} {s.snippet}")))[:5],
                )
            )

    return benchmarks


# ── Opportunity synthesis ──


def _synthesize_opportunities(
    trends: list[TechTrend],
    pricing: list[PricingBenchmark],
) -> list[str]:
    """Generate actionable opportunity statements."""
    opportunities: list[str] = []

    for trend in trends:
        if trend.direction == "rising":
            opportunities.append(
                f"{trend.technology} is trending ({trend.mention_count} mentions) — "
                f"companies need devs who know this. Consider writing a technical post."
            )

    for p in pricing:
        if p.contract_range_max > 5000:
            opportunities.append(
                f"{p.niche}: contracts range ${p.contract_range_min:,}-${p.contract_range_max:,} "
                f"({p.sample_count} data points). High-value niche."
            )

    return opportunities


# ── Main entry point ──


async def run_market_scan() -> MarketReport:
    """Run full market intelligence scan across all sources."""
    import asyncio

    signals: list[MarketSignal] = []
    errors: list[str] = []

    results = await asyncio.gather(
        _search_queries(FUNDING_QUERIES, "funding", "funding"),
        _search_queries(TREND_QUERIES, "tech_trend", "tech_trend"),
        _search_queries(LAUNCH_QUERIES, "product_launch", "product"),
        _search_queries(PRICING_QUERIES, "pricing", "pricing"),
        _search_queries(HIRING_SIGNAL_QUERIES, "hiring_signal", "hiring"),
        _github_trending(),
        return_exceptions=True,
    )

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            errors.append(f"Source {i} failed: {result}")
        else:
            signals.extend(result)

    # Dedup by URL
    seen: set[str] = set()
    unique_signals: list[MarketSignal] = []
    for s in signals:
        if s.url not in seen:
            seen.add(s.url)
            unique_signals.append(s)

    # Extract trends and pricing
    trends = extract_tech_trends(unique_signals)
    pricing = extract_pricing_benchmarks(unique_signals)
    opportunities = _synthesize_opportunities(trends, pricing)

    # Generate summary
    summary_parts = []
    if trends:
        top = [t for t in trends if t.direction == "rising"][:5]
        if top:
            summary_parts.append(f"Rising tech: {', '.join(t.technology for t in top)}")
    if pricing:
        top_pay = sorted(pricing, key=lambda p: -p.contract_range_max)[:3]
        if top_pay:
            summary_parts.append(
                f"Top-paying niches: {', '.join(f'{p.niche} (${p.contract_range_max:,})' for p in top_pay)}"
            )
    if opportunities:
        summary_parts.append(f"{len(opportunities)} actionable opportunities identified")
    if errors:
        summary_parts.append(f"{len(errors)} sources had errors")

    summary = " | ".join(summary_parts) if summary_parts else "Market scan completed with limited data."

    return MarketReport(
        signals=unique_signals,
        tech_trends=trends,
        pricing_benchmarks=pricing,
        hot_opportunities=opportunities,
        summary=summary,
    )


# ── Convenience ──


async def generate_report() -> dict:
    """Run market scan and return a serializable report dict."""
    report = await run_market_scan()

    return {
        "scanned_at": report.scanned_at,
        "summary": report.summary,
        "total_signals": len(report.signals),
        "signals": [
            {
                "category": s.category,
                "source": s.source,
                "title": s.title,
                "url": s.url,
                "snippet": s.snippet[:200],
                "relevance": s.relevance_score,
                "tags": s.tags,
            }
            for s in sorted(report.signals, key=lambda x: -x.relevance_score)[:50]
        ],
        "tech_trends": [
            {
                "technology": t.technology,
                "mentions": t.mention_count,
                "direction": t.direction,
                "contexts": t.contexts,
            }
            for t in sorted(report.tech_trends, key=lambda x: -x.mention_count)
        ],
        "pricing_benchmarks": [
            {
                "niche": p.niche,
                "contract_range_min": p.contract_range_min,
                "contract_range_max": p.contract_range_max,
                "hourly_min": p.hourly_min,
                "hourly_max": p.hourly_max,
                "sample_count": p.sample_count,
            }
            for p in sorted(report.pricing_benchmarks, key=lambda x: -x.contract_range_max)
        ],
        "hot_opportunities": report.hot_opportunities,
    }
