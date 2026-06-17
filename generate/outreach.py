"""Outreach draft generator with templates A-D and asset-registry claim validation."""

from datetime import datetime, timezone
from typing import Optional

from assets.registry import AssetRegistry, load_registry, verify_draft_claims
from leads.schema import Lead
from leads.store import log_outreach

_registry: AssetRegistry | None = None


def _get_registry() -> AssetRegistry:
    global _registry
    if _registry is None:
        _registry = load_registry()
    return _registry


TEMPLATES = {
    "A_plugin_contract": """Subject: your {format} plugin

Hi {name},

Saw you need {tech} development for {context}.

I build real-time audio engines (C++/Rust) — {asset_proof}.

15 min to see if this fits your timeline?

No pressure either way.

P.S. {demo_link}""",
    "B_reaper_automation": """Subject: your {daw} workflow

Hey {name},

Noticed {specific_repetitive_task}.

I automate REAPER workflows — batch processing, tagging, rendering, Lua scripting. Shipped a REAPER extension via ReaPack.

Want me to script your biggest time-suck? 15 min chat.

No pressure.

P.S. {script_demo_link}""",
    "C_game_audio": """Subject: real-time audio on {platform}

Hi {name},

Working on {game} — saw you need real-time audio tooling.

I ship C++/Rust audio code with sub-1ms processing per buffer at 48kHz (benchmarked publicly).

Quick screen share to discuss?

No pressure.

P.S. {benchmark_link}""",
    "D_cold_outbound": """Subject: {company}'s {product_area}

Hi {name},

{specific_observation_about_their_product_or_recent_post}.

I work on real-time, CPU-only neural audio inference (Mamba/SSM architectures) — public benchmarks here: {benchmark_link}.

If you ever need contract DSP/inference work, happy to do a quick intro call.

No pressure either way.

P.S. {benchmark_link}""",
}


def generate_outreach(
    lead: Lead,
    template_key: str = "A_plugin_contract",
    context: Optional[dict] = None,
) -> dict:
    """Generate an outreach draft for a lead using the specified template.

    Validates all asset claims against the registry before returning.
    Logs the draft to the outreach ChromaDB collection.
    """
    if context is None:
        context = {}

    template = TEMPLATES.get(template_key)
    if template is None:
        raise ValueError(
            f"Unknown template '{template_key}'. "
            f"Available: {', '.join(TEMPLATES.keys())}"
        )

    # Fill template with context
    draft = template.format(**context)

    # Pre-flight claim validation
    registry = _get_registry()
    violations = verify_draft_claims(draft, registry)

    result = {
        "lead_id": str(lead.id),
        "template": template_key,
        "draft": draft,
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "violations": violations,
        "safe_to_send": len(violations) == 0,
    }

    # Log to ChromaDB outreach collection
    try:
        log_outreach(
            lead_id=str(lead.id),
            template_used=template_key,
            draft_text=draft,
            status="BLOCKED" if violations else "DRAFTED",
        )
    except Exception:
        pass

    return result
