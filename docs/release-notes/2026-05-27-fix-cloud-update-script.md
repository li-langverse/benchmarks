# Release notes: 2026-05-27 — fix-cloud-update-script

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/fix-update-cloud-agent-env-ce9b`)  

---

## Summary

Hardens Cloud VM setup: `cloud-agent-install.sh` entrypoint delegates to `update-cloud-agent-env.sh`, which calls `lic/scripts/cloud-vm-bootstrap.sh` (LLVM **22**, `~/.config/environment.d/99-li-cloud.conf`, `dashboard-next`) instead of the broken inline `LLVM_DIR="$LLVM_DIR"` snippet.

## Agent continuation

1. Read: `AGENTS.md` § Cloud Agent VM setup; `lic/docs/ecosystem/cloud-agent-vm.md`.
2. Run: `bash scripts/cloud-agent-install.sh` (or `SKIP_PULL=1` after first success).
3. Then: Set Cursor Cloud **install script** to `bash /agent/repos/benchmarks/scripts/cloud-agent-install.sh`.
4. Blocked on: none.

## Changed

| Area | What | Evidence |
|------|------|----------|
| Entry | `scripts/cloud-agent-install.sh` | exec-safe under `set -u` |
| Update | `update-cloud-agent-env.sh` → `cloud-vm-bootstrap.sh` | no duplicate cmake/llvm logic |
| lic | `cloud-vm-bootstrap.sh` sudo LLVM install, `dashboard-next`, `LI_CLOUD_SKIP_PYTEST` | `lic` PR companion |
| Docs | AGENTS + `cloud-agent-vm.md` | install path + anti-pattern note |

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
