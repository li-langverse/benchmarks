import Link from "next/link";
import {
  FACET_ORDER,
  facetCellsFromSummaryRow,
  type FacetId,
} from "@/components/bench/algorithm-facet-grid";
import { Badge } from "@/components/ui/badge";
import type { SummaryRow } from "@/lib/summary";

const FACET_LABELS: Record<FacetId, string> = {
  validity: "Validity",
  perf: "Perf vs SOTA",
  os: "OS",
  memory: "Memory",
  security: "Security",
};

export function FacetMatrixSnippet({ row }: { row: SummaryRow }) {
  const cells = facetCellsFromSummaryRow(row);

  return (
    <section className="facet-matrix-snippet" aria-label="Algorithm facet matrix snippet" style={{ marginTop: "1.25rem" }}>
      <h3 style={{ fontSize: "1rem", margin: "0 0 0.5rem", color: "var(--text)" }}>
        Facet matrix (this algorithm)
      </h3>
      <p className="mono" style={{ fontSize: "0.85rem", color: "var(--muted)", marginBottom: "0.75rem" }}>
        Five facet columns from <Link href="/matrix/">/matrix</Link> for this row.
      </p>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${FACET_ORDER.length}, minmax(0, 1fr))`,
          gap: "0.5rem",
          fontSize: "0.85rem",
        }}
      >
        {FACET_ORDER.map((facet) => {
          const cell = cells[facet];
          const tone = cell.claimable || cell.tone === "neutral" ? cell.tone : "unknown";
          return (
            <article
              key={facet}
              style={{
                border: "1px solid var(--border)",
                borderRadius: "6px",
                padding: "0.5rem 0.65rem",
                opacity: facet === "perf" && !cell.claimable ? 0.75 : 1,
              }}
            >
              <header className="mono" style={{ color: "var(--muted)", marginBottom: "0.35rem" }}>
                {FACET_LABELS[facet]}
              </header>
              <p style={{ margin: 0 }}>
                {facet === "validity" || facet === "perf" || facet === "security" ? (
                  <Badge status={tone === "neutral" ? "unknown" : tone}>{cell.label}</Badge>
                ) : (
                  <span className="mono">{cell.label}</span>
                )}
              </p>
              {cell.detail ? (
                <p className="mono" style={{ margin: "0.35rem 0 0", color: "var(--muted)", fontSize: "0.8rem" }}>
                  {cell.detail}
                </p>
              ) : null}
            </article>
          );
        })}
      </div>
    </section>
  );
}
