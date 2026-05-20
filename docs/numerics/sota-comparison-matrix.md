# SOTA comparison matrix (numerics · simulation · stability)

**Audience:** **lic** kernel authors, **benchmarks** catalog maintainers, numerics agents (`research-li-numerics`, `numerics-autoresearch`, `bench_improver`).  
**Policy:** [benchmark honesty](../honesty/benchmark-dashboard.md) — the public dashboard today is primarily **Li vs in-repo C++ (or shared `common/*_core.c`)** on fixed harness sizes. **“Beats SOTA products”** requires named oracles, reproducible configs, and a study — not a green cell alone.

**Methodology:** [research-methodology.md](./research-methodology.md) (Mode A survey vs Mode B autoresearch). **HPC rubric signals:** [ecosystem-explorer.md](../ecosystem/ecosystem-explorer.md). **GEMM N-scaling / huge matrices:** [matmul-scaling-and-huge-gemm.md](./matmul-scaling-and-huge-gemm.md).

---

## 1. What “SOTA” means here

| Layer | Meaning | Owned by |
|-------|---------|----------|
| **Tiered harness** | Reproducible problem definitions, sizes, and metrics in **lic** `benchmarks/tier*` + **li-tests** | **lic** |
| **Org catalog** | Which kernels appear on the dashboard + thresholds | **benchmarks** `catalog.toml` |
| **Reference implementations** | C++/Julia/Rust oracles **in the same harness** today; optional vendor BLAS / external simulators **only when wired as extra columns** | **lic** harness + ingest |
| **Field SOTA** | Published codes (LAMMPS, GROMACS, OpenFOAM, Taichi, PhysX, Chrono, etc.) | **Evidence** in `docs/numerics/studies/*` + optional future bench columns |

We want **stability, performance at small and large particle counts, memory, and long horizons** — but each claim must name **metric, configuration, commit, and comparator**.

---

## 2. Measurement axes (required for serious simulation claims)

| Axis | Small scale | Large scale | Long horizon | Notes |
|------|-------------|-------------|--------------|--------|
| **Stability** | tier-0 / invariants | no blow-up at max N in harness | energy / momentum drift vs step count | Use **tier-0** + explicit invariant tests; plot drift in studies |
| **Wall time** | tier-1 micro + small N tier-2 | largest N the harness supports | total time to T_end | Dashboard **`wall_time`** + `ratio_vs_cpp`; scaling ≠ single-node ratio |
| **Throughput** | steps/s at small DOF | steps/s at large DOF | sustained average (exclude cold start) | Define warmup policy in harness README |
| **Memory** | peak RSS small | peak RSS large | allocator churn / arena reuse | **Not** on dashboard today by default — add **lic** harness metric + CSV column + ingest extension |
| **Accuracy** | L2/L∞ vs analytic or fine grid | same at coarse grid | error growth in time | Needs reference solution column in study |
| **Determinism / reproducibility** | same hash across runs | bitwise vs tolerance policy | cross-platform | Tie to **tier-0** and CI seeds |

**Regression rule (from methodology):** do not trade stability or accuracy for wall time without a written study and human approval.

---

## 3. Map: catalog tiers ↔ axes

| Tier | Typical contents | Stability | Perf | Memory / long run |
|------|------------------|-----------|------|---------------------|
| **0** | Correctness / parse / invariant smoke | **Primary** | N/A | Short |
| **1** | Microkernels (SIMD, GEMM, reductions) | Invariants where applicable | **Primary** | Measure for allocator-bound kernels |
| **2** | PDE / particles / fluids / rigid / cloth | **Primary** + CFL-aware harnesses | **Primary** | **Extend harness** for peak RSS + long T |
| **3+** | Tooling, HTTP, demos | Smoke | Secondary | Profile sparingly |

**Game / simulation product proxies** (for *future* explicit oracles — not implied by current green rows):

| Domain | Example external comparators | Li-side anchor today |
|--------|-------------------------------|----------------------|
| Molecular / particles | LAMMPS, GROMACS, OpenMM | `md_lennard_jones`, `nbody_gravity`, SPH / MD harnesses |
| Fluids / PDE | OpenFOAM, Clawpack, Basilisk | `euler_fluid_2d`, `advection_diffusion_2d`, `wave_equation_*` |
| Rigid / multibody | Bullet, Chrono, MuJoCo | `rigid_body_stack`, `double_pendulum` |
| Cloth / deformables | ARCSim-style refs, projective dyn papers | `cloth_swing` |
| Game engines (end-to-end) | Unreal/Unity **only** as *latency/throughput* studies outside micro harness | World Studio composables = **integration**, not GPU fill-rate SOTA |

---

## 4. Small vs large particles / bodies (checklist)

When extending or reviewing a **particle** or **N-body** style kernel:

1. **N sweep** — publish a table: N ∈ {1e2, 1e3, 1e4, …} vs wall time and peak RSS (even if only in a study until CSV supports it).
2. **Neighbor policy** — O(N²) vs grid/linked-list; state which the harness uses; compare apples-to-apples vs external MD codes.
3. **FP precision** — float vs double; mixed precision needs explicit error budget.
4. **Long run** — ≥ 10× the default step count in a **study** plot: drift, energy, max |v|.
5. **SOTA citation** — at least two references: one **textbook or survey**, one **reference implementation** (paper + code).

---

## 5. Work queue (honest gaps)

| Gap | Action | Repo |
|-----|--------|------|
| Memory not in CSV | Add optional `peak_rss_mb` (or allocator ticks) to **lic** bench export + **ingest** merge | **lic** + **benchmarks** |
| Long-horizon plots | `docs/numerics/studies/*` + GIF pipeline ([benchmark honesty](../honesty/benchmark-dashboard.md)) | **lic** / **benchmarks** |
| External simulator column | Second CSV language tag (e.g. `oracle=lammps`) + policy in catalog | **lic** harness |
| Distributed / GPU SOTA | Kokkos / PETSc-class stacks — org **explorer** + **lic** issues (**G-par**, **lic#15**) | **roadmap** / **lic** |
| “Beats product X” | **Never** from dashboard alone; needs study + pinned versions of X | **docs/numerics/studies** |

---

## 6. Commands (preflight)

```bash
# Catalog vs lic tree (tier-0 … tier-2 paths)
LIC_ROOT=../lic python3 scripts/plan-completion-audit.py

# Full composable / tier regressions (run inside lic checkout)
cd ../lic && ./li-tests/run_all.sh composable

# Refresh dashboard data after lic CSV export
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
```

---

## 7. Related issues (org)

Use **`explorer-finding`** / **`ecosystem-gap`** when blocked on missing harness columns or external oracle policy — link this matrix.

---

*Living document — bump when new catalog rows or ingest metrics land.*
