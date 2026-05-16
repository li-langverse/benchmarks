# Release notes: 2026-05-16 — org-agent-kit-rollout

**Status:** Released  
**Repo:** li-langverse/benchmarks  
**PH / REQ:** meta-governance  
**Author:** agent

---

## Summary

Adopted roadmap agent-kit v1.1.0 and release-notes/CHANGELOG/PR scaffolding; refreshed `AGENTS.md`.

## Agent continuation

1. Read: [roadmap release-notes policy](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md)
2. On merge-worthy PRs: update `CHANGELOG.md` + dated `docs/release-notes/` before `gh pr create`
3. After roadmap `agent-kit/` changes: `./scripts/sync-agent-kit.sh`
4. Dashboard: https://li-langverse.github.io/benchmarks/ — unchanged URL

## Changed

| Area | What | Evidence |
|------|------|----------|
| Agent-kit | `.cursor/` v1.1.0 | `scripts/expected-agent-kit-version` |
| Docs | `AGENTS.md`, `CHANGELOG.md`, PR template | org policy links |
| Tooling | `scripts/sync-agent-kit.sh` | sibling `roadmap` install |

## Not changed

- `catalog.toml`, ingest scripts, dashboard charts — **not** in this rollout
- GitHub Pages deploy workflow — unchanged

## Breaking changes

None.

## Security

N/A.

## Performance

N/A.

## Downstream

| Repo | Action |
|------|--------|
| lic, lis | Continue uploading bench CSV artifacts on main merge |

## CHANGELOG entry

```markdown
### Added
- Agent-kit v1.1.0 sync, release-notes scaffolding, PR template (org rollout)
```
