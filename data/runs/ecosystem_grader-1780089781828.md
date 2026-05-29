# Ecosystem grader — proactive sweep

**Run id:** `ecosystem_grader-1780089781828`  
**Generated:** 2026-05-29T21:23Z  
**Source:** proactive  
**north_star_fit:** ecosystem orchestration — proof → easy → fast (PH-2i, PH-5b, PH-7e); meta lane before implementers  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-29T19:05Z  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-29T21:22:56Z

---

## Executive summary

- **Grade C · overall 71.3 / 100** — `unattended_safe: false` ([scorecard](../latest/ecosystem-quality-report.json)).
- **Score improved +3.7 pts** since prior pass (67.6 → 71.3); `swarm_execution` recovered from 55.0 → **70.0** but remains below the 75.0 dispatch threshold.
- **Swarm execution still blocks unattended dispatch**: **21%** error rate on 28 terminal runs; **92** runs still `running` (stuck-reconcile risk); top errors: `bench_improver` (2), `studio_ui_ux_builder`, `pr_alignment`.
- **Goal-directed loops starved**: **6/8** runners not progressing (`agents_live: 0`, **23/90** plan todos pending); only **httpd** + **swarm-observer** shells show `running: true` (both supervisor-idle, logs 2–2.1h stale).
- **Gap pressure steady-degraded** (70.0): **57** open registry gaps (3 `missing_package`, 18 `plan_debt`, 30 `competitor_feature`, 6 `ui_ux`).
- **Ecosystem posture mixed** (67.0): **0** open PRs on briefing audit, but **6 red** tier-1 benchmark rows (ingest @ 07:01Z — stale vs active `bench_improver` work).
- **Briefing health good** (84.0): **2** preflight fails (`org_agent_kit_audit`, `security_cwe_audit`); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Dispatch meta before implementers** — scorecard orders `swarm_observer` + `gap_explorer` first; briefing P0 still needs `workspace_sweeper` + governance (`plan_verifier`, `implementation_gaps`).

---

## Dimension drill-down

### briefing_health (84.0 · weight 0.15)

Preflight produced a usable briefing (`briefing_present: true`, **12** recommended agents). Two scripts exited non-zero: **`org_agent_kit_audit`** (9 repos missing kit, 3 drift — canonical `1.3.5+6018e18bf2ed91f4`) and **`security_cwe_audit`** (`JSONDecodeError: Expecting value` on empty input — CWE feed sync succeeded separately with **19** Top-25 CWEs missing from catalog). **`agent_deliverable_gate`** was skipped because `li-cursor-agents` scan is disabled locally. Plan audit, ecosystem audit, and merge-plan scripts all passed — governance agents can run, but security catalog completeness should be fixed before unattended `security_auditor` waves.

### ecosystem_posture (67.0 · weight 0.25)

PR surface is quiet (**0** open, **0** failed per briefing) and org CI audit reports **0** repos missing CI on `main`. Benchmark posture shows **6 red** tier-1 rows (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`) at ratios 1.33–1.55× vs C++. Active `bench_improver` branches on `lic` may already green some rows locally — ingest at 07:01Z is stale. **8** repos lack live docs pages; **129** branches pushed without open PRs (`pr_branch_hygiene`). **11** CI/bug queue items remain in triage JSON (9 GHA-red PRs across `lic`, `lip`, `lit`, `lis`, `li-httpd`, `li-demo`).

### goal_directed_health (70.0 · weight 0.20)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json` @ 21:22Z). **8** runners; **6** not actively progressing (`compiler-studio`, `sim`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research` — all `supervisor off`, logs 4–9 days stale). **httpd** has `running: true` but supervisor idle (log ~7574s stale) with **2** pending todos (`gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk`). **swarm-observer** shell process is snapshot refresh only — plan complete (5/5) but log ~8453s stale. **`agents_live: 0`**. Pending todos: **23/90**. Proof and sim work is frozen in snapshot handoffs (`sim-p1-num-dot-axpy`, `wave-d-gui-scaffold` in_progress, research loops) — restart supervisors or route explicit branches via `code_implementer`.

### swarm_execution (70.0 · weight 0.25)

Sampled **120** local run JSON files; **28** terminal, **92** still `running`. Among terminal runs: **6** errors (**21%**), **4** incomplete (**14%**). Top error agents in sample: **`bench_improver` (2)**, **`studio_ui_ux_builder` (1)**, **`pr_alignment` (1)**. Recent failures (21:12–21:14Z batch) include a **10-agent simultaneous error burst** (`plan_verifier`, `implementation_gaps`, `workspace_sweeper`, `ci_maintainer`, etc.) — likely SDK supersede/session collision, not product logic. `bench_improver-1780089585400` ran 34 tool calls then SDK error after investigating matmul codegen (release-note vs `kUnrollMax` mismatch) — premature deliverable, no bench evidence. Supabase `agent_runs`: historical error mass dominated by orchestration debt (`implementation_gaps` 203, `pr_reviewer` 198). Unattended dispatch remains unsafe until `swarm_observer` reconciles stuck `running` rows and hardens tick/session boundaries.

### gap_pressure (70.0 · weight 0.15)

Gap report present; **57** open gaps per `swarm-gap-actions.json` (ingest **2026-05-29T21:07Z**). **3** `missing_package` (`std.summary`, `std.plot`, line-profiler seed). **18** `plan_debt` rows mostly deferred without runner mapping (master-plan partial phases 2i, 7d, 7e, 8p). **30** `competitor_feature` rows from verticals.toml / explorer ingest. **6** `ui_ux` studio signals. Score held at 70.0 — absolute gap count grew (+4 since prior 53-gap pass) after continued competitor ingest — **`gap_explorer`** must reconcile registry vs filesystem and close stale rows before new package PRs.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| `preflight-failures` | high | `agent-briefing.json` → `preflight_runs` | `agent_kit_maintainer`, `ci_maintainer` |
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | plan loops / `plan_verifier` |
| `swarm-error-rate` | high | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `repos-missing-live-docs` | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

### Coordinator lane health

| Coordinator | Heap priority | Status | Notes |
|-------------|---------------|--------|-------|
| `coord_numerics` | 20 | **active** | 6 red rows; `bench_improver` on `lic` branch; ingest stale |
| `coord_governance` | 30 | **weak** | 64 master-plan open items; 40 open checkboxes |
| `coord_ecosystem` | 40 | **degraded** | 57 registry gaps; 2 missing std modules |
| `coord_platform` | 50 | **degraded** | 9 agent-kit drifts; security CWE audit broken |

### Recommended dispatch order

Merged **scorecard** (`recommended_agents`) with **briefing P0** (`recommended_agents` + `heap_plan.flat_tasks`). Scorecard meta agents lead; briefing P0 follows without contradiction.

| Step | Agent | Rationale |
|------|-------|-----------|
| 1 | `swarm_observer` | Scorecard P0: `swarm_execution` 70 < 75 — reconcile 92 `running`, 21% terminal errors, 21:12Z batch |
| 2 | `gap_explorer` | Scorecard P0: `gap_pressure` 70 < 80 — reconcile 57-gap registry |
| 3 | `workspace_sweeper` | Briefing P0 + scorecard: dirty **lic** + **benchmarks** (7 + 2 changed files) |
| 4 | `plan_verifier` | Briefing P0 + heap: 64 plan-completion findings |
| 5 | `implementation_gaps` | Briefing P0: cross-check PH trackers vs implementation |
| 6 | `ci_maintainer` | Scorecard + preflight: fix `security_cwe_audit` empty JSON input |
| 7 | `agent_kit_maintainer` | Preflight exit 1 — 9 repos missing/drifted kit |
| 8 | `numerics_researcher` → `bench_improver` | Heap P20: red rows; re-ingest after lic merges |
| 9 | `bug_fixer` → `code_implementer` | CI queue (11 items) — **after** steps 1–5 |
| 10 | `gap_explorer` (briefing) | 2 missing std modules — after registry reconcile |
| 11 | `docs_maintainer` | 8 repos without live pages |
| 12 | `pr_branch_opener` | 129 branches without PR — low urgency while open_prs=0 |
| 13 | `security_auditor` | Top-25 catalog gaps=19 — after CWE audit script fix |

**Defer stacked implementer waves** until `swarm_observer` clears the 21:12Z error batch and workspace sweep isolates clones.

### Human-only blockers

| Blocker | Evidence | Action |
|---------|----------|--------|
| **`security_cwe_audit` JSON parse** | `preflight_runs.security_cwe_audit` stderr | Human/fix script: empty JSON input to decoder |
| **`LI_CURSOR_AGENTS_ENABLED=0`** | `agent_deliverable_gate` skipped | Enable for deliverable gate scans in CI/automation |
| **Goal-directed supervisor restart** | 6 runners `supervisor off`, 4–9 day stale logs | Human: restart plan loops or accept manual branch work |
| **Benchmark ingest freshness** | Audit @ 07:01Z vs local greens | Human/CI: `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh` after lic merges |
| **`trusted.lean` edits** | Swarm mandate | Human-approved issues only |
| **129 orphan branches** | `pr_branch_hygiene` | Human triage before mass `pr_branch_opener` |
| **9 GHA-red PRs** | `ci-bug-triage.json` → `gha_failing_prs` | Human review merge vs close |

### Agent deliverable checklist (this run)

- [x] Cited fresh scorecard fields (no manual re-score)
- [x] Narrative under `data/runs/ecosystem_grader-1780089781828.md`
- [x] Dispatch order aligned with scorecard + briefing P0
- [x] Control-plane SQL sampled (`agent_runs` status histogram, recent errors)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate to `swarm_observer` if reconcile rules need code change
- [ ] Did not merge PRs or push to protected branches

### Handoff to meta-agents

| Signal | Delegate |
|--------|----------|
| 21% terminal error rate + 92 `running` | `swarm_observer` |
| 57 open gaps / competitor_feature ingest | `gap_explorer` + `swarm_observer` apply |
| 6 red benchmarks | `bench_improver`, `numerics_researcher` via briefing queue |
| 6 runners stopped / plan_pending | Relevant plan loop or `plan_verifier` |

---

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| bug(cloud-agent): ManagePullRequest false 'no commits on remote' after successful push | `lic` #120 | `bug` — triage queue |
| chore(lic): bench improver horner honesty | `lic` PR #413 | GHA red — numerics lane |
| chore(agent-kit): sync 1.3.5 stub-then-implement rule | `lip` PR #23, `lit` PR #14 | GHA red — platform |
| chore(agent-kit): sync roadmap cursor policy (sync) | `lip` PR #22, `lit` PR #13, `li-demo` PR #15 | GHA red |
| chore(lis): staging majico httpd bridge | `lis` PR #15 | GHA red |
| feat(li-net-httpd): plan-loop split from lic/cursor/httpd-plan-continue | `li-httpd` PR #10 | GHA red — httpd runner |
| **Meta (no PR yet)** | `li-cursor-agents` | Fix `security_cwe_audit` empty-input handling; SDK session lock for parallel tick |
| **Meta (no PR yet)** | `benchmarks` | Re-ingest lic benchmarks after matmul merges |
| Install agent-kit on 9 repos | `li-demo`, `li-httpd`, `li-language`, `li-net`, `li-std-*`, `lic`, `lis`, `roadmap` | `agent_kit_maintainer` |

---

## Deferred

- **`pr_branch_opener`** for 129 orphan branches — defer until `swarm_observer` stabilizes execution and open_prs stay at 0.
- **`code_implementer`** / stacked implementer waves — defer until workspace sweep + meta reconcile (steps 1–5).
- **`security_auditor`** catalog sweep — defer until `security_cwe_audit` preflight passes.
- **Benchmark strict tier-1 gate** (`check-tier1-li-vs-cpp.sh` strict mode) — defer until reds cleared and ingest refreshed.
- **Goal-directed supervisor restarts** for `compiler-studio`, `sim`, research loops — human decision; snapshot shows plan debt handoffs ready but supervisors off.
- **Provability gate changes** — never disable; `trusted.lean` human-only per swarm mandate.

---

## References

- Scorecard: [`data/latest/ecosystem-quality-report.json`](../latest/ecosystem-quality-report.json)
- Briefing: [`data/latest/agent-briefing.json`](../latest/agent-briefing.json)
- Gap actions: [`data/latest/swarm-gap-actions.json`](../latest/swarm-gap-actions.json)
- Goal snapshot: [`lic/data/goal-directed-agents/snapshot.json`](../../../lic/data/goal-directed-agents/snapshot.json)
- Sample run: [`bench_improver-1780089585400.json`](../../../li-cursor-agents/data/runs/bench_improver-1780089585400.json)
- Prior pass: [`ecosystem_grader-1780083675763.md`](ecosystem_grader-1780083675763.md)
