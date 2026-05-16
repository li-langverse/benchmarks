# Release notes: 2026-05-16 — failed-benchmarks-automation

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (this branch)  
**PH / REQ:** PH-5b, PH-7e  
**Author:** agent

---

## Summary (one sentence)

Adds a Cursor Automation prompt and `benchmark-failures-report.sh` for agents to fix red/near-threshold rows on https://li-langverse.github.io/benchmarks/ via **lic**, not threshold tweaks here.

## Agent continuation (required)

1. Merge PR; create automation at cursor.com/automations from `.cursor/automations/failed-benchmarks-maintainer.md` (weekly; repo `lic` + `benchmarks` multi-repo; Open PR).
2. Run `./scripts/benchmark-failures-report.sh` to verify.
3. First target: `horner_pure_li` in lic (PH-7e).
4. Blocked on: none.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Automation | `.cursor/automations/failed-benchmarks-maintainer.md` | Dashboard-focused prompt |
| Script | `scripts/benchmark-failures-report.sh` | Prints red/yellow/near/unknown |
| Docs | `.cursor/automations/README.md`, `AGENTS.md` | Setup table |

## Not changed (scope fence)

- `catalog.toml` thresholds — unchanged
- lic compiler — fixes happen in lic PRs the automation opens
- Ingest workflow — still dispatch-only

## Breaking changes

None.

## Security

N/A.

## Performance

N/A — reporting script only.

## Downstream

| Repo | Action |
|------|--------|
| lic | Receive bench fix PRs from automation |

## CHANGELOG entry

### Added

- Cursor Automation `failed-benchmarks-maintainer` + `scripts/benchmark-failures-report.sh`.
