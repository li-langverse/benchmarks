import Link from "next/link";
import { Suspense } from "react";
import { MatrixCatalogTable } from "@/components/matrix-catalog-table";
import { groupByBenchmark } from "@/lib/benchmark-groups";
import { COVERAGE_GAP_DOC, coverageHonesty } from "@/lib/coverage";
import { flattenMatrixSections, loadBenchmarkMatrix } from "@/lib/matrix";
import { buildSummaryById, loadSummary } from "@/lib/summary";

export default function MatrixPage() {
  const matrix = loadBenchmarkMatrix();
  if (!matrix) {
    return (
      <main>
        <section className="placeholder">
          <h2>Benchmark matrix</h2>
          <p>
            No <span className="mono">data/latest/benchmark-matrix.json</span> at
            build time.
          </p>
          <p style={{ marginTop: "1.25rem" }}>
            <Link href="/">← Overview</Link>
          </p>
        </section>
      </main>
    );
  }
  const rows = flattenMatrixSections(matrix);
  const summary = loadSummary();
  const honesty = coverageHonesty(summary.rows);
  const summaryById = buildSummaryById(summary.rows);
  const benchmarkGroups = groupByBenchmark(summary.rows);
  const groupsById = Object.fromEntries(
    benchmarkGroups.map((g) => [g.benchmark, g]),
  );
  const osValues =
    summary.reporting?.os_values?.filter((o) => o && o !== "unknown") ?? [];
  const exploitMatrix = matrix.http_exploits?.matrix;
  const exploitLangs = exploitMatrix
    ? [...new Set(Object.values(exploitMatrix).flatMap((r) => Object.keys(r)))].sort()
    : [];
  return (
    <main>
      <section className="placeholder" style={{ marginBottom: "1.5rem" }}>
        <h2>Benchmark matrix</h2>
        <p className="mono" style={{ marginTop: "0.75rem" }}>
          Generated: {matrix.generated_at}
        </p>
        <p className="coverage-honesty matrix-coverage-honesty">
          <strong>
            {honesty.measured} of {honesty.total}
          </strong>{" "}
          rows have wall-clock data; <strong>{honesty.pending}</strong> catalog pending until
          harness CSV.{" "}
          <a href={COVERAGE_GAP_DOC} target="_blank" rel="noopener noreferrer">
            Coverage gaps
          </a>
        </p>
        {osValues.length > 0 ? (
          <p className="mono" style={{ marginTop: "0.75rem" }}>
            OS in ingest: {osValues.join(", ")} — filter below or use{" "}
            <code>?os=linux</code> on this page.
          </p>
        ) : null}
      </section>
      <Suspense fallback={<p className="mono">Loading matrix…</p>}>
        <MatrixCatalogTable
          rows={rows}
          summaryById={summaryById}
          groupsById={groupsById}
        />
      </Suspense>
      {exploitMatrix && exploitLangs.length > 0 ? (
        <section style={{ marginTop: "2rem" }}>
          <h3 className="section-heading">HTTP exploit matrix</h3>
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Exploit</th>
                  {exploitLangs.map((lang) => (
                    <th key={lang}>{lang}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.entries(exploitMatrix).map(([exploit, cells]) => (
                  <tr key={exploit}>
                    <td className="mono">{exploit}</td>
                    {exploitLangs.map((lang) => (
                      <td key={lang}>{cells[lang] ?? "—"}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ) : null}
      <p style={{ marginTop: "1.5rem" }}>
        <Link href="/">← Overview</Link>
      </p>
    </main>
  );
}
