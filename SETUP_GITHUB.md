# GitHub setup (human-only)

1. Create `li-langverse/benchmarks` (see [roadmap SETUP_GITHUB.md](../roadmap/SETUP_GITHUB.md)).
2. **Settings → Pages → GitHub Actions** — deploy from `pages.yml`.
3. Secret `BENCHMARKS_INGEST_TOKEN` (optional): PAT with `contents:write` for ingest bot commits.
4. On **lic**: secret `LI_BENCHMARKS_DISPATCH_TOKEN` to call `repository_dispatch` on ingest workflow.

Ingest triggers: `workflow_dispatch`, `repository_dispatch` (`lic-bench-complete`), push to `data/**` on PRs.
