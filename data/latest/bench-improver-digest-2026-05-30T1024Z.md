# Bench improver digest — 2026-05-30T10:24Z

**Agent:** `bench_improver` · **Run:** `bench_improver-1780136668286` · **Source:** proactive ecosystem sweep  
**North star fit:** blazingly-fast tier-1 numerics (PH-5b, PH-7e) — proof-before-perf; dashboard oracle = shared **cpp** cores  
**Dashboard:** https://li-langverse.github.io/benchmarks/

## Executive summary

- **No RED or YELLOW lic rows** on the public dashboard (`summary.json` generated 2026-05-30T10:00Z); **22 green** tier-1 lic benchmarks, all ≤ **1.2×** cpp threshold.
- **5 near-threshold greens** (>1.0× cpp, headroom shrinking): `num_integ_rk4` **1.083×**, `matmul_naive` **1.056×**, `simd_dot` **1.052×**, `matmul_blocked` **1.023×**, `fft_1d_fixed` **1.007×**.
- **Major recovery since last snapshot:** 23 rows flipped `skip` → `green` (matmul family, horner, fft, num_* integrators); prior reds cleared via ingest without threshold relaxation.
- **`tier0_stability` is UNKNOWN** (not red): ingest expects `tier0_stability` row in `lic/benchmarks/results/stability.csv` but file uses per-test schema — validity stuck at `unknown`.
- **Stale PR stack:** ≥10 open `chore/agent-bench_improver-*` lic PRs overlap on matmul codegen; [lic#524](https://github.com/li-langverse/lic/pull/524) CI green; [lic#499](https://github.com/li-langverse/lic/pull/499) CI red on linux/macos.
- **HPC competitive script missing** in benchmarks checkout (`scripts/check-hpc-competitive.sh` not present; only `competitive/stdlib_registry.toml`) — registry gate skipped this pass.
- **Prior agent runs errored** (`unregistered_running_reconciled`) — supervisor reconciliation, not benchmark regression.
- **Next micro-opt target:** `num_integ_rk4` (shared-C RK4 stub, largest gap among near-threshold rows).

## Deliverable / findings

### Preflight (`ecosystem-audit` benchmarks section)

| Signal | Value |
|--------|-------|
| `red` | `[]` |
| `yellow` | `[]` |
| `near_threshold` | 5 rows (see table below) |
| `green_count` | 22 (lic linux tier-1+) |
| `unknown` | `tier0_stability` |

```bash
cd benchmarks && ./scripts/benchmark-failures-report.sh
# RED: none
# GREEN near threshold (>1.0× cpp, 5): num_integ_rk4 … fft_1d_fixed
# UNKNOWN: tier0_stability
```

### Near-threshold CSV rows (`results/latest.csv` / dashboard)

| Benchmark | Li (s) | Cpp (s) | Ratio | Variant | PH | Micro-opt lever |
|-----------|--------|---------|-------|---------|-----|-----------------|
| `num_integ_rk4` | 0.0013 | 0.0012 | **1.083×** | shared C kernel | PH-5b | FFI/wrapper + RK4 stage unroll in Li driver |
| `matmul_naive` | 0.0019 | 0.0018 | **1.056×** | pure Li `@` | PH-5b, PH-7e | `@vectorized` / FMA inner loop (Phase 7e) |
| `simd_dot` | 0.0181 | 0.0172 | **1.052×** | shared C kernel | PH-5b, PH-7e | `common/simd_dot_core.c` + Li call overhead |
| `matmul_blocked` | 0.0090 | 0.0088 | **1.023×** | pure Li blocked | PH-5b | BK sweep / LLVM autovec (study: `docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`) |
| `fft_1d_fixed` | 0.0153 | 0.0152 | **1.007×** | FFTW reference | PH-5b, PH-7e | parity — monitor only |

**Wins already on dashboard:** `horner_pure_li` **0.80×** cpp (pure Li FMA); matmul family down from prior **1.33–1.55×** reds.

### Tier-0 stability ingest gap

- `lic/benchmarks/results/stability.csv` has 17 per-test rows (`harmonic_energy`, `nve_energy_msd`, …) but **no aggregate `tier0_stability` row**.
- `build_summary.py` → `load_stability_index()` keys on `test` column; without `tier0_stability`, validity = `unknown`.
- **Not a numerics regression** — Li/cpp both report `li_value=1.0` pass in summary rollup; dashboard cell shows grey/unknown.
- **Fix path:** emit rollup row from tier-0 harness ingest **or** teach ingest to aggregate per-test passes (benchmarks repo).

### HPC competitive review (partial)

- `competitive/registry.toml` absent in local benchmarks tree; `check-hpc-competitive.sh` missing — full registry gate deferred.
- Manual read of `results/latest.csv`: all measured lic tier-1 rows ≤ **1.2×** cpp on linux x86_64 (`11ef5e37` / `c18c48e6` commits).

### lic workspace / study evidence

- Partial study on disk: `lic/docs/numerics/studies/2026-05-30-matmul-blocked-7e.md` — local blocked matmul **1.023×** on dashboard matches study “after” column.
- Multiple local perf branches (`perf/bench-improver-matmul-*-20260530`) not yet merged; dashboard already reflects earlier ingest (`11ef5e37`).

### Control plane

- 9 prior `bench_improver` runs today ended `error: unregistered_running_reconciled` — orchestration cleanup, not bench failure.

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P1 | lic | [#524](https://github.com/li-langverse/lic/pull/524) perf(bench): tier-1 matmul_blocked harness | `numerics-research`, PH-7e — **CI green**, ready for human review |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) fix(bench): restore tier-1 matmul MIR fast paths | PH-5b, PH-7e — **build-and-test FAIL** linux/macos; fix before merge |
| P2 | lic | **New:** micro-opt `num_integ_rk4` ≤1.0× cpp | `numerics-research`, PH-5b — shared-C wrapper + study doc |
| P2 | benchmarks | **New issue:** tier0_stability ingest rollup | `ecosystem-gap` — aggregate `stability.csv` or ingest logic |
| Hygiene | lic | Close/supersede #407, #409, #418, #427, #435, #437, #446, #469 + agent branches | Delegate to `pr_alignment`; canonical = #524 / #499 |
| Hygiene | benchmarks | [#208](https://github.com/li-langverse/benchmarks/pull/208) matmul tier-1 digest | Align with current green dashboard; refresh near-threshold table |
| Hygiene | benchmarks | [#211](https://github.com/li-langverse/benchmarks/pull/211) tier-1 red-clear ingest | Verify still needed post-matmul greens |

## Deferred

- **Micro-opt implementation** for `num_integ_rk4` / `matmul_naive` / `simd_dot` — requires lic codegen PR + local `bench.py` proof + normal ingest (no hand-edited `summary.json`).
- **`check-hpc-competitive.sh` / `registry.toml`** restoration in benchmarks repo — file gap or branch drift.
- **macOS / Windows** tier-1 platform rows — all `skip` (`platform_not_measured`); out of scope for linux-only agent pass.
- **li-math** `ml_*` stubs — not in lic harness; separate repo when wired.
- **Lean / `@parallel` proofs** for SIMD matmul changes — human-approved issues only (Phase 7d G-par).
- **Merge execution** — no self-merge; human + pr_merger gate.

## Commands (reproduce)

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh

export LIC="$(./scripts/resolve-lic.sh)"
python3 "$LIC/benchmarks/harness/bench.py" --tier 1 --runs 5 \
  --only num_integ_rk4,matmul_naive,matmul_blocked,simd_dot,fft_1d_fixed

cd benchmarks && LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
```
