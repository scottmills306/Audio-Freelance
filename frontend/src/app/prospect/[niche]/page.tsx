"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { prospectNiche, ProspectResult } from "@/lib/api";

export default function ProspectPage() {
  const params = useParams();
  const niche = params.niche as string;
  const [result, setResult] = useState<ProspectResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    prospectNiche(niche)
      .then(setResult)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [niche]);

  const allLeads = [...(result?.hot_leads || []), ...(result?.warm_leads || [])];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight capitalize">{niche.replace("_", " ")}</h1>
        <p className="text-sm text-muted-foreground mt-1">Prospect scan results</p>
      </div>

      {loading && <p className="text-sm text-muted-foreground">Scanning...</p>}
      {error && <p className="text-sm text-red-500">Error: {error}</p>}

      {result && (
        <>
          <div className="grid grid-cols-4 gap-4">
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs text-muted-foreground uppercase">Candidates</p>
              <p className="text-2xl font-semibold mt-1">{result.total_candidates}</p>
            </div>
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs text-muted-foreground uppercase">Hot</p>
              <p className="text-2xl font-semibold mt-1 text-red-500">{result.hot}</p>
            </div>
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs text-muted-foreground uppercase">Warm</p>
              <p className="text-2xl font-semibold mt-1 text-amber-500">{result.warm}</p>
            </div>
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs text-muted-foreground uppercase">Errors</p>
              <p className="text-2xl font-semibold mt-1">{result.errors.length}</p>
            </div>
          </div>

          {result.errors.length > 0 && (
            <div className="rounded-lg border border-red-500/30 bg-card p-4">
              <p className="text-sm font-medium text-red-500">Errors</p>
              {result.errors.map((e, i) => <p key={i} className="text-xs text-muted-foreground mt-1">{e}</p>)}
            </div>
          )}

          {allLeads.length === 0 ? (
            <p className="text-sm text-muted-foreground">No hot or warm leads found for this niche.</p>
          ) : (
            <div className="space-y-2">
              <h2 className="text-base font-medium">Hot & Warm Leads</h2>
              {allLeads.map((lead) => (
                <div key={lead.id} className="rounded-lg border border-border bg-card p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`inline-block w-2 h-2 rounded-full ${lead.verdict === "HOT" ? "bg-red-500" : "bg-amber-500"}`} />
                        <span className="font-medium">{lead.title}</span>
                      </div>
                      {lead.company && <p className="text-sm text-muted-foreground mt-0.5">{lead.company}</p>}
                      <p className="text-xs text-muted-foreground mt-1">{lead.raw_text.slice(0, 200)}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <p className={`text-lg font-semibold ${lead.verdict === "HOT" ? "text-red-500" : "text-amber-500"}`}>
                        {lead.score}
                      </p>
                      <p className="text-xs text-muted-foreground">{lead.source}</p>
                    </div>
                  </div>
                  <div className="mt-2 flex gap-2 text-xs">
                    <a href={lead.url} target="_blank" className="text-blue-500 hover:underline">Open →</a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
