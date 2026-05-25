import { existsSync, readFileSync } from "fs";
import path from "path";

export type ReleaseArtifact = {
  path: string;
  kind: string;
};

export type ReleasePackageEntry = {
  version: string;
  git_sha: string;
  published_at: string;
  bench_required: boolean;
  artifacts: ReleaseArtifact[];
  manifest_source?: string;
  csv_refresh_needed?: boolean;
  notes?: string[];
};

export type ReleaseIndex = {
  updated_at: string;
  packages: Record<string, ReleasePackageEntry>;
};

const INDEX_PATH = path.join(
  process.cwd(),
  "..",
  "data",
  "latest",
  "release-index.json",
);

/**
 * Load release-index.json at build time from ../data/latest/release-index.json.
 * Returns an empty index when the file is missing (e.g. before first manifest ingest).
 */
export function loadReleaseIndex(): ReleaseIndex {
  if (!existsSync(INDEX_PATH)) {
    return { updated_at: "", packages: {} };
  }
  const raw = readFileSync(INDEX_PATH, "utf8");
  const parsed = JSON.parse(raw) as ReleaseIndex;
  return {
    updated_at: parsed.updated_at ?? "",
    packages: parsed.packages ?? {},
  };
}

export function hasIndexedReleases(index: ReleaseIndex): boolean {
  return Object.keys(index.packages).length > 0;
}
