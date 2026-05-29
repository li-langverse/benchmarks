# Tier-1 matmul dashboard sprint (workloads sync)

## Summary

Sync `benchmarks/workloads/tier1_micro/matmul_{naive,blocked}/li/main.li` with **lic** drivers that match C++ IKJ / blocked IKJ (see lic `docs/release-notes/2026-05-29-tier1-matmul-bench-align-cpp.md`). Dashboard reds clear after `LIC_ROOT` bench + `./scripts/ingest/ingest-lic.sh`.

## Preflight baseline (2026-05-29)

| Status | Benchmark | Ratio vs C++ | Repo |
|--------|-----------|--------------|------|
| red | matmul_blocked | 1.549× | lic |
| red | matmul_naive | 1.333× | lic |
| red | num_gmres | 1.400× | lic |
| red | ml_* (×3) | 1.333× | li-math |

## Agent continuation

1. Merge lic PR with matmul driver + codegen fix.
2. `LIC_ROOT=../lic python3 benchmarks/harness/bench.py --tier 1` (in lic).
3. `./scripts/ingest/ingest-lic.sh` here; confirm `./scripts/benchmark-failures-report.sh` shows zero tier-1 matmul reds.

## Changed

| Path | Evidence |
|------|----------|
| `benchmarks/workloads/tier1_micro/matmul_naive/li/main.li` | 256³ IKJ |
| `benchmarks/workloads/tier1_micro/matmul_blocked/li/main.li` | 512× blocked 64³ |

## Deferred

- `num_gmres`, `li-math` ML kernels — need package-local fixes.
- CSV refresh blocked on agent host without LLVM 18 (`./scripts/build.sh`).
