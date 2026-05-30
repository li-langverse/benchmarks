# Agent-kit maintainer — org rollout digest

**Run id:** `agent-kit-1780113525891`  
**Agent id:** `agent_kit_maintainer`  
**Canonical stamp:** `1.3.5+6018e18bf2ed91f4`  
**north_star_fit:** ecosystem governance / platform — Cursor policy parity across org repos (proof → easy → fast).

## Executive summary

- **This run's rollout failed** — GitHub **GraphQL rate limit exhausted** (0/5000) blocked `gh repo clone` / `gh pr list` in `rolloutAgentKitPrs`. Invalid `GH_TOKEN` in env also caused empty workspace clones under `agent-kit-1780113525891/`.
- **Prior rollouts succeeded** — all **9 drifted repos** already have **open PRs** on `chore/agent-kit-sync-<repo>` with branch stamp **`1.3.5+6018e18bf2ed91f4`**. No new commits required this pass.
- **Local audit still reports 9 needing sync** — `ensure-org-agent-kit.py --local-only` checks sibling working trees on disk, not merged remote state. Audit clears after PRs merge.
- **`li-cursor-agents`** — already at canonical stamp; no action.

## PR URLs (open, stamp verified on branch)

| Repo | PR | Branch stamp | CI (head) |
|------|-----|--------------|-----------|
| li-demo | https://github.com/li-langverse/li-demo/pull/15 | 1.3.5+6018e18bf2ed91f4 | check **failure** (Build lic — pre-existing infra) |
| li-httpd | https://github.com/li-langverse/li-httpd/pull/13 | 1.3.5+6018e18bf2ed91f4 | docs-only ✅ |
| li-language | https://github.com/li-langverse/li-language/pull/11 | 1.3.5+6018e18bf2ed91f4 | no checks |
| li-net | https://github.com/li-langverse/li-net/pull/12 | 1.3.5+6018e18bf2ed91f4 | docs-only ✅ |
| li-std-core | https://github.com/li-langverse/li-std-core/pull/8 | 1.3.5+6018e18bf2ed91f4 | docs-only ✅ |
| li-std-math | https://github.com/li-langverse/li-std-math/pull/9 | 1.3.5+6018e18bf2ed91f4 | docs-only ✅ |
| lic | https://github.com/li-langverse/lic/pull/379 | 1.3.5+6018e18bf2ed91f4 | CI green ✅ |
| lis | https://github.com/li-langverse/lis/pull/14 | 1.3.5+6018e18bf2ed91f4 | no checks |
| roadmap | https://github.com/li-langverse/roadmap/pull/25 | 1.3.5+6018e18bf2ed91f4 | verify-kit ✅ (governance — human merge) |

## Install failures

None on branch content — `install-agent-kit.sh` content is present on all sync branches.

## Blockers / follow-up

1. **Merge queue** — human review + `merge-approved` on each PR; **roadmap#25** is governance (never agent-merge).
2. **GraphQL quota** — unset stale `GH_TOKEN` or wait for reset before re-running `./scripts/agent-repo-workflow.sh agent-kit-rollout`.
3. **li-demo#15** — CI `Build lic` failure appears unrelated to agent-kit files; triage separately if merge-blocking.
4. **lic#379** — PR body missing some `- [x]` on bench/release deliverable lines (policy-only sync; optional body tidy).

## Audit (local-only, post-pass)

```
canonical: 1.3.5+6018e18bf2ed91f4
OK: 3  needing sync: 9
```

Expected until PRs land on `main`.
