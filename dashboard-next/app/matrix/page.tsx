import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { flattenMatrixSections, loadBenchmarkMatrix } from "@/lib/matrix";

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
      </section>
      <section>
        <h3 className="section-heading">Catalog sections</h3>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Tier</th>
                <th>Category</th>
                <th>Repo</th>
                <th>Metric</th>
                <th>Status</th>
                <th>Ratio</th>
                <th>PH ids</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={`${row.category}-${row.id}`}>
                  <td>
                    <Link href={`/bench/${row.id}/`}>{row.id}</Link>
                  </td>
                  <td>{row.tier}</td>
                  <td>{row.category}</td>
                  <td>{row.repo}</td>
                  <td>{row.metric}</td>
                  <td>
                    <Badge status={row.status} />
                  </td>
                  <td className="mono">
                    {row.ratio_vs_reference != null
                      ? row.ratio_vs_reference.toFixed(4)
                      : "—"}
                  </td>
                  <td className="mono">{row.ph_ids.join(", ") || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
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
