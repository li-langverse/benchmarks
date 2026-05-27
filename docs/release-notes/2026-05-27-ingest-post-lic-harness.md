# Release notes: 2026-05-27 — ingest-post-lic-harness

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/bench-ingest-post-lic-harness-5599`)  
**PH / REQ:** PH-5b / PH-7e  

---

## Summary

Refreshes dashboard `summary.json` and matrix artifacts after `lic` bench harness merges (#304–#309, #329) via `ingest-lic.sh`.

## Agent continuation

1. Read: `data/latest/benchmark-matrix.md`, `data/history/index.json` (`latest_deltas`)
2. Run: `LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh` for full CSV refresh (long)
3. Then: verify live `/matrix` row count vs `catalog.toml`
4. Blocked on: ~109 `path=unknown` rows until lic harness CSV paths land

## Changed

| Area | What | Evidence |
|------|------|----------|
| Ingest | 187 summary rows, history snapshot | `data/latest/summary.json`, `data/history/2026-05-27T185618Z.json` |
| Matrix | Regenerated JSON/MD | `data/latest/benchmark-matrix.*` |

## Not changed

- `catalog.toml`
- Dashboard Next.js app
- lic compiler

## Breaking / Security / Performance / Downstream

N/A — data refresh only.
