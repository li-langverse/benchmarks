import Link from "next/link";
import { BenchmarkSearch } from "@/components/benchmark-search";
import { CatalogAuditStrip } from "@/components/overview/catalog-audit-strip";
import { IngestSourcesStrip } from "@/components/overview/ingest-sources-strip";
import { Tier1VerifyStrip } from "@/components/overview/tier1-verify-strip";
import { Badge } from "@/components/ui/badge";
import { getPillar, PILLAR_IDS } from "@/lib/pillars";
import {
  countStatusesByPillar,
  countValidityUnknownByPillar,
  packageFreshnessRows,
  regressionRows,
  topBenchmarksByStatus,
} from "@/lib/overview";
import {
  hasIndexedReleases,
  loadReleaseIndex,
} from "@/lib/release-index";
import { releaseFreshnessBanner } from "@/lib/release-freshness";
import { COVERAGE_GAP_DOC, coverageHonesty, splitTierCounts } from "@/lib/coverage";
import { loadSummary } from "@/lib/summary";
import { loadLigGpuMatrix } from "@/lib/lig-gpu-matrix";
import { tier1VerifyStats } from "@/lib/tier1-verify";
import { pillarPerfCounts } from "@/lib/validity";

const TIER_ORDER = ["0", "1", "2", "3", "5", "6"];

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
  const tierSplit = splitTierCounts(summary.rows);
  const honesty = coverageHonesty(summary.rows);
  const releaseIndex = loadReleaseIndex();
  const pillarCounts = countStatusesByPillar(summary.rows);
  const validityUnknownByPillar = countValidityUnknownByPillar(summary.rows);
  const reds = regressionRows(summary.rows);
  const osFilterValues = summary.reporting?.os_values?.filter((o) => o !== "unknown") ?? [];
  const freshness = packageFreshnessRows(releaseIndex, summary.generated_at);
  const releaseBanner = releaseFreshnessBanner(releaseIndex, summary.generated_at);
  const tier1Stats = tier1VerifyStats(summary.rows);
  let gpuMatrix: ReturnType<typeof loadLigGpuMatrix> | null = null;
  try {
    gpuMatrix = loadLigGpuMatrix();
  } catch {
    gpuMatrix = null;
  }

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

      {releaseBanner ? (
        <section
          className={`release-freshness-banner bento-full freshness-${releaseBanner.level}`}
          role="status"
          aria-label="Release index freshness"
        >
          <p>{releaseBanner.message}</p>
        </section>
      ) : null}

      <section className="coverage-honesty bento-full" aria-label="Coverage honesty">
        <p>
          <strong>
            {honesty.measured} of {honesty.total}
          </strong>{" "}
          catalog rows have wall-clock data in this ingest;{" "}
          <strong>{honesty.pending}</strong> are catalog placeholders until harness runs
          produce CSV.
        </p>
        {honesty.validityFail + honesty.validityUnknown > 0 ? (
          <p className="mono coverage-honesty-sub">
            Measured but not claimable: {honesty.validityFail} validity fail,{" "}
            {honesty.validityUnknown} validity unknown (see matrix validity column).
          </p>
        ) : null}
        <p className="honesty-links">
          <a href={COVERAGE_GAP_DOC} target="_blank" rel="noopener noreferrer">
            Coverage gap analysis
          </a>
        </p>
      </section>

      <section className="honesty-strip bento-full" aria-label="Measurement honesty">
        <p>
          <strong>Li never SOTA; green perf requires validity</strong> — tier-0 stability or
          harness <code>passed</code> before wall-clock green is claimable. Best-competitor
          charts pin the best competitor at 1.0; the table shows <code>li</code> when Li leads.
        </p>
        <p>
          Red or unknown perf when validity failed or is missing — even if wall time looks good.
        </p>
        {osFilterValues.length > 0 ? (
          <p className="mono">
            OS in this ingest:{" "}
            {osFilterValues.map((os, i) => (
              <span key={os}>
                {i > 0 ? ", " : ""}
                <Link href={`/matrix/?os=${os}`}>{os}</Link>
              </span>
            ))}
          </p>
        ) : null}
        <p className="honesty-variants">
          <span className="honesty-variants-label">Variants:</span>
          {VARIANT_LEGEND.map((v) => (
            <span key={v.variant} className="mono">
              <code>{v.variant}</code> — {v.label}
            </span>
          ))}
        </p>
        <p className="honesty-links">
          <a href="https://li-langverse.github.io/proof-library/">Proof library</a>
          {" · "}
          <Link href="/proofs/">Proofs ≠ bench</Link>
          {" · "}
          <a href={HONESTY_DOC_URL} target="_blank" rel="noopener noreferrer">
            Benchmark honesty policy
          </a>
        </p>
      </section>

      {gpuMatrix ? (
        <section className="gpu-donate-banner bento-full" aria-label="GPU chip matrix">
          <div>
            <strong>{String(gpuMatrix.summary.contribution_count)} donated chip(s)</strong>
            {Number(gpuMatrix.summary.open_slot_count) > 0 ? (
              <>
                {" "}
                · {String(gpuMatrix.summary.open_slot_count)} open slots (M1, RTX 3090, …)
              </>
            ) : null}
            {" "}
            — donate your hardware for the cross-vendor matrix.
          </div>
          <Link href="/gpu-matrix/">GPU matrix →</Link>
        </section>
      ) : null}

      <Tier1VerifyStrip stats={tier1Stats} />
      <CatalogAuditStrip />
      <IngestSourcesStrip summary={summary} />

      <section className="tier-strip bento-full" aria-label="Tier status counts">
        {TIER_ORDER.map((tier) => {
          const split = tierSplit[tier] ?? {
            measured: { green: 0, yellow: 0, red: 0, unknown: 0 },
            pending: 0,
          };
          const m = split.measured;
          const measuredTotal = m.green + m.yellow + m.red + m.unknown;
          return (
            <Link
              key={tier}
              href={`/matrix/?tier=${tier}`}
              className="tier-card"
              aria-label={`Tier ${tier}: ${measuredTotal} measured (${m.green} ok, ${m.yellow} warn, ${m.red} fail), ${split.pending} catalog pending`}
            >
              <h3>Tier {tier}</h3>
              <p className="tier-card-section-label">Measured</p>
              <div className="counts">
                <span className="g">{m.green} ok</span>
                <span className="y">{m.yellow} warn</span>
                <span className="r">{m.red} fail</span>
                {m.unknown > 0 ? <span className="u">{m.unknown} ?</span> : null}
              </div>
              {split.pending > 0 ? (
                <>
                  <p className="tier-card-section-label">Catalog pending</p>
                  <div className="counts">
                    <span className="p">{split.pending} pending</span>
                  </div>
                </>
              ) : null}
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
          {PILLAR_IDS.map((pillarId) => {
            const block = summary.pillars?.[pillarId];
            const counts = pillarCounts[pillarId] ?? {
              green: 0,
              yellow: 0,
              red: 0,
              unknown: 0,
            };
            const nav = getPillar(pillarId);
            const label = block?.label ?? nav?.label ?? pillarId;
            const chartCount = block?.charts.length ?? 0;
            const rowTotal =
              counts.green + counts.yellow + counts.red + counts.unknown;
            const redIds = topBenchmarksByStatus(summary.rows, pillarId, "red");
            const unknownIds = topBenchmarksByStatus(
              summary.rows,
              pillarId,
              "unknown",
            );
            const validityUnknown = validityUnknownByPillar[pillarId] ?? 0;
            const perf = pillarPerfCounts(summary.rows, pillarId);

            return (
              <article key={pillarId} className="pillar-card chart-card">
                <h3>
                  <Link href={`/pillar/${pillarId}/`}>{label}</Link>
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
                {rowTotal > 0 ? (
                  <div className="counts pillar-perf-counts" aria-label="Perf claimability">
                    <span className="g">{perf.claimable} claimable</span>
                    <span className="r">{perf.invalid} invalid</span>
                    <span className="u">{perf.unknown} unknown</span>
                    {perf.threshold > 0 ? (
                      <span className="y">{perf.threshold} over threshold</span>
                    ) : null}
                  </div>
                ) : null}
                {rowTotal === 0 ? (
                  <p className="pillar-card-meta mono">No catalog rows in this ingest</p>
                ) : null}
                {(redIds.length > 0 || unknownIds.length > 0) && (
                  <ul className="pillar-hotspots mono">
                    {redIds.map((id) => (
                      <li key={`r-${id}`}>
                        <Link href={`/bench/${id}/`}>{id}</Link>{" "}
                        <Badge status="red" />
                      </li>
                    ))}
                    {unknownIds.map((id) => (
                      <li key={`u-${id}`}>
                        <Link href={`/bench/${id}/`}>{id}</Link>{" "}
                        <Badge status="unknown" />
                      </li>
                    ))}
                  </ul>
                )}
                {validityUnknown > 0 ? (
                  <p className="pillar-card-meta mono pillar-validity-unknown">
                    {validityUnknown} row{validityUnknown === 1 ? "" : "s"} with unknown
                    validity
                  </p>
                ) : null}
                <p className="pillar-card-meta mono">
                  {chartCount} chart{chartCount === 1 ? "" : "s"} · {rowTotal} row
                  {rowTotal === 1 ? "" : "s"}
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
