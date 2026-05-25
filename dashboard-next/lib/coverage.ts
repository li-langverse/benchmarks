import type { SummaryRow } from "@/lib/summary";

/** Mirrors `scripts/ingest/build_summary.py` `is_pending_catalog_row` without catalog.toml at runtime. */
export function isCatalogPending(row: SummaryRow): boolean {
  if (row.pending === true) return true;
  if (row.status !== "unknown") return false;
  if (row.li_value != null || row.cpp_value != null) return false;
  if (row.path === "unknown" || row.benchmark.endsWith("_stub")) return true;
  if (row.base_id) return true;
  if (row.size_label === "harness pending") return true;
  return false;
}

/** Row has wall-clock perf in this ingest (colored status or oracle values). */
export function hasWallClock(row: SummaryRow): boolean {
  if (row.status === "green" || row.status === "yellow" || row.status === "red") {
    return true;
  }
  return row.li_value != null || row.cpp_value != null;
}

/** @deprecated Use {@link hasWallClock}. */
export function isMeasured(row: SummaryRow): boolean {
  return hasWallClock(row);
}

export function isValidityFailed(row: SummaryRow): boolean {
  if (isCatalogPending(row)) return false;
  return row.validity_status === "fail";
}

export type RowCoverageKind = "measured" | "pending" | "validity_fail" | "validity_unknown";

export function rowCoverageKind(row: SummaryRow): RowCoverageKind {
  if (isCatalogPending(row)) return "pending";
  if (!hasWallClock(row)) return "pending";
  if (isValidityFailed(row)) return "validity_fail";
  if (row.validity_status !== "pass") return "validity_unknown";
  return "measured";
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
    total: rows.length,
    measured: 0,
    pending: 0,
    validityFail: 0,
    validityUnknown: 0,
  };
  for (const row of rows) {
    const kind = rowCoverageKind(row);
    if (kind === "pending") out.pending += 1;
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
