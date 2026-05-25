# Li benchmarks dashboard — demo video script

**Target length:** 2–3 minutes (~150–180 s)  
**Public URL (after deploy):** https://li-langverse.github.io/benchmarks/  
**Design reference:** [design-system.md](./design-system.md) — scientific HPC board; **proof ≠ green**

**Deliverable:** Narration + on-screen beats only. No video file is produced by this doc.

---

## Record today in under 15 minutes

| Step | Time | Action |
|------|------|--------|
| 1 | 2 min | `./scripts/record-dashboard-demo.sh` (build + static serve + copy `data/latest` into `out/`) |
| 2 | 1 min | Open **http://127.0.0.1:4321/benchmarks/** (or dev URL below); set browser zoom **100%**, dark room, hide notifications |
| 3 | 8–10 min | One take following **beats** below; pause ≤2 s on each URL |
| 4 | 2 min | Optional trim in QuickTime or `ffmpeg` (commands printed by the script) |

**Alternate (faster preview):** `cd dashboard-next && npm run dev` → http://localhost:3000/benchmarks/ (same routes; ingest timestamp may differ from Pages).

---

## Recording guide

### Base path

All routes use Next.js `basePath: /benchmarks` and **trailing slashes**.

| Environment | Base URL |
|-------------|----------|
| Static (script) | http://127.0.0.1:**4321**/benchmarks/ |
| `npm run dev` | http://localhost:**3000**/benchmarks/ |
| GitHub Pages | https://li-langverse.github.io/benchmarks/ |

Append paths from the **Route cheat sheet** (e.g. `/bench/horner_pure_li/` → full URL `…/benchmarks/bench/horner_pure_li/`).

### Local dev (live reload)

```bash
cd dashboard-next
npm install   # first time
npm run dev
```

Open http://localhost:3000/benchmarks/ — walk the same beats as below.

### Static build (matches Pages)

```bash
./scripts/record-dashboard-demo.sh
# leaves server running; Ctrl+C when done recording
```

Ensures `out/latest/summary.json`, `release-index.json`, and `benchmark-matrix.json` are present when files exist under `data/latest/`.

### Browser capture options (macOS)

1. **QuickTime Player** — File → New Screen Recording → select window → follow beats.
2. **Cursor IDE browser** — navigate beats for a live demo without a file; not a substitute for published MP4.
3. **ffmpeg** (if installed) — script prints an `avfoundation` example; list devices with `ffmpeg -f avfoundation -list_devices true -i ""`.

### Pre-flight checklist

- [ ] `data/latest/summary.json` exists (ingest or copy from CI artifact).
- [ ] Window ≥1280×720; monospace numbers readable.
- [ ] Scroll slowly on pillar grid and matrix table.
- [ ] Say aloud once: “Green is wall-clock vs reference — not Lean proof.”

### Route cheat sheet

| Beat | Path |
|------|------|
| Overview | `/` |
| Compiler bench | `/bench/horner_pure_li/` |
| Proofs map | `/proofs/` |
| Matrix + HTTP | `/matrix/` |
| History deltas | `/history/` |
| Package (example) | `/packages/lip/` |
| Pillar (example) | `/pillar/compiler/` |
| Agent deep link | `/bench/<id>/` (see beat 9) |

---

## Narration script (beats)

Read the **Say** column; **Show** is what should be on screen. Approximate cumulative time in **T**.

### 1. Opening — overview bento + tier strip (0:00–0:25)

| T | Show | Say |
|---|------|-----|
| 0:00 | `/` — header, ingest timestamp | “This is the Li scientific benchmark portal — performance, security, and correctness across the ecosystem, not a marketing dashboard.” |
| 0:08 | Tier strip (0, 1, 2, 3, 5) | “The tier strip is a scan-first health board: green, yellow, red, and unknown counts per tier. Click a tier to jump into the matrix filtered by that tier.” |
| 0:18 | Bento layout (regression + freshness beside tiers) | “The overview is a bento grid — dense tiles, progressive detail on drill-down routes.” |

### 2. Honesty strip — proof vs performance (0:25–0:45)

| T | Show | Say |
|---|------|-----|
| 0:25 | Honesty strip on `/` | “This honesty strip is the most important label on the site: green rows are wall-clock ratios against the catalog reference — usually C++ or tier-5 nginx — not formal proof.” |
| 0:35 | Variant legend (`pure_li`, `shared_c_kernel`, …) | “Variants tell you how to interpret red. `pure_li` is Li-only codegen — red there is compiler work, PH-7e, not a missing G-star closure.” |
| 0:40 | Link to **Proof coverage map** | “Proof lives on a separate route — we’ll open `/proofs` in a minute.” |

### 3. Pillar cards (0:45–1:05)

| T | Show | Say |
|---|------|-----|
| 0:45 | Pillar grid on `/` | “Pillars group the catalog for agents and reviewers: numerics, compiler, server, physics, proofs, security, database, graphics, and tooling.” |
| 0:52 | Hover one card (e.g. **Compiler**) — counts + hotspots | “Each card shows status counts and hot benchmarks — red and unknown link straight to bench detail.” |
| 1:00 | Click **Compiler** pillar | “Pillar pages list every row in that pillar for triage.” |

*Optional quick clicks (montage, 3 s each):* `/pillar/numerics/`, `/pillar/server/`, `/pillar/security/`.

### 4. Drill-down — `horner_pure_li` compiler honesty (1:05–1:25)

| T | Show | Say |
|---|------|-----|
| 1:05 | `/bench/horner_pure_li/` | “`horner_pure_li` is the canonical pure-Li microbench — tier 1, compiler pillar.” |
| 1:12 | Status badge + **HonestyCallout** for `pure_li` | “The callout states the rule: red is compiler performance debt; green does not mean Lean verified this kernel.” |
| 1:18 | Lang table / PH ids / GitHub source link | “PH ids tie back to the master plan; source links open the harness in lic.” |
| 1:22 | History deltas section (if present) | “When history ingest runs, deltas show movement between snapshots — still measurement, not proof.” |

### 5. Proofs — G-* table (1:25–1:40)

| T | Show | Say |
|---|------|-----|
| 1:25 | `/proofs/` | “The proofs page is provability posture from lic’s gap register — G-star rows and compiler maturity colors.” |
| 1:32 | Gap register table | “These colors are not bench greens. A green bench and a stub G-star can coexist — that’s intentional honesty.” |
| 1:38 | Link to provability-gaps.md (external) | “Source of truth stays in lic; this dashboard is a snapshot for agents at preflight.” |

### 6. Matrix — catalog + HTTP oracles (1:40–1:55)

| T | Show | Say |
|---|------|-----|
| 1:40 | `/matrix/` | “The matrix is the full catalog: tier, category, repo, ratio, PH ids.” |
| 1:46 | Scroll tier-5 / **server** rows | “Tier-5 HTTP rows compare against nginx where the catalog sets `compare_oracle` — RPS oracles, not C++ microbench semantics.” |
| 1:50 | **HTTP exploit matrix** section (if rendered) | “The exploit grid is tier-5 security harness output — separate from throughput greens.” |

### 7. History — deltas (1:55–2:05)

| T | Show | Say |
|---|------|-----|
| 1:55 | `/history/` | “History indexes ingest snapshots; latest deltas highlight what moved between runs.” |
| 2:02 | Click a benchmark link in the table | “Each row links back to bench detail for context.” |

### 8. Package freshness — release-index (2:05–2:20)

| T | Show | Say |
|---|------|-----|
| 2:05 | Package freshness tile on `/` | “Freshness is publish metadata from `release-index.json` — what shipped, not what measured fast.” |
| 2:10 | `/packages/lip/` (or first indexed package) | “Package pages connect registry metadata to benchmark rows filtered by package id.” |
| 2:18 | Mention `bench_required` when shown | “Manifests can declare a release without inventing CSV rows — ingest still needs real artifacts.” |

### 9. Agent deep link + close (2:20–2:45)

| T | Show | Say |
|---|------|-----|
| 2:20 | `/bench/horner_pure_li/` or first **red** row from overview | “Agents consume `agent-briefing.json`: `benchmark_dashboard_base` plus per-red-bench URLs like this path.” |
| 2:28 | Show example URL in browser bar or paste overlay | “Example: `https://li-langverse.github.io/benchmarks/bench/horner_pure_li/` — copy into intervention prompts or PR comments.” |
| 2:35 | `/` — search box (`#search`) | “Overview search filters by id, PH id, package, or pillar client-side for quick triage.” |
| 2:40 | Honesty strip again | “Remember: measurement status and proof coverage are different channels — both belong in the workflow, never conflated.” |

---

## Post-production notes

- **Lower third (optional):** `li-langverse.github.io/benchmarks`
- **Thumbnail:** tier strip + honesty strip crop
- **Captions:** spell `horner_pure_li`, `pure_li`, `G-*`
- **Do not claim:** “proved fast”, “SOTA”, or “all green” without citing catalog variant and reference oracle

## Related docs

- [sitemap.md](./sitemap.md)
- [release-manifest.md](./release-manifest.md)
- [../honesty/benchmark-dashboard.md](../honesty/benchmark-dashboard.md)
- [demo-storyboard.html](./demo-storyboard.html) — clickable beat board for recording
