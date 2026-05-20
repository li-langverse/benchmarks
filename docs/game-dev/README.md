# Physics & game engine engineering (org map)

**Implement here:** runtime, world simulation, studio flows, and **tier-2 physics harnesses** live in **[lic](https://github.com/li-langverse/lic)** — under `benchmarks/tier2_physics/*`, world/sim packages, and `docs/game-dev/` on the branches that ship them.

**Track here (this repo):** [`catalog.toml`](../../catalog.toml), ingest (`./scripts/ingest/ingest-lic.sh`), and the [dashboard](https://li-langverse.github.io/benchmarks/). This tree is the **measurement** surface for PH-5b / PH-7e goals, not the engine source tree.

If you are continuing **World Studio**, composable gates, or cross-package sim APIs, work in a **lic** checkout (or sibling `li` clone); open that workspace in Cursor — the aggregates repo cannot host those packages.

---

## Tier-2 catalog ↔ engine concerns

These rows in `catalog.toml` (`repo = "lic"`, `tier = 2`) map to common game / sim engineering threads:

| Catalog `id` | Typical engine thread |
|--------------|------------------------|
| `rigid_body_stack` | Contact stacks, rigid dynamics |
| `cloth_swing` | Cloth / soft constraints |
| `sph_dam_break_2d` | Particle fluids (SPH) |
| `euler_fluid_2d` | Grid-based fluids |
| `advection_diffusion_2d` | Smoke / heat–like scalar transport |
| `wave_equation_2d` | 2D wave PDEs (fields, probes) |
| `wind_field_bc` | Wind / environment fields |
| `combustion_passive` | Passive scalar + flow (fire-ish) |
| `nbody_gravity`, `three_body` | N-body / reduced gravity proxies |
| `double_pendulum`, `harmonic_oscillator_chain` | Integrator stiffness / stability |
| `md_lennard_jones` | Molecular-style interactions (tier-2 MD) |
| `wave_equation_1d`, `heat_equation_2d` | Baseline PDE kernels |

Paths are `benchmarks/tier2_physics/<id>` on **lic**. Until those directories exist on **lic** `main`, audits may flag **catalog-only** gaps — see the sync plan below.

---

## Plans & issues (canonical)

| Link | Role |
|------|------|
| [Tier-2 gaming-physics catalog ↔ lic sync](../ecosystem/plans/2026-05-18-tier2-catalog-lic-sync.md) | Reconcile catalog paths with **lic** tree; [benchmarks#19](https://github.com/li-langverse/benchmarks/issues/19), [lic#24](https://github.com/li-langverse/lic/issues/24) |
| [Physics catalog expansion (2026-05-16)](../release-notes/2026-05-16-physics-catalog-expansion.md) | Release note when rows were extended |
| [Li master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) | Normative **PH-*** order (tier-1/2 goals) |
| [Benchmarks & simulations (lic)](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-benchmarks-and-simulations.md) | Harness ownership |
| [Phase-07 native HPC](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-phase-07-native-hpc.md) | Native / SIMD alignment |
| [Provability gaps](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) | **G-*** register — honest proof status |

Wider plan index: [plan-cross-links.md](../ecosystem/plan-cross-links.md).

**Related intent:** [li-language PR #6](https://github.com/li-langverse/li-language/pull/6) (tier-2 gaming-physics suite expansion — implementation still lands under **lic** harness paths per sync plan).

---

## Local workflow

1. Clone **lic** beside this repo (`LIC_ROOT=../lic` or `../li`).
2. Add or tune kernels under `lic/benchmarks/tier2_physics/<id>/` and run **lic**’s bench / CI.
3. After CSV paths exist, run `./scripts/ingest/ingest-lic.sh` here so `data/latest/summary.json` and Pages stay honest.

---

## Honesty

Do not improve dashboard color by editing `threshold_ratio_cpp` without real speedups — [benchmark-dashboard.md](../honesty/benchmark-dashboard.md).
