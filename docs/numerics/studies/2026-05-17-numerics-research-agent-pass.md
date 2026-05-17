# Agent pass: numerics research cycle (2026-05-17)

**Skill:** `research-li-numerics`  
**Mode:** Mode A — SOTA survey (no novel algorithms)  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Evidence:** this file + linked studies satisfy **`docs/numerics/`** gate with bench ids and repro commands.

---

## Executive summary

- Single **red** row: **`horner_pure_li`** (~88.8× vs cpp, tier 1, `pure_li`) — PH-**5b**/**7e** gap is compiler-side (scalar FMA/vectorization), not recipe novelty.
- **Seven** **green** rows sit **above 1.0×** cpp (1.003–1.035×): `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`, `heat_equation_2d`, `reduce_sum` — mostly harness/oracle parity and LLVM autovec on shared C, not wrong physics.
- SOTA anchors: Numerical Recipes / Hairer symplectic / LeVeque FD / Eigen–BLIS GEMM + PETSc operator long-read for future scalable PDE (see §2).
- **lic** path: **PH-7e** + **G-math** first (FMA, counted loops, reduction vectorization); **G-par** later for tiled/`@parallel` outer loops — coordinate with **bench_improver**.
- **Do not:** relax `threshold_ratio_cpp`; hide errors with `sorry`/`unsafe`; open novel-method PRs here → **`numerics-autoresearch`**.
- Catalog/data gaps: **`tier0_stability`** + several tier-3/5 **unknown** rows — **deferred** to measurement harness work ([`benchmark-failures-report.sh`](#6-repro--bench-dashboard)).
- Ecosystem preflight recommends closing **failing PR CI** (e.g. **benchmarks#15**) before stacking new catalog work.
- Full drill-downs: [`2026-05-17-horner-pure-li-codegen.md`](./2026-05-17-horner-pure-li-codegen.md), [`2026-05-17-near-limit-tier12-sota.md`](./2026-05-17-near-limit-tier12-sota.md).

---

## 1. SOTA survey — Learned from (2–4)

| # | Reference | What we take |
|---|-----------|----------------|
| 1 | [Numerical Recipes §5.3 — Polynomials and rational functions](https://numerical.recipes/book/bookcpdf/c5-3.pdf) | Horner / multiply-add recurrence baseline — maps **`horner_pure_li`**. |
| 2 | [Eigen — efficient matrix product](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) + [BLIS kernel how-to](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md) | Blocked GEMM + micro-kernel discipline — maps **`matmul_blocked`**, **G-math**. |
| 3 | Hairer–Lubich–Wanner — *Geometric Numerical Integration* ([Springer SSCM](https://link.springer.com/book/10.1007/3-540-30666-8)) | Symplectic integrators — maps **`nbody_gravity`**, **`double_pendulum`**, **`harmonic_oscillator_chain`**. |
| 4 | LeVeque FDM book ([site](https://faculty.washington.edu/~rjl/fdmbook/)) + [PETSc manual](https://petsc.org/main/manual/) | Explicit CFL stencils now; PETSc KSP/SNES/DM stack for future **G-par** / tier-3 implicit PDE — maps **`wave_equation_1d`**, **`heat_equation_2d`**. |

---

## 2. Map to Li pillars

| ID | Role |
|----|------|
| **PH-5b** | Tier-1/2 competitive posture vs cpp oracle; **`horner_pure_li`** is the headline red proof debt. |
| **PH-7e** | Math → SIMD / FMA / loop-vectorize; applies to **`horner_pure_li`**, **`reduce_sum`**, future pure-Li physics. |
| **G-math** | Peephole FMA, reduction patterns, eventual blocked GEMM in Li surface and codegen. |
| **G-par** | Outer parallel loops / PETSc-class scaling — **after** math lowering; secondary for current ~3% “green but slow” rows. |

---

## 3. Implementation path (**lic** — contracts + bench evidence)

1. **P0:** FMA fusion + countable loop form for pure-Li microkernels (`horner_pure_li` study §4).
2. **P1:** Fairness — align `bench.py` / `LI_EXTRA_C` flags with cpp (near-limit study §4).
3. **P2:** Reduction / dot / sum vectorization shared with simd-dot work (**`reduce_sum`**).
4. Every change: **`lic`** tests + harness before/after **`ratio_vs_cpp`**; no catalog threshold edits without human approval.

---

## 4. Recommended issues / PRs (titles + repos)

| Priority | Repo | Title (proposed) |
|----------|------|-------------------|
| P0 | **lic** | `fix(codegen): PH-7e FMA + loop metadata for pure-Li Horner microbench (horner_pure_li)` |
| P0 | **benchmarks** | `fix(ci): restore green CI for tier-2 catalog PRs (unblock dashboard ingest)` — *align with org preflight failed PRs* |
| P1 | **lic** | `perf(math): reduction / matmul wrapper parity for near-limit tier-1 rows (reduce_sum, matmul_blocked)` |
| P1 | **benchmarks** | `chore(catalog): resolve tier0_stability path or remove gap row (master-plan-gap)` |
| P2 | **roadmap** / **benchmarks** | `docs: PETSc vs Li physics packages — when to add implicit PDE tier (evidence from numerics studies)` |

Do **not** merge PRs from this agent pass without human review.

---

## 5. Deferred items

- **`tier0_stability`**, **`lip_smoke`**, **`lit_smoke`**, **`keepalive_pipelining`**, **`static_small`** — unknown / no ratio until harness + ingest path is wired.
- Novel integrators, implicit solvers, or AMG — **autoresearch** + new algorithm note, not this Mode A cycle.
- **FFT** micro-bench and **`std` I/O** modules flagged by ecosystem explorer — **PH-IO** / catalog expansion, separate issues.

---

## 6. Repro — bench & dashboard

**Mandatory dashboard:** https://li-langverse.github.io/benchmarks/

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh
```

**Affected bench ids:** `horner_pure_li` (red); `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`, `heat_equation_2d`, `reduce_sum` (green, >1.0× cpp).

```bash
export LIC_ROOT=/path/to/lic
cd "$LIC_ROOT/benchmarks/harness"
python3 bench.py horner_pure_li --release
# Optional per-row sweeps — see linked studies for full loops

cd /path/to/benchmarks/repo
LIC_ROOT=/path/to/lic ./scripts/ingest/ingest-lic.sh
```

**Evidence checklist:**

```bash
cd benchmarks
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-17-numerics-research-agent-pass.md
```

---

## 7. Quality / regression posture

Improve **speed** only with **stability** (tier-0), **accuracy** vs oracle, and **visual** sanity untouched — see [research-methodology.md](../research-methodology.md).
