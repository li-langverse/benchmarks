import { rowCoverageKind, type RowCoverageKind } from "@/lib/coverage";
import type { SummaryRow } from "@/lib/summary";
import { Badge } from "@/components/ui/badge";

type CoverageStatusBadgeProps = {
  row: SummaryRow;
  showPerfStatus?: boolean;
};

export function CoverageStatusBadge({
  row,
  showPerfStatus = true,
}: CoverageStatusBadgeProps) {
  const kind = rowCoverageKind(row);
  if (showPerfStatus && kind === "measured") {
    return <Badge status={row.status} />;
  }
  if (!showPerfStatus) {
    if (kind === "pending") {
      return (
        <span className="badge badge-unknown badge-pending" title={coverageTitle(kind)}>
          pending
        </span>
      );
    }
    if (kind === "validity_fail") {
      return (
        <span className="badge badge-red badge-validity-fail" title={coverageTitle(kind)}>
          fail
        </span>
      );
    }
    if (kind === "validity_unknown") {
      return (
        <span
          className="badge badge-unknown badge-validity-unknown"
          title={coverageTitle(kind)}
        >
          unknown
        </span>
      );
    }
    return (
      <Badge status={row.validity_status === "pass" ? "green" : "unknown"}>
        {row.validity_status ?? "pass"}
      </Badge>
    );
  }
  const label =
    kind === "pending"
      ? "pending"
      : kind === "validity_fail"
        ? "validity fail"
        : kind === "validity_unknown"
          ? "validity ?"
          : row.status;
  const extra =
    kind === "pending"
      ? "badge-pending"
      : kind === "validity_fail"
        ? "badge-validity-fail"
        : kind === "validity_unknown"
          ? "badge-validity-unknown"
          : "";
  return (
    <span className={`badge badge-unknown ${extra}`.trim()} title={coverageTitle(kind)}>
      {label}
    </span>
  );
}

function coverageTitle(kind: RowCoverageKind): string {
  switch (kind) {
    case "pending":
      return "Catalog placeholder — no wall-clock CSV in this ingest";
    case "validity_fail":
      return "Measured but validity gate failed";
    case "validity_unknown":
      return "Wall-clock present; validity signal missing";
    default:
      return "Measured perf status";
  }
}
