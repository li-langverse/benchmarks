# Benchmark matrix (full)

Generated: 2026-05-21T10:36:56.439638+00:00

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
| keepalive_pipelining | 208,697 | 96,160 | 58,195 | 232,308 | 24,043 |
| lb_least_conn | 123,980 | 44,777 | — | — | — |
| lb_peer_down | 128,000 | 52,321 | — | — | — |
| lb_round_robin | 99,822 | 50,853 | — | — | — |
| proxy_loopback | 152,310 | 79,787 | — | — | — |
| static_large | 7,872 | 8,391 | 8,759 | 9,126 | 2,764 |
| static_small | 137,930 | 85,304 | 50,717 | 184,667 | 29,007 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.444× | lic |
| matmul_blocked | 1 | green | 0.972× | lic |
| matmul_naive | 1 | green | 0.971× | lic |
| reduce_sum | 1 | green | 1.004× | lic |
| simd_dot | 1 | green | 0.012× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 0.940× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.004× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 1.000× | lic |
| heat_equation_2d | 2 | green | 1.023× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 1.002× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.001× | lic |
| three_body | 2 | green | 1.000× | lic |
| wave_equation_1d | 2 | green | 0.959× | lic |
| wave_equation_2d | 2 | green | 1.008× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| keepalive_pipelining | 5 | green | 0.461× | lis |
| lb_least_conn | 5 | green | 0.361× | lis |
| lb_peer_down | 5 | green | 0.409× | lis |
| lb_round_robin | 5 | green | 0.509× | lis |
| proxy_loopback | 5 | green | 0.607× | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | yellow | 1.066× | lis |
| static_small | 5 | green | 0.619× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

