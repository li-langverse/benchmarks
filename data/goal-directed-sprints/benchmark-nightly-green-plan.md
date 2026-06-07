# Benchmark nightly — full green (merge + publish-dashboard)

**Repos:** `benchmarks` (primary), `lic` (linker + compile), `lis` (optional tier5)  
**Branch:** `cursor/benchmark-nightly-green` (benchmarks); lic fixes via PR to `main`  
**Agent:** `code_implementer`  
**North star:** proof → easy → fast — scheduled + dispatch **benchmark-nightly** fast profile completes green through `publish-dashboard`.

## Phase status

| Phase | Scope | Status |
|-------|-------|--------|
| **BN1** | Fix `lic` linker failures (`async_await_chain`, registry tier7 Li builds) | **done** — runtime link inputs in cache key; Linux cache prefix `lic-build-linux-` (no macOS restore bleed) |
| **BN2** | Sample-run parity — equal `sample_runs` for li vs competitors in harness CSV | **done** — resume re-runs imbalanced benches; locked CSV merge in parallel tier runners |
| **BN3** | Tier1 parallel CSV safety + workflow env (`BENCH_EQUALIZE_RUNS=1`, `BENCH_RUNS=6`) | **done** — workflow + tier-group runner export equalize env; `csv_bench_io` file locks |
| **BN4** | Local progress + completion gates pass on worker | **done** — `./scripts/benchmark-nightly-green-progress-gate.sh` PASS (lic link smoke tier3+registry, 13 unit tests) |
| **BN5** | Dispatch nightly fast; verify `publish-dashboard` on GitHub Actions | **in progress** — dispatched on branch ref (run 27091622764); merge PR #439 after green |

## Gates

```bash
./scripts/benchmark-nightly-green-progress-gate.sh
./scripts/benchmark-nightly-green-gate.sh   # after BN1–BN4; polls CI when BENCHMARK_NIGHTLY_GATE_POLL=1
```

## Iteration log

| Date | Agent | Change |
|------|-------|--------|
| 2026-06-07 | code_implementer | Progress gate: link shared C kernels via `LI_EXTRA_C`; workflow `BENCH_RUNS=6` + `BENCH_EQUALIZE_RUNS=1`; tier-group runner exports equalize |
| 2026-06-07 | code_implementer | BN1: lic cache key includes runtime link inputs; BN2: parity resume + locked CSV merge; `build_li` sets `LI_REPO_ROOT` |
| 2026-06-07 | code_implementer | BN4: progress gate PASS locally (lic link smoke + 13 harness tests); BN5 deferred until PR merge |
| 2026-06-07 | code_implementer | BN5 prep: progress gate warns on stale committed CSV; `run-benchmark-ci-nightly.sh` exports `BENCH_EQUALIZE_RUNS` |
| 2026-06-07 | code_implementer | Re-verified BN4: WSL progress gate PASS (lic link smoke tier3+registry, 13 unit tests); PR #439 CI green; BN5 awaits merge to `main` |
| 2026-06-07 | code_implementer | BN5: dispatched `benchmark-nightly.yml` fast on `cursor/benchmark-nightly-green` (run 27091622764); re-verified BN4 progress gate PASS in WSL |
| 2026-06-07 | code_implementer | BN1 follow-up: Linux lic cache key `lic-build-linux-*` — `restore-keys: lic-build-` was restoring macOS CMakeCache on Linux (run 27091622764) |
