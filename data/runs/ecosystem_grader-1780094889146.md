# Ecosystem grader — proactive sweep

**Run id:** `ecosystem_grader-1780094889146`  
**Generated:** 2026-05-29T22:48Z  
**Source:** proactive  
**north_star_fit:** ecosystem orchestration — proof → easy → fast (PH-2i, PH-5b, PH-7e); meta lane before implementers  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-29T22:07Z  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-29T22:48:01Z

---

## Executive summary

- **Grade D · overall 69.6 / 100** — `unattended_safe: false` ([scorecard](../latest/ecosystem-quality-report.json)).
- **Swarm execution remains the binding constraint** (55.0): **33%** error rate on 21 terminal runs (7 errors); **99** local run JSON still `running`; control-plane last 3h: **783 errors / 19 running / 54 finished**.
- **22:37Z simultaneous error burst** — 10+ agents (`plan_verifier`, `implementation_gaps`, `workspace_sweeper`, UX testers, etc.) failed with `briefing_hash: null`; SDK session collision, not product regressions.
- **Goal-directed loops starved** (70.0): **6/8** runners stopped or idle-supervisor, `agents_live: 0`, **23/90** plan todos pending; only **httpd** + **swarm-observer** shells show `running: true` (logs 3.5–12h stale).
- **Gap pressure steady-degraded** (70.0): **57** open registry gaps (3 `missing_package`, 18 `plan_debt`, 30 `competitor_feature`, 6 `ui_ux`); `swarm-observer` orch plan **5/5 complete** but apply pipeline backlog persists.
- **Ecosystem posture improved** (75.0): **0** open PRs, **0** failed CI on main audit, **0** repos missing CI — but **6 red** tier-1 benchmark rows (ingest @ 07:01Z stale vs local `bench_improver` greens).
- **Briefing health good** (84.0): **2** preflight fails (`org_agent_kit_audit`, `security_cwe_audit`); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Dispatch meta before implementers** — scorecard orders `swarm_observer` + `gap_explorer` first; briefing P0 still needs `workspace_sweeper` + governance (`plan_verifier`, `implementation_gaps`).

---

## Dimension drill-down

### briefing_health (84.0 · weight 0.15)

Preflight produced a usable briefing (`briefing_present: true`, **12** recommended agents). Two scripts exited non-zero: **`org_agent_kit_audit`** (9 repos missing kit, 3 drift — canonical `1.3.5+6018e18bf2ed91f4`) and **`security_cwe_audit`** (`JSONDecodeError: Expecting value` on empty input — CWE feed sync succeeded separately with **19** Top-25 CWEs missing from catalog). **`agent_deliverable_gate`** was skipped because `li-cursor-agents` scan is disabled locally. Plan audit (166 findings), ecosystem audit, merge-plan, and CI triage (20 queue items) all passed — governance agents can run, but security catalog completeness and agent-kit sync should precede unattended `security_auditor` / platform waves.

### ecosystem_posture (75.0 · weight 0.25)

PR surface is quiet (**0** open, **0** failed per briefing) and org CI audit reports **0** repos missing CI on `main`. Benchmark posture shows **6 red** tier-1 rows (`matmul_blocked` 1.549×, `matmul_naive` 1.333×, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres` 1.4×) — all PH-5b/7e. Active `bench_improver` runs report local `matmul_naive` ~1.05× and pushed branch `chore/agent-bench_improver-94501069`, but dashboard ingest at 07:01Z is stale. **132** branches pushed without open PRs; **1** PR flagged for close/supersede review. Master plan tracks **166** open items (Phase 2i partial is current PH focus).

### goal_directed_health (70.0 · weight 0.20)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json` @ 22:47Z). **8** runners; scorecard counts **6** not actively progressing. Stopped/idle: `compiler-studio` (46/47 done, `wave-d-gui-scaffold` in_progress but supervisor off 4d), `sim` (gates fail on `sim-p1-num-dot-axpy`), `studio-ui-ux` (11/11 done, supervisor off), `sim-md-research`, `sim-chem-research`, `security-research`. **httpd** process alive but supervisor idle (**12669s** log stale) with **2** pending todos (`gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk`). **swarm-observer** shell alive, plan **5/5** complete, log **13549s** stale. **`agents_live: 0`**. Pending todos: **23/90**. Proof/sim/compiler work frozen — restart supervisors or route explicit branches via heap after swarm reconcile.

### swarm_execution (55.0 · weight 0.25)

Sampled **120** local run JSON files; **21** terminal, **99** still `running`. Among terminal runs: **7** errors (**33.3%**), **3** incomplete (**14.3%**). Top error agents in sample: **`bench_improver` (2)**, **`bug_fixer` (1)**, **`pr_reviewer` (1)**. Recent failures (22:37–22:47Z) include a **multi-agent simultaneous error burst** with null `briefing_hash` — consistent with SDK supersede/session lock contention. `bench_improver-1780094501069` completed 39 tool calls, pushed commit `e31a00aa`, then SDK error (label `li-swarm` not found). Supabase `agent_runs` (last 3h): **783** errors dominate. Unattended dispatch remains unsafe until `swarm_observer` reconciles stuck `running` rows and hardens tick/session boundaries.

### gap_pressure (70.0 · weight 0.15)

Gap report present; **57** open gaps per `swarm-gap-actions.json` (ingest **2026-05-29T21:07Z**). **3** `missing_package` (`std.summary`, `std.plot`, line-profiler seed). **18** `plan_debt` rows mostly deferred without runner mapping (master-plan partial phases 2i, 7d, 7e, 8p). **30** `competitor_feature` + **6** `ui_ux` from verticals/explorer/studio ingest. `swarm-observer` completed orch-r0–r4 but registry apply backlog unchanged — **`gap_explorer`** must reconcile registry vs filesystem, close stale rows, and wire plan_debt to goal-directed runners before new package PRs.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| `swarm-error-rate` | critical | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `preflight-failures` | high | `agent-briefing.json` → `preflight_runs` | `agent_kit_maintainer`, `ci_maintainer` |
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | plan loops / `plan_verifier` |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` | `swarm_observer` |

### Coordinator lane health

| Coordinator | Heap priority | Status | Notes |
|-------------|---------------|--------|-------|
| `coord_pull_requests` | 10 | **idle** | 0 open PRs; 132 orphan branches; 1 supersede review |
| `coord_numerics` | 20 | **active** | 6 red rows; `bench_improver` branch pushed; ingest stale |
| `coord_governance` | 30 | **weak** | 166 master-plan open items; plan audit 26 open checkboxes |
| `coord_ecosystem` | 40 | **degraded** | 57 registry gaps; briefing cites 2 missing std modules |
| `coord_platform` | 50 | **degraded** | 9 agent-kit drifts; security CWE audit broken |

### Recommended dispatch order

Merged **scorecard** (`recommended_agents`) with **briefing P0** (`recommended_agents` + `heap_plan.flat_tasks`). Scorecard meta agents lead; briefing P0 follows without contradiction.

| Step | Agent | Rationale |
|------|-------|-----------|
| 1 | `swarm_observer` | Scorecard P0: `swarm_execution` 55 — reconcile 99 `running`, 33% terminal errors, 22:37Z batch |
| 2 | `gap_explorer` | Scorecard P0: `gap_pressure` 70 — reconcile 57-gap registry vs explorer/briefing |
| 3 | `workspace_sweeper` | Briefing P0: dirty **lic** (4 files on `chore/agent-bench_improver-matmul-naive-at-2026-05-29`) |
| 4 | `plan_verifier` | Briefing P0 + heap: 166 plan-completion findings |
| 5 | `implementation_gaps` | Briefing P0: cross-check PH trackers vs implementation |
| 6 | `ci_maintainer` | Preflight: fix `security_cwe_audit` empty JSON input |
| 7 | `agent_kit_maintainer` | Preflight exit 1 — 9 repos missing/drifted kit |
| 8 | `numerics_researcher` → `bench_improver` | Heap P20: red rows; re-ingest after lic merges |
| 9 | `bug_fixer` → `code_implementer` | CI queue (20 items) — **after** steps 1–5 |
| 10 | `pr_alignment` | 1 PR flagged close/supersede |
| 11 | `pr_branch_opener` | 132 branches without PR — low urgency while open_prs=0 |
| 12 | `security_auditor` | Top-25 catalog gaps=19 — after CWE audit script fix |

**Defer stacked implementer waves** until `swarm_observer` clears the 22:37Z error batch and workspace sweep isolates clones.

### Human-only blockers

| Blocker | Evidence | Action |
|---------|----------|--------|
| **`security_cwe_audit` JSON parse** | `preflight_runs.security_cwe_audit` stderr | Human/fix script: empty JSON input to decoder |
| **`LI_CURSOR_AGENTS_ENABLED=0`** | `agent_deliverable_gate` skipped | Enable for deliverable gate scans in CI/automation |
| **Goal-directed supervisor restart** | 6 runners stopped/idle, 3.5–4d stale logs | Human: restart plan loops or accept manual branch work |
| **Benchmark ingest freshness** | Audit @ 07:01Z vs local greens | Human/CI: `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh` after lic merges |
| **`trusted.lean` edits** | Swarm mandate | Human-approved issues only |
| **132 orphan branches** | `pr_branch_hygiene` | Human triage before mass `pr_branch_opener` |
| **`li-swarm` label missing** | `bench_improver-1780094501069` post-hook | Human: create org label or fix post-hook |

### Agent deliverable checklist (this run)

- [x] Cited fresh scorecard fields (no manual re-score)
- [x] Narrative under `data/runs/ecosystem_grader-1780094889146.md`
- [x] Dispatch order aligned with scorecard + briefing P0
- [x] Control-plane SQL sampled (`agent_runs` status histogram, recent errors)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate to `swarm_observer` if reconcile rules need code change
- [ ] Did not merge PRs or push to protected branches

### Handoff to meta-agents

| Signal | Delegate |
|--------|----------|
| 33% terminal error rate + 99 `running` | `swarm_observer` |
| 57 open gaps / plan_debt deferred | `gap_explorer` + `swarm_observer` apply |
| 6 red benchmarks (ingest-lagged) | `bench_improver`, `numerics_researcher` via `coord_numerics` |
| 6 stopped goal runners / 23 plan_pending | Relevant plan loop or `plan_verifier` |

---

## Recommended issues/PRs

| Title | Repo | Labels / agent |
|-------|------|----------------|
| fix(preflight): `security_cwe_audit` empty JSON input | **benchmarks** | `ci`, `security` → `ci_maintainer` |
| Re-ingest tier-1 after lic matmul merge | **benchmarks** | `numerics`, PH-7e — clears stale dashboard reds |
| perf(7e): matmul_blocked vec4 FMA + blocked codegen | **lic** | `bench_improver`, PH-7e — branch `chore/agent-bench_improver-94501069` |
| Sync agent-kit to canonical 1.3.5 | **li-demo**, **li-httpd**, **li-std-*** | `agent_kit_maintainer` |
| Restart goal-directed `sim` / `compiler-studio` supervisors | **lic** | human ops — unblocks `sim-p1-num-dot-axpy`, `wave-d-gui-scaffold` |
| Reconcile registry 57 gaps vs briefing explorer | **lic** / **benchmarks** | `gap_explorer` |
| Swarm stuck-run reconcile + SDK session timeout | **li-cursor-agents** | `swarm_observer` — PR + `npm test` |
| Create `li-swarm` org label for post-hook | **li-langverse org settings** | human — unblocks agent PR labeling |

---

## Deferred

- **`pr_branch_opener` mass run** — 132 branches; wait until PR program has review bandwidth (open_prs=0 today).
- **30 `competitor_feature` gaps** — informational until plan_debt runners mapped; no implementer wave yet.
- **6 `ui_ux` gaps** — studio-ui-ux runner complete; defer until gui scaffold loop restarts.
- **Tier-2 yellow MD thermostats** — extern wrappers sufficient until tier-1 green + ingest.
- **42 unknown benchmark rows** — tier5/tier6 harness pending; not ecosystem-grade blockers this pass.
- **Lean `trusted.lean` for fused matmul** — human-approved track only.

<!-- li-agent -->
## Agent deliverable
- [x] Scorecard cited: `data/latest/ecosystem-quality-report.json` (grade D, 69.6)
- [x] Run narrative: `data/runs/ecosystem_grader-1780094889146.md`
- [x] Control-plane SQL sampled (`agent_runs` 3h window: 783 error / 19 running)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] `li-cursor-agents` prompt PR — delegated to `swarm_observer` if reconcile code change needed
