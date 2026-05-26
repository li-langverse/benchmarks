import type { SummaryRow } from "@/lib/summary";

export type OracleKind = "analytical" | "iterative" | "pending";

export function rowOracleKind(row: SummaryRow): OracleKind {
  if (row.pending) return "pending";
  const oracle = row.numeric_validity?.oracle;
  if (oracle === "analytical" || oracle === "iterative") return oracle;
  return "iterative";
}

export function oracleLabel(kind: OracleKind): string {
  switch (kind) {
    case "analytical":
      return "analytical closed form";
    case "iterative":
      return "iterative spec (C loop)";
    case "pending":
      return "not measured";
  }
}

export function rowWithin1Ulp(row: SummaryRow): boolean | null {
  if (row.pending) return null;
  if (row.numeric_validity?.within_1ulp != null) {
    return row.numeric_validity.within_1ulp;
  }
  return null;
}
