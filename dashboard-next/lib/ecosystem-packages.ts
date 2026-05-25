import { readFileSync } from "fs";
import path from "path";

export type EcosystemPackage = {
  id: string;
  repo: string;
  pillar_defaults: string[];
  csv_paths: string[];
  bench_required?: boolean;
  dispatch_event?: string;
};

const ECO_PATH = path.join(process.cwd(), "..", "ecosystem-packages.toml");

function parseStringArray(block: string, key: string): string[] {
  const re = new RegExp(`${key}\\s*=\\s*\\[([^\\]]*)\\]`, "s");
  const m = block.match(re);
  if (!m) return [];
  return [...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]);
}

function parseBool(block: string, key: string): boolean | undefined {
  const m = block.match(new RegExp(`${key}\\s*=\\s*(false|true)`));
  if (!m) return undefined;
  return m[1] === "true";
}

/**
 * Load ecosystem-packages.toml at build time (fixed [[package]] schema).
 */
export function loadEcosystemPackages(): EcosystemPackage[] {
  const text = readFileSync(ECO_PATH, "utf8");
  return text
    .split("[[package]]")
    .slice(1)
    .map((block) => {
      const id = block.match(/^id\s*=\s*"([^"]+)"/m)?.[1];
      const repo = block.match(/^repo\s*=\s*"([^"]+)"/m)?.[1];
      if (!id || !repo) return null;
      const pkg: EcosystemPackage = {
        id,
        repo,
        pillar_defaults: parseStringArray(block, "pillar_defaults"),
        csv_paths: parseStringArray(block, "csv_paths"),
      };
      const benchRequired = parseBool(block, "bench_required");
      if (benchRequired !== undefined) pkg.bench_required = benchRequired;
      const dispatch = block.match(/^dispatch_event\s*=\s*"([^"]+)"/m)?.[1];
      if (dispatch) pkg.dispatch_event = dispatch;
      return pkg;
    })
    .filter((p): p is EcosystemPackage => p !== null);
}

export function findPackage(
  packages: EcosystemPackage[],
  id: string,
): EcosystemPackage | undefined {
  return packages.find((p) => p.id === id);
}
