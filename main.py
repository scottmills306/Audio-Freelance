#!/usr/bin/env python3
"""FastAPI entry point — serves dashboard + API + briefing dispatch."""

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Load .env before anything else
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

from api.routes import router

app = FastAPI(
    title="Audio-Dev Freelance Acquisition System",
    description="Automated multi-tier lead sourcing, scoring, outreach, and market intelligence pipeline.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

DASHBOARD_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Freelance Acquisition System</title>
<style>
  :root { --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --green: #3fb950; --yellow: #d29922; --red: #f85149; --blue: #58a6ff; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; line-height: 1.6; }
  h1 { font-size: 1.5rem; margin-bottom: .25rem; }
  .subtitle { color: #8b949e; font-size: .9rem; margin-bottom: 2rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; }
  .card h3 { font-size: .85rem; text-transform: uppercase; letter-spacing: .05em; color: #8b949e; margin-bottom: .75rem; }
  .stat { font-size: 2rem; font-weight: 600; }
  .stat.green { color: var(--green); } .stat.yellow { color: var(--yellow); } .stat.red { color: var(--red); }
  .row { display: flex; justify-content: space-between; padding: .35rem 0; border-bottom: 1px solid var(--border); font-size: .9rem; }
  .row:last-child { border: none; }
  a { color: var(--blue); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .badge { display: inline-block; padding: .15rem .5rem; border-radius: 12px; font-size: .75rem; font-weight: 500; }
  .badge.hot { background: #3fb95022; color: var(--green); } .badge.warm { background: #d2992222; color: var(--yellow); } .badge.cold { background: #8b949e22; color: #8b949e; }
  .actions { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }
  .btn { display: inline-block; padding: .5rem 1rem; border-radius: 6px; background: #21262d; border: 1px solid var(--border); color: var(--text); font-size: .85rem; cursor: pointer; text-decoration: none; }
  .btn:hover { background: #30363d; }
  .btn.primary { background: #238636; border-color: #2ea043; }
  .btn.primary:hover { background: #2ea043; }
  .bar { height: 8px; border-radius: 4px; background: var(--border); margin-top: .3rem; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 4px; }
  .file-list { list-style: none; }
  .file-list li { padding: .3rem 0; font-size: .9rem; }
  .file-list li::before { content: "📄 "; }
  .timestamp { color: #8b949e; font-size: .8rem; margin-top: 2rem; text-align: center; }
</style>
</head>
<body>
<h1>🎧 Freelance Acquisition System</h1>
<p class="subtitle">Controls at <a href="/docs">/docs</a> &middot; Data refreshes on scan</p>

<div class="grid" id="status-grid">
  <div class="card"><h3>Leads</h3><div id="lead-counts">Loading...</div></div>
  <div class="card"><h3>Market Trends</h3><div id="trends">Loading...</div></div>
  <div class="card"><h3>Pricing</h3><div id="pricing">Loading...</div></div>
  <div class="card"><h3>System</h3><div id="system">Loading...</div></div>
</div>

<div class="grid">
  <div class="card">
    <h3>Quick Actions</h3>
    <div class="actions">
      <a class="btn primary" href="/api/v1/prospect/plugin_dev">🔍 Prospect plugin_dev</a>
      <a class="btn primary" href="/api/v1/prospect/reaper_scripts">🔍 Prospect REAPER</a>
      <a class="btn" href="/api/v1/market">📊 Market Scan</a>
      <a class="btn" href="/api/v1/market/opportunities">🎯 Opportunities</a>
      <a class="btn" href="/api/v1/market/trends">📈 Trends</a>
      <a class="btn" href="/api/v1/market/pricing">💰 Pricing</a>
      <a class="btn" href="/api/v1/status">📋 Status</a>
      <a class="btn" href="/api/v1/health">❤️ Health</a>
      <a class="btn" href="/api/v1/debug">🔧 Debug</a>
    </div>
  </div>
  <div class="card">
    <h3>Saved Files</h3>
    <ul class="file-list">
      <li><a href="/briefing">📋 Daily Briefing</a></li>
      <li><code>outreach/READY_TO_SEND.md</code> — 8 app drafts</li>
      <li><code>~/Documents/MAMBA_SSM_ALL_REFERENCES.md</code></li>
      <li><code>~/Desktop/MAMBA_SSM_ALL_REFERENCES.md</code></li>
      <li><code>BUILD_PLAN.md</code> — Project roadmap</li>
    </ul>
  </div>
</div>

<div class="card" style="margin-bottom:2rem">
  <h3>Recent Opportunities</h3>
  <div id="opportunities"><p class="subtitle">Run <a href="/api/v1/market/opportunities">market scan</a> to populate.</p></div>
</div>

<div class="card">
  <h3>All Niches</h3>
  <div class="actions" id="niches"></div>
</div>

<p class="timestamp" id="timestamp"></p>

<script>
async function load() {
  try {
    const [statusRes, marketRes, healthRes] = await Promise.all([
      fetch('/api/v1/status').then(r=>r.json()).catch(()=>({lead_counts:{}})),
      fetch('/api/v1/market').then(r=>r.json()).catch(()=>({tech_trends:[], pricing_benchmarks:[], hot_opportunities:[]})),
      fetch('/api/v1/health').then(r=>r.json()).catch(()=>({status:'error', ollama:false})),
    ]);

    // Lead counts
    const counts = statusRes.lead_counts || {};
    const total = Object.values(counts).reduce((a,b)=>a+b,0);
    document.getElementById('lead-counts').innerHTML = `
      <div class="stat">${total}</div>
      <div class="row"><span>HOT</span><span class="stat green" style="font-size:1rem">${counts.HOT||0}</span></div>
      <div class="row"><span>WARM</span><span class="stat yellow" style="font-size:1rem">${counts.WARM||0}</span></div>
      <div class="row"><span>COLD</span><span>${counts.COLD||0}</span></div>
      <div class="row"><span>CONTACTED</span><span>${counts.CONTACTED||0}</span></div>
      <div class="row"><span>NEW</span><span>${counts.NEW||0}</span></div>
    `;

    // Trends
    const trends = marketRes.tech_trends || [];
    document.getElementById('trends').innerHTML = trends.length ? trends.slice(0,6).map(t=>
      `<div class="row"><span>${t.technology}</span><span style="color:${t.direction==='rising'?'var(--green)':'var(--yellow)'}">${t.mentions} (${t.direction})</span></div>`
    ).join('') : '<p class="subtitle">Run market scan.</p>';

    // Pricing
    const pricing = marketRes.pricing_benchmarks || [];
    document.getElementById('pricing').innerHTML = pricing.length ? pricing.map(p=>
      `<div class="row"><span>${p.niche}</span><span>$${p.contract_range_min}-$${p.contract_range_max}</span></div>`
    ).join('') : '<p class="subtitle">Run market scan.</p>';

    // System
    document.getElementById('system').innerHTML = `
      <div class="row"><span>API</span><span class="stat green" style="font-size:1rem">${healthRes.status||'ok'}</span></div>
      <div class="row"><span>Ollama</span><span style="color:${healthRes.ollama?'var(--green)':'var(--red)'}">${healthRes.ollama?'✓':'✗'}</span></div>
      <div class="row"><span>Port</span><span>${location.port||8080}</span></div>
    `;

    // Opportunities
    const opps = marketRes.hot_opportunities || [];
    document.getElementById('opportunities').innerHTML = opps.length ? opps.map(o=>'<div class="row">→ '+o+'</div>').join('') : '<p class="subtitle">Run market scan.</p>';

    // Niches
    const niches = ['plugin_dev','reaper_scripts','rust_audio','audio_ml','game_audio_dev'];
    document.getElementById('niches').innerHTML = niches.map(n=>`<a class="btn" href="/api/v1/prospect/${n}">${n}</a>`).join('');

    document.getElementById('timestamp').textContent = 'Updated: ' + new Date().toISOString();
  } catch(e) {
    document.getElementById('status-grid').innerHTML = '<div class="card"><h3>Error</h3><p>Could not load data. Server may be starting.</p></div>';
  }
}
load();
</script>
</body>
</html>"""


@app.get("/")
async def root():
    return HTMLResponse(DASHBOARD_HTML)


@app.get("/briefing")
async def briefing():
    """Compile a plain-text daily briefing of everything."""
    from leads.store import get_all_leads, get_leads_by_status, check_ollama_available
    from leads.schema import LeadStatus

    lines = []
    lines.append("=" * 60)
    lines.append("  FREELANCE ACQUISITION SYSTEM — DAILY BRIEFING")
    lines.append(f"  {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 60)
    lines.append("")

    # System health
    ollama_ok = check_ollama_available()
    lines.append(f"Ollama: {'✓' if ollama_ok else '✗'}")

    # Lead counts
    try:
        all_leads = get_all_leads()
        lines.append(f"\nTotal leads: {len(all_leads)}")
        for status in LeadStatus:
            try:
                leads = get_leads_by_status(status)
                if leads:
                    lines.append(f"  {status.value}: {len(leads)}")
            except Exception:
                pass
    except Exception:
        lines.append("\nLeads: storage not available")

    # Hot leads
    try:
        hot = get_leads_by_status(LeadStatus.HOT)
        if hot:
            lines.append(f"\n🔥 HOT LEADS ({len(hot)}):")
            for l in hot[:5]:
                lines.append(f"  • {l.title} ({l.source})")
                lines.append(f"    {l.url}")
    except Exception:
        pass

    lines.append("")
    lines.append("─" * 60)
    lines.append("ACTIONS")
    lines.append("─" * 60)
    lines.append("")
    lines.append("  Dashboard:    http://localhost:8080")
    lines.append("  Prospect:     http://localhost:8080/api/v1/prospect/{niche}")
    lines.append("  Market:       http://localhost:8080/api/v1/market")
    lines.append("  Opportunities: http://localhost:8080/api/v1/market/opportunities")
    lines.append("")
    lines.append("  Saved files:")
    lines.append("    outreach/READY_TO_SEND.md — 8 application drafts")
    lines.append("    ~/Documents/MAMBA_SSM_ALL_REFERENCES.md")
    lines.append("    ~/Desktop/MAMBA_SSM_ALL_REFERENCES.md")
    lines.append("")
    lines.append("=" * 60)

    return Response(content="\n".join(lines), media_type="text/plain")


@app.post("/dispatch")
async def dispatch_briefing():
    """Email the briefing to the configured address."""
    addr = os.getenv("BRIEFING_EMAIL", "")
    if not addr:
        return {"error": "No BRIEFING_EMAIL set in .env. Add it like: BRIEFING_EMAIL=scott@sgmstudios.ca"}

    # Build briefing text
    from leads.store import get_all_leads, get_leads_by_status
    from leads.schema import LeadStatus

    lines = []
    lines.append(f"Subject: Daily Briefing — {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')}")
    lines.append("")
    try:
        total = len(get_all_leads())
        lines.append(f"Total leads: {total}")
        for s in LeadStatus:
            try:
                leads = get_leads_by_status(s)
                if leads:
                    lines.append(f"  {s.value}: {len(leads)}")
            except Exception:
                pass
    except Exception:
        lines.append("Leads: N/A")

    lines.append("")
    lines.append("Dashboard: http://localhost:8080")
    body = "\n".join(lines)

    # Try to send via sendmail or mail command
    try:
        proc = subprocess.run(
            ["mail", "-s", f"Briefing {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')}", addr],
            input=body, text=True, capture_output=True, timeout=15,
        )
        if proc.returncode == 0:
            return {"sent": True, "to": addr, "method": "mail"}
        return {"sent": False, "to": addr, "error": proc.stderr}
    except FileNotFoundError:
        return {
            "sent": False,
            "to": addr,
            "error": "No mail command found. Install mailutils or set SMTP in .env",
            "body": body,
        }


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
