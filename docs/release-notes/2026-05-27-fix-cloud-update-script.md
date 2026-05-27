# Release notes: 2026-05-27 — fix-cloud-update-script

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/fix-update-cloud-agent-env-ce9b`)  

---

## Summary

Adds `scripts/update-cloud-agent-env.sh` to replace the broken Cloud VM install snippet (`LLVM_DIR` unbound under `set -u`, wrong dashboard path, cmake cwd). Discovers all ~30+ org repos via `gh repo list` plus local checkouts; pins **LLVM 22** for `lic` build.

## Agent continuation

1. Read: `AGENTS.md` § Cloud Agent VM setup.
2. Run: `bash scripts/update-cloud-agent-env.sh` (or `SKIP_PULL=1` after first success).
3. Then: Point Cursor Cloud environment install script at this path.
4. Blocked on: none.

## Changed

| Area | What | Evidence |
|------|------|----------|
| Script | `update-cloud-agent-env.sh` | `scripts/update-cloud-agent-env.sh` |
| Docs | AGENTS install pointer | `AGENTS.md` |

## Not changed

- `run-full-benchmark-suite.sh` adaptive runs (see PR #113)  
- Ingest `build_summary.py` relative paths  

## Breaking changes

None.

## Security

N/A.

## Performance

N/A — setup only.

## Downstream

| Repo | Action |
|------|--------|
| Cloud config | Set install script to benchmarks `update-cloud-agent-env.sh` |

## CHANGELOG entry

### Fixed

- **Cloud VM update script:** `scripts/update-cloud-agent-env.sh` — LLVM detect via lic `llvm-env.sh`, `dashboard-next`, safe git pull — `docs/release-notes/2026-05-27-fix-cloud-update-script.md`.
