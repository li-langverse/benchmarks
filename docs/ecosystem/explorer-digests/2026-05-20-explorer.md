# Gap explorer digest — 2026-05-20 (20:12Z pass)

**Agent:** `gap_explorer` · **Skill:** `explore-li-ecosystem` · **Heap:** `coord_ecosystem`  
**Vision:** [vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) · pillars: **proof → easy → fast** ([`org_roadmap`](../../data/latest/agent-briefing.json))  
**Master plan:** [2026-05-14-li-master-plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md)  
**Preflight:** `ecosystem-explorer.py` (2026-05-20T20:12Z), `ecosystem-audit.json` (2026-05-20T20:13Z), briefing `generated_at` 2026-05-20T20:12Z  
**Static JSON:** [`data/latest/ecosystem-explorer.json`](../../data/latest/ecosystem-explorer.json) · **Control plane:** latest report `briefing_hash` `7d7f86e03968a608` (`gap_explorer` runs `finished`)

---

## Executive summary

- **LIC_ROOT absent** (`lic_present: false`, `lic_root: /workspace/lic`) — static scan cannot enumerate `lic` `std/*`; **21 catalog path gaps** in plan-completion audit are partly **checkout layout**, not only missing implementations ([benchmarks#20](https://github.com/li-langverse/benchmarks/issues/20)).
- **Four PH-IO std modules missing** (`std.io`, `std.csv`, `std.summary`, `std.plot`) while benchmarks `.li` already import them — blocks Python-free ingest/dashboard ([lic#13](https://github.com/li-langverse/lic/issues/13)).
- **HPC rubric: 6/10 libraries missing or partial** (Kokkos, PETSc, FFTW, hypre, HPX, RAJA) vs minimal `std/execution` decorators and **9/15** tier-2 `shared_c_kernel` variants ([lic#15](https://github.com/li-langverse/lic/issues/15)).
- **Catalog:** no tier-1 FFT row; **1/25** `pure_li` variant — `horner_pure_li` **~88.8×** cpp ([`data/latest/summary.json`](../../data/latest/summary.json), [PH-7e study](../../docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md)).
- **SOTA (2025–2026):** Kokkos **4.6** + **mdspan** View refactor; Eigen **5.0** BLAS ABI; PETSc **3.25** `PCBJKOKKOS`; Chapel **2.8** ROCm/RISC-V; LLVM MLIR **canonical loop** OpenMP lowering — mostly tracked; gaps below.
- **Web/Reddit:** Indexed `site:reddit.com` returned no thread URLs; proxy signals from HPC Carpentry, Trilinos, and portability papers (URLs in §2).
- **P0 ecosystem:** **7 failing PRs**; horner fix triplicate (**lic#85/#122/#123**); **li-local-ci** missing `ci.yml` on main.
- **This pass filed 3 new `explorer-finding` issues:** mdspan/View buffer ABI, OpenMP affinity occupancy, mandatory LIC_ROOT for explorer accuracy — §4.

---

## Deliverable / findings

### 1. Static scan ([`ecosystem-explorer.json`](../../data/latest/ecosystem-explorer.json))

| Signal | Evidence path | Li gap / PH |
|--------|---------------|-------------|
| `lic_present: false` | `lic_root`, empty `std_modules_on_disk` | Mount **lic** at `LIC_ROOT` in agent/CI workspaces |
| Missing std (4) | `missing_std_modules[]` | **PH-IO-4/5/7** — `scripts/ingest/csv_ingest_smoke.li`, `build_summary.li`, `render_dashboard.li` |
| Catalog 25 rows | `catalog.*`, [`catalog.toml`](../../catalog.toml) | FFT missing; 1 `pure_li` vs 9 `shared_c_kernel` |
| Suggested gaps | `catalog.suggested_catalog_gaps` | FFTW/vendor FFT; expand `pure_li` for **PH-7e** |
| HPC libraries | `hpc_libraries[]` | See table |
| Open issues | `open_ecosystem_gap_issues` | 20+ trackers — avoid duplicate filings |

**HPC library rubric:**

| Library | Status | Li analog | Trackers |
|---------|--------|-----------|----------|
| Eigen | partial | `li-std-math`, tier-1 matmul | **lic#33**, **#27** |
| Kokkos | missing | `std/execution` decorators | **lic#110**, **#116**, **#66**, **#15** |
| PETSc | missing | physics stubs, shared-C benches | **lic#117**, **#108**, **#28** |
| FFTW | missing | none | **benchmarks#18**, **#26**, **#51–52** |
| OpenMP | partial | LLVM only | **lic#34**, **#124**, **#116** |
| HPX / RAJA | missing | none / harness | **lic#112**, **#109** |
| SUNDIALS / hypre | partial / missing | tier-2 integrators | **lic#35**, **#108** |
| C++ `std::execution` | partial | `decorators.li` | **lic#125**, **#109** |

**Numerics (preflight [`ecosystem-audit.json`](../../data/latest/ecosystem-audit.json)):**

- **RED:** `horner_pure_li` ratio **88.8208** vs cpp — compiler/DCE (**PH-5b**, **PH-7e**), not missing algorithm ([`docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md`](../../docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md)).
- **Near threshold (~1.02–1.03×):** `matmul_blocked`, `nbody_gravity`, `double_pendulum`, `wave_equation_1d`, `harmonic_oscillator_chain`.
- **Catalog paths under LIC_ROOT:** 21 rows reported missing when **lic** not checked out ([`plan-completion-audit`](../../data/latest/agent-briefing.json) → `catalog_gaps`).

### 2. Web + Reddit research (≥7 queries; no Reddit API)

#### Required: `site:reddit.com r/HPC Kokkos OR OpenMP`

- No indexed Reddit URLs in this environment.
- **Proxy (community practice):** Kokkos+OpenMP thread model for LAMMPS — `OMP_NUM_THREADS`, `OMP_PROC_BIND=spread`, `OMP_PLACES=threads`; ensure MPI tasks × threads ≤ physical cores — [HPC Carpentry Kokkos+OpenMP](http://www.hpc-carpentry.org/tuning_lammps/07-kokkos-openmp/index.html).
- **Trilinos:** prefer Kokkos OpenMP backend when host code already uses OpenMP — [Trilinos#1391](https://github.com/trilinos/Trilinos/issues/1391).
- **Academic:** prescriptive vs descriptive Kokkos/OpenMP branches still needed for peak performance — [White Rose eprint 235565](https://eprints.whiterose.ac.uk/id/eprint/235565/1/P3_Paper_on_Kokkos_vs_OpenMP_descriptive_and_prescriptive_-6.pdf) → **lic#124**.

#### Kokkos 4.6 + mdspan View refactor

- [Kokkos 4.6.0 release](https://github.com/kokkos/kokkos/releases/tag/4.6.00) — H100 reductions, HIP multi-GPU, graph `then` nodes.
- [View meets std::mdspan](https://kokkos.org/blog/2025-04-view-refactor) — core refactor post-4.6.
- **Li:** tier-2 memory spaces / strided buffers — **lic#110**, **#66**; **new:** mdspan-aligned buffer ABI (**lic#128** this pass).

#### PETSc + Kokkos PDE stack

- [ALCF PETSc exascale](https://www.alcf.anl.gov/news/optimizing-petsc-exascale) — single-source Kokkos, isolate CPU↔GPU sync.
- [PCBJKOKKOS](https://petsc.org/release/manualpages/PC/PCBJKOKKOS/) — device batched block Jacobi, `-ksp_type preonly`.
- **Li:** implicit tier-2 preconditioner rubric — **lic#117**, **#108**.

#### Eigen 5.0

- [Eigen 5.0 release](https://libeigen.gitlab.io/releases/5.0/) — semver, BLAS returns `void`, last C++14 release.
- [Efficient products](https://eigen.tuxfamily.org/dox/TopicWritingEfficientProductExpression.html) — `.noalias()` for peak GEMM.
- **Li:** numerics reference policy — **lic#33**; matmul rows near 1.03× cpp.

#### Chapel 2.8

- [Chapel 2.8 announcement](https://chapel-lang.org/blog/posts/announcing-chapel-2-8/) — RISC-V, ROCm 6.3/7, LLVM 21.
- **Li:** portability + launcher ergonomics — **lic#113**, **#54**.

#### FFT / VkFFT

- [VkFFT performance](https://pyvkfft.readthedocs.io/en/latest/performance.html) — competitive vs cuFFT at large N.
- **Li:** tier-1 FFT + roofline — **benchmarks#18**, **#26**, **#51–52**.

#### LLVM OpenMP / MLIR

- [Canonical loop lowering](https://github.com/llvm/llvm-project/commit/96bc07d49221) — `omp.canonical_loop` + unroll heuristic.
- [Composite distribute+wsloop](https://github.com/llvm/llvm-project/pull/127819) — host lowering path.
- **Li:** decorator → IR — **lic#34**.

#### Systems languages (2025–2026)

- [Vex](https://www.vex-lang.org/docs/guide/introduction) — ownership + tensor/SIMD lowering.
- [Lockstep](https://news.ycombinator.com/item?id=47393552) — data-oriented, straight-line SIMD, static arenas.
- **Li:** deferred competitive rubric (see **lic#65** Carbon/Mojo); not filed again this pass.

### 3. Org / audit cross-check

| Source | Metric | Next agent |
|--------|--------|------------|
| `ecosystem-audit.json` | 7 failed PRs, `horner_pure_li` red | **bench_improver**, **bug_fixer** |
| `issue_triage` | 24 `plan-needed` | **issue_planner** |
| `org_ci_audit` | `li-local-ci` missing CI | **ci_maintainer** |
| `org_agent_kit_audit` | 8 repos drifted from 1.3.2 | **agent_kit_maintainer** |
| `merge_plan` | lic#85/#122/#123 redundant | **pr_alignment** |

### 4. Issues filed (this pass — max 3)

| Repo | # | Title | PH / G |
|------|---|-------|--------|
| lic | [#128](https://github.com/li-langverse/lic/issues/128) | Kokkos 4.6+ `std::mdspan` View refactor — Li tier-2 strided buffer ABI rubric | **PH-7e**, **G-par** |
| lic | [#129](https://github.com/li-langverse/lic/issues/129) | OpenMP affinity + MPI×threads occupancy rubric for portable Li runtime | **G-par**, **PH-7e** |
| benchmarks | [#54](https://github.com/li-langverse/benchmarks/issues/54) | Gap-explorer: require LIC_ROOT lic checkout for accurate static scan in cloud agents | **PH-IO**, easy |

**Earlier today (same digest cycle):** **lic#124**, **#125**, **benchmarks#53** — prescriptive OpenMP branches, C++26 senders, Python parity gate.

---

## Recommended issues / PRs

| P | Repo | Item | Labels |
|---|------|------|--------|
| P0 | lic | [#13](https://github.com/li-langverse/lic/issues/13) | PH-IO std modules |
| P0 | lic | One of PR [#85](https://github.com/li-langverse/lic/pull/85) / [#122](https://github.com/li-langverse/lic/pull/122) / [#123](https://github.com/li-langverse/lic/pull/123) | horner DCE |
| P1 | lic | [#15](https://github.com/li-langverse/lic/issues/15), [#34](https://github.com/li-langverse/lic/issues/34), [#124](https://github.com/li-langverse/lic/issues/124) | portable lowering |
| P1 | benchmarks | [#18](https://github.com/li-langverse/benchmarks/issues/18), [#41](https://github.com/li-langverse/benchmarks/issues/41), [#52](https://github.com/li-langverse/benchmarks/issues/52) | FFT + pure_li |
| P1 | benchmarks | [#54](https://github.com/li-langverse/benchmarks/issues/54) | LIC_ROOT for explorer |
| P2 | benchmarks | [PR #47](https://github.com/li-langverse/benchmarks/pull/47) | numerics docs (CI green) |

**No code, no merges, no Actions cron** in gap_explorer runs.

---

## Deferred

- Manual Reddit review: [r/HPC](https://www.reddit.com/r/HPC/), [r/ProgrammingLanguages](https://www.reddit.com/r/ProgrammingLanguages/).
- Duplicate explorer trackers: Kokkos 4.6 (**#110**, **#66**), Chapel 2.8 (**#113**), PETSc (**#117**), Eigen 5.0 (**#33**); Vex/Lockstep competitive matrix deferred (**lic#65**).
- Implementation work → **code_implementer** / **issue_planner** after `plan-approved`.
- Master plan + `provability-gaps.md` not visible without **lic** at `/lic` or `../lic`.

---

## Suggested next agents

| Agent | Reason |
|-------|--------|
| **issue_planner** | 24 `plan-needed` + new explorer findings |
| **bench_improver** / **numerics_researcher** | `horner_pure_li` red |
| **gap_explorer** | Re-run after **lic** mounted at `LIC_ROOT=../lic` |
| **ci_maintainer** | `li-local-ci` missing `ci.yml` |
