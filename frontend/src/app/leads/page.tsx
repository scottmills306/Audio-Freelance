"use client";

import { useEffect, useState } from "react";
import { fetchLeads, Lead } from "@/lib/api";

const STATUSES = ["NEW", "HOT", "WARM", "COLD", "SKIPPED", "CONTACTED", "PROPOSAL_SENT", "WON", "LOST", "DEAD"];

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { load(); }, [filter]);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await fetchLeads(filter || undefined);
      setLeads(data.leads);
    } catch (e: any) {
      if (e.name === "AbortError") setError("Backend not responding. Start the server.");
      else setError("Could not load leads. Backend may be down.");
      setLeads([]);
    }
    setLoading(false);
  }

  const hotCount = leads.filter(l => l.verdict === "HOT").length;
  const warmCount = leads.filter(l => l.verdict === "WARM").length;

  if (error && leads.length === 0) {
    return (
      <div className="max-w-lg mx-auto mt-16 text-center">
        <h1 className="text-2xl font-semibold tracking-tight mb-3">Backend Not Running</h1>
        <p className="text-muted-foreground mb-4">{error}</p>
        <code className="block bg-muted rounded p-2 text-xs text-left">
          cd ~/Desktop/Dev/Github\ Repo\'s/Audio\ Freelance\ Dev\ System<br />
          uv run python main.py
        </code>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Leads</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {loading ? "Loading..." : `${leads.length} total · ${hotCount} hot · ${warmCount} warm`}
          </p>
        </div>
        <button onClick={load} className="rounded-md border border-border bg-card px-3 py-1.5 text-sm hover:bg-accent">
          {loading ? "..." : "Refresh"}
        </button>
      </div>

      <div className="flex flex-wrap gap-1">
        <button onClick={() => setFilter("")}
          className={`rounded-md px-3 py-1 text-xs ${!filter ? "bg-primary text-primary-foreground" : "bg-card border border-border hover:bg-accent"}`}
        >All</button>
        {STATUSES.map(s => (
          <button key={s} onClick={() => setFilter(s)}
            className={`rounded-md px-3 py-1 text-xs ${filter === s ? "bg-primary text-primary-foreground" : "bg-card border border-border hover:bg-accent"}`}
          >{s}</button>
        ))}
      </div>

      {loading ? (
        <p className="text-sm text-muted-foreground animate-pulse">Loading...</p>
      ) : leads.length === 0 ? (
        <p className="text-sm text-muted-foreground">No leads yet. Run a prospect scan from the Dashboard.</p>
      ) : (
        <div className="space-y-2">
          {leads.map((lead) => (
            <div key={lead.id} className="rounded-lg border border-border bg-card p-4 hover:bg-accent/50 transition-colors">
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className={`inline-block w-2 h-2 rounded-full ${lead.verdict === "HOT" ? "bg-red-500" : lead.verdict === "WARM" ? "bg-amber-500" : lead.verdict === "SKIP" ? "bg-gray-500" : "bg-blue-500"}`} />
                    <span className="font-medium truncate">{lead.title}</span>
                    {lead.tier ? <span className="text-xs text-muted-foreground shrink-0">T{lead.tier}</span> : null}
                  </div>
                  {lead.company && <p className="text-sm text-muted-foreground mt-0.5">{lead.company}</p>}
                  <p className="text-xs text-muted-foreground mt-1 truncate">{lead.raw_text.slice(0, 200)}</p>
                </div>
                <div className="text-right shrink-0">
                  <p className={`text-lg font-semibold ${lead.verdict === "HOT" ? "text-red-500" : lead.verdict === "WARM" ? "text-amber-500" : "text-muted-foreground"}`}>
                    {lead.score}
                  </p>
                  <p className="text-xs text-muted-foreground">{lead.source}</p>
                </div>
              </div>
              <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                <a href={lead.url} target="_blank" className="hover:text-foreground">Open →</a>
                <span>Status: {lead.status}</span>
                <span>{new Date(lead.discovered_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
