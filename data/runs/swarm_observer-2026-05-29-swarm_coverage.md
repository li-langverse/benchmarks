# Swarm observer digest — `swarm_coverage`

> Meta-audit · 2026-05-29T19:08Z · north_star_fit: ecosystem + ai orchestration

## Executive summary

- **Health: degraded.** Grade **D** (66.3); not unattended-safe.
- **orch-r3 complete:** missing-package sweep — 3 open gaps, 5 backlog todos, explorer aligned.
- **53 open registry gaps** (30 competitor, 20 plan_debt, 3 missing_package).
- **Swarm execution:** 29+ stuck `running` in DB; 2925 historical errors; observer idle.
- **6 red benchmarks** — numerics lane active (`bench_improver`, `numerics_researcher`).
- **Briefing drift: low** — recommended agents match heap priorities.
- **PH-IO:** `std.summary` + `std.plot` missing → handoff `issue_planner` / `package_architect`.
- **Next:** orch-r4 ui_ux signals; stuck-run finalize; refresh stale control-plane report.

## Deliverable / findings

Full report: [lic/data/runs/swarm_observer-orch-r3-missing-package-sweep.md](../../../lic/data/runs/swarm_observer-orch-r3-missing-package-sweep.md)

Orchestrator note: [lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md](../../../lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md)

Evidence:

- `data/latest/ecosystem-quality-report.json`
- `data/latest/swarm-gap-actions.json`
- `data/latest/agent-briefing.json`
- `data/latest/ecosystem-explorer.json`
- `../lic/data/swarm-gap-registry/registry.yaml`
- `../lic/docs/ecosystem/ecosystem-package-backlog.md`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(std): PH-IO-7 `std.summary` for benchmark ingest | lic | PH-IO-7, ecosystem |
| feat(std): PH-IO-5 `std.plot` static dashboard hooks | lic | PH-IO-5, ecosystem |
| fix(control-plane): finalize stuck SDK runs | li-cursor-agents | swarm |
| research: PH-7e tier-1 matmul / gmres red rows | lic | numerics |

## Deferred

- `orch-r4-ui-ux-signals`
- Master-plan plan_debt without backlog mapping
- HPC competitor research (handoff-only)
