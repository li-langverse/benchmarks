# Release notes: Issue backlog hygiene agent

## Summary

Adds `issue_hygiene` agent and `issue-backlog-hygiene.py` preflight to triage duplicate/stale org issues and route work to planners vs implementers.

## Agent continuation

1. **Read** `data/latest/issue-backlog-hygiene.json` after `./scripts/agent-preflight.sh` (or `python3 scripts/issue-backlog-hygiene.py` with `gh`).
2. **Run** Cursor automation [issue-hygiene-agent.md](../.cursor/automations/issue-hygiene-agent.md) or `LI_CURSOR_AGENTS_ROOT=../li-cursor-agents ./scripts/cursor-agent-run.sh --agent issue_hygiene --mock`.
3. **Then** hand `route_to_issue_planner` rows to **issue_planner**; `route_to_code_implementer` to **code_implementer**; max 8 issue actions per hygiene run.
4. **Blocked on** human issue close for duplicates unless thread explicitly requests bulk close.

## Changed

- `scripts/issue-backlog-hygiene.py` — JSON report + `--self-test`
- `scripts/agent-briefing.py` — preflight key `issue_hygiene`, recommendation, `issue_backlog_hygiene` payload
- `scripts/heap_plan.py` — `coord_governance` leaf `issue_hygiene`
- `.cursor/automations/issue-hygiene-agent.md`, `docs/ecosystem/agent-automations.md`, `tooling-catalog.md`
- **li-cursor-agents** (sibling PR): `src/agents/registry.ts`, `src/types.ts`, `src/heap/coordinators.ts`, mock body, `prompts/issue-hygiene-agent.md`

## Not changed

- `issue-feature-triage.py` scoring (still `needs_plan` / `planned` only)
- GitHub Actions workflows (no new `schedule:` cron)
- Merge queue / PR alignment scripts
- lic compiler or benchmark harness kernels

## Breaking

N/A — additive agent and preflight script.

## Security

N/A — read-only `gh issue list`; comments require token already used by other agents.

## Performance

N/A — bounded `--limit 80` per repo on preflight.

## Downstream

- Sync **li-cursor-agents** registry after merge; run `npm run test:e2e` in that repo.
- Optional: add `issue-backlog-hygiene.py` to `ecosystem-audit.yml` artifact commit list.
