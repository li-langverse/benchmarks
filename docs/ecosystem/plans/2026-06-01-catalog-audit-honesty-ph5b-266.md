# Catalog audit honesty — repo field, vertical stubs, competitive rows (PH-5b / REQ-BENCH-CATALOG-1)

> **Issue:** [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266)  
> **Related:** [#179](https://github.com/li-langverse/benchmarks/issues/179) (duplicate — reconcile on close), [#20](https://github.com/li-langverse/benchmarks/issues/20)–[#29](https://github.com/li-langverse/benchmarks/issues/29) (LIC_ROOT), [single-repo ADR](../benchmarks-single-repo-layout.md), [prior reconciliation plan](./2026-05-31-catalog-path-reconciliation-ph5b.md)  
> **Repo:** li-langverse/benchmarks (+ lic toolchain only for tier-0 proofs)  
> **Vision:** **Provable** (honest catalog + dashboard), **Fast** (measurement surface for PH-5b / PH-7e)  
> **north_star_fit:** Scientific computing / HPC benchmark posture — **PH-5b** (competitive catalog + ingest honesty), **PH-7e** (tier-1 pure-Li rows unaffected by catalog-only work)  
> **Learned from:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md), [engineering-standards.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md), [benchmarks-single-repo-layout.md](../benchmarks-single-repo-layout.md), [benchmark-dashboard honesty](../../honesty/benchmark-dashboard.md)

## Goal

Eliminate **false `catalog_gaps`** from `plan-completion-audit.py` and dashboard overclaim by aligning `catalog.toml` with the **benchmarks-only workload ADR**: paths that live under `benchmarks/workloads/` must use `repo = "benchmarks"`. Separately, mark **competitive-vertical stub rows** (algo_registry remaps, tier-2 physics ahead of harness) as explicitly `catalog_lifecycle = "planned"` with honest `path = "unknown"` where no dedicated workload exists — **no silent deletion** and **no bogus path reuse** (e.g. `bio_proteinmpnn` must not point at `num_sparse_mv`).

## Non-goals

- Implementing tier-2 CFD/MD/QM kernels in this plan (tracked under **lic** / **benchmarks** workload PRs post-approval).
- Weakening `threshold_ratio_cpp` or marking rows green without measurements.
- Copying harness back into `lic/benchmarks/` (deprecated per ADR).
- Closing **G-math** / **G-par** provability gaps via catalog edits alone.

## Root cause (2026-06-01 preflight)

| Signal | Count | Notes |
|--------|------:|-------|
| Rows with `repo = "lic"` but path exists under **benchmarks** | **139** | Audit checks `LIC_ROOT`; ADR moved workloads to benchmarks |
| **Bogus vertical remaps** (`bio_*`, `drug_*`, `am_*` → `tier1_micro/*`) | **9** | Dashboard shows wrong workload id vs path |
| True missing paths (`repo = "benchmarks"`, path absent) | **7** | Tier-2 / competitive stubs — mark `planned` or implement |
| Audit `catalog_gaps` with `LIC_ROOT=/tmp/lic` | **~146** | Dominated by repo-field mismatch, not missing harness |

## Dependencies

- **PH-5b** — master plan phase **5b** (benchmark catalog + dashboard).
- **PH-7e** — perf work stays on **lic** codegen; catalog honesty is prerequisite only.
- Merged **LIC_ROOT** resolver ([PR #135](https://github.com/li-langverse/benchmarks/pull/135)).
- Human: label **`plan-approved`** before implementation PRs; approve dashboard UX for `planned` rows.

## Sub-phases

| Sub | Deliverable | Owner | Exit gate |
|-----|-------------|-------|-----------|
| **A** | **`repo` correction** — script `scripts/catalog/fix-catalog-repo-field.py` sets `repo = "benchmarks"` when `benchmarks/<path>` exists | benchmarks | `plan-completion-audit` `catalog_gaps` ≤ 20 with `LIC_ROOT` + `BENCHMARKS_ROOT` |
| **B** | **Bogus remap purge** — 9 vertical ids: `path = "unknown"`, `catalog_lifecycle = "planned"`, `variant = "vertical_stub"`; remove shared `tier1_micro` alias | benchmarks | `check-dashboard-invariants.py` passes; matrix shows `planned` not `skip` with fake path |
| **C** | **Competitive / tier-2 stubs** — rows from `sync-from-algo-registry.py` without `benchmarks/workloads/...` dir → `planned` + `ph_ids` | benchmarks | Audit `catalog_gaps_actionable` only lists rows pending real harness |
| **D** | **Audit split** — `plan-completion-audit.py` emits `catalog_gaps_actionable`, `catalog_gaps_repo_mismatch`, `lic_present`, `benchmarks_root` in JSON | benchmarks | Agent briefing surfaces mismatch separately from true gaps |
| **E** | **Sync script ADR** — `sync-paths-from-lic-tree.py` walks `benchmarks/workloads/` (not `lic/benchmarks`); deprecate lic-tree walk | benchmarks | Docs in `plan-cross-links.md` updated |
| **F** | **lic** follow-ups (separate PRs) — tier-2 physics harness clusters per [tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md) | lic | Linked issues from catalog; not blocking honesty PR |

## Tests / benches

- `python3 scripts/plan-completion-audit.py` — `catalog_gaps_actionable` documented in issue comment artifact.
- `python3 scripts/check-dashboard-invariants.py` — no row claims `repo=lic` for benchmarks-only paths.
- `python3 scripts/catalog/audit-catalog-coverage.py` — competitive vertical policy.
- Ingest smoke: `./scripts/ingest/ingest-lic.sh` after catalog PR (row count stable).
- Sample tier-1: `num_sparse_mv`, `num_cg` — unchanged paths, corrected `repo`.
- Sample vertical: `bio_proteinmpnn` — must not resolve to `num_sparse_mv` path in summary.

## Provability

- **G-math** — remains **Partial**; catalog honesty does not imply proof closure.
- **G-par** — unchanged.
- Do not mark tracker **PH-5b** complete in master plan until actionable gaps ≤ 20 **and** tier-1 red/yellow policy satisfied separately.

## Rollout

1. **This PR (draft):** plan doc only — [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266).
2. After **`plan-approved`:** benchmarks PR — sub-phases A–E (catalog + audit script; ≤200 row diff).
3. **lic** issues (sub-phase F): one issue per physics cluster; link from catalog comments.
4. Re-run audit; attach `data/latest/plan-completion-audit.json` snippet to #266.
5. Close **#179** as duplicate of #266 when A–D land.

## Human-only

- Approve `catalog_lifecycle = "planned"` badge copy on dashboard.
- Confirm competitive-vertical policy: defer vs implement for bio/drug/am stubs.
- Add **`plan-approved`** label; remove **`plan-needed`**.

## Issue reconciliation

| Issue | Action |
|-------|--------|
| **#266** | Canonical tracking issue for this plan |
| **#179** | Duplicate — close when implementation PR merges |
| **#20–#29** | LIC_ROOT layout — already addressed; verify `lic_present` in audit JSON |
