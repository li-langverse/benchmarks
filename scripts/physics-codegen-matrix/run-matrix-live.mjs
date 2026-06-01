#!/usr/bin/env node
/**
 * Live SDK matrix: one code_implementer run per cell with real token_usage.
 *
 * Env:
 *   LI_CURSOR_AGENTS_ROOT  (default /app on K8s)
 *   LIC_ROOT               (default /workspace/lic)
 *   BENCHMARKS_ROOT        (default …/benchmarks)
 *   PHYSICS_CODEGEN_PILOT=1|0
 *   PHYSICS_CODEGEN_RESUME=1   skip cells already in results JSON
 *   PHYSICS_CODEGEN_MAX=N      cap cells this invocation
 *   LI_SKIP_IMPLEMENTER_PREFLIGHT_GATE=1
 */
import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import path from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import {
  benches,
  cellKey,
  expectedRowCount,
  iterateCells,
  pilotMode,
  sdkModelId,
} from "./config.mjs";
import { buildCellPrompt } from "./prompt-cell.mjs";
import { verifyBench } from "./verify-cell.mjs";

const __dir = path.dirname(fileURLToPath(import.meta.url));
const BENCH_ROOT = process.env.BENCHMARKS_ROOT || path.resolve(__dir, "../..");
const LIC_ROOT = process.env.LIC_ROOT || "/workspace/lic";
const AGENTS_ROOT =
  process.env.LI_CURSOR_AGENTS_ROOT ||
  path.resolve(BENCH_ROOT, "../li-cursor-agents");
const OUT =
  process.env.PHYSICS_CODEGEN_RESULTS ||
  path.join(BENCH_ROOT, "results", "physics-codegen-matrix.json");

const maxCells = Number(process.env.PHYSICS_CODEGEN_MAX || "0") || Infinity;
const resume = process.env.PHYSICS_CODEGEN_RESUME !== "0";

function loadAgents() {
  const dist = path.join(AGENTS_ROOT, "dist");
  if (!existsSync(path.join(dist, "runner.js"))) {
    throw new Error(`missing ${dist}/runner.js — npm run build in li-cursor-agents`);
  }
  return import(pathToFileURL(path.join(dist, "runner.js"))).then(async (runner) => {
    const env = await import(pathToFileURL(path.join(dist, "env.js")));
    env.loadRuntimeEnv();
    return { runAgent: runner.runAgent };
  });
}

function loadExisting() {
  if (!resume || !existsSync(OUT)) return { rows: [], done: new Set() };
  const data = JSON.parse(readFileSync(OUT, "utf8"));
  const rows = data.rows || [];
  const done = new Set(
    rows
      .filter((r) => r.llm?.token_source === "sdk" && r.validity?.verify_within_1ulp)
      .map((r) => cellKey(r)),
  );
  return { rows: rows.filter((r) => r.llm?.token_source === "sdk"), done, meta: data };
}

function llmFromResult(result, modelLabel) {
  const u = result.trace?.token_usage;
  const durationMs = result.durationMs ?? 0;
  if (u) {
    return {
      duration_ms: durationMs,
      input_tokens: u.input_tokens,
      output_tokens: u.output_tokens,
      thinking_tokens: u.thinking_tokens,
      thinking_chars: u.thinking_chars,
      thinking_tokens_estimated: u.thinking_tokens_estimated,
      tool_calls: result.trace?.tool_call_count ?? 0,
      token_source: "sdk",
      model_label: modelLabel,
      sdk_model: sdkModelId(modelLabel),
      status: result.status,
    };
  }
  const thinkLen = result.trace?.thinking_text?.length ?? 0;
  return {
    duration_ms: durationMs,
    input_tokens: 0,
    output_tokens: 0,
    thinking_tokens: Math.ceil(thinkLen / 4),
    thinking_chars: thinkLen,
    thinking_tokens_estimated: true,
    tool_calls: result.trace?.tool_call_count ?? 0,
    token_source: "sdk-estimated",
    model_label: modelLabel,
    sdk_model: sdkModelId(modelLabel),
    status: result.status,
  };
}

function writePayload(rows) {
  const payload = {
    generated_at: new Date().toISOString(),
    pilot: pilotMode(),
    token_source: "sdk",
    benches: benches(),
    rows,
  };
  mkdirSync(path.dirname(OUT), { recursive: true });
  writeFileSync(OUT, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function runCell(runAgent, cell) {
  const prompt = buildCellPrompt(cell);
  const sdkModel = sdkModelId(cell.model);
  process.stderr.write(
    `\n=== LIVE ${cell.arm} ${cell.model} (${sdkModel}) ${cell.bench_id} ${cell.lang} ===\n`,
  );

  process.env.LI_SKIP_IMPLEMENTER_PREFLIGHT_GATE =
    process.env.LI_SKIP_IMPLEMENTER_PREFLIGHT_GATE || "1";
  process.env.LI_SDK_LOG_SKIP_TOKEN_DELTAS = "0";

  const result = await runAgent({
    agentId: "code_implementer",
    cwd: LIC_ROOT,
    benchmarksRoot: BENCH_ROOT,
    mock: false,
    dryRun: false,
    modelId: sdkModel,
    extraInstruction: prompt,
    workflowRepo: "benchmarks",
  });

  const validity = verifyBench(cell.bench_id, {
    requireNativeLang: process.env.PHYSICS_CODEGEN_REQUIRE_NATIVE === "1",
  });

  return {
    ...cell,
    validity: {
      verify_within_1ulp: validity.verify_within_1ulp,
      checksum: validity.checksum,
    },
    llm: llmFromResult(result, cell.model),
    harness_ok: validity.ok,
    agent_status: result.status,
  };
}

async function main() {
  const { runAgent } = await loadAgents();
  const { rows, done } = loadExisting();
  let ran = 0;

  for (const cell of iterateCells()) {
    const key = cellKey(cell);
    if (done.has(key)) {
      process.stderr.write(`skip ${key} (resume)\n`);
      continue;
    }
    if (ran >= maxCells) {
      process.stderr.write(`PHYSICS_CODEGEN_MAX=${maxCells} reached\n`);
      break;
    }

    try {
      const row = await runCell(runAgent, cell);
      const idx = rows.findIndex((r) => cellKey(r) === key);
      if (idx >= 0) rows[idx] = row;
      else rows.push(row);
      writePayload(rows);
      ran++;
      process.stderr.write(
        `saved ${key} verify=${row.validity.verify_within_1ulp} thinking=${row.llm.thinking_tokens} status=${row.agent_status}\n`,
      );
    } catch (err) {
      process.stderr.write(`ERROR ${key}: ${err}\n`);
      rows.push({
        ...cell,
        validity: { verify_within_1ulp: false },
        llm: { token_source: "sdk-error", error: String(err) },
        harness_ok: false,
      });
      writePayload(rows);
    }
  }

  console.log(`physics-codegen-live: ${rows.length} sdk rows in ${OUT} (ran ${ran} this invocation)`);
  const exp = expectedRowCount();
  const sdkRows = rows.filter((r) => r.llm?.token_source?.startsWith("sdk"));
  if (sdkRows.length >= exp && sdkRows.every((r) => r.validity?.verify_within_1ulp)) {
    console.log("physics-codegen-live: matrix complete");
    return;
  }
  if (sdkRows.length < exp) {
    process.exitCode = 2;
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
