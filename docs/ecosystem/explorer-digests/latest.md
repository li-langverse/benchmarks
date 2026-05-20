# Gap explorer digest — 2026-05-20

**Agent:** `gap_explorer` · **Skill:** `explore-li-ecosystem` · **Heap:** `coord_ecosystem`  
**Vision:** [org roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) · pillars: proof → easy → fast  
**Master plan:** [2026-05-14-li-master-plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)  
**Preflight:** `ecosystem-explorer.py` (2026-05-20T19:57Z), `ecosystem-audit.json` (2026-05-20T19:57Z), briefing preflight JSON  
**Static JSON:** `data/latest/ecosystem-explorer.json` · **Control plane:** `gap_explorer` runs finished (latest `gap_explorer-1779306082157`)

**north_star_fit:** HPC + simulation competitiveness (Kokkos/PETSc/Chapel/Eigen SOTA) · AI-first ingest without Python fallbacks · pure-Li codegen proof (**PH-7e**, **PH-5b**) · easy benchmark loop (**PH-IO-4/5/7**)

---

## Executive summary

- **LIC_ROOT absent in this workspace** (`lic_present: false` at `/workspace/lic`; `/lic` not mounted) — explorer cannot see `std/*` on disk; **21 catalog path gaps** in plan-completion audit are partly **checkout layout**, not only missing code (**benchmarks#20**, **#25**, **#28**).
- **Four PH-IO std modules still missing** (`std.io`, `std.csv`, `std.summary`, `std.plot`) while benchmarks `.li` already import them — blocks Python-free ingest/dashboard (**lic#13**).
- **HPC stack rubric: 6/10 libraries missing or partial** — Kokkos, PETSc, FFTW, hypre, HPX, RAJA vs Li `std/execution` decorators + shared-C tier-2 physics (**lic#15**, **#108–117**).
- **Catalog gaps:** no tier-1 FFT micro-bench; only **1/25** `pure_li` rows (`horner_pure_li` **~88.8×** cpp per `data/latest/summary.json`) — expand proof surface (**benchmarks#18**, **#41**, **#51–52**).
- **SOTA releases (2025–2026):** Kokkos **4.6.0/4.6.1** (multi-GPU, graph nodes), Eigen **5.0** (BLAS ABI, C++14 floor), PETSc **3.25** `PCBJKOKKOS`, Chapel **2.8** (RISC-V, ROCm 6.3/7) — track in bench policy (**benchmarks#27**).
- **Web/Reddit:** Direct `site:reddit.com` queries returned no indexed hits; academic/industry sources confirm **portable HPC needs divergent platform branches** (Kokkos vs OpenMP) and **GPU-native PETSc preconditioners** beat naive CPU offload.
- **P0 ecosystem:** **7 failing PRs** including horner fix triplicate (**lic#85/#122/#123**); **horner_pure_li** remains primary numerics debt (**PH-5b**, **PH-7e**).
- **This run filed 3 new `explorer-finding` issues** (prescriptive OpenMP branches, C++ `std::execution` senders, ingest parity gate) — see §Issues filed.

---

## Deliverable / findings

### 1. Static scan (`ecosystem-explorer.json`)

| Signal | Evidence | Li gap / PH |
|--------|----------|-------------|
| `lic_present: false` | `lic_root: /workspace/lic`, empty `std_modules_on_disk` | CI/agents must checkout **lic** sibling; false “missing std” in automation |
| Missing std modules (4) | `missing_std_modules[]` | **PH-IO-4/5/7** — `scripts/ingest/*.li`, `render_dashboard.li` |
| Catalog 25 rows | `catalog.total`, variants: 9 `shared_c_kernel`, 1 `pure_li` | FFT row missing; PH-7e needs more `pure_li` rows |
| Suggested gaps | `catalog.suggested_catalog_gaps` | FFTW/vendor FFT; pure_li expansion |
| HPC libraries | `hpc_libraries[]` | See table below |
| Agent kit | `1.3.2+130de1d9a8d0e52c`, `drift: false` in benchmarks stamp | Org repos still drift per `org-agent-kit-audit` |

**HPC library status (explorer rubric):**

| Library | Li status | Gap hint | Existing tracker |
|---------|-----------|----------|------------------|
| Eigen | partial | SIMD GEMM, sparse | **lic#33**, **lic#27** |
| Kokkos | missing | Views, execution spaces, GPU | **lic#110**, **#116**, **#66**, **#15** |
| PETSc | missing | KSP/SNES, implicit PDE | **lic#117**, **#108**, **#28** |
| FFTW | missing | No catalog FFT | **benchmarks#18**, **#26**, **#51–52** |
| OpenMP | partial | No first-class Li pragma surface | **lic#34**, **#116**, **#124** |
| HPX | missing | Async game physics | **lic#112** |
| RAJA | missing | Portable loop policies | **lic#109** |
| SUNDIALS | partial | Stiff ODE / sensitivity | **lic#35** |
| hypre | missing | BoomerAMG | **lic#108** |
| C++ std::execution | partial | Decorators only | **lic#109**, **#125** |

**Numerics evidence (dashboard):**

- `data/latest/summary.json` → `horner_pure_li` Li **0.9415 s** vs cpp **0.0106 s** (~**88.8×**); tier-1 near-threshold greens: `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain` (~1.02–1.03× cpp).
- `ecosystem-audit.json` → same red row; **5 near_threshold** entries; failed PRs include **lic#122/#123/#85** (horner timing/DCE).

**Language heuristics (explorer):**

1. **stdlib-surface** — ship PH-IO modules before expanding HPC physics APIs.  
2. **pure-li-benches** — fix **PH-7e** codegen (Estrin/FMA/lexer), not catalog thresholds.  
3. **python-fallback** — `ingest-lic.sh` → `build_summary.py` until `std.summary` (**new benchmarks#53**).  
4. **shared-c-kernels** — tier-2 `shared_c_kernel` variants need pure-Li plan per `GAME_DEV.md`.  
5. **agent-kit-drift** — sync roadmap **1.3.2** across org clones.

### 2. Web + Reddit research (≥7 queries; no Reddit API)

Queries from `web_search_queries` plus required Reddit/HPC and SOTA release searches.

#### Kokkos vs OpenMP performance portability

- **Kokkos 4.6.0** (2025-03-29) and **4.6.1** patch: CUDA reduction gains on H100, HIP `hipMallocAsync` default, experimental **multi-GPU per process**, graph `then` nodes — [release 4.6.0](https://github.com/kokkos/kokkos/releases/tag/4.6.00), [OLCF briefing](https://www.olcf.ornl.gov/calendar/kokkos-4-6-release-briefing-april-2025/).
- **Comparative study (Kokkos vs OpenMP):** portable frameworks still need **divergent code branches** to match vendor-specific performance — [White Rose eprint 235565](https://eprints.whiterose.ac.uk/id/eprint/235565/1/P3_Paper_on_Kokkos_vs_OpenMP_descriptive_and_prescriptive_-6.pdf).
- **Li gap:** `std/execution/decorators.li` is policy AST without memory spaces, NUMA, or prescriptive/descriptive branch policy — **lic#15**, **#110**, **#116**, **lic#124**.

#### PETSc + Kokkos PDE stack

- **PETSc 3.25 `PCBJKOKKOS`:** batched block-Jacobi on device via Kokkos; use with `-ksp_type preonly` — [PCBJKOKKOS manual](https://petsc.org/release/manualpages/PC/PCBJKOKKOS/).
- **2025 user thread:** Kokkos path exposes `MatGetDiagonal_SeqAIJKOKKOS()` unavailable in CUDA-only backend — [petsc-users July 2025](https://lists.mcs.anl.gov/pipermail/petsc-users/2025-July/052187.html).
- **Li gap:** tier-2 implicit PDE uses shared-C stubs; no device-native preconditioner rubric — **lic#117**, **#108**.

#### Eigen / numerics

- **Eigen 5.0** (2025-09-30): semver, **C++14 minimum** (last release on C++14), **BLAS routines return `void`**, LGPL removed — [Eigen 5.0 release](https://libeigen.gitlab.io/releases/5.0/).
- Expression-template GEMM defers temporaries; `.noalias()` required for peak GEMM — [efficient product expressions](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html).
- **Li gap:** pin reference oracles for tier-1 matmul; pure-Li SIMD vs Eigen/MKL — **lic#33**, numerics docs under `lic` (not in this clone).

#### Chapel / AI-first portability

- **Chapel 2.8** (2026-03-12): RISC-V Qthreads, ROCm 6.3/7, LLVM 21, Slurm launcher flags — [announcement](https://chapel-lang.org/blog/posts/announcing-chapel-2-8/), [HPSF post](https://hpsf.io/blog/2026/chapel-2-8-released/).
- **Li gap:** portability + launcher ergonomics vs minimal decorators — **lic#113**, **#54**.

#### FFT / roofline

- **VkFFT vs cuFFT:** competitive on large transforms; cross-vendor GPU FFT — [pyvkfft performance](https://pyvkfft.readthedocs.io/en/latest/performance.html), [VkFFT repo](https://github.com/DTolm/VkFFT).
- **Li gap:** no tier-1 FFT catalog row or roofline harness — **benchmarks#18**, **#26**, **#51**, **#52**.

#### LLVM OpenMP / MLIR (codegen parity)

- MLIR `omp` dialect lowers `wsloop`, composite `parallel+distribute+wsloop`, and **canonical loop** unroll heuristics to LLVM IR — [OpenMP dialect](https://mlir.llvm.org/docs/Dialects/OpenMPDialect/), [canonical loop lowering commit](https://github.com/llvm/llvm-project/commit/96bc07d49221).
- **Li gap:** map `std/execution` decorators to real IR policies — **lic#34**.

#### Systems language landscape (2025)

- Rust vs Carbon vs Mojo: memory safety + C++ interop tradeoffs; raw perf often secondary to velocity — [LWN Rust vs Carbon](https://lwn.net/Articles/1036912/), [Modular Mojo vs Rust](https://modular.com/blog/mojo-vs-rust).
- **Li gap:** competitive safety/verify story vs **lic build certificate** — **lic#65**.

#### Reddit (`site:reddit.com`)

- Indexed search returned **no direct thread URLs** for `r/HPC Kokkos OpenMP` or PL/HPC SIMD queries in this environment.
- **Proxy signal:** HPC Carpentry Kokkos+OpenMP tutorial and Trilinos issue #1391 (prefer OpenMP backend when code already uses OpenMP) — [HPC Carpentry](http://www.hpc-carpentry.org/tuning_lammps/07-kokkos-openmp/index.html), [Trilinos#1391](https://github.com/trilinos/Trilinos/issues/1391).

### 3. Org / audit cross-check

| Source | Key metric | Action |
|--------|------------|--------|
| `ecosystem-audit.json` | 7 failed PRs, 1 repo missing CI (`li-local-ci`) | **bug_fixer**, **ci_maintainer** |
| `plan-completion-audit` (briefing) | 21 catalog gaps, master plan file missing at `/lic/...` | Checkout **lic**; **plan_verifier** |
| `issue_triage` | 22 `plan-needed` issues | **issue_planner** |
| Open explorer issues | 14 lic + 6 benchmarks labeled `explorer-finding` | Plan, do not re-file duplicates |

### 4. Issues filed (this run — max 3)

| Repo | # | Title | PH / G |
|------|---|-------|--------|
| lic | [#124](https://github.com/li-langverse/lic/issues/124) | OpenMP prescriptive vs descriptive divergent-branch rubric for competitive portable codegen | **G-par**, **PH-7e** |
| lic | [#125](https://github.com/li-langverse/lic/issues/125) | C++26 `std::execution` sender/receiver rubric vs Li async tier-2 scheduling | **G-par**, **G-ai** |
| benchmarks | [#53](https://github.com/li-langverse/benchmarks/issues/53) | PH-IO-7: Python `build_summary.py` parity gate until `std.summary` ships | **PH-IO-7**, easy |

**Budget:** 3 new issues; deferred duplicate filings (Kokkos 4.6, Chapel 2.8, PETSc PCBJKOKKOS, VkFFT, Eigen 5.0 already tracked).

---

## Recommended issues / PRs

| Priority | Repo | Item | Labels | Why |
|----------|------|------|--------|-----|
| P0 | lic | [#13](https://github.com/li-langverse/lic/issues/13) | plan-needed, feature | Ship PH-IO std modules |
| P0 | lic | Pick one: [#85](https://github.com/li-langverse/lic/pull/85) / [#122](https://github.com/li-langverse/lic/pull/122) / [#123](https://github.com/li-langverse/lic/pull/123) | — | Horner DCE/timing; stop triplicate |
| P1 | lic | [#15](https://github.com/li-langverse/lic/issues/15), [#34](https://github.com/li-langverse/lic/issues/34), [#124](https://github.com/li-langverse/lic/issues/124) | explorer-finding | Portable parallel lowering |
| P1 | benchmarks | [#18](https://github.com/li-langverse/benchmarks/issues/18), [#26](https://github.com/li-langverse/benchmarks/issues/26), [#52](https://github.com/li-langverse/benchmarks/issues/52) | explorer-finding | FFT + roofline |
| P1 | benchmarks | [#41](https://github.com/li-langverse/benchmarks/issues/41) | explorer-finding | More `pure_li` catalog rows |
| P2 | benchmarks | [#20](https://github.com/li-langverse/benchmarks/issues/20), [#53](https://github.com/li-langverse/benchmarks/issues/53) | plan-needed / explorer-finding | LIC_ROOT + ingest parity |
| P2 | lic | [#50](https://github.com/li-langverse/lic/issues/50), [#14](https://github.com/li-langverse/lic/issues/14) | ecosystem-gap | Physics packages + mirrors |
| Docs | benchmarks | [PR #47](https://github.com/li-langverse/benchmarks/pull/47) | — | Numerics researcher pass (CI green) |

**Do not merge** without `merge-approved`. **No feature code** in gap_explorer runs.

---

## Deferred

- **Reddit-first evidence:** repeat manual review on [r/HPC](https://www.reddit.com/r/HPC/), [r/ProgrammingLanguages](https://www.reddit.com/r/ProgrammingLanguages/) when indexed search unavailable.
- **Duplicate explorer filings:** Kokkos 4.6 (**#110**, **#66**), Chapel 2.8 (**#113**), PETSc PCBJKOKKOS (**#117**), Eigen 5.0 (**#33**), RAJA (**#109**), HPX (**#112**), hypre (**#108**), SUNDIALS (**#35**), VkFFT/gearshifft (**#51–52**), pure_li expansion (**#41**), release cadence doc (**#27**).
- **Implementation:** PH-IO module code, LLVM lowering, tier-2 pure-Li physics kernels → **code_implementer** / **issue_planner** after `plan-approved`.
- **Master plan file** at `lic/docs/superpowers/plans/2026-05-14-li-master-plan.md` not visible without **lic** checkout in workspace.
- **Agent-kit org drift** (8 repos) → **agent_kit_maintainer**; **li-local-ci** missing `ci.yml` → **ci_maintainer**.

---

## Suggested agent — next tick

| Agent | Reason |
|-------|--------|
| **issue_planner** | 22 `plan-needed` + 3 new explorer findings |
| **numerics_researcher** / **bench_improver** | `horner_pure_li` red |
| **implementation_gaps** | catalog vs lic tree with LIC_ROOT fix |
| **gap_explorer** | Re-run after **lic** sibling mounted at `LIC_ROOT` |
