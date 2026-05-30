# Benchmark matrix (full)

Generated: 2026-05-30T09:57:30.712478+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **green** — 0 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | pass | pass | pass |
| command_injection_path | pass | pass | pass |
| connection_flood | pass | pass | pass |
| duplicate_content_length | pass | pass | pass |
| host_header_ssrf | pass | pass | pass |
| oversized_request_line | pass | pass | pass |
| path_traversal | pass | pass | pass |
| privilege_path_escalation | pass | pass | pass |
| reverse_shell_canary | pass | pass | pass |
| sensitive_file_read | pass | pass | pass |
| shellshock_user_agent | pass | pass | pass |
| slowloris | pass | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | — | 12,087 | — | — | 4,626 | — | — |
| keepalive_pipelining | — | 22,604 | — | — | 15,817 | — | — |
| static_large | — | 4,149 | — | — | 1,805 | — | — |
| proxy_loopback | no bin | 21,415 | — | — | — | — | — |
| lb_round_robin | no bin | 24,167 | — | — | — | — | — |
| lb_least_conn | no bin | 24,309 | — | — | — | — | — |
| lb_peer_down | no bin | 25,179 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: no_li_httpd_bin; `lb_peer_down`: no_li_httpd_bin; `lb_round_robin`: no_li_httpd_bin; `proxy_loopback`: no_li_httpd_bin

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | no_li_httpd_bin | other oracles N/A |
| https_static | skip | nginx=583 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | skip | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| cfd_fvm_face_flux | 1 | skip | — | lic |
| cfd_pimple | 1 | skip | — | lic |
| cfd_piso | 1 | skip | — | lic |
| cfd_simple | 1 | skip | — | lic |
| cfd_turbulence_k_epsilon | 1 | skip | — | lic |
| cfd_turbulence_k_omega_sst | 1 | skip | — | lic |
| fea_gauss_quadrature | 1 | skip | — | lic |
| fea_linear_elasticity | 1 | skip | — | lic |
| fea_mesh_tri_tet | 1 | skip | — | lic |
| fea_solver_direct | 1 | skip | — | lic |
| fea_solver_iterative | 1 | skip | — | lic |
| fea_stiffness_assembly | 1 | skip | — | lic |
| fft_1d_fixed | 1 | skip | — | lic |
| horner_pure_li | 1 | skip | — | lic |
| matmul_blocked | 1 | skip | — | lic |
| matmul_blocked_N1024 | 1 | skip | — | lic |
| matmul_naive | 1 | skip | — | lic |
| matmul_naive_N1024 | 1 | skip | — | lic |
| ml_conv2d_forward | 1 | skip | — | li-math |
| ml_mlp_forward | 1 | skip | — | li-math |
| ml_mlp_train_step | 1 | skip | — | li-math |
| nbody_barnes_hut | 1 | skip | — | lic |
| num_cg | 1 | skip | — | lic |
| num_cholesky | 1 | skip | — | lic |
| num_eig_symmetric | 1 | skip | — | lic |
| num_fft_r2c | 1 | skip | — | lic |
| num_gmres | 1 | skip | — | lic |
| num_integ_euler | 1 | skip | — | lic |
| num_integ_rk4 | 1 | skip | — | lic |
| num_integ_semi_implicit | 1 | skip | — | lic |
| num_integ_symplectic | 1 | skip | — | lic |
| num_integ_verlet | 1 | skip | — | lic |
| num_opt_bfgs | 1 | skip | — | lic |
| num_opt_line_search | 1 | skip | — | lic |
| num_quadrature_gauss | 1 | skip | — | lic |
| num_rng_pcg | 1 | skip | — | lic |
| num_root_newton | 1 | skip | — | lic |
| num_sparse_mv | 1 | skip | — | lic |
| reduce_sum | 1 | skip | — | lic |
| simd_dot | 1 | skip | — | lic |
| stdlib_binary_search | 1 | skip | — | lic |
| stdlib_deque_rotate | 1 | skip | — | lic |
| stdlib_dict_insert_lookup | 1 | skip | — | lic |
| stdlib_hash_flood | 1 | skip | — | lic |
| stdlib_heap_push_pop | 1 | skip | — | lic |
| stdlib_list_push_pop | 1 | skip | — | lic |
| stdlib_set_ops | 1 | skip | — | lic |
| stdlib_sort_int | 1 | skip | — | lic |
| viz_colormap | 1 | skip | — | lig |
| viz_decimate | 1 | skip | — | lig |
| viz_inspector_panels | 1 | skip | — | lig |
| viz_linked_views | 1 | skip | — | lig |
| viz_marching_cubes | 1 | skip | — | lig |
| viz_pipeline_graph | 1 | skip | — | lig |
| viz_resample | 1 | skip | — | lig |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | skip | — | lic |
| auto_bicycle_model | 2 | skip | — | lic |
| auto_dyn_rk4 | 2 | skip | — | lic |
| auto_sensor_raycast | 2 | skip | — | lic |
| bio_proteinmpnn | 2 | skip | — | lic |
| bio_rfdiffusion | 2 | skip | — | lic |
| bio_rosetta_energy | 2 | skip | — | lic |
| bio_rotamer_packing | 2 | skip | — | lic |
| cloth_swing | 2 | skip | — | lic |
| combustion_passive | 2 | skip | — | lic |
| double_pendulum | 2 | skip | — | lic |
| drug_docking_diffusion | 2 | skip | — | lic |
| drug_docking_score_vina | 2 | skip | — | lic |
| drug_fep_alchemical | 2 | skip | — | lic |
| drug_litl_stages | 2 | skip | — | lic |
| drug_ml_retrain_loop | 2 | skip | — | lic |
| euler_fluid_2d | 2 | skip | — | lic |
| fdtd_waveguide_2d | 2 | skip | — | lic |
| harmonic_oscillator_chain | 2 | skip | — | lic |
| heat_equation_2d | 2 | skip | — | lic |
| md_barostat_parrinello_rahman | 2 | skip | — | lic |
| md_constraints_rattle | 2 | skip | — | lic |
| md_constraints_shake | 2 | skip | — | lic |
| md_energy_drift | 2 | skip | — | lic |
| md_init_fcc_mb | 2 | skip | — | lic |
| md_integrator_leapfrog | 2 | skip | — | lic |
| md_integrator_verlet | 2 | skip | — | lic |
| md_lennard_jones | 2 | skip | — | lic |
| md_longrange_ewald | 2 | skip | — | lic |
| md_longrange_pme | 2 | skip | — | lic |
| md_neighbor_cell_list | 2 | skip | — | lic |
| md_neighbor_verlet_skin | 2 | skip | — | lic |
| md_oracle_external | 2 | skip | — | lic |
| md_thermostat_berendsen | 2 | skip | — | lic |
| md_thermostat_nose_hoover | 2 | skip | — | lic |
| nbody_gravity | 2 | skip | — | lic |
| orbit_two_body | 2 | skip | — | lic |
| pde_cfl_timestep | 2 | skip | — | lic |
| pde_heat_implicit_jacobi | 2 | skip | — | lic |
| qm_ase_calculator | 2 | skip | — | lic |
| qm_ccsd | 2 | skip | — | lic |
| qm_dft_grid_becke | 2 | skip | — | lic |
| qm_dft_grid_lebedev | 2 | skip | — | lic |
| qm_dft_hybrid_exchange | 2 | skip | — | lic |
| qm_dft_scf_energy | 2 | skip | — | lic |
| qm_dft_xc_gga | 2 | skip | — | lic |
| qm_dft_xc_lda | 2 | skip | — | lic |
| qm_dft_xc_mgga | 2 | skip | — | lic |
| qm_dispersion_d3 | 2 | skip | — | lic |
| qm_ecp | 2 | skip | — | lic |
| qm_eri_density_fitting | 2 | skip | — | lic |
| qm_eri_os | 2 | skip | — | lic |
| qm_eri_screening | 2 | skip | — | lic |
| qm_geom_opt_bfgs | 2 | skip | — | lic |
| qm_geom_opt_internal | 2 | skip | — | lic |
| qm_grad_analytical | 2 | skip | — | lic |
| qm_gto_eval | 2 | skip | — | lic |
| qm_hf_canonical_ortho | 2 | skip | — | lic |
| qm_hf_diis | 2 | skip | — | lic |
| qm_hf_fock_build | 2 | skip | — | lic |
| qm_job_queue_io | 2 | skip | — | lic |
| qm_kinetic_integrals | 2 | skip | — | lic |
| qm_mp2 | 2 | skip | — | lic |
| qm_nuclear_attraction | 2 | skip | — | lic |
| qm_overlap_integrals | 2 | skip | — | lic |
| qm_property_dipole | 2 | skip | — | lic |
| qm_property_freq | 2 | skip | — | lic |
| qm_scf_solver | 2 | skip | — | lic |
| qm_tddft_casida | 2 | skip | — | lic |
| qm_tddft_rpa | 2 | skip | — | lic |
| qm_xtb_gfn | 2 | skip | — | lic |
| ragdoll_chain | 2 | skip | — | lic |
| rigid_body_stack | 2 | skip | — | lic |
| rigid_broadphase_bvh | 2 | skip | — | lic |
| rigid_broadphase_sap | 2 | skip | — | lic |
| rigid_constraints | 2 | skip | — | lic |
| rigid_contact_solver | 2 | skip | — | lic |
| rigid_semi_implicit | 2 | skip | — | lic |
| robo_ik_jacobian | 2 | skip | — | lic |
| robo_multibody_step | 2 | skip | — | lic |
| robo_plan_prm | 2 | skip | — | lic |
| robo_plan_rrt | 2 | skip | — | lic |
| robo_traj_opt | 2 | skip | — | lic |
| schrodinger_1d_barrier | 2 | skip | — | lic |
| sph_dam_break_2d | 2 | skip | — | lic |
| three_body | 2 | skip | — | lic |
| three_body_pure | 2 | skip | — | lic |
| wave_equation_1d | 2 | skip | — | lic |
| wave_equation_2d | 2 | skip | — | lic |
| wind_field_bc | 2 | skip | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| https_static | 5 | skip | — | lis |
| keepalive_pipelining | 5 | skip | — | lis |
| lb_least_conn | 5 | skip | — | lis |
| lb_peer_down | 5 | skip | — | lis |
| lb_round_robin | 5 | skip | — | lis |
| proxy_loopback | 5 | skip | — | lic |
| rate_limit_429 | 5 | skip | — | benchmarks |
| static_large | 5 | skip | — | lis |
| static_small | 5 | skip | — | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | skip | — | lis |
| injection_blocked | 6 | skip | — | lidb |
| rls_bypass_blocked | 6 | skip | — | lidb |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| am_export_gcode_3mf | 3 | skip | — | lic |
| am_infill_grid_lines | 3 | skip | — | lic |
| am_infill_gyroid | 3 | skip | — | lic |
| am_offset_perimeters | 3 | skip | — | lic |
| am_plane_mesh_intersect | 3 | skip | — | lic |
| am_polygon_clip | 3 | skip | — | lic |
| am_slice_layers | 3 | skip | — | lic |
| am_support_tree | 3 | skip | — | lic |
| am_thermal_warp | 3 | skip | — | lic |
| am_toolpath_arcs | 3 | skip | — | lic |
| lip_smoke | 3 | skip | — | lip |
| lit_smoke | 3 | skip | — | lit |

