# Study: autoresearch proactive sweep v9 (2026-05-30)

**Date:** 2026-05-30  
**Mode:** Autoresearch (B) → **closed negative** (no novel algorithm shipped)  
**Target:** tier-1 dashboard reds — pure_li codegen-bound rows  
**Agent:** autoresearch proactive pass (`autoresearch-1780128198169`)  
**north_star_fit:** PH-5b, PH-7e

---

## 1. Problem framing

Ecosystem audit listed **6 red** tier-1 rows (ingest @ 2026-05-29). After local ingest refresh (2026-05-30T08:06Z), dashboard rows show **`harness_pending`** — tier-1 Li timings are not flowing into `benchmarks/results/latest.csv`. Autoresearch asks whether any gap requires **novel** numerics vs PH-7e codegen / ingest debt.

---

## 2. SOTA survey (Mode A)

| Bench | Closest published method | Li variant | Autoresearch? |
|-------|-------------------------|------------|---------------|
| matmul_blocked | BLIS IKJ + BK=64 micro-kernel | pure_li (`C = A @ B`) | **No** — 1.230× local; ~3% PH-7e emit gap |
| matmul_naive | Classical IKJ GEMM | pure_li | **No** — 1.158× local green |
| horner_pure_li | Horner FMA chain (NR §5.3) | pure_li | **No** — 2.6× scalar loop; PH-7e vectorize (Mode A) |
| num_gmres | Saad GMRES | shared_c_kernel | **No** — harness not in lic tier-1 |
| ml_conv2d / ml_mlp_* | im2col + GEMM / MLP | algo_registry (li-math) | **No** — wrong repo/agent |

**Learned from:**

1. BLIS kernel how-to — blocked IKJ + micro-kernel for `matmul_blocked`.
2. Eigen efficient matrix product — `@` / MIR lowering target.
3. Numerical Recipes §5.3 — Horner recurrence for `horner_pure_li`.
4. Saad, *Iterative Methods* — GMRES baseline for `num_gmres`.
5. Prior negative: [`2026-05-17-horner-pure-li-autoresearch-negative.md`](./2026-05-17-horner-pure-li-autoresearch-negative.md).

---

## 3. Hypothesis + experiments

### H1 — Vec-FMA blocked codegen closes pure_li gap (not novel algorithm)

**Hypothesis:** In-tree 4-wide inner-`j` FMA (`e6fcf17f`) brings `matmul_blocked` ≤1.2× without changing the numerical recipe.

**Result:** **Partial** — local **1.230×** (cpp 0.0087 s, li 0.0107 s); checksum `1288460.7563999966` matches oracle. Marginal ~3% gap → register/tile polish on `perf/bench-improver-matmul-simd-j-20260530`, not new blocking scheme.

### H2 — Novel blocking / Horner reordering

**Result:** **Rejected** — BLIS IKJ+BK=64 and classical Horner are SOTA; invention adds proof debt without measured win.

### H3 — Ingest / harness wiring

**Result:** **Confirmed gap** — post-ingest tier-1 rows show `validity_source: harness_pending`; lic `bench.py` writes `lic/benchmarks/results/latest.csv` but benchmarks ingest does not surface Li/cpp ratios on dashboard. **ecosystem-gap** for ingest path, not autoresearch.

---

## 4. Quality table

| Axis | Before (dashboard) | After (local @ e6fcf17f) | Verdict |
|------|-------------------|--------------------------|---------|
| Speed matmul_blocked | 1.549× red | **1.230×** red | Improved; PH-7e polish open |
| Speed matmul_naive | 1.333× red | **1.158×** green | Local pass; ingest stale |
| Speed horner_pure_li | 0.750× green | **2.600×** red (local) | PH-7e scalar; Mode A |
| Accuracy | — | matmul checksum pass | **Pass** |
| Novel invention | — | None | **Negative (valuable)** |

---

## 5. Commands

```bash
cd lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_blocked,matmul_naive,horner_pure_li --runs 3

cd benchmarks
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
python3 scripts/ecosystem-audit.py
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-autoresearch-proactive-sweep-v9.md
```

---

## 6. Status

**Closed — negative autoresearch.** No tier-1 red requires a novel numerical method. Hand off PH-7e codegen polish + ingest wiring to **bench_improver** / **code_implementer**; Horner FMA vectorization to **numerics_researcher** (Mode A).
