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
  if (showPerfStatus && kind === "platform_skip") {
    return (
      <Badge status="skip" title={platformSkipTitle(row)}>
        skip
      </Badge>
    );
  }
  if (!showPerfStatus) {
    if (kind === "platform_skip") {
      return (
        <Badge status="skip" title={platformSkipTitle(row)}>
          skip
        </Badge>
      );
    }
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
      : kind === "platform_skip"
        ? "skip"
        : kind === "validity_fail"
          ? "validity fail"
          : kind === "validity_unknown"
            ? "validity ?"
            : row.status;
  const extra =
    kind === "pending"
      ? "badge-pending"
      : kind === "platform_skip"
        ? "badge-skip"
        : kind === "validity_fail"
          ? "badge-validity-fail"
          : kind === "validity_unknown"
            ? "badge-validity-unknown"
            : "";
  return (
    <span className={`badge badge-unknown ${extra}`.trim()} title={coverageTitle(kind, row)}>
      {label}
    </span>
  );
}

function platformSkipTitle(row: SummaryRow): string {
  const src = row.validity_source ?? "platform_not_measured";
  return `Not measured on ${row.os ?? "this platform"} (${src}) — open drill-down for other OS results.`;
}

function coverageTitle(kind: RowCoverageKind, row?: SummaryRow): string {
  switch (kind) {
    case "pending":
      return "Catalog placeholder — no wall-clock CSV in this ingest";
    case "platform_skip":
      return platformSkipTitle(row!);
    case "validity_fail":
      return "Measured but validity gate failed";
    case "validity_unknown":
      return "Wall-clock present; validity signal missing";
    default:
      return "Measured perf status";
  }
}
