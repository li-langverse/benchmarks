# Swarm-gap-actions.json refresh pipeline (governance / REQ-bench-swarm)

> **Issue:** [benchmarks#181](https://github.com/li-langverse/benchmarks/issues/181)  
> **Repo:** li-langverse/benchmarks (+ **lic** ingest scripts)  
> **Vision:** **AI-first** (agents see honest gap backlog), **Provable** (plan_debt reflects completed todos)  
> **Learned from:** [agent-coordination.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/agent-coordination.md), [plan-cross-links.md](../plan-cross-links.md), `data/latest/swarm-gap-actions.json` (2026-05-25 stale), lic [#473](https://github.com/li-langverse/lic/issues/473) / [#471](https://github.com/li-langverse/lic/issues/471)

## Goal

Wire **benchmarks** preflight so `data/latest/swarm-gap-actions.json` is regenerated from the canonical **lic** swarm-gap registry after each plan-completion audit, closing stale `plan_debt` rows (e.g. completed sim/httpd/studio-ui todos) and removing false `missing_package` entries for shipped std modules.

## Non-goals

- Copying `lic/scripts/swarm-gap-ingest.py` into **benchmarks** (ingest stays in **lic**).
- Self-merging **lic** PRs that land ingest on `main` — tracked separately in lic#473.
- Adding GitHub Actions `schedule:` cron (Cursor Automations / manual dispatch only).
- Closing master-plan tracker rows without evidence (registry sync ≠ PH closure).

## Dependencies

- **lic#473** — ship `swarm-gap-ingest.py` on **lic** `main` (blocker for CI agents without worktree override).
- **lic#471** — reconcile ingest to honor `todo.status=completed`, not only `state.completed_ids`.
- **lic#436** — resolve `swarm-gap-registry/registry.yaml` merge conflict before ingest is reliable.
- Human: maintainer **`plan-approved`** before implementation agents run.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | `scripts/refresh-swarm-gap-actions.sh` — invoke lic ingest + apply, write `data/latest/swarm-gap-actions.json` | Local one-command refresh documented |
| B | `agent-preflight.sh` / `agent-briefing.py`: optional step after `plan_audit` when `LIC_ROOT` present | Briefing JSON includes `swarm_gap.generated_at` ≤24h old on dispatch |
| C | Extend `ecosystem-quality-grade.py` stale threshold check; fail grade when registry >7d old | Quality report cites refresh command |
| D | Update `audit-plan-completion` skill + [tooling-catalog.md](../tooling-catalog.md) with refresh path | Agents run refresh before plan_verifier handoff |
| E | Close stale rows: std.io/csv/summary/plot when packages exist; sim/studio-ui plan_debt when snapshot completed | `open_gaps` ≤10 (matches fresh ingest 2026-05-30) |

## Tests / benches

- Dry-run: `LIC_ROOT=../lic bash scripts/refresh-swarm-gap-actions.sh --dry-run` exits 0.
- `python3 scripts/ecosystem-quality-grade.py` — `swarm-gap-backlog` finding absent after refresh.
- No tier-N bench changes; governance-only artifact.

## Provability

- **G-*** rows unchanged — registry sync improves agent honesty, not proof closure.
- Do not mark **G-ai** or governance gaps **Done** from JSON refresh alone.

## Rollout

1. **benchmarks** PR (this plan) — after **`plan-approved`**.
2. **lic** PR(s) for ingest script + reconcile (#473, #471) — separate repo, human merge.
3. Bot/dedicated branch may commit refreshed JSON when org policy allows.
4. Remove `plan-needed` on #181 when PR merged + comment posted; maintainer adds **`plan-approved`**.

## Human-only

- Merge **lic** ingest PR before enabling preflight auto-refresh in cloud agents without `LIC_ROOT` worktree hacks.
- Decide whether refreshed JSON commits land on `main` via bot branch or manual PR.
