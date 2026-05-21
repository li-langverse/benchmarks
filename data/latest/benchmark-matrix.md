# Benchmark matrix (full)

Generated: 2026-05-21T09:46:06.788829+00:00

Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`

## HTTP exploits (tier 5)

Status: **unknown** — 0 failures / 0 cells

_No exploit_report.csv — run `./scripts/run-tier5-http-exploits.sh`_

## HTTP performance (RPS)

| scenario | li | nginx | apache | lighttpd | node |
|---|---|---|---|---|---|
| keepalive_pipelining | 203,477 | 77,406 | 54,105 | 202,775 | 22,100 |
| lb_least_conn | 153,270 | 71,259 | — | — | — |
| lb_peer_down | 159,298 | 71,292 | — | — | — |
| lb_round_robin | 158,913 | 71,130 | — | — | — |
| proxy_loopback | 98,364 | 50,739 | — | — | — |
| static_large | 8,920 | 7,335 | 6,386 | 8,009 | 2,793 |
| static_small | 141,072 | 83,929 | 46,649 | 148,220 | 28,563 |

## Correctness

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier0_stability | 0 | unknown | — | lic |

## Micro

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| horner_pure_li | 1 | green | 0.545× | lic |
| matmul_blocked | 1 | red | 1.339× | lic |
| matmul_naive | 1 | green | 0.658× | lic |
| reduce_sum | 1 | green | 0.979× | lic |
| simd_dot | 1 | green | 0.014× | lic |

## Physics

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| advection_diffusion_2d | 2 | green | 1.022× | lic |
| cloth_swing | 2 | unknown | — | lic |
| combustion_passive | 2 | unknown | — | lic |
| double_pendulum | 2 | green | 1.038× | lic |
| euler_fluid_2d | 2 | unknown | — | lic |
| harmonic_oscillator_chain | 2 | green | 0.999× | lic |
| heat_equation_2d | 2 | green | 1.101× | lic |
| md_lennard_jones | 2 | green | 0.001× | lic |
| nbody_gravity | 2 | green | 0.999× | lic |
| rigid_body_stack | 2 | unknown | — | lic |
| sph_dam_break_2d | 2 | green | 1.008× | lic |
| three_body | 2 | green | 1.000× | lic |
| wave_equation_1d | 2 | green | 0.977× | lic |
| wave_equation_2d | 2 | green | 1.017× | lic |
| wind_field_bc | 2 | unknown | — | lic |

## HTTP catalog gates

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| keepalive_pipelining | 5 | green | 0.380× | lis |
| lb_least_conn | 5 | green | 0.511× | lis |
| lb_peer_down | 5 | green | 0.428× | lis |
| lb_round_robin | 5 | green | 0.508× | lis |
| proxy_loopback | 5 | green | 0.299× | lic |
| static_large | 5 | red | 1.287× | lis |
| static_small | 5 | green | 0.595× | lis |

## Security

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| tier5_http_exploits | 5 | unknown | — | lis |

## Tooling

| benchmark | tier | status | ratio | repo |
|---|---|---|---|---|
| lip_smoke | 3 | unknown | — | lip |
| lit_smoke | 3 | unknown | — | lit |

