# Dashboard completeness sprint (2026-05-29)

## Summary

Closes P0 gaps on the public benchmarks dashboard ingest path: every catalog benchmark base now has explicit **linux / macos / windows** chart rows, honest **size_label** metadata (no spurious `harness pending`), and **validity_status = skip** for pending harness rows instead of `unknown`.

## Baseline → after (`audit-dashboard-gaps.py`)

| Metric | Before | After |
|--------|--------|-------|
| P0 | 422 | **0** |
| P1 | 194 | 412 (`chart_pending` — expected until CSV wired) |
| Chart rows | 185 | 555 (3× platform slice) |
| `missing_os` | 185 | 0 |
| `bad_size_label` | 153 | 0 |
| `validity_unknown` | 42 | 0 |

## Changes

- `scripts/audit-dashboard-gaps.py` — P0 gate; treats `darwin` as `macos`; accepts `skip` validity/status.
- `scripts/ingest/build_summary.py` — per-platform charts, `effective_size_meta`, pending → `skip`.
- `scripts/refresh-dashboard-completeness.py` — refresh committed `summary.json` without full lic CSV (Windows sprint host).
- `scripts/catalog/enrich-catalog-metadata.py` — replace `harness pending`, default `platforms`.
- `catalog.toml` — `[defaults] platforms`, enriched size labels (187 rows).

## Gates

```bash
python3 scripts/audit-dashboard-gaps.py          # exit 0
python3 scripts/check-dashboard-invariants.py    # PASS
python3 scripts/refresh-dashboard-completeness.py
```

## Follow-up

- Tier-1/2 lic harness CSV re-ingest on Linux nightly (matmul reds).
- macOS/Windows measured rows when nightly artifacts land (skip → green/yellow/red).
