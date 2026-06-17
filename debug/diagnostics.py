"""Pipeline diagnostics: per-source connectivity, Chroma health, error logs, failure-mode remediation."""

import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@dataclass
class DiagnosticReport:
    timestamp: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )
    ollama_available: bool = False
    chroma_healthy: bool = False
    env_keys_present: dict[str, bool] = field(default_factory=dict)
    python_version: str = ""
    errors: list[str] = field(default_factory=list)
    remediation: list[str] = field(default_factory=list)


def run_diagnostics() -> dict:
    """Run all diagnostics and return a report as a dict."""
    report = DiagnosticReport()
    report.python_version = sys.version

    # 1. Check environment variables
    keys_to_check = [
        ("TAVILY_API_KEY", "tvly-"),
        ("SERPER_API_KEY", "c0203d"),
        ("FIRECRAWL_API_KEY", "***"),
        ("OLLAMA_HOST", "http://"),
        ("MIN_RATE_CAD", ""),
        ("HOURLY_FLOOR_CAD", ""),
        ("CHROMA_COLLECTION_LEADS", ""),
        ("CHROMA_COLLECTION_OUTREACH", ""),
        ("EMBEDDING_MODEL", ""),
        ("DEDUP_SIMILARITY_THRESHOLD", ""),
    ]
    for key, stub_value in keys_to_check:
        val = os.getenv(key, "")
        # Check if value is empty or still a stub/placeholder
        if not val:
            report.env_keys_present[key] = False
            report.errors.append(f"Missing env var: {key}")
        elif stub_value and val.strip().startswith(stub_value) and len(val.strip()) < 15:
            report.env_keys_present[key] = False
            report.errors.append(
                f"Env var '{key}' appears to be a stub/placeholder: '{val[:20]}'"
            )
        else:
            report.env_keys_present[key] = True

    # 2. Check Ollama
    try:
        import ollama

        ollama.list()
        report.ollama_available = True
    except Exception as e:
        report.ollama_available = False
        report.errors.append(f"Ollama not available: {e}")
        report.remediation.append(
            "Start Ollama: `ollama serve` or check OLLAMA_HOST in .env"
        )

    # 3. Check ChromaDB
    try:
        from chromadb import PersistentClient

        data_dir = (
            Path(__file__).resolve().parent.parent / "leads" / "data" / "chroma"
        )
        data_dir.mkdir(parents=True, exist_ok=True)
        client = PersistentClient(path=str(data_dir))
        client.heartbeat()
        report.chroma_healthy = True
    except Exception as e:
        report.chroma_healthy = False
        report.errors.append(f"ChromaDB error: {e}")
        report.remediation.append(
            "Check chromadb installation: `pip install chromadb`"
        )

    # 4. Check search API keys specifically
    tavily = os.getenv("TAVILY_API_KEY", "")
    serper = os.getenv("SERPER_API_KEY", "")
    firecrawl = os.getenv("FIRECRAWL_API_KEY", "")

    if ("tvly-" in tavily and len(tavily) < 15) or not tavily:
        report.remediation.append(
            "Tavily API key is a stub. Set TAVILY_API_KEY in .env for Tier 1-2 search."
        )
    if ("c0203d" in serper and len(serper) < 15) or not serper:
        report.remediation.append(
            "Serper API key is a stub. Set SERPER_API_KEY in .env for Tier 2 fallback."
        )
    if not firecrawl or firecrawl == "***":
        report.remediation.append(
            "Firecrawl API key not set. Set FIRECRAWL_API_KEY in .env for Tier 3 fallback."
        )

    # 5. Common failure-mode checks
    if not report.env_keys_present.get("TAVILY_API_KEY", False):
        report.remediation.append(
            "Tier 1-2 search will return 0 results until Tavily key is configured."
        )

    if not report.ollama_available:
        report.remediation.append(
            "Dedup will fail. Embedding model needs Ollama running with 'nomic-embed-text' pulled."
        )

    return {
        "status": "degraded" if report.errors else "healthy",
        "timestamp": report.timestamp,
        "ollama_available": report.ollama_available,
        "chroma_healthy": report.chroma_healthy,
        "env_keys": report.env_keys_present,
        "python_version": report.python_version,
        "errors": report.errors,
        "remediation": report.remediation,
    }
