# Release notes: Dynamic org repo discovery

## Summary

All agent preflight scripts now load li-langverse repo names from `scripts/org_repos.py` via `gh repo list`, with `org_repos_catalog` embedded in `agent-briefing.json`.

## Agent continuation

1. **Read** `data/latest/org-repos-catalog.json` after `./scripts/agent-preflight.sh` — `all_repos`, `sweep_repos`, `merge_queue_repos`.
2. **Run** `python3 scripts/org_repos.py` to refresh catalog; `python3 scripts/org_repos.py --self-test` in CI.
3. **Then** issue/triage/PR scripts automatically include new org repos (e.g. `li-local-ci`) without code edits.
4. **Blocked on** `gh` auth in cloud agents — uses `FALLBACK_ORG_REPOS` until `gh` works.

## Changed

- `scripts/org_repos.py` — `list_org_repos()`, `org_repos_for_sweep()`, `org_repos_for_merge()`, `build_org_repos_catalog()`
- `scripts/agent-briefing.py` — writes `org-repos-catalog.json`, `org_repos_catalog` in briefing
- `scripts/issue-feature-triage.py`, `issue-backlog-hygiene.py`, `pr-merge-queue-plan.py`, `pr-merge-gate.py`, `run-pr-program.py`, `pr-branch-hygiene.py`, `ci-bug-triage.py`, `security-cwe-audit.py`, `local-ci-sweep.py`, `workspace-dirty-sweep.py`
- `scripts/ecosystem-audit.py`, `ensure-org-repo-ci.py`, `ensure-org-agent-kit.py` — dedupe `list_org_repos`
- `docs/ecosystem/tooling-catalog.md`

## Not changed

- `IGNORE_REPOS` / `MERGE_IGNORE_REPOS` policy (`li-cursor-agents`, `li-demo`)
- lic compiler, harness, dashboard ingest
- li-cursor-agents registry (separate repo)

## Breaking

N/A — broader scan coverage; JSON adds `repo_names` / `by_repo` in issue-feature-triage (was ambiguous `repos` key).

## Security

N/A — read-only repo list.

## Performance

N/A — one `gh repo list` per script run; briefing writes catalog once per preflight.

## Downstream

- Re-run `./scripts/agent-preflight.sh` so agents see full `sweep_repos` (13 repos as of 2026-05-21).
