import { rowOracleKind, rowWithin1Ulp } from "@/lib/oracle";
import type { SummaryRow } from "@/lib/summary";
import { rowValidityStatus } from "@/lib/validity";

export function rowMatchesValidityFilter(
  row: SummaryRow | undefined,
  validity: string | null,
): boolean {
  if (!validity) return true;
  if (!row) return validity === "unknown";
  return rowValidityStatus(row) === validity;
}

export function rowMatchesOracleFilter(
  row: SummaryRow | undefined,
  oracle: string | null,
): boolean {
  if (!oracle) return true;
  if (!row) return oracle === "pending";
  return rowOracleKind(row) === oracle;
}

export function rowMatchesWithin1UlpFilter(
  row: SummaryRow | undefined,
  within: string | null,
): boolean {
  if (!within) return true;
  if (!row) return false;
  const ulp = rowWithin1Ulp(row);
  if (within === "1") return ulp === true;
  if (within === "0") return ulp === false;
  return true;
}
