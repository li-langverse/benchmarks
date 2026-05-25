import { emptyCounts, incrementCounts } from "@/lib/overview";
import type { StatusCounts, SummaryRow } from "@/lib/summary";

export function isMeasuredPerfRow(row: SummaryRow): boolean {
  if (row.pending) return false;
  if (row.ratio_vs_sota == null || row.ratio_vs_sota <= 0) return false;
  if (row.li_value == null) return false;
  return true;
}

export function measuredPerfRows(rows: SummaryRow[]): SummaryRow[] {
  return rows.filter(isMeasuredPerfRow);
}

export function statusCountsForRows(rows: SummaryRow[]): StatusCounts {
  const counts = emptyCounts();
  for (const row of rows) incrementCounts(counts, row.status);
  return counts;
}

export type BenchmarkRelativeItem = {
  benchmark: string;
  relative: number;
  sotaLang?: string | null;
  status: string;
  claimable: boolean;
};

export function benchmarkRelativeItems(
  rows: SummaryRow[],
  claimableFn: (row: SummaryRow) => boolean,
): BenchmarkRelativeItem[] {
  return measuredPerfRows(rows).map((row) => ({
    benchmark: row.benchmark,
    relative: row.ratio_vs_sota!,
    sotaLang: row.sota_lang,
    status: row.status,
    claimable: claimableFn(row),
  }));
}

export function topRelativeItems(
  items: BenchmarkRelativeItem[],
  limit: number,
): BenchmarkRelativeItem[] {
  return [...items].sort((a, b) => b.relative - a.relative).slice(0, limit);
}

export function bottomRelativeItems(
  items: BenchmarkRelativeItem[],
  limit: number,
): BenchmarkRelativeItem[] {
  return [...items].sort((a, b) => a.relative - b.relative).slice(0, limit);
}
