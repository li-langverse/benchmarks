import { readFileSync } from "fs";
import path from "path";

export type StatusCounts = {
  green: number;
  yellow: number;
  red: number;
  unknown: number;
};

export type ValidityStatus = "pass" | "fail" | "unknown";

export type NumericValidity = {
  oracle: string;
  analytical_value?: number | null;
  checksum_value?: number | null;
  abs_error?: number | null;
  rel_error?: number | null;
  ulps?: number | null;
  within_1ulp?: boolean;
};

export type LangPoint = {
  lang: string;
  /** Wall-clock or metric mean (harness no longer uses median). */
  value: number;
  /** Sample standard deviation (same unit as value). */
  stddev?: number | null;
  /** Number of timed repetitions aggregated into value/stddev. */
  sample_runs?: number | null;
  unit: string;
  variant?: string;
  label?: string;
  passed?: boolean;
  os?: string;
  /** Relative speed vs best competitor — SOTA lang = 1.0, higher is better. */
  relative_perf?: number;
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
  ratio_vs_sota?: number | null;
  sota_lang?: string | null;
  validity_status?: ValidityStatus;
  validity_source?: string;
  os?: string;
  pending?: boolean;
  problem_size?: string | null;
  size_label?: string | null;
  base_id?: string | null;
};

export type CategoryBlock = {
  label: string;
  charts: ChartSpec[];
};

export type PillarBlock = {
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
  li_stddev?: number | null;
  li_sample_runs?: number | null;
  cpp_value: number | null;
  cpp_stddev?: number | null;
  cpp_sample_runs?: number | null;
  ratio_vs_cpp: number | null;
  ratio_vs_sota?: number | null;
  sota_lang?: string | null;
  sota_value?: number | null;
  unit: string | null;
  variant?: string | null;
  problem_size?: string | null;
  size_label?: string | null;
  base_id?: string | null;
  status: string;
  validity_status?: ValidityStatus;
  validity_source?: string;
  numeric_validity?: NumericValidity | null;
  os?: string;
  compare_oracle?: string;
  ph_ids: string[];
  path: string;
  threshold_ratio_cpp: number;
  ci_url?: string;
  langs?: LangPoint[];
  pending?: boolean;
};

export type SummaryReporting = {
  sota_policy?: string;
  /** Primary aggregate for timed metrics in latest.csv (mean of repetitions). */
  value_stat?: "mean";
  /** Diagram axis: relative_perf where 1.0 = best competitor speed. */
  relative_perf_higher_is_better?: boolean;
  validity_required_default?: boolean;
  os_values?: string[];
  size_labels?: string[];
};

export type Summary = {
  generated_at: string;
  sources: Record<string, string>;
  reporting?: SummaryReporting;
  tier_counts: Record<string, StatusCounts>;
  categories: Record<string, CategoryBlock>;
  pillars?: Record<string, PillarBlock>;
  rows: SummaryRow[];
};

const SUMMARY_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "summary.json",
);

export const SUMMARY_PUBLIC_URL = "/benchmarks/latest/summary.json";

export function loadSummary(): Summary {
  const raw = readFileSync(SUMMARY_PATH, "utf8");
  return JSON.parse(raw) as Summary;
}

export function findRow(
  summary: Summary,
  benchmarkId: string,
  os?: string | null,
): SummaryRow | undefined {
  if (os) {
    const exact = summary.rows.find(
      (r) => r.benchmark === benchmarkId && r.os === os,
    );
    if (exact) return exact;
  }
  return summary.rows.find((r) => r.benchmark === benchmarkId);
}

/** All ingest rows for a catalog benchmark (one per measured OS). */
export function rowsForBenchmark(summary: Summary, benchmarkId: string): SummaryRow[] {
  return summary.rows.filter((r) => r.benchmark === benchmarkId);
}

export function summaryLookupKey(row: SummaryRow): string {
  if (row.os && row.os !== "unknown") {
    return `${row.benchmark}@${row.os}`;
  }
  return row.benchmark;
}

export function buildSummaryById(rows: SummaryRow[]): Record<string, SummaryRow> {
  const out: Record<string, SummaryRow> = {};
  for (const row of rows) {
    out[summaryLookupKey(row)] = row;
    if (!out[row.benchmark]) {
      out[row.benchmark] = row;
    }
  }
  return out;
}

