import { existsSync, readFileSync } from "fs";
import path from "path";

export type ProofPostureRow = {
  id: string;
  status: string;
  phase: string;
};

export type ProofPosture = {
  generated_at: string;
  source: string;
  missing_source?: boolean;
  rows: ProofPostureRow[];
};

const POSTURE_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "proof-posture.json",
);

export function loadProofPosture(): ProofPosture | null {
  if (!existsSync(POSTURE_PATH)) return null;
  const raw = readFileSync(POSTURE_PATH, "utf8");
  const parsed = JSON.parse(raw) as ProofPosture;
  return {
    generated_at: parsed.generated_at ?? "",
    source: parsed.source ?? "",
    missing_source: parsed.missing_source,
    rows: parsed.rows ?? [],
  };
}

export function postureStatusClass(status: string): string {
  const key = status.toLowerCase();
  if (key === "done") return "green";
  if (key.startsWith("partial")) return "yellow";
  if (key === "missing" || key === "stub") return "red";
  return "unknown";
}
