# Release notes: 2026-05-25 — demo-video-package

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** `feat/demo-video`  
**PH / REQ:** N/A (docs + recording helper)  
**Author:** agent

---

## Summary (one sentence)

Adds a 2–3 minute dashboard demo script, local recording guide, optional HTML storyboard, and `record-dashboard-demo.sh` to build/serve `dashboard-next` for same-day capture.

## Agent continuation (required)

1. Read: `docs/dashboard/demo-video-script.md`, `docs/dashboard/design-system.md`
2. Run: `./scripts/record-dashboard-demo.sh` → open printed URL → follow beats (no video committed)
3. Then: upload MP4 to release/assets or social channel; link from README if human approves
4. Blocked on: none

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Script | `docs/dashboard/demo-video-script.md` — beats, routes, &lt;15 min guide | paths |
| Storyboard | `docs/dashboard/demo-storyboard.html` — clickable local/Pages paths | static HTML |
| Record helper | `scripts/record-dashboard-demo.sh` — build, stage `out/latest`, `python3 -m http.server` | executable |
| Sitemap | link to demo docs | `docs/dashboard/sitemap.md` |

## Not changed (scope fence)

- `dashboard-next` UI components and routes
- GitHub Pages workflow (`pages.yml`)
- Ingest pipelines and `summary.json` generation
- No committed `.mp4` or other binary recording

## Breaking changes

None.

## Security

N/A — local static server binds `127.0.0.1` by default; no new secrets.

## Performance

N/A — docs and one-shot build script only.

## Downstream

| Repo | Action |
|------|--------|
| li-cursor-agents | optional link in control-plane onboarding docs |

## CHANGELOG entry (paste into Unreleased)

- **Demo video package:** dashboard walkthrough script, storyboard HTML, `record-dashboard-demo.sh` — [2026-05-25-demo-video-package.md](docs/release-notes/2026-05-25-demo-video-package.md).
