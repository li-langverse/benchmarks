# Benchmark matrix (full)

Generated: 2026-06-04T02:53:48.144778+00:00

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

| scenario | li | nginx | apache | lighttpd | caddy | traefik | node | bun | li/nginx |
|---|---|---|---|---|---|---|---|---|---|
| static_small | 4,030 | 109 | 660 | 5,171 | — | — | 1,759 | — | 37.00× |
| keepalive_pipelining | 5,457 | 149 | 1,426 | 6,528 | — | — | 2,845 | — | 36.58× |
| static_large | FAIL | 71 | 448 | 171 | — | — | 265 | — | — |
| proxy_loopback | 32,327 | 120 | 120 | 120 | — | — | — | — | 268.83× |
| lb_round_robin | 32,750 | 2,040 | 2,071 | 1,914 | — | — | — | — | 16.05× |
| lb_least_conn | 30,280 | 2,010 | 1,958 | 1,804 | — | — | — | — | 15.07× |
| lb_peer_down | 32,265 | 1,940 | 1,884 | 1,827 | — | — | — | — | 16.63× |

**Li notes:** `lb_least_conn`: verify_fail_caddy:/; `lb_peer_down`: verify_fail_caddy:/; `lb_round_robin`: verify_fail_caddy:/; `proxy_loopback`: verify_fail_caddy:/; `static_large`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | — | li=5,868; nginx=112; apache=1,041; lighttpd=5,706; caddy=1,706; traefik=120 |
| https_tls_matrix | — | li=5,688; nginx=119; apache=1,530; lighttpd=5,907; caddy=2,467; traefik=116 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | green | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| cfd_fvm_face_flux | 1 | unknown | — | lic |
| cfd_pimple | 1 | unknown | — | lic |
| cfd_piso | 1 | unknown | — | lic |
| cfd_simple | 1 | unknown | — | lic |
| cfd_turbulence_k_epsilon | 1 | unknown | — | lic |
| cfd_turbulence_k_omega_sst | 1 | unknown | — | lic |
| fea_gauss_quadrature | 1 | unknown | — | lic |
| fea_linear_elasticity | 1 | unknown | — | lic |
| fea_mesh_tri_tet | 1 | unknown | — | lic |
| fea_solver_direct | 1 | unknown | — | lic |
| fea_solver_iterative | 1 | unknown | — | lic |
| fea_stiffness_assembly | 1 | unknown | — | lic |
| fft_1d_fixed | 1 | unknown | — | lic |
| horner_pure_li | 1 | unknown | — | lic |
| matmul_blocked | 1 | unknown | — | lic |
| matmul_blocked_N1024 | 1 | unknown | — | lic |
| matmul_naive | 1 | unknown | — | lic |
| matmul_naive_N1024 | 1 | unknown | — | lic |
| ml_conv2d_forward | 1 | unknown | — | li-math |
| ml_mlp_forward | 1 | unknown | — | li-math |
| ml_mlp_train_step | 1 | unknown | — | li-math |
| nbody_barnes_hut | 1 | unknown | — | lic |
| num_cg | 1 | unknown | — | lic |
| num_cholesky | 1 | unknown | — | lic |
| num_eig_symmetric | 1 | unknown | — | lic |
| num_fft_r2c | 1 | unknown | — | lic |
| num_gmres | 1 | unknown | — | lic |
| num_integ_euler | 1 | unknown | — | lic |
| num_integ_rk4 | 1 | unknown | — | lic |
| num_integ_semi_implicit | 1 | unknown | — | lic |
| num_integ_symplectic | 1 | unknown | — | lic |
| num_integ_verlet | 1 | unknown | — | lic |
| num_opt_bfgs | 1 | unknown | — | lic |
| num_opt_line_search | 1 | unknown | — | lic |
| num_quadrature_gauss | 1 | unknown | — | lic |
| num_rng_pcg | 1 | unknown | — | lic |
| num_root_newton | 1 | unknown | — | lic |
| num_sparse_mv | 1 | unknown | — | lic |
| reduce_sum | 1 | unknown | — | lic |
| simd_dot | 1 | unknown | — | lic |
| stdlib_binary_search | 1 | unknown | — | lic |
| stdlib_deque_rotate | 1 | unknown | — | lic |
| stdlib_dict_insert_lookup | 1 | unknown | — | lic |
| stdlib_hash_flood | 1 | unknown | — | lic |
| stdlib_heap_push_pop | 1 | unknown | — | lic |
| stdlib_list_push_pop | 1 | unknown | — | lic |
| stdlib_set_ops | 1 | unknown | — | lic |
| stdlib_sort_int | 1 | unknown | — | lic |
| viz_colormap | 1 | unknown | — | lig |
| viz_decimate | 1 | unknown | — | lig |
| viz_inspector_panels | 1 | unknown | — | lig |
| viz_linked_views | 1 | unknown | — | lig |
| viz_marching_cubes | 1 | unknown | — | lig |
| viz_pipeline_graph | 1 | unknown | — | lig |
| viz_resample | 1 | unknown | — | lig |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | unknown | — | lic |
| auto_bicycle_model | 2 | unknown | — | lic |
| auto_dyn_rk4 | 2 | unknown | — | lic |
| auto_sensor_raycast | 2 | unknown | — | lic |
| bio_proteinmpnn | 2 | unknown | — | lic |
| bio_rfdiffusion | 2 | unknown | — | lic |
| bio_rosetta_energy | 2 | unknown | — | lic |
| bio_rotamer_packing | 2 | unknown | — | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | unknown | — | lic |
| drug_docking_diffusion | 2 | unknown | — | lic |
| drug_docking_score_vina | 2 | unknown | — | lic |
| drug_fep_alchemical | 2 | unknown | — | lic |
| drug_litl_stages | 2 | unknown | — | lic |
| drug_ml_retrain_loop | 2 | unknown | — | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| fdtd_waveguide_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | unknown | — | lic |
| heat_equation_2d | 2 | unknown | — | lic |
| md_barostat_parrinello_rahman | 2 | unknown | — | lic |
| md_constraints_rattle | 2 | unknown | — | lic |
| md_constraints_shake | 2 | unknown | — | lic |
| md_energy_drift | 2 | unknown | — | lic |
| md_init_fcc_mb | 2 | unknown | — | lic |
| md_integrator_leapfrog | 2 | unknown | — | lic |
| md_integrator_verlet | 2 | unknown | — | lic |
| md_lennard_jones | 2 | unknown | — | lic |
| md_longrange_ewald | 2 | unknown | — | lic |
| md_longrange_pme | 2 | unknown | — | lic |
| md_neighbor_cell_list | 2 | unknown | — | lic |
| md_neighbor_verlet_skin | 2 | unknown | — | lic |
| md_oracle_external | 2 | unknown | — | lic |
| md_thermostat_berendsen | 2 | unknown | — | lic |
| md_thermostat_nose_hoover | 2 | unknown | — | lic |
| nbody_gravity | 2 | unknown | — | lic |
| orbit_two_body | 2 | unknown | — | lic |
| pde_cfl_timestep | 2 | unknown | — | lic |
| pde_heat_implicit_jacobi | 2 | unknown | — | lic |
| qm_ase_calculator | 2 | unknown | — | lic |
| qm_ccsd | 2 | unknown | — | lic |
| qm_dft_grid_becke | 2 | unknown | — | lic |
| qm_dft_grid_lebedev | 2 | unknown | — | lic |
| qm_dft_hybrid_exchange | 2 | unknown | — | lic |
| qm_dft_scf_energy | 2 | unknown | — | lic |
| qm_dft_xc_gga | 2 | unknown | — | lic |
| qm_dft_xc_lda | 2 | unknown | — | lic |
| qm_dft_xc_mgga | 2 | unknown | — | lic |
| qm_dispersion_d3 | 2 | unknown | — | lic |
| qm_ecp | 2 | unknown | — | lic |
| qm_eri_density_fitting | 2 | unknown | — | lic |
| qm_eri_os | 2 | unknown | — | lic |
| qm_eri_screening | 2 | unknown | — | lic |
| qm_geom_opt_bfgs | 2 | unknown | — | lic |
| qm_geom_opt_internal | 2 | unknown | — | lic |
| qm_grad_analytical | 2 | unknown | — | lic |
| qm_gto_eval | 2 | unknown | — | lic |
| qm_hf_canonical_ortho | 2 | unknown | — | lic |
| qm_hf_diis | 2 | unknown | — | lic |
| qm_hf_fock_build | 2 | unknown | — | lic |
| qm_job_queue_io | 2 | unknown | — | lic |
| qm_kinetic_integrals | 2 | unknown | — | lic |
| qm_mp2 | 2 | unknown | — | lic |
| qm_nuclear_attraction | 2 | unknown | — | lic |
| qm_overlap_integrals | 2 | unknown | — | lic |
| qm_property_dipole | 2 | unknown | — | lic |
| qm_property_freq | 2 | unknown | — | lic |
| qm_scf_solver | 2 | unknown | — | lic |
| qm_tddft_casida | 2 | unknown | — | lic |
| qm_tddft_rpa | 2 | unknown | — | lic |
| qm_xtb_gfn | 2 | unknown | — | lic |
| ragdoll_chain | 2 | unknown | — | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| rigid_broadphase_bvh | 2 | unknown | — | lic |
| rigid_broadphase_sap | 2 | unknown | — | lic |
| rigid_constraints | 2 | unknown | — | lic |
| rigid_contact_solver | 2 | unknown | — | lic |
| rigid_semi_implicit | 2 | unknown | — | lic |
| robo_ik_jacobian | 2 | unknown | — | lic |
| robo_multibody_step | 2 | unknown | — | lic |
| robo_plan_prm | 2 | unknown | — | lic |
| robo_plan_rrt | 2 | unknown | — | lic |
| robo_traj_opt | 2 | unknown | — | lic |
| schrodinger_1d_barrier | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | unknown | — | lic |
| three_body | 2 | unknown | — | lic |
| three_body_pure | 2 | unknown | — | lic |
| wave_equation_1d | 2 | unknown | — | lic |
| wave_equation_2d | 2 | unknown | — | lic |
| wind_field_bc | 2 | unknown | — | lic |

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
| am_export_gcode_3mf | 3 | unknown | — | lic |
| am_infill_grid_lines | 3 | unknown | — | lic |
| am_infill_gyroid | 3 | unknown | — | lic |
| am_offset_perimeters | 3 | unknown | — | lic |
| am_plane_mesh_intersect | 3 | unknown | — | lic |
| am_polygon_clip | 3 | unknown | — | lic |
| am_slice_layers | 3 | unknown | — | lic |
| am_support_tree | 3 | unknown | — | lic |
| am_thermal_warp | 3 | unknown | — | lic |
| am_toolpath_arcs | 3 | unknown | — | lic |
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

