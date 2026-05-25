# Li scientific benchmark portal — design system

**WP0** specification for the next-generation [benchmarks dashboard](https://li-langverse.github.io/benchmarks/). This document is the source of truth for visual language, layout, routes, and components before Vite implementation work (WP1+).

**Learned from:** [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) pairing **Developer Tool** (dense monospace data, GitHub-dark chrome) with **Data Dashboard** (bento overview, status semantics, scan-first hierarchy). Adapted to Li org gates: proof ≠ performance ([benchmark honesty](../honesty/benchmark-dashboard.md)).

**Implementation anchor:** tokens and class names today live in [`dashboard/src/style.css`](../../dashboard/src/style.css). New routes must not change that file until WP1; align new UI to these variables.

---

## Design intent

| Axis | Choice |
|------|--------|
| Audience | Li contributors, agent preflight, numerics/HPC reviewers |
| Mood | Scientific instrument panel — not marketing site, not “AI product” chrome |
| Density | High information density; progressive disclosure on drill-down routes |
| Trust | Separate **measurement status** (green/yellow/red) from **proof coverage** (G-*, Lean) |

---

## Color & typography tokens

Dark OLED / GitHub-dark palette. Use CSS custom properties exactly as in `style.css` so static Pages and Vite builds stay consistent.

| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#0d1117` | Page background (true black-adjacent OLED) |
| `--surface` | `#161b22` | Cards, header, inputs |
| `--border` | `#30363d` | Dividers, table rules, card outlines |
| `--text` | `#e6edf3` | Primary copy |
| `--muted` | `#8b949e` | Labels, meta, tier subtitles |
| `--accent` | `#58a6ff` | Links, focus ring, selected nav |
| `--green` | `#3fb950` | Status: within `threshold_ratio_cpp` |
| `--yellow` | `#d29922` | Status: warn band (ingest policy) |
| `--red` | `#f85149` | Status: above threshold / alert |
| `--lang-*` | per language | Bar chart fills only — not brand accents |

**Typography**

- UI: `"IBM Plex Sans", system-ui, sans-serif`
- Data: `"IBM Plex Mono", monospace` for ratios, counts, benchmark ids, SHAs

**Status badges**

- `.badge.green` / `.yellow` / `.red` / `.unknown` — tinted background at ~15% opacity of status hue; never use status color as sole indicator (pair with text label).

**Surfaces**

- Row hover: `rgba(88, 166, 255, 0.06)` — subtle accent wash, not full row recolor.
- Alerts / regression: `rgba(248, 81, 73, 0.1)` border `var(--red)` (see `.alert`).

---

## Layout: bento grid overview (`/`)

The home route is a **bento grid** — irregular but aligned tiles on a 12-column logical grid, `max-width: 1400px`, `gap: 1rem`, same horizontal padding as `main` (`1.5rem 2rem`).

### Grid spec (desktop ≥1024px)

```
┌─────────────────────────────────────────────────────────────┐
│ Site header (full width): title + ingest generated_at     │
├─────────────────────────────────────────────────────────────┤
│ Honesty strip (full width, 1 row)                           │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────┤
│ Tier 0   │ Tier 1   │ Tier 2   │ Tier 3   │ Tier 5   │      │  ← tier strip (5 cols)
├────────────────────────────┬────────────────────────────────┤
│ Regression banner (8 col)  │ Package freshness (4 col)    │
├──────────────┬─────────────┴──────────────┬─────────────────┤
│ Pillar: proof│ Pillar: easy               │ Pillar: fast    │  ← pillar cards (4+4+4)
├──────────────┴────────────────────────────┴─────────────────┤
│ Category bento: micro | physics | http (2×2 chart cards)  │
├─────────────────────────────────────────────────────────────┤
│ Bench table teaser (full width, top N + link to /matrix)    │
└─────────────────────────────────────────────────────────────┘
```

| Tile | Span (12-col) | Min height | Content |
|------|---------------|------------|---------|
| Honesty strip | 12 | auto | Fixed copy: measurements ≠ proofs; link to `/proofs` |
| Tier strip | 12 (internal 5× equal) | 120px | Per-tier green/yellow/red/unknown counts |
| Regression banner | 8 | 80px | Rows that regressed vs `data/history` |
| Package freshness | 4 | 80px | lip/lit/lis publish or commit age |
| Pillar cards ×3 | 4 each | 160px | Proof / easy / fast pillar summary + deep links |
| Category bento | 12 (auto-fill `minmax(320px, 1fr)`) | chart height | Reuse `.chart-grid` / `.chart-card` patterns |
| Table teaser | 12 | 240px | Filterable subset; CTA → `/matrix` |

**Tablet (768–1023px):** tier strip wraps 2+3; pillar cards stack 6+6+12; regression + freshness stack full width.

**Mobile (&lt;768px):** single column; tier strip horizontal scroll with `scroll-snap`; no nested horizontal scroll inside charts.

---

## Sitemap & routes

Canonical paths for the SPA (or multi-page) portal. Base URL: `https://li-langverse.github.io/benchmarks/`.

| Route | Purpose | Primary data |
|-------|---------|----------------|
| `/` | Bento overview (above) | `data/latest/summary.json`, tier_counts |
| `/pillar/[id]` | Vision pillar drill-down (`proof`, `easy`, `fast`, `ai`, `hpc`) | PH-* ids, provability gaps cross-links |
| `/bench/[id]` | Single benchmark detail | catalog row + history series + honesty labels |
| `/matrix` | Full bench matrix table + filters | `summary.json` rows |
| `/history` | Time series / run index | `data/history/index.json` |
| `/proofs` | G-* / Lean coverage map (not bench green) | lic `provability-gaps.md` snapshot or ingest sidecar |
| `/packages/[pkg]` | Package freshness (`lip`, `lit`, `lis`, …) | registry + publish metadata |

**Navigation**

- Global header: logo/title, primary nav (Overview, Matrix, History, Proofs, Packages).
- Breadcrumbs on `/bench/[id]` and `/pillar/[id]`.
- External links (lic, lis, roadmap) open in new tab with visible affordance.

See also [sitemap.md](./sitemap.md) for a route-only quick reference.

### Diagram layout

Facet-first IA for per-algorithm reporting (validity, perf vs SOTA, OS, memory stub, security): **one portal diagram**, **one drill-down composition**, overview as **Algorithm × Facet** matrix. Full spec, wireframes, JSON mapping, and scale notes: **[diagram-layout.md](./diagram-layout.md)**.

---

## Components

### Tier strip

- **Role:** At-a-glance health per tier (0, 1, 2, 3, 5).
- **Markup pattern:** `.tier-strip` > `.tier-card` × N; counts use `.counts` with `.g` / `.y` / `.r` / `.u`.
- **Behavior:** Click tier → `/matrix?tier=N` (filter pre-applied).
- **Copy:** “ok / warn / fail / ?” — not “pass/fail proof”.

### Pillar cards

- **Role:** Map benchmarks to Li vision pillars (proof → easy → fast).
- **Content:** Count of catalog rows tagged with pillar PH-ids; top red/unknown ids; link to `/pillar/[id]`.
- **Visual:** Same `.chart-card` surface; optional thin left border in `--accent` (not pillar-specific rainbow).

### Regression banner

- **Role:** Highlight benchmarks whose ratio worsened vs previous ingest in `data/history`.
- **Visual:** `.alert` styling (red tint); dismissible per session only if no regression remains.
- **Copy:** “Regression vs {previous_generated_at}” with benchmark id links.

### Package freshness row

- **Role:** Show age of sibling packages (lip publish, lit, lis bench harness) relative to dashboard `generated_at`.
- **Visual:** Compact mono timestamps; yellow if &gt;7d stale, red if &gt;30d or missing.
- **Link:** `/packages/[pkg]` detail.

### Honesty strip (proof ≠ green)

- **Role:** Persistent trust label on every overview and matrix view.
- **Copy (required):** “Green rows are wall-clock ratios vs catalog reference — not formal proof or correctness certificates.”
- **Link:** `/proofs` and [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md).
- **Placement:** First content row below header on `/` and sticky subheader on `/matrix`.

### Shared primitives (existing)

| Primitive | Classes | Notes |
|-----------|---------|-------|
| Status badge | `.badge.{green,yellow,red,unknown}` | Always include text status |
| Data table | `table`, `th`, `td` | Sortable in WP1; row `data-*` filters |
| Category pills | `.category-nav`, `.cat-pill` | micro / physics / http / tooling / correctness |
| Bar charts | `.chart-grid`, `.chart-card`, `.bar-*` | Language colors from `--lang-*` only in charts |
| Filters | `.filters` | Select/input on `--surface` |

---

## WCAG 2.2 checklist

| Criterion | Requirement |
|-----------|-------------|
| **Contrast** | Body text `#e6edf3` on `#0d1117` ≥ 12:1; muted `#8b949e` on surface ≥ 4.5:1 for secondary labels only; status hues never below 4.5:1 against surface for badge text |
| **Focus** | Visible `:focus-visible` outline 2px `--accent` offset 2px on links, pills, tier cards, table rows |
| **Motion** | Respect `prefers-reduced-motion: reduce` — disable bar height transitions and hover animations |
| **Targets** | Interactive controls ≥ 44×44px touch target (tier cards, pills, filter controls) |
| **Icons** | **No emoji icons** — use text labels, SVG icons with `aria-hidden`, or mono abbreviations |
| **Tables** | `<th scope="col">`; status column includes text + badge, not color alone |
| **Live regions** | Regression banner and ingest errors use `role="alert"` |
| **Skip link** | “Skip to main content” as first focusable element |

---

## Anti-patterns

| Do not | Do instead |
|--------|------------|
| AI-style purple gradients, neon glows, glassmorphism | Flat `--surface` cards, 1px `--border`, accent only on links/focus |
| Imply proof from green bench status | Honesty strip + separate `/proofs`; cite G-* and PH-* on detail pages |
| “Proved fast”, “SOTA”, “beats C++” on green alone | “Dashboard green at ratio *r* vs cpp on commit *sha*” per honesty doc |
| Emoji tier/pillar icons (🟢🔴⚡) | Text + badge + mono counts |
| Single rainbow pillar branding | Neutral chrome; pillar identity via copy and PH-ids |
| Hide `unknown` or empty series | Show explicit “no measurement” per HTTP/nginx honesty rules |
| Conflate `li-local-ci` green with ingest | Local CI is merge gate only; label separately from dashboard data |

---

## Agent continuation (WP1+)

1. **Read:** this file, [sitemap.md](./sitemap.md), [benchmark honesty](../honesty/benchmark-dashboard.md), `dashboard/src/style.css`.
2. **Run:** `cd dashboard && npm ci && npm run build` after route/component changes.
3. **Next:** WP1 — router + `/` bento using existing tokens; wire honesty strip before matrix table.
4. **Blocked:** Do not weaken honesty copy or map proof status to bench badge colors without roadmap review.

---

## References

- Tokens: [`dashboard/src/style.css`](../../dashboard/src/style.css)
- Honesty policy: [`docs/honesty/benchmark-dashboard.md`](../honesty/benchmark-dashboard.md)
- Catalog: [`catalog.toml`](../../catalog.toml)
- Handbook: [`docs/handbook/README.md`](../handbook/README.md)
