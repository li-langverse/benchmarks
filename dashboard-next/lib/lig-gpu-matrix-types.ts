export type GpuBackendCell = {
  label: string;
  cpu_sec?: number | null;
  gpu_sec?: number | null;
  gpu_timing_ns?: number | string | null;
  status?: string | null;
  gpu_execution_status?: string | null;
  reason?: string | null;
  validity_gate_pass?: boolean | null;
  validity_ratio?: number | null;
  compile_ok?: boolean | null;
  note?: string | null;
};

export type GpuMatrixRow = {
  workload_kind: string;
  workload_id: string;
  label: string;
  backends: Record<string, GpuBackendCell>;
};

export type GpuChip = {
  chip_id: string;
  kind: "cpu" | "gpu";
  label: string;
  vendor?: string;
  model?: string;
  visible?: boolean;
  platform?: string;
  driver_version?: string;
  compute_capability?: string;
  memory_total_mib?: number;
  backend?: string;
};

export type GpuDiagramSeriesPoint = {
  workload_id: string;
  label: string;
  value_sec: number;
  validity_gate_pass?: boolean | null;
  status?: string | null;
};

export type GpuDiagram = {
  chip_id: string;
  title: string;
  backend: string;
  field: string;
  unit: string;
  series: GpuDiagramSeriesPoint[];
};

export type LigGpuMatrix = {
  schema: string;
  generated_at: string;
  sources: Record<string, string>;
  host_os?: string;
  gpu?: Record<string, unknown>;
  backends?: Array<Record<string, unknown>>;
  summary: Record<string, unknown>;
  possible_now?: Record<string, unknown>;
  funding_gaps?: Array<{ id: string; title: string; reason: string }>;
  honest_pilot?: {
    status?: string | null;
    gpu_timing_ns?: number | string | null;
    note?: string | null;
  };
  chips: GpuChip[];
  diagrams: Record<string, GpuDiagram>;
  rows: GpuMatrixRow[];
};

export function formatTimingSec(sec: number | null | undefined): string {
  if (sec == null || Number.isNaN(sec)) return "—";
  if (sec >= 1) return `${sec.toFixed(4)} s`;
  if (sec >= 1e-3) return `${(sec * 1e3).toFixed(3)} ms`;
  if (sec >= 1e-6) return `${(sec * 1e6).toFixed(2)} µs`;
  return `${(sec * 1e9).toFixed(1)} ns`;
}

export function validityLabel(cell: GpuBackendCell | undefined): string {
  if (!cell) return "—";
  if (cell.validity_gate_pass === true) return "pass";
  if (cell.validity_gate_pass === false) return "fail";
  if (cell.status?.includes("blocked") || cell.status === "stub") return "pending";
  return "unknown";
}

export function compareBackends(row: GpuMatrixRow): {
  cpu: GpuBackendCell | undefined;
  cuda: GpuBackendCell | undefined;
  vulkan: GpuBackendCell | undefined;
} {
  const b = row.backends;
  return {
    cpu: b.li_native,
    cuda: b.cuda,
    vulkan: b.vulkan,
  };
}
