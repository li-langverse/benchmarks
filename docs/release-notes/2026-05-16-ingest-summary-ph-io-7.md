# PH-IO-7 — Li summary.json ingest

## Summary

`ingest-lic.sh` runs `build-summary-li.sh` (`std/summary` from `lic`) before falling back to Python `build_summary.py`.

## Agent continuation

1. **Read:** `scripts/ingest/build-summary-li.sh`, `lic` `runtime/li_rt_summary.c`.
2. **Run:** `LIC_ROOT=./lic ./scripts/ingest/build-summary-li.sh` after `./scripts/ingest/ingest-lic.sh` prerequisites.
3. **Then:** merge lic PH-IO-7; optional CI diff vs Python summary.
4. **Blocked on:** `lic` branch `cursor/li-summary-ph-io-7-c9a5` on `main`.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Ingest | `scripts/ingest/build_summary.li`, `build-summary-li.sh` | `PASS build-summary-li` |
| Flow | `scripts/ingest/ingest-lic.sh` | Li first, Python fallback |

## Not changed

- CSV smoke (PH-IO-4).
- Static dashboard render (PH-IO-5).
- `catalog.toml` schema beyond `[[benchmark]]` fields used today.

## Breaking

N/A.

## Security

N/A — same data sources as Python ingest; output path validated in `li_rt_summary`.

## Performance

N/A.

## Downstream

Merge **lic** PH-IO-7 before enabling Li-only ingest in CI without fallback.
