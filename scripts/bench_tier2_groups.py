#!/usr/bin/env python3
"""Named tier-2 physics shards for parallel nightly CI."""
from __future__ import annotations

TIER2_GROUP_MD: frozenset[str] = frozenset(
    {
        "md_lennard_jones",
        "md_barostat_parrinello_rahman",
        "md_constraints_rattle",
        "md_constraints_shake",
        "md_energy_drift",
        "md_init_fcc_mb",
        "md_integrator_leapfrog",
        "md_integrator_verlet",
        "md_longrange_ewald",
        "md_longrange_pme",
        "md_neighbor_cell_list",
        "md_neighbor_verlet_skin",
        "md_oracle_external",
        "md_thermostat_berendsen",
        "md_thermostat_nose_hoover",
        "three_body",
    }
)

TIER2_GROUP_PDE: frozenset[str] = frozenset(
    {
        "wave_equation_1d",
        "heat_equation_2d",
        "advection_diffusion_2d",
        "wave_equation_2d",
        "sph_dam_break_2d",
        "wind_field_bc",
        "combustion_passive",
        "fdtd_waveguide_2d",
        "schrodinger_1d_barrier",
        "euler_fluid_2d",
    }
)

TIER2_GROUP_MECH: frozenset[str] = frozenset(
    {
        "nbody_gravity",
        "harmonic_oscillator_chain",
        "double_pendulum",
        "rigid_body_stack",
        "three_body_pure",
        "orbit_two_body",
        "cloth_swing",
        "ragdoll_chain",
    }
)

TIER2_GROUPS: dict[str, frozenset[str]] = {
    "md": TIER2_GROUP_MD,
    "pde": TIER2_GROUP_PDE,
    "mech": TIER2_GROUP_MECH,
}
