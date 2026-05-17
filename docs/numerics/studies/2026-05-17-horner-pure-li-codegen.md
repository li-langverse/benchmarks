# Study: `horner_pure_li` — pure-Li scalar loop vs cpp FMA/autovec

**Date:** 2026-05-17  
**Mode:** SOTA survey (Mode A) — no novel algorithm  
**Catalog:** `horner_pure_li` (`benchmarks/catalog.toml`, tier 1, `variant = pure_li`)  
**Dashboard:** https://li-langverse.github.io/benchmarks/ (micro chart, status **red**)  
**Coordination:** bench_improver / lic compiler (PH-7e); do not weaken `threshold_ratio_cpp`

---

## 1. Problem summary

Evaluate a degree-0 Horner-style recurrence for fixed `x = 1.1` over `5_000_000` steps:

\[
\text{acc} \leftarrow \text{acc} \cdot x + 1
\]

This is the canonical **polynomial / rational function** micro-kernel from Numerical Recipes §5.3 (nested multiply-add). The **pure_li** variant compiles only `li/main.li` (no `LI_EXTRA_C`); cpp/rust/julia call the shared oracle `common/horner_core.c`.

**Failure mode (speed, not stability):** Li release wall time is dominated by **unfused scalar** `fmul` + `fadd` per iteration and lack of LLVM loop-vectorization on the hand-lowered `while` CFG — not by numerical blow-up (same FP semantics as oracle).

---

## 2. SOTA survey — Learned from

| # | Reference | What we take |
|---|-----------|--------------|
| 1 | [Numerical Recipes §5.3 — Polynomials and rational functions](https://numerical.recipes/book/bookcpdf/c5-3.pdf) | Horner nested form `acc = acc*x + c`; 2 flops/step; baseline algorithm for tier-1 micro. |
| 2 | [LLVM loop vectorizer / FMA](https://llvm.org/docs/Vectorizers.html) + Hal Finkel, *LLVM Autovectorization* ([slides](https://llvm.org/devmtg/2012-04-12/Slides/Hal_Finkel.pdf)) | `llvm.fmuladd` / `-ffast-math` + `loop-vectorize` on tight reduction loops; target for **PH-7e** codegen. |
| 3 | H. Murai, *Evaluating Polynomials Using AVX-512 FMA* ([Zenn / herumi](https://zenn.dev/herumi/articles/poly-evaluation-by-fma?locale=en)) | Broadcast `x`, unrolled FMA chains for **many** `x` values; informs future `@vectorized` on math surface, not required for this scalar bench. |
| 4 | [Eigen GEMM blocking](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) + [BLIS micro-kernels](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) | Cache-blocked `mc×kc×nc` panels + register micro-kernel — maps to near-threshold **`matmul_blocked`** (1.035× cpp), separate from Horner but same **G-math** / **PH-7e** track. |

**Stability:** No CFL/stiffness issue; FP associativity differs only if reordering without proved reduction contract (locked axis: **accuracy** — keep left-to-right or document `fast` contract).

---

## 3. Map to Li pillars

| ID | Role for this target |
|----|----------------------|
| **PH-5b** | Tier-1 competitive posture; `horner_pure_li` is the sole **red** row; proves pure-Li micro path before tier-2 physics. |
| **PH-7e** | Math → SIMD/parallel lowering: fuse `acc*x+1` → FMA; enable LLVM vectorize on counted loops; later `@vectorized` on math surface. |
| **G-math** | `BinOpFloat` today emits separate `fmul`/`fadd` (`emit.cpp`); need pattern reassociation + `ArrayDotF64`-style fast-math flags on reductions. |
| **G-par** | Not on critical path for scalar Horner; **matmul_blocked** / tier-2 near-threshold rows may need `@parallel` on outer tiles after **G-math** blocking lands. |

---

## 4. Implementation path (lic)

**Phase A — compiler (P0, unblocks ~88× gap)**

1. **FMA peephole / MIR fusion:** In `acc = acc * x + 1.0`, lower to one `llvm.fmuladd` when `--release` and fast-math allowed (`compiler/codegen/emit.cpp` `emit_fbinop` / stmt pattern in `mir/lower.cpp`).
2. **Counted `while` → LLVM `loop-vectorize`:** Emit `llvm.loop` metadata or canonical `for i in 0..<N` lowering so Clang/LLVM can unroll/vectorize the 5M-step body (today: scalar locals + back-edge).
3. **Sink call placement:** Keep `li_rt_sink_double` outside hot loop (already); verify no alloca traffic in loop via `opt -O3` IR diff vs `horner_core.c`.

**Phase B — math surface (P1, aligns with [li-math-linalg-surface](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-math-linalg-surface.md))**

4. Document Horner as reduction template in `li-tests/math_linalg/` once `sum` / fused multiply-add surface exists.
5. Optional: `horner_eval(coeffs, x)` in `li-std-math` — still pure-Li, no `LI_EXTRA_C`.

**Phase C — near-threshold tier-1/2 (coordinate bench_improver)**

| Bench id | ratio_vs_cpp | Oracle | SOTA lever |
|----------|--------------|--------|------------|
| `matmul_blocked` | 1.035 | shared C | Eigen/BLIS block sizes in `common/*`; Li wrapper only today |
| `nbody_gravity` | 1.035 | shared C | Leapfrog + softening; SUNDIALS CVODE for stiff path if Li owns integrator later |
| `double_pendulum` | 1.032 | shared C | Symplectic Verlet / Hairer Vol. II §VI.3 |
| `wave_equation_1d` | 1.024 | shared C | CFL explicit stencil; LeVeque FDM Ch. 2 |
| `harmonic_oscillator_chain` | 1.018 | shared C | Staggered leapfrog chain |
| `heat_equation_2d` | 1.004 | shared C | Jacobi/GS iteration count vs cpp |
| `reduce_sum` | 1.003 | shared C | SIMD horizontal sum (same pipeline as `simd_dot`) |

Do **not** relax `threshold_ratio_cpp = 1.2` in `catalog.toml`.

---

## 5. Quality table (before implementation)

| Axis | Before (ingest 2026-05-16) | Target | Locked? |
|------|----------------------------|--------|---------|
| **Stability** | Same recurrence as `horner_core.c`; no tier-0 row for this id | Match cpp checksum via `verify.py` when added | Yes |
| **Speed** | Li 0.9415 s vs cpp 0.0106 s (**88.82×**) | ≤ 1.2× cpp (`threshold_ratio_cpp`) | Primary improvement axis |
| **Accuracy** | Bitwise drift possible under fast-math reorder; document if FMA fused | ≤ 1 ulp vs strict scalar oracle on `--verify` | Yes |
| **Memory** | Stack locals only | No regression | — |

**Verdict:** Survey-only cycle — **speed** improvement required in **lic** codegen; **no catalog threshold change**.

---

## 6. Repro commands

```bash
# Dashboard status
cd benchmarks
./scripts/benchmark-failures-report.sh

# Local bench (requires built lic)
export LIC_ROOT=../li   # or path to lic checkout
cd "$LIC_ROOT/benchmarks/harness"
python3 bench.py horner_pure_li --release

# Ingest + dashboard data
cd benchmarks
LIC_ROOT=../li ./scripts/ingest/ingest-lic.sh

# Visuals (tier-2 physics; optional for this micro study)
LIC_ROOT=../li ./scripts/render-benchmark-visuals.sh
```

**Evidence checklist:**

```bash
cd benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-17-horner-pure-li-codegen.md
```

---

## 7. Visual / dashboard evidence

| Asset | Location |
|-------|----------|
| Live bar chart | https://li-langverse.github.io/benchmarks/ — micro → `horner_pure_li` |
| Summary JSON | `benchmarks/data/latest/summary.json` → `ratio_vs_reference: 88.8208` |
| Li source | `lic/benchmarks/tier1_micro/horner_pure_li/li/main.li` |
| Oracle | `lic/benchmarks/tier1_micro/horner_pure_li/common/horner_core.c` |

Post-fix: re-run ingest and link updated dashboard snapshot in lic PR.

---

## 8. Follow-up

- [ ] **lic** PR: FMA + loop metadata for `BinOpFloat` Horner pattern (**PH-7e**, **G-math**)
- [ ] **bench_improver:** Re-run `bench.py` + ingest; confirm green row without threshold tweak
- [ ] Human review: fast-math vs deterministic `--verify` policy for pure_li micros
- [ ] Separate issues for tier-2 **1.02–1.04×** rows (shared C tuning vs future pure-Li integrators)

**Novel methods:** defer to **autoresearch** agent — not needed for Horner (SOTA sufficient).
