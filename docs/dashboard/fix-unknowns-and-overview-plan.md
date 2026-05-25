# Fix unknowns and overview tier cards

**Date:** 2026-05-25  
**Branch:** `feat/fix-overview-tier-cards`  
**WP-O owner:** dashboard-next (`lib/overview.ts`, `app/page.tsx`, `lib/coverage.ts`)

## Problem

`summary.json` `tier_counts[*].unknown` mixes **catalog-pending** rows (no wall-clock CSV) with a small set of **validity-unresolved** measured rows. The overview tier strip read that bucket as gray **`?`**, so tiers **5** and **6** looked like “0 ok, only ?” even when tier **1–3** had dozens of green rows in the same ingest.

## Root cause (math)

| Source | Behavior |
|--------|----------|
| Ingest `build_summary.py` | Pending catalog rows increment `tier_counts[tier].unknown` |
| Dashboard (before WP-O) | UI displayed `tier_counts` verbatim → pending counted as `?` |
| `rowCoverageKind` (bug) | `status: unknown` without wall-clock fell through to `"measured"` |

**Fix:** Derive tier strip from `summary.rows` via `splitTierCounts()` in `lib/overview.ts`: **measured** = green/yellow/red only; **pending** = catalog pending or no wall-clock.

## Waves

### Wave 1 — parallel

| WP | Scope |
|----|--------|
| **WP-O** | Overview + tier strip (this PR) |
| **WP-T0** | tier0 stability ingest |
| **WP-T2** | tier2 lic builds |
| **WP-T5** | HTTP tier5 |
| **WP-DB** | lidb harness |
| **WP-TOOL** | lip/lit smoke |

### Wave 2 — sequential

Full bench run + ingest.

### Wave 3 — merge + Pages verify

## Agent continuation

1. Read this plan + `dashboard-next/lib/overview.ts`
2. Run `cd dashboard-next && npm run test:overview && npm run build`
3. Wave 2 ingest after harness CSV land
