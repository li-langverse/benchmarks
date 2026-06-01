#!/usr/bin/env node
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { benches, expectedRowCount, fixedModelArmB, LANGS, modelsForArmA, pilotMode } from "./config.mjs";
import { verifyBench } from "./verify-cell.mjs";

const ROOT = process.env.BENCHMARKS_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const OUT = process.env.PHYSICS_CODEGEN_RESULTS || path.join(ROOT, "results", "physics-codegen-matrix.json");

function hashSeed(...parts) {
  let h = 2166136261;
  for (const p of parts) {
    for (let i = 0; i < p.length; i++) {
      h ^= p.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
  }
  return h >>> 0;
}

function tokenFixture(model, benchId, lang) {
  const seed = hashSeed(model, benchId, lang);
  return {
    input_tokens: 900 + (seed % 500),
    output_tokens: 450 + (seed % 250),
    thinking_tokens: 180 + (seed % 420),
    thinking_tokens_estimated: true,
  };
}

function buildRows() {
  const rows = [];
  const benchList = benches();
  const models = modelsForArmA();
  const requireNative = process.env.PHYSICS_CODEGEN_REQUIRE_NATIVE === "1";

  for (const model of models) {
    for (const benchId of benchList) {
      const validity = verifyBench(benchId, { requireNativeLang: requireNative });
      rows.push({
        arm: "A",
        bench_id: benchId,
        model,
        lang: "li",
        validity: { verify_within_1ulp: validity.verify_within_1ulp, checksum: validity.checksum },
        llm: tokenFixture(model, benchId, "li"),
        harness_ok: validity.ok,
      });
      process.stderr.write(`A ${model} ${benchId} li ${validity.ok ? "ok" : "FAIL"}\n`);
    }
  }

  const modelB = fixedModelArmB();
  for (const benchId of benchList) {
    for (const lang of LANGS) {
      const validity = verifyBench(benchId, { requireNativeLang: requireNative });
      rows.push({
        arm: "B",
        bench_id: benchId,
        model: modelB,
        lang,
        validity: { verify_within_1ulp: validity.verify_within_1ulp, checksum: validity.checksum },
        llm: tokenFixture(modelB, benchId, lang),
        harness_ok: validity.ok,
      });
      process.stderr.write(`B ${modelB} ${benchId} ${lang} ${validity.ok ? "ok" : "FAIL"}\n`);
    }
  }
  return rows;
}

const rows = buildRows();
const payload = {
  generated_at: new Date().toISOString(),
  pilot: pilotMode(),
  models_arm_a: modelsForArmA(),
  model_arm_b: fixedModelArmB(),
  benches: benches(),
  token_source: "fixture",
  rows,
};
mkdirSync(path.dirname(OUT), { recursive: true });
writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n", "utf8");
console.log(`wrote ${rows.length} rows -> ${OUT}`);
const failed = rows.filter((r) => !r.validity?.verify_within_1ulp);
if (failed.length) process.exit(1);
if (rows.length !== expectedRowCount()) process.exit(1);
