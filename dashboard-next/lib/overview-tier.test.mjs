import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const summary = JSON.parse(readFileSync(join(root, "data/latest/summary.json"), "utf8"));
function isCatalogPending(row) {
  if (row.pending === true) return true;
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
function rowCoverageKind(row) {
  if (isCatalogPending(row)) return "pending";
  if (!hasWallClock(row)) return "pending";
  if (row.validity_status === "fail") return "validity_fail";
  if (row.validity_status !== "pass") return "validity_unknown";
  return "measured";
}
function splitTierCounts(rows) {
  const out = {};
  for (const row of rows) {
    const tier = String(row.tier);
    if (!out[tier]) out[tier] = { measured: { green: 0, yellow: 0, red: 0, unknown: 0 }, pending: 0 };
    if (isCatalogPending(row) || !hasWallClock(row)) { out[tier].pending += 1; continue; }
    const st = row.status;
    if (st === "green" || st === "yellow" || st === "red") out[tier].measured[st] += 1;
    else out[tier].measured.unknown += 1;
  }
  return out;
}
let failed = 0;
const split = splitTierCounts(summary.rows);
for (const tier of ["0","1","2","3","5","6"]) {
  const ingest = summary.tier_counts[tier] ?? { green: 0, yellow: 0, red: 0, unknown: 0 };
  const s = split[tier] ?? { measured: { green: 0, yellow: 0, red: 0, unknown: 0 }, pending: 0 };
  const colored = s.measured.green + s.measured.yellow + s.measured.red;
  const ingestColored = ingest.green + ingest.yellow + ingest.red;
  if (colored !== ingestColored) failed++;
  if (s.pending !== ingest.unknown) failed++;
}
if (summary.rows.some((r) => r.status === "unknown" && rowCoverageKind(r) === "measured")) failed++;
console.log(failed === 0 ? "overview-tier.test: OK" : "FAILED");
process.exit(failed === 0 ? 0 : 1);
