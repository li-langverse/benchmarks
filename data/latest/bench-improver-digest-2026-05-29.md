# Bench improver digest — 2026-05-29

**Agent:** `bench_improver` · **Source:** proactive · **Branch:** `chore/agent-bench_improver-50434717`  
**north_star_fit:** PH-5b, PH-7e — tier-1 pure-Li matmul vs C++ oracle; proof-before-perf (checksum parity)

## Executive summary

- **Preflight:** 0 red, **1 yellow** (`matmul_blocked`), 55 green; 131 unknown (harness pending / no local run).
- **After lic codegen pass + ingest:** `matmul_blocked` **1.253×** C++ (was **1.298×**) — still yellow, **~3.5%** closer to 1.2× gate.
- **Implemented:** fused init+blocked GEMM+vector sum in LLVM (`emit.cpp`), BSS 512² matrices, vector `fmuladd`, 8-wide `j` unroll; slim `matmul_blocked/li/main.li`.
- **Verified:** checksum `1288460.7564000632` vs C reference (pure Li, `bench.py --verify-results`).
- **Not edited:** `summary.json` by hand — ingest via `build_summary.py` + copied `latest.csv`.
- **131 unknown rows:** tier-0/CFD/FEA/DB — ecosystem gap for harness coverage, not codegen regressions.
- **Horner / matmul_naive:** briefing greens; no change this pass.
- **Strict gate:** `LI_TIER1_PERF_STRICT=1` still fails `matmul_blocked` (~1.25×) on this host.

## Deliverable / findings

| Benchmark | Status (ingest) | ratio_vs_cpp | Action taken |
|-----------|-----------------|--------------|--------------|
| `matmul_blocked` | yellow | 1.253 | PH-7e codegen fusion + study doc |
| `num_cholesky` | green (near 1.2) | — | deferred |
| `matmul_naive` | green | — | no change |
| tier-0 / CFD / FEA | unknown | — | file harness gaps; not lic perf |

**Study:** `lic/docs/numerics/studies/2026-05-29-matmul-blocked-codegen.md`

**CSV (local):** `matmul_blocked` cpp=0.0091s li=0.0114s (RTX-class linux, `-O3 -march=native -ffast-math`)

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| perf(7e): fuse tier-1 matmul_blocked pure-Li kernel (init+GEMM+sink) | **lic** | `PH-7e`, `numerics`; PR from `chore/agent-bench_improver-50434717` |
| Close G-math slice when `matmul_blocked` ≤1.2× on CI ingest | **lic** | `#27` / master-plan 7e-b |
| Ingest tier-1 full matrix after lic merge | **benchmarks** | normal `ingest-lic.sh` only |
| Register blocking / AVX-256 micro-panel for `ArrayMatMulBlocked2DF64` | **lic** | follow-up if still >1.2× |

## Deferred

- ≤1.2× **green** on all runners (needs ~5% more or machine-specific variance).
- `matmul_blocked_N1024` catalog row (unknown).
- Lean on fused MIR path (no `trusted.lean` change).
- 128 tier-1/2 **unknown** harness rows — `gap_explorer` / harness owners.
- HPC registry `last_reviewed` bump (no competitor release review this pass).
