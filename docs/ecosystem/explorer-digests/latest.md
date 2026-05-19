# Gap explorer digest — 2026-05-19

**Agent:** gap_explorer · **Skill:** explore-li-ecosystem  
**Research goal:** `ecosystem_gaps` · **north_star_fit:** ecosystem, hpc, web  
**Full digest:** [2026-05-19-explorer.md](./2026-05-19-explorer.md)

---

## Executive summary

- **PH-IO (P1 / easy):** `std.io`, `std.csv`, `std.summary`, `std.plot` still **missing** — benchmarks ingest imports them (**PH-IO-4/5/7**).
- **PH-7e (P1 / proof→fast):** `horner_pure_li` **red** (~88.8× cpp); catalog has only **1** `pure_li` row — expand proof surface.
- **HPC:** Kokkos/PETSc/FFTW/hypre/RAJA/HPX **missing**; Eigen/OpenMP/SUNDIALS **partial** — tier-2 physics leans on **shared_c_kernel**.
- **SOTA 2025–2026:** Eigen **5.0.0**; Kokkos **4.6.2**; PETSc **3.25** (Mar 2026); Chapel **2.4**; MLIR `omp` canonical loops.
- **PETSc+Kokkos:** GPU preconditioners + isolated sync — Li needs memory-space rules (**lic#28**).
- **Competitive:** Carbon **p4880** + Mojo **1.0b** — Li wins on **`lic build` certificate**, not “safety later.”
- **Reddit:** `site:reddit.com` returned no hits — use HPC Carpentry + Kokkos GitHub issues as bibliography.
- **New issues this pass:** [lic#65](https://github.com/li-langverse/lic/issues/65), [lic#66](https://github.com/li-langverse/lic/issues/66), [benchmarks#41](https://github.com/li-langverse/benchmarks/issues/41).

---

## Deferred

Agent-kit drift · org CI · HPX/RAJA/hypre · deep Reddit curation · distributed AMG.
