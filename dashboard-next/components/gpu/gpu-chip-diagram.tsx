import type { GpuDiagram } from "@/lib/lig-gpu-matrix-types";
import { formatTimingSec } from "@/lib/lig-gpu-matrix-types";

type GpuChipDiagramProps = {
  diagram: GpuDiagram;
  chipLabel: string;
  emptyMessage?: string;
};

export function GpuChipDiagram({
  diagram,
  chipLabel,
  emptyMessage = "No timed workloads on this chip yet.",
}: GpuChipDiagramProps) {
  const series = diagram.series;
  const maxVal = series.length > 0 ? Math.max(...series.map((p) => p.value_sec)) : 1;

  return (
    <figure className="gpu-chip-diagram">
      <figcaption className="gpu-chip-diagram-caption">
        <strong>{chipLabel}</strong>
        <span className="mono">{diagram.title}</span>
      </figcaption>
      {series.length === 0 ? (
        <p className="mono gpu-chip-diagram-empty">{emptyMessage}</p>
      ) : (
        <ul className="gpu-chip-diagram-bars" role="img" aria-label={diagram.title}>
          {series.map((point) => {
            const widthPct = Math.min(100, (point.value_sec / maxVal) * 100);
            const valid = point.validity_gate_pass;
            return (
              <li key={point.workload_id} className="gpu-chip-bar-row">
                <span className="mono gpu-chip-bar-label" title={point.workload_id}>
                  {point.label}
                </span>
                <div className="gpu-chip-bar-track">
                  <div
                    className={`gpu-chip-bar-fill ${valid === false ? "gpu-chip-bar-invalid" : ""}`}
                    style={{ width: `${widthPct}%` }}
                  />
                </div>
                <span className="mono gpu-chip-bar-value">{formatTimingSec(point.value_sec)}</span>
                <span
                  className={`badge ${valid === true ? "badge-green" : valid === false ? "badge-red" : "badge-unknown"}`}
                >
                  {valid === true ? "valid" : valid === false ? "invalid" : "?"}
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </figure>
  );
}
