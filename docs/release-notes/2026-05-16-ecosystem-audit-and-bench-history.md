# Release notes: 2026-05-16 — ecosystem-audit-and-bench-history

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (this branch)  
**PH / REQ:** PH-5b (benchmark posture visibility)  
**Author:** agent

---

## Summary (one sentence)

Adds scheduled ecosystem audits (failed PRs, missing CI/docs) and timestamped benchmark history with ratio deltas for time-resolved improvement tracking.

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
| CI | `.github/workflows/ecosystem-audit.yml` (6h), `ci.yml` dry-run | Commits on `main` when audit changes |

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

- Ecosystem audit (`scripts/ecosystem-audit.py`, 6-hour workflow) and benchmark history snapshots (`data/history/`).
