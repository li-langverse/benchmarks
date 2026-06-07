# Catalog path reconciliation — repo-field honesty refresh (PH-5b / REQ-BENCH-CATALOG-1)

> **Issue:** [benchmarks#179](https://github.com/li-langverse/benchmarks/issues/179)  
> **Implementation track:** [benchmarks#266](https://github.com/li-langverse/benchmarks/issues/266) (`plan-approved`, [plan doc](./2026-06-01-catalog-audit-honesty-ph5b-266.md))  
> **Related:** [#20](https://github.com/li-langverse/benchmarks/issues/20)–[#29](https://github.com/li-langverse/benchmarks/issues/29) (LIC_ROOT), [single-repo ADR](../benchmarks-single-repo-layout.md), [prior reconciliation](./2026-05-31-catalog-path-reconciliation-ph5b.md)  
> **Repo:** li-langverse/benchmarks (+ lic toolchain for tier-0 proofs only)  
> **Vision:** **Provable** (honest catalog + dashboard), **Fast** (measurement surface for PH-5b / PH-7e)  
> **north_star_fit:** Scientific computing / HPC benchmark posture — **PH-5b** (competitive catalog + ingest honesty), **PH-7e** (tier-1 pure-Li perf unaffected by catalog-only work)  
> **Learned from:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md), [engineering-standards.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md), [benchmarks-single-repo-layout.md](../benchmarks-single-repo-layout.md), [benchmark-dashboard honesty](../../honesty/benchmark-dashboard.md)

## Goal

Close the **master-plan-gap** on #179: stop `plan-completion-audit.py` and dashboard ingest from overclaiming coverage when `catalog.toml` rows point at paths that do not exist under the resolved `LIC_ROOT`. After the **benchmarks-only workload ADR** (2026-05-30), most gaps are **repo-field mismatch** (`repo = "lic"` on rows whose workloads live under `benchmarks/workloads/`), not missing harness trees. This refresh reconciles #179 with the approved implementation plan on **#266**.

## Non-goals

- Implementing tier-2 CFD/MD/QM kernels (tracked under **lic** / **benchmarks** workload PRs post-approval).
- Weakening `threshold_ratio_cpp` or marking rows green without measurements.
- Copying harness back into `lic/benchmarks/` (deprecated per ADR).
- Closing **G-math** / **G-par** provability gaps via catalog edits alone.
- Silent catalog deletion to green the audit.

## Root cause (2026-06-07 preflight)

| Signal | Count | Notes |
|--------|------:|-------|
| `catalog.toml` rows with `repo = "lic"` | **147** | Audit validates paths under `LIC_ROOT` |
| Audit `catalog_gaps` with `LIC_ROOT=/tmp/lic` | **146** | Dominated by `benchmarks/workloads/...` paths absent under lic |
| **Bogus vertical remaps** (`bio_*`, `drug_*`, `am_*` → `tier1_micro/*`) | **9** | Dashboard shows wrong workload id vs path |
| True missing workload dirs (`repo = "benchmarks"`, path absent) | **~7** | Tier-2 / competitive stubs — mark `planned` or implement |
| Tier-0 `tier0_stability` | **1** | Correctly under `lic/li-tests` — separate track |

The original **117-gap** spike and the brief **0-gap** window (2026-05-31) reflected resolver/checkout variance, not sustained honesty. With ADR migration complete, the actionable fix is **repo-field correction + planned-row policy**, not creating duplicate trees under lic.

## Dependencies

- **PH-5b** — master plan phase **5b** (benchmark catalog + dashboard).
- **PH-7e** — perf work stays on **lic** codegen; catalog honesty is prerequisite only.
- Merged **LIC_ROOT** resolver ([PR #135](https://github.com/li-langverse/benchmarks/pull/135)).
- **#266** implementation plan (`plan-approved`) — canonical code path for sub-phases A–E.
- Human: label **`plan-approved`** on #179 (or close as duplicate of #266 after plan merge).

## Sub-phases

| Sub | Deliverable | Owner | Exit gate |
|-----|-------------|-------|-----------|
| **A** | **`repo` correction** — `scripts/catalog/fix-catalog-repo-field.py` sets `repo = "benchmarks"` when `benchmarks/<path>` exists | benchmarks | `catalog_gaps` ≤ 20 with `LIC_ROOT` + `BENCHMARKS_ROOT` |
| **B** | **Bogus remap purge** — 9 vertical ids: `path = "unknown"`, `catalog_lifecycle = "planned"`, `variant = "vertical_stub"` | benchmarks | `check-dashboard-invariants.py` passes |
| **C** | **Competitive / tier-2 stubs** — rows without `benchmarks/workloads/...` dir → `planned` + `ph_ids` | benchmarks | Audit actionable gaps only list rows pending real harness |
| **D** | **Audit split** — `plan-completion-audit.py` emits `catalog_gaps_actionable`, `catalog_gaps_repo_mismatch`, `lic_present` | benchmarks | Agent briefing surfaces mismatch separately |
| **E** | **Sync script ADR** — `sync-paths-from-lic-tree.py` walks `benchmarks/workloads/` (not `lic/benchmarks`) | benchmarks | `plan-cross-links.md` updated |
| **F** | **lic** follow-ups — tier-2 physics harness clusters per [tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md) | lic | Linked issues; not blocking honesty PR |

> **Note:** Sub-phases A–F are specified in full on [#266](./2026-06-01-catalog-audit-honesty-ph5b-266.md). #179 tracks the **master-plan-gap**; implementation agents should target **#266** PRs (#305, #323, #336, etc.).

## Tests / benches

- `python3 scripts/plan-completion-audit.py` with `LIC_ROOT` + `BENCHMARKS_ROOT` — attach `catalog_gaps_actionable` snippet.
- `python3 scripts/check-dashboard-invariants.py` — no `repo=lic` for benchmarks-only paths.
- `python3 scripts/catalog/audit-catalog-coverage.py` — competitive vertical policy.
- Ingest smoke: `./scripts/ingest/ingest-lic.sh` after catalog PR.
- Sample fixes: `horner_pure_li`, `num_cg` — `repo = "benchmarks"`; `bio_proteinmpnn` — must not alias `num_sparse_mv`.

## Provability

- **G-math** — remains **Partial**; catalog honesty does not imply proof closure.
- **G-par** — unchanged.
- Do not mark tracker **PH-5b** complete until actionable gaps ≤ 20 **and** tier-1 red/yellow policy satisfied separately (**PH-7e**).

## Rollout

1. **This PR (draft):** plan refresh for #179 — reconciles with merged [PR #263](https://github.com/li-langverse/benchmarks/pull/263) and #266 track.
2. Maintainer: add **`plan-approved`** on #179 **or** close #179 as duplicate of #266 when plan merged.
3. After approval: benchmarks PR implementing sub-phases A–E (via #266 implementer queue).
4. **lic** issues (sub-phase F): one issue per physics cluster.
5. Close **#179** when audit `catalog_gaps_actionable` ≤ 20 and dashboard shows honest `planned` rows.

## Human-only

- Approve `catalog_lifecycle = "planned"` badge copy on dashboard.
- Confirm competitive-vertical policy: defer vs implement for bio/drug/am stubs.
- Add **`plan-approved`** label on #179; remove **`plan-needed`** if present.
- Choose whether #179 stays open as parent tracker or closes as duplicate of #266.

## Issue reconciliation

| Issue | Action |
|-------|--------|
| **#179** | Plan refresh (this doc); close when #266 implementation lands |
| **#266** | Canonical **`plan-approved`** implementation track |
| **#29** | Closed — LIC_ROOT layout merged via PR #135 |
| **#20–#28** | Close when audit split + repo-field fix verified on CI |
