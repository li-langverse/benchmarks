# Gap explorer digest — 2026-05-17

**Agent:** gap_explorer · **Skill:** explore-li-ecosystem  
**Preflight:** `ecosystem-explorer.py` (LIC_ROOT=`../li`), `ecosystem-audit.py`  
**Vision:** [proof → easy → fast](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) · [master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)  
**JSON:** `data/latest/ecosystem-explorer.json` · `data/latest/ecosystem-audit.json`

> Full digest: [2026-05-17-explorer.md](./2026-05-17-explorer.md)

---

## Executive summary

- **LIC_ROOT note:** `../lic` is not present on this machine; scan used `../li` (`lic_present: true`). Automation should set `LIC_ROOT` to the local compiler clone (often `../li`).
- **PH-IO blockers (P1 / easy):** Four std modules still missing on disk: `std.io`, `std.csv`, `std.summary`, `std.plot` — benchmarks ingest/dashboard already import them ([PH-IO-4](https://github.com/li-langverse/lic/issues?q=PH-IO-4), [PH-IO-5](https://github.com/li-langverse/lic/issues?q=PH-IO-5), [PH-IO-7](https://github.com/li-langverse/lic/issues?q=PH-IO-7)).
- **On-disk std today:** only `std.bytes.bytes`, `std.execution.decorators` — execution decorators exist but are not wired to codegen policies.
- **Proof / fast (P1):** `horner_pure_li` remains **red** (~88.8× cpp); needs **PH-5b**, **PH-7e** pure-Li codegen in lic — not catalog threshold tweaks.
- **Catalog gaps (P2):** No FFT tier-1 micro-bench (FFTW/MKL roofline peer); only **2** `pure_li` variants vs 37 default — weak PH-7e proof surface.
- **HPC stack (P1–P2):** Kokkos/PETSc/hypre/RAJA **missing**; Eigen/FFTW/OpenMP/SUNDIALS/stdpar **partial** — tier-2 physics still leans on shared C kernels (1 row) vs pure-Li path.
- **External SOTA (2024–2026):** Kokkos 4.x–5.x, PETSc 3.22+ Kokkos GPU preconditioners, Eigen 3.4.1 / 5.0, Chapel 2.0+ stability — Li needs portability + solver *interfaces* before full stacks.
- **Platform (deferred):** Agent-kit drift, 12 repos missing `ci.yml` on main — platform agents, not this pass.

---

## Recommended issues (file with `explorer-finding`)

| Repo | Title | PH ids |
|------|-------|--------|
| **lic** | PH-IO: ship std.io, std.csv, std.summary, std.plot for benchmarks ingest | PH-IO-4, PH-IO-5, PH-IO-7 |
| **benchmarks** | Catalog: tier-1 FFT micro-bench (FFTW/MKL/cpp baseline) | PH-5b |
| **lic** | std/execution: document OpenMP/Kokkos lowering plan for tier-2 physics | PH-7e |

**Status:** Issues not filed — `gh auth login` required.

---

## Deferred

Agent-kit sync · org CI on main · HPX/RAJA/hypre · live docs · horner codegen implementation (numerics agent).
