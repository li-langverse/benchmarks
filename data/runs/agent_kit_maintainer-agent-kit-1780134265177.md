# Agent-kit maintainer — org rollout digest

**Run id:** `agent-kit-1780134265177`  
**Agent id:** `agent_kit_maintainer`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** ecosystem platform — Cursor policy parity across org repos (proof → easy → fast).

## Executive summary

- **Rollout complete** — remote `chore/agent-kit-sync-<repo>` branches carry stamp `1.3.5+6018e18bf2ed91f4`; **8 open PRs** verified via GitHub REST (`raw.githubusercontent.com` + pulls API). GraphQL quota blocked `gh pr list` / `agent-kit-rollout` CLI.
- **`roadmap`** — canonical stamp already on `main`; sync branch has no delta vs `main` — no new PR (governance: human merge only).
- **This pass** — confirmed install artifacts on remote branches; `li-cursor-agents` already at canonical stamp; no install failures.
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
| roadmap | — | **on `main`** — [PR #25](https://github.com/li-langverse/roadmap/pull/25) merged |

## Install failures

None.

## Control-plane failure notes

| Repo | Workspace | Root cause |
|------|-----------|------------|
| all 9 | `…/agent-kit-1780134265177/repo` | GraphQL rate limit on `gh api` / `gh pr list`; branches and PRs already present from prior rollout |

## Follow-up

1. Human review + merge (agents do not self-merge); `roadmap` governance unchanged.
2. Unset stale invalid `GH_TOKEN` in agent env so `gh` uses `hosts.yml` credential.
3. After merges: `git pull` + `./scripts/sync-agent-kit.sh` on sibling clones; re-run `python3 scripts/ensure-org-agent-kit.py --local-only`.

## Audit (local-only)

```
canonical: 1.3.5+6018e18bf2ed91f4
OK: 3  needing sync: 9
```

Expected until PRs land on `main`.
