# Bench improver digest — proactive sweep 2026-05-30

**Generated:** 2026-05-30 · **Agent:** `bench_improver` · **north_star_fit:** blazingly-fast (PH-5b, PH-7e) · **Preflight:** `ecosystem-audit.json`, `summary.json`, `lic/benchmarks/results/latest.csv`

## Executive summary

- Public dashboard (`summary.json` **2026-05-29**) still shows **6 RED** and **2 YELLOW** tier-1/2 rows vs C++ — stale ingest; local lic harness already clears the two matmul reds.
- Local tier-1 proof (`lic/benchmarks/results/latest.csv`, ingest with `BENCHMARKS_CSV=../lic/benchmarks/results/latest.csv`): **`matmul_blocked` 1.023×**, **`matmul_naive` 1.056×** — both **green** under the 1.2× gate.
- **`horner_pure_li` regressed to 2.333×** on the same local CSV (li=0.0014 s, cpp=0.0006 s) — new **RED** once ingested; PH-7e FMA lowering is the next lic codegen target.
- Ingest footgun: default `benchmarks/results/latest.csv` is a **5-row stub** (md_lennard_jones only); it masks lic CSV and flips catalog rows to `harness_pending` / skip — always set `BENCHMARKS_CSV` to lic path for tier-1 ingest.
- Tier-2 **yellow** thermostats (`md_thermostat_berendsen` 1.303×, `md_thermostat_nose_hoover` 1.291×) remain on the published dashboard; not in local tier-1 CSV — need `bench.py --tier 12` before ingest.
- **`num_gmres` (1.4×)** and **`ml_*` (1.333×, li-math)** stay red on dashboard; out of scope for a single lic matmul pass.
- Open lic stacks (**#524**, **#499**, `perf/bench-improver-matmul-*` branches) carry blocked IKJ codegen + harness alignment; merge then run full ingest — do not hand-edit `summary.json`.
- Study doc **`lic/docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`** documents SOTA tiling + before/after quality table.

## Deliverable / findings

### Dashboard posture (published)

Source: `./scripts/benchmark-failures-report.sh` on `data/latest/summary.json` (generated_at **2026-05-29T18:47Z**).

| Status | Benchmark | Tier | ratio_vs_cpp | Repo | PH |
|--------|-----------|------|--------------|------|-----|
| RED | matmul_blocked | 1 | 1.549× | lic | PH-5b |
| RED | matmul_naive | 1 | 1.333× | lic | PH-5b, PH-7e |
| RED | num_gmres | 1 | 1.400× | lic | PH-5b |
| RED | ml_conv2d_forward | 1 | 1.333× | li-math | PH-5b |
| RED | ml_mlp_forward | 1 | 1.333× | li-math | PH-5b |
| RED | ml_mlp_train_step | 1 | 1.333× | li-math | PH-5b |
| YELLOW | md_thermostat_berendsen | 2 | 1.303× | lic | PH-5b |
| YELLOW | md_thermostat_nose_hoover | 2 | 1.291× | lic | PH-5b |

### Local lic harness (post-PH-7e matmul codegen)

Source: `lic/benchmarks/results/latest.csv` → ingest preview (`BENCHMARKS_CSV=../lic/benchmarks/results/latest.csv`).

| Benchmark | cpp (s) | li (s) | ratio_vs_cpp | Post-ingest status |
|-----------|---------|--------|--------------|-------------------|
| matmul_blocked | 0.0088 | 0.0090 | **1.023×** | green |
| matmul_naive | 0.0018 | 0.0019 | **1.056×** | green |
| simd_dot | 0.0184 | 0.0184 | 1.000× | green (shared C kernel) |
| reduce_sum | — | — | 1.043× | green (near threshold) |
| horner_pure_li | 0.0006 | 0.0014 | **2.333×** | **red** (regression vs dashboard 0.75×) |

**Matmul codegen path (lic, Mode A SOTA):** blocked IKJ tiles BK=64 via `ArrayMatMulBlocked2DF64` + 4-wide FMA inner `j` — aligned with org oracle `common/matmul_blocked_core.c` and BLIS/Goto tiling recipes (see study doc).

### Ingest / measurement gaps

| Gap | Impact | Follow-up |
|-----|--------|-----------|
| Stub `benchmarks/results/latest.csv` preferred over lic CSV | Entire catalog → `skip` / `harness_pending` on naive ingest | Set `BENCHMARKS_CSV=../lic/benchmarks/results/latest.csv` in ingest-lic CI/docs; or remove/rename stub |
| Local CSV tier-1 only | Tier-2 greens drop on partial ingest | Run `python3 bench.py --tier 12 --runs 5` in lic before ingest |
| `build-summary-li.sh` skips (PH-IO-7) | Falls back to Python `build_summary.py` | Track PH-IO-7; no fake greens |
| GitHub API rate limit this run | Could not live-verify PR CI via `gh` | Human confirms **lic#524** / **#499** merge queue |

### HPC competitive review

- `check-hpc-competitive.sh` not present in benchmarks repo (registry review deferred).
- Near-threshold greens on dashboard (>1.0×, top): `num_cholesky` 1.167×, `cloth_swing` 1.154×, robo_* cluster 1.105× — micro-opt backlog after reds clear.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| perf(bench): tier-1 matmul_blocked harness — clear dashboard yellow | **lic** (#524) | `PH-5b`, `PH-7e`, `performance` |
| fix(bench): restore tier-1 matmul MIR fast paths (PH-5b, PH-7e) | **lic** (#499) | `PH-7e`, `performance` |
| chore(bench): ingest tier-1 matmul greens from lic CSV | **benchmarks** | `PH-5b`, `ingest` |
| perf(codegen): PH-7e — lower horner_pure_li to FMA LLVM (≤1.2× cpp) | **lic** | `PH-7e`, `numerics-research`, `novel-algorithm` (if new lowering) |
| perf(bench): tier-2 MD thermostat wrapper overhead (≤1.2× cpp) | **lic** | `PH-5b`, `tier-2` |
| perf(li-math): ML tier-1 kernels vs cpp oracle | **li-math** | `PH-5b` |
| fix(ingest): prefer lic `benchmarks/results/latest.csv` over stub | **benchmarks** | `ecosystem`, `ingest` |

**Merge order:** lic matmul PRs → `LIC_ROOT=../lic BENCHMARKS_CSV=../lic/benchmarks/results/latest.csv ./scripts/ingest/ingest-lic.sh` → benchmarks ingest PR with cited CSV rows (no manual JSON edits).

## Deferred

- **`num_gmres` (1.4×)** — shared-C iterative solver wrapper; needs lic harness + possibly `common/*_core.c` proof path.
- **`ml_*` reds** — owned by **li-math**, not lic codegen.
- **Tier-2 thermostat yellows** — require full tier-12 bench run + visual sanity (`render-benchmark-visuals.sh`) before micro-opt.
- **Near-threshold tier-1/2 greens** (`num_cholesky`, robo_*, `cloth_swing`) — batch after primary reds ingested.
- **`tier0_stability`** — unknown on dashboard; tier-0 gate unchanged (do not weaken tolerances).
- **Lean / `@parallel` proof** — any parallel/simd codegen changes still need human-approved Lean evidence per swarm mandate.

## Error

None (GitHub `gh` API rate-limited — PR CI status inferred from preflight `ecosystem-audit.json` ready list, not re-fetched this run).
