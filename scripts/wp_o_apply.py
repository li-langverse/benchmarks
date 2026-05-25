#!/usr/bin/env python3
"""Apply WP-O overview tier card fix (run from repo root)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COVERAGE = r'''import type { SummaryRow } from "@/lib/summary";

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
'''

OVERVIEW_PATH = ROOT / "dashboard-next/lib/overview.ts"
overview_tail = OVERVIEW_PATH.read_text().split("export function emptyCounts", 1)
if len(overview_tail) < 2:
    raise SystemExit("overview.ts unexpected shape")
OVERVIEW = '''import {
  hasWallClock,
  isCatalogPending,
  rowCoverageKind,
} from "@/lib/coverage";
import type { ReleaseIndex } from "@/lib/release-index";
import type { StatusCounts, SummaryRow } from "@/lib/summary";

const STATUS_KEYS = ["green", "yellow", "red", "unknown"] as const;

export type TierCoverageSplit = {
  measured: StatusCounts;
  pending: number;
};

export function splitTierCounts(rows: SummaryRow[]): Record<string, TierCoverageSplit> {
  const out: Record<string, TierCoverageSplit> = {};
  for (const row of rows) {
    const tier = String(row.tier);
    if (!out[tier]) {
      out[tier] = {
        measured: { green: 0, yellow: 0, red: 0, unknown: 0 },
        pending: 0,
      };
    }
    if (isCatalogPending(row) || !hasWallClock(row)) {
      out[tier].pending += 1;
      continue;
    }
    const st = row.status;
    if (st === "green" || st === "yellow" || st === "red") {
      out[tier].measured[st] += 1;
    } else {
      out[tier].measured.unknown += 1;
    }
  }
  return out;
}

export type PillarOverviewCounts = {
  measured: StatusCounts;
  pending: number;
};

export function countPillarOverview(
  rows: SummaryRow[],
): Record<string, PillarOverviewCounts> {
  const out: Record<string, PillarOverviewCounts> = {};
  for (const row of rows) {
    const pillar = row.pillar;
    if (!pillar) continue;
    if (!out[pillar]) {
      out[pillar] = { measured: emptyCounts(), pending: 0 };
    }
    if (rowCoverageKind(row) === "pending") {
      out[pillar].pending += 1;
      continue;
    }
    const st = row.status;
    if (st === "green" || st === "yellow" || st === "red") {
      out[pillar].measured[st] += 1;
    } else if (hasWallClock(row)) {
      out[pillar].measured.unknown += 1;
    } else {
      out[pillar].pending += 1;
    }
  }
  return out;
}

export function topPendingBenchmarks(
  rows: SummaryRow[],
  pillarId: string,
  limit = 3,
): string[] {
  return rows
    .filter((r) => r.pillar === pillarId && rowCoverageKind(r) === "pending")
    .map((r) => r.benchmark)
    .slice(0, limit);
}

export function emptyCounts''' + overview_tail[1]

(ROOT / "dashboard-next/lib/coverage.ts").write_text(COVERAGE)
OVERVIEW_PATH.write_text(OVERVIEW)
print("wrote coverage.ts and overview.ts")
