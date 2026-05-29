# Org repo onboarder digest — 2026-05-29

**Source:** proactive sweep · briefing `2026-05-29T19:05Z` · discovery refresh `2026-05-29T19:21Z` (live `gh repo list`) · CI audit `2026-05-29T19:09Z` · agent-kit audit `2026-05-29T19:20Z`

## Executive summary

- **Discovery (refreshed):** `github=34` `known=33` **`new=1`** **`stale=0`** — one net-new org repo since last preflight JSON (`2026-05-29T15:53Z`).
- **New repo:** **`proof-library`** (created `2026-05-29T19:10Z`) — Li proof corpus UI split from benchmarks; **`ci.yml` green on `main`**; Pages not live yet (404).
- **Classification:** `proof-library` → **`core_tooling`** (provability / proof visibility; pairs with `lic` proof-db, not a domain package mirror).
- **Highest onboarding risk:** new repo without agent-kit or catalog row — **do not** register in catalog until `sync_agent_kit` PR lands.
- **Existing platform risk:** `lidb` gated on non-`main` default (`feat/ph-db-2-liorm-liq`); **29** repos missing/drifted agent-kit (canonical `1.3.5+6018e18bf2ed91f4`); **8** without live docs per ecosystem metrics.
- **CI posture:** **31** repos OK on `main`, **0** missing `ci.yml`, **1** gated (`lidb`); `li-cursor-agents` excluded from org CI sweep; `proof-library` has `ci.yml` + `pages.yml` but not yet in stale CI audit snapshot.
- **Agent-kit:** **4** OK, **29** need sync (26 `missing_kit`, 3 `drift`: `lic`, `lis`, `roadmap`); `li-gui` = `missing_local_clone`.
- **North star:** `proof-library` supports **provable** pillar (G-* posture, catalog vs Lean divergence); platform hygiene before perf work.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 34 |
| Known (prior catalog / audits) | 33 |
| **New** | **1** |
| **Stale known** | **0** |

Preflight artifacts: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

> **Note:** `org_new_repos_discovery` is not embedded in `agent-briefing.json` this cycle — control plane reads `org-new-repos-discovery.json` directly. Re-run `agent-briefing.py` after merging discovery JSON so heap picks up `org_repo_onboarder`.

### New repos (classification + handoffs)

| Repo | Classification | CI | Agent-kit | Docs | Recommended handoffs |
|------|----------------|----|-----------|------|----------------------|
| **proof-library** | **core_tooling** | `ci.yml` ✅ on `main` | `missing_kit` | Pages 404 | `agent_kit_maintainer` → `sync_agent_kit`; `docs_maintainer` → `live_docs_smoke`; `code_implementer` → `register_in_catalog` (after kit) |

**Rationale:** Dedicated proof corpus UI (`data/library.json`, ingest from `lic` proof-db). Not an `official_mirror` (no `lip` package push target). Not `unclassified` domain sim/physics package.

### Stale catalog entries

*None this cycle.* No archive/delete candidates without human approval.

### Onboarding plan (existing repos — hygiene)

Downstream agents own isolated clone PRs; onboarder does **not** open PRs or edit sibling working trees.

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 29 repos (see handoff queue) | `agent_kit_maintainer` | `sync_agent_kit` | 26 `missing_kit`, 3 `drift` |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | Set default branch `main` before enforcing `ci.yml` on default |
| 10 repos | `docs_maintainer` | `live_docs_smoke` | per briefing / ecosystem metrics |
| `li-gui` | `agent_kit_maintainer` | `sync_agent_kit` | `missing_local_clone` — clone workspace before kit PR |
| `research-findings` | — | — | CI-exempt per org policy; optional kit only |

### Handoff queue (control plane)

**New-repo onboarding (`org_repo_onboarding`):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable — cursor policy before catalog |
| `docs_maintainer` | `proof-library` | `live_docs_smoke` | provable / easy — Pages handbook for proof corpus |
| `code_implementer` | `proof-library` | `register_in_catalog` | provable — known-set + explorer after CI + kit |

**Platform hygiene (existing repos):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — default-branch gate |
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | drift → canonical stamp |
| `agent_kit_maintainer` | `lis` | `sync_agent_kit` | drift |
| `agent_kit_maintainer` | `roadmap` | `sync_agent_kit` | drift |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-httpd` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-language` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-net` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-std-core` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-std-math` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | missing_kit (after WP-H0) |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `sim.scientific` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | missing_kit |
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | clone + install kit |
| `docs_maintainer` | `lic` | `live_docs_smoke` | provable / easy |
| `docs_maintainer` | `lip` | `live_docs_smoke` | platform |
| `docs_maintainer` | `lit` | `live_docs_smoke` | platform |
| `docs_maintainer` | `lis` | `live_docs_smoke` | platform |
| `docs_maintainer` | `li-demo` | `live_docs_smoke` | easy |
| `docs_maintainer` | `li-httpd` | `live_docs_smoke` | secure / web |
| `docs_maintainer` | `li-net` | `live_docs_smoke` | secure / web |
| `docs_maintainer` | `li-std-core` | `live_docs_smoke` | provable std surface |
| `docs_maintainer` | `li-std-math` | `live_docs_smoke` | PH-2i math surface |
| `docs_maintainer` | `roadmap` | `live_docs_smoke` | org vision / standards |

### Catalog sync (reference classification)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents`, **`proof-library`** |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `li-local-ci`, `lidb` |
| **unclassified** (domain packages) | `sim*`, `physics.*`, `render`, `studio`, `studio.ai`, `ui`, `world`, `mmo`, `store.realtime`, `research-findings` |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `proof-library` | chore(agent-kit): install canonical cursor rules from roadmap | `agent-kit`, `chore`, `platform` |
| `proof-library` | docs: enable GitHub Pages smoke for proof corpus UI | `docs`, `platform` |
| `benchmarks` | chore(ecosystem): add proof-library to org known-repo list | `platform`, `catalog` |
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore` |

## Deferred

- **Catalog pruning:** no stale entries.
- **`package_architect` for `proof-library`:** not required (`core_tooling` placement clear).
- **`ci_maintainer` `add_ci_yml` for `proof-library`:** skipped — `ci.yml` already green; optional `ecosystem-upstream.yml` parity later.
- **Explorer / plan_audit / ci_bug_triage:** out of onboarder scope this pass.
- **Merge program / open PR volume:** out of onboarder scope.

## Error

**Discovery script missing (non-blocking):** `python3 scripts/discover-new-org-repos.py` → `No such file or directory`. Refreshed via live `gh repo list li-langverse` and updated `data/latest/org-new-repos-discovery.json` manually. Restore `scripts/discover-new-org-repos.py` on `benchmarks` for automated preflight.
