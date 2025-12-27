export interface KPIResult {
  project_id: number;
  ev: number;
  ac: number;
  pv: number;
  cv: number;
  sv: number;
  cpi: number;
  spi: number;
}

export interface PortfolioKPIs {
  kpis: KPIResult[];
  totals: Record<string, number>;
}

export interface Project {
  id: number;
  client_id: number;
  region: string;
  sector: string;
  start_date: string;
  end_date: string;
  baseline_budget: number;
  current_forecast: number;
  actual_spend: number;
  baseline_schedule_days: number;
  forecast_schedule_days: number;
  percent_complete: number;
  safety_incidents: number;
  status: string;
}

export interface Recommendation {
  decision_type: string;
  affected_project_ids: number[];
  expected_impact: Record<string, any>;
  explanation: string;
  confidence: number;
}

export interface Decision {
  id: number;
  decision_type: string;
  rationale: string;
  status: string;
  owner: string;
  related_project_ids: number[];
}

export interface GapInput {
  id: number;
  created_at: string;
  category: string;
  question: string;
  answer: string;
  confidence: number;
}

export interface ProcessTemplate {
  id: number;
  name: string;
  description: string;
  adoption_rate_pct: number;
}

export interface ScenarioResult {
  project_id: number;
  p50_cost: number;
  p80_cost: number;
  p50_days: number;
  p80_days: number;
}
