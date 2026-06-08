import type { SummaryRow } from "@/lib/summary";

export type ValidityStatus = "pass" | "fail" | "unknown" | "skip";

export function rowValidityStatus(row: SummaryRow): ValidityStatus {
  const v = row.validity_status;
  if (v === "pass" || v === "fail" || v === "unknown" || v === "skip") return v;
  return "unknown";
}

/** Green wall-clock status is only claimable when the validity gate passes. */
export function isPerfClaimable(row: SummaryRow): boolean {
  return row.status === "green" && rowValidityStatus(row) === "pass";
}

export function perfNotClaimableReason(row: SummaryRow): string | null {
  if (isPerfClaimable(row)) return null;
  const v = rowValidityStatus(row);
  if (v === "fail") {
    return "Correctness/stability gate failed — throughput is not claimable.";
  }
  if (v === "unknown") {
    return "Validity unknown — missing stability or harness pass signal.";
  }
  if (v === "skip") {
    return "Platform not measured in this ingest — see drill-down for OS coverage.";
  }
  if (row.status !== "green") {
    return `Perf status is ${row.status} — green ratio requires passing validity first.`;
  }
  return "Perf not claimable for this row.";
}

export function formatRatioVsSota(row: SummaryRow): string {
  if (row.ratio_vs_sota == null) return "—";
  const ref = row.sota_ref_lang ?? row.sota_lang ?? "competitor";
  const pct = (row.ratio_vs_sota * 100).toFixed(1);
  return `${row.ratio_vs_sota.toFixed(3)} (${pct}% of ${ref} speed)`;
}

export type PillarPerfCounts = {
  claimable: number;
  invalid: number;
  unknown: number;
  threshold: number;
};

export function pillarPerfCounts(rows: SummaryRow[], pillarId: string): PillarPerfCounts {
  const out: PillarPerfCounts = { claimable: 0, invalid: 0, unknown: 0, threshold: 0 };
  for (const row of rows) {
    if (row.pillar !== pillarId) continue;
    const v = rowValidityStatus(row);
    if (v === "fail") {
      out.invalid += 1;
      continue;
    }
    if (v === "unknown") {
      out.unknown += 1;
      continue;
    }
    if (isPerfClaimable(row)) {
      out.claimable += 1;
    } else if (row.status === "red" || row.status === "yellow") {
      out.threshold += 1;
    } else {
      out.unknown += 1;
    }
  }
  return out;
}
