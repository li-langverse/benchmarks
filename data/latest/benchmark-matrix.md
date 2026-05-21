# Benchmark matrix (full)

Generated: 2026-05-21T10:23:54.100800+00:00

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
| keepalive_pipelining | 230,780 | 90,186 | 65,389 | 249,801 | 30,429 |
| lb_least_conn | 159,087 | 71,132 | — | — | — |
| lb_peer_down | 158,374 | 64,322 | — | — | — |
| lb_round_robin | 158,140 | 70,253 | — | — | — |
| proxy_loopback | 153,843 | 79,488 | — | — | — |
| static_large | 9,360 | 9,028 | 8,846 | 8,927 | 3,180 |
| static_small | 136,342 | 83,192 | 52,747 | 173,141 | 28,919 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.444× | lic |
| matmul_blocked | 1 | red | 1.453× | lic |
| matmul_naive | 1 | green | 1.042× | lic |
| reduce_sum | 1 | green | 0.994× | lic |
| simd_dot | 1 | green | 0.014× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.011× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 0.999× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.834× | lic |
| heat_equation_2d | 2 | green | 0.914× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 1.002× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.006× | lic |
| three_body | 2 | green | 1.000× | lic |
| wave_equation_1d | 2 | green | 1.012× | lic |
| wave_equation_2d | 2 | green | 1.041× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| keepalive_pipelining | 5 | green | 0.391× | lis |
| lb_least_conn | 5 | green | 0.447× | lis |
| lb_peer_down | 5 | green | 0.406× | lis |
| lb_round_robin | 5 | green | 0.444× | lis |
| proxy_loopback | 5 | green | 0.475× | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | green | 0.965× | lis |
| static_small | 5 | green | 0.610× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

