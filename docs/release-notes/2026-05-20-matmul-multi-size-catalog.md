# Catalog: matmul multi-size (128 / 512 / 1024)

**Repo:** benchmarks + **lic** harness  
**Audience:** PH-5b / bench_improver

## Summary

- **benchmarks** `catalog.toml`: `matmul_blocked_n128`, `matmul_blocked_n1024`, `matmul_naive_n128` rows (variants label N regime).
- **lic:** new `tier1_micro` harness dirs + `bench.py` registration; tier-2 Li shim hygiene bundled on same branch.
- **Docs:** [matmul-scaling-and-huge-gemm.md](../numerics/matmul-scaling-and-huge-gemm.md); [tier1 matmul snapshot](../benchmark-reports/2026-05-20-tier1-matmul-scaling.md).

## Verification

- `python3 benchmarks/harness/bench.py --tier 1 --runs 1 --skip-verify` in **lic**; ingest `build_summary.py`.

## Note

`matmul_naive_n128` may land **yellow** (~1.22×) on a single run — threshold 1.2×; track as real micro-variance, not a catalog tweak without kernel work.
