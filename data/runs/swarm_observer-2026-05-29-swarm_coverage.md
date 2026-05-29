# Swarm observer digest — `swarm_coverage`

> Meta-audit · 2026-05-29T19:05Z · north_star_fit: ecosystem + ai orchestration

## Executive summary

- **Health: degraded.** Grade **D** (64.8); not unattended-safe.
- **Critical:** 117 stuck SDK runs; high historical error volume (2599/24h in DB).
- **orch-r2 complete:** competitor_feature ingest + 12 vertical stub backlog patches.
- **54 open gaps** in registry (30 competitor, 21 plan_debt, 3 missing_package).
- **6 red benchmarks** — numerics lane active (`bench_improver`, `numerics_researcher`).
- **Briefing drift: low** — recommended agents align with heap plan priorities.
- **Programmatic heal idle** — empty retry_counts; meta-observer invoked correctly.
- **Next:** orch-r3 package sweep; stuck-run finalize; un-skip slow preflights.

## Deliverable / findings

See full report: [lic/data/runs/swarm_observer-orch-r2-competitor-stubs.md](../../../lic/data/runs/swarm_observer-orch-r2-competitor-stubs.md)

Evidence:

- `data/latest/ecosystem-quality-report.json`
- `data/latest/swarm-gap-actions.json`
- `data/latest/agent-briefing.json`
- `../lic/data/swarm-gap-registry/registry.yaml`
- `../lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r2-competitor-stubs.md`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| chore(benchmarks): publish competitive/verticals.toml on main | benchmarks | ecosystem |
| fix(control-plane): finalize stuck SDK runs | li-cursor-agents | swarm |
| research: PH-7e tier-1 matmul / gmres red rows | lic | numerics |

## Deferred

- orch-r3, orch-r4 orchestrator todos
- Master-plan plan_debt without backlog mapping
- HPC library competitor research (handoff-only)
