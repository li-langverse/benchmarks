# Agent-kit maintainer — org rollout digest

**Run id:** `agent-kit-1780123391848`  
**Agent id:** `agent_kit_maintainer`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** ecosystem platform — Cursor policy parity across org repos (proof → easy → fast).

## Executive summary

- **Rollout complete** — isolated workspaces have stamp `1.3.5+6018e18bf2ed91f4`, branches pushed, **8 open PRs** on `chore/agent-kit-sync-<repo>`.
- **`roadmap`** — already merged on `main` via [PR #25](https://github.com/li-langverse/roadmap/pull/25); no new PR (branch equals `main`).
- **Control-plane “failed” rows** — transient: invalid `GH_TOKEN` in env + GraphQL quota exhausted for `gh pr list`/`gh pr create`; PRs were created earlier via REST or prior runs.
- **Local audit** — `ensure-org-agent-kit.py --local-only` still reports 9 needing sync until PRs merge and sibling clones pull/install.

## PR URLs (open)

| Repo | PR | Notes |
|------|-----|-------|
| li-demo | https://github.com/li-langverse/li-demo/pull/15 | |
| li-httpd | https://github.com/li-langverse/li-httpd/pull/13 | |
| li-language | https://github.com/li-langverse/li-language/pull/11 | |
| li-net | https://github.com/li-langverse/li-net/pull/12 | |
| li-std-core | https://github.com/li-langverse/li-std-core/pull/8 | |
| li-std-math | https://github.com/li-langverse/li-std-math/pull/9 | |
| lic | https://github.com/li-langverse/lic/pull/379 | |
| lis | https://github.com/li-langverse/lis/pull/14 | |
| roadmap | https://github.com/li-langverse/roadmap/pull/25 | **merged** — governance |

## Install failures

None — `install-agent-kit.sh` succeeded in workspaces; `scripts/sync-agent-kit.sh` present on sync branches.

## Follow-up

1. Human review + merge (do not agent-merge `roadmap` or other governance paths).
2. Unset stale `GH_TOKEN` in agent env so `gh` uses `hosts.yml` credential.
3. After merges: `git pull` / `./scripts/sync-agent-kit.sh` on sibling clones; re-run local audit.

## Audit (local-only)

```
canonical: 1.3.5+6018e18bf2ed91f4
OK: 3  needing sync: 9
```

Expected until PRs land on `main`.
