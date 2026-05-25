# Release notes: 2026-05-25 — fix-tier0-stability-ingest

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (feat/fix-tier0-stability)  
**PH / REQ:** PH-5b  
**Author:** agent

---

## Summary (one sentence)

Ingest maps `lic` `stability.csv` per-test rows to `tier0_stability` validity via strict tests (`harmonic_energy`, `momentum_drift`), clearing the dashboard **unknown** row when CSV is present.

## Agent continuation (required)

1. **Read:** `scripts/ingest/build_summary.py` (`tier0_li_validity_from_stability`), `lic/benchmarks/results/stability.csv`, `catalog.toml` (`tier0_stability`).
2. **Run:** `LIC_ROOT=../lic LIS_ROOT=../lis python3 scripts/ingest/build_summary.py ../lic ../lis`; `python3 scripts/check-dashboard-invariants.py`; `python3 scripts/benchmark-matrix-report.py`.
3. **Then:** Re-run lic tier-0 harness in CI so published `stability.csv` stays fresh; close benchmarks **#17** path gap follow-ups if plan-audit still flags harness dirs.
4. **Blocked on:** none

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `TIER0_STRICT_STABILITY_TESTS` + `tier0_li_validity_from_stability`; fixture `tier0_stability` row still supported | `python3 scripts/ingest/build_summary.py ../lic ../lis` → `tier0_stability` **green** / **pass** |
| Data | `data/latest/summary.json`, `benchmark-matrix.{json,md}` | `grep tier0_stability data/latest/benchmark-matrix.md` → **green** |
| Charts | Correctness chart `status` / `validity_*` synced with row gate | `build_summary.py` tier0 branch |

## Not changed (scope fence)

- **lic** `benchmarks/harness/stability.py` CSV schema — already exports per-test rows; no harness edit required.
- Advisory stability tests (`nve_energy_msd`, `timestep_halving_ratio`) — still shown in chart series; not part of tier0 pass gate.
- Other **unknown** catalog rows (lip/lit smoke, HTTP RPS) — unchanged.

## Breaking changes

None.

## Security

N/A — ingest-only; no trusted surface change.

## Performance

N/A — correctness validity gate only; no bench timing claims.

## Downstream

| Repo | Action |
|------|--------|
| lic | N/A — existing `stability.csv` producer |
| dashboard-next | N/A — consumes regenerated `summary.json` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **tier0_stability ingest:** Map lic `stability.csv` strict tests to validity pass; refresh `summary.json` / matrix — [2026-05-25-fix-tier0-stability-ingest.md](docs/release-notes/2026-05-25-fix-tier0-stability-ingest.md).
```
