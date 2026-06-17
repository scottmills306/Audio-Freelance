# Audio-Dev Freelance Acquisition System

Automated multi-tier lead sourcing, scoring, and outreach pipeline for freelance audio/DSP/plugin development work.

## Quick Start

```bash
# 1. Install dependencies
uv venv && uv pip install -e .

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Ensure Ollama is running with the embedding model
ollama pull nomic-embed-text

# 4. Start the server
uv run python main.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root info |
| GET | `/api/v1/health` | Health check (verifies Ollama) |
| GET | `/api/v1/status` | Pipeline status + lead counts |
| POST | `/api/v1/prospect/{niche}` | Run full search → score → verdict pipeline |
| POST | `/api/v1/score` | Manually score a raw candidate |
| GET | `/api/v1/leads` | List all leads (filterable by status) |
| GET | `/api/v1/leads/{id}` | Get single lead |
| POST | `/api/v1/leads/{id}/status` | Update lead status |
| POST | `/api/v1/translate` | Translate tech capability to client pitch |
| POST | `/api/v1/rate` | Generate rate tiers for a task |
| POST | `/api/v1/outreach/{lead_id}` | Generate outreach draft for a lead |
| POST | `/api/v1/proposal` | Generate structured proposal |
| GET | `/api/v1/market` | Full market intelligence report |
| GET | `/api/v1/market/trends` | Technology trends & skills demand |
| GET | `/api/v1/market/pricing` | Pricing benchmarks by niche |
| GET | `/api/v1/market/opportunities` | Actionable opportunities right now |
| POST | `/api/v1/debug` | Run diagnostics sweep |

## Project Structure

```
├── main.py                 # FastAPI entry point
├── leads/                  # Data layer (schema + ChromaDB store)
├── search/                 # Multi-tier search (1-4)
├── scoring/                # Signal detection + scoring
├── graph/                  # LangGraph pipeline DAG
├── api/                    # FastAPI routes
├── generate/               # Outreach generation (translate, outreach, proposal, rate)
├── research/               # Market intelligence (trends, pricing, opportunities)
├── assets/                 # Asset registry (portfolio claim verification)
├── debug/                  # Diagnostics
├── tests/                  # Test suite
└── asset_registry.yml      # Portfolio items with statuses
```

## Architecture

See [BUILD_PLAN.md](BUILD_PLAN.md) and [audio-dev-freelance-system.md](audio-dev-freelance-system.md) for the full spec.
