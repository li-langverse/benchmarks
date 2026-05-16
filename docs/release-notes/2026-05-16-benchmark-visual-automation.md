# Release notes: 2026-05-16 — benchmark-visual-automation

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PH / REQ:** PH-5b  
**Author:** agent

---

## Summary (one sentence)

Adds Cursor Automation prompt and scripts to render lic physics/math visuals, vision-validate against cpp oracle, and publish download links (manifest + zip) in PRs.

## Agent continuation (required)

1. Merge PR; create automation from `.cursor/automations/benchmark-visual-validation.md` (weekly; repos `lic` + `benchmarks`; Open PR).
2. Run `LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh` locally once.
3. Agent must paste raw GitHub links + vision verdict in each run.
4. Blocked on: lic not checked out / no matplotlib.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Automation | `.cursor/automations/benchmark-visual-validation.md` | Vision + download link workflow |
| Scripts | `render-benchmark-visuals.sh`, `visual-manifest.py` | `data/visuals/latest/` + zip |
| Docs | `data/visuals/README.md` | Asset layout |

## Not changed (scope fence)

- lic `animate_physics.py` grid dump wiring — still stub for wave/heat grids
- Pages dashboard — still JSON charts only; visuals via PR raw links
- Actions cron — none

## Breaking changes

None.

## Security

N/A — public plots only; no tokens in manifests.

## Performance

N/A — local render; do not commit huge GIFs to main by default.

## Downstream

| Repo | Action |
|------|--------|
| lic | Source of `plot_shareables.sh` |

## CHANGELOG entry

### Added

- Benchmark visual validation automation + `scripts/render-benchmark-visuals.sh`.
