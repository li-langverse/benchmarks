# Workload scale & algorithm depth (tier-2)

**Honesty:** Many **gaming / engineering** catalog rows are **`workload_class = v0_gaming`** — scaled harness loops, not production game-engine physics. Full reference sims use **`workload_class = full`**.

## Timing methodology (now in harness)

| Item | Policy |
|------|--------|
| Repetitions | **3–6** timed runs after **1** warmup (`--runs`, default **5**) |
| Reported value | **Median** wall time → CSV `value` |
| Spread | Sample **stdev** (seconds) → CSV `value_stdev` |
| Runs count | CSV `timing_runs` |

Ingest exposes `li_value_stdev`, `cpp_value_stdev`, `timing_runs` on `summary.json` rows. **Green/yellow/red** still uses median ratio only; use stdev to judge sub-ms noise.

## Workload classes (`catalog.toml`)

| Class | Count (tier-2) | Use for claims |
|-------|----------------|----------------|
| **full** | 9 | “Li within 1.2× C++ on reference PDE/N-body/MD (C kernel)” |
| **v0_gaming** | 10 | Harness / roadmap only — not “beats Unreal/Houdini” |
| *(tier-1 micro)* | 8 | SIMD/GEMM — separate from simulation |

## v0_gaming — algorithm status (lic)

See **`lic/benchmarks/tier2_physics/BENCH_WORKLOADS.md`** for per-bench grid/steps and what is still missing (Euler equations, SPH density, cloth grid, rigid contact, etc.).

**Production-scale proxy today:** `advection_diffusion_2d` (128×128, 15k steps), `wave_equation_2d`, `sph_dam_break_2d` (512 particles after 2026-05 scale-up).

## Recent scale / algorithm bumps (lic)

- **euler_fluid_2d**, **wind_field_bc:** 64×64 2D advection (was 1D micro-loops).
- **schrodinger_1d_barrier:** barrier potential + 128 cells.
- **sph_dam_break_2d:** 512 particles, 10k steps.
- **fdtd**, **combustion**, **cloth**, **rigid_body_stack:** larger N/steps.

Regenerate: `python3 benchmarks/harness/bench.py --tier 12 --runs 5` in **lic**, then `build_summary.py` in **benchmarks**.
