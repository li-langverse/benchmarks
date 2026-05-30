# Agent-kit maintainer — org rollout digest

**Run id:** `agent-kit-1780124464879`  
**Agent id:** `agent_kit_maintainer`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** ecosystem platform — Cursor policy parity across org repos (proof → easy → fast).

## Executive summary

- **Rollout complete** — all drifted repos have isolated workspaces at stamp `1.3.5+6018e18bf2ed91f4`, branches pushed, **8 open PRs** on `chore/agent-kit-sync-<repo>`.
- **`roadmap`** — already merged on `main` via [PR #25](https://github.com/li-langverse/roadmap/pull/25); remote `main` carries canonical stamp; no new PR required.
- **This pass** — control-plane retry hit GraphQL rate limit (`gh repo view` / `gh pr list`); verified state via REST API and git ls-remote instead. No install failures; no new commits required.
- **Local audit** — `ensure-org-agent-kit.py --local-only` still reports 9 needing sync until PRs merge and sibling clones run `install-agent-kit.sh` / `sync-agent-kit.sh`.

## PR URLs (open)

| Repo | PR | Head stamp |
|------|-----|------------|
| li-demo | https://github.com/li-langverse/li-demo/pull/15 | `1.3.5+6018e18bf2ed91f4` |
| li-httpd | https://github.com/li-langverse/li-httpd/pull/13 | `1.3.5+6018e18bf2ed91f4` |
| li-language | https://github.com/li-langverse/li-language/pull/11 | `1.3.5+6018e18bf2ed91f4` |
| li-net | https://github.com/li-langverse/li-net/pull/12 | `1.3.5+6018e18bf2ed91f4` |
| li-std-core | https://github.com/li-langverse/li-std-core/pull/8 | `1.3.5+6018e18bf2ed91f4` |
| li-std-math | https://github.com/li-langverse/li-std-math/pull/9 | `1.3.5+6018e18bf2ed91f4` |
| lic | https://github.com/li-langverse/lic/pull/379 | `1.3.5+6018e18bf2ed91f4` |
| lis | https://github.com/li-langverse/lis/pull/14 | `1.3.5+6018e18bf2ed91f4` |
| roadmap | https://github.com/li-langverse/roadmap/pull/25 | **merged** — governance |

## Install failures

None.

## Follow-up

1. Human review + merge (agents do not self-merge; `roadmap` governance already merged).
2. Unset stale invalid `GH_TOKEN` in agent env so `gh` uses `hosts.yml` credential and avoids GraphQL quota churn.
3. After merges: `git pull` + `./scripts/sync-agent-kit.sh` (or `install-agent-kit.sh`) on sibling clones; re-run local audit.

## Audit (local-only)

```
canonical: 1.3.5+6018e18bf2ed91f4
OK: 3  needing sync: 9
```

Expected until PRs land on `main`.
