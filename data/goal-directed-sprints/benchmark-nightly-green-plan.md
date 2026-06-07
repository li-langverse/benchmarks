# Benchmark nightly — full green (merge + publish-dashboard)

**Repos:** `benchmarks` (primary), `lic` (linker + compile), `lis` (optional tier5)  
**Branch:** `cursor/benchmark-nightly-green` (benchmarks); lic fixes via PR to `main`  
**Agent:** `code_implementer`  
**North star:** proof → easy → fast — scheduled + dispatch **benchmark-nightly** fast profile completes green through `publish-dashboard`.

## Phase status

| Phase | Scope | Status |
|-------|-------|--------|
| **BN1** | Fix `lic` linker failures (`async_await_chain`, registry tier7 Li builds) | **in progress** — progress gate smoke passes tier3 + registry alias when `LI_EXTRA_C` is set for shared C kernels |
| **BN2** | Sample-run parity — equal `sample_runs` for li vs competitors in harness CSV | pending — committed `summary.json` still fails `MEASUREMENT_STRICT_PARITY=1` (22 imbalances); needs fresh nightly after BN3 |
| **BN3** | Tier1 parallel CSV safety + workflow env (`BENCH_EQUALIZE_RUNS=1`, `BENCH_RUNS=6`) | **done** — workflow + tier-group runner export equalize env |
| **BN4** | Local progress + completion gates pass on worker | **in progress** — progress gate passes locally after BN1 smoke fix |
| **BN5** | Dispatch nightly fast; verify `publish-dashboard` on GitHub Actions | pending |

## Gates

```bash
./scripts/benchmark-nightly-green-progress-gate.sh
./scripts/benchmark-nightly-green-gate.sh   # after BN1–BN4; polls CI when BENCHMARK_NIGHTLY_GATE_POLL=1
```

## Iteration log

| Date | Agent | Change |
|------|-------|--------|
| 2026-06-07 | code_implementer | Progress gate: link shared C kernels via `LI_EXTRA_C`; workflow `BENCH_RUNS=6` + `BENCH_EQUALIZE_RUNS=1`; tier-group runner exports equalize |
