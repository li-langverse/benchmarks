import type { StatusCounts } from "@/lib/summary";
import type { PillarPerfCounts } from "@/lib/validity";

type PillarSummaryStripProps = {
  statusCounts: StatusCounts;
  perfCounts: PillarPerfCounts;
  measuredCount: number;
  totalRows: number;
};

export function PillarSummaryStrip({
  statusCounts,
  perfCounts,
  measuredCount,
  totalRows,
}: PillarSummaryStripProps) {
  return (
    <div
      className="pillar-summary-strip"
      aria-label="Pillar status summary"
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "0.75rem 1.25rem",
        marginTop: "1rem",
        padding: "0.75rem 1rem",
        border: "1px solid var(--border)",
        borderRadius: "8px",
        background: "color-mix(in srgb, var(--border) 25%, transparent)",
      }}
    >
      <div className="counts pillar-counts">
        <span className="g">{statusCounts.green} green</span>
        <span className="y">{statusCounts.yellow} yellow</span>
        <span className="r">{statusCounts.red} red</span>
        <span className="u">{statusCounts.unknown} unknown</span>
      </div>
      <div className="counts pillar-perf-counts" aria-label="Perf claimability">
        <span className="g">{perfCounts.claimable} claimable</span>
        <span className="r">{perfCounts.invalid} invalid</span>
        <span className="u">{perfCounts.unknown} validity unknown</span>
        {perfCounts.threshold > 0 ? (
          <span className="y">{perfCounts.threshold} over threshold</span>
        ) : null}
      </div>
      <p className="mono" style={{ margin: 0, color: "var(--muted)", fontSize: "0.85rem" }}>
        {measuredCount} measured with <code>ratio_vs_sota</code> · {totalRows} catalog row
        {totalRows === 1 ? "" : "s"}
      </p>
    </div>
  );
}
