#!/usr/bin/env node
/** Print markdown summary of physics-codegen-matrix.json */
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT =
  process.env.BENCHMARKS_ROOT ||
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const jsonPath =
  process.env.PHYSICS_CODEGEN_RESULTS ||
  path.join(ROOT, "results", "physics-codegen-matrix.json");

const data = JSON.parse(readFileSync(jsonPath, "utf8"));
const rows = data.rows || [];

function groupBy(key) {
  const m = new Map();
  for (const r of rows) {
    const k = r[key];
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(r);
  }
  return m;
}

const passed = rows.filter((r) => r.validity?.verify_within_1ulp);
console.log("# Physics codegen matrix report\n");
console.log(`Generated: ${data.generated_at}`);
console.log(`Pilot: ${data.pilot}`);
console.log(`Token source: ${data.token_source || "unknown"}`);
console.log(`Rows: ${rows.length} (${passed.length} verify pass)\n`);

console.log("## Arm A — by model (Li only)\n");
console.log("| Model | Pass | Median thinking tokens |");
console.log("|-------|------|------------------------|");
for (const [model, rs] of groupBy("model")) {
  const armA = rs.filter((r) => r.arm === "A");
  if (!armA.length) continue;
  const ok = armA.filter((r) => r.validity?.verify_within_1ulp).length;
  const think = armA.map((r) => r.llm?.thinking_tokens || 0).sort((a, b) => a - b);
  const med = think[Math.floor(think.length / 2)] || 0;
  console.log(`| ${model} | ${ok}/${armA.length} | ${med} |`);
}

console.log("\n## Arm B — by language (fixed model)\n");
console.log(`Fixed model: ${data.model_arm_b || rows.find((r) => r.arm === "B")?.model}\n`);
console.log("| Lang | Pass | Median thinking tokens |");
console.log("|------|------|------------------------|");
for (const lang of ["cpp", "rust", "julia", "li"]) {
  const rs = rows.filter((r) => r.arm === "B" && r.lang === lang);
  if (!rs.length) continue;
  const ok = rs.filter((r) => r.validity?.verify_within_1ulp).length;
  const think = rs.map((r) => r.llm?.thinking_tokens || 0).sort((a, b) => a - b);
  const med = think[Math.floor(think.length / 2)] || 0;
  console.log(`| ${lang} | ${ok}/${rs.length} | ${med} |`);
}

const failed = rows.filter((r) => !r.validity?.verify_within_1ulp);
if (failed.length) {
  console.log("\n## Failures\n");
  for (const r of failed) {
    console.log(`- ${r.arm} ${r.model} ${r.bench_id} ${r.lang}`);
  }
}
