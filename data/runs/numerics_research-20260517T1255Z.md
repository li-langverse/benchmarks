# Numerics researcher digest — 2026-05-17T12:55Z

**Agent:** `numerics_researcher`  
**Skill:** `research-li-numerics`  
**Preflight:** `./scripts/benchmark-failures-report.sh` (`generated_at: 2026-05-16T15:10:14Z` ingest snapshot)  
**Dashboard:** https://li-langverse.github.io/benchmarks/

---

## Executive summary

- **One red catalog row:** **`horner_pure_li`** (~**88.8×** cpp) — pure-Li Horner recurrence; pillars **PH-5b**, **PH-7e**; codegen/FMA/`llvm.fmuladd` + countable loop metadata (**G-math**), **not** `threshold_ratio_cpp` edits.
- **Seven near-limit greens:** `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`, `heat_equation_2d`, `reduce_sum` at **1.003–1.035×** cpp — overwhelmingly **oracle + link/LTO parity** and autovec fairness vs cpp; textbook SOTA aligns with Numerical Recipes, Hairer GNINT lineage, LeVeque FD, Eigen/BLIS GEMM folklore, PETSc-class future implicit stacks.
- **Learned-from URLs** (survey): Numerical Recipes [Ch. 5 PDF](https://numerical.recipes/book/bookcpdf/c5-3.pdf); Eigen [efficient matrix product](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html); BLIS [kernels doc](https://github.com/flame/blis/blob/master/docs/KernelsHowTo.md); [how-to-optimize-gemm](https://github.com/flame/how-to-optimize-gemm/wiki); Hairer GNINT [Springer monograph](https://link.springer.com/book/10.1007/3-540-30666-8); LeVeque [FDM book](https://faculty.washington.edu/~rjl/fdmbook/); PETSc [Users Manual](https://petsc.org/main/manual/); SUNDIALS [CVODE docs](https://sundials.readthedocs.io/en/latest/cvode/).
- **`G-par`** for these rows means outer tiling / Kokkos-style execution + future PETSc DM/KSP tiers — secondary until **PH-7e** pure-Li and harness parity stabilize **ratio_vs_cpp**.
- **Evidence docs:** [`docs/numerics/studies/2026-05-17-horner-pure-li-codegen.md`](../docs/numerics/studies/2026-05-17-horner-pure-li-codegen.md) (Horner/red), [`docs/numerics/studies/2026-05-17-near-limit-tier12-sota.md`](../docs/numerics/studies/2026-05-17-near-limit-tier12-sota.md) (near-limit cluster); **`python3 scripts/numerics-evidence-checklist.py`** passes on the latter.
- **Mandatory repro:** `./scripts/benchmark-failures-report.sh` locally; ingest via `LIC_ROOT=… ./scripts/ingest/ingest-lic.sh`; tier-2 **plots/GIF**: `./scripts/render-benchmark-visuals.sh`.
- **Forbidden:** weakening **`threshold_ratio_cpp`**, **`sorry`/`unsafe`** for speed-only wins, novel methods without **autoresearch** gates.

---

## Recommended issues / PRs

| Kind | Repo | Title (suggested) |
|------|------|-------------------|
| Issue | **lic** | `horner_pure_li`: PH-7e FMA + anti-DCE checksum (coordinate bench_improver) — link study `2026-05-17-horner-pure-li-codegen.md` |
| Issue | **lic** | Near-limit tier-2: LI_EXTRA_C / `clang` flags + LTO parity vs cpp oracle — study `2026-05-17-near-limit-tier12-sota.md` |
| PR | **lic** | `perf(codegen): PH-7e fused FMA pattern for multiply-add recurrence` (+ `bench.py` transcripts) |
| PR | **lic** | `chore(bench): align cpp/Li oracle release flags & sinks for near-limit rows` |
| PR | **benchmarks** | `docs(numerics): near-limit tier-12 SOTA study + studies index` (this artifact) |

*Do **not** self-merge PRs.*

---

## Deferred

| Item | Why |
|------|-----|
| Novel integrators / preconditioners | **autoresearch** + algorithm note |
| FFT micro-catalog row | Explorer P2; no red row |
| PETSc-backed distributed tiers | Org roadmap pillar “fast”; needs proof path + packages |
| `tier0_stability` / lis/lip smoke **unknown** | Separate catalog/harness hygiene — not numerics-core |
| Threshold-only “fixes” | Policy-forbidden |
