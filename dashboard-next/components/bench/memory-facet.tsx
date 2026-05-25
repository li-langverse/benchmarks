import type { SummaryRow } from "@/lib/summary";

export function MemoryFacet({ row }: { row: SummaryRow }) {
  return (
    <section className="facet-panel" aria-label="Memory facet">
      <h3 style={{ fontSize: "1rem", margin: "1.5rem 0 0.5rem" }}>④ Memory</h3>
      <p className="mono" style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
        Peak RSS not in ingest for <code>{row.benchmark}</code> — show — until lic exports{" "}
        <code>peak_rss_mb</code>.
      </p>
    </section>
  );
}
