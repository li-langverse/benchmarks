# Org repo onboarder digest — 2026-05-30T1052Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T10:52Z` · CI audit `2026-05-30T10:41Z` · agent-kit audit `2026-05-30T10:50Z` · briefing `2026-05-30T10:41Z`

## Executive summary

- **Discovery (refreshed):** `github=35` `known=13` **`new=22`** **`stale=0`** via `gh_api_orgs_repos` — known set is `CORE_AGENT_KIT_REPOS` + agent-kit audit entries only; 22 GitHub repos are not yet in briefing/catalog known set.
- **Regress vs prior cycle:** last digest (`09:35Z`) reported `known=35` / `new=0`; known-set source narrowed — treat all 22 as net-new for onboarding fan-out.
- **No stale catalog entries** — nothing in known set missing from GitHub; no archive/delete candidates without human approval.
- **Highest-risk repos:** `lidb` (WP-H0: non-`main` default before CI gate), `lic-docs` + `net.httpd` (placement/CI ambiguity), `store.realtime` (unclear product vs infra), `studio` / `studio.ai` (PH-GD core — must not stall behind experimental sim repos).
- **Classification split:** 2 `candidate_official` (`li-gui`, `li-local-ci`), 20 `unclassified` by script — **7 routing overrides** to `core_tooling` / `official_mirror` for product/platform repos (see table below).
- **Platform hygiene (existing 13 known):** 9 repos missing/drifted agent-kit in briefing heap; CI audit lists `lidb` under `non_main_default_gates` only — no `repos_missing_ci` rows yet (new repos not audited locally).
- **North star:** onboard **provable** first (`proof-library`, `lic-docs`), then **easy/ai-first** (`studio`, `studio.ai`, `ui`), then domain sim mirrors — no catalog registration before CI + agent-kit.
- **Briefing gap:** `agent-briefing.json` still does not embed `org_new_repos_discovery` — read `data/latest/org-new-repos-discovery.json` directly.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 35 |
| Known (catalog + audits) | 13 |
| **New** | **22** |
| **Stale known** | **0** |

Preflight: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

**Known set (13):** `benchmarks`, `li-cursor-agents`, `li-demo`, `li-httpd`, `li-language`, `li-net`, `li-std-core`, `li-std-math`, `lic`, `lip`, `lis`, `lit`, `roadmap`

### New repos (classification + handoffs)

| Repo | Script class | **Confirmed class** | Priority | Recommended handoffs |
|------|--------------|---------------------|:--------:|----------------------|
| `lidb` | unclassified | **candidate_official** | P0 | `ci_maintainer` → `wp_h0_main_default` then `add_ci_yml`; `agent_kit_maintainer` → `sync_agent_kit`; `package_architect` → `placement_review`; `docs_maintainer` → `live_docs_smoke`; `code_implementer` → `register_in_catalog` (after gates) |
| `lic-docs` | unclassified | **candidate_official** | P0 | CI → kit → docs → placement → catalog |
| `net.httpd` | unclassified | **official_mirror** | P0 | CI → kit → docs → catalog (skip placement — mirror of lic httpd / `lis` pattern) |
| `studio` | unclassified | **core_tooling** (PH-GD) | P0 | CI → kit → docs → catalog |
| `studio.ai` | unclassified | **core_tooling** (ai-first) | P0 | CI → kit → docs → catalog |
| `li-local-ci` | candidate_official | **core_tooling** | P1 | CI → kit → docs → catalog |
| `proof-library` | unclassified | **core_tooling** (provable) | P1 | CI → kit → docs → catalog |
| `sim` | unclassified | **core_tooling** (PH-SIM) | P1 | CI → kit → docs → catalog |
| `ui` | unclassified | **core_tooling** | P1 | CI → kit → docs → catalog |
| `render` | unclassified | **core_tooling** (PH-GD) | P1 | CI → kit → docs → catalog |
| `li-gui` | candidate_official | candidate_official | P2 | CI → kit → docs → `package_architect` → catalog |
| `store.realtime` | unclassified | unclassified | P2 | CI → kit → docs → **placement_review** → catalog |
| `research-findings` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `world` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `mmo` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `sim.scientific` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `sim.robotics` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `sim.automotive` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `sim.drug_design` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `sim.additive` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `physics.runtime` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |
| `physics.custom` | unclassified | unclassified | P3 | CI → kit → docs → placement → catalog |

**Onboarding pipeline (all new repos):** `ci_maintainer` → `agent_kit_maintainer` → `docs_maintainer` → [`package_architect` if unclassified/candidate] → `code_implementer` (`register_in_catalog` only after CI + kit green). Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Stale catalog entries

*None.* `stale_known_repos` is `[]`. No archive/delete without human sign-off.

### Handoff queue (control plane)

**Wave P0 — placement / platform blockers**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — PH-DB-0 default branch |
| `ci_maintainer` | `lidb` | `add_ci_yml` | platform / secure (after WP-H0) |
| `ci_maintainer` | `lic-docs` | `add_ci_yml` | easy — handbook CI gate |
| `ci_maintainer` | `net.httpd` | `add_ci_yml` | secure / web — httpd mirror |
| `ci_maintainer` | `studio` | `add_ci_yml` | easy / PH-GD |
| `ci_maintainer` | `studio.ai` | `add_ci_yml` | ai-first / PH-GD |
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first |
| `package_architect` | `lidb` | `placement_review` | secure / PH-DB-0 |
| `package_architect` | `lic-docs` | `placement_review` | easy — lic vs standalone docs |
| `docs_maintainer` | `lic-docs` | `live_docs_smoke` | easy |
| `docs_maintainer` | `studio` | `live_docs_smoke` | PH-GD |

**Wave P1 — core product / tooling**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `li-local-ci` | `add_ci_yml` | platform |
| `ci_maintainer` | `proof-library` | `add_ci_yml` | provable |
| `ci_maintainer` | `sim` | `add_ci_yml` | scientific computing / PH-SIM |
| `ci_maintainer` | `ui` | `add_ci_yml` | easy |
| `ci_maintainer` | `render` | `add_ci_yml` | PH-GD / graphics |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform |
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | PH-GD |
| `docs_maintainer` | `sim` | `live_docs_smoke` | PH-SIM |
| `docs_maintainer` | `ui` | `live_docs_smoke` | easy |

**Wave P2 — candidate / ambiguous**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `li-gui` | `add_ci_yml` | easy |
| `ci_maintainer` | `store.realtime` | `add_ci_yml` | secure / infra TBD |
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` | secure |
| `package_architect` | `li-gui` | `placement_review` | easy |
| `package_architect` | `store.realtime` | `placement_review` | secure |

**Wave P3 — domain sim / physics / research (batch after P0–P2)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `sim.scientific` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `sim.robotics` | `add_ci_yml` | robotics / PH-SIM |
| `ci_maintainer` | `sim.automotive` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `sim.drug_design` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `sim.additive` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `physics.runtime` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `physics.custom` | `add_ci_yml` | PH-SIM |
| `ci_maintainer` | `world` | `add_ci_yml` | gaming / PH-GD |
| `ci_maintainer` | `mmo` | `add_ci_yml` | gaming |
| `ci_maintainer` | `research-findings` | `add_ci_yml` | research |
| `agent_kit_maintainer` | `sim.scientific` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` | robotics |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | PH-GD |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` | gaming |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` | research |
| `package_architect` | `sim.scientific` | `placement_review` | PH-SIM |
| `package_architect` | `sim.robotics` | `placement_review` | robotics |
| `package_architect` | `store.realtime` | `placement_review` | secure (if not done in P2) |

**Deferred catalog step (all 22 — enqueue only after CI + kit PRs merge)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `code_implementer` | `*` (22 repos) | `register_in_catalog` | ecosystem — after CI + agent-kit gates |

**Existing known-repo hygiene (parallel — briefing heap)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | provable — drift `1.3.3` → `1.3.5` |
| `agent_kit_maintainer` | `lis` | `sync_agent_kit` | provable — drift |
| `agent_kit_maintainer` | `roadmap` | `sync_agent_kit` | governance — drift |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | platform templates |
| `agent_kit_maintainer` | `li-httpd` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `li-language` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `li-net` | `sync_agent_kit` | secure |
| `agent_kit_maintainer` | `li-std-core` | `sync_agent_kit` | provable / std |
| `agent_kit_maintainer` | `li-std-math` | `sync_agent_kit` | provable / PH-2i |
| `docs_maintainer` | (10 repos) | `live_docs_smoke` | easy — briefing `repos_without_live_pages` |
| `org_repo_onboarder` | `*` | `refresh_discovery` | embed `org_new_repos_discovery` in briefing |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci`, `PH-DB-0` |
| `lidb` | chore(ci): add required `ci.yml` for org CI policy | `platform`, `ci` |
| `lic-docs` | chore(ci): add required `ci.yml` for org CI policy | `platform`, `ci`, `docs` |
| `net.httpd` | chore(onboard): bootstrap org CI + agent-kit for httpd mirror | `platform`, `ci`, `secure` |
| `studio` | chore(onboard): CI + agent-kit for World Studio shell | `agent-kit`, `PH-GD`, `platform` |
| `studio.ai` | chore(onboard): CI + agent-kit for studio AI integration | `agent-kit`, `ai-first`, `PH-GD` |
| `li-local-ci` | chore(onboard): CI + agent-kit for local CI tooling | `platform`, `ci`, `agent-kit` |
| `proof-library` | chore(onboard): CI + agent-kit for proof library | `agent-kit`, `provable` |
| `sim` | chore(onboard): CI + agent-kit for li-sim core | `agent-kit`, `PH-SIM` |
| `ui` | chore(onboard): CI + agent-kit for li-ui package | `agent-kit`, `easy` |
| `render` | chore(onboard): CI + agent-kit for li-render | `agent-kit`, `PH-GD` |
| `lic` | chore(agent-kit): align cursor stamp to canonical `1.3.5` | `agent-kit`, `drift`, `provable` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |
| `benchmarks` | chore(org): expand `collect_known_repos()` to include explorer catalog | `platform`, `agent-kit` |

## Deferred

- **`code_implementer` / `register_in_catalog`** for all 22 new repos — blocked until CI + agent-kit PRs merge on each repo.
- **Stale catalog pruning** — none identified.
- **Bulk P3 sim/physics wave** — defer until P0–P2 complete to avoid swarming domain mirrors ahead of `studio` / `lidb`.
- **`docs_maintainer` live Pages** for existing 10 repos — separate heap task; not onboarder-owned.
- **CI re-audit of all 35 repos** — `org-repo-ci-audit.json` has empty `per_repo` (new repos not locally cloned in audit scope); run full audit after first onboarding PRs land.
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
