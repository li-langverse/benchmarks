#!/usr/bin/env node
/**
 * Emit LI_AGENT_EXTRA_INSTRUCTION for the next incomplete physics-codegen cell.
 * Prevents undefined bench_id when the goal-directed loop runs without run-matrix-live.
 *
 * Usage:
 *   eval "$(node export-next-cell-instruction.mjs --export-env)"
 *   node export-next-cell-instruction.mjs --print-prompt
 */
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cellKey, iterateCells } from "./config.mjs";
import { buildCellPrompt } from "./prompt-cell.mjs";

const __dir = path.dirname(fileURLToPath(import.meta.url));
const BENCH_ROOT = process.env.BENCHMARKS_ROOT || path.resolve(__dir, "../..");
const OUT =
  process.env.PHYSICS_CODEGEN_RESULTS ||
  path.join(BENCH_ROOT, "results", "physics-codegen-matrix.json");

function loadDone() {
  if (!existsSync(OUT)) return new Set();
  const data = JSON.parse(readFileSync(OUT, "utf8"));
  const rows = data.rows || [];
  return new Set(
    rows
      .filter((r) => r.validity?.verify_within_1ulp && r.bench_id && r.lang)
      .map((r) => cellKey(r)),
  );
}

function pickNextCell() {
  const forced = process.env.PHYSICS_CODEGEN_CELL?.trim();
  if (forced) {
    const [arm, model, bench_id, lang] = forced.split("|");
    if (arm && model && bench_id && lang) {
      return { arm, model, bench_id, lang };
    }
  }
  const done = loadDone();
  const langFilter = process.env.PHYSICS_CODEGEN_LANG?.trim();
  const armFilter = process.env.PHYSICS_CODEGEN_ARM?.trim();
  for (const cell of iterateCells()) {
    if (!cell.bench_id) continue;
    if (langFilter && cell.lang !== langFilter) continue;
    if (armFilter && cell.arm !== armFilter) continue;
    if (!done.has(cellKey(cell))) return cell;
  }
  return null;
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\"'\"'`)}'`;
}

const cell = pickNextCell();
if (!cell) {
  console.error("physics-codegen: matrix complete — no pending cells");
  process.exit(2);
}

const prompt = buildCellPrompt(cell);
const exportEnv = process.argv.includes("--export-env");
const printPrompt = process.argv.includes("--print-prompt") || !exportEnv;

if (exportEnv) {
  console.log(`export LI_AGENT_EXTRA_INSTRUCTION=${shellQuote(prompt)}`);
  console.log(`export PHYSICS_CODEGEN_CELL=${shellQuote(cellKey(cell))}`);
  console.log("export LI_REPO_WORKFLOW_REPO=benchmarks");
  console.log(`export PHYSICS_CODEGEN_BENCH_ID=${shellQuote(cell.bench_id)}`);
}

if (printPrompt) {
  process.stdout.write(`${prompt}\n`);
}

process.stderr.write(
  `physics-codegen next cell: ${cell.arm} ${cell.model} ${cell.bench_id} ${cell.lang}\n`,
);
