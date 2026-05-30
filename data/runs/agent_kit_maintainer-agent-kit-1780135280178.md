# Agent-kit maintainer — org rollout digest

**Run id:** `agent-kit-1780135280178`  
**Agent id:** `agent_kit_maintainer`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** ecosystem platform — Cursor policy parity across org repos (proof → easy → fast).

## Executive summary

- **Rollout complete** — no new commits required. All 8 drifted repos have open sync PRs on `chore/agent-kit-sync-<repo>` with stamp `1.3.5+6018e18bf2ed91f4`, required rules 3/3, `AGENTS.md`, and `scripts/sync-agent-kit.sh`.
- **`roadmap`** — `main` already at canonical stamp (PR #25 merged); no new PR needed (governance: human merge only).
- **`li-cursor-agents`** — already at canonical stamp `1.3.5+6018e18bf2ed91f4`.
- **Control-plane rollout** — failed to clone workspaces (`agent-kit-1780135280178/repo` dirs absent) due to GraphQL rate limit on `gh`; prior rollout branches/PRs remain valid.
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
| roadmap | — | **on `main`** at canonical stamp |

## Install failures

None.

## Control-plane failure notes

| Repo | Workspace | Root cause |
|------|-----------|------------|
| all 9 | `…/agent-kit-1780135280178/repo` | GraphQL rate limit on `gh repo clone` / `gh pr list`; workspace dirs never created |
| all 9 | prior runs `1780134265177`, `1780135115060` | Same GraphQL quota; branches and PRs already present |

## Verification (this pass)

- REST API + `raw.githubusercontent.com`: all 8 sync branches at stamp `1.3.5+6018e18bf2ed91f4`.
- Required rules present on every sync branch: `li-pr-only.mdc`, `li-ecosystem-gates.mdc`, `li-release-notes.mdc`.
- `roadmap` `main`: stamp `1.3.5+6018e18bf2ed91f4`.
- Re-ran `ensure-org-agent-kit.py --local-only` — OK: 3, needing sync: 9 (expected pre-merge).

## Follow-up

1. Human review + merge all 8 sync PRs (agents do not self-merge).
2. Unset stale invalid `GH_TOKEN` in agent env so `gh` uses `hosts.yml` credential when GraphQL quota resets.
3. After merges: `git pull` + `./scripts/sync-agent-kit.sh` on sibling clones; re-run audit.

## Audit (local-only)

```
canonical: 1.3.5+6018e18bf2ed91f4
OK: 3  needing sync: 9
```

Expected until PRs land on `main`.
