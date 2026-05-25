import type { LangPoint } from "@/lib/summary";

type LangsTableProps = {
  series: LangPoint[];
  metric?: string;
};

export function LangsTable({ series, metric }: LangsTableProps) {
  if (series.length === 0) {
    return (
      <p className="mono" style={{ color: "var(--muted)", marginTop: "1rem" }}>
        No language series ingested yet.
      </p>
    );
  }

  return (
    <table className="data-table" style={{ marginTop: "1rem" }}>
      <caption className="sr-only">Language comparison</caption>
      <thead>
        <tr>
          <th scope="col">Lang</th>
          <th scope="col">Value</th>
          <th scope="col">Unit</th>
          <th scope="col">Variant</th>
        </tr>
      </thead>
      <tbody>
        {series.map((pt) => (
          <tr key={`${pt.lang}-${pt.variant ?? ""}`}>
            <td>
              <span className={`lang-chip lang-${pt.lang}`}>{pt.lang}</span>
            </td>
            <td className="mono">{pt.value}</td>
            <td className="mono">{pt.unit || "—"}</td>
            <td className="mono">{pt.variant ?? "—"}</td>
          </tr>
        ))}
      </tbody>
      {metric ? (
        <tfoot>
          <tr>
            <td colSpan={4} className="mono" style={{ color: "var(--muted)" }}>
              Metric: {metric}
            </td>
          </tr>
        </tfoot>
      ) : null}
    </table>
  );
}
