import { existsSync, readFileSync } from "fs";
import path from "path";

export type MatrixRow = {
  id: string;
  tier: number;
  repo: string;
  category: string;
  metric: string;
  status: string;
  ratio_vs_reference: number | null;
  ph_ids: string[];
  problem_size?: string | null;
  size_label?: string | null;
  base_id?: string | null;
};

export type BenchmarkMatrix = {
  generated_at: string;
  sections: Record<string, MatrixRow[]>;
  http_exploits?: {
    matrix?: Record<string, Record<string, string>>;
    status?: string;
  };
};

const MATRIX_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "benchmark-matrix.json",
);

export function loadBenchmarkMatrix(): BenchmarkMatrix | null {
  if (!existsSync(MATRIX_PATH)) return null;
  const raw = readFileSync(MATRIX_PATH, "utf8");
  return JSON.parse(raw) as BenchmarkMatrix;
}

export function flattenMatrixSections(matrix: BenchmarkMatrix): MatrixRow[] {
  return Object.values(matrix.sections).flat();
}
