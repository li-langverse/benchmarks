import { isPlatformSkip } from "@/lib/coverage";
import type { SummaryRow } from "@/lib/summary";

export type BenchmarkGroup = {
  benchmark: string;
  primary: SummaryRow;
  variants: SummaryRow[];
};

const OS_ORDER = ["linux", "darwin", "macos", "windows"];

function isMeasuredStatus(status: string): boolean {
  return status === "green" || status === "yellow" || status === "red";
}

/** Prefer a measured linux row; else any measured OS; else first catalog platform. */
export function pickPrimaryRow(variants: SummaryRow[]): SummaryRow {
  const measured = variants.filter((r) => isMeasuredStatus(r.status));
  if (measured.length) {
    for (const os of OS_ORDER) {
      const hit = measured.find((r) => r.os === os);
      if (hit) return hit;
    }
    return measured[0];
  }
  for (const os of OS_ORDER) {
    const hit = variants.find((r) => r.os === os);
    if (hit) return hit;
  }
  return variants[0];
}

export function formatOsSummary(variants: SummaryRow[]): string {
  const sorted = [...variants].sort((a, b) => {
    const ai = OS_ORDER.indexOf(a.os ?? "");
    const bi = OS_ORDER.indexOf(b.os ?? "");
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });
  return sorted
    .map((r) => {
      const os = r.os ?? "?";
      if (isMeasuredStatus(r.status)) return `${os} ✓`;
      if (isPlatformSkip(r) || r.pending) return `${os} skip`;
      if (r.status === "unknown") return `${os} ?`;
      return os;
    })
    .join(" · ");
}

export function groupByBenchmark(rows: SummaryRow[]): BenchmarkGroup[] {
  const map = new Map<string, SummaryRow[]>();
  for (const row of rows) {
    const list = map.get(row.benchmark) ?? [];
    list.push(row);
    map.set(row.benchmark, list);
  }
  return [...map.entries()]
    .map(([benchmark, variants]) => ({
      benchmark,
      variants,
      primary: pickPrimaryRow(variants),
    }))
    .sort((a, b) => a.benchmark.localeCompare(b.benchmark));
}

export function rowForOs(group: BenchmarkGroup, os: string | null): SummaryRow {
  if (!os) return group.primary;
  return group.variants.find((r) => r.os === os) ?? group.primary;
}

export function groupMatchesQuery(group: BenchmarkGroup, q: string): boolean {
  const needle = q.trim().toLowerCase();
  if (!needle) return true;
  return group.variants.some((row) => {
    if (row.benchmark.toLowerCase().includes(needle)) return true;
    if (row.package?.toLowerCase().includes(needle)) return true;
    if (row.pillar?.toLowerCase().includes(needle)) return true;
    if (row.ph_ids.some((id) => id.toLowerCase().includes(needle))) return true;
    if (row.os?.toLowerCase().includes(needle)) return true;
    if (row.sota_lang?.toLowerCase().includes(needle)) return true;
    if (row.size_label?.toLowerCase().includes(needle)) return true;
    if (row.problem_size?.toLowerCase().includes(needle)) return true;
    if (row.base_id?.toLowerCase().includes(needle)) return true;
    return false;
  });
}
