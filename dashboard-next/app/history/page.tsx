import Link from "next/link";
import { loadHistoryIndex } from "@/lib/history";
import { loadSummary } from "@/lib/summary";

function formatDelta(d: {
  from?: number | string;
  to?: number | string;
  delta?: number;
}): string {
  const parts: string[] = [];
  if (d.from !== undefined) parts.push(String(d.from));
  if (d.to !== undefined) parts.push(`→ ${d.to}`);
  if (d.delta !== undefined) parts.push(`(Δ ${d.delta})`);
  return parts.join(" ") || "—";
}

export default function HistoryPage() {
  const index = loadHistoryIndex();
  if (!index) {
    return (
      <main>
        <section className="placeholder">
          <h2>History</h2>
          <p>
            No <span className="mono">data/history/index.json</span> at build time.
          </p>
          <p style={{ marginTop: "1.25rem" }}>
            <Link href="/">← Overview</Link>
          </p>
        </section>
      </main>
    );
  }

  const summary = loadSummary();
  const prov = (summary as { provenance?: Record<string, string> }).provenance;
  const summaryById = Object.fromEntries(summary.rows.map((r) => [r.benchmark, r]));

  return (
    <main>
      <section className="placeholder" style={{ marginBottom: "1.5rem" }}>
        <h2>History</h2>
        {index.updated_at ? (
          <p className="mono" style={{ marginTop: "0.75rem" }}>
            Updated: {index.updated_at}
          </p>
        ) : null}
        <p className="mono">{index.snapshots.length} snapshots</p>
        <p className="history-ulp-hint">
          Numeric context column shows current ingest ULPs — compare with Δ fields when
          history tracks <code>verify_ulps</code>.
        </p>
      </section>
      <section>
        <h3 className="section-heading">Latest deltas</h3>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Benchmark</th>
                <th>Field</th>
                <th>Change</th>
                <th>Current ULPs</th>
                <th>Improved</th>
              </tr>
            </thead>
            <tbody>
              {index.latest_deltas.map((d, i) => {
                const row = summaryById[d.benchmark];
                const ulps = row?.numeric_validity?.ulps;
                const within = row?.numeric_validity?.within_1ulp;
                return (
                  <tr key={`${d.benchmark}-${d.field}-${i}`}>
                    <td>
                      <Link href={`/bench/${d.benchmark}/`}>{d.benchmark}</Link>
                    </td>
                    <td className="mono">{d.field}</td>
                    <td className="mono">{formatDelta(d)}</td>
                    <td className="mono">
                      {ulps != null ? (
                        <>
                          {ulps}
                          {within === true ? " ≤1" : within === false ? " >1" : ""}
                        </>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td>
                      {d.improved === undefined ? "—" : d.improved ? "yes" : "no"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
      <p style={{ marginTop: "1.5rem" }}>
        <Link href="/">← Overview</Link>
      </p>
    </main>
  );
}
