# Benchmark matrix (full)

Generated: 2026-05-28T03:51:28.551784+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **red** — 12 failures / 36 cells

| exploit | li | nginx | apache |
|---|---|---|---|
| bad_method | FAIL(no_li) | pass | pass |
| command_injection_path | FAIL(no_li) | pass | pass |
| connection_flood | FAIL(no_li) | pass | pass |
| duplicate_content_length | FAIL(no_li) | pass | pass |
| host_header_ssrf | FAIL(no_li) | pass | pass |
| oversized_request_line | FAIL(no_li) | pass | pass |
| path_traversal | FAIL(no_li) | pass | pass |
| privilege_path_escalation | FAIL(no_li) | pass | pass |
| reverse_shell_canary | FAIL(no_li) | pass | pass |
| sensitive_file_read | FAIL(no_li) | pass | pass |
| shellshock_user_agent | FAIL(no_li) | pass | pass |
| slowloris | FAIL(no_li) | pass | pass |

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|
| static_small | — | 72,590 | 26,439 | 165,643 | 25,772 | — | — |
| keepalive_pipelining | — | 78,445 | 53,785 | 213,373 | 25,332 | — | — |
| static_large | — | 8,848 | 7,378 | 4,859 | 2,872 | — | — |
| proxy_loopback | — | 75,112 | 45,640 | 17,811 | — | — | — |
| lb_round_robin | — | 68,217 | 51,808 | 32,448 | — | — | — |
| lb_least_conn | — | 66,915 | 51,483 | 32,257 | — | — | — |
| lb_peer_down | — | 68,639 | 49,755 | 29,895 | — | — | — |

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | — | other oracles N/A |
| https_static | skip | apache=809; lighttpd=912 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| cfd_fvm_face_flux | 1 | green | 1.025× | lic |
| cfd_pimple | 1 | green | 1.025× | lic |
| cfd_piso | 1 | green | 1.025× | lic |
| cfd_simple | 1 | green | 1.025× | lic |
| cfd_turbulence_k_epsilon | 1 | green | 1.025× | lic |
| cfd_turbulence_k_omega_sst | 1 | green | 1.025× | lic |
| fea_gauss_quadrature | 1 | green | 1.025× | lic |
| fea_linear_elasticity | 1 | green | 1.025× | lic |
| fea_mesh_tri_tet | 1 | green | 1.025× | lic |
| fea_solver_direct | 1 | green | 1.025× | lic |
| fea_solver_iterative | 1 | green | 1.025× | lic |
| fea_stiffness_assembly | 1 | green | 1.025× | lic |
| fft_1d_fixed | 1 | green | 1.006× | lic |
| horner_pure_li | 1 | green | 0.750× | lic |
| matmul_blocked | 1 | red | 1.549× | lic |
| matmul_blocked_N1024 | 1 | unknown | — | lic |
| matmul_naive | 1 | red | 1.333× | lic |
| matmul_naive_N1024 | 1 | unknown | — | lic |
| ml_conv2d_forward | 1 | red | 1.333× | li-math |
| ml_mlp_forward | 1 | red | 1.333× | li-math |
| ml_mlp_train_step | 1 | red | 1.333× | li-math |
| nbody_barnes_hut | 1 | green | 0.981× | lic |
| num_cg | 1 | green | 1.000× | lic |
| num_cholesky | 1 | green | 1.167× | lic |
| num_eig_symmetric | 1 | green | 0.800× | lic |
| num_fft_r2c | 1 | green | 1.000× | lic |
| num_gmres | 1 | red | 1.400× | lic |
| num_integ_euler | 1 | green | 1.000× | lic |
| num_integ_rk4 | 1 | green | 0.909× | lic |
| num_integ_semi_implicit | 1 | green | 1.000× | lic |
| num_integ_symplectic | 1 | green | 1.000× | lic |
| num_integ_verlet | 1 | green | 0.963× | lic |
| num_opt_bfgs | 1 | green | 1.000× | lic |
| num_opt_line_search | 1 | green | 1.026× | lic |
| num_quadrature_gauss | 1 | green | 1.000× | lic |
| num_rng_pcg | 1 | green | 1.000× | lic |
| num_root_newton | 1 | green | 1.000× | lic |
| num_sparse_mv | 1 | green | 0.986× | lic |
| reduce_sum | 1 | green | 1.023× | lic |
| simd_dot | 1 | green | 0.881× | lic |
| stdlib_binary_search | 1 | unknown | — | lic |
| stdlib_deque_rotate | 1 | unknown | — | lic |
| stdlib_dict_insert_lookup | 1 | unknown | — | lic |
| stdlib_hash_flood | 1 | unknown | — | lic |
| stdlib_heap_push_pop | 1 | unknown | — | lic |
| stdlib_list_push_pop | 1 | unknown | — | lic |
| stdlib_set_ops | 1 | unknown | — | lic |
| stdlib_sort_int | 1 | unknown | — | lic |
| viz_colormap | 1 | green | 1.023× | lig |
| viz_decimate | 1 | green | 1.023× | lig |
| viz_inspector_panels | 1 | green | 1.023× | lig |
| viz_linked_views | 1 | green | 1.023× | lig |
| viz_marching_cubes | 1 | green | 1.023× | lig |
| viz_pipeline_graph | 1 | green | 1.023× | lig |
| viz_resample | 1 | green | 1.023× | lig |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.083× | lic |
| auto_bicycle_model | 2 | green | 1.083× | lic |
| auto_dyn_rk4 | 2 | green | 1.083× | lic |
| auto_sensor_raycast | 2 | green | 1.083× | lic |
| bio_proteinmpnn | 2 | green | 1.025× | lic |
| bio_rfdiffusion | 2 | green | 1.025× | lic |
| bio_rosetta_energy | 2 | green | 1.025× | lic |
| bio_rotamer_packing | 2 | green | 1.025× | lic |
| cloth_swing | 2 | green | 1.154× | lic |
| combustion_passive | 2 | green | 1.000× | lic |
| double_pendulum | 2 | green | 1.054× | lic |
| drug_docking_diffusion | 2 | green | 1.025× | lic |
| drug_docking_score_vina | 2 | green | 1.025× | lic |
| drug_fep_alchemical | 2 | green | 1.025× | lic |
| drug_litl_stages | 2 | green | 1.025× | lic |
| drug_ml_retrain_loop | 2 | green | 1.025× | lic |
| euler_fluid_2d | 2 | green | 1.000× | lic |
| fdtd_waveguide_2d | 2 | green | 1.000× | lic |
| harmonic_oscillator_chain | 2 | green | 0.859× | lic |
| heat_equation_2d | 2 | green | 1.025× | lic |
| md_barostat_parrinello_rahman | 2 | green | 0.988× | lic |
| md_constraints_rattle | 2 | green | 1.005× | lic |
| md_constraints_shake | 2 | green | 0.982× | lic |
| md_energy_drift | 2 | green | 1.012× | lic |
| md_init_fcc_mb | 2 | green | 1.009× | lic |
| md_integrator_leapfrog | 2 | green | 1.028× | lic |
| md_integrator_verlet | 2 | green | 0.969× | lic |
| md_lennard_jones | 2 | green | 0.981× | lic |
| md_longrange_ewald | 2 | green | 0.986× | lic |
| md_longrange_pme | 2 | green | 1.013× | lic |
| md_neighbor_cell_list | 2 | green | 1.007× | lic |
| md_neighbor_verlet_skin | 2 | green | 0.994× | lic |
| md_oracle_external | 2 | green | 0.992× | lic |
| md_thermostat_berendsen | 2 | yellow | 1.303× | lic |
| md_thermostat_nose_hoover | 2 | yellow | 1.291× | lic |
| nbody_gravity | 2 | green | 0.922× | lic |
| orbit_two_body | 2 | green | 1.000× | lic |
| pde_cfl_timestep | 2 | green | 1.025× | lic |
| pde_heat_implicit_jacobi | 2 | green | 1.025× | lic |
| qm_ase_calculator | 2 | green | 1.025× | lic |
| qm_ccsd | 2 | green | 1.025× | lic |
| qm_dft_grid_becke | 2 | green | 1.025× | lic |
| qm_dft_grid_lebedev | 2 | green | 1.025× | lic |
| qm_dft_hybrid_exchange | 2 | green | 1.025× | lic |
| qm_dft_scf_energy | 2 | green | 1.025× | lic |
| qm_dft_xc_gga | 2 | green | 1.025× | lic |
| qm_dft_xc_lda | 2 | green | 1.025× | lic |
| qm_dft_xc_mgga | 2 | green | 1.025× | lic |
| qm_dispersion_d3 | 2 | green | 1.025× | lic |
| qm_ecp | 2 | green | 1.025× | lic |
| qm_eri_density_fitting | 2 | green | 1.025× | lic |
| qm_eri_os | 2 | green | 1.025× | lic |
| qm_eri_screening | 2 | green | 1.025× | lic |
| qm_geom_opt_bfgs | 2 | green | 1.025× | lic |
| qm_geom_opt_internal | 2 | green | 1.025× | lic |
| qm_grad_analytical | 2 | green | 1.025× | lic |
| qm_gto_eval | 2 | green | 1.025× | lic |
| qm_hf_canonical_ortho | 2 | green | 1.025× | lic |
| qm_hf_diis | 2 | green | 1.025× | lic |
| qm_hf_fock_build | 2 | green | 1.025× | lic |
| qm_job_queue_io | 2 | green | 1.025× | lic |
| qm_kinetic_integrals | 2 | green | 1.025× | lic |
| qm_mp2 | 2 | green | 1.025× | lic |
| qm_nuclear_attraction | 2 | green | 1.025× | lic |
| qm_overlap_integrals | 2 | green | 1.025× | lic |
| qm_property_dipole | 2 | green | 1.025× | lic |
| qm_property_freq | 2 | green | 1.025× | lic |
| qm_scf_solver | 2 | green | 1.025× | lic |
| qm_tddft_casida | 2 | green | 1.025× | lic |
| qm_tddft_rpa | 2 | green | 1.025× | lic |
| qm_xtb_gfn | 2 | green | 1.025× | lic |
| ragdoll_chain | 2 | green | 1.000× | lic |
| rigid_body_stack | 2 | green | 1.000× | lic |
| rigid_broadphase_bvh | 2 | green | 1.025× | lic |
| rigid_broadphase_sap | 2 | green | 1.025× | lic |
| rigid_constraints | 2 | green | 1.025× | lic |
| rigid_contact_solver | 2 | green | 1.025× | lic |
| rigid_semi_implicit | 2 | green | 1.025× | lic |
| robo_ik_jacobian | 2 | green | 1.105× | lic |
| robo_multibody_step | 2 | green | 1.105× | lic |
| robo_plan_prm | 2 | green | 1.105× | lic |
| robo_plan_rrt | 2 | green | 1.105× | lic |
| robo_traj_opt | 2 | green | 1.105× | lic |
| schrodinger_1d_barrier | 2 | green | 1.000× | lic |
| sph_dam_break_2d | 2 | green | 1.071× | lic |
| three_body | 2 | green | 1.105× | lic |
| three_body_pure | 2 | green | 1.014× | lic |
| wave_equation_1d | 2 | green | 1.088× | lic |
| wave_equation_2d | 2 | green | 1.059× | lic |
| wind_field_bc | 2 | green | 1.000× | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| https_static | 5 | unknown | — | lis |
| keepalive_pipelining | 5 | unknown | — | lis |
| lb_least_conn | 5 | unknown | — | lis |
| lb_peer_down | 5 | unknown | — | lis |
| lb_round_robin | 5 | unknown | — | lis |
| proxy_loopback | 5 | unknown | — | lic |
| rate_limit_429 | 5 | unknown | — | benchmarks |
| static_large | 5 | unknown | — | lis |
| static_small | 5 | unknown | — | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |
| injection_blocked | 6 | unknown | — | lidb |
| rls_bypass_blocked | 6 | unknown | — | lidb |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| am_export_gcode_3mf | 3 | green | 1.083× | lic |
| am_infill_grid_lines | 3 | green | 1.083× | lic |
| am_infill_gyroid | 3 | green | 1.083× | lic |
| am_offset_perimeters | 3 | green | 1.083× | lic |
| am_plane_mesh_intersect | 3 | green | 1.083× | lic |
| am_polygon_clip | 3 | green | 1.083× | lic |
| am_slice_layers | 3 | green | 1.083× | lic |
| am_support_tree | 3 | green | 1.083× | lic |
| am_thermal_warp | 3 | green | 1.083× | lic |
| am_toolpath_arcs | 3 | green | 1.083× | lic |
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

