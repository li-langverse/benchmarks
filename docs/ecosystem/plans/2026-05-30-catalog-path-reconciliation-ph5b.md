# Catalog path reconciliation — 117 missing lic paths (PH-5b / REQ-BENCH-CATALOG-1)

> **Issue:** [benchmarks#179](https://github.com/li-langverse/benchmarks/issues/179)  
> **Related:** [#20](https://github.com/li-langverse/benchmarks/issues/20)–[#29](https://github.com/li-langverse/benchmarks/issues/29), [LIC_ROOT plan](./2026-05-18-lic-root-audit-layout.md), [tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md)  
> **Repo:** li-langverse/benchmarks + li-langverse/lic  
> **Vision:** **Provable** (honest catalog), **Fast** (measurement surface for PH-5b/PH-7e)  
> **Learned from:** [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md), [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md), `plan-completion-audit.json` (117 `catalog_gaps`), [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md)

## Goal

Reduce `plan-completion-audit` **catalog_gaps** from 117 to an honest set: fix mis-mapped `catalog.toml` paths where harness already exists under **lic**, mark aspirational rows `status = "planned"` until harness lands, and split tier-2 physics stubs to **lic** implementation issues — without weakening `threshold_ratio_cpp` or copying harness into **benchmarks**.

## Non-goals

- Copying `lic/benchmarks/harness` into **benchmarks** (ingest-only per AGENTS.md).
- Weakening benchmark thresholds to green incomplete kernels.
- Claiming **G-math** / **G-par** closure from catalog edits alone.
- Bulk-removing catalog rows without master-plan / PH-5b alignment.

## Dependencies

- **PH-5b** — harness ownership in **lic**; catalog is dashboard index only.
- **PH-7e** — tier-1 red rows (`matmul_*`, `ml_*`, `num_gmres`) need **lic** perf work, not catalog-only fixes.
- [PR #135](https://github.com/li-langverse/benchmarks/pull/135) — LIC_ROOT resolver (reduces false positives when sibling checkout missing).
- **lic** stacked PRs for missing tier-2 physics dirs ([tier-2 sync plan](./2026-05-18-tier2-catalog-lic-sync.md)).
- Human: **`plan-approved`** before implementation PRs.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | **Triage script** `scripts/catalog-gap-triage.py` — classify each gap: `fix_path`, `planned`, `lic_impl`, `remove` | JSON report in `data/latest/catalog-gap-triage.json` |
| B | **Path fixes** — correct mis-mapped bio/drug/am rows pointing at wrong tier-1 micro paths | ≤30 rows fixed where harness exists elsewhere in lic tree |
| C | **Catalog schema** — optional `status = "planned"` + `planned_ph` on rows without harness | Audit skips or tags planned rows; dashboard shows planned badge |
| D | **lic** issues/PRs — one per missing tier-2 kernel cluster (CFD, MD, QM stubs) | Each cluster has lic owner issue linked from catalog |
| E | **Reconcile with audit** — `plan-completion-audit.py` respects `status=planned`; emit `catalog_gaps_actionable` vs `catalog_gaps_planned` | Actionable gaps ≤20 after lic paths land or defer |

## Tests / benches

- `python3 scripts/plan-completion-audit.py` with `LIC_ROOT=../lic` — actionable gaps documented.
- `python3 scripts/check-dashboard-invariants.py` — row count stable; no silent unknown regression.
- Tier-1 red benches remain tracked separately (lic#424, lic#463); catalog sync does not fake green.
- Ingest smoke: `./scripts/ingest/ingest-lic.sh` for fixed-path rows produces CSV or explicit skip.

## Provability

- **G-math** — stays **Partial** until proofs + green tier-1 where claimed; catalog honesty only.
- **G-par** — unchanged; no perf claims from path mapping.
- Update **provability-gaps.md** only when **lic** harness + proof evidence land (not from this PR alone).

## Rollout

1. **benchmarks** draft PR: this plan + triage script (after **`plan-approved`**).
2. Scoped **benchmarks** PR: `catalog.toml` path fixes + `status=planned` (≤50 rows per PR).
3. **lic** PR(s): missing harness directories (separate repo, proof-before-perf).
4. Cross-link and close #179 when actionable gaps ≤20; remove `plan-needed`.

## Human-only

- Approve `status=planned` policy for dashboard UX (planned vs missing).
- Prioritize which tier-2 physics clusters land on **lic** `main` vs contributor branches.
