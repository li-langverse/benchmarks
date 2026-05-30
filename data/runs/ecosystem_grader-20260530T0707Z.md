# Ecosystem grader digest — `ecosystem_grader-20260530T0707Z`

**Date:** 2026-05-30T07:07Z  
**Agent:** ecosystem_grader (proactive sweep)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (regenerated 2026-05-30T07:07:16Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T07:06Z)  
**north_star_fit:** PH-5b (tier-1 competitive), provable-before-fast — no gate weakening

---

## Executive summary

- **Grade D** · **overall score 69.8 / 100** · **unattended-safe: no** (`ecosystem-quality-report.json`: `grade`, `overall_score`, `unattended_safe`).
- Score dropped from prior **C (78.1)** after refresh: **gap_pressure** fell (27→54 open gaps, severity upgraded to high) and **swarm_execution** fell (90→70; 50% incomplete rate in local run sample).
- **Briefing P0 preserved:** `proof_gap_researcher` (provability_holes) and `workspace_sweeper` (lic dirty on `perf/7e-matmul-blocked-codegen-20260530`) stay ahead of heap numerics despite `coord_numerics` priority 20.
- **Meta lane first:** scorecard orders `swarm_observer` → `gap_explorer` before implementers; aligns with degraded `swarm_execution` + `gap_pressure` dimensions.
- **Six red benchmark rows** (dashboard ingest @ 2026-05-29T18:47Z); local autoresearch shows `matmul_naive` likely stale — delegate **bench_improver** + ecosystem-audit refresh, not novel numerics.
- **Goal-directed loops starved:** 6/8 runners stopped, 24 plan todos pending, `agents_live: 0` — httpd loop active but last agent exits **124** (timeout) on perf soak todos.
- **Control-plane:** 7,553 historical `error` runs vs 21 `running`; local JSON sample shows 110 “running” stubs — **swarm_observer** should reconcile SDK terminalization.
- **Human-only:** no open org PRs; **lic#439** local-ci failure; **org_agent_kit_audit** exit 1 (9 repos missing/drifted kit); 8 preflights skipped (`--skip-slow`).

---

## Dimension drill-down

### briefing_health (77.0)

Briefing is present with 13 recommended agents and healthy ecosystem/org CI preflights (exit 0). Weakness is **operational coverage**: one preflight failed (`org_agent_kit_audit`, exit 1 — 9 repos missing or drifted agent-kit) and eight slow paths skipped (plan_audit, pr_program, ci_bug_triage, security_cwe_audit, etc.), so plan/PR/security signals are stale relative to the 07:06Z briefing timestamp. Scorecard finding `preflight-failures` / `preflight-skipped` both apply. Refresh via full preflight (drop `--skip-slow` in automation) and dispatch **plan_verifier** after plan_audit runs.

### ecosystem_posture (65.0)

Org CI posture is strong (0 repos missing CI on main, 0 failed PRs, 0 open PRs in audit). The dimension is dragged by **six red tier-1/2 benchmark rows** (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`) and secondary doc debt (10 repos without live pages). No failed-PR fire, but numerics debt blocks “blazingly-fast” pillar after proof. Route **numerics_researcher** / **bench_improver** under `coord_numerics`; refresh `ecosystem-audit.py` ingest after lic codegen lands.

### goal_directed_health (70.0)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`, 2026-05-30T07:07Z): 8 runners, **6 not running** (`compiler-studio`, `sim-algo`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research`), **24 pending todos** of 92, **`agents_live: 0`**. Only **httpd** reports `running: true` (soak fixture process) but `agent_live: false` with pending `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` and recent `agent_exit: 124`. Finding `goal-runners-stopped` is high severity — restart or reschedule plan loops; **plan_verifier** for backlog truth vs master plan.

### swarm_execution (70.0)

Local run dir sample (n=120): **110 running**, **10 terminal**, **5 incomplete**, **0 errors** in sample; **incomplete_rate 0.5** among terminal rows triggers `swarm-incomplete-rate` and `swarm-many-running`. Control-plane DB (full history): 7,553 `error`, 377 `finished`, 24 `incomplete`, 21 `running` — historical error volume is high but not reflected in the 120-file sample’s error_count. Delegate **swarm_observer** for status reconciliation, stuck SDK runs, and prompt/supervisor fixes on **li-cursor-agents** (PR + `npm test`, no protected-branch push).

### gap_pressure (70.0)

`swarm-gap-actions.json`: **54 open gaps** — `competitor_feature: 30`, `plan_debt: 21`, `missing_package: 3` (std.plot, std.summary, line-profiler seeds). Severity upgraded to **high** (`swarm-gap-backlog`). Briefing still lists only 2 missing std modules for **gap_explorer**; registry reconcile is broader. **gap_explorer** + **swarm_observer** apply pipeline before **implementation_gaps** floods implementers.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| benchmark-red-rows | high | `data/latest/ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| goal-runners-stopped | high | `lic/data/goal-directed-agents/snapshot.json` | plan loop owners / `plan_verifier` |
| swarm-gap-backlog | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| preflight-failures | medium | `data/latest/agent-briefing.json` → `preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| preflight-skipped | medium | `data/latest/agent-briefing.json` → `preflight_runs` (--skip-slow) | orchestrator / human (enable slow preflight) |
| swarm-incomplete-rate | medium | `li-cursor-agents/data/runs` (+ CP `agent_runs` incomplete) | `swarm_observer` |
| swarm-many-running | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| repos-missing-live-docs | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

---

## Recommended dispatch order

Merged **scorecard** `recommended_agents` with **briefing P0** (briefing wins on ties when cited):

1. **proof_gap_researcher** — briefing P0: provability_holes research goal (priority 9); proof-before-perf.
2. **workspace_sweeper** — briefing P0: lic dirty (`perf/7e-matmul-blocked-codegen-20260530`, 3 files); run `./li-tests/run_all.sh` before sweep commit.
3. **swarm_observer** — scorecard: `swarm_execution` &lt; 75; incomplete rate + stuck running rows.
4. **gap_explorer** — scorecard: `gap_pressure` &lt; 80; 54 registry gaps vs briefing’s 2 std modules.
5. **plan_verifier** — scorecard + briefing: plan-completion-audit (166 open items); requires plan_audit preflight.
6. **implementation_gaps** — briefing: cross-check plan vs implementation (after verifier).
7. **agent_kit_maintainer** — preflight exit 1: 9 repos (li-demo, li-httpd, li-language, li-net, li-std-*, lic/lis/roadmap drift).
8. **bench_improver** / **numerics_researcher** — heap `coord_numerics` P20 + red rows (after meta lanes).
9. **bug_fixer** → **code_implementer** — lic#439 local-ci failure (work_queue size 1).
10. **docs_maintainer**, **pr_branch_opener**, **security_auditor** — briefing queue (docs, 132 orphan branches, CWE catalog gaps).

**Do not contradict briefing P0:** numerics heap tasks remain important but follow proof + workspace + meta reconciliation.

---

## Human-only blockers

| Blocker | Detail |
|---------|--------|
| Slow preflight disabled | 8 scripts skipped (`--skip-slow`) — plan_audit, pr_program, ci_bug_triage, security_cwe_audit not in this cycle |
| Agent deliverable gate off | `LI_CURSOR_AGENTS_ENABLED` unset — no scan of agent PR completion |
| lic PR #439 | [lic#439](https://github.com/li-langverse/lic/pull/439) local-ci exit 1 — needs human/log review before merge |
| Agent-kit canonical sync | 9 org repos missing or drifted from kit `1.3.5+6018e18bf2ed91f4` — may need org-wide rollout approval |
| Goal loop timeouts | httpd todos `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exited 124 — wrk soak may need longer budget or human gate tweak |
| No open merge queue | 0 open PRs — merge-first automation idle; branch hygiene (132 unpushed PR branches) is organizational debt |

No missing API keys surfaced in this briefing cycle.

---

## Agent deliverable checklist

<!-- li-agent -->
## Agent deliverable

- [x] Regenerated `ecosystem-quality-report.json` via `python3 scripts/ecosystem-quality-grade.py`
- [x] Cited scorecard fields (no manual re-score)
- [x] Dimension narratives + findings table + dispatch order
- [x] Control-plane SQL spot-check (`agent_runs` status histogram)
- [x] Goal-directed snapshot reviewed (`lic/data/goal-directed-agents/snapshot.json`)
- [ ] **swarm_observer** PR on `li-cursor-agents` (run terminalization / incomplete handling)
- [ ] **gap_explorer** reconcile `swarm-gap-actions.json` (54 open) with briefing std gaps
- [ ] Full preflight without `--skip-slow` (human/automation config)
- [ ] Refresh ecosystem-audit benchmark ingest after lic tier-1 fixes land
<!-- /li-agent -->

---

## Deliverable / findings (agent-specific)

### Handoff matrix

| Signal | Delegate to |
|--------|-------------|
| Incomplete rate 50% + 110 running stubs (local sample) | `swarm_observer` |
| 54 open gaps (30 competitor_feature) | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks + stale ingest | `bench_improver`, `ci_maintainer` (ingest refresh) |
| 6 stopped goal runners + 24 pending todos | Plan loops / `plan_verifier` |
| lic dirty + matmul_blocked codegen branch | `workspace_sweeper` then `code_implementer` |

### Control-plane evidence

```text
agent_runs status histogram (full DB):
  error: 7553 | finished: 377 | incomplete: 24 | running: 21
Recent incomplete: docs_maintainer, ecosystem_grader, bench_improver, agent_kit_maintainer
```

### Goal-directed runners (stopped)

| id | branch | plan_pending | note |
|----|--------|--------------|------|
| compiler-studio | cursor/compiler-studio-plan-loop | yes | `running: false` |
| sim-algo | cursor/sim-algo-plan-loop | yes | stopped |
| studio-ui-ux | cursor/studio-ui-ux-plan-loop | yes | stopped |
| sim-md-research | cursor/sim-md-research-loop | yes | stopped |
| sim-chem-research | cursor/sim-chem-research-loop | yes | stopped |
| security-research | cursor/security-research-loop | yes | stopped |
| httpd | cursor/httpd-plan-continue | 2 todos | soak running; agent timeout 124 |

---

## Recommended issues/PRs

| Title (suggested) | Repo | Labels / notes |
|-------------------|------|----------------|
| chore: sync org agent-kit to 1.3.5+6018e18 | li-demo, li-httpd, li-language, li-net, li-std-core, li-std-math | `agent-kit`, `ecosystem` |
| fix(local-ci): lic#439 failure | lic | `bug`, `ci` — work_queue P0 |
| perf(7e): matmul_blocked pure_li ≤1.2× cpp | lic | `PH-7e`, `PH-5b` — branch `perf/7e-matmul-blocked-codegen-20260530` |
| docs: enable GitHub Pages for 10 repos without live docs | lic, lip, lit, lis, roadmap, li-net, li-httpd, li-std-*, li-demo | `docs` |
| chore: open PRs for 132 orphan agent branches | org-wide | `pr_branch_opener` backlog |
| research: provability_holes goal | lic / lean | `proof_gap_researcher` P0 |
| meta: reconcile stuck `running` agent run records | li-cursor-agents | `swarm_observer` |
| gap: std.plot + std.summary packages | li-std-* | `gap_explorer` |

---

## Deferred

- **pr_program / merge_plan automation** — 0 open PRs; merge-first idle until branches opened.
- **security_cwe_audit full pass** — skipped `--skip-slow`; Top25 catalog gaps (19) tracked but not blocking scorecard.
- **132 pr_branch_opener branches** — hygiene debt; defer until meta lanes stabilize (avoid PR flood).
- **ML benchmark reds** (`ml_conv2d_forward`, `ml_mlp_*`) — li-math / algo_registry; not tier-1 lic harness alone.
- **Competitor_feature gaps (30)** — registry apply pipeline; no single implementer until `gap_explorer` triages.
- **Provability gate changes** — none proposed; all work stays proof-before-perf.

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Prior numerics sweep: `benchmarks/data/runs/autoresearch-1780124755372.md`
- Vision: `roadmap/docs/ecosystem/vision-and-roadmap.md`
