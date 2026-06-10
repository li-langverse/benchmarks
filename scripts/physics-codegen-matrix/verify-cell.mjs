#!/usr/bin/env node
/** Verify one bench cell against C oracle via harness bench.py. */
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const BENCH_ROOT =
  process.env.BENCHMARKS_ROOT ||
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

export function verifyBench(benchId, { requireNativeLang = false, lang = "li" } = {}) {
  const args = [
    path.join(BENCH_ROOT, "harness/bench.py"),
    "--tier",
    "2",
    "--verify-results",
    "--only",
    benchId,
  ];
  if (requireNativeLang) args.push("--require-native-lang");
  const env = {
    ...process.env,
    LIC_ROOT: process.env.LIC_ROOT || "/workspace/lic",
  };
  const proc = spawnSync("python3", args, {
    cwd: BENCH_ROOT,
    env,
    encoding: "utf8",
    timeout: 600_000,
  });
  const ok = proc.status === 0;
  const text = `${proc.stdout || ""}${proc.stderr || ""}`;
  const m = text.match(/checksum=([0-9.eE+-]+)/) || text.match(/result=([0-9.eE+-]+)/);
  return {
    ok,
    verify_within_1ulp: ok,
    checksum: m ? m[1] : undefined,
    log: text.slice(-600),
    lang,
  };
}
