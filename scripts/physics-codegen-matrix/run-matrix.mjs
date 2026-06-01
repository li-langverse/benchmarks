#!/usr/bin/env node
/**
 * Physics codegen matrix — pilot orchestrator stub.
 * Full matrix: models × benches × langs. Records token_usage + verify results.
 *
 * Usage:
 *   PHYSICS_CODEGEN_PILOT=1 node run-matrix.mjs
 *   BENCHMARKS_ROOT=../.. LIC_ROOT=../../lic node run-matrix.mjs
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const BENCH_ROOT =
  process.env.BENCHMARKS_ROOT?.trim() ||
  (existsSync(join(__dir, "../..")) ? join(__dir, "../..") : join(__dir, "../../.."));

const PILOT_BENCHES = [
  "wave_equation_1d",
  "heat_equation_2d",
  "schrodinger_1d_barrier",
];

const PDE10 = [
  ...PILOT_BENCHES,
  "advection_diffusion_2d",
  "wave_equation_2d",
  "sph_dam_break_2d",
  "wind_field_bc",
  "combustion_passive",
  "fdtd_waveguide_2d",
  "euler_fluid_2d",
];

const MODELS = (process.env.PHYSICS_CODEGEN_MODELS || "default")
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);

const LANGS = ["cpp", "rust", "julia", "li"];
const pilot = process.env.PHYSICS_CODEGEN_PILOT === "1";
const benches = pilot ? PILOT_BENCHES : PDE10;

const outPath =
  process.env.PHYSICS_CODEGEN_RESULTS ||
  join(BENCH_ROOT, "results", "physics-codegen-matrix.json");

function stubRow(bench_id, model_id, lang) {
  return {
    bench_id,
    model_id,
    lang,
    llm: {
      duration_ms: 0,
      input_tokens: 0,
      output_tokens: 0,
      thinking_tokens: 0,
      thinking_tokens_estimated: true,
      tool_calls: 0,
    },
    validity: { compile_ok: false, verify_within_1ulp: false },
    runtime: { wall_time_s: null, median_of_3: null },
    note: "stub — implement SDK cells via goal-directed agent",
  };
}

const rows = [];
for (const model_id of MODELS) {
  for (const bench_id of benches) {
    const langs = pilot ? ["li"] : LANGS;
    const runLangArm = !pilot || model_id === MODELS[0];
    if (!runLangArm && pilot) continue;
    for (const lang of langs) {
      rows.push(stubRow(bench_id, model_id, lang));
    }
  }
}

mkdirSync(dirname(outPath), { recursive: true });
const payload = {
  generated_at: new Date().toISOString(),
  pilot,
  benches,
  models: MODELS,
  rows,
};
writeFileSync(outPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
console.log(`physics-codegen-matrix: wrote ${rows.length} stub rows → ${outPath}`);
console.log("Next: goal-directed agent replaces stubs with real SDK runs + verify.");
