# Benchmark matrix (full)

Generated: 2026-05-25T17:45:32.634600+00:00

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
| static_small | — | 17,365 | — | — | 7,592 | — | — |
| keepalive_pipelining | — | 25,032 | — | — | 15,010 | — | — |
| static_large | — | 4,057 | — | — | 1,107 | — | — |
| proxy_loopback | no bin | 12,373 | — | — | — | — | — |
| lb_round_robin | no bin | 20,458 | — | — | — | — | — |
| lb_least_conn | no bin | 11,998 | — | — | — | — | — |
| lb_peer_down | no bin | 25,578 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: no_li_httpd_bin; `lb_peer_down`: no_li_httpd_bin; `lb_round_robin`: no_li_httpd_bin; `proxy_loopback`: no_li_httpd_bin

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | no_li_httpd_bin | other oracles N/A |
| https_static | — | nginx=362 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | green | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| cfd_fvm_face_flux | 1 | green | 1.107× | lic |
| cfd_pimple | 1 | green | 1.107× | lic |
| cfd_piso | 1 | green | 1.107× | lic |
| cfd_simple | 1 | green | 1.107× | lic |
| cfd_turbulence_k_epsilon | 1 | green | 1.107× | lic |
| cfd_turbulence_k_omega_sst | 1 | green | 1.107× | lic |
| fea_gauss_quadrature | 1 | green | 1.107× | lic |
| fea_linear_elasticity | 1 | green | 1.107× | lic |
| fea_mesh_tri_tet | 1 | green | 1.107× | lic |
| fea_solver_direct | 1 | green | 1.107× | lic |
| fea_solver_iterative | 1 | green | 1.107× | lic |
| fea_stiffness_assembly | 1 | green | 1.107× | lic |
| fft_1d_fixed | 1 | green | 1.151× | lic |
| horner_pure_li | 1 | green | 0.541× | lic |
| matmul_blocked | 1 | yellow | 1.243× | lic |
| matmul_blocked_N1024 | 1 | unknown | — | lic |
| matmul_naive | 1 | green | 1.171× | lic |
| matmul_naive_N1024 | 1 | unknown | — | lic |
| ml_conv2d_forward | 1 | green | 1.171× | li-math |
| ml_mlp_forward | 1 | green | 1.171× | li-math |
| ml_mlp_train_step | 1 | green | 1.171× | li-math |
| nbody_barnes_hut | 1 | green | 0.004× | lic |
| num_cg | 1 | green | 1.083× | lic |
| num_cholesky | 1 | green | 0.911× | lic |
| num_eig_symmetric | 1 | green | 0.229× | lic |
| num_fft_r2c | 1 | green | 0.650× | lic |
| num_gmres | 1 | red | 1.685× | lic |
| num_integ_euler | 1 | red | 1.398× | lic |
| num_integ_rk4 | 1 | green | 1.160× | lic |
| num_integ_semi_implicit | 1 | green | 0.795× | lic |
| num_integ_symplectic | 1 | yellow | 1.247× | lic |
| num_integ_verlet | 1 | red | 1.345× | lic |
| num_opt_bfgs | 1 | green | 0.427× | lic |
| num_opt_line_search | 1 | red | 2.000× | lic |
| num_quadrature_gauss | 1 | green | 0.583× | lic |
| num_rng_pcg | 1 | green | 1.056× | lic |
| num_root_newton | 1 | green | 0.753× | lic |
| num_sparse_mv | 1 | green | 0.967× | lic |
| reduce_sum | 1 | green | 0.406× | lic |
| simd_dot | 1 | green | 1.053× | lic |
| viz_colormap | 1 | green | 0.406× | lig |
| viz_decimate | 1 | green | 0.406× | lig |
| viz_inspector_panels | 1 | green | 0.406× | lig |
| viz_linked_views | 1 | green | 0.406× | lig |
| viz_marching_cubes | 1 | green | 0.406× | lig |
| viz_pipeline_graph | 1 | green | 0.406× | lig |
| viz_resample | 1 | green | 0.406× | lig |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.142× | lic |
| auto_bicycle_model | 2 | green | 1.142× | lic |
| auto_dyn_rk4 | 2 | green | 1.142× | lic |
| auto_sensor_raycast | 2 | green | 1.142× | lic |
| bio_proteinmpnn | 2 | green | 1.107× | lic |
| bio_rfdiffusion | 2 | green | 1.107× | lic |
| bio_rosetta_energy | 2 | green | 1.107× | lic |
| bio_rotamer_packing | 2 | green | 1.107× | lic |
| cloth_swing | 2 | red | 1.368× | lic |
| combustion_passive | 2 | green | 0.871× | lic |
| double_pendulum | 2 | green | 0.971× | lic |
| drug_docking_diffusion | 2 | green | 1.107× | lic |
| drug_docking_score_vina | 2 | green | 1.107× | lic |
| drug_fep_alchemical | 2 | green | 1.107× | lic |
| drug_litl_stages | 2 | green | 1.107× | lic |
| drug_ml_retrain_loop | 2 | green | 1.107× | lic |
| euler_fluid_2d | 2 | green | 0.827× | lic |
| fdtd_waveguide_2d | 2 | green | 1.081× | lic |
| harmonic_oscillator_chain | 2 | yellow | 1.310× | lic |
| heat_equation_2d | 2 | green | 1.107× | lic |
| md_barostat_parrinello_rahman | 2 | green | 0.875× | lic |
| md_constraints_rattle | 2 | green | 1.026× | lic |
| md_constraints_shake | 2 | green | 1.175× | lic |
| md_energy_drift | 2 | green | 1.002× | lic |
| md_init_fcc_mb | 2 | yellow | 1.274× | lic |
| md_integrator_leapfrog | 2 | green | 0.827× | lic |
| md_integrator_verlet | 2 | green | 0.990× | lic |
| md_lennard_jones | 2 | green | 0.004× | lic |
| md_longrange_ewald | 2 | green | 1.083× | lic |
| md_longrange_pme | 2 | green | 1.147× | lic |
| md_neighbor_cell_list | 2 | green | 1.176× | lic |
| md_neighbor_verlet_skin | 2 | green | 1.015× | lic |
| md_oracle_external | 2 | green | 0.829× | lic |
| md_thermostat_berendsen | 2 | green | 1.103× | lic |
| md_thermostat_nose_hoover | 2 | green | 1.114× | lic |
| nbody_gravity | 2 | green | 0.827× | lic |
| orbit_two_body | 2 | red | 1.688× | lic |
| pde_cfl_timestep | 2 | green | 1.107× | lic |
| pde_heat_implicit_jacobi | 2 | green | 1.107× | lic |
| qm_ase_calculator | 2 | green | 1.107× | lic |
| qm_ccsd | 2 | green | 1.107× | lic |
| qm_dft_grid_becke | 2 | green | 1.107× | lic |
| qm_dft_grid_lebedev | 2 | green | 1.107× | lic |
| qm_dft_hybrid_exchange | 2 | green | 1.107× | lic |
| qm_dft_scf_energy | 2 | green | 1.107× | lic |
| qm_dft_xc_gga | 2 | green | 1.107× | lic |
| qm_dft_xc_lda | 2 | green | 1.107× | lic |
| qm_dft_xc_mgga | 2 | green | 1.107× | lic |
| qm_dispersion_d3 | 2 | green | 1.107× | lic |
| qm_ecp | 2 | green | 1.107× | lic |
| qm_eri_density_fitting | 2 | green | 1.107× | lic |
| qm_eri_os | 2 | green | 1.107× | lic |
| qm_eri_screening | 2 | green | 1.107× | lic |
| qm_geom_opt_bfgs | 2 | green | 1.107× | lic |
| qm_geom_opt_internal | 2 | green | 1.107× | lic |
| qm_grad_analytical | 2 | green | 1.107× | lic |
| qm_gto_eval | 2 | green | 1.107× | lic |
| qm_hf_canonical_ortho | 2 | green | 1.107× | lic |
| qm_hf_diis | 2 | green | 1.107× | lic |
| qm_hf_fock_build | 2 | green | 1.107× | lic |
| qm_job_queue_io | 2 | green | 1.107× | lic |
| qm_kinetic_integrals | 2 | green | 1.107× | lic |
| qm_mp2 | 2 | green | 1.107× | lic |
| qm_nuclear_attraction | 2 | green | 1.107× | lic |
| qm_overlap_integrals | 2 | green | 1.107× | lic |
| qm_property_dipole | 2 | green | 1.107× | lic |
| qm_property_freq | 2 | green | 1.107× | lic |
| qm_scf_solver | 2 | green | 1.107× | lic |
| qm_tddft_casida | 2 | green | 1.107× | lic |
| qm_tddft_rpa | 2 | green | 1.107× | lic |
| qm_xtb_gfn | 2 | green | 1.107× | lic |
| ragdoll_chain | 2 | green | 0.717× | lic |
| rigid_body_stack | 2 | green | 1.115× | lic |
| rigid_broadphase_bvh | 2 | green | 1.107× | lic |
| rigid_broadphase_sap | 2 | green | 1.107× | lic |
| rigid_constraints | 2 | green | 1.107× | lic |
| rigid_contact_solver | 2 | green | 1.107× | lic |
| rigid_semi_implicit | 2 | green | 1.107× | lic |
| robo_ik_jacobian | 2 | green | 1.067× | lic |
| robo_multibody_step | 2 | green | 1.067× | lic |
| robo_plan_prm | 2 | green | 1.067× | lic |
| robo_plan_rrt | 2 | green | 1.067× | lic |
| robo_traj_opt | 2 | green | 1.067× | lic |
| schrodinger_1d_barrier | 2 | red | 1.767× | lic |
| sph_dam_break_2d | 2 | green | 1.196× | lic |
| three_body | 2 | green | 1.067× | lic |
| three_body_pure | 2 | green | 0.834× | lic |
| wave_equation_1d | 2 | green | 0.930× | lic |
| wave_equation_2d | 2 | green | 0.789× | lic |
| wind_field_bc | 2 | green | 1.062× | lic |

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
| am_export_gcode_3mf | 3 | green | 1.142× | lic |
| am_infill_grid_lines | 3 | green | 1.142× | lic |
| am_infill_gyroid | 3 | green | 1.142× | lic |
| am_offset_perimeters | 3 | green | 1.142× | lic |
| am_plane_mesh_intersect | 3 | green | 1.142× | lic |
| am_polygon_clip | 3 | green | 1.142× | lic |
| am_slice_layers | 3 | green | 1.142× | lic |
| am_support_tree | 3 | green | 1.142× | lic |
| am_thermal_warp | 3 | green | 1.142× | lic |
| am_toolpath_arcs | 3 | green | 1.142× | lic |
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

