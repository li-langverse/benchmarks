# Agent-kit rollout digest

**Run:** `agent-kit-1780106686276`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**Generated:** 2026-05-30

## Summary

Prior control-plane rollout created sync branches and open PRs. This pass verified remote branches (REST/git) after GraphQL rate-limit blocked `gh repo clone` / `agent-kit-rollout` retries. **Install OK** on all nine target repos at canonical stamp; **no install failures** on remote heads.

Local `--local-only` audit still reports drift until PRs merge into `main` (expected).

## PRs (open — human merge; `roadmap` is governance)

| Repo | PR | Remote stamp |
|------|-----|--------------|
| li-demo | https://github.com/li-langverse/li-demo/pull/15 | 1.3.5+6018e18bf2ed91f4 |
| li-httpd | https://github.com/li-langverse/li-httpd/pull/13 | 1.3.5+6018e18bf2ed91f4 |
| li-language | https://github.com/li-langverse/li-language/pull/11 | 1.3.5+6018e18bf2ed91f4 |
| li-net | https://github.com/li-langverse/li-net/pull/12 | 1.3.5+6018e18bf2ed91f4 |
| li-std-core | https://github.com/li-langverse/li-std-core/pull/8 | 1.3.5+6018e18bf2ed91f4 |
| li-std-math | https://github.com/li-langverse/li-std-math/pull/9 | 1.3.5+6018e18bf2ed91f4 |
| lic | https://github.com/li-langverse/lic/pull/379 | 1.3.5+6018e18bf2ed91f4 |
| lis | https://github.com/li-langverse/lis/pull/14 | 1.3.5+6018e18bf2ed91f4 |
| roadmap | https://github.com/li-langverse/roadmap/pull/25 | 1.3.5+6018e18bf2ed91f4 |

## Workspaces

Isolated clones: `li-cursor-agents/data/workspaces/li-langverse/<repo>/agent-kit-1780106686276/repo`

## Blockers encountered

- **GraphQL rate limit** (`gh` API 5000/5000) — rollout CLI reported all repos failed; git+REST verification showed branches already pushed.
- **Push rejected** on retry — remote `chore/agent-kit-sync-*` already ahead; do not force-push.

## li-cursor-agents

Local checkout already at `1.3.5+6018e18bf2ed91f4` (`./scripts/sync-agent-kit.sh` not required this run).

## Next steps

1. Human review + merge PRs (especially **roadmap** governance).
2. After merge: `cd benchmarks && python3 scripts/ensure-org-agent-kit.py --local-only` should clear drift for merged repos.
