# Study: autoresearch proactive sweep v8 (2026-05-30)

**Date:** 2026-05-30  
**Mode:** Autoresearch (B) → **closed negative** (no novel algorithm shipped)  
**Target:** tier-1 dashboard reds — focus pure_li codegen-bound rows  
**Agent:** autoresearch proactive pass (`autoresearch-1780124755372`)  
**north_star_fit:** PH-5b, PH-7e

---

## 1. Problem framing

Ecosystem audit (2026-05-29 ingest) lists **6 red** tier-1 rows. Autoresearch runs **after** numerics_researcher when SOTA is insufficient. This pass asks: do any reds require **novel** numerics, or are they codegen/harness/ingest debt?

---

## 2. SOTA survey (Mode A)

| Bench | Closest published method | Li column variant | Autoresearch? |
|-------|-------------------------|-------------------|---------------|
| matmul_blocked | BLIS blocked GEMM (IKJ, BK=64) | pure_li (`C = A @ B`) | **No** — marginal PH-7e emit (~1.229×) |
| matmul_naive | Classical IKJ GEMM | pure_li | **No** — local 1.056× green; ingest stale |
| horner_pure_li | Horner FMA chain (NR §5.3) | pure_li | **No** — PH-7e scalar loop; SOTA sufficient |
| num_gmres | Saad GMRES | shared_c_kernel | **No** — harness not in lic tier-1 scope |
| ml_conv2d / ml_mlp_* | im2col + GEMM / MLP layers | algo_registry (li-math) | **No** — wrong repo/agent |

**Learned from:**

1. [BLIS kernel how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) — micro-kernel + blocking for `matmul_blocked`.
2. [Eigen — efficient matrix product](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) — `@` / MIR lowering target.
3. [Numerical Recipes §5.3](https://numerical.recipes/book/bookcpdf/c5-3.pdf) — Horner recurrence for `horner_pure_li`.
4. Saad, *Iterative Methods for Sparse Linear Systems* — GMRES baseline for `num_gmres`.
5. Prior study [`2026-05-17-horner-pure-li-autoresearch-negative.md`](./2026-05-17-horner-pure-li-autoresearch-negative.md).

---

## 3. Hypothesis + experiments

### H1 — Vec-FMA blocked codegen closes pure_li gap (not novel algorithm)

**Hypothesis:** In-tree blocked IKJ+vec-FMA brings `matmul_blocked` Li/cpp ≤ 1.2× without changing the numerical recipe.

**Result:** **Partial** — local **1.229×** (cpp 0.0083 s, li 0.0102 s); checksum `1288460.7563999966` matches oracle. ~3% gap → PH-7e tile/register polish, not new blocking scheme.

### H2 — Novel blocking / Horner reordering

**Result:** **Rejected** — BLIS IKJ+BK=64 and classical Horner are SOTA; invention adds proof debt without measured win.

### H3 — Dashboard stale rows

**Result:** `matmul_naive` local **1.056×** green vs dashboard **1.333×** red; `num_gmres` not runnable in lic tier-1 harness. Ingest refresh required.

---

## 4. Quality table

| Axis | Before (dashboard) | After (local @ 4d9112ce) | Verdict |
|------|-------------------|--------------------------|---------|
| Speed matmul_blocked | 1.549× red | 1.229× red | Improved; still open |
| Speed matmul_naive | 1.333× red | 1.056× green | Ingest stale |
| Speed horner_pure_li | 0.750× green | 2.600× red (local) | PH-7e scalar; dashboard may differ by host |
| Accuracy | — | matmul checksum pass | **Pass** |
| Novel invention | — | None | **Negative (valuable)** |

---

## 5. Commands

```bash
cd lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_blocked,matmul_naive --runs 2
python3 bench.py --tier 1 --only horner_pure_li --runs 5

cd benchmarks
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-autoresearch-proactive-sweep-v8.md
```

---

## 6. Status

**Closed — negative autoresearch.** No tier-1 red row requires a novel numerical method. Ship PH-7e codegen polish + ingest refresh via **bench_improver** / **code_implementer**.
