import type { SummaryRow } from "@/lib/summary";
import { rowWithin1Ulp } from "@/lib/oracle";

export type Tier1VerifyStats = {
  total: number;
  pass: number;
  fail: number;
  unknown: number;
  within1ulp: number;
  over1ulp: number;
  noNumeric: number;
};

/** Tier-1 micro rows with validity / numeric oracle signals (UX-B04). */
export function tier1VerifyStats(rows: SummaryRow[]): Tier1VerifyStats {
  const tier1 = rows.filter((r) => r.tier === 1 && !r.pending);
  const stats: Tier1VerifyStats = {
    total: tier1.length,
    pass: 0,
    fail: 0,
    unknown: 0,
    within1ulp: 0,
    over1ulp: 0,
    noNumeric: 0,
  };
  for (const row of tier1) {
    const vs = row.validity_status ?? "unknown";
    if (vs === "pass") stats.pass += 1;
    else if (vs === "fail") stats.fail += 1;
    else stats.unknown += 1;
    const ulp = rowWithin1Ulp(row);
    if (ulp === true) stats.within1ulp += 1;
    else if (ulp === false) stats.over1ulp += 1;
    else stats.noNumeric += 1;
  }
  return stats;
}
