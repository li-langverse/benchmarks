# GitHub setup (human-only)

1. Create `li-langverse/benchmarks` (see [roadmap SETUP_GITHUB.md](../roadmap/SETUP_GITHUB.md)).
2. **Settings → Pages → GitHub Actions** — deploy from `pages.yml` (not “Deploy from branch”).
3. Secret `BENCHMARKS_INGEST_TOKEN` (optional): PAT with `contents:write` for ingest bot commits.
4. On **lic**: secret `LI_BENCHMARKS_DISPATCH_TOKEN` to call `repository_dispatch` on ingest workflow.

Ingest triggers: `workflow_dispatch`, `repository_dispatch` (`lic-bench-complete`), push to `data/**` on PRs.

## Fix dashboard 404 (`live_docs_down`)

`ecosystem-audit.py` HEAD-checks https://li-langverse.github.io/benchmarks/ — **404** means Pages is not published yet.

1. **Org/repo exists** — `gh repo view li-langverse/benchmarks`
2. **Pages source** — Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**
3. **Enable via API** (optional):  
   `gh api repos/li-langverse/benchmarks/pages -X POST -f build_type=workflow`
4. **Run deploy (no Actions)** — from a machine with `gh` + push access:  
   `./scripts/deploy-pages-local.sh --build`  
   (builds Vite dashboard, pushes `gh-pages`, sets Pages source to branch deploy)
5. **Verify** — `curl -sI https://li-langverse.github.io/benchmarks/ | head -1` → `HTTP/2 200`

**Actions alternative:** `gh workflow run pages.yml --repo li-langverse/benchmarks` or `./scripts/deploy-pages-local.sh --workflow`

Or run [`scripts/publish-github-pages.sh`](scripts/publish-github-pages.sh) (wraps local deploy).

**Offline preview (no GitHub):** `LIC_ROOT=../lic ./scripts/dashboard/render-static.sh` → open `static-dashboard/index.html`.

**Refresh benchmark data (no ingest Actions):**  
`LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh` then `./scripts/deploy-pages-local.sh --build`

Handbook: [docs/handbook/README.md](docs/handbook/README.md).
