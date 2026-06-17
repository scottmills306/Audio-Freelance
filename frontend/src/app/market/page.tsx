"use client";

import { useEffect, useState } from "react";
import { fetchMarket, MarketReport } from "@/lib/api";

export default function MarketPage() {
  const [report, setReport] = useState<MarketReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    try { setReport(await fetchMarket()); } catch { setReport(null); }
    setLoading(false);
  }

  if (loading) return <p className="text-sm text-muted-foreground animate-pulse">Scanning market...</p>;
  if (!report) {
    return (
      <div className="max-w-lg mx-auto mt-16 text-center">
        <h1 className="text-2xl font-semibold tracking-tight mb-3">Backend Not Running</h1>
        <p className="text-muted-foreground mb-4">Start the backend to scan the market.</p>
        <code className="block bg-muted rounded p-2 text-xs text-left">
          cd ~/Desktop/Dev/Github\ Repo\'s/Audio\ Freelance\ Dev\ System<br />
          uv run python main.py
        </code>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Market Intelligence</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {report.total_signals} signals · Scanned {new Date(report.scanned_at).toLocaleString()}
          </p>
        </div>
        <button onClick={load} className="rounded-md border border-border bg-card px-3 py-1.5 text-sm hover:bg-accent">
          Rescan
        </button>
      </div>

      {/* Summary */}
      <div className="rounded-lg border border-border bg-card p-5">
        <p className="text-sm">{report.summary}</p>
      </div>

      {/* Technology Trends */}
      <div>
        <h2 className="text-base font-medium mb-4">Technology Trends</h2>
        <div className="rounded-lg border border-border bg-card overflow-hidden">
          {report.tech_trends.length === 0 ? (
            <p className="text-sm text-muted-foreground p-5">No trends detected.</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left p-3 font-medium text-muted-foreground">Technology</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">Mentions</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">Direction</th>
                </tr>
              </thead>
              <tbody>
                {report.tech_trends.map((t) => (
                  <tr key={t.technology} className="border-b border-border last:border-0">
                    <td className="p-3">{t.technology}</td>
                    <td className="p-3 text-right">{t.mentions}</td>
                    <td className="p-3 text-right">
                      <span className={`text-xs ${
                        t.direction === "rising" ? "text-green-500" :
                        t.direction === "declining" ? "text-red-500" : "text-muted-foreground"
                      }`}>
                        {t.direction === "rising" ? "↑ Rising" : t.direction === "declining" ? "↓ Declining" : "→ Stable"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Pricing */}
      <div>
        <h2 className="text-base font-medium mb-4">Pricing Benchmarks</h2>
        <div className="rounded-lg border border-border bg-card overflow-hidden">
          {report.pricing_benchmarks.length === 0 ? (
            <p className="text-sm text-muted-foreground p-5">No pricing data found.</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left p-3 font-medium text-muted-foreground">Niche</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">Contract Range</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">Hourly</th>
                  <th className="text-right p-3 font-medium text-muted-foreground">Samples</th>
                </tr>
              </thead>
              <tbody>
                {report.pricing_benchmarks.map((p) => (
                  <tr key={p.niche} className="border-b border-border last:border-0">
                    <td className="p-3">{p.niche.replace("_", " ")}</td>
                    <td className="p-3 text-right">${p.contract_range_min.toLocaleString()}–${p.contract_range_max.toLocaleString()}</td>
                    <td className="p-3 text-right">{p.hourly_min > 0 ? `$${p.hourly_min}–$${p.hourly_max}/hr` : "—"}</td>
                    <td className="p-3 text-right">{p.sample_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Opportunities */}
      {report.hot_opportunities.length > 0 && (
        <div>
          <h2 className="text-base font-medium mb-4">Opportunities</h2>
          <div className="space-y-2">
            {report.hot_opportunities.map((o, i) => (
              <div key={i} className="rounded-lg border border-border bg-card p-4 text-sm">
                {o}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Raw Signals */}
      <div>
        <h2 className="text-base font-medium mb-4">Recent Signals ({report.total_signals})</h2>
        <div className="space-y-2">
          {report.signals.slice(0, 20).map((s, i) => (
            <div key={i} className="rounded-lg border border-border bg-card p-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs bg-accent text-accent-foreground rounded px-1.5 py-0.5">{s.category}</span>
                <span className="text-xs text-muted-foreground">{s.source}</span>
                <span className="text-xs text-muted-foreground">· {s.relevance}/10</span>
              </div>
              <p className="text-sm font-medium">{s.title}</p>
              <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{s.snippet}</p>
              {s.url && <a href={s.url} target="_blank" className="text-xs text-blue-500 hover:underline mt-1 block">Open →</a>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
