# Gap explorer digest — HPC, simulations, AI-first tooling

**Generated:** 2026-05-26T06:17Z  
**Agent:** `gap_explorer`  
**Preflight:** `benchmarks/scripts/ecosystem-explorer.py` (LIC_ROOT=../lic), briefing `agent-briefing.json` @ 2026-05-26T06:16Z  
**Quality scorecard:** `benchmarks/data/latest/ecosystem-quality-report.json` — grade **D** (62.4), `gap_pressure` **72.0** (45 open gaps), `ecosystem_posture` **25.0** (bias `benchmark-red-rows`, `swarm-gap-backlog`)

---

## Executive summary

- **Static scan:** `std.summary` and `std.plot` remain **missing** on disk; `std.io` / `std.csv` are **present** — close/reconcile registry rows `gap-missing-std-std-io` / `std-csv` (already `closed` in registry).
- **HPC rubric:** Kokkos, PETSc, FFTW, hypre, HPX, RAJA **missing**; Eigen, OpenMP, SUNDIALS **partial** — Li `std/execution` decorators are the Kokkos-class portability gap (lic #15, registry `gap-hpc-kokkos-execution-memory-spaces`).
- **Benchmark pressure:** **8** red tier-1/2 rows vs C++ in `ecosystem-audit.json` — six new registry `competitor_feature` rows added this pass; route to `numerics_researcher` / `bench_improver` (PH-5b, PH-7e).
- **Catalog:** `suggested_catalog_gaps` — increase **pure_li** variant rows for PH-7e codegen proof (`gap-competitor-pure-li-ph7e-catalog`).
- **Competitive honesty:** `competitive/verticals.toml` exists in `lic-worktrees/compiler-studio` but **not** on benchmarks `main` — vertical stub ingest is a no-op (`gap-infra-verticals-toml-missing-benchmarks-main`).
- **Web/Reddit (≥7 queries):** PETSc 3.25 Kokkos views, Eigen 5.0 semver, Kokkos 4.5–5.x + Chapel 2.8 HPSF, FFT roofline vs cuFFT, Kokkos vs OpenMP portability papers; `site:reddit.com` index returned no thread snippets — cite arXiv/OSTI + https://www.reddit.com/r/HPC/ for manual follow-up.
- **Swarm registry:** **9** new `competitor_feature` rows appended; **0** new GitHub issues (existing lic/benchmarks ecosystem issues + swarm goals cover themes).
- **North star fit:** Scientific computing / HPC — PH-2i (linalg partial), PH-5b (tier-1 numerics), PH-7e (SIMD/parallel), PH-IO (agent ingest/dashboard); proof → easy → fast.

---

## Deliverable / findings

### 1. Quality scorecard bias

| Signal | Value | Evidence |
|--------|------:|----------|
| `gap_pressure` | 72.0 | 45 open gaps; finding `swarm-gap-backlog` |
| `ecosystem_posture` | 25.0 | 61 failed PRs (briefing), 1 repo missing CI on main |
| `benchmark-red-rows` | high | 8 rows in `ecosystem-audit.json` → `benchmarks.red` |
| `swarm-gap-backlog` | medium | `benchmarks/data/latest/swarm-gap-actions.json` |

Paths: `benchmarks/data/latest/ecosystem-quality-report.json`, `benchmarks/data/latest/agent-briefing.json`.

### 2. Missing std modules (`data/latest/ecosystem-explorer.json`)

| Module | Status | PH | Why |
|--------|--------|-----|-----|
| `std.io` | **present** | PH-IO-4 | Registry `gap-missing-std-std-io` → **closed** |
| `std.csv` | **present** | PH-IO-4 | Registry `gap-missing-std-std-csv` → **closed** |
| `std.summary` | **missing** | PH-IO-7 | `benchmarks/scripts/ingest/build_summary.li` |
| `std.plot` | **missing** | PH-IO-5 | `benchmarks/scripts/dashboard/render_dashboard.li` |

Registry: `gap-missing-std-std-summary`, `gap-missing-std-std-plot` (`missing_package`). Target: `lic/docs/ecosystem/ecosystem-package-backlog.md`, lic #13.

### 3. HPC libraries (explorer rubric)

| Library | Li status | Gap hint | Evidence URLs |
|---------|-----------|----------|---------------|
| Eigen | partial | SIMD matmul, sparse | https://libeigen.gitlab.io/releases/5.0/, https://libeigen.gitlab.io/eigen/docs-5.0/TopicUsingBlasLapack.html |
| Kokkos | missing | Views, GPU backends | https://github.com/kokkos/kokkos, https://kokkos.org/blog/blog-post-09/ |
| PETSc | missing | KSP/SNES on device | https://petsc.org/release/changes/325/, https://petsc.org/main/src/mat/impls/aij/seq/kokkos/aijkok.kokkos.cxx.html |
| FFTW | missing | Catalog FFT row | https://github.com/project-gemmi/benchmarking-fft, benchmarks #18 |
| OpenMP | partial | Lowering vs Kokkos GPU | https://www.osti.gov/servlets/purl/2224192 |
| hypre | missing | BoomerAMG | lic #108 |
| SUNDIALS | partial | Stiff ODE | lic #35, `gap-hpc-sundials-stiff-ode-sensitivity` |
| RAJA | missing | Policy loops | https://arxiv.org/html/2402.08950v1, lic #109 |
| Chapel | competitor | HPSF productivity | https://chapel-lang.org/blog/posts/announcing-chapel-2.0/, https://github.com/chapel-lang/chapel/releases/tag/2.8.0 |

Li analogs: `lic/std/execution/decorators.li`, `li-math-numerics`, `li-tests/` tier-1 harness, `docs/numerics/`.

### 4. Red benchmark rows (numerics path)

From `benchmarks/data/latest/ecosystem-audit.json` → `lic/li-tests/`, `benchmarks/competitive/`:

| Bench ID | ratio_vs_cpp | PH | Registry id (new this pass) |
|----------|-------------:|-----|------------------------------|
| `matmul_naive` | 1.73 | PH-5b, PH-7e | `gap-benchmark-red-matmul-naive-tier1` |
| `num_gmres` | 1.68 | PH-5b | `gap-benchmark-red-num-gmres-tier1` |
| `num_integ_euler` | 1.40 | PH-5b | `gap-benchmark-red-num-integ-euler-tier1` **new** |
| `num_integ_verlet` | 1.35 | PH-5b | `gap-benchmark-red-num-integ-verlet-tier1` **new** |
| `num_opt_line_search` | 2.00 | PH-5b | `gap-benchmark-red-num-opt-line-search-tier1` **new** |
| `cloth_swing` | 1.37 | PH-5b | `gap-benchmark-red-cloth-swing-tier1` **new** |
| `orbit_two_body` | 1.69 | PH-5b | `gap-benchmark-red-orbit-two-body-tier1` **new** |
| `schrodinger_1d_barrier` | 1.77 | PH-5b | `gap-benchmark-red-schrodinger-1d-barrier-tier1` **new** |

**Action:** `coord_numerics` heap — proof-before-perf; no catalog threshold-only tweaks.

### 5. Competitive verticals (stub / honesty)

Source: `lic-worktrees/compiler-studio/benchmarks/competitive/verticals.toml` (15 `workload_class = stub` rows).

| Vertical ID | Incumbent | Notes |
|-------------|-----------|-------|
| `md_lennard_jones` | LAMMPS / GROMACS | Not parity — oracle stub |
| `pde_heat_2d` | OpenFOAM / PETSc | heat_equation_2d in verify.py |
| `fea_linear_elasticity` | CalculiX / ANSYS | No bench oracle |
| `cfd_lid_driven_cavity` | OpenFOAM / COMSOL | PH-CAE CFD track |

Registry rows: `gap-vertical-stub-*` (four simulation verticals ingested prior pass).

### 6. Web + Reddit research (URLs)

| Query | Summary | URLs |
|-------|---------|------|
| `site:reddit.com r/HPC Kokkos OR OpenMP` | No indexed snippets; manual r/HPC follow-up | https://www.reddit.com/r/HPC/ |
| Kokkos vs OpenMP portability | Kokkos/RAJA outperform directive-only OpenMP on complex GPU kernels | https://arxiv.org/html/2402.08950v1, https://arxiv.org/html/2411.05009v1, https://www.osti.gov/servlets/purl/2224192 |
| PETSc + Kokkos 3.25 | `VecKokkosPlaceArray`, `MatCreateSeqAIJKokkosWithKokkosViews`, PCBJKOKKOS | https://petsc.org/release/changes/323/, https://petsc.org/ |
| Eigen 5.0 SOTA | Released 2025-09-30; semantic versioning; `EIGEN_USE_BLAS` | https://libeigen.gitlab.io/releases/5.0/, https://gitlab.com/libeigen/eigen/-/releases/5.0.0 |
| Kokkos 4.5–5.x | SYCL production; auto-tuning; Kokkos 5.0 on master | https://github.com/kokkos/kokkos/issues/7183, https://www.olcf.ornl.gov/calendar/kokkos-4-5-release-briefing/ |
| Chapel 2.8 | HPSF project; ROCm 7, LLVM 21 | https://github.com/chapel-lang/chapel/releases/tag/2.8.0, https://hpsf.io/blog/2025/hpsf-welcomes-chapel/ |
| FFT roofline | FFTW CPU reference; cuFFT GPU crossover ~2^16 | https://github.com/project-gemmi/benchmarking-fft, https://github.com/faliszewskii/fourier_transform_benchmark |

### 7. Swarm goals vs new GitHub issues

Existing coverage: PH-IO (#13), Kokkos (#15), FFT (#18, #26, #52), PETSc/hypre (#108, #117), Eigen (#33), physics (#14, #50). **No new issues filed** — prefer `swarm_coverage` / `numerics_researcher` goal apply in `li-cursor-agents`.

---

## Recommended issues/PRs

| Title | Repo | Labels / agent |
|-------|------|----------------|
| Mirror `competitive/verticals.toml` onto benchmarks `main` | benchmarks | `ecosystem` → unblocks `swarm-gap-ingest` vertical sweep |
| Ship `std.summary` / `std.plot` (PH-IO) | lic | `missing_package`, `package_architect` |
| Tier-1 red-row evidence bundle (matmul + GMRES + integrators) | lic | `numerics`, PH-5b → `numerics_researcher` |

---

## Deferred

- **Chapel / Carbon competitive matrices** — lic #65; registry `gap-competitor-chapel-hpsf-productivity` tracks Chapel only.
- **Full 15-row verticals stub sweep** — blocked until benchmarks hosts `verticals.toml`.
- **Reddit deep dive** — re-run manual r/HPC when indexers return threads; no unofficial APIs.
- **GPU FFT vendor harness** — benchmarks #52 / #26; after tier-1 matmul green.
- **Physics org mirrors (12 packages)** — lic #50.

---

## Appendix A — Swarm gap registry (ingest-ready)

Machine-readable: `benchmarks/data/latest/gap-explorer-ingest-2026-05-26.json`

```bash
cd /path/to/lic && python3 scripts/swarm-gap-ingest.py
python3 scripts/swarm-gap-apply-actions.py --dry-run
```

**New rows this pass (9):** six tier-1 red benches, `gap-hpc-raja-execution-policies`, `gap-hpc-sundials-stiff-ode-sensitivity`, `gap-hpc-openmp-llvm-lowering-rubric`, `gap-competitor-chapel-hpsf-productivity`.

**North star fit:** Scientific computing + HPC; PH-2i, PH-5b, PH-7e, PH-IO; proof → easy → fast.
