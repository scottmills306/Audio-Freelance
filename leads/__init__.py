"""Lead data layer: schema, ChromaDB store, and raw candidate models."""

from leads.schema import PREFERRED_NICHES, Lead, LeadStatus, RawCandidate, Verdict
from leads.store import (
    check_duplicate,
    check_ollama_available,
    delete_lead,
    embed_text,
    ensure_collections_initialized,
    get_all_leads,
    get_lead_by_id,
    get_leads_by_status,
    search_leads,
    update_status,
    upsert_lead,
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
