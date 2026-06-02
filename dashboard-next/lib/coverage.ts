import type { StatusCounts, SummaryRow } from "@/lib/summary";
import { groupByBenchmark, pickPrimaryRow } from "@/lib/benchmark-groups";

/** Platform placeholder — catalog expects OS but nightly CSV has no measurements. */
export function isPlatformSkip(row: SummaryRow): boolean {
  return row.status === "skip" || row.validity_status === "skip";
}

/** Mirrors `scripts/ingest/build_summary.py` `is_pending_catalog_row` without catalog.toml at runtime. */
export function isCatalogPending(row: SummaryRow): boolean {
  if (row.pending === true) return true;
  if (isPlatformSkip(row)) return true;
  if (row.status !== "unknown") return false;
  if (row.li_value != null || row.cpp_value != null) return false;
  if (row.path === "unknown" || row.benchmark.endsWith("_stub")) return true;
  if (row.base_id) return true;
  if (row.size_label === "harness pending") return true;
  return false;
}

export function isMeasured(row: SummaryRow): boolean {
  if (row.status === "green" || row.status === "yellow" || row.status === "red") {
    return true;
  }
  return row.li_value != null || row.cpp_value != null;
}

export function isValidityFailed(row: SummaryRow): boolean {
  if (isCatalogPending(row)) return false;
  return row.validity_status === "fail";
}

export type RowCoverageKind =
  | "measured"
  | "pending"
  | "platform_skip"
  | "validity_fail"
  | "validity_unknown";

export function rowCoverageKind(row: SummaryRow): RowCoverageKind {
  if (isPlatformSkip(row)) return "platform_skip";
  if (isCatalogPending(row)) return "pending";
  if (isValidityFailed(row)) return "validity_fail";
  if (isMeasured(row) && row.validity_status !== "pass") return "validity_unknown";
  return "measured";
}

export type TierCoverageSplit = {
  measured: StatusCounts;
  pending: number;
};

export function splitTierCounts(rows: SummaryRow[]): Record<string, TierCoverageSplit> {
  const out: Record<string, TierCoverageSplit> = {};
  for (const group of groupByBenchmark(rows)) {
    const row = pickPrimaryRow(group.variants);
    const tier = String(row.tier);
    if (!out[tier]) {
      out[tier] = {
        measured: { green: 0, yellow: 0, red: 0, unknown: 0 },
        pending: 0,
      };
    }
    if (isCatalogPending(row) && !isMeasured(row)) {
      out[tier].pending += 1;
      continue;
    }
    const st = row.status;
    if (st === "green" || st === "yellow" || st === "red") {
      out[tier].measured[st] += 1;
    } else if (isMeasured(row)) {
      out[tier].measured.unknown += 1;
    } else {
      out[tier].pending += 1;
    }
  }
  return out;
}

export type CoverageHonesty = {
  total: number;
  measured: number;
  pending: number;
  validityFail: number;
  validityUnknown: number;
};

export function coverageHonesty(rows: SummaryRow[]): CoverageHonesty {
  const out: CoverageHonesty = {
    total: 0,
    measured: 0,
    pending: 0,
    validityFail: 0,
    validityUnknown: 0,
  };
  for (const group of groupByBenchmark(rows)) {
    out.total += 1;
    const row = pickPrimaryRow(group.variants);
    const kind = rowCoverageKind(row);
    if (kind === "pending" || kind === "platform_skip") out.pending += 1;
    else if (kind === "validity_fail") {
      out.validityFail += 1;
      out.measured += 1;
    } else if (kind === "validity_unknown") {
      out.validityUnknown += 1;
      out.measured += 1;
    } else {
      out.measured += 1;
    }
  }
  return out;
}

export const COVERAGE_GAP_DOC =
  "https://github.com/li-langverse/benchmarks/blob/main/docs/dashboard/coverage-gap-analysis.md";
