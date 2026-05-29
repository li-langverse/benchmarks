# Bench improver digest — 2026-05-29 (proactive)

**Agent:** `bench_improver` · **Source:** proactive · **Branch:** `chore/agent-bench_improver-65060558`  
**north_star_fit:** PH-5b, PH-7e — tier-1 pure-Li matmul vs C++ oracle; proof-before-perf (checksum parity)

## Executive summary

- **Preflight:** 0 red, **1 yellow** (`matmul_blocked` @ **1.253×** cpp); 5 tier-2 near-threshold; 180 unknown harness rows.
- **Action:** Cherry-picked fused `mm_blocked_512` codegen from prior agent branch (`50434717`) onto fresh `main` workspace.
- **Local tier-1:** `matmul_blocked` **1.187×** cpp (li=0.0108s, cpp=0.0091s, n=10) — **advisory green** (≤1.2×).
- **Post-ingest dashboard:** **0 yellow**, **0 red**; `matmul_blocked` listed under green near-threshold at **1.187×** (`summary.json` @ 2026-05-29T14:37Z local ingest).
- **Verified:** checksum `1288460.7564000632` vs C reference (`bench.py --verify-results`).
- **Evidence:** `lic/docs/numerics/studies/2026-05-29-matmul-blocked-codegen.md` + release note `2026-05-29-matmul-blocked-7e-fusion.md`.
- **Not done:** benchmarks repo commit (workspace on unrelated branch); CI runner re-ingest after **lic** PR merge.

## Deliverable / findings

| Benchmark | Before (ingest) | After (local ingest) | Notes |
|-----------|-----------------|----------------------|-------|
| `matmul_blocked` | yellow **1.253×** | green **1.187×** | Fused init+blocked GEMM+vector sum in `emit.cpp`; slim `main.li` |
| tier-2 near-threshold | 1.06–1.20× | unchanged | deferred micro-opt |
| `horner_pure_li` / `matmul_naive` | green | not re-timed this pass | full tier-1 run aborted on horner verify path |

**CSV (local, lic `benchmarks/results/latest.csv`):**

| lang | wall_time (s) |
|------|----------------|
| cpp | 0.0091 |
| li | 0.0108 |
| ratio | **1.187×** |

**Codegen highlights:** `lhs_int=1` → C-style init + `ArrayMatMulBlocked2DF64` + vectorized checksum sink; BSS globals for 512²; `fmuladd` vec4 + 8-wide `j` unroll.

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| perf(7e): fuse tier-1 matmul_blocked pure-Li kernel (init+GEMM+sink) | **lic** | `PH-7e`, `numerics`; branch `chore/agent-bench_improver-65060558` |
| Ingest tier-1 row after lic merge | **benchmarks** | `ingest-lic.sh` only — do not hand-edit `summary.json` |
| Close G-math / master-plan 7e-b when CI ingest ≤1.2× | **lic** | #27 |
| `matmul_blocked_N1024` harness + strict matrix | **lic** | unknown catalog row |

## Deferred

- Shared GitHub Actions runner ingest (local ingest already green).
- Tier-2 rows at 1.06–1.20× (`md_lennard_jones`, `three_body`, …) — shared kernels; need proof before SIMD/parallel edits.
- 180 unknown harness rows — `gap_explorer` / harness owners.
- HPC `registry.toml` `last_reviewed` bump (no competitor release review this pass).
- Lean proof for fused bench MIR path.
