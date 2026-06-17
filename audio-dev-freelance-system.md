# Audio-Dev Freelance Acquisition System — Hermes / Opencode Bundle

## How to use this file

- **TIER 0** and **HERMES OPERATING PRIMER**: load into Hermes context every session (system context / `AGENTS.md`-style include).
- **TIER 1–6**: each is a self-contained spec block. Feed one TIER at a time to opencode (`@CodeSquad`) to scaffold the corresponding module. Don't dump all six at once — generate, review, integrate, then move to the next tier.
- All "asset registry" claims must be re-verified weekly. If `/translate` or `/outreach` would need to claim something not in the registry as `shipped`, it must fall back to `in_progress` / `benchmark` framing instead. No fabrication, ever — this is a hard constraint baked into TIER 4.
- Outreach is **never auto-sent**. Every draft lands in a review queue (Gmail Drafts) and requires explicit human send.

---

## TIER 0 — Shared Context (Hermes: load every session)

### 0.1 Asset Registry

Update this table weekly. If `last_verified` is >7 days old, Hermes should ask "has anything here changed?" before generating outreach.

```yaml
asset_registry:
  last_verified: "<UPDATE_WEEKLY>"
  assets:
    - id: mamba_audio_rt_bench
      status: shipped          # public repo, portfolio piece
      description: "Public benchmark demonstrating Mamba/SSM linear-recurrence inference meeting hard RT audio constraints (≤1ms per 512-sample buffer @ 48kHz)"
      proof: "GitHub repo — latency benchmarks, lock-free SPSC ring buffer, threading model comparisons"
      pitch_value: "Concrete, verifiable evidence of RT-safe neural inference on CPU. This is the lead differentiator for any ML/inference-flavored lead."

    - id: reaper_sgm_extension
      status: shipped
      description: "REAPER extension shipped under SGM via ReaPack"
      proof: "Live ReaPack listing"
      pitch_value: "Evidence of shipped, distributed DAW tooling — strong for REAPER/ReaScript automation leads."

    - id: trackclear_suite
      status: in_progress       # v1 scoped for Gumroad
      description: "REAPER ReaScript Lua tools for Suno AI import workflows"
      proof: "Working scripts, validators (validate_lua.sh / validate_rpp.py), 10-agent audit completed"
      pitch_value: "Use as 'currently building' proof for AI-music/REAPER workflow automation leads. Do NOT claim as released until Gumroad v1 ships."

    - id: stem_surgeon
      status: in_progress       # architecture finalized, Mamba3-MIMO design done
      description: "5-stem separation (CLAP delta embedding, CRM decoder heads, complex SSM state), CPU-only Demucs v4 pipeline target"
      proof: "Finalized architecture doc, corrected CRMStemHead shape contract"
      pitch_value: "Frame as 'in active development' for source-separation / stem-tooling leads. Architecture-level detail is itself credible to technical buyers."

    - id: mambafx_clap
      status: broken            # get_factory returns nullptr — needs clap_plugin_factory_t fix
      description: "CLAP plugin (C++17, LibTorch, FFTW3), installed to ~/.clap/MambaFX.clap, rejected by REAPER"
      proof: "Builds, installs, fails to load"
      pitch_value: "DO NOT mention in outreach until fixed. Internal-only until resolved."

    - id: clap_spec_mcp
      status: shipped
      description: "PEP 723 single-file MCP server, 10 CLAP spec lookup tools for opencode"
      proof: "Working server, correct uv invocation pattern"
      pitch_value: "Evidence of building your own dev tooling — minor credibility signal, use sparingly (internal tooling, not client-facing)."

    - id: background_credentials
      status: shipped
      description: "Berklee background, 17+ years professional audio experience"
      proof: "Credential / career history"
      pitch_value: "Use as the 'why trust the DSP math' anchor in pitches, not as the headline."
```

### 0.2 Stack & Environment

```yaml
environment:
  os: "Bazzite (immutable Fedora)"
  build_envs: "distrobox (mutable build environments), uv for Python"
  preferred_language: "Rust (new code)"
  also: ["Python", "C++17 (plugin SDK integration: JUCE/CLAP/ARA/VST3)"]
  local_harness:
    reasoning_layer: "Hermes (Nous Hermes via Ollama)"
    code_execution_agent: "Opencode"
    orchestration: "LangGraph"
    state_queue: "Redis"
    vector_store: "ChromaDB"
    api: "FastAPI"
    squads: ["@CodeSquad", "@AnalyticsSquad", "@OutreachSquad"]
  connected_mcp_tools_relevant_here:
    - "Gmail (create_draft → outreach review queue)"
    - "Slack (HOT lead notifications)"
    - "Google Calendar (scoping call scheduling)"
    - "Google Drive (proposal docs, optional)"
```

### 0.3 Operating Rules & Configurable Variables

```yaml
operating_rules:
  - "Never fabricate leads — every result must come from a live search/fetch with a verifiable URL."
  - "Never claim 'shipped' for anything marked in_progress or broken in the asset registry."
  - "Never auto-send outreach. Drafts → Gmail Drafts queue → human send."
  - "Bound prospecting time per the daily ritual (Section: HERMES OPERATING PRIMER)."
  - "Use accurate professional descriptors (e.g., 'audio software developer / DSP engineer'), never informal self-deprecating titles."

configurable_variables:
  MIN_RATE_CAD: 3000            # floor for custom plugin/DSP work
  HOURLY_FLOOR_CAD: 150
  PREFERRED_NICHES: ["plugin_contract", "reaper_automation", "rust_audio", "ml_inference_audio", "game_audio"]
  CHROMA_COLLECTION_LEADS: "freelance_leads"
  CHROMA_COLLECTION_OUTREACH: "freelance_outreach_log"
  EMBEDDING_MODEL: "nomic-embed-text"   # local via Ollama — keeps dedup fully local
  DEDUP_SIMILARITY_THRESHOLD: 0.92      # cosine similarity above which two leads are treated as duplicates
```

### 0.4 Hard Skip Conditions

```yaml
skip_conditions:        # any match → verdict = SKIP, score not computed further
  - "revenue share"
  - "equity only"
  - "profit share"
  - "free work"
  - "for exposure"
  - "unpaid"
configurable_skip_conditions:   # toggle per current constraints
  - key: "mac_only"
    active: true        # no Mac in current environment
  - key: "projucer_required"
    active: false        # CMake preferred but not a hard blocker
  - key: "requires_incorporation"
    active: true         # sole proprietor
```

---

## ARCHITECTURE OVERVIEW

```
                ┌─────────────────────────────────────────────────────────┐
                │                    @AnalyticsSquad                       │
                │                                                           │
  Tier 1-3      │  Search Nodes ──▶ Raw Candidates ──▶ Dedup (Chroma)       │
  Search ───────┤                                          │                │
  Tier 4        │                                          ▼                │
  Outbound      │                                   Scoring Node            │
                │                                          │                │
                │                          ┌───────────────┼───────────┐    │
                │                          ▼               ▼           ▼    │
                │                       HOT (≥15)     WARM (8-14)   COLD (<8)│
                └──────────────────────────┼───────────────┼───────────┘    │
                                            │               │ (weekly batch)
                                            ▼               ▼
                ┌─────────────────────────────────────────────────────────┐
                │                    @OutreachSquad                        │
                │                                                           │
                │  /translate → /outreach → Gmail Draft (review queue)     │
                │       │                                                   │
                │       ▼                                                   │
                │  HOT → Slack notification                                 │
                └─────────────────────────────────────────────────────────┘
                                            │
                                            ▼ (reply received)
                ┌─────────────────────────────────────────────────────────┐
                │  Hermes Orchestrator (human-in-loop gate)                │
                │  Triage reply → /proposal or /rate or decline draft      │
                │  → if scoped: Calendar event + handoff to @CodeSquad     │
                └─────────────────────────────────────────────────────────┘
```

**Components opencode will build (Tiers 1–6):**

| Module | Owns |
|---|---|
| `leads/schema.py` | Pydantic `Lead` model, status enum |
| `leads/store.py` | ChromaDB collection setup, embed/dedup helpers |
| `search/tier1.py` … `search/tier4.py` | Per-tier source connectors |
| `scoring/score.py` | Signal extraction + weighted scoring |
| `generate/translate.py`, `generate/outreach.py`, `generate/proposal.py`, `generate/rate.py` | Asset-registry-grounded text generation |
| `graph/pipeline.py` | LangGraph graph wiring all of the above |
| `api/routes.py` | FastAPI endpoints |
| `debug/diagnostics.py` | `/debug` sweep |

---

## TIER 1 — [opencode] Data Layer: Lead Schema + ChromaDB

**Prompt for opencode (`@CodeSquad`):**

> Generate `leads/schema.py` and `leads/store.py`.
>
> `schema.py`:
> - Pydantic `Lead` model with fields: `id` (uuid), `source` (str), `tier` (int 1-4), `title` (str), `company` (Optional[str]), `url` (str), `raw_text` (str), `niche` (str, one of PREFERRED_NICHES), `signals` (dict[str, int] — raw scoring breakdown), `score` (int), `verdict` (Literal["HOT","WARM","COLD","SKIP"]), `status` (enum — see below), `contact_path` (Optional[str]), `discovered_at` (datetime), `last_updated` (datetime), `notes` (Optional[str]).
> - `LeadStatus` enum: `NEW, SCORED, HOT, WARM, COLD, SKIPPED, CONTACTED, REPLIED, PROPOSAL_SENT, WON, LOST, DEAD`.
>
> `store.py`:
> - Initialize a ChromaDB persistent client (local path under the project's data dir) with collection `CHROMA_COLLECTION_LEADS`.
> - Use `EMBEDDING_MODEL` (`nomic-embed-text` via Ollama) as the embedding function — fully local, no external API calls.
> - `embed_text(lead: Lead) -> str` — concatenate `title + " — " + raw_text[:500]` as the text to embed (consistent normalization: lowercase, strip whitespace, collapse newlines — this matters for dedup stability).
> - `check_duplicate(lead: Lead) -> Optional[str]` — query the collection for nearest neighbor; if cosine similarity ≥ `DEDUP_SIMILARITY_THRESHOLD`, return the existing lead's id, else `None`.
> - `upsert_lead(lead: Lead)`, `get_leads_by_status(status: LeadStatus) -> list[Lead]`, `update_status(lead_id, new_status)`.
> - Also create a second collection `CHROMA_COLLECTION_OUTREACH` with the same embedding setup, for logging generated outreach (see TIER 4).

---

## TIER 2 — [opencode] Search Layer: Expanded Multi-Tier Sourcing

**Prompt for opencode (`@AnalyticsSquad`):**

> Generate `search/tier1.py` through `search/tier4.py`. Each module exposes `run(niche: str) -> list[RawCandidate]` where `RawCandidate` is a lightweight dataclass (`source, title, url, snippet, company`). All searches use the web_search/web_fetch tooling available in the agent runtime — no scraping libraries that violate site ToS; prefer official search/API surfaces where they exist.

### Tier 1 — Daily, job-board direct

```yaml
tier_1_sources:
  - name: "KVR Audio Job Board"
    query: 'site:kvraudio.com "C++" "plugin" "contract" OR "freelance"'
  - name: "JUCE Forum Jobs"
    query: 'site:forum.juce.com "jobs" "contract" OR "freelance"'
  - name: "r/AudioProgramming"
    query: 'site:reddit.com/r/audioprogramming "hiring" OR "contract" OR "paid"'
  - name: "r/REAPER"
    query: 'site:reddit.com/r/Reaper "custom script" "paid"'
  - name: "r/WeAreTheMusicMakers"
    query: 'site:reddit.com/r/WeAreTheMusicMakers "looking for" "developer" "paid"'
```

### Tier 2 — Weekly, broad remote/freelance

```yaml
tier_2_sources:
  - name: "We Work Remotely"
    query: 'site:weworkremotely.com audio OR DSP OR "audio plugin"'
  - name: "RemoteOK"
    query: 'site:remoteok.com audio dsp'
  - name: "Wellfound (AngelList)"
    query: 'site:wellfound.com "audio" "contract" OR "contractor"'
  - name: "Upwork (filtered)"
    query: '"C++" "audio" "fixed price" site:upwork.com'
  - name: "Hacker News Who's Hiring (via Algolia)"
    note: "Use HN Algolia API directly — more reliable than web search."
    endpoint: "https://hn.algolia.com/api/v1/search_by_date"
    params:
      tags: "comment"
      query: "audio OR DSP OR 'audio plugin' OR Mamba OR 'real-time audio'"
      # filter results to comments whose story title matches /Who is hiring/
      # then filter for "contract"/"freelance"/"part-time" within the comment text
```

### Tier 3 — Niche/specialist communities

```yaml
tier_3_sources:
  - name: "The Audio Programmer community"
    query: '"The Audio Programmer" job OR contract audio plugin'
  - name: "ADC (Audio Developer Conference) community"
    query: 'site:audio.dev OR "Audio Developer Conference" hiring contract'
  - name: "GitHub bounty/contractor issues — audio orgs"
    query: 'is:issue label:bounty audio OR DSP OR "audio plugin" site:github.com'
  - name: "Music-tech specific boards"
    query: '"music tech" "developer" "contract" jobs site:musictech.net OR site:musicradar.com'
```

### Tier 4 — Outbound / Cold (target-list generation, not job postings)

> This tier produces a **target company list**, scored separately (see TIER 3 fit-score table below), feeding the cold-outreach variant in TIER 4 generation.

```yaml
tier_4_sources:
  - name: "Known audio plugin companies — careers pages"
    seed_companies: ["iZotope", "Output", "Native Instruments", "Arturia", "u-he", "Soundtoys", "Eventide", "Plugin Boutique", "FabFilter"]
    query_template: 'site:{company_domain}/careers OR site:{company_domain}/jobs "contract" OR "audio" OR "DSP"'
  - name: "YC company directory — audio category"
    query: 'site:ycombinator.com/companies audio OR "audio AI" OR "music AI"'
    filter: "recent batches (last 4), check for public 'hiring' or 'contractors' mentions"
  - name: "AI-audio startups (general)"
    query: '"audio AI" OR "music AI" startup funding 2025 OR 2026'
    purpose: "Build candidate list of small/seed-stage companies likely to need contract DSP/inference work"
  - name: "Game audio middleware vendors"
    query: '"Wwise" OR "FMOD" middleware partner OR contractor real-time audio'
```

---

## TIER 3 — [opencode] Scoring Layer

**Prompt for opencode (`@AnalyticsSquad`):**

> Generate `scoring/score.py`. `score_lead(candidate: RawCandidate, niche: str) -> ScoreResult` where `ScoreResult` contains `signals: dict[str, int]`, `total: int`, `verdict: Literal["HOT","WARM","COLD","SKIP"]`.
>
> Apply hard-skip check first (Section 0.4) — if any skip keyword matches `raw_text`, return `verdict="SKIP"` immediately with `total=0`.
>
> Otherwise compute signals per the table below, sum, and assign verdict by threshold.

### Tier 1–3 Scoring Table (job postings)

| Signal | Pattern match (case-insensitive) | Points |
|---|---|---|
| Real-time C++/Rust DSP explicit | `c++`, `rust`, `dsp`, `real-time`, `realtime` (any combo) | +5 |
| Plugin format mentioned | `vst3`, `clap`, `ara2`, `ara`, `au`, `audio unit` | +5 |
| ML/neural inference for audio | `onnx`, `libtorch`, `mamba`, `ssm`, `state space`, `neural`, `ml inference`, `machine learning` | +8 |
| Rust audio specifically | `nih-plug`, `clap-rs`, `rust audio`, `rust plugin` | +6 |
| REAPER/ReaScript automation | `reaper`, `reascript`, `lua script`, `daw automation` | +4 |
| Edge/local/CPU-only inference | `on-device`, `edge`, `cpu-only`, `no cloud`, `offline inference` | +5 |
| Low-latency explicit | `low latency`, `<5ms`, `<1ms`, `real-time constraint` | +4 |
| Budget stated above MIN_RATE | numeric budget/rate parsed and ≥ `MIN_RATE_CAD` (or hourly × est. hours ≥ floor) | +10 |
| Remote-friendly or PNW local | `remote`, `vancouver`, `pacific time`, `pst` | +3 |
| **Negative —** budget explicitly below floor | numeric budget < `MIN_RATE_CAD` | −15 |
| **Negative —** GUI-only, no DSP | `projucer` AND `gui` AND no DSP keywords matched | −3 |
| **Negative —** Mac-only/Dante (if `mac_only` active) | `mac only`, `macos only`, `dante` | −10 |

**Thresholds:** `total ≥ 15` → `HOT` · `8 ≤ total < 15` → `WARM` · `total < 8` → `COLD`

### Tier 4 Fit-Score Table (target companies, not postings)

| Signal | Points |
|---|---|
| Company builds real-time audio product | +5 |
| Company's product needs ML/inference (stated or inferable from product description) | +5 |
| Seed/small stage (≤~30 employees, recent funding round, or no dedicated DSP team visible) | +5 |
| Active public technical content (engineering blog, conference talks — signals active dev, approachable) | +3 |

**Threshold:** `total ≥ 10` → add to cold-outreach target list (TIER 4 variant D outreach).

---

## TIER 4 — [opencode] Generation Layer: Translate / Outreach / Proposal / Rate

**Prompt for opencode (`@OutreachSquad`):**

> Generate `generate/translate.py`, `generate/outreach.py`, `generate/proposal.py`, `generate/rate.py`. **Every generation function must load the Asset Registry (Section 0.1) and refuse to emit `shipped`-tier claims for any asset marked `in_progress` or `broken`.** Build this as a pre-flight validation step that scans the generated draft text for asset IDs/keywords and cross-checks status before returning.

### `/translate` — capability → client value

```yaml
translate:
  input: "technical_description: str"
  output_format:
    headline: "outcome-focused, no jargon"
    pitch: "2 sentences, credentials only when relevant"
    bullets: ["performance", "portability/privacy", "your IP stays yours"]
    pricing_anchor: "vs traditional dev/agency quote"
  example:
    input: "Real-time Mamba/SSM inference for audio effects on CPU"
    output:
      headline: "Neural audio processing that runs on the user's CPU — no cloud, no per-call cost"
      pitch: "I build real-time C++/Rust audio engines using state-space (Mamba/SSM) architectures. Public RT-safety benchmarks available (mamba-audio-rt-bench)."
      bullets:
        - "Sub-1ms processing per 512-sample buffer @ 48kHz — benchmarked, not estimated"
        - "Runs on any laptop CPU — no GPU dependency, no API costs"
        - "Your model weights, your IP — nothing leaves the binary"
      pricing_anchor: "30-50% below a dedicated DSP-ML hire for a fixed-scope integration"
```

### `/outreach` — templates A–D

```yaml
outreach_rules:
  max_words: 150
  subject_max_words: 8
  subject_case: lowercase
  required_elements:
    - "specific observation from their post/site (not generic)"
    - "one relevant proof point from asset registry (status-checked)"
    - "15-minute chat ask"
    - "'No pressure either way.'"
    - "P.S. with demo link or public repo"

templates:
  A_plugin_contract: |
    Subject: your {format} plugin

    Hi {name},

    Saw you need {tech} development for {context}.

    I build real-time audio engines (C++/Rust) — {asset_proof}.

    15 min to see if this fits your timeline?

    No pressure either way.

    P.S. {demo_link}

  B_reaper_automation: |
    Subject: your {daw} workflow

    Hey {name},

    Noticed {specific_repetitive_task}.

    I automate REAPER workflows — batch processing, tagging, rendering, Lua scripting. Shipped a REAPER extension via ReaPack.

    Want me to script your biggest time-suck? 15 min chat.

    No pressure.

    P.S. {script_demo_link}

  C_game_audio: |
    Subject: real-time audio on {platform}

    Hi {name},

    Working on {game} — saw you need real-time audio tooling.

    I ship C++/Rust audio code with sub-1ms processing per buffer at 48kHz (benchmarked publicly).

    Quick screen share to discuss?

    No pressure.

    P.S. {benchmark_link}

  D_cold_outbound: |
    Subject: {company}'s {product_area}

    Hi {name},

    {specific_observation_about_their_product_or_recent_post}.

    I work on real-time, CPU-only neural audio inference (Mamba/SSM architectures) — public benchmarks here: {benchmark_link}.

    If you ever need contract DSP/inference work, happy to do a quick intro call.

    No pressure either way.

    P.S. {benchmark_link}
```

### `/proposal`

```yaml
proposal:
  pricing_tiers_cad:
    small: "1500-3000   # script, single tool/feature"
    medium: "5000-12000  # plugin component, integration"
    large: "15000-30000  # full plugin + UI + testing"
  rate_anchors:
    cpp_plugin_contract: "5k-12k (agency: 15k-30k)"
    ml_inference_integration: "4k-8k (agency: 12k-20k)"
    reaper_automation: "1.5k-3k (agency: 4k-8k)"
    realtime_ml: "8k-15k (agency: 25k-50k)"
  structure:
    - "Problem (mirror their words)"
    - "Fixed scope — deliverables (✅) + explicit out-of-scope (❌)"
    - "Investment — total, 50/50 split, revisions included, support window"
    - "Timeline — business days with buffer"
    - "Why — speed + verifiable proof (asset registry, status-checked)"
    - "CTA — 'Reply APPROVED to start'"
  output_path: "proposals/{client}_{date}.md"
  ip_note: "Flag in proposal: underlying engines/tooling (Mamba3, REAPER toolkit) are LICENSED for this deliverable, not assigned — only deliverable-specific integration code transfers. Surface this explicitly before sending."
```

### `/rate`

```yaml
rate:
  input: ["task_description: str", "estimated_hours: int"]
  tiers:
    premium: "hours * HOURLY_FLOOR_CAD * 1.5  # + 30d support, docs, source"
    standard: "hours * HOURLY_FLOOR_CAD * 1.0  # + 7d support"
    mvp: "hours * HOURLY_FLOOR_CAD * 0.7       # proof of concept only"
  floor_check: |
    if estimated_hours * HOURLY_FLOOR_CAD < MIN_RATE_CAD:
        return "Below minimum. Consider productizing as a standalone tool (Gumroad) instead of custom contract."
  anchor_template: "Traditional agency: ~${agency_est}. I can do ${your_est} because the inference engine/benchmark already exists ({asset_id})."
```

**Logging:** every generated outreach is upserted into `CHROMA_COLLECTION_OUTREACH` with `status=DRAFTED`, `lead_id`, `template_used`, `created_at`, and a `follow_up_due` timestamp (+5 days).

---

## TIER 5 — [opencode] Orchestration & Integration Wiring

**Prompt for opencode (`@CodeSquad`):**

> Generate `graph/pipeline.py` (LangGraph) and `api/routes.py` (FastAPI).

### LangGraph graph

```yaml
nodes:
  - search_tier1, search_tier2, search_tier3, search_tier4   # @AnalyticsSquad
  - dedup                                                      # checks against CHROMA_COLLECTION_LEADS
  - score                                                       # TIER 3
  - route_by_verdict                                            # conditional edge: HOT/WARM/COLD/SKIP
  - generate_translate, generate_outreach                       # @OutreachSquad
  - queue_for_review                                            # Gmail draft creation
  - notify_hot                                                  # Slack DM
  - await_human_send                                            # HUMAN-IN-LOOP GATE — terminal until Scott sends manually
  - reply_triage                                                # entry point when a reply arrives (manual trigger or Gmail watch)

edges:
  - search_* -> dedup -> score -> route_by_verdict
  - route_by_verdict(HOT)  -> generate_translate -> generate_outreach -> queue_for_review -> notify_hot -> await_human_send
  - route_by_verdict(WARM) -> generate_translate -> generate_outreach -> queue_for_review -> await_human_send   # batched weekly
  - route_by_verdict(COLD) -> end (archive, status=COLD)
  - route_by_verdict(SKIP) -> end (archive, status=SKIPPED)
  - reply_triage -> [proposal_path | rate_path | decline_path]   # see Hermes primer
```

### FastAPI routes

```yaml
routes:
  - "POST /prospect/{niche}"     # triggers search_tier1-4 + dedup + score for given niche; returns table of new HOT/WARM leads
  - "POST /translate"            # body: {technical_description} -> translate output
  - "POST /outreach/{lead_id}"   # generates draft, creates Gmail draft, logs to outreach collection
  - "POST /proposal"             # body: {client, need, scope} -> proposal markdown
  - "POST /rate"                 # body: {task_description, estimated_hours} -> rate breakdown
  - "GET  /status"               # pipeline status snapshot (see Hermes primer 0.1)
  - "POST /debug"                # runs TIER 6 diagnostic sweep
```

### MCP integration points (already connected — wire directly, no new infra)

```yaml
integrations:
  gmail:
    use: "Gmail:create_draft — every queue_for_review draft becomes a Gmail draft. This IS the review queue."
  slack:
    use: "Slack:slack_send_message — HOT lead notification, format: '🎯 HOT: {title} @ {company} — {why} — draft ready in Gmail'"
  google_calendar:
    use: "Google Calendar:create_event — scoping calls once a reply moves to PROPOSAL_SENT or WON (see Hermes primer)"
```

---

## TIER 6 — [opencode] Debug & Diagnostics Layer

**Prompt for opencode (`@CodeSquad`):**

> Generate `debug/diagnostics.py` exposing `run_diagnostics() -> DiagnosticReport`. The report covers per-source connectivity, Chroma collection health, and recent error logs. Map each failure mode below to a concrete check + remediation suggestion.

```yaml
failure_modes:
  - symptom: "Tier N search returns 0 results"
    checks:
      - "Was the query string actually sent? Log raw query."
      - "Did the site/search return a block page or CAPTCHA (check response text for known block signatures)?"
      - "Has this source returned results in the last 7 days? If never, query syntax may be wrong — test query manually."
    remediation: "Retry with backoff; if persistent >3 days, flag query for manual revision (site structure may have changed)."

  - symptom: "Most/all leads scored COLD"
    checks:
      - "Dump raw `signals` dict for last 10 leads — which signals fired vs. expected?"
      - "Are search results actually relevant to the niche, or is the query too broad?"
    remediation: "If signals aren't firing on clearly-relevant text, check pattern matching (case sensitivity, word boundaries). If results are irrelevant, narrow the query."

  - symptom: "Dedup marking distinct leads as duplicates"
    checks:
      - "Log cosine similarity scores for flagged duplicates."
      - "Check text normalization — are titles being truncated identically across genuinely different posts?"
    remediation: "Raise DEDUP_SIMILARITY_THRESHOLD incrementally (0.92 → 0.95) and re-test against known-distinct pairs."

  - symptom: "Same lead reappears across runs despite dedup"
    checks:
      - "Confirm embedding model produces stable output for identical input (run twice, compare)."
      - "Check normalization — trailing whitespace, HTML entities, emoji in titles can shift embeddings."
    remediation: "Strip HTML/emoji and normalize whitespace before embedding; lower threshold slightly if still failing."

  - symptom: "Outreach draft contains an unverifiable/fabricated claim"
    checks:
      - "Diff generated draft text against Asset Registry (Section 0.1) — flag any asset ID referenced with a status mismatch."
      - "Check whether the pre-flight validation step in TIER 4 actually ran (log its invocation)."
    remediation: "Block draft creation; surface the offending sentence for manual rewrite. This is a hard stop, not a warning."

  - symptom: "Gmail draft not appearing in review queue"
    checks:
      - "Confirm Gmail:create_draft call succeeded (check response, not just that it was called)."
      - "Check for auth/credential errors on the Gmail connector."
    remediation: "Re-auth Gmail connector if credential error; otherwise log full draft payload and retry once."
```

---

## HERMES OPERATING PRIMER (load alongside Tier 0 every session)

### Session-start status check

At the start of each session, query and surface:
- Lead counts by status (`get_leads_by_status` for each enum value)
- Last run timestamp per search tier
- Count of items in `CHROMA_COLLECTION_OUTREACH` with `status=DRAFTED` and `follow_up_due ≤ today` (overdue follow-ups)
- Asset registry `last_verified` — if >7 days old, ask Scott if anything changed

### Daily / Weekly Ritual

```yaml
morning_30min:
  - "POST /prospect/{preferred_niche_of_the_day}"
  - "Review HOT leads surfaced via Slack; approve/edit Gmail drafts"

midday_20min:
  - "Send approved Gmail drafts manually (Hermes does NOT send)"
  - "Mark sent in lead status -> CONTACTED"

evening_15min:
  - "Check Gmail for replies"
  - "Run reply_triage if any replies present"
  - "Log any wins/lessons against the lead record (notes field)"

weekly_friday:
  - "Batch-review WARM leads -> generate outreach for top candidates"
  - "Run /debug — sanity check pipeline health"
  - "Update Asset Registry last_verified"
  - "Run Tier 4 outbound sweep -> refresh cold-outreach target list"
```

### Outreach Management Playbook

1. **Reviewing drafts**: Hermes summarizes new Gmail drafts (lead, score, template used) — does not edit/send without explicit instruction.
2. **Follow-ups**: at session start, surface any `DRAFTED`/`CONTACTED` items with `follow_up_due ≤ today`. Offer to draft a one-line follow-up ("Just floating this back up — still happy to chat if useful. No pressure.").
3. **Reply triage** — classify incoming reply:
   - *Interested / wants more info* → route to `/rate` (if scope unclear) or `/proposal` (if scope clear) → update status `PROPOSAL_SENT` once sent.
   - *Negotiating budget below floor* → check `/rate` floor logic; if genuinely below `MIN_RATE_CAD`, draft polite redirect toward productized option, or decline.
   - *Not interested / no fit* → status → `LOST`, log reason in notes (useful for scoring recalibration).
   - *Silence past follow-up* → status → `DEAD` after second follow-up with no response.

### "Landed a Reply / Possible Gig" Playbook

When a lead moves toward `PROPOSAL_SENT` or `WON`:

1. **Scoping call prep**: pull the lead's `raw_text` + any reply content; draft 3-5 clarifying questions specific to their stated need (don't reuse generic questions — ground in their actual words).
2. **Proposal**: run `/proposal` — confirm the IP note (Section TIER 4) is included before it goes out.
3. **Contract checklist** (not legal advice — flag for actual review before signing):
   - Deliverables match proposal scope exactly
   - IP terms: underlying engines/tooling (Mamba3, REAPER toolkit components) **licensed**, not assigned
   - Payment terms (50/50 or milestone), revision count, support window
   - If this is a real signed contract, route to `legal:review-contract` or `small-business:contract-review` skill for a structured pass before signing.
4. **Scheduling**: offer to create a Google Calendar event for the scoping call once a time is agreed.
5. **Handoff to @CodeSquad**: once scope is locked, create a work item/spec for the actual implementation — this is where TIER 1-style ARD/PRD generation from your existing build workflow takes over.

### Debug Invocation Patterns

- "search isn't finding anything" / "why is everything COLD" / "dedup is eating real leads" → run `/debug`, interpret `DiagnosticReport` against the TIER 6 failure-mode table, propose either a config tweak (query string, threshold) or a code patch for opencode.
- "this outreach draft mentions MambaFX as working" → this should never happen if TIER 4 pre-flight validation is wired correctly; treat as a P1 bug, route to opencode to fix the validation step, not just the one draft.

---

## QUICK REFERENCE CARD

```
COMMAND              | ROUTE                          | OUTPUT
---------------------|--------------------------------|--------------------------------
POST /prospect/{n}   | search 1-4 -> dedup -> score    | HOT/WARM leads, Slack ping (HOT)
POST /translate      | generate.translate              | headline/pitch/bullets/anchor
POST /outreach/{id}  | generate.outreach -> Gmail draft| draft in Gmail, logged to Chroma
POST /proposal       | generate.proposal               | proposals/{client}_{date}.md
POST /rate           | generate.rate                   | quote tiers or "productize" flag
GET  /status         | session-start summary           | counts by status, overdues
POST /debug          | TIER 6 diagnostics              | DiagnosticReport

FLOOR: $3,000 CAD / $150 CAD-hr   |   HARD SKIPS: revenue-share, equity-only, unpaid
ASSET TRUTH SOURCE: Section 0.1 — status-checked before every generated draft, no exceptions
```
