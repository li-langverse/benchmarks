# Benchmark matrix (full)

Generated: 2026-05-21T10:10:58.696302+00:00

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

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 216,833 | 95,551 | 65,714 | 245,944 | 27,705 |
| lb_least_conn | 163,029 | 68,559 | — | — | — |
| lb_peer_down | 159,101 | 72,551 | — | — | — |
| lb_round_robin | 156,930 | 71,685 | — | — | — |
| proxy_loopback | 157,554 | 74,445 | — | — | — |
| static_large | 9,233 | 8,298 | 7,593 | 8,944 | 3,206 |
| static_small | 115,905 | 81,851 | 52,212 | 162,307 | 28,462 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.500× | lic |
| matmul_blocked | 1 | green | 1.020× | lic |
| matmul_naive | 1 | green | 0.714× | lic |
| reduce_sum | 1 | green | 0.983× | lic |
| simd_dot | 1 | green | 0.010× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 0.981× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.004× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.978× | lic |
| heat_equation_2d | 2 | green | 0.979× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 0.989× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.000× | lic |
| three_body | 2 | green | 1.000× | lic |
| wave_equation_1d | 2 | green | 1.079× | lic |
| wave_equation_2d | 2 | green | 1.024× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| keepalive_pipelining | 5 | green | 0.441× | lis |
| lb_least_conn | 5 | green | 0.420× | lis |
| lb_peer_down | 5 | green | 0.456× | lis |
| lb_round_robin | 5 | green | 0.457× | lis |
| proxy_loopback | 5 | green | 0.638× | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | green | 0.899× | lis |
| static_small | 5 | green | 0.706× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

