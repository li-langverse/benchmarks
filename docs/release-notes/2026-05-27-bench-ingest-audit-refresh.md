# Release notes: 2026-05-27 — bench-ingest-audit-refresh

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/bench-ingest-audit-ce9b`)  
**PH / REQ:** PH-5b  

---

## Summary

Full-suite script exports adaptive timing env vars; ingest summary uses repo-relative source paths; fresh `ecosystem-audit.json` for org PR health.

## Agent continuation

1. Read: `data/latest/ecosystem-audit.json`, `docs/ecosystem/vision-implementation-status-2026-05-27.md` (roadmap).
2. Run: `LIC_ROOT=../lic python3 scripts/ingest/build_summary.py ../lic ../lis` after lic bench CSV exists.
3. Then: `./scripts/run-full-benchmark-suite.sh` when lic is built.
4. Blocked on: lic ULP fixes for dashboard red rows.

## Changed

| Area | What | Evidence |
|------|------|----------|
| Suite | `BENCH_MIN_RUNS=20` exports | `scripts/run-full-benchmark-suite.sh` |
| Ingest | Relative `sources.*` paths + `lic_root` | `scripts/ingest/build_summary.py` |
| Audit | Regenerated JSON | `data/latest/ecosystem-audit.json` |

## Not changed

- `catalog.toml` row count  
- Dashboard Next.js routes  
- lic compiler

## Breaking changes

None.

## Security

N/A.

## Performance

N/A — ingest metadata only unless full suite re-run.

## Downstream

| Repo | Action |
|------|--------|
| lic | Merge adaptive timing PR first for consistent CSV |

## CHANGELOG entry

### Changed

- **Bench suite / ingest:** adaptive run env + relative summary sources + ecosystem audit refresh — `docs/release-notes/2026-05-27-bench-ingest-audit-refresh.md`.
