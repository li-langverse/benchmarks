# Benchmark matrix (full)

Generated: 2026-05-21T12:05:31.801670+00:00

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
| keepalive_pipelining | 232,360 | 93,595 | 62,240 | 216,744 | 22,280 |
| lb_least_conn | — | 45,794 | — | — | — |
| lb_peer_down | — | 49,980 | — | — | — |
| lb_round_robin | — | 43,623 | — | — | — |
| proxy_loopback | — | 58,771 | — | — | — |
| static_large | 7,891 | 8,946 | 8,791 | 9,105 | 2,619 |
| static_small | 139,091 | 86,561 | 53,065 | 165,505 | 28,772 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.364× | lic |
| matmul_blocked | 1 | red | 1.525× | lic |
| matmul_naive | 1 | red | 1.360× | lic |
| reduce_sum | 1 | green | 0.989× | lic |
| simd_dot | 1 | green | 0.014× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 0.992× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.000× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.744× | lic |
| heat_equation_2d | 2 | green | 1.076× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 1.000× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.005× | lic |
| three_body | 2 | green | 1.000× | lic |
| wave_equation_1d | 2 | green | 0.993× | lic |
| wave_equation_2d | 2 | green | 1.019× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| https_static | 5 | green | 1.000× | lic |
| keepalive_pipelining | 5 | green | 0.403× | lis |
| lb_least_conn | 5 | unknown | — | lis |
| lb_peer_down | 5 | unknown | — | lis |
| lb_round_robin | 5 | unknown | — | lis |
| proxy_loopback | 5 | unknown | — | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | red | 1.134× | lis |
| static_small | 5 | green | 0.622× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

