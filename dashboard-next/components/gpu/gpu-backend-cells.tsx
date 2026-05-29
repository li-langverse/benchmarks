import type { GpuBackendCell } from "@/lib/lig-gpu-matrix-types";
import { formatTimingSec, validityLabel } from "@/lib/lig-gpu-matrix-types";

type GpuBackendBadgeProps = {
  cell?: GpuBackendCell;
};

export function GpuBackendBadge({ cell }: GpuBackendBadgeProps) {
  if (!cell?.status) {
    return <span className="badge badge-unknown">—</span>;
  }
  const s = cell.status;
  let cls = "badge-unknown";
  if (s.includes("timed") || s.includes("pilot") || s === "li_smoke_cpu_only") {
    cls = cell.validity_gate_pass === false ? "badge-yellow" : "badge-green";
  } else if (s.includes("blocked")) {
    cls = "badge-yellow";
  } else if (s === "stub") {
    cls = "badge-pending";
  }
  return (
    <span className={`badge ${cls}`} title={cell.reason ?? undefined}>
      {s.replace(/_/g, " ")}
    </span>
  );
}

type GpuTimingCellProps = {
  cell?: GpuBackendCell;
  mode: "cpu" | "gpu";
};

export function GpuTimingCell({ cell, mode }: GpuTimingCellProps) {
  if (!cell) {
    return <span className="mono gpu-timing-empty">—</span>;
  }
  const sec = mode === "cpu" ? cell.cpu_sec : cell.gpu_sec;
  if (sec == null) {
    return (
      <span className="mono gpu-timing-empty" title={cell.reason ?? cell.status ?? undefined}>
        N/A
      </span>
    );
  }
  return (
    <span className="mono gpu-timing-value" title={cell.note ?? undefined}>
      {formatTimingSec(sec)}
    </span>
  );
}

type GpuValidityCellProps = {
  cell?: GpuBackendCell;
};

export function GpuValidityCell({ cell }: GpuValidityCellProps) {
  const label = validityLabel(cell);
  const cls =
    label === "pass"
      ? "badge-green"
      : label === "fail"
        ? "badge-red"
        : label === "pending"
          ? "badge-yellow"
          : "badge-unknown";
  return <span className={`badge ${cls}`}>{label}</span>;
}
