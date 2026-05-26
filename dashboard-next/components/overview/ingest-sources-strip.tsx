import type { Summary } from "@/lib/summary";

const VERIFY_CSV_DOC =
  "https://github.com/li-langverse/lic/blob/main/benchmarks/results/README.md";

type IngestSourcesStripProps = {
  summary: Summary;
};

export function IngestSourcesStrip({ summary }: IngestSourcesStripProps) {
  const entries = Object.entries(summary.sources ?? {});
  if (entries.length === 0) return null;

  return (
    <section
      className="ingest-sources-strip bento-full"
      aria-labelledby="ingest-sources-heading"
    >
      <h2 id="ingest-sources-heading" className="bento-section-title">
        Ingest sources
      </h2>
      <ul className="ingest-sources-list mono">
        {entries.map(([key, path]) => (
          <li key={key}>
            <span className="ingest-sources-key">{key}</span>
            <span className="ingest-sources-path">{path}</span>
          </li>
        ))}
      </ul>
      <p className="ingest-sources-hint">
        Re-run tier-1 with <code>--verify</code> in{" "}
        <code>lic</code> to populate <code>verify_ulps</code> columns.{" "}
        <a href={VERIFY_CSV_DOC} target="_blank" rel="noopener noreferrer">
          CSV column reference
        </a>
      </p>
    </section>
  );
}
