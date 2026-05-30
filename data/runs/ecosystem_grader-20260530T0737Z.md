# Ecosystem grader digest — `ecosystem_grader-20260530T0737Z`

**Date:** 2026-05-30T07:37Z  
**Agent:** ecosystem_grader (proactive sweep)  
**Scorecard:** `data/latest/ecosystem-quality-report.json` (regenerated 2026-05-30T07:37:08Z)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T07:33Z)  
**north_star_fit:** PH-5b / PH-7e (tier-1 competitive), provable-before-fast — no gate weakening

---

## Executive summary

- **Grade C** · **overall score 70.8 / 100** · **unattended-safe: no** (`ecosystem-quality-report.json`: `grade`, `overall_score`, `unattended_safe`).
- **+1.0 vs prior pass** (69.8 / D @ 07:07Z): full preflight restored (`briefing_health` 77→84); still below unattended threshold (typically ≥75 overall + clean meta lanes).
- **Meta lanes degraded:** `swarm_execution` 70 (`error_rate` 0.2222 on last 18 terminal runs), `gap_pressure` 70 (57 open gaps), `ecosystem_posture` 65 (6 red benchmarks).
- **Briefing P0 (current file):** `workspace_sweeper` → `plan_verifier` → `implementation_gaps` — no `proof_gap_researcher` in `recommended_agents` this cycle; respect briefing order over heap-only numerics.
- **Scorecard meta-first:** `swarm_observer` → `gap_explorer` → `ci_maintainer` before implementers; aligns with high-severity `swarm-error-rate` + `swarm-gap-backlog`.
- **Goal-directed loops starved:** 6/8 runners stopped, 26 plan todos pending, `agents_live: 0`; httpd soak process alive but agent exits **124** on perf todos.
- **Preflight:** 2 failures — `org_agent_kit_audit` (exit 1, 9 repos), `security_cwe_audit` (JSONDecodeError on empty feed); 1 skip (`agent_deliverable_gate`).
- **Human-only:** lic#439 local-ci; 133 orphan branches; `LI_CURSOR_AGENTS_ENABLED` unset; security_cwe_audit feed parse fix.

---

## Dimension drill-down

### briefing_health (84.0)

Briefing is present with **12 recommended agents** and a **full preflight cycle** (plan_audit, pr_program, ci_bug_triage, explorer all exit 0). Strength vs the 07:07Z pass: only **one** skipped script (`agent_deliverable_gate`). Weakness: **two non-zero exits** — `org_agent_kit_audit` (9 repos missing/drifted kit `1.3.5+6018e18bf2ed91f4`) and `security_cwe_audit` (empty/invalid JSON input → `JSONDecodeError`). Scorecard finding `preflight-failures` (high). Dispatch **agent_kit_maintainer** and **security_auditor**; fix CWE audit input before unattended runs.

### ecosystem_posture (65.0)

Org CI posture is clean: **0** repos missing CI on main, **0** failed/open PRs in ecosystem audit. Dimension held at 65 by **six red benchmark rows** (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres` — ingest @ 2026-05-29T18:47Z) plus **10 repos without live docs**. Finding `benchmark-red-rows` (high). Route **bench_improver** + **numerics_researcher** under `coord_numerics` (heap P20) after meta reconciliation; refresh `ecosystem-audit.py` ingest after lic tier-1 codegen lands on `research/provability-cycle16-mat2-codegen-lean-drift-2026-05-30`.

### goal_directed_health (70.0)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`, 2026-05-30T07:36Z): **8 runners**, **6 not running** (`compiler-studio`, `sim`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research`), **26 pending todos** of 97, **`agents_live: 0`**. **httpd** and **swarm-observer** show `running: true` (fixture/soak processes) but `agent_live: false`; httpd last todos `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exited **124** (timeout). **studio-ui-ux** has 4 pending wave-2 todos (`studio-ux-14`…`17`) despite completed state entries — **plan_verifier** should reconcile. Finding `goal-runners-stopped` (high).

### swarm_execution (70.0)

Local sample (n=120): **102 running**, **18 terminal**, **4 error**, **2 incomplete** → `error_rate` **0.2222**, `incomplete_rate` **0.1111**. Findings `swarm-error-rate` (high), `swarm-many-running` (medium). Recent terminal errors in `li-cursor-agents/data/runs/`: `studio_ui_ux_builder-1780125874363.json` (SDK error after non-FF push rejected), `implementation_gaps-1780125488312.json`, `pr_reviewer-1780125488288.json`. Control-plane DB (full history): **7689 error**, 387 finished, 24 incomplete, 20 running — historical error volume dominates; **07:30Z batch** shows 8+ concurrent `error` runs (orchestrator wave). Delegate **swarm_observer** for terminalization, SDK status mapping, and push/FF policy on **li-cursor-agents** (PR + `npm test`).

### gap_pressure (70.0)

`swarm-gap-actions.json`: **57 open gaps** — `competitor_feature: 30`, `plan_debt: 24`, `missing_package: 3` (`std.plot`, `std.summary`, line-profiler seed). Finding `swarm-gap-backlog` (high). Briefing lists **2 missing std modules** for **gap_explorer**; registry is broader. **gap_explorer** + **swarm_observer** apply pipeline before **implementation_gaps** floods implementers.

---

## Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| preflight-failures | high | `data/latest/agent-briefing.json` → `preflight_runs.org_agent_kit_audit`, `security_cwe_audit` | `agent_kit_maintainer`, `security_auditor` |
| benchmark-red-rows | high | `data/latest/ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| goal-runners-stopped | high | `lic/data/goal-directed-agents/snapshot.json` | plan loop owners / `plan_verifier` |
| swarm-error-rate | high | `li-cursor-agents/data/runs` (+ CP `agent_runs` recent errors) | `swarm_observer` |
| swarm-gap-backlog | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| swarm-many-running | medium | `li-cursor-agents/data/runs` | `swarm_observer` |
| repos-missing-live-docs | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

---

## Recommended dispatch order

Merged **scorecard** `recommended_agents` with **briefing** `recommended_agents` (briefing wins on ties):

1. **workspace_sweeper** — briefing P0: lic dirty on `research/provability-cycle16-mat2-codegen-lean-drift-2026-05-30` (5 safe files: snapshot, registry, nginx submodule path, logs); run `./li-tests/run_all.sh` before commit.
2. **swarm_observer** — scorecard: `swarm_execution` &lt; 75; 22% error rate on recent terminal sample + 102 “running” stubs; SDK terminalization + push policy.
3. **gap_explorer** — scorecard: `gap_pressure` &lt; 80; 57 registry gaps vs briefing’s 2 std modules.
4. **plan_verifier** — scorecard + briefing: plan-completion-audit (166 findings); plan_audit now exit 0.
5. **implementation_gaps** — briefing: cross-check plan vs implementation (after verifier; prior run errored without deliverable section).
6. **agent_kit_maintainer** — preflight exit 1: li-demo, li-httpd, li-language, li-net, li-std-core, li-std-math (missing); lic, lis, roadmap (drift).
7. **ci_maintainer** — scorecard: weak `ecosystem_posture`; lic#439 local-ci in work queue.
8. **bug_fixer** → **code_implementer** — briefing: 1 CI item ([lic#439](https://github.com/li-langverse/lic/pull/439)).
9. **bench_improver** / **numerics_researcher** — heap `coord_numerics` P20 + 6 red rows (after meta + workspace).
10. **docs_maintainer**, **pr_branch_opener**, **security_auditor** — 10 repos without live pages; 133 orphan branches; CWE audit fix + Top25 catalog gaps (19).

**Do not contradict briefing P0:** numerics remain important but follow workspace + meta reconciliation first.

---

## Human-only blockers

| Blocker | Detail |
|---------|--------|
| Agent deliverable gate off | `LI_CURSOR_AGENTS_ENABLED` unset — no agent PR completion scan |
| lic PR #439 | [lic#439](https://github.com/li-langverse/lic/pull/439) local-ci exit 1 — needs log review before merge |
| Agent-kit canonical sync | 9 org repos vs kit `1.3.5+6018e18bf2ed91f4` — org rollout may need approval |
| security_cwe_audit broken | `JSONDecodeError` — empty/malformed CWE catalog JSON; human fix script input |
| Goal loop timeouts | httpd `gap-phase2-perf-wrk-soak` / `gap-phase2-streaming-wrk` exit 124 — longer budget or human gate |
| No open merge queue | 0 open PRs — merge automation idle; 133 pushed branches without PRs |
| studio_ui_ux_builder push | Non-fast-forward rejected on `chore/agent-bench_improver-*` — human rebase/branch hygiene |

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
- [x] Sample error runs cited (`implementation_gaps`, `studio_ui_ux_builder`)
- [ ] **swarm_observer** PR on `li-cursor-agents` (terminalization / error-rate / stuck running)
- [ ] **gap_explorer** reconcile `swarm-gap-actions.json` (57 open)
- [ ] Fix `security-cwe-audit.py` empty JSON input
- [ ] Enable `LI_CURSOR_AGENTS_ENABLED=1` for deliverable gate
<!-- /li-agent -->

---

## Deliverable / findings (agent-specific)

### Handoff matrix

| Signal | Delegate to |
|--------|-------------|
| Error rate 22% on recent terminal runs | `swarm_observer` |
| 57 open gaps (30 competitor_feature) | `gap_explorer` + `swarm_observer` apply pipeline |
| 6 red benchmarks | `bench_improver`, `numerics_researcher` |
| 6 stopped goal runners + 26 pending todos | Plan loops / `plan_verifier` |
| lic dirty provability research branch | `workspace_sweeper` |

### Control-plane evidence

```text
agent_runs status histogram (full DB):
  error: 7689 | finished: 387 | incomplete: 24 | running: 20
Recent errors @ 2026-05-30T07:30Z: workspace_sweeper, plan_verifier, bug_fixer, autoresearch, gui_ui_tester, …
Scorecard sample (n=120 local JSON): error_rate=0.2222, incomplete_rate=0.1111, running_count=102
```

### Goal-directed runners (stopped / idle)

| id | branch | plan_pending | note |
|----|--------|--------------|------|
| compiler-studio | cursor/compiler-studio-plan-loop | 0 | supervisor off; plan complete |
| sim | cursor/sim-algo-plan-loop | 0 | supervisor off |
| studio-ui-ux | cursor/studio-ui-ux-plan-loop | 4 | active: `studio-ux-14-native-sdl-ci` |
| sim-md-research | cursor/sim-md-research-loop | 1 | `md-r3-oracle-plan` |
| sim-chem-research | cursor/sim-chem-research-loop | 2 | DFT handoff todos |
| security-research | cursor/security-research-loop | 3 | fuzz/exploit todos |
| httpd | cursor/httpd-plan-continue | 2 | agent_exit 124 on wrk soak |
| swarm-observer | cursor/swarm-observer-plan-loop | 0 | orch plan complete; supervisor idle |

### Execution drift samples

| run_id | agent | failure mode |
|--------|-------|----------------|
| `implementation_gaps-1780125488312` | implementation_gaps | SDK status error @ ~394s; no deliverable section |
| `studio_ui_ux_builder-1780125874363` | studio_ui_ux_builder | SDK error; git push non-fast-forward after local commit |
| `pr_reviewer-1780125488288` | pr_reviewer | SDK status error (0 open PRs in briefing) |

---

## Recommended issues/PRs

| Title (suggested) | Repo | Labels / notes |
|-------------------|------|----------------|
| chore: sync org agent-kit to 1.3.5+6018e18 | li-demo, li-httpd, li-language, li-net, li-std-core, li-std-math | `agent-kit`, `ecosystem` |
| fix(security): security-cwe-audit empty catalog JSON | benchmarks | `security`, `ci` |
| fix(local-ci): lic#439 failure | lic | `bug`, `ci` — work_queue P0 |
| perf(7e): tier-1 matmul/ml/gmres ≤1.2× cpp | lic | `PH-7e`, `PH-5b` — branch `research/provability-cycle16-mat2-codegen-lean-drift-2026-05-30` |
| meta: reconcile stuck `running` agent run records | li-cursor-agents | `swarm_observer` |
| gap: std.plot + std.summary packages | li-std-* | `gap_explorer` |
| docs: GitHub Pages for 10 repos without live docs | org-wide | `docs` |
| chore: open PRs for 133 orphan agent branches | org-wide | `pr_branch_opener` |
| httpd: extend wrk soak timeout / split todos | lic | goal-directed httpd loop exit 124 |

---

## Deferred

- **pr_program / merge_plan automation** — 0 open PRs; merge-first idle until branches opened.
- **133 pr_branch_opener branches** — hygiene debt; defer until meta lanes stabilize.
- **ML benchmark reds** (`ml_conv2d_forward`, `ml_mlp_*`) — not tier-1 lic harness alone.
- **Competitor_feature gaps (30)** — registry apply pipeline; triage before implementers.
- **Provability gate changes** — none proposed; proof-before-perf preserved.
- **Prior pass proof_gap_researcher P0** — not in current briefing `recommended_agents`; re-enable via research_goals_status if provability_holes regresses.

---

## References

- Scorecard: `benchmarks/data/latest/ecosystem-quality-report.json`
- Briefing: `benchmarks/data/latest/agent-briefing.json`
- Prior grader: `benchmarks/data/runs/ecosystem_grader-20260530T0707Z.md`
- Swarm observer: `benchmarks/data/runs/swarm_observer-1780124879899.md`
- Vision: `roadmap/docs/ecosystem/vision-and-roadmap.md`
