# Bench improver — proactive sweep (2026-05-30)

**Agent:** `bench_improver` · **Source:** proactive ecosystem sweep  
**north_star_fit:** blazingly-fast — PH-5b / PH-7e tier-1 lic harness; proof-before-perf (checksum parity, no `trusted.lean` edits)  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Oracle:** `data/latest/summary.json` @ `2026-05-30T10:00:49Z` · `lic_sha` `c18c48e6`

## Executive summary

- **Public dashboard: no RED or YELLOW** tier-1 lic rows on linux after latest ingest; briefing yellow (`matmul_*`) was stale vs refreshed `summary.json`.
- **22 tier-1 greens** for lic on linux; **5 near-threshold** greens with ratio **>1.0×** but **≤1.2×** catalog cap (`threshold_ratio_cpp`).
- **Top headroom target:** `num_integ_rk4` at **1.083×** cpp — micro-opt in lic integrator lowering or RK4 loop codegen (no threshold change).
- **`perf/bench-improver-matmul-tier1-green-20260530`** (lic) holds merged emit work + study; **not on main** — open PR, full CI ingest after merge.
- **`tier0_stability`** remains **unknown** (no `stability.csv` on this runner); tier-0 must run on CI, not hand-edited JSON.
- Swarm gap registry still lists **stale** `gap-benchmark-red-matmul-naive-tier1` / `num_gmres` — close or repoint after ingest confirms green.
- HPC competitive registry gate **clear** (`lic/scripts/check-hpc-competitive.sh`).
- Do **not** edit `summary.json` alone; use `ingest-lic.sh` + full/partial harness CSV.

## Deliverable / findings

### Failures report (`./scripts/benchmark-failures-report.sh`)

```
RED: none
YELLOW: none
GREEN near threshold (>1.0× cpp, 5):
  num_integ_rk4     1.083×  PH-5b
  matmul_naive      1.056×  PH-5b, PH-7e
  simd_dot          1.052×  PH-5b, PH-7e
  matmul_blocked    1.023×  PH-5b
  fft_1d_fixed      1.007×  PH-5b, PH-7e
UNKNOWN: tier0_stability (tier 0)
```

Fresh `python3 scripts/ecosystem-audit.py` matches: `red=[]`, `yellow=[]`, same near-threshold set.

### Ingested linux tier-1 rows (before/after vs prior digest)

| benchmark | ratio vs cpp | status | li (s) | cpp (s) | Notes |
|-----------|--------------|--------|--------|---------|-------|
| `matmul_blocked` | **1.023×** | green | 0.0090 | 0.0088 | Was yellow ~1.24× in `bench_improver-20260530-tier1-red-clear` pass |
| `matmul_naive` | **1.056×** | green | 0.0019 | 0.0018 | Was yellow ~1.22×; `@` codegen on main ingest |
| `num_integ_rk4` | **1.083×** | green | 0.0013 | 0.0012 | Largest slack above parity |
| `simd_dot` | **1.052×** | green | 0.0181 | 0.0172 | PH-7e SIMD dot product |
| `fft_1d_fixed` | **1.007×** | green | 0.0153 | 0.0152 | Within noise of cpp |
| `horner_pure_li` | (green) | green | — | — | Prior red 3.0× cleared (stale CSV + cold compiler) |

### lic branch ready for PR (not merged)

Branch: `perf/bench-improver-matmul-tier1-green-20260530`  
Study: `lic/docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`

| Change | Purpose |
|--------|---------|
| `compiler/codegen/emit.cpp` | Blocked IKJ tiles, 4-wide FMA inner-`j`, 32-byte `ArrayAlloc` alignment |
| `matmul_naive/li/main.li` | `C = A @ B` pure-Li path |
| Study claims (10-run median, local) | `matmul_naive` **0.947×**, `matmul_blocked` **1.000×** |

**Gap:** Ingested dashboard still shows ~1.02–1.06× for matmul — branch not on `main` / CI full suite not re-run with branch compiler. Merge + ingest required for public parity with study.

### Repro (assessment only)

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh
python3 scripts/ecosystem-audit.py

cd ../lic && ./scripts/check-hpc-competitive.sh
# After lic PR merge:
cd lic/benchmarks/harness && python3 bench.py --tier 1 --runs 10
cd benchmarks && LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
```

### Prior agent artifacts

- `data/digest/bench_improver-2026-05-30-tier1-red-clear.md` — tier-1 red clear narrative (matmul yellow at time of write; now green on ingest).
- `data/runs/bench_improver-1780102308278.md` — matmul_blocked emit sprint context.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| `perf(7e): merge matmul blocked/naive emit (IKJ tiles, FMA SIMD, aligned alloc)` | **lic** | `PH-7e`, `PH-5b`, `numerics` — branch `perf/bench-improver-matmul-tier1-green-20260530` |
| `perf(7e): RK4 integrator loop — bring num_integ_rk4 ≤1.0× cpp` | **lic** | `PH-5b`, `numerics` — highest near-threshold row |
| `perf(7e): simd_dot pure-Li — vectorized reduction ≤1.0×` | **lic** | `PH-7e`, `PH-5b` |
| `chore(swarm): close stale gap-benchmark-red-matmul-naive / num_gmres` | **lic** or **benchmarks** | `ecosystem-gap` — rows green on dashboard |
| `ci: tier0_stability ingest on linux runner` | **benchmarks** / **lic** | `PH-5b` — populate `stability.csv` |
| `chore: ingest tier-1 after lic 7e matmul merge` | **benchmarks** | `benchmarks` — via `ingest-lic.sh` only |

## Deferred

- **≤1.0× cpp advisory** for all tier-1 micro rows — optional polish after 1.2× gate is stable; start with `num_integ_rk4`.
- **`md_thermostat_*`** tier-2 yellow (~1.29×) — shared MD oracle; separate numerics pass (not in current tier-1 ingest).
- **`ml_conv2d_forward` / `ml_mlp_*`** — **li-math** stubs; not lic codegen.
- **Parallel/simd codegen** beyond matmul — requires Lean / contract evidence per master plan PH-7d.
- **Full `./scripts/run-full-benchmark-suite.sh` on CI** after lic merge — partial `--only` ingest must not replace oracle rows.
