# Study: tier-1 matmul autoresearch (negative result)

**Date:** 2026-05-30  
**Mode:** Autoresearch (B) → closed as negative  
**Target:** `matmul_naive`, `matmul_blocked` (PH-5b, PH-7e) — yellow tier-1 rows (~1.22–1.24× cpp)  
**Agent:** autoresearch proactive pass (li-langverse)  
**north_star_fit:** blazingly-fast pillar — PH-5b/7e pure-Li `@` matmul; proof pillar blocks novel perf claims until loop witness closes (lic#472)

---

## 1. Hypothesis

| ID | Hypothesis | Falsifiable metric |
|----|------------|-------------------|
| H1 | A **novel** Li-specific matmul scheme (non-BLAS blocking, custom accumulation order, or Strassen-class shortcut) closes the tier-1 gap without PH-7e SIMD/tile lowering. | `ratio_vs_cpp` ≤ 1.2 for `matmul_naive` and `matmul_blocked` with checksum parity vs cpp oracle. |
| H2 | Li `@` on 512×512 already matches cpp blocked IKJ+micro-kernel performance when work is observable (volatile sink). | Local + dashboard `wall_time` Li/cpp ≤ 1.2 at N=512 blocked. |

---

## 2. SOTA survey (Mode A — sufficient; see also 2026-05-17 numerics pass)

**Problem:** Dense GEMM C = A·B for N ∈ {256, 512}; blocked variant uses B_k = 64 tiles.

**Learned from:**

1. **BLIS / Goto algorithm** — cache-blocked IKJ with register micro-kernels ([BLIS how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md)).
2. **Eigen product expressions** — lazy fusion + blocking in reference cpp cores ([Eigen topic](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html)).
3. **Li codegen** — `ArrayMatMul2DF64` emits IKJ loops or unrolled path at kUnrollMax=24 (`emit.cpp:1175-1194`); optional `llvm.fmuladd` when not numerically-stable mode.
4. **Proof gap (cycle 19)** — tier-1 matmul loop lacks `witness_matmul*` / `matmul_loop_eval` (lic#472); perf certificate is advisory until closed.

**Conclusion:** Published blocked GEMM is the correct recipe. The cpp oracle in `matmul_blocked_core.c` already implements 3-level blocking; Li bench uses a **single** `C = A @ B` without source-level tiles — gap is **codegen + oracle parity**, not missing numerics invention.

---

## 3. Experiments (local repro, 2026-05-30)

```bash
cd ../lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_naive,matmul_blocked --runs 2
```

**Median wall_time (local linux, release):**

| bench id | cpp | li | Li/cpp |
|----------|-----|-----|--------|
| matmul_naive (N=256) | 0.0019 s | 0.0021 s | **1.11×** |
| matmul_blocked (N=512) | 0.0082 s | 0.0133 s | **1.62×** |

**Dashboard ingest (2026-05-30T09:25Z, linux):**

| bench id | cpp | li | ratio_vs_reference | status |
|----------|-----|-----|-------------------|--------|
| matmul_naive | 0.0018 s | 0.0022 s | **1.22×** | yellow |
| matmul_blocked | 0.0086 s | 0.0107 s | **1.24×** | yellow |

Verify checksums pass (`--verify`): naive ≈ 161055.19, blocked ≈ 1288460.76 — accuracy locked.

**Codegen observation:** 256×256 and 512×512 force IKJ loop path (>24); LLVM autovec on cpp blocked triple loops vs scalar/store-heavy Li `@` lowering explains blocked gap locally (1.62×).

---

## 4. Novel ideas considered (not pursued)

| Idea | Why rejected |
|------|--------------|
| Strassen / Winograd shortcuts | Worse constants at N=256–512; accuracy/stability trade; not SOTA for tier-1 |
| Li-only “fused LUT init + matmul” IR | Harness already separates init from timed `@`; no measured win |
| Manual 64×64 blocking purely in Li source | **SOTA (BLIS)**, not novel — belongs in **bench_improver** / `@` tile lowering (PH-7e), not autoresearch |
| `@vectorized` inner-k loops without MIR proc tags | PH-7d partial; needs compiler design + proof review |
| Randomized / mixed-precision matmul | Violates oracle parity + proof-before-perf |

---

## 5. Quality table (no improvement shipped)

| Axis | Before | After autoresearch | Verdict |
|------|--------|-------------------|---------|
| Speed (naive) | 1.22× yellow | No novel kernel shipped | **No improvement** |
| Speed (blocked) | 1.24× yellow | No novel kernel shipped | **No improvement** |
| Accuracy | checksum pass | unchanged | **Locked** |
| Stability | tier-0 N/A micro | — | — |
| Provability | loop witness open (lic#472) | unchanged | **Blocks perf certificate** |

---

## 6. Recommended follow-up (not autoresearch)

| Priority | Repo | Action |
|----------|------|--------|
| P0 | **lic** | **bench_improver / PH-7e:** cache-tile `@` matmul or align Li blocked bench with cpp 3-level blocking in source |
| P0 | **lic** | Merge [lic#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore when CI green |
| P1 | **lic** | lic#472 — `witness_matmul2d_ijk_loop` + pilot `matmul_loop_eval` before claiming proved fast GEMM |
| P2 | **lic** | `ml_conv2d_forward`, `num_gmres` — harness/catalog gaps; defer until paths exist (ecosystem audit catalog gaps) |

Do **not** relax `threshold_ratio_cpp` in `catalog.toml`.

---

## 7. Commands

```bash
cd /path/to/lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_naive,matmul_blocked --runs 3

cd /path/to/benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-matmul-tier1-autoresearch-negative.md
```

---

## 8. Status

**Closed — negative autoresearch.** Tier-1 matmul yellow rows are **codegen-bound** (PH-7e blocking/SIMD + optional source blocking parity), not evidence that a novel numerical method is required. Prior horner negative ([2026-05-17](./2026-05-17-horner-pure-li-autoresearch-negative.md)) pattern holds: measure real work first, then codegen — do not invent new GEMM mathematics.
