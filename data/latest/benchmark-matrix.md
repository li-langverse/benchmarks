# Benchmark matrix (full)

Generated: 2026-05-21T11:52:18.014422+00:00

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
| keepalive_pipelining | 223,327 | 95,678 | 66,731 | 247,621 | 30,930 |
| lb_least_conn | — | 67,004 | — | — | — |
| lb_peer_down | — | 65,027 | — | — | — |
| lb_round_robin | — | 71,539 | — | — | — |
| proxy_loopback | — | 77,412 | — | — | — |
| static_large | 9,156 | 8,999 | 8,889 | 9,166 | 3,196 |
| static_small | 138,867 | 83,177 | 52,565 | 185,305 | 28,925 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.818× | lic |
| matmul_blocked | 1 | green | 1.019× | lic |
| matmul_naive | 1 | green | 0.686× | lic |
| reduce_sum | 1 | green | 1.044× | lic |
| simd_dot | 1 | green | 0.014× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.012× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.007× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.889× | lic |
| heat_equation_2d | 2 | green | 0.838× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 0.998× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 0.998× | lic |
| three_body | 2 | green | 0.990× | lic |
| wave_equation_1d | 2 | green | 0.993× | lic |
| wave_equation_2d | 2 | green | 1.008× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| https_static | 5 | green | 1.000× | lic |
| keepalive_pipelining | 5 | green | 0.428× | lis |
| lb_least_conn | 5 | unknown | — | lis |
| lb_peer_down | 5 | unknown | — | lis |
| lb_round_robin | 5 | unknown | — | lis |
| proxy_loopback | 5 | unknown | — | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | green | 0.983× | lis |
| static_small | 5 | green | 0.599× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

