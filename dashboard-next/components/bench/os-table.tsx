import type { LangPoint, SummaryRow } from "@/lib/summary";

type OsTableProps = {
  row: SummaryRow;
  series: LangPoint[];
};

function osForLang(series: LangPoint[], lang: string): string {
  const pt = series.find((s) => s.lang === lang);
  return pt?.os ?? "—";
}

export function OsTable({ row, series }: OsTableProps) {
  const rowOs = row.os ?? "unknown";
  const langs = series.length > 0 ? series : row.langs ?? [];

  return (
    <section aria-label="Host operating systems">
      <h3 style={{ fontSize: "1rem", marginTop: "1.5rem", color: "var(--text)" }}>
        Host OS
      </h3>
      <table className="data-table" style={{ marginTop: "0.5rem" }}>
        <caption className="sr-only">Measurement hosts by language</caption>
        <thead>
          <tr>
            <th scope="col">Scope</th>
            <th scope="col">OS</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Row aggregate</td>
            <td className="mono">{rowOs}</td>
          </tr>
          {langs.map((pt) => (
            <tr key={`${pt.lang}-${pt.variant ?? ""}`}>
              <td>
                <span className={`lang-chip lang-${pt.lang}`}>{pt.lang}</span>
                {pt.variant ? (
                  <span className="mono" style={{ color: "var(--muted)" }}>
                    {" "}
                    ({pt.variant})
                  </span>
                ) : null}
              </td>
              <td className="mono">{pt.os ?? osForLang(series, pt.lang)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {langs.length === 0 ? (
        <p className="mono" style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
          Per-language OS appears when CSV exports include an <code>os</code> column.
        </p>
      ) : null}
    </section>
  );
}
