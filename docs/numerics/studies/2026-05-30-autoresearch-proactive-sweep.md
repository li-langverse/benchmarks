# Study: autoresearch proactive sweep (2026-05-30)

**Date:** 2026-05-30  
**Mode:** Autoresearch (B) → **closed negative** (no novel algorithm shipped)  
**Target:** tier-1 dashboard reds — focus pure_li codegen-bound rows  
**Agent:** autoresearch proactive pass (`autoresearch-1780115445230`)  
**north_star_fit:** PH-5b, PH-7e

---

## 1. Problem framing

Ecosystem audit (2026-05-29 ingest) lists **6 red** tier-1 rows. Autoresearch runs **after** numerics_researcher when SOTA is insufficient. This pass asks: do any reds require **novel** numerics, or are they codegen/harness/ingest debt?

---

## 2. SOTA survey (Mode A)

| Bench | Closest published method | Li column variant | Autoresearch? |
|-------|-------------------------|-------------------|---------------|
| matmul_blocked | BLIS blocked GEMM (IKJ, BK=64) | pure_li (MIR `mm_blocked_512`) | **No** — marginal PH-7e emit (~1.256×) |
| matmul_naive | Classical IKJ GEMM | pure_li | **No** — local 1.00×; ingest stale |
| num_gmres | Saad GMRES | shared_c_kernel | **No** — local 1.00×; ingest stale |
| ml_conv2d / ml_mlp_* | im2col + GEMM / MLP layers | algo_registry (li-math) | **No** — wrong repo/agent |
| horner_pure_li | Horner FMA chain | pure_li | **Closed** — local 0.80× green |

**Learned from:**

1. [BLIS kernel how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) — micro-kernel + blocking for `matmul_blocked`.
2. [Eigen — efficient matrix product](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) — `@` / MIR lowering target.
3. Saad, *Iterative Methods for Sparse Linear Systems* — GMRES baseline for `num_gmres`.
4. Prior study [`2026-05-17-horner-pure-li-autoresearch-negative.md`](./2026-05-17-horner-pure-li-autoresearch-negative.md) — DCE harness bug; lexer fix landed.

---

## 3. Hypothesis + experiments

### H1 — Vec-FMA blocked codegen closes pure_li gap (not novel algorithm)

**Hypothesis:** In-tree `ArrayMatMulBlocked2DF64` + `emit_matmul2d_blocked_ijk` vec-FMA brings `matmul_blocked` Li/cpp ≤ 1.2× without changing the numerical recipe.

**Metric:** median `wall_time` Li/cpp, checksum vs C oracle.

**Local results (lic `c6e9ca7d`, 2026-05-30):**

| lang | wall_time |
|------|-----------|
| cpp | 0.0090 s |
| li | 0.0113 s |
| **ratio** | **1.256×** |

**Verdict:** Hypothesis **partially confirmed** — MIR hook + vec-FMA emit works (checksum pass) but **5% above threshold**. Route to **code_implementer / bench_improver** micro-opt, not autoresearch invention.

### H2 — Novel tile schedule

**Hypothesis:** Non-standard tile ordering beats BLIS IKJ for N=512 BK=64.

**Verdict:** **Rejected** — no accuracy/stability axis gain; adds proof surface. SOTA sufficient.

---

## 4. Quality table

| Axis | Before (dashboard) | Local spot-check @ c6e9ca7d | After autoresearch | Verdict |
|------|-------------------|----------------------------|-------------------|---------|
| matmul_blocked speed | 1.549× red | 1.256× red | No code shipped | Open → PH-7e micro-opt |
| matmul_naive speed | 1.333× red | 1.000× green | No code shipped | Ingest stale |
| num_gmres speed | 1.400× red | 1.000× green | N/A shared kernel | Ingest stale |
| horner_pure_li speed | 0.750× green | 0.800× green | N/A | Pass |
| Novel algorithm | — | — | None | **Negative (valuable)** |

**Locked axes:** accuracy (checksum) — **pass** for matmul_blocked.

---

## 5. Plots / visuals

Tier-1 micro sweep — no physics GIF required. Speed evidence is tabular (§3). After ingest refresh:

```bash
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh
```

Dashboard row: `matmul_blocked` on https://li-langverse.github.io/benchmarks/ (stale until ingest).

---

## 6. Commands

```bash
cd lic && ./scripts/build.sh
cd lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_blocked --runs 3
python3 bench.py --tier 1 --only matmul_naive --runs 3
python3 bench.py --tier 1 --only num_gmres --runs 3

cd benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-autoresearch-proactive-sweep.md
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
```

---

## 7. Status

**Closed — negative autoresearch (no novel method).** Actionable follow-up: **PH-7e micro-opt** on `matmul_blocked` vec-FMA tile (~5% gap), **ingest refresh** to clear stale dashboard reds, re-run autoresearch only if pure_li remains >1.2× post-codegen.
