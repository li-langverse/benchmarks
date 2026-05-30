# Bench improver digest — proactive sweep 1780140538756

**Generated:** 2026-05-30 · **Agent:** `bench_improver` · **north_star_fit:** blazingly-fast (PH-5b, PH-7e)

Canonical run artifact: [`data/runs/bench_improver-1780140538756.md`](../../../data/runs/bench_improver-1780140538756.md)

## Executive summary

- Published dashboard oracle (`summary.json` @ 2026-05-29T18:47Z): **6 RED, 2 YELLOW**, 137 green — tier-1 lic matmul + GMRES block public competitiveness.
- Preflight briefing compact slice (@ 2026-05-30T10:00) incorrectly reports 0 red — **oracle mismatch**; trust `benchmark-failures-report.sh` until full ingest on `main`.
- **lic PR #499** restores matmul MIR fast paths (claimed naive → 1.0×) but **CI failing** on linux/macos — highest-priority unblock.
- Three **li-math ML reds** are stub parity gaps, not lic codegen.
- Two **tier-2 thermostat yellows** (~1.29–1.30×) deferred until tier-1 crisis clears.
- `horner_pure_li` green at 0.75×; swarm gap registry entries for matmul/gmres are stale.

## Deliverable / findings

See full CSV citations, history deltas, and SOTA notes in the run artifact linked above.

## Recommended issues/PRs

1. **lic:** unblock + merge PR #499 (`fix(bench): restore tier-1 matmul MIR fast paths`).
2. **lic:** `matmul_blocked` micro-kernel follow-up for ≤1.2× (post-#499).
3. **lic:** `num_gmres` wrapper overhead reduction.
4. **benchmarks:** full tier-1 ingest via `ingest-lic.sh` after lic merge.
5. **lic:** close stale `gap-benchmark-red-*` swarm entries after ingest proof.
6. **li-math:** ML conv2d/MLP stub performance (separate repo).

## Deferred

Tier-2 thermostat micro-opt, briefing/oracle reconciliation, catalog path gaps (117), Lean-gated parallel/simd beyond matmul — see run artifact.
