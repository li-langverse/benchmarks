# GitHub setup (human-only)

1. Create `li-langverse/benchmarks` (see [roadmap SETUP_GITHUB.md](../roadmap/SETUP_GITHUB.md)).
2. **Settings → Pages → GitHub Actions** — deploy from `pages.yml` (not “Deploy from branch”).
3. Secret `BENCHMARKS_INGEST_TOKEN` (optional): PAT with `contents:write` for ingest bot commits.
4. On **lic**: secret `LI_BENCHMARKS_DISPATCH_TOKEN` to call `repository_dispatch` on ingest workflow.

Ingest triggers: `workflow_dispatch`, `repository_dispatch` (`lic-bench-complete`, `package-release`), push to `data/**` on PRs. Release manifests: [docs/dashboard/release-manifest.md](docs/dashboard/release-manifest.md).

## Fix package handbook 404 (`live_docs_down`)

Handbook content may already be on `main` while Pages is disabled. From **benchmarks**:

```bash
./scripts/enable-org-handbook-pages.sh
```

Or per repo: **Settings → Pages → Build and deployment → GitHub Actions**, then run **Handbook (Pages)** workflow on `main`.

## Fix dashboard 404 (`live_docs_down`)

`ecosystem-audit.py` HEAD-checks https://li-langverse.github.io/benchmarks/ — **404** means Pages is not published yet.

1. **Org/repo exists** — `gh repo view li-langverse/benchmarks`
2. **Pages source** — Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**
3. **Enable via API** (optional):  
   `gh api repos/li-langverse/benchmarks/pages -X POST -f build_type=workflow`
4. **Run deploy** — push to `main` touching `data/latest/**` or `scripts/dashboard/**`, or:  
   `gh workflow run pages.yml --repo li-langverse/benchmarks`
5. **Wait for green** — workflow **Deploy dashboard** → environment **github-pages**
6. **Verify** — `curl -sI https://li-langverse.github.io/benchmarks/ | head -1` → `HTTP/2 200`

Or run [`scripts/publish-github-pages.sh`](scripts/publish-github-pages.sh) from a machine with `with-github-env.sh` + push access.

**Local fallback (no Pages):** `LIC_ROOT=../li ./scripts/dashboard/render-static.sh` → open `static-dashboard/index.html`.

Handbook: [docs/handbook/README.md](docs/handbook/README.md).
