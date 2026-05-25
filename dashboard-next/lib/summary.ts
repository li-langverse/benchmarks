import { readFileSync } from "fs";
import path from "path";

export type StatusCounts = {
  green: number;
  yellow: number;
  red: number;
  unknown: number;
};

export type LangPoint = {
  lang: string;
  value: number;
  unit: string;
  variant?: string;
  label?: string;
  passed?: boolean;
};

export type ChartSpec = {
  id: string;
  title: string;
  metric: string;
  unit: string;
  lower_is_better: boolean;
  reference_lang: string;
  series: LangPoint[];
  grouped?: boolean;
  repo: string;
  path: string;
  status: string;
  ratio_vs_reference?: number | null;
  pending?: boolean;
};

export type CategoryBlock = {
  label: string;
  charts: ChartSpec[];
};

export type SummaryRow = {
  benchmark: string;
  repo: string;
  tier: number;
  category?: string;
  pillar?: string;
  package?: string;
  metric: string;
  li_value: number | null;
  cpp_value: number | null;
  ratio_vs_cpp: number | null;
  unit: string | null;
  variant?: string | null;
  status: string;
  ph_ids: string[];
  path: string;
  threshold_ratio_cpp: number;
  ci_url?: string;
  langs?: LangPoint[];
};

export type Summary = {
  generated_at: string;
  sources: Record<string, string>;
  tier_counts: Record<string, StatusCounts>;
  categories: Record<string, CategoryBlock>;
  rows: SummaryRow[];
};

const SUMMARY_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "summary.json",
);

/** Public URL for deployed static assets (runtime / client). */
export const SUMMARY_PUBLIC_URL = "/benchmarks/latest/summary.json";

/**
 * Load summary.json at build time from ../data/latest/summary.json.
 * Used in server components and generateStaticParams.
 */
export function loadSummary(): Summary {
  const raw = readFileSync(SUMMARY_PATH, "utf8");
  return JSON.parse(raw) as Summary;
}

export function findRow(summary: Summary, benchmarkId: string): SummaryRow | undefined {
  return summary.rows.find((r) => r.benchmark === benchmarkId);
}
