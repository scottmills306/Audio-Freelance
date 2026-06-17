"""Lead data layer: schema, ChromaDB store, and raw candidate models."""

from leads.schema import Lead, LeadStatus, RawCandidate, Verdict, PREFERRED_NICHES
from leads.store import (
    embed_text,
    check_duplicate,
    upsert_lead,
    get_leads_by_status,
    update_status,
    get_lead_by_id,
    search_leads,
    check_ollama_available,
    ensure_collections_initialized,
    get_all_leads,
    delete_lead,
)

__all__ = [
    "Lead",
    "LeadStatus",
    "RawCandidate",
    "Verdict",
    "PREFERRED_NICHES",
    "embed_text",
    "check_duplicate",
    "upsert_lead",
    "get_leads_by_status",
    "update_status",
    "get_lead_by_id",
    "search_leads",
    "check_ollama_available",
    "ensure_collections_initialized",
    "get_all_leads",
    "delete_lead",
]