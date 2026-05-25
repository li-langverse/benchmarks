# WP3 release manifest ingest foundation

## Summary

Adds JSON Schema and ingest for per-package `v*` release manifests into `data/latest/release-index.json`, plus `package-release` repository dispatch on the benchmarks ingest workflow.

## Agent continuation

1. **Read:** `docs/dashboard/release-manifest.md`, `schema/release-manifest.json`, `scripts/ingest/ingest-release-manifests.py`.
2. **Run:** `python3 scripts/ingest/ingest-release-manifests.py` after dropping manifests in `data/incoming/manifests/`; then `./scripts/ingest/ingest-lic.sh` only when a real CSV exists.
3. **Next:** Wire lic/lis/lip tag CI to dispatch `package-release` with `client_payload.manifest`; do not fabricate `summary.json` rows from manifests alone.
4. **Blocked:** Org secret `LI_BENCHMARKS_DISPATCH_TOKEN` on each publishing repo (human).

## Changed

- `schema/release-manifest.json` — manifest contract
- `scripts/ingest/ingest-release-manifests.py` — merge → `data/latest/release-index.json`
- `data/incoming/manifests/` — incoming staging (`.gitkeep`, `example-lic.json`)
- `.github/workflows/ingest.yml` — `package-release` dispatch, manifest stage step, index commit
- `docs/dashboard/release-manifest.md`, `SETUP_GITHUB.md`, `CHANGELOG.md`

## Not changed

- `data/latest/summary.json` build logic (`build_summary.py`, `ingest-lic.sh`)
- Dashboard Vite UI (no release-index panel yet)
- lic `lic-bench-complete` artifact contract

## Breaking

N/A — new files and optional dispatch type.

## Security

N/A — manifests are public metadata; no secrets in example manifest.

## Performance

N/A — index merge only; no benchmark execution.

## Downstream

Publishing repos should document dispatch in their release workflow README when secrets are provisioned.
