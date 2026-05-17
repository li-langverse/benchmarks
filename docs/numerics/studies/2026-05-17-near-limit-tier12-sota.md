# Study: Near-limit tier-1 / tier-2 rows (green above 1.0× cpp)

**Date:** 2026-05-17  
**Mode:** SOTA survey (Mode A) — benchmark harness / codegen parity  
**Affected catalog ids:** `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`, `heat_equation_2d`, `reduce_sum`  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Red sibling:** `horner_pure_li` is handled in [2026-05-17-horner-pure-li-codegen.md](./2026-05-17-horner-pure-li-codegen.md) — do **not** relax `threshold_ratio_cpp`.

---

## 1. Problem summary

Ingest snapshot `2026-05-16T15:10:14Z` shows **seven** benchmarks still classified **green** but with `ratio_vs_cpp` marginally above 1.0 (1.003–1.035×). Tier-2 physics kernels use **`LI_EXTRA_C`** shared oracles aligned with Numerical Recipes / standard texts; disparity vs cpp is predominantly **compile/link/LTO parity** and **`clang -O3` autovec** on the oracle C path, **not** missing science on the discrete equations.

Goal: shave wall time toward **≤1.0×** (and stay under **`threshold_ratio_cpp = 1.2`**) using **contracts + benchmark evidence**, without novel discretizations (defer **autoresearch**).

---

## 2. SOTA survey — Learned from

| # | Reference | What we take |
|---|-----------|---------------|
| 1 | [Numerical Recipes Ch. 5 — Polynomial evaluation / recursion](https://numerical.recipes/book/bookcpdf/c5-3.pdf) (& related chapters on ODE/PDE scaffolding) | Baseline flops structure for recurrence-style microkernels and textbook integrator patterns echoed in benches. |
| 2 | [Eigen — Topic: Writing efficient matrix product code](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) + [BLIS — kernels how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) + [GEMM tutorials (how-to-optimize-gemm)](https://github.com/flame/how-to-optimize-gemm/wiki) | Blocked register-resident GEMM mirrors **`matmul_blocked`**; informs cache blocking / micro-kernel shape if Li ever lowers pure GEMM (**PH-7e**, **G-math**). |
| 3 | E. Hairer, C. Lubich, G. Wanner — *Geometric Numerical Integration* ([Springer SSCM Vol. 31](https://link.springer.com/book/10.1007/3-540-30666-8)) | Leapfrog / Störmer-Verlet lineage for **`nbody_gravity`**, **`double_pendulum`**, **`harmonic_oscillator_chain`** — preserve symplectic structure when tightening timing experiments. |
| 4 | R. J. LeVeque — *Finite Difference Methods for ODE and PDEs* ([book site](https://faculty.washington.edu/~rjl/fdmbook/)) + PETSc [Users Manual — KSP / SNES / time stepping context](https://petsc.org/main/manual/) | Explicit CFL-stable stencils (**`wave_equation_1d`**, **`heat_equation_2d`**); scalable implicit path for future tiers lives in PETSc-tier methodology (**G-par**, future packages). |

**Complement:** Stiff IVPs and adaptive steps are canonically documented in [SUNDIALS / CVODE](https://sundials.readthedocs.io/en/latest/cvode/) — reserve for tier-3+ stiff extensions, **not** required to explain current ~3% deltas on explicit benches.

---

## 3. Map to Li pillars

| ID | Role for near-limit rows |
|----|---------------------------|
| **PH-5b** | Org posture: cpp reference is authoritative; Li must remain within catalog threshold via fair release builds (LTO, same flags, observable sinks). |
| **PH-7e** | When kernels are pure Li (later physics packages), SIMD / FMA lowering and counted-loop vectorization close gaps; today most rows are oracle-driven. |
| **G-math** | GEMM blocking theory applies to **`matmul_blocked`**; SIMD horizontal reductions apply to **`reduce_sum`** alongside Horner-track work. |
| **G-par** | Outer-loop tiling (`@parallel` / Kokkos-style policies — see org explorer) applies after math surface + codegen; PETSc DM/KSP stacks inform future distributed PDE rows. |

---

## 4. Implementation path (**lic** + harness)

**P0 — measurement fairness (coordinate `bench_improver`)**

1. Align **`LI_EXTRA_C`** compile flags with cpp oracle (`-ffast-math`, LTO if cpp uses it, identical `optimization` knob in `bench.py`).
2. Ensure **volatile / checksum sinks** mirror across languages so LLVM cannot DCE hot paths (lesson from **`horner_pure_li`** investigations).

**P1 — compiler (**lic**, only where Li code is hot)**

3. **`reduce_sum`** — expose reduction to LLVM **`loop-vectorize`** / widen loads (same playbook as simd dot inner loops).
4. **`matmul_blocked`** — verify Li wrapper emits tight nested loops comparable to cpp; defer vendor BLAS; keep blocked loop order NR/Eigen-compatible.

**P2 — physics (later pure-Li packages)**

5. Preserve **Hairer/LeVeque** discrete properties when rewriting integrators — add **tier-0** drift checks before chasing wall time.

**Forbidden:** weakening **`threshold_ratio_cpp`**, **`sorry`**/**`unsafe`** shortcuts, unstability-prone “fixes”.

---

## 5. Bench → recipe map (Modes A linkage)

| Catalog id | ratio (ingest) | SOTA anchoring |
|------------|----------------|----------------|
| `matmul_blocked` | 1.035× | Eigen/BLIS blocked GEMM |
| `nbody_gravity` | 1.035× | Leapfrog + softening; MD literature |
| `double_pendulum` | 1.032× | Symplectic splitting (Hairer GNINT family) |
| `wave_equation_1d` | 1.024× | LeVeque hyperbolic FD Ch. introductory material |
| `harmonic_oscillator_chain` | 1.018× | Same symplectic chain as NR-style molecular updates |
| `heat_equation_2d` | 1.004× | Explicit heat / Jacobi smoothing — LeVeque parabolic FD |
| `reduce_sum` | 1.003× | SIMD reduction / clang autovec parity |

---

### Quality axes (speed vs locked regression posture)

Improvements are acceptable only where **speed** rises and **stability**, **accuracy** (orbit/energy morphology vs oracle), and **tier-0** cleanliness do **not regress**. Closing a wall_time gap via different FP reordering requires a documented **`--verify`** policy (parity with cpp within stated tolerances), not silent fast-math drift.

---

### Stability (tier-0) and visualization evidence

Tier-2 physics benches must keep existing **tier-0** / checksum gates when timing flags move. Generate plots and GIFs via the harness + ingest path so reviewers can sanity-check morphology:

```bash
cd benchmarks
LIC_ROOT=/path/to/lic ./scripts/render-benchmark-visuals.sh
```

Use dashboard bars + optional `data/visuals/latest/*.png|*.gif` for human review (**plot** parity with prior runs).

---

## 6. Repro commands (performance / bench tooling)

Interpret `ratio_vs_cpp` from harness JSON / ingest `summary.json` against catalog `threshold_ratio_cpp`. Compare **`wall_time`** medians across languages before changing compiler knobs.

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh

# Per-bench (requires built lic checkout)
export LIC_ROOT=/path/to/lic
cd "$LIC_ROOT/benchmarks/harness"
for id in matmul_blocked nbody_gravity double_pendulum wave_equation_1d \
          harmonic_oscillator_chain heat_equation_2d reduce_sum; do
  python3 bench.py "$id" --release
done

cd /path/to/benchmarks/repo
LIC_ROOT=/path/to/lic ./scripts/ingest/ingest-lic.sh
```

**Evidence checklist:**

```bash
cd benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-17-near-limit-tier12-sota.md
```

---

## 7. Follow-up

- [ ] **benchmarks**: keep dashboard ingest fresh after harness flag alignment.
- [ ] **lic**: issue/PR per bench cluster with **study link** + `bench.py` transcripts.
- [ ] Separate **PETSc-aligned** roadmap issue when tier-3 implicit PDE work starts — do not conflate with current 1–4% deltas.
