# Li def + short imports in benchmarks PH-IO samples

## Summary

Benchmarks ingest/dashboard `.li` programs and ecosystem explorer metadata now follow the current `lic` language standard: `def` entrypoints, short `import io|csv|summary|plot`, and `raises IoError, AllocError` instead of `proc`, `import std.*`, and bare `IO` / `Alloc`.

## Agent continuation

1. **Read:** `scripts/ingest/*.li`, `scripts/dashboard/render_dashboard.li`, `scripts/ecosystem-explorer.py`, `docs/ecosystem/ecosystem-explorer.md`.
2. **Run:** `python3 scripts/ecosystem-explorer.py` (refreshes `data/latest/ecosystem-explorer.json` when executed in CI or locally).
3. **Then:** ensure `lic` on the pinned toolchain accepts `def`, short imports, and the new `raises` names before turning skip gates into hard CI failures.
4. **Blocked on:** `lic` implementation of import aliases (`io` → `std/io`) and error-type names in the compiler/stdlib; benchmarks only reflects the contract.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| PH-IO Li samples | `scripts/ingest/csv_ingest_smoke.li`, `build_summary.li`, `build_summary_fixture.li`, `scripts/dashboard/render_dashboard.li` | `def`, `import io` / `csv` / `summary` / `plot`, `raises IoError, AllocError` |
| Shell gates | `scripts/ingest/ingest-csv-smoke.sh`, `scripts/ingest/build-summary-li.sh`, `scripts/dashboard/render-static.sh` | User-facing skip messages reference short module names |
| Explorer | `scripts/ecosystem-explorer.py` | `EXPECTED_STD_MODULES` uses `io`, `csv`, `summary`, `plot`; `std_module_present` maps short names to `std.*` on disk |
| Preflight copy | `scripts/agent-briefing.py` | Gap-explorer reasons say “PH-IO modules” |
| Docs | `docs/ecosystem/ecosystem-explorer.md`, `docs/ecosystem/explorer-digests/2026-05-17-explorer.md`, `2026-05-17-gaps.md`, `2026-05-19-gaps.md` | Tables and gap text match import surface |
| Generated | `data/latest/ecosystem-explorer.json` | Regenerated when `ecosystem-explorer.py` runs |

## Not changed

- `catalog.toml` benchmark definitions and ingest Python (`build_summary.py`) behavior.
- `lic` compiler implementation in this repo (benchmarks does not vendor `lic`).
- Other `data/latest/*.json` preflight artifacts (`agent-briefing.json`, `pr-program-run.json`, …) — only `ecosystem-explorer.json` was regenerated for this PR.
- GitHub Actions workflow YAML beyond what reads regenerated JSON artifacts.

## Breaking / Security / Performance / Downstream

| Topic | Status |
|-------|--------|
| **Breaking** | **Yes for older `lic`:** toolchains that only accept `proc` / `import std.io` / `raises IO, Alloc` will fail to compile these samples until upgraded to the new standard. |
| **Security** | N/A — sample paths and contracts unchanged. |
| **Performance** | N/A |
| **Downstream** | `lic` must ship matching module aliases and error types; explorer digest/issue text should reference `import io` etc. when filing PH-IO gaps. |
