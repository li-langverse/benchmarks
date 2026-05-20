# Benchmark dashboard honesty labels

The [public dashboard](https://li-langverse.github.io/benchmarks/) and `data/latest/summary.json` report **wall-clock ratios vs C++**, not formal proof or correctness certificates. Tier 1–2 harness runs always include **`numpy`** (`harness/numpy_kernels.py`); matmul/dot/sum use BLAS-backed NumPy ops.

## Status colors

| Status | Meaning | Agent action |
|--------|---------|--------------|
| **green** | `ratio_vs_cpp` ≤ `threshold_ratio_cpp` in [`catalog.toml`](../../catalog.toml) | Maintain; investigate regressions |
| **yellow** | Between threshold and org alert band (ingest policy) | Compiler/harness work in **lic** |
| **red** | Above threshold | **lic** codegen or kernel — not threshold tweaks here |
| **unknown** | Missing ingest, failed run, or smoke-only row | Fix harness path or ingest; do not publish perf claims |

## Variants (catalog)

| `variant` | Honest label |
|-----------|----------------|
| `default` | Li vs C++ on shared problem size; may use shared build flags |
| `shared_c_kernel` | Numerics may share C kernel — **not** pure-Li proof |
| `pure_li` | Li-only codegen path — cite **PH-7e**; red here is compiler work |
| `async_stub` | Tooling smoke — not HPC competitive |

## Timing spread

`latest.csv` may include **`value_stdev`** and **`timing_runs`** (harness: 3–6 repetitions, median reported). Sub-millisecond **v0_gaming** rows can flip green/yellow/red while stdev is large — read spread before tuning thresholds.

## Workload class

Catalog field **`workload_class`**: `full` (reference sim scale) vs `v0_gaming` (roadmap harness). See [workload-scale-and-algorithm-depth.md](../benchmark-reports/workload-scale-and-algorithm-depth.md).

## Proof vs performance

- **G-*** rows in [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) describe **proof wiring**, not bench color.
- A **green** row does **not** imply `lic build` discharges Lean for that kernel.
- A **red** `pure_li` row (e.g. `horner_pure_li`) is **performance debt**, not a missing G-* closure.

## Writing release notes / ADRs

Use: “dashboard **green** at ratio *r* vs cpp on commit *sha*” — not “proved fast” or “beats SOTA” without study citations ([numerics methodology](../numerics/research-methodology.md)). For **simulation / particles / memory / long runs**, see [SOTA comparison matrix](../numerics/sota-comparison-matrix.md) (what we measure today vs future oracle columns).
