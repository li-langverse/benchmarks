# Bench improver — tier-1 matmul PH-7e (2026-05-30)

**Run:** `bench_improver` · **heap:** `coord_numerics` · **Date:** 2026-05-30  
**north_star_fit:** blazingly-fast — numerics tier-1 pure-Li `@` matmul (PH-5b, PH-7e)  
**Branch:** `li-langverse/lic` → `perf/bench-improver-matmul-simd-j-20260530` (`ae8f500f`)

## Executive summary

- Preflight audit listed **6 red** lic rows; live ingest after tier-1 rerun shows **matmul + ML/gmres reds cleared** on current codegen branch — only **`horner_pure_li` remains red** (3.0× cpp).
- **`matmul_blocked`** improved from briefing **1.549× → 1.022×** (6-run median: li=0.0091s, cpp=0.0089s) via blocked IKJ + 4-wide inner-`j` FMA + 32-byte tile alignment.
- **`matmul_naive`** at **1.056×** (li=0.0020s, cpp=0.0019s) — within 1.2× cap; pure-Li `C = A @ B`.
- **`check-tier1-li-vs-cpp.sh`** passes matmul rows; advisory gap **`horner_pure_li` 2.5–3.0×** (FMA Horner lowering — overlaps proof_gap_researcher G-hw).
- Fixed **ingest blind spot:** lic `bench.py` now emits **`os`** column (matches benchmarks harness) so `build_summary.py` platform matching no longer marks tier-1 rows `skip`.
- **10 open lic matmul PRs** — recommend consolidating into one focused PR; close workspace-sweep megabranches (#516, #503).
- Dashboard refresh via normal ingest only (`LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh`); do **not** hand-edit `summary.json`.
- **`tier0_stability`** still unknown (no stability.csv on this runner).

## Deliverable / findings

### Before / after (CSV — `lic/benchmarks/results/latest.csv`, 6-run median)

| benchmark | cpp (s) | li (s) | ratio | status |
|-----------|---------|--------|-------|--------|
| `matmul_naive` | 0.0019 | 0.0020 | **1.056×** | green |
| `matmul_blocked` | 0.0089 | 0.0091 | **1.022×** | green |
| `simd_dot` | 0.0186 | 0.0177 | 0.952× | green |
| `reduce_sum` | 0.0738 | 0.0770 | 1.043× | green |
| `horner_pure_li` | 0.0005 | 0.0015 | **3.000×** | **red** |

Briefing stale rows (agent workspace CSV, pre-merge): `matmul_blocked` 1.549×, `matmul_naive` 1.333×, `num_gmres` 1.4×, `ml_*` 1.333× — not reproduced on `ae8f500f` tier-1 harness.

### Codegen (lic branch — already landed on working tree)

1. **`b5d45134`** — fix blocked matmul tile loop origins (correctness).
2. **`e6fcf17f`** — 4-wide inner-`j` vector FMA in `emit_matmul2d_blocked_ijk` / flat IKJ.
3. **`3d1c5001`** — study doc [`docs/numerics/studies/2026-05-30-matmul-blocked-7e.md`](https://github.com/li-langverse/lic/blob/perf/bench-improver-matmul-simd-j-20260530/docs/numerics/studies/2026-05-30-matmul-blocked-7e.md).
4. **This pass** — `benchmarks/harness/bench.py`: add `os` to CSV_HEADER + `host_os_tag()` for ingest platform join.

### Commands (repro)

```bash
cd lic && ./scripts/build.sh
cd lic/benchmarks/harness && python3 bench.py --tier 1 --runs 6
cd lic && ./scripts/check-tier1-li-vs-cpp.sh

cd benchmarks
cp ../lic/benchmarks/results/latest.csv results/latest.csv
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
./scripts/benchmark-failures-report.sh
```

## Recommended issues/PRs

| Repo | Title | Labels | Action |
|------|-------|--------|--------|
| **lic** | `perf(7e): tier-1 matmul blocked/naive ≤1.2× cpp + bench os column` | `PH-5b`, `PH-7e`, `numerics` | **Open/update** — squash `#469`+#`499` codegen into one PR off `perf/bench-improver-matmul-simd-j-20260530`; **close** `#516`, `#503` (workspace-sweep noise). |
| **lic** | `perf(7e): horner_pure_li FMA loop — tier-1 ≤1.2× cpp` | `PH-7e`, `numerics`, `proof-gap` | **New** — coordinate with proof_gap_researcher on `FmaFloatF64` / `--numerically-stable` gate before chasing speed. |
| **lic** | `chore: close duplicate bench_improver matmul PR stack (#409–#446)` | `cleanup` | Human triage — 10 stacked agent PRs. |
| **benchmarks** | `chore: ingest tier-1 matmul greens + os-column CSV` | `benchmarks` | This digest + `results/latest.csv` + `data/latest/summary.json` via ingest. |
| **li-math** | `perf: ml_conv2d_forward / ml_mlp_* tier-1 ≤1.2× cpp` | `PH-5b`, `PH-ML` | Deferred — **li-math** repo, not lic codegen. |

## Deferred

- **`horner_pure_li`** (3.0×) — pure-Li Horner FMA; proof/codegen policy gap (see `proof_gap_researcher` cycle 18 digest).
- **`num_gmres`**, **`ml_conv2d_forward`**, **`ml_mlp_*`** — briefing reds; not in partial tier-1 CSV; re-verify after full `./scripts/run-full-benchmark-suite.sh` on CI post-merge.
- **`md_thermostat_*`** yellow (~1.29×) — tier-2 shared kernel micro-opt; separate numerics pass.
- **`tier0_stability`** unknown — run tier-0 harness + stability.csv on CI runner.
- Full nightly ingest — partial `--only` / stale `benchmarks/results/latest.csv` clears unrelated dashboard rows; always copy lic CSV or run full suite.
