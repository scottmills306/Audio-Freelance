"""Tier 3 — Niche/specialist communities with actual hiring posts."""

import contextlib

import httpx

from search.base import RawCandidate, web_search

QUERIES = {
    "plugin_dev": [
        '"The Audio Programmer" job OR contract OR hiring OR freelance audio plugin -discussion',
        "site:audio.dev job OR hiring OR contract OR career -speaker -conference",
        '"music tech" OR "pro audio" "developer" OR "engineer" contract OR freelance OR hiring',
        '"audio plugin company" OR "plugin developer" hiring OR contract OR job',
    ],
    "reaper_scripts": [
        '"reaper" OR "reascript" OR "sws extension" "commission" OR "paid" OR "developer needed"',
        '"daw automation" OR "audio workflow" "script" OR "developer" contract OR freelance',
        '"reaper developer needed" OR "reaper script commission"',
    ],
    "rust_audio": [
        '"The Audio Programmer" rust audio contract OR job',
        '"rust" "audio" "developer" OR "engineer" contract OR job -tutorial -"how to"',
        '"nih-plug" OR "clap-rs" OR "rust-vst" developer OR contract OR job',
    ],
    "audio_ml": [
        '"audio developer conference" OR "adc" job OR contract OR career',
        '"mamba" OR "ssm" OR "state space model" "audio" OR "dsp" developer OR engineer OR contract',
        '"neural audio" OR "ai audio" developer OR engineer hiring OR contract OR job',
        '"on-device machine learning" OR "edge ml" "audio" OR "dsp" contract OR job',
    ],
    "game_audio_dev": [
        '"wwise" OR "fmod" developer OR programmer hiring OR contract OR job',
        '"game audio middleware" OR "audio engine" developer OR programmer contract OR job',
        '"game studio" OR "game developer" "audio programmer" OR "audio engineer" hiring OR contract',
    ],
}


async def _github_bounty_search() -> list[RawCandidate]:
    """Search GitHub for bounty/contractor issues in audio orgs."""
    url = "https://api.github.com/search/issues"
    params = {
        "q": 'is:issue label:bounty OR label:"good first issue" OR label:contract audio OR DSP OR plugin OR REAPER',
        "per_page": 20,
        "sort": "updated",
    }
    candidates: list[RawCandidate] = []
    with contextlib.suppress(Exception):
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            for item in resp.json().get("items", []):
                candidates.append(
                    RawCandidate(
                        source="github_bounty",
                        title=item.get("title", ""),
                        url=item.get("html_url", ""),
                        snippet=(item.get("body") or "")[:500],
                        company=None,
                        raw_text=(item.get("body") or "")[:500],
                        tier=3,
                    )
                )
    return candidates


async def run(niche: str) -> list[RawCandidate]:
    queries = QUERIES.get(niche, QUERIES.get("plugin_dev", []))
    all_candidates: list[RawCandidate] = []
    seen_urls: set[str] = set()

    for query in queries:
        try:
            results = await web_search(query, max_results=10)
            for r in results:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    all_candidates.append(
                        RawCandidate(
                            source=r.source_api,
                            title=r.title,
                            url=r.url,
                            snippet=r.snippet,
                            raw_text=r.snippet,
                            tier=3,
                        )
                    )
        except Exception:  # noqa: S112
            # Ignore failed queries and continue with the next one
            continue

    for c in await _github_bounty_search():
        if c.url not in seen_urls:
            seen_urls.add(c.url)
            all_candidates.append(c)

    return all_candidates
