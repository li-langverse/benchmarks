# Benchmark matrix (full)

Generated: 2026-05-21T13:50:17.090999+00:00

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
| static_small | 135,343 | 85,276 | 52,230 | 177,456 | 29,382 | — | 1.59× |
| keepalive_pipelining | 233,938 | 95,637 | 64,981 | 235,147 | 29,975 | — | 2.45× |
| static_large | 9,226 | 8,857 | 8,820 | 9,084 | 3,141 | — | 1.04× |
| proxy_loopback | FAIL | 77,204 | — | — | — | — | — |
| lb_round_robin | FAIL | 68,477 | — | — | — | — | — |
| lb_least_conn | FAIL | 71,359 | — | — | — | — | — |
| lb_peer_down | FAIL | 72,199 | — | — | — | — | — |

**Li notes:** `lb_least_conn`: wrk_parse_fail_li; `lb_peer_down`: wrk_parse_fail_li; `lb_round_robin`: wrk_parse_fail_li; `proxy_loopback`: wrk_parse_fail_li

## HTTP verify / feature gates (non-RPS)

| scenario | li | other oracles |
|---|---|---|
| rate_limit_429 | pass | N/A (li-only or pending) |
| https_static | skip | N/A (li-only or pending) |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.444× | lic |
| matmul_blocked | 1 | red | 1.535× | lic |
| matmul_naive | 1 | red | 1.400× | lic |
| reduce_sum | 1 | green | 0.978× | lic |
| simd_dot | 1 | green | 0.015× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.111× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.000× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | yellow | 1.215× | lic |
| heat_equation_2d | 2 | green | 0.959× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 1.000× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 0.995× | lic |
| three_body | 2 | green | 0.998× | lic |
| wave_equation_1d | 2 | green | 1.001× | lic |
| wave_equation_2d | 2 | green | 0.999× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| https_static | 5 | green | 1.000× | lic |
| keepalive_pipelining | 5 | green | 0.390× | lis |
| lb_least_conn | 5 | unknown | — | lis |
| lb_peer_down | 5 | unknown | — | lis |
| lb_round_robin | 5 | unknown | — | lis |
| proxy_loopback | 5 | unknown | — | lic |
| rate_limit_429 | 5 | green | 1.000× | lic |
| static_large | 5 | green | 0.948× | lis |
| static_small | 5 | green | 0.519× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

