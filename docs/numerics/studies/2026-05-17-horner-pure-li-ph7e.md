# Study: `horner_pure_li` — PH-7e pure-Li codegen (SOTA survey)

**Date:** 2026-05-17  
**Mode:** SOTA survey (Mode A)  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Status:** red — **88.82×** cpp (`li` 0.9415 s vs cpp 0.0106 s, ingest 2026-05-16)

---

## Problem

Tier-1 micro-benchmark `horner_pure_li` evaluates a scalar recurrence 5M times:

```text
acc = 0; for i in 0..5_000_000: acc = acc * x + 1.0   (x = 1.1)
```

- **Li path:** `lic/benchmarks/tier1_micro/horner_pure_li/li/main.li` — pure `.li`, no `LI_EXTRA_C`
- **Oracle:** `common/horner_core.c` — same loop, `-O3 -march=native -ffast-math`
- **Invariant:** checksum via `li_horner_checksum()`; tier-0 not required for this micro row
- **Goal (org):** `ratio_vs_cpp` ≤ **1.2** per `catalog.toml`; long-term PH-7e proves math-only Li ≈ native

This is **not** a missing numerical method — cpp/rust/julia already match the C oracle. The gap is **compiler lowering**, not discretization choice.

---

## SOTA survey — Learned from

| # | Reference | What we take |
|---|-----------|--------------|
| 1 | **Numerical Recipes** Ch. 5 (polynomial evaluation); classic Horner form `((…)x + aₙ)x + …` | Recurrence `acc = acc*x + c` is the minimal FMA-shaped inner loop; no algorithm change needed — match NR Horner semantics in LLVM |
| 2 | [Golub & Van Loan, *Matrix Computations*](https://www.cs.utexas.edu/users/ivanov/LEAST_SQUARES/MatrixComp.pdf) §1.1 + LLVM LangRef on `fmuladd` | Map `acc*x + 1.0` to **fused multiply-add** when fast-math allows; avoid separate mul+add that blocks FMA formation |
| 3 | [Breese — Evaluating Polynomials](https://breese.github.io/2022/08/21/evaluating-polynomials.html); [Herumi — AVX-512 FMA poly eval](https://zenn.dev/herumi/articles/poly-evaluation-by-fma?locale=en) | Horner is **sequential** (latency-bound); SOTA on modern CPUs = FMA + modest unroll (4–8) to hide 4-cycle FMA latency — **not** Estrin/Dorn unless vectorizing coefficients (out of scope for scalar bench) |
| 4 | **Eigen** `PolynomialEvaluator` / `evalHorner` pattern ([eigen/doc/TutorialAdvancedInitialization.md](https://eigen.tuxfamily.org/dox/)) and **BLIS** philosophy (isolate hot micro-kernel, compile rest) | Keep hot loop in Li source; **lic** must emit a single tight LLVM loop comparable to `horner_core.c`, not interpreter dispatch |

**Not in scope (→ autoresearch):** Estrin/Dorn reorderings, SIMD coefficient batches, or novel reassociation that changes FP semantics without proof.

---

## Stability / accuracy

- Non-stiff scalar recurrence; no CFL. With `-ffast-math`, cpp and Li should document **same reordering policy** (FMA contraction).
- Locked axis: **bitwise or tight FP parity** with oracle on `--verify` checksum before claiming green speed.
- Do **not** weaken `threshold_ratio_cpp` or skip verify to go green.

---

## Map to Li tracks

| Track | Role for this bench |
|-------|---------------------|
| **PH-5b** | Harness + dashboard ingest; oracle `horner_core.c` |
| **PH-7e** | **Primary** — pure-Li `while` + `BinOpFloat` → LLVM loop with FMA, no interpreter hot path |
| **G-math** | Future: `@` / `dot` SIMD MIR; horner is scalar float loop today — still exercises float codegen pipeline |
| **G-par** | N/A (serial micro-bench) |

**Master plan:** Phase **7e** — “Math → SIMD MIR; tier-1 Li sources math-only; lowering proved or documented” ([lic master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)).

---

## Implementation path (lic)

**Proof path (bench_improver coordinates):**

1. **Confirm build mode** — `bench.py` `li_pure=True` must use `lic build` release, not interpreter loop over bytecode (`benchmarks/results/README.md`: pure_li until 7e matures).
2. **MIR → LLVM** for `while` + float `*`/`+`:
   - Induction variable `i` → canonical `phi` + icmp exit
   - `acc = acc * x + 1.0` → `llvm.fmuladd` or `fmul`+`fadd` with `fast` flags matching harness `-ffast-math`
   - `noinline` only on `main` boundary if needed; **do not** mark inner loop cold
3. **Regression tests** — `li-tests/` micro: compile `horner_pure_li/li/main.li`, run `--verify` checksum vs cpp
4. **Evidence** — re-run:
   ```bash
   cd lic/benchmarks/harness && python3 bench.py --tier 1 --bench horner_pure_li --runs 5
   cd benchmarks && LIC_ROOT=../li ./scripts/ingest/ingest-lic.sh
   ./scripts/benchmark-failures-report.sh
   python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md
   ```
5. **Target:** `ratio_vs_cpp` ≤ 1.2 without catalog threshold change

**Optional lic PR title:** `perf(codegen): PH-7e — lower horner_pure_li float loop to FMA LLVM (tier-1)`

---

## Quality table (before — current ingest)

| Axis | Before | Target | Regression risk |
|------|--------|--------|-----------------|
| Stability | N/A (micro) | checksum match cpp | FP fast-math drift |
| Speed | **88.82×** cpp | ≤ **1.2×** | — |
| Accuracy | checksum oracle | unchanged | — |
| Memory | N/A | N/A | — |

---

## Visual / plots

Tier-1 micro — no GIF required; speed bar from dashboard ingest after fix.

```bash
cd benchmarks
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh
# PNG: data/visuals/latest/horner_pure_li_speed.png (when harness emits)
```

- Dashboard: https://li-langverse.github.io/benchmarks/ (micro chart `horner_pure_li`)
- Plot/GIF animation N/A for scalar micro-bench (physics tier-2 only)

---

## Verdict

- **Mode A sufficient** — adopt standard Horner/FMA lowering; no novel algorithm.
- **Blocker:** PH-7e / release codegen for pure `.li` float loops, not benchmarks-repo threshold.
- **Coordinate:** `bench_improver` for harness verification; **autoresearch** only if new IR fusion patterns are proposed beyond SOTA FMA+unroll.
