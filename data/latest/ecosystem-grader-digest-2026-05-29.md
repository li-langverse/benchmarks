# Ecosystem grader digest — 2026-05-29 (proactive)

**Agent:** `ecosystem_grader` · **Run:** `ecosystem_grader-1780082990753` · **Source:** proactive  
**Full run log:** `data/runs/ecosystem_grader-1780082990753.md`  
**Scorecard:** `data/latest/ecosystem-quality-report.json` — grade **C** (70.9), `unattended_safe: false`  
**north_star_fit:** PH-2i, PH-5b, PH-7e — orchestration before implementers; proof → easy → fast

## Executive summary

- **Grade C (70.9)** — not unattended-safe; **swarm_execution** (55) is the binding constraint.
- **28% error rate** on 25 terminal SDK runs; **95** runs stuck `running` — dispatch `swarm_observer` first.
- **6 red** tier-1 benchmarks on dashboard (stale ingest); local harness shows partial greens on active branches.
- **6/8** goal-directed runners stopped; **25/90** plan todos pending; **`agents_live: 0`**.
- **27** open swarm gaps (5 packages, 22 plan_debt); PR surface quiet (**0** open PRs).
- **2 preflight fails:** agent-kit audit (9 repos) + security CWE audit (JSON decode).
- **Next meta lane:** `swarm_observer` → `workspace_sweeper` → governance → numerics ingest.

See `data/runs/ecosystem_grader-1780082990753.md` for dimension drill-down, findings table, dispatch order, and human blockers.
