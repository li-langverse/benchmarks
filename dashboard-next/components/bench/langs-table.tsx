import type { LangPoint } from "@/lib/summary";
import { formatMeanStd } from "@/lib/format-measurement";

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
          <th scope="col">Mean ± σ</th>
          <th scope="col">Runs</th>
          <th scope="col">Unit</th>
          <th scope="col">Variant</th>
          <th scope="col">OS</th>
        </tr>
      </thead>
      <tbody>
        {series.map((pt) => (
          <tr key={`${pt.lang}-${pt.variant ?? ""}`}>
            <td>
              <span className={`lang-chip lang-${pt.lang}`}>{pt.lang}</span>
            </td>
            <td className="mono">
              {formatMeanStd(pt.value, pt.stddev, null, null)}
            </td>
            <td className="mono">{pt.sample_runs ?? "—"}</td>
            <td className="mono">{pt.unit || "—"}</td>
            <td className="mono">{pt.variant ?? "—"}</td>
            <td className="mono">{pt.os ?? "—"}</td>
          </tr>
        ))}
      </tbody>
      {metric ? (
        <tfoot>
          <tr>
            <td colSpan={6} className="mono" style={{ color: "var(--muted)" }}>
              Metric: {metric} (value = mean of timed runs)
            </td>
          </tr>
        </tfoot>
      ) : null}
    </table>
  );
}
