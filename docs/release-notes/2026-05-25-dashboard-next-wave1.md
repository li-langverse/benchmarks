# Dashboard Next wave 1 — pillars, release manifests, Next scaffold

## Summary

Adds `dashboard-next/` (Next 15 static export), pillar fields in `catalog.toml` + `summary.json`, `ecosystem-packages.toml` registry, and `package-release` ingest path without fabricating bench rows.

## Agent continuation

1. **Read:** `docs/dashboard/design-system.md`, `docs/dashboard/release-manifest.md`, `dashboard-next/README.md`, `ecosystem-packages.toml`.
2. **Run:** `cd dashboard-next && npm ci && npm run build`; `LIC_ROOT=../lic python3 scripts/ingest/build_summary.py ../lic ../lis`; `python3 scripts/ingest/ingest-release-manifests.py`.
3. **Then:** WP5–WP7 on `dashboard-next` (bento overview, pillar filtering, `/matrix`, history UI); WP8 switch `pages.yml` to `dashboard-next/out`; wire `release-index.json` banner on home page.
4. **Blocked on:** Per-repo `v*` tag workflows dispatching `package-release` (lic/lis/lip/lit/lidb/lig/li-math) — not in this PR.

## Changed

| Area | Paths |
|------|--------|
| Next dashboard | `dashboard-next/**` — `/`, `/pillar/[id]`, `/bench/[id]`, basePath `/benchmarks` |
| Design / IA | `docs/dashboard/design-system.md`, `sitemap.md` |
| Catalog pillars | `catalog.toml` — `pillar`, `package`; stubs `lig_viewport_stub`, `li_math_gemm_stub` |
| Ingest | `scripts/ingest/build_summary.py` — `pillars` map (8 pillars); `ecosystem-packages.toml` |
| Release ingest | `schema/release-manifest.json`, `scripts/ingest/ingest-release-manifests.py`, `.github/workflows/ingest.yml` `package-release` |
| History | `scripts/record-benchmark-history.py` — skip snapshot when summary content hash unchanged |
| Schema | `schema/bench-result.json` — optional `pillar`, `package`, `tags` |

## Not changed

- GitHub Pages still deploys **Vite** `dashboard/` (WP8).
- **lic/lis** tag → dispatch workflows in owning repos.
- Bench thresholds and harness measurements (no threshold tweaks).
- Agent control plane UI in **li-cursor-agents** (`dashboard-ui/`).
- Proof closure in **lic** (`provability-gaps.md`); `/proofs` sidecar page is WP4/WP6.

## Breaking

N/A — additive; Vite dashboard remains until WP8 cutover.

## Security

N/A — static site; manifests validated against `ALLOWED_PACKAGES`; no secrets in `data/incoming/manifests/`.

## Performance

N/A — no new harness runs; ingest emits `pillars` from existing CSVs when present.

## Downstream

- Agents should deep-link `/benchmarks/bench/<id>/` after WP6 URLs ship on Pages.
- `agent-briefing.py` pillar summary (WP9).
