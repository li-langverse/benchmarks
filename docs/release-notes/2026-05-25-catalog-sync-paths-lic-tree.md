# Release notes: 2026-05-25 — catalog sync paths lic tree

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (feat/catalog-sync-paths)  
**PH / REQ:** PH-5b, fill-all-benchmarks WP5  
**Author:** agent

---

## Summary (one sentence)

Adds `scripts/catalog/sync-paths-from-lic-tree.py` and wires **83** catalog rows from `path = unknown` to existing **lic** harness directories under `benchmarks/tier1_micro` and `benchmarks/tier2_physics`, then refreshes `data/latest/summary.json` from `lic/benchmarks/results/latest.csv`.

## Agent continuation (required)

1. **Read:** `scripts/catalog/sync-paths-from-lic-tree.py`, `docs/dashboard/fill-all-benchmarks-plan.md` (WP5–WP8).
2. **Run:** `LIC_ROOT=../lic python3 scripts/catalog/sync-paths-from-lic-tree.py --dry-run` after **lic** harness landings; `LIC_ROOT=../lic LIS_ROOT=../lis python3 scripts/ingest/build_summary.py ../lic ../lis` when CSV updates.
3. **Then:** WP7 full bench run → WP8 ingest coverage gate (`check-summary-measurement-coverage.py`).
4. **Blocked on:** **lic** harness dirs for remaining **26** `unknown` rows (no matching dir in sibling lic tree yet).

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Catalog sync | `scripts/catalog/sync-paths-from-lic-tree.py` — scan `tier*`, tier5 scenarios, `ml`/`viewport`; reuse `sync-from-algo-registry` resolve/aliases | `--dry-run` lists 83 updates |
| Catalog | `catalog.toml` — **83** `path` fields `unknown` → `benchmarks/tier{1,2}_*/…` | `unknown` count **109 → 26** (179 rows) |
| Ingest | `data/latest/summary.json` regenerated when `../lic/benchmarks/results/latest.csv` present | `build_summary.py` → 179 rows |

## Not changed (scope fence)

- **lic** harness implementation for rows still `unknown`.
- `vendor/lis-tier5`, `li-tests/`, database tier-6 suite stubs.
- Dashboard Next UI components and Pages deploy workflow.

## Breaking changes

N/A — catalog path corrections only.

## Security

N/A — no trusted creep.

## Performance

N/A — ingest refresh only; no bench threshold changes.

## Downstream

| Repo | Action |
|------|--------|
| lic | Re-run sync after new harness dirs; WP7 CSV for colored rows |
| li-cursor-agents | Briefing `catalog_gaps` should drop after merge + snapshot |

## CHANGELOG entry (paste into Unreleased)

### Added

- **WP5 catalog path sync:** `scripts/catalog/sync-paths-from-lic-tree.py` — 83 lic harness paths wired; `summary.json` refresh — [2026-05-25-catalog-sync-paths-lic-tree.md](docs/release-notes/2026-05-25-catalog-sync-paths-lic-tree.md).
