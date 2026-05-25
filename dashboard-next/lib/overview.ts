import type { ReleaseIndex } from "@/lib/release-index";
import type { StatusCounts, Summary, SummaryRow } from "@/lib/summary";

const STATUS_KEYS = ["green", "yellow", "red", "unknown"] as const;

export function emptyCounts(): StatusCounts {
  return { green: 0, yellow: 0, red: 0, unknown: 0 };
}

/** Per-pillar status counts from catalog rows (row.pillar), not category filters. */
export function countStatusesByPillar(rows: SummaryRow[]): Record<string, StatusCounts> {
  const out: Record<string, StatusCounts> = {};
  for (const row of rows) {
    const pillar = row.pillar;
    if (!pillar) continue;
    if (!out[pillar]) out[pillar] = emptyCounts();
    incrementCounts(out[pillar], row.status);
  }
  return out;
}

export function topBenchmarksByStatus(
  rows: SummaryRow[],
  pillarId: string,
  status: string,
  limit = 3,
): string[] {
  return rows
    .filter((r) => r.pillar === pillarId && r.status === status)
    .map((r) => r.benchmark)
    .slice(0, limit);
}

export function regressionRows(summary: Summary): SummaryRow[] {
  return summary.rows.filter((r) => r.status === "red");
}

export type FreshnessLevel = "fresh" | "warn" | "stale" | "missing";

export type PackageFreshnessRow = {
  id: string;
  level: FreshnessLevel;
  version?: string;
  published_at?: string;
  ageDays: number | null;
};

const FRESHNESS_PACKAGES = ["lip", "lit", "lis", "lic"] as const;

export function packageFreshnessRows(
  index: ReleaseIndex,
  referenceIso: string,
): PackageFreshnessRow[] {
  const refMs = Date.parse(referenceIso);
  const refValid = Number.isFinite(refMs);

  return FRESHNESS_PACKAGES.map((id) => {
    const entry = index.packages[id];
    if (!entry?.published_at) {
      return { id, level: "missing" as const, ageDays: null };
    }
    const pubMs = Date.parse(entry.published_at);
    if (!refValid || !Number.isFinite(pubMs)) {
      return {
        id,
        level: "missing" as const,
        version: entry.version,
        published_at: entry.published_at,
        ageDays: null,
      };
    }
    const ageDays = Math.floor((refMs - pubMs) / (1000 * 60 * 60 * 24));
    let level: FreshnessLevel = "fresh";
    if (ageDays > 30) level = "stale";
    else if (ageDays > 7) level = "warn";
    return {
      id,
      level,
      version: entry.version,
      published_at: entry.published_at,
      ageDays,
    };
  });
}

export function incrementCounts(counts: StatusCounts, status: string): void {
  if (STATUS_KEYS.includes(status as (typeof STATUS_KEYS)[number])) {
    counts[status as keyof StatusCounts] += 1;
  } else {
    counts.unknown += 1;
  }
}
