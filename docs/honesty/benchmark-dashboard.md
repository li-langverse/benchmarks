# Benchmark dashboard honesty labels

The [public dashboard](https://li-langverse.github.io/benchmarks/) and `data/latest/summary.json` report **wall-clock ratios vs C++**, not formal proof or correctness certificates.

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

## Proof vs performance

- **G-*** rows in [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) describe **proof wiring**, not bench color.
- A **green** row does **not** imply `lic build` discharges Lean for that kernel.
- A **red** `pure_li` row (e.g. `horner_pure_li`) is **performance debt**, not a missing G-* closure.

## Writing release notes / ADRs

Use: “dashboard **green** at ratio *r* vs cpp on commit *sha*” — not “proved fast” or “beats SOTA” without study citations ([numerics methodology](../numerics/research-methodology.md)).
