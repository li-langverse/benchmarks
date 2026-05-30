# Ecosystem grader digest — `ecosystem_grader-20260530T0806Z`

**Date:** 2026-05-30T08:06Z  
**Agent:** ecosystem_grader (proactive sweep)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (regenerated 2026-05-30T08:06:03Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T08:04Z)  
**north_star_fit:** PH-2f / PH-5b / PH-7e — proof-before-perf; no gate weakening

---

## Executive summary

- **Grade D** · **overall score 67.8 / 100** · **unattended-safe: no** (`ecosystem-quality-report.json`: `grade`, `overall_score`, `unattended_safe`).
- **−3.0 vs prior pass** (70.8 / C @ 07:37Z): `swarm_execution` fell 70→**60** (`incomplete_rate` **0.40** on last 10 terminal runs); `briefing_health` 84→**77** (8 preflights skipped under `--skip-slow`).
- **Meta lanes degraded:** `swarm_execution` 60, `gap_pressure` 70 (57 open gaps), `briefing_health` 77 — scorecard routes **swarm_observer** and **gap_explorer** before implementers.
- **Briefing P0 (respect over heap):** `proof_gap_researcher` (provability_holes priority 9) → `workspace_sweeper` (2 dirty repos) → `plan_verifier` → `implementation_gaps`.
- **Goal-directed loops starved:** 6/8 runners not running, 26 plan todos pending, `agents_live: 0`; **httpd** wrk-soak todos exit **124** (timeout); **studio-ui-ux** just closed `studio-ux-14-native-sdl-ci`.
- **Ecosystem posture:** 6 red benchmark rows (ingest stale @ 2026-05-29), 0 failed PRs, 0 repos missing CI; lic dirty on `perf/bench-improver-matmul-simd-j-20260530`.
- **Preflight:** 1 failure (`org_agent_kit_audit` exit 1 — 9 repos); 8 skipped (`--skip-slow`); `cwe_feed_sync` exit 0 (Top25 missing_in_catalog=19).
- **Human-only:** lic#439 local-ci; 133 orphan branches; `LI_CURSOR_AGENTS_ENABLED` unset; httpd soak timeout budget.

---

## Dimension drill-down

### briefing_health (77.0)

Briefing is present with **13 recommended agents** and core fast preflights green (`ecosystem_audit`, `org_ci_audit`, `merge_plan`, `cwe_feed_sync`, `workspace_dirty_sweep` all exit 0). Weakness: **8 scripts skipped** (`plan_audit`, `explorer`, `ci_bug_triage`, `pr_program`, etc.) under `--skip-slow` — finding `preflight-skipped` (medium). Single non-zero exit: **`org_agent_kit_audit`** (9 repos missing/drifted kit `1.3.5+6018e18bf2ed91f4`) — finding `preflight-failures` (medium). `agent_deliverable_gate` still skipped (`LI_CURSOR_AGENTS_ENABLED` unset). Dispatch **plan_verifier** to refresh plan audit on next full preflight; **agent_kit_maintainer** for kit drift.

### ecosystem_posture (67.0)

Org CI posture is clean: **0** repos missing CI on main, **0** open/failed PRs in ecosystem audit. Dimension held down by **six red benchmark rows** (`matmul_blocked` 1.549×, `matmul_naive` 1.333×, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres` 1.4× — PH-5b/7e) plus **8 repos without live docs**. Finding `benchmark-red-rows` (high). Route **bench_improver** + **numerics_researcher** under `coord_numerics` (heap P20) after meta reconciliation; refresh benchmark ingest after lic matmul SIMD work lands.

### goal_directed_health (70.0)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`, 2026-05-30T08:05Z): **8 runners**, **6 not running** (`compiler-studio`, `sim`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research`), **26 pending todos** of 97, **`agents_live: 0`**. **httpd** and **swarm-observer** show `running: true` (tier5 soak fixture PID) but `agent_live: false`; httpd last todos `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exited **124**. **studio-ui-ux** completed wave-2 SDL CI (`studio-ux-14-native-sdl-ci` @ 08:05Z); active todo `studio-ux-15-wgpu-readback`. Finding `goal-runners-stopped` (high). Delegate plan loop restarts or **plan_verifier** backlog reconciliation.

### swarm_execution (60.0)

Local sample (n=120): **110 running**, **10 terminal**, **1 error**, **4 incomplete** → `error_rate` **0.10**, `incomplete_rate` **0.40**. Findings `swarm-incomplete-rate` (medium), `swarm-many-running` (medium). Control-plane DB (24h): **7186 error**, 380 finished, 25 running, 5 incomplete — historical error volume dominates; recent terminal batch @ 07:56–07:57Z shows concurrent SDK failures (`implementation_gaps`, `pr_reviewer`, `workspace_sweeper`, `agent_kit_maintainer`). Many local JSON runs still marked `"status": "running"` despite terminal traces — delegate **swarm_observer** for terminalization and status mapping on **li-cursor-agents** (PR + `npm test`).

### gap_pressure (70.0)

`swarm-gap-actions.json`: **57 open gaps** — `competitor_feature: 30`, `plan_debt: 24`, `missing_package: 3` (`std.plot`, `std.summary`, line-profiler seed). Finding `swarm-gap-backlog` (high). Briefing lists **2 missing std modules** for **gap_explorer**; registry is broader. **gap_explorer** + **swarm_observer** apply pipeline before **implementation_gaps** floods implementers.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| benchmark-red-rows | high | `data/latest/ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| goal-runners-stopped | high | `lic/data/goal-directed-agents/snapshot.json` | plan loop owners / `plan_verifier` |
| swarm-gap-backlog | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| preflight-failures | medium | `data/latest/agent-briefing.json` → `preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| preflight-skipped | medium | `data/latest/agent-briefing.json` → `preflight_runs` (--skip-slow) | orchestrator / full preflight cycle |
| swarm-incomplete-rate | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| swarm-many-running | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| repos-missing-live-docs | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

---

## Recommended dispatch order

Merged **scorecard** `recommended_agents` with **briefing** `recommended_agents` (briefing wins on ties):

1. **proof_gap_researcher** — briefing P0: research goal `provability_holes` eligible (priority 9); aligns with active lic branch `research/provability-cycle17-mat2-fma-lean-drift-2026-05-30`.
2. **workspace_sweeper** — briefing P0: **2** dirty repos — lic (`perf/bench-improver-matmul-simd-j-20260530`, 6 safe files) + benchmarks (`chore/agent-docs_maintainer-ecosystem-audit-*`, history JSON).
3. **swarm_observer** — scorecard: `swarm_execution` &lt; 75; 40% incomplete rate + 110 “running” stubs; SDK terminalization.
4. **gap_explorer** — scorecard: `gap_pressure` &lt; 80; 57 registry gaps vs briefing’s 2 std modules.
5. **plan_verifier** — scorecard + briefing: plan-completion-audit (166 findings); run full `plan_audit` preflight when `--skip-slow` lifted.
6. **implementation_gaps** — briefing: cross-check plan vs implementation (after verifier).
7. **agent_kit_maintainer** — preflight exit 1: li-demo, li-httpd, li-language, li-net, li-std-core, li-std-math (missing); lic, lis, roadmap (drift).
8. **ci_maintainer** — scorecard: weak `ecosystem_posture`; lic#439 local-ci in work queue.
9. **bug_fixer** → **code_implementer** — briefing: 1 CI item ([lic#439](https://github.com/li-langverse/lic/pull/439)).
10. **bench_improver** / **numerics_researcher** — heap `coord_numerics` P20 + 6 red rows (after meta + workspace).
11. **docs_maintainer**, **pr_branch_opener**, **security_auditor** — 8 repos without live pages; 133 orphan branches; Top25 catalog gaps (19).

**Do not contradict briefing P0:** numerics remain important but follow provability research + workspace + meta reconciliation first.

---

## Human-only blockers

| Blocker | Detail |
|---------|--------|
| Agent deliverable gate off | `LI_CURSOR_AGENTS_ENABLED` unset — no agent PR completion scan |
| lic PR #439 | [lic#439](https://github.com/li-langverse/lic/pull/439) local-ci exit 1 — needs log review before merge |
| Agent-kit canonical sync | 9 org repos vs kit `1.3.5+6018e18bf2ed91f4` — org rollout may need approval |
| Goal loop timeouts | httpd `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exit 124 — longer budget or human gate |
| No open merge queue | 0 open PRs — merge automation idle; 133 pushed branches without PRs |
| Full preflight skipped | `--skip-slow` hides plan_audit, ci_bug_triage, pr_program signals |

No missing API keys surfaced in this briefing cycle.

---

## Agent deliverable checklist

<!-- li-agent -->
## Agent deliverable

- [x] Regenerated `ecosystem-quality-report.json` via `python3 scripts/ecosystem-quality-grade.py`
- [x] Cited scorecard fields (no manual re-score)
- [x] Dimension narratives + findings table + dispatch order
- [x] Control-plane SQL spot-check (`agent_runs` 24h + status histogram)
- [x] Goal-directed snapshot reviewed (`lic/data/goal-directed-agents/snapshot.json`)
- [x] Sample incomplete/error runs cited (`implementation_gaps`, `code_implementer` wrk-soak)
- [ ] **swarm_observer** PR on `li-cursor-agents` (terminalization / incomplete-rate / stuck running)
- [ ] **gap_explorer** reconcile `swarm-gap-actions.json` (57 open)
- [ ] Enable `LI_CURSOR_AGENTS_ENABLED=1` for deliverable gate
- [ ] Full preflight (drop `--skip-slow`) before next unattended cycle
<!-- /li-agent -->

---

## Deliverable / findings (agent-specific)

### Handoff matrix

| Signal | Delegate to |
|--------|-------------|
| Incomplete rate 40% on recent terminal runs | `swarm_observer` |
| 57 open gaps (30 competitor_feature) | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `bench_improver`, `numerics_researcher` |
| 6 stopped goal runners + 26 pending todos | Plan loops / `plan_verifier` |
| 2 dirty sibling repos | `workspace_sweeper` |
| provability_holes research eligible | `proof_gap_researcher` |

### Control-plane evidence

```text
agent_runs status histogram (last 24h):
  error: 7186 | finished: 380 | running: 25 | incomplete: 5
Recent errors @ 2026-05-30T07:56–07:57Z: implementation_gaps, pr_reviewer, workspace_sweeper,
  agent_kit_maintainer, code_implementer, bench_improver, bug_fixer
Scorecard sample (n=120 local JSON): error_rate=0.10, incomplete_rate=0.40, running_count=110
```

### Goal-directed runners (stopped / idle)

| id | branch | plan_pending | note |
|----|--------|--------------|------|
| compiler-studio | cursor/compiler-studio-plan-loop | 0 | supervisor off; plan complete |
| sim | cursor/sim-algo-plan-loop | 0 | supervisor off |
| studio-ui-ux | cursor/studio-ui-ux-plan-loop | 3 | just completed `studio-ux-14`; active: `studio-ux-15-wgpu-readback` |
| sim-md-research | cursor/sim-md-research-loop | 1 | `md-r3-oracle-plan` |
| sim-chem-research | cursor/sim-chem-research-loop | 2 | DFT handoff todos |
| security-research | cursor/security-research-loop | 3 | fuzz/exploit todos |
| httpd | cursor/httpd-plan-continue | 2 | agent_exit 124 on wrk soak |
| swarm-observer | cursor/swarm-observer-plan-loop | 0 | orch plan complete; supervisor idle |

### Execution drift samples

| run_id | agent | failure mode |
|--------|-------|----------------|
| `implementation_gaps-1780127830403` | implementation_gaps | CP status error; JSON still `"running"` |
| `code_implementer-1780127785185` | code_implementer | httpd wrk-soak goal; long-running / incomplete |
| `pr_reviewer-1780127816950` | pr_reviewer | SDK error @ 07:56Z (0 open PRs in briefing) |

---

## Recommended issues/PRs

| Title (suggested) | Repo | Labels / notes |
|-------------------|------|----------------|
| research: provability_holes cycle17 mat2 FMA Lean drift | lic | `PH-2f`, `proof_gap_researcher` — branch `research/provability-cycle17-mat2-fma-lean-drift-2026-05-30` |
| chore: sync org agent-kit to 1.3.5+6018e18 | li-demo, li-httpd, li-language, li-net, li-std-core, li-std-math | `agent-kit`, `ecosystem` |
| fix(local-ci): lic#439 failure | lic | `bug`, `ci` — work_queue P0 |
| perf(7e): tier-1 matmul/ml/gmres ≤1.2× cpp | lic | `PH-7e`, `PH-5b` — branch `perf/bench-improver-matmul-simd-j-20260530` |
| meta: reconcile stuck `running` agent run records | li-cursor-agents | `swarm_observer` |
| gap: std.plot + std.summary packages | lic / li-std-* | `gap_explorer`, `ecosystem-gap` |
| docs: GitHub Pages for 8 repos without live docs | org-wide | `docs` |
| chore: open PRs for 133 orphan agent branches | org-wide | `pr_branch_opener` |
| httpd: extend wrk soak timeout / split todos | lic | goal-directed httpd loop exit 124 |
| security: map CWE Top25 missing_in_catalog (19) | lic | `security_auditor` |

---

## Deferred

- **pr_program / merge_plan automation** — 0 open PRs; merge-first idle until branches opened.
- **133 pr_branch_opener branches** — hygiene debt; defer until meta lanes stabilize.
- **ML benchmark reds** (`ml_conv2d_forward`, `ml_mlp_*`) — not tier-1 lic harness alone; defer to numerics research after matmul tier-1.
- **Competitor_feature gaps (30)** — registry apply pipeline; triage before implementers.
- **Provability gate changes** — none proposed; proof-before-perf preserved.
- **Full slow preflight** — plan_audit, ci_bug_triage, pr_program deferred this cycle (`--skip-slow`).

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Prior grader: `benchmarks/data/runs/ecosystem_grader-20260530T0737Z.md`
- Swarm observer: `benchmarks/data/runs/swarm_observer-1780124879899.md`
- Vision: `roadmap/docs/ecosystem/vision-and-roadmap.md`
