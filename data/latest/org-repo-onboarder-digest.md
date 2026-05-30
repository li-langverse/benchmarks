# Org repo onboarder digest — 2026-05-30T1355Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T13:55Z` · CI audit `2026-05-30T13:47Z` · agent-kit audit `2026-05-30T13:55Z` · briefing `2026-05-30T12:07Z`

## Executive summary

- **Discovery (refreshed):** `github=35` `known=35` **`new=0`** **`stale=0`** via `gh_repo_list` — org catalog/known set matches GitHub.
- **No net-new repos** — `new_repo_entries` is empty; do not add catalog rows without CI + agent-kit path.
- **CI audit clean:** **0** repos missing `ci.yml` on default branch; **0** gated non-main; `research-findings` exempt.
- **Agent-kit gap:** **21** repos `missing_kit` (canonical `1.3.5+6018e18bf2ed91f4`); **13** OK including `li-language` (resolved since prior briefing tail).
- **Highest-risk if they appear in `new_repos` next cycle:** `lidb`, `lic-docs`, `net.httpd`, `store.realtime` — placement/CI ambiguity before catalog registration.
- **North star:** platform hygiene → **provable** (`lic`, `lit`, `proof-library`), **easy** (`lic-docs`, `studio`), **secure** (`li-httpd`, `li-net`, `lidb`).
- **Briefing gap:** `agent-briefing.json` does not embed `org_new_repos_discovery` — read `data/latest/org-new-repos-discovery.json` directly.
- **Live docs:** ecosystem audit reports **0** repos without live Pages (was 1 in compact briefing snapshot).

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (catalog + audits) | 35 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

### New repos (classification + handoffs)

*None this cycle.*

| Repo | Classification | Recommended handoffs |
|------|----------------|----------------------|
| — | — | — |

### Stale catalog entries

*None.* All 35 catalog-known repos exist on GitHub. No archive/delete without human approval.

### Catalog sync — reference classification (all 35 GitHub repos)

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents`, `li-local-ci` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `lidb`, `lic-docs` |
| **unclassified** (domain / product) | `studio`, `studio.ai`, `ui`, `render`, `sim`, `sim.*`, `physics.*`, `world`, `mmo`, `proof-library`, `store.realtime`, `research-findings` |

**Routing overrides:** `studio`, `studio.ai`, `ui`, `render`, `sim` are first-class product repos (PH-GD / PH-SIM) — treat as **core_tooling** for agent handoffs even though `classify_new_repo()` labels them `unclassified` when they appear in `new_repos`.

### Onboarding plan (existing repos — hygiene, no new-repo fan-out)

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 21 repos (`repos_needing_sync`, `missing_kit`) | `agent_kit_maintainer` | `sync_agent_kit` | canonical `1.3.5+6018e18bf2ed91f4`; see handoff queue |
| `lic-docs` | `agent_kit_maintainer` | `sync_agent_kit` | `missing_local_clone` in audit — clone then install kit |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | policy note only if default ≠ `main`; CI audit shows `main` + `ok` |
| All 35 | `org_repo_onboarder` | `refresh_discovery` | wire `org_new_repos_discovery` into `agent-briefing.py` |

Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Handoff queue (control plane)

**`org_repo_onboarding` (new repos):** *empty* — `new_repo_entries` is `[]`.

**Enqueue (platform hygiene — priority order):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure / PH-DB |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | scientific computing / PH-SIM |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | graphics / PH-GD |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | gaming / PH-GD |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure / server |
| `agent_kit_maintainer` | `li-httpd` | *(ok)* | — already synced |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — needs local clone first |
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` | PH-SIM robotics |
| `agent_kit_maintainer` | `sim.scientific` | `sync_agent_kit` | PH-SIM HPC |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` | PH-SIM domain |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` | PH-SIM domain |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` | PH-SIM domain |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` | PH-SIM physics |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` | PH-SIM physics |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` | gaming |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` | secure / realtime |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` | provable / research |
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | easy / GUI |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform / CI tooling |
| `org_repo_onboarder` | `*` | `refresh_discovery` | embed discovery in briefing each preflight |

**If `new_repos` non-empty next cycle**, per-repo fan-out:

| agent_id | action |
|----------|--------|
| `ci_maintainer` | `add_ci_yml` |
| `agent_kit_maintainer` | `sync_agent_kit` |
| `docs_maintainer` | `live_docs_smoke` |
| `package_architect` | `placement_review` (unclassified / candidate_official) |
| `code_implementer` | `register_in_catalog` (after CI + kit) |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `PH-GD` |
| `studio.ai` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `ai-first` |
| `proof-library` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `provable` |
| `lidb` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `secure` |
| `sim` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `PH-SIM` |
| `lic-docs` | chore(agent-kit): install canonical cursor rules (after clone) | `agent-kit`, `docs` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |

## Deferred

- **Catalog registration** for any repo — blocked until it appears in `new_repos` with CI + agent-kit complete.
- **Stale catalog pruning** — none identified; no archive/delete without human sign-off.
- **Bulk agent-kit wave** — remaining `missing_kit` domain mirrors after P0 platform/product repos (`sim.*`, `physics.*`, `mmo`, `store.realtime`, `research-findings`, `li-gui`, `li-local-ci`).
- **`docs_maintainer`** live Pages — ecosystem audit shows **0** gaps this cycle; no enqueue.
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
- **`package_architect` placement** — only when `new_repos` non-empty.
