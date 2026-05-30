import { readFileSync } from "fs";
import path from "path";
import type {
  GpuChipContribution,
  LigGpuMatrix,
  LigGpuMatrixV1,
  LigGpuMatrixV2,
} from "@/lib/lig-gpu-matrix-types";

const MATRIX_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "lig-gpu-matrix.json",
);

export const LIG_GPU_MATRIX_PUBLIC_URL = "/benchmarks/latest/lig-gpu-matrix.json";

function normalizeV1(raw: LigGpuMatrixV1): LigGpuMatrixV2 {
  const gpuName = (raw.gpu as { name?: string } | undefined)?.name ?? "Lab GPU";
  const contribution: GpuChipContribution = {
    chip_slug: "legacy-lab",
    label: gpuName,
    vendor: "nvidia",
    host_os: raw.host_os,
    primary_backend: "cuda",
    summary: raw.summary,
    honest_pilot: raw.honest_pilot,
    funding_gaps: raw.funding_gaps,
    diagrams: raw.diagrams ?? {},
    rows: raw.rows,
  };
  return {
    schema: "benchmarks/lig-gpu-matrix/v2",
    generated_at: raw.generated_at,
    summary: {
      contribution_count: 1,
      open_slot_count: 0,
      ...raw.summary,
    },
    contributions: [contribution],
    open_slots: [],
    cross_chip: [],
  };
}

export function loadLigGpuMatrix(): LigGpuMatrix {
  const raw = JSON.parse(readFileSync(MATRIX_PATH, "utf8")) as LigGpuMatrixV2 | LigGpuMatrixV1;
  if (raw.schema === "benchmarks/lig-gpu-matrix/v2") {
    return raw as LigGpuMatrixV2;
  }
  return normalizeV1(raw as LigGpuMatrixV1);
}

export function getContribution(matrix: LigGpuMatrix, slug: string): GpuChipContribution | undefined {
  return matrix.contributions.find((c) => c.chip_slug === slug);
}

export type {
  CrossChipRow,
  GpuBackendCell,
  GpuChipContribution,
  GpuDiagram,
  GpuDiagramSeriesPoint,
  GpuMatrixRow,
  GpuOpenSlot,
  LigGpuMatrix,
} from "@/lib/lig-gpu-matrix-types";

export {
  backendLabel,
  compareBackends,
  formatTimingSec,
  validityLabel,
  vendorBadgeClass,
} from "@/lib/lig-gpu-matrix-types";
