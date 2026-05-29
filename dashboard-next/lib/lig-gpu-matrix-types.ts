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

export type GpuDiagramSeriesPoint = {
  workload_id: string;
  label: string;
  value_sec: number;
  validity_gate_pass?: boolean | null;
  status?: string | null;
};

export type GpuDiagram = {
  title: string;
  backend: string;
  field: string;
  unit: string;
  series: GpuDiagramSeriesPoint[];
};

export type GpuChipContribution = {
  chip_slug: string;
  label: string;
  vendor?: string;
  host_os?: string;
  primary_backend: string;
  contributor?: Record<string, unknown>;
  submitted_at?: string;
  notes?: string;
  hardware?: Record<string, unknown>;
  sources?: Record<string, string>;
  summary: Record<string, unknown>;
  honest_pilot?: {
    status?: string | null;
    gpu_timing_ns?: number | string | null;
    note?: string | null;
  };
  diagrams: Record<string, GpuDiagram>;
  rows: GpuMatrixRow[];
  funding_gaps?: Array<{ id: string; title: string; reason: string }>;
};

export type GpuOpenSlot = {
  chip_slug: string;
  label: string;
  vendor: string;
  host_os: string;
  primary_backend: string;
  status: string;
};

export type CrossChipRow = {
  workload_id: string;
  label: string;
  workload_kind?: string;
  chips: Record<
    string,
    {
      gpu_sec?: number | null;
      cpu_sec?: number | null;
      validity_gate_pass?: boolean | null;
      backend?: string;
      status?: string | null;
    }
  >;
};

export type LigGpuMatrixV2 = {
  schema: string;
  generated_at: string;
  contribution_policy_url?: string;
  summary: Record<string, unknown>;
  contributions: GpuChipContribution[];
  open_slots: GpuOpenSlot[];
  cross_chip: CrossChipRow[];
};

/** @deprecated v1 single-host shape — normalized to v2 in loader */
export type LigGpuMatrixV1 = {
  schema: string;
  generated_at: string;
  rows: GpuMatrixRow[];
  chips?: unknown[];
  diagrams?: Record<string, GpuDiagram>;
  summary: Record<string, unknown>;
  honest_pilot?: GpuChipContribution["honest_pilot"];
  funding_gaps?: GpuChipContribution["funding_gaps"];
  gpu?: Record<string, unknown>;
  host_os?: string;
};

export type LigGpuMatrix = LigGpuMatrixV2;

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
  primary: GpuBackendCell | undefined;
} {
  const b = row.backends;
  const primaryKey = b.metal ? "metal" : b.hip ? "hip" : b.cuda ? "cuda" : "cuda";
  return {
    cpu: b.li_native,
    cuda: b.cuda,
    vulkan: b.vulkan,
    primary: b[primaryKey],
  };
}

export function vendorBadgeClass(vendor?: string): string {
  switch (vendor) {
    case "nvidia":
      return "gpu-vendor-nvidia";
    case "apple":
      return "gpu-vendor-apple";
    case "amd":
      return "gpu-vendor-amd";
    default:
      return "gpu-vendor-other";
  }
}

export function backendLabel(backend: string): string {
  const map: Record<string, string> = {
    cuda: "CUDA",
    metal: "Metal",
    hip: "HIP",
    vulkan: "Vulkan",
    li_native: "CPU",
  };
  return map[backend] ?? backend;
}
