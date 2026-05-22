# Benchmark matrix (full)

Generated: 2026-05-22T15:56:49.752237+00:00

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
| static_small | 135,466 | — | — | — | — | — | — |
| keepalive_pipelining | 235,097 | — | — | — | — | — | — |
| static_large | FAIL | — | — | — | — | — | — |
| proxy_loopback | 9,121 | — | — | — | — | — | — |
| lb_round_robin | 9,141 | — | — | — | — | — | — |
| lb_least_conn | 11,405 | — | — | — | — | — | — |
| lb_peer_down | 18,455 | — | — | — | — | — | — |

**Li notes:** `static_large`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | other oracles N/A |
| https_static | skip | other oracles N/A |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | red | 5.857× | lic |
| matmul_blocked | 1 | green | 0.575× | lic |
| matmul_naive | 1 | green | 0.667× | lic |
| reduce_sum | 1 | green | 0.811× | lic |
| simd_dot | 1 | red | 1.478× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.001× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.013× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.993× | lic |
| heat_equation_2d | 2 | green | 0.988× | lic |
| md_lennard_jones | 2 | green | 0.000× | lic |
| nbody_gravity | 2 | green | 1.006× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.003× | lic |
| three_body | 2 | green | 0.982× | lic |
| wave_equation_1d | 2 | green | 1.023× | lic |
| wave_equation_2d | 2 | green | 0.970× | lic |
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
| rate_limit_429 | 5 | unknown | — | lic |
| static_large | 5 | unknown | — | lis |
| static_small | 5 | unknown | — | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

