# Physics benchmark catalog expansion

**Date:** 2026-05-16  
**Repos:** benchmarks

## Summary

Extended `catalog.toml` with Tier-2 physics benches implemented in `lic` (fluids, rigid stack, weather, chemistry, EM, quantum).

## Changes

- Added catalog rows: `advection_diffusion_2d`, `wave_equation_2d`, `sph_dam_break_2d`, `rigid_body_stack`, `three_body_pure`, `wind_field_bc`, `combustion_passive`, `orbit_two_body`, `fdtd_waveguide_2d`, `schrodinger_1d_barrier`
- Added agent skill pointer: `.cursor/skills/research-li-numerics`

## Verification

- `./scripts/ingest/ingest-lic.sh` with sibling `lic` checkout (when CSV available)
