# Tier-1 snapshot — matmul multi-size (2026-05-20)

**Harness:** `lic` `bench.py --tier 1 --runs 1 --skip-verify` (warmup + 1 median).  
**Ingest:** `build_summary.py /workspace/lic /workspace/lis`.

## Matmul Li vs C++ (`wall_time`, threshold **1.2×** unless noted)

| Benchmark | N | Li (s) | C++ (s) | Ratio | Status |
|-----------|---|--------|---------|-------|--------|
| `matmul_naive_n128` | 128 | 0.0011 | 0.0009 | **1.22** | **yellow** |
| `matmul_naive` | 256 | 0.0026 | 0.0037 | 0.70 | green |
| `matmul_blocked_n128` | 128, BK=32 | 0.0012 | 0.0012 | 1.00 | green |
| `matmul_blocked` | 512, BK=64 | 0.0103 | 0.0102 | 1.01 | green |
| `matmul_blocked_n1024` | 1024, BK=64 | 0.0833 | 0.0822 | 1.01 | green |

**Takeaway:** blocked GEMM stays **near parity** across **128 → 1024** on this runner; **naive at N=128** is slightly over **1.2×** vs cpp (compiler/heuristic variance — track with `bench_improver` / PH-5b).

## Research

- [matmul scaling & huge GEMM](../numerics/matmul-scaling-and-huge-gemm.md) — BLIS-style blocking, Strassen, SUMMA, out-of-core.

## Honesty

Single-run medians; not a release certificate. See [benchmark-dashboard.md](../honesty/benchmark-dashboard.md).
