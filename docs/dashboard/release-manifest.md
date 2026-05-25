# Release manifest ingest (WP3)

The benchmarks repo tracks **published package versions** separately from **measured** CSV rows. Release manifests declare what shipped; ingest and `summary.json` still require real benchmark artifacts.

## Schema

[`schema/release-manifest.json`](../../schema/release-manifest.json) defines each manifest:

| Field | Purpose |
|-------|---------|
| `package` | One of `lic`, `lis`, `lip`, `lit`, `lidb`, `lig`, `li-math` |
| `version` | Tag or semver (e.g. `v0.4.0`) |
| `git_sha` | Commit at publish |
| `published_at` | ISO-8601 timestamp |
| `bench_required` | Dashboard should refresh CSV when artifacts exist |
| `artifacts` | `{path, kind}` with `kind` ∈ `csv` \| `manifest` \| `other` |

Paths are **repo-relative under benchmarks** (typically `data/incoming/...` or a dispatch-staged file).

## Tag `v*` workflow (per repo)

On each ecosystem repo, when a maintainer tags `v*`:

1. **Build release metadata** — version from tag, `git_sha` from the tagged commit, `published_at` from the release time.
2. **Attach artifacts** (optional but recommended when `bench_required` is true):
   - `kind: csv` — path where CI will place `latest.csv` (or copy into `lic/benchmarks/results/latest.csv` before ingest).
   - `kind: manifest` — copy of this JSON for audit.
   - `kind: other` — checksums, SBOM, etc.
3. **Dispatch benchmarks ingest** — `repository_dispatch` event `package-release` on `li-langverse/benchmarks` with `client_payload` containing the manifest object (see below).
4. **Run benchmarks in the source repo** when perf is required — lic uses `lic-bench-complete` with the `benchmark-csv` artifact; benchmarks **never** invents rows from the manifest alone.

| Package | Typical bench owner | CSV / notes |
|---------|---------------------|-------------|
| **lic** | [`.github/workflows/benchmark-release.yml`](https://github.com/li-langverse/lic/blob/main/.github/workflows/benchmark-release.yml) on tag `v*` → `benchmark-csv` | `lic/benchmarks/results/latest.csv`; rebuilds when `benchmarks/**` changed since previous tag |
| **lis** | lis tier harness | `lis/results/latest.csv` (when present) |
| **lip**, **lit** | tooling smoke / catalog | often `bench_required: false` |
| **lidb**, **lig**, **li-math** | package-specific | set `bench_required` only when a CSV path is published |

**lic wired CI:** push tag `v*` runs [lic `benchmark-release`](https://github.com/li-langverse/lic/blob/main/.github/workflows/benchmark-release.yml) — conditional `ci-bench.sh`, always uploads `benchmark-csv` (`latest.csv`), dispatches `package-release` with `bench_required` from CSV presence.

Example-only file (not wired to CI): [`data/incoming/manifests/example-lic.json`](../../data/incoming/manifests/example-lic.json).

## Local ingest

```bash
# Drop manifests into data/incoming/manifests/*.json
python3 scripts/ingest/ingest-release-manifests.py
# → data/latest/release-index.json
```

If `bench_required` is true and a listed `kind: csv` path **exists on disk**, the index records `csv_refresh_needed` and a note — then run `./scripts/ingest/ingest-lic.sh` (or copy the CSV into `lic/benchmarks/results/latest.csv` first). No benchmark numbers are synthesized from the manifest.

## GitHub Actions: `package-release`

Repos need secret `LI_BENCHMARKS_DISPATCH_TOKEN` (see [SETUP_GITHUB.md](../../SETUP_GITHUB.md)).

```bash
gh api repos/li-langverse/benchmarks/dispatches \
  -f event_type=package-release \
  -f 'client_payload[package]=lic' \
  -f 'client_payload[version]=v0.4.0' \
  -f 'client_payload[git_sha]=<sha>' \
  -f 'client_payload[published_at]=2026-05-25T12:00:00Z' \
  -f 'client_payload[bench_required]=true' \
  -f 'client_payload[manifest]=<url-encoded-json-or-use-workflow-to-write-file>'
```

Preferred: pass a full `manifest` object in `client_payload` (same shape as the schema). The ingest workflow writes `data/incoming/manifests/<package>-<version>.json`, runs `ingest-release-manifests.py`, then `./scripts/ingest/ingest-lic.sh` when lic CSV paths or `lic-bench-complete` artifacts are present.

## `lic-bench-complete` (unchanged)

lic CI still dispatches `lic-bench-complete` with the `benchmark-csv` artifact. That path copies `artifacts/latest.csv` into `lic/benchmarks/results/latest.csv`, then runs manifest ingest and `ingest-lic.sh`.

## Output: `release-index.json`

```json
{
  "updated_at": "2026-05-25T12:00:00Z",
  "packages": {
    "lic": {
      "version": "v0.4.0",
      "git_sha": "abc…",
      "published_at": "…",
      "bench_required": true,
      "artifacts": [{ "path": "…", "kind": "csv" }],
      "manifest_source": "data/incoming/manifests/lic-v0.4.0.json",
      "csv_refresh_needed": true,
      "csv_artifact_paths": ["data/incoming/…/latest.csv"]
    }
  },
  "notes": ["lic: csv refresh needed (…)"
  ]
}
```

Agents: read this file for **what version is current**; read [`summary.json`](../../data/latest/summary.json) for **measured** ratios. See [benchmark honesty labels](../honesty/benchmark-dashboard.md).
