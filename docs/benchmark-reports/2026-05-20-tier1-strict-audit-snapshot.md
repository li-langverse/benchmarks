# Tier-1 snapshot — post strict-build / package audit doc (2026-05-20)

**Context:** New Cursor rules + [lic package↔bench audit](https://github.com/li-langverse/lic/blob/main/docs/benchmarks/package-suite-coverage-audit.md).  
**Harness:** `lic` `bench.py --tier 1 --runs 1 --skip-verify` · ingest `build_summary.py`.

## Tier counts

- **Tier 1:** 7 **green**, 1 **yellow**, 0 red  
- **Tier 2:** all **unknown** (no tier-2 rows in this CSV ingest)

## Tier-1 ratios (Li vs cpp)

| id | ratio | status |
|----|-------|--------|
| simd_dot | 0.012 | green |
| horner_pure_li | 0.364 | green |
| matmul_naive | 0.703 | green |
| matmul_naive_n128 | 1.222 | **yellow** |
| matmul_blocked_n128 | 1.000 | green |
| matmul_blocked | 1.010 | green |
| matmul_blocked_n1024 | 1.013 | green |
| reduce_sum | 1.044 | green |

## Rules added (same day)

- **lic:** `.cursor/rules/li-package-benchmark-suites.mdc` · `docs/benchmarks/package-suite-coverage-audit.md` · `benchmarks.mdc` tightened for **`lic build`** + audit links.
- **benchmarks:** `.cursor/rules/lic-benchmark-catalog-parity.mdc` for `catalog.toml` ↔ `LIC_ROOT` path parity.
