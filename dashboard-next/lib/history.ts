import { existsSync, readFileSync } from "fs";
import path from "path";

export type HistoryDelta = {
  benchmark: string;
  field: string;
  from?: number | string;
  to?: number | string;
  delta?: number;
  improved?: boolean;
};

export type HistoryIndex = {
  snapshots: { at: string; path: string }[];
  latest_deltas: HistoryDelta[];
  updated_at?: string;
};

const HISTORY_INDEX_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "history",
  "index.json",
);

export function loadHistoryIndex(): HistoryIndex | null {
  if (!existsSync(HISTORY_INDEX_PATH)) return null;
  const raw = readFileSync(HISTORY_INDEX_PATH, "utf8");
  return JSON.parse(raw) as HistoryIndex;
}

export function deltasForBenchmark(
  index: HistoryIndex | null,
  benchmarkId: string,
): HistoryDelta[] {
  if (!index) return [];
  return index.latest_deltas.filter((d) => d.benchmark === benchmarkId);
}
