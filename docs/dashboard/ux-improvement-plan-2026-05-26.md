# Benchmark dashboard UX improvement plan (2026-05-26)

**Scope:** [dashboard-next/](https://github.com/li-langverse/benchmarks/tree/main/dashboard-next) (Next.js static export) + ingest honesty layer.  
**Audit basis:** WCAG 2.2 AA targets, internal [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md), [INVARIANTS](./INVARIANTS.md), Studio rubric [ui-ux-by-dimension](https://github.com/li-langverse/lic/blob/main/docs/game-dev/competitive-intel/ui-ux-by-dimension.md) (adapted for data dashboards), and `li-cursor-agents/scripts/check-dashboard-no-motion.mjs`.

**Live site:** https://li-langverse.github.io/benchmarks/

---

## Executive summary

The dashboard is **honest and information-dense** but optimized for agents who already know the catalog. This plan prioritizes **correctness visibility first** (analytical oracles, ULP deviation), then **scanability** (overview → drill-down), then **accessibility** (contrast, focus, motion). Performance claims stay gated by validity — no UX change may imply green = proved fast.

---

## Current strengths (keep)

| Area | What works |
|------|------------|
| Honesty | Validity gate, “Li never SOTA”, `PerfNotClaimable`, variant callouts |
| Structure | Pillar pages, per-bench drill-down, matrix facet table |
| Data model | `summary.json` ↔ `catalog.toml` parity checks in CI |
| Motion policy | No gratuitous animation (agent gate) |

---

## Gaps found in audit (2026-05-26)

### P0 — Correctness communication

| ID | Gap | Impact | Remediation |
|----|-----|--------|-------------|
| UX-B01 | No **analytical oracle** surface on bench pages | Users see wall-time colors without knowing if checksum matched math | **Done:** `NumericValidityPanel` + ingest `numeric_validity` from `verify_*` CSV |
| UX-B02 | `validity_source` jargon without plain English | Agents misread `latest.csv:perf_present` as full verify | Add one-line “what this means” map in `ValidityPanel` |
| UX-B03 | Iterative vs analytical not distinguished in matrix | `pure_li` red looks like “wrong math” | Matrix column: `oracle` = analytical \| iterative \| pending |

### P1 — Navigation and scanability

| ID | Gap | Impact | Remediation |
|----|-----|--------|-------------|
| UX-B04 | Overview lacks **tier-1 correctness strip** | Horner/simd regressions buried in bench list | Home card: “Tier-1 verify: N pass / M fail” linking to filtered matrix |
| UX-B05 | Search does not filter by `within_1ulp` / validity | Hard to find failing numeric rows | Extend `benchmark-search` with validity + oracle filters |
| UX-B06 | `pending` rows visually similar to measured | False confidence on catalog-only entries | Stronger `pending` pattern (hatched bar + “not measured”) in `perf-relative-bars` |
| UX-B07 | Long benchmark IDs wrap poorly on mobile | Horizontal scroll fatigue | `text-wrap: balance` on titles; truncate with full id in `title` tooltip |

### P1 — Accessibility (WCAG AA)

| ID | Gap | Impact | Remediation |
|----|-----|--------|-------------|
| UX-A01 | Status relies on **color alone** (green/yellow/red) | WCAG 1.4.1 | Badge text already present — add patterns/icons (✓ / ~ / ✗) in `Badge` |
| UX-A02 | Focus rings inconsistent on tables/links | Keyboard nav | Global `:focus-visible` outline in `globals.css` (2px accent) |
| UX-A03 | Muted text `#8b949e` on `#0d1117` | ~4.8:1 for small mono — borderline for AA small text | Bump muted to `#9ba3af` or increase table font to 0.95rem |
| UX-A04 | `ValidityPanel` / `dl` grids lack landmark hierarchy | Screen readers | Use `<section aria-labelledby>` + visible `<h3>` ids |

### P2 — Trust and agent ergonomics

| ID | Gap | Impact | Remediation |
|----|-----|--------|-------------|
| UX-T01 | No “last ingest” / git sha on overview | Stale data confusion | Header strip: `generated_at`, `lic` csv sha from `summary.sources` |
| UX-T02 | No export of verify deviation CSV | Agents re-parse logs | Link “Download verify metrics” → raw `latest.csv` filter docs |
| UX-T03 | History page deltas without validity context | Regressions vs oracle drift unclear | `deltasForBenchmark` show ΔULP when `numeric_validity` present |

### P2 — Visual design consistency

| ID | Gap | Impact | Remediation |
|----|-----|--------|-------------|
| UX-V01 | Inline styles mixed with Tailwind | Maintenance | Migrate bench panels to Tailwind utilities incrementally |
| UX-V02 | Chart bars unlabeled at a glance | Compare oracle unclear | Always show `compare_oracle` under chart title |
| UX-V03 | Matrix 5 facets dense on laptop | Cognitive load | Sticky first column + facet tooltips (one sentence each) |

---

## Phased roadmap

### Wave 1 (shipped in this PR — correctness)

- [x] Harness: analytical oracles + ULP reporting (`lic/benchmarks/harness/reference.py`)
- [x] CSV: `verify_ulps`, `verify_within_1ulp`, `oracle_kind`, `passed`, `os`
- [x] Ingest: `numeric_validity` on summary rows; validity from verify metrics
- [x] UI: `NumericValidityPanel` on `/bench/[id]`
- [x] Docs: this plan + updated `benchmark-dashboard.md` honesty section

### Wave 2 (1–2 weeks — scanability)

1. Overview tier-1 verify strip (UX-B04)
2. Matrix filters: validity, oracle, `within_1ulp` (UX-B05, UX-B03)
3. Pending vs measured visual language (UX-B06)
4. `ValidityPanel` plain-language sources (UX-B02)

### Wave 3 (2–4 weeks — accessibility & trust)

1. Badge icons + non-color cues (UX-A01)
2. Focus-visible pass on all routes (UX-A02)
3. Contrast token tweak (UX-A03)
4. Ingest metadata strip (UX-T01)
5. History ΔULP (UX-T03)

### Wave 4 (backlog — design system)

1. Tailwind migration for bench components (UX-V01)
2. Responsive matrix (UX-V03)
3. Optional: light theme for presentations (not default — dark is brand)

---

## Acceptance criteria (per wave)

| Wave | Gate |
|------|------|
| 1 | `horner_pure_li` row in `summary.json` has `numeric_validity.within_1ulp`; bench page renders panel |
| 2 | `check-dashboard-invariants.py` green; matrix filter e2e (Playwright) for validity=fail |
| 3 | `check-dashboard-no-motion.mjs` green; axe-core smoke on `/` and `/bench/horner_pure_li` (0 critical) |
| 4 | Design tokens doc in `dashboard-next/README.md` |

---

## Skills and rules to use when implementing

| Resource | Use when |
|----------|----------|
| [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md) | Any color/status copy |
| [INVARIANTS](./INVARIANTS.md) | Before changing ingest or row counts |
| `check-dashboard-invariants.py` | Every catalog/summary PR |
| `check-dashboard-no-motion.mjs` | After CSS/animation changes |
| Studio `ui-ux-by-dimension` | Borrow UX-10 (a11y), UX-13 (perf honesty), UX-14 (marketing truth) — **not** viewport FPS gates |
| Canvas skill | Only if building interactive exploration (e.g. ULP histogram) — prefer static panel first |

---

## Non-goals

- Claiming **Lean proof** from dashboard green (see lic provability gaps)
- Replacing CSV ingest with live API (static Pages remains source of truth)
- Animations / chart transitions (violates motion gate)
- Hiding `unknown` or `pending` rows to improve aesthetics

---

## Owners

| Repo | Primary files |
|------|----------------|
| **lic** | `benchmarks/harness/reference.py`, `bench.py`, `results/latest.csv` |
| **benchmarks** | `scripts/ingest/build_summary.py`, `dashboard-next/`, `catalog.toml` |

---

## References

- [Numerics: fast-math DCE whitepaper](https://github.com/li-langverse/lic/blob/main/docs/numerics/benchmark-fastmath-dce-2026-05-22.md)
- [Coverage gap analysis](./coverage-gap-analysis.md)
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
