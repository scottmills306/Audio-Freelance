const API = "/api/v1";

async function get<T>(path: string, timeoutMs = 10000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API}${path}`, { signal: controller.signal });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return res.json();
  } finally {
    clearTimeout(timer);
  }
}

async function post<T>(path: string, timeoutMs = 30000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${API}${path}`, { method: "POST", signal: controller.signal });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return res.json();
  } finally {
    clearTimeout(timer);
  }
}

export interface LeadCounts {
  NEW?: number; HOT?: number; WARM?: number; COLD?: number;
  CONTACTED?: number; SKIPPED?: number; PROPOSAL_SENT?: number; WON?: number; LOST?: number; DEAD?: number;
}

export interface StatusResponse {
  lead_counts: LeadCounts;
  ollama_available: boolean;
  timestamp: string;
}

export interface Lead {
  id: string; source: string; tier: number; title: string; company?: string;
  url: string; raw_text: string; niche: string; signals: Record<string, number>;
  score: number; verdict: "HOT" | "WARM" | "COLD" | "SKIP"; status: string;
  contact_path?: string; discovered_at: string; last_updated: string; notes?: string;
}

export interface HealthResponse {
  status: string; ollama: boolean; timestamp: string;
}

export interface TechTrend {
  technology: string; mentions: number; direction: "rising" | "stable" | "declining"; contexts: string[];
}

export interface PricingBenchmark {
  niche: string; contract_range_min: number; contract_range_max: number;
  hourly_min: number; hourly_max: number; sample_count: number;
}

export interface MarketSignal {
  category: string; source: string; title: string; url: string;
  snippet: string; relevance: number; tags: string[];
}

export interface MarketReport {
  scanned_at: string; summary: string; total_signals: number;
  signals: MarketSignal[]; tech_trends: TechTrend[]; pricing_benchmarks: PricingBenchmark[]; hot_opportunities: string[];
}

export interface ProspectResult {
  niche: string; total_candidates: number; total_leads: number;
  hot: number; warm: number; cold: number; skipped: number;
  hot_leads: Lead[]; warm_leads: Lead[]; errors: string[];
}

export async function fetchHealth(): Promise<HealthResponse> {
  return get("/health");
}

export async function fetchStatus(): Promise<StatusResponse> {
  return get("/status");
}

export async function fetchLeads(status?: string): Promise<{ count: number; leads: Lead[] }> {
  const qs = status ? `?status=${status}` : "";
  return get(`/leads${qs}`);
}

export async function fetchMarket(): Promise<MarketReport> {
  return get("/market", 60000);
}

export async function fetchMarketTrends(): Promise<{
  scanned_at: string; tech_trends: TechTrend[];
}> {
  return get("/market/trends", 60000);
}

export async function fetchMarketPricing(): Promise<{
  scanned_at: string; pricing_benchmarks: PricingBenchmark[];
}> {
  return get("/market/pricing", 60000);
}

export async function fetchMarketOpportunities(): Promise<{
  scanned_at: string; summary: string; opportunities: string[]; recent_signals: MarketSignal[];
}> {
  return get("/market/opportunities", 60000);
}

export async function prospectNiche(niche: string): Promise<ProspectResult> {
  return post(`/prospect/${niche}`, 120000);
}
