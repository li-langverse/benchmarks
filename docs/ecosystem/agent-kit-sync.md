# Agent-kit sync (benchmarks)

> **Issue:** [benchmarks#38](https://github.com/li-langverse/benchmarks/issues/38)  
> **Canonical stamp:** `scripts/expected-agent-kit-version` (synced from `roadmap/agent-kit`)

## Expected workflow

1. **Canonical source** — `li-langverse/roadmap` `agent-kit/` (human merge on governance paths).
2. **Install into this repo** — from benchmarks root:
   ```bash
   ../roadmap/scripts/install-agent-kit.sh benchmarks
   ```
3. **Verify** — `./scripts/check-agent-kit-sync.sh` (or `python3 ../benchmarks/scripts/ensure-org-agent-kit.py --local-only`).
4. **Delegate org-wide drift** — `agent_kit_maintainer` in **li-cursor-agents** for repos still behind canonical.

## Stamps (2026-05-25)

| Repo | Stamp | Action |
|------|-------|--------|
| **benchmarks** | `scripts/expected-agent-kit-version` | Bump via install-agent-kit PR after roadmap kit lands |
| **roadmap** | May trail canonical until install PR merges | `install-agent-kit.sh roadmap` |
| **li-cursor-agents** | `./scripts/sync-agent-kit.sh` | Same canonical line as benchmarks |

Do **not** weaken `agent-kit/hooks/guard-*.sh` when closing drift — align versions only.

## Related

- [ADOPTION.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/ADOPTION.md) (roadmap)
- [explorer digest 2026-05-19](explorer-digests/2026-05-19-explorer.md) — original drift report
