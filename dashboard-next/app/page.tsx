import Link from "next/link";
import { BenchmarkSearch } from "@/components/benchmark-search";
import { Badge } from "@/components/ui/badge";
import { getPillar } from "@/lib/pillars";
import {
  countStatusesByPillar,
  packageFreshnessRows,
  regressionRows,
  topBenchmarksByStatus,
} from "@/lib/overview";
import { hasIndexedReleases, loadReleaseIndex } from "@/lib/release-index";
import { loadSummary } from "@/lib/summary";

const TIER_ORDER = ["0", "1", "2", "3", "5"];

const HONESTY_DOC_URL =
  "https://github.com/li-langverse/benchmarks/blob/main/docs/honesty/benchmark-dashboard.md";

const VARIANT_LEGEND: { variant: string; label: string }[] = [
  { variant: "default", label: "Li vs C++ shared problem size" },
  { variant: "shared_c_kernel", label: "May share C kernel — not pure-Li proof" },
  { variant: "pure_li", label: "Li-only codegen (PH-7e); red is compiler work" },
  { variant: "async_stub", label: "Tooling smoke — not HPC competitive" },
];

export default function HomePage() {
  const summary = loadSummary();
  const releaseIndex = loadReleaseIndex();
  const pillarCounts = countStatusesByPillar(summary.rows);
  const reds = regressionRows(summary.rows);
  const freshness = packageFreshnessRows(releaseIndex, summary.generated_at);
  const pillarIds = Object.keys(summary.pillars ?? {}).sort();

  return (
    <main className="bento">
      <p className="ingest-meta mono" aria-live="polite">
        Ingest: {summary.generated_at}
        {releaseIndex.updated_at ? (
          <>
            {" "}
            · releases indexed {releaseIndex.updated_at}
          </>
        ) : null}
      </p>

      <section className="honesty-strip bento-full" aria-label="Measurement honesty">
        <p>
          <strong>Green rows are wall-clock ratios vs catalog reference</strong> — not formal
          proof or correctness certificates.
        </p>
        <p className="honesty-variants">
          <span className="honesty-variants-label">Variants:</span>
          {VARIANT_LEGEND.map((v) => (
            <span key={v.variant} className="mono">
              <code>{v.variant}</code> — {v.label}
            </span>
          ))}
        </p>
        <p className="honesty-links">
          <Link href="/proofs/">Proof coverage map</Link>
          {" · "}
          <a href={HONESTY_DOC_URL} target="_blank" rel="noopener noreferrer">
            Benchmark honesty policy
          </a>
        </p>
      </section>

      <section className="tier-strip bento-full" aria-label="Tier status counts">
        {TIER_ORDER.map((tier) => {
          const c = summary.tier_counts[tier] ?? {
            green: 0,
            yellow: 0,
            red: 0,
            unknown: 0,
          };
          return (
            <Link
              key={tier}
              href={`/matrix/?tier=${tier}`}
              className="tier-card"
              aria-label={`Tier ${tier}: ${c.green} ok, ${c.yellow} warn, ${c.red} fail, ${c.unknown} unknown`}
            >
              <h3>Tier {tier}</h3>
              <div className="counts">
                <span className="g">{c.green} ok</span>
                <span className="y">{c.yellow} warn</span>
                <span className="r">{c.red} fail</span>
                <span className="u">{c.unknown} ?</span>
              </div>
            </Link>
          );
        })}
      </section>

      <section
        className={`regression-banner bento-regression ${reds.length === 0 ? "regression-empty" : ""}`}
        role="alert"
        aria-label="Regressions"
      >
        <h2>Regressions</h2>
        {reds.length === 0 ? (
          <p className="regression-none">No failing (red) benchmarks in this ingest.</p>
        ) : (
          <>
            <p>
              <strong>{reds.length}</strong> benchmark{reds.length === 1 ? "" : "s"} above{" "}
              <span className="mono">threshold_ratio_cpp</span>:
            </p>
            <ul className="regression-list">
              {reds.map((row) => (
                <li key={row.benchmark}>
                  <Link href={`/bench/${row.benchmark}/`}>{row.benchmark}</Link>
                  {row.ratio_vs_cpp != null ? (
                    <span className="mono regression-ratio">
                      {" "}
                      {row.ratio_vs_cpp.toFixed(2)}×
                    </span>
                  ) : null}
                  <Badge status={row.status} />
                </li>
              ))}
            </ul>
          </>
        )}
      </section>

      <section className="package-freshness bento-freshness" aria-label="Package freshness">
        <h2>Package freshness</h2>
        {!hasIndexedReleases(releaseIndex) ? (
          <p className="freshness-empty" role="status">
            No releases indexed
          </p>
        ) : (
          <ul className="freshness-list">
            {freshness.map((pkg) => (
              <li key={pkg.id} className={`freshness-row freshness-${pkg.level}`}>
                <Link href={`/packages/${pkg.id}/`} className="freshness-id">
                  {pkg.id}
                </Link>
                {pkg.version ? (
                  <span className="mono freshness-version">{pkg.version}</span>
                ) : (
                  <span className="freshness-missing">not indexed</span>
                )}
                {pkg.published_at ? (
                  <span className="mono freshness-date">{pkg.published_at}</span>
                ) : null}
                {pkg.ageDays != null ? (
                  <span className="freshness-age">{pkg.ageDays}d before ingest</span>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="pillar-bento bento-full" aria-label="Pillar summaries">
        <h2 className="bento-section-title">Pillars</h2>
        <div className="pillar-grid">
          {pillarIds.map((pillarId) => {
            const block = summary.pillars![pillarId];
            const counts = pillarCounts[pillarId] ?? {
              green: 0,
              yellow: 0,
              red: 0,
              unknown: 0,
            };
            const nav = getPillar(pillarId);
            const redIds = topBenchmarksByStatus(summary.rows, pillarId, "red");
            const unknownIds = topBenchmarksByStatus(summary.rows, pillarId, "unknown");

            return (
              <article key={pillarId} className="pillar-card chart-card">
                <h3>
                  <Link href={`/pillar/${pillarId}/`}>{block.label}</Link>
                </h3>
                {nav ? (
                  <p className="pillar-card-desc">{nav.description}</p>
                ) : null}
                <div className="counts pillar-counts">
                  <span className="g">{counts.green} ok</span>
                  <span className="y">{counts.yellow} warn</span>
                  <span className="r">{counts.red} fail</span>
                  <span className="u">{counts.unknown} ?</span>
                </div>
                {(redIds.length > 0 || unknownIds.length > 0) && (
                  <ul className="pillar-hotspots mono">
                    {redIds.map((id) => (
                      <li key={`r-${id}`}>
                        <Link href={`/bench/${id}/`}>{id}</Link> <Badge status="red" />
                      </li>
                    ))}
                    {unknownIds.map((id) => (
                      <li key={`u-${id}`}>
                        <Link href={`/bench/${id}/`}>{id}</Link> <Badge status="unknown" />
                      </li>
                    ))}
                  </ul>
                )}
                <p className="pillar-card-meta mono">
                  {block.charts.length} chart{block.charts.length === 1 ? "" : "s"} in ingest
                </p>
              </article>
            );
          })}
        </div>
      </section>

      <BenchmarkSearch rows={summary.rows} />
    </main>
  );
}
