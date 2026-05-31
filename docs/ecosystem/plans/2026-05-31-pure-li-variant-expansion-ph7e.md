# Pure-Li variant catalog expansion (PH-7e / REQ-BENCH-PURELI-1)

> **Issue:** [benchmarks#41](https://github.com/li-langverse/benchmarks/issues/41)  
> **Related:** [lic#9](https://github.com/li-langverse/lic/issues/9), [lic#27](https://github.com/li-langverse/lic/issues/27), [lic#424](https://github.com/li-langverse/lic/issues/424)  
> **Repo:** li-langverse/benchmarks (catalog) + **lic** (harness + codegen)  
> **Vision:** **Fast** (measured pure-Li vs C++), **Provable** (codegen proof surface for PH-7e)  
> **Learned from:** [ecosystem-explorer.json](../../../data/latest/ecosystem-explorer.json), [master plan PH-7e](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md), [research-methodology.md](../../numerics/research-methodology.md), [benchmark-dashboard honesty](../../honesty/benchmark-dashboard.md)

## Goal

Expand tier-1 **catalog** rows with `variant = "pure_li"` so PH-7e codegen lowering has multiple measured proof surfaces beyond the single red `horner_pure_li` row (~88× cpp). Harness implementations stay in **lic**; **benchmarks** adds catalog metadata and ingest only.

## Non-goals

- Weakening `threshold_ratio_cpp` to greenwash red rows.
- Copying harness into **benchmarks**.
- Claiming **G-math** closure from catalog rows alone.
- Adding pure-Li variants for tier-2 physics before tier-1 micro coverage is honest.

## Dependencies

- **PH-7e** — SIMD/parallel lowering for loop matmul, dot, reductions.
- **PH-5b** — tier-1 micro harness patterns under `lic/benchmarks/tier1_micro/`.
- **lic** codegen PRs for each new pure-Li kernel (blocked on **`plan-approved`** here).
- Existing green default variants: `matmul_naive`, `simd_dot`, `fft_1d_fixed` (near-threshold).

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **Numerics study** `docs/numerics/studies/2026-05-31-pure-li-tier1-candidates.md` — rank 5 kernels by codegen leverage | Study merged; cites SOTA + current ratios |
| B | **Catalog rows** — add `pure_li` variant for 3–5 tier-1 ids (see candidates below) | Rows merged with `catalog_lifecycle=planned` until harness green |
| C | **lic** harness — `*_pure_li/` dirs mirroring default micro benches | `bench.py --tier 1` includes ids |
| D | **PH-7e lowering** — vectorize/FMA paths per kernel | Each row ≤1.2× advisory or documented defer |
| E | Dashboard ingest — separate `variant` column visible on matrix | No threshold weakening |

## Candidate pure-Li rows (initial)

| Catalog id | Rationale | Current default ratio |
|------------|-----------|----------------------|
| `matmul_naive` | Loop matmul codegen (PH-7e core) | ~1.11× (near threshold) |
| `simd_dot` | Reduction + SIMD dot product | ~1.04× |
| `matmul_blocked` | Blocked GEMM lowering | yellow >1.2× |
| `num_integ_rk4` | FMA-heavy integration loop | green near 1.08× |
| `reduction_sum` (new) | Scalar reduction codegen surface | — |

Defer `horner_pure_li` greening to dedicated numerics track (lic#424); use as stress case, not first expansion target.

## Tests / benches

- **lic:** `benchmarks/harness/bench.py --tier 1 --variant pure_li` for each new id.
- **benchmarks:** ingest after lic PR; `ecosystem-audit.py` tracks pure_li count ≥4.
- **li-tests:** no compiler changes in catalog PR; codegen tests in **lic** only.

## Provability

- **G-math** — stays **Partial**; pure-Li benches supply perf evidence for lowering, not proof closure.
- **G-par** — unchanged unless `@parallel` pure-Li variants added later (out of scope).
- Update **provability-gaps.md** only when Lean witnesses exist for lowered kernels.

## Rollout

1. **benchmarks** draft PR: this plan (after human review).
2. **benchmarks** PR: catalog rows + numerics study (post **`plan-approved`**).
3. **lic** PR(s): harness + PH-7e lowering per kernel (one PR per kernel cluster).
4. Close #41 when pure_li catalog count ≥4 and ≥2 green at ≤1.2×.

## Human-only

- Approve which kernels enter wave 1 (matmul vs dot vs RK4).
- Confirm CI budget for additional pure-Li compile+run time on tier-1 matrix.
