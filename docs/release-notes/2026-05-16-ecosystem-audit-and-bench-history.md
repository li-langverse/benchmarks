# Release notes: 2026-05-16 — ecosystem-audit-and-bench-history

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (this branch)  
**PH / REQ:** PH-5b (benchmark posture visibility)  
**Author:** agent

---

## Summary (one sentence)

Adds ecosystem audit scripts and benchmark history; recurring runs via **Cursor Automations** (not Actions cron) to stay within Actions budget.

## Agent continuation (required)

1. Read: `data/latest/ecosystem-audit.json`, `data/history/index.json`, `AGENTS.md` standing ops.
2. Run: `python3 scripts/ecosystem-audit.py` each session; after lic bench CSV updates run `./scripts/ingest/ingest-lic.sh`.
3. Then: fix P0 items in audit (`failed_prs`, `missing_ci_on_main`); horner_pure_li needs **lic** PH-7e codegen, not threshold tweaks here.
4. Blocked on: human merge of package CI PRs; Windows CI on lic#1 / li-language#5.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Audit | `scripts/ecosystem-audit.py` → `data/latest/ecosystem-audit.json` | `gh` PR + workflow presence + summary reds |
| History | `scripts/record-benchmark-history.py`, `data/history/` | Snapshots + `latest_deltas` in `index.json` |
| CI | `ecosystem-audit.yml` manual dispatch only; `ci.yml` ingest + dashboard | No `schedule:` cron |
| Cursor | `.cursor/automations/*.md` | Prompts for cursor.com/automations |
| Docs | `docs/ecosystem/actions-budget.md` | Minute estimates; avoid roadmap 15m cron |

## Not changed (scope fence)

- `lic` compiler / `horner_pure_li` performance — **not** in this PR (88× gap needs PH-7e in lic).
- `catalog.toml` thresholds — unchanged.
- Roadmap development overview — separate repo PR #2.
- Ingest from live `latest.csv` in CI — still best-effort without lic bench artifact.

## Breaking changes

None.

## Security

N/A — public GitHub metadata only.

## Performance

N/A — audit scripts; no benchmark execution in this PR.

## Downstream

| Repo | Action |
|------|--------|
| lic | Fix Windows CI; improve pure-Li tier-1 codegen |
| roadmap | Merge live overview PR |

## CHANGELOG entry (paste into Unreleased)

### Added

- Ecosystem audit scripts + benchmark history; Cursor Automation prompts; Actions audit workflow manual-only.
