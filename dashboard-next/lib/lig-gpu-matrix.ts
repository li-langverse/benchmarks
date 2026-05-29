import { readFileSync } from "fs";
import path from "path";
import type { LigGpuMatrix } from "@/lib/lig-gpu-matrix-types";

const MATRIX_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "lig-gpu-matrix.json",
);

export const LIG_GPU_MATRIX_PUBLIC_URL = "/benchmarks/latest/lig-gpu-matrix.json";

export function loadLigGpuMatrix(): LigGpuMatrix {
  const raw = readFileSync(MATRIX_PATH, "utf8");
  return JSON.parse(raw) as LigGpuMatrix;
}

export type {
  GpuBackendCell,
  GpuChip,
  GpuDiagram,
  GpuDiagramSeriesPoint,
  GpuMatrixRow,
  LigGpuMatrix,
} from "@/lib/lig-gpu-matrix-types";

export {
  compareBackends,
  formatTimingSec,
  validityLabel,
} from "@/lib/lig-gpu-matrix-types";
