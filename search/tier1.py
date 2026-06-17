"""Tier 1 — Daily: job boards and communities with actual hiring posts.

All queries include negative keywords to exclude forum chatter and tutorials.
"""

from search.base import RawCandidate, web_search, fetch_url

# Queries organized by niche - focused on actual job/contract/freelance listings
QUERIES = {
    "plugin_dev": [
        # KVR Audio job board - actual listings
        'site:kvraudio.com "hiring" OR "contract" OR "freelance" "C++" OR "DSP" OR "plugin" -discussion -tutorial -question',
        # JUCE forum jobs section
        'site:forum.juce.com "jobs" OR "looking" OR "hiring" OR "contract" "C++" OR "plugin" -discussion -tutorial',
        # Reddit audio programming - hiring/paid posts only
        'site:reddit.com/r/audioprogramming "hiring" OR "contract" OR "paid" OR "looking for"',
        # General search for audio plugin contract work
        '"audio plugin" "contract" OR "freelance" OR "hiring" "developer" -discussion -tutorial -forum',
    ],
    "reaper_scripts": [
        # REAPER forum commissions
        'site:forum.cockos.com "commission" OR "paid" OR "hiring" OR "looking for" "script" OR "action" OR "extension" -discussion -question',
        # Reddit REAPER - paid requests
        'site:reddit.com/r/Reaper "paid" OR "commission" OR "hiring" "script" OR "action" OR "automation"',
        # General REAPER freelance work
        '"reaper" "script" OR "reascript" OR "extension" "contract" OR "freelance" OR "paid" OR "hiring" -tutorial -"how to"',
        # Cockos developer forum
        'site:forum.cockos.com "developer" "paid" OR "contract" OR "hire" -discussion',
    ],
    "rust_audio": [
        # Rust audio jobs/contracts
        '"rust" "audio" "hiring" OR "contract" OR "freelance" OR "job" -tutorial -discussion -"how to"',
        # nih-plug/CLAP-rs specific
        '"nih-plug" OR "clap-rs" "hiring" OR "contract" OR "paid" OR "job"',
        # Reddit rust + audio paid
        'site:reddit.com/r/rust "audio" "hiring" OR "contract" OR "paid"',
        # Rust audio developer positions
        '"rust" "audio developer" OR "audio engineer" OR "dsp engineer" "hiring" OR "job" OR "contract"',
    ],
    "audio_ml": [
        # ML/AI audio jobs
        '"machine learning" OR "ML" OR "neural" "audio" OR "dsp" "hiring" OR "contract" OR "freelance" -conference -paper -research',
        # Job platforms with ML audio roles
        '"ml engineer" OR "ai engineer" "audio" OR "speech" OR "music" "remote" OR "contract"',
        # ONNX/LibTorch audio
        '"onnx" OR "libtorch" OR "mamba" OR "state space" "audio" OR "dsp" "hiring" OR "contract"',
        # Audio AI startups hiring
        '"audio ai" OR "music ai" "hiring" OR "contract" OR "looking for" "engineer" OR "developer"',
    ],
    "game_audio_dev": [
        # Game audio programmer positions
        '"audio programmer" OR "audio engineer" "game" "hiring" OR "contract" OR "freelance" -discussion',
        # Wwise/FMOD specific
        '"wwise" OR "fmod" "contract" OR "freelance" OR "hiring" "developer" OR "programmer"',
        # Game studios hiring audio devs
        '"game studio" OR "game company" "audio" "hiring" OR "contract" OR "freelance"',
        # Reddit game audio dev
        'site:reddit.com/r/GameAudio "paid" OR "contract" OR "hiring" OR "looking for"',
    ],
}

# Forum noise patterns to filter from results
_FORUM_NOISE = [
    "discussion", "how to", "tutorial", "what is", "anyone else",
    "question", "help with", "thoughts on", "opinion", "should i",
    "vs", "versus", "which is better", "recommend", "suggestion",
]


def _is_forum_noise(text: str) -> bool:
    """Check if result looks like forum chatter, not a job posting."""
    lower = text.lower()
    # If it has hiring signals, it's not noise even if in a forum
    hiring_signals = ["hiring", "contract", "freelance", "paid", "job", "commission", "looking for", "we need", "we are looking"]
    has_hiring = any(s in lower for s in hiring_signals)
    if has_hiring:
        return False
    # Check for forum noise patterns
    noise_count = sum(1 for p in _FORUM_NOISE if p in lower)
    return noise_count >= 1


async def run(niche: str) -> list[RawCandidate]:
    """Run Tier 1 search for the given niche."""
    queries = QUERIES.get(niche, QUERIES.get("plugin_dev", []))
    all_candidates: list[RawCandidate] = []
    seen_urls: set[str] = set()

    for query in queries:
        try:
            results = await web_search(query, max_results=10)
            for r in results:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    # Filter out obvious forum noise
                    snippet = r.snippet or ""
                    if _is_forum_noise(f"{r.title} {snippet}"):
                        continue
                    all_candidates.append(
                        RawCandidate(
                            source=r.source_api,
                            title=r.title,
                            url=r.url,
                            snippet=snippet,
                            company=None,
                            raw_text=snippet,
                            tier=1,
                        )
                    )
        except Exception:
            continue

    return all_candidates
