import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const summary = JSON.parse(readFileSync(join(root, "data/latest/summary.json"), "utf8"));

function isPlatformSkip(row) {
  return row.status === "skip" || row.validity_status === "skip";
}
function isCatalogPending(row) {
  if (row.pending === true) return true;
  if (isPlatformSkip(row)) return true;
  if (row.status !== "unknown") return false;
  if (row.li_value != null || row.cpp_value != null) return false;
  if (row.path === "unknown" || row.benchmark.endsWith("_stub")) return true;
  if (row.base_id) return true;
  if (row.size_label === "harness pending") return true;
  return false;
}
function hasWallClock(row) {
  if (row.status === "green" || row.status === "yellow" || row.status === "red") return true;
  return row.li_value != null || row.cpp_value != null;
}
function pickPrimaryRow(variants) {
  const order = ["linux", "darwin", "macos", "windows"];
  const measured = variants.filter((r) => hasWallClock(r));
  if (measured.length) {
    for (const os of order) {
      const hit = measured.find((r) => r.os === os);
      if (hit) return hit;
    }
    return measured[0];
  }
  for (const os of order) {
    const hit = variants.find((r) => r.os === os);
    if (hit) return hit;
  }
  return variants[0];
}
function groupByBenchmark(rows) {
  const map = new Map();
  for (const row of rows) {
    const list = map.get(row.benchmark) ?? [];
    list.push(row);
    map.set(row.benchmark, list);
  }
  return [...map.entries()].map(([benchmark, variants]) => ({
    benchmark,
    variants,
    primary: pickPrimaryRow(variants),
  }));
}
function splitTierCounts(rows) {
  const out = {};
  for (const group of groupByBenchmark(rows)) {
    const row = group.primary;
    const tier = String(row.tier);
    if (!out[tier]) out[tier] = { measured: { green: 0, yellow: 0, red: 0, unknown: 0 }, pending: 0 };
    if (isCatalogPending(row) && !hasWallClock(row)) {
      out[tier].pending += 1;
      continue;
    }
    const st = row.status;
    if (st === "green" || st === "yellow" || st === "red") out[tier].measured[st] += 1;
    else if (hasWallClock(row)) out[tier].measured.unknown += 1;
    else out[tier].pending += 1;
  }
  return out;
}
let failed = 0;
const split = splitTierCounts(summary.rows);
for (const tier of ["0", "1", "2", "3", "5", "6"]) {
  const ingest = summary.tier_counts[tier] ?? { green: 0, yellow: 0, red: 0, unknown: 0 };
  const s = split[tier] ?? { measured: { green: 0, yellow: 0, red: 0, unknown: 0 }, pending: 0 };
  const colored = s.measured.green + s.measured.yellow + s.measured.red;
  const ingestColored = ingest.green + ingest.yellow + ingest.red;
  if (colored !== ingestColored) failed++;
  const unattributed = s.pending + s.measured.unknown;
  if (unattributed !== ingest.unknown) failed++;
}
console.log(failed === 0 ? "overview-tier.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
