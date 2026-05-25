# Benchmark dashboard ship integration (regression gates)

## Summary

Merges dashboard ship stack (PR #85): **169-row** catalog/summary, `dashboard-next` facet matrix, and **CI invariant scripts** so row-count and honesty regressions fail PRs before Pages deploy.

## Agent continuation

1. **Read:** `docs/dashboard/SHIP-STATUS.md`, `docs/dashboard/INVARIANTS.md`, `docs/dashboard/ARCHITECTURE.md`.
2. **Run:** `python3 scripts/check-dashboard-invariants.py`; `cd dashboard-next && npm ci && npm run build && bash ../scripts/check-dashboard-static-routes.sh`; confirm Benchmarks CI `ingest-smoke` + `dashboard-build` on `main`.
3. **Next:** Wire **lic** harness CSV for high-priority `path=unknown` ids; re-run `./scripts/ingest/ingest-lic.sh` and commit refreshed `summary.json` when ratios are real (not fixture-only).
4. **Blocked:** Live site stays at 35 rows until `main` includes this branch's `data/latest/summary.json` and Pages workflow completes; ~109 stubs remain `unknown` by design.

## Changed

| Area | Paths / evidence |
|------|------------------|
| Docs | `docs/dashboard/ARCHITECTURE.md`, `INVARIANTS.md`, `SHIP-STATUS.md`; README + `AGENTS.md` + `design-system.md` links |
| CI | `.github/workflows/ci.yml` — `Dashboard invariants`, `Dashboard static routes` steps |
| Scripts | `scripts/check-dashboard-invariants.py`, `scripts/check-dashboard-static-routes.sh` |
| Integration | PR #85 — catalog 169, summary 169, SOTA/validity/OS, matrix facet IA (supersedes #79–#82) |
| Data | `data/latest/summary.json` committed (fixture ingest parity) |

## Not changed

- **lic**/**lis** production CSV refresh on every PR (fixture path for dashboard artifact).
- Demo video PR #78 (docs-only).
- Weakening min row count or stub bans without human approval.

## Breaking

N/A — additive dashboard + CI gates.

## Security

N/A — honesty enforcement only; no trusted creep.

## Performance

N/A — static export; invariant checks are O(n) on JSON.

## Downstream

Pages workflow copies `data/latest/*.json` into `dashboard-next/out/latest/` on push to `main` when `data/latest/**` or `dashboard-next/**` changes.
