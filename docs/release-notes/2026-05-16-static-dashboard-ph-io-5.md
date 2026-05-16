# PH-IO-5 — static GitHub Pages dashboard (no Node)

## Summary

GitHub Pages deploys `static-dashboard/` built by `lic` `std/plot` (`plot_render_dashboard`) instead of the Vite `dashboard/` npm bundle on the critical path.

## Agent continuation

1. **Read:** `scripts/dashboard/render-static.sh`, `lic` `runtime/li_rt_plot.c`, `.github/workflows/pages.yml`.
2. **Run:** `LIC_ROOT=../lic ./scripts/dashboard/render-static.sh` after `data/latest/summary.json` exists; open `static-dashboard/index.html`.
3. **Then:** merge `lic` PH-IO-5; pin `lic` ref in Pages workflow after release; PH-IO-6 `std/io` for compiler `-o`.
4. **Blocked on:** `li-langverse/lic` PH-IO-5 merge (CI checks out `main` until branch lands).

## Changed

| Area | Path | Evidence |
|------|------|----------|
| Render | `scripts/dashboard/render_dashboard.li`, `render-static.sh` | SVG in `index.html` |
| CI | `.github/workflows/pages.yml`, `ci.yml` `dashboard-static` | LLVM + lic build + render |
| Ignore | `.gitignore` | generated `static-dashboard/*` except `.gitkeep` |

## Not changed

- Vite `dashboard/` (optional `npm run dev` for interactive filters).
- Python `build_summary.py` and `summary.json` schema.
- Ingest dispatch workflow (`ingest.yml`).
- PH-IO-4 CSV smoke (still runs in `ingest-lic.sh`).

## Breaking

N/A — Pages artifact path is `static-dashboard/` instead of `dashboard/dist`; same public URL.

## Security

N/A — read-only render of committed `summary.json`; path validation in `li_rt_plot` / `li_rt_io`.

## Performance

N/A — deploy-time only.

## Downstream

Merge order: **lic** PH-IO-5 → **benchmarks** this PR → verify Pages workflow green.
