import type { SummaryRow } from "@/lib/summary";
import { isPerfClaimable, perfNotClaimableReason } from "@/lib/validity";

type PerfNotClaimableProps = {
  row: SummaryRow;
};

export function PerfNotClaimable({ row }: PerfNotClaimableProps) {
  if (isPerfClaimable(row)) return null;
  const reason = perfNotClaimableReason(row);
  if (!reason) return null;

  return (
    <aside className="perf-not-claimable" role="alert">
      <strong>Perf not claimable</strong>
      <p>{reason}</p>
    </aside>
  );
}
