# Org repo onboarder digest — 2026-05-30T1206Z

**Agent:** `org_repo_onboarder` · **Source:** proactive · discovery `2026-05-30T12:05Z` · CI audit `2026-05-30T12:03Z` · agent-kit audit `2026-05-30T12:04Z` · briefing `2026-05-30T12:03Z`

## Executive summary

- **Discovery (refreshed):** `github=35` `known=13` **`new=22`** **`stale=0`** via `gh_api_orgs_repos` — known set is `CORE_AGENT_KIT_REPOS` + CI/agent-kit audit entries only.
- **CI gate (progress since 10:52Z):** REST spot-check confirms **all 22 new repos have `ci.yml` on `main`**; `ci_maintainer` pass reports 0 missing. **`lidb` default branch is now `main`** — WP-H0 resolved; stale gate note in `org-repo-ci-audit.json` should be cleared on next audit.
- **Agent-kit is the primary blocker:** 14 repos **missing** kit, 7 on **drift** (`1.3.3`), 1 **ok** (`sim.scientific` @ `1.3.5+6018e18bf2ed91f4`). No catalog registration until kit sync PRs merge.
- **No stale catalog entries** — nothing in known set missing from GitHub; no archive/delete candidates without human approval.
- **Highest-risk unclassified:** `lidb` (control-plane DB), `store.realtime` (infra vs product TBD), `lic-docs` (handbook placement vs lic monorepo docs).
- **Highest-risk core (confirmed overrides):** `studio` / `studio.ai` (PH-GD, kit drift), `proof-library` (provable pillar), `net.httpd` (httpd mirror — kit missing).
- **North star:** proof-first onboarding (`proof-library`, `lidb`) → easy/ai-first (`studio`, `studio.ai`, `ui`, `lic-docs`) → domain sim mirrors — **no catalog add before CI + agent-kit green**.
- **Briefing gap:** `agent-briefing.json` still does not embed `org_new_repos_discovery` — read `data/latest/org-new-repos-discovery.json` directly.
- **Discovery script:** `scripts/discover-new-org-repos.py` was absent on branch; restored from prior digest commit and re-run successfully.

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

| Repo | Script class | **Confirmed class** | Priority | CI on `main` | Agent-kit | Recommended handoffs |
|------|--------------|---------------------|:--------:|:------------:|:---------:|----------------------|
| `lidb` | unclassified | **candidate_official** (PH-DB-0) | P0 | ✓ | missing | `agent_kit_maintainer` → `sync_agent_kit`; `package_architect` → `placement_review`; `docs_maintainer` → `live_docs_smoke`; `code_implementer` → `register_in_catalog` |
| `lic-docs` | unclassified | **candidate_official** (handbook) | P0 | ✓ | missing | kit → docs → placement → catalog |
| `net.httpd` | unclassified | **official_mirror** | P0 | ✓ | missing | kit → docs → catalog (skip placement) |
| `studio` | unclassified | **core_tooling** (PH-GD) | P0 | ✓ | drift 1.3.3 | `agent_kit_maintainer` → `sync_agent_kit`; docs → catalog |
| `studio.ai` | unclassified | **core_tooling** (ai-first) | P0 | ✓ | drift 1.3.3 | kit → docs → catalog |
| `proof-library` | unclassified | **core_tooling** (provable) | P1 | ✓ | missing | kit → docs → catalog |
| `li-local-ci` | candidate_official | **core_tooling** | P1 | ✓ | drift 1.3.3 | kit → docs → catalog |
| `sim` | unclassified | **core_tooling** (PH-SIM) | P1 | ✓ | drift 1.3.3 | kit → docs → catalog |
| `ui` | unclassified | **core_tooling** | P1 | ✓ | drift 1.3.3 | kit → docs → catalog |
| `render` | unclassified | **core_tooling** (PH-GD) | P1 | ✓ | drift 1.3.3 | kit → docs → catalog |
| `li-gui` | candidate_official | candidate_official | P2 | ✓ | missing | kit → docs → placement → catalog |
| `store.realtime` | unclassified | unclassified | P2 | ✓ | missing | kit → docs → **placement_review** → catalog |
| `sim.scientific` | unclassified | unclassified | P2 | ✓ | **ok** | docs → placement → catalog (kit done) |
| `world` | unclassified | unclassified | P3 | ✓ | drift 1.3.3 | kit → docs → placement → catalog |
| `mmo` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.robotics` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.automotive` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.drug_design` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `sim.additive` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `physics.runtime` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `physics.custom` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |
| `research-findings` | unclassified | unclassified | P3 | ✓ | missing | kit → docs → placement → catalog |

**Onboarding pipeline (all new repos):** ~~`ci_maintainer`~~ (CI done on GitHub) → **`agent_kit_maintainer`** → `docs_maintainer` → [`package_architect` if unclassified/candidate] → `code_implementer` (`register_in_catalog` only after kit green). Downstream agents own isolated-clone PRs — onboarder does **not** open PRs or edit sibling trees.

### Stale catalog entries

*None.* `stale_known_repos` is `[]`. No archive/delete without human sign-off.

### Handoff queue (control plane)

**Wave P0 — platform / PH-GD blockers (agent-kit primary)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lidb` | `sync_agent_kit` | secure / PH-DB-0 |
| `agent_kit_maintainer` | `lic-docs` | `sync_agent_kit` | easy — handbook |
| `agent_kit_maintainer` | `net.httpd` | `sync_agent_kit` | secure / web |
| `agent_kit_maintainer` | `studio` | `sync_agent_kit` | easy / PH-GD (drift 1.3.3→1.3.5) |
| `agent_kit_maintainer` | `studio.ai` | `sync_agent_kit` | ai-first / PH-GD |
| `package_architect` | `lidb` | `placement_review` | secure / PH-DB-0 |
| `package_architect` | `lic-docs` | `placement_review` | easy — lic vs standalone docs |
| `docs_maintainer` | `lic-docs` | `live_docs_smoke` | easy |
| `docs_maintainer` | `studio` | `live_docs_smoke` | PH-GD |
| `ci_maintainer` | `benchmarks` | `expand_audit_scope` | platform — add 22 repos to `org-repo-ci-audit.json` per_repo |

**Wave P1 — core product / tooling**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `proof-library` | `sync_agent_kit` | provable |
| `agent_kit_maintainer` | `li-local-ci` | `sync_agent_kit` | platform (drift) |
| `agent_kit_maintainer` | `sim` | `sync_agent_kit` | PH-SIM (drift) |
| `agent_kit_maintainer` | `ui` | `sync_agent_kit` | easy (drift) |
| `agent_kit_maintainer` | `render` | `sync_agent_kit` | PH-GD (drift) |
| `docs_maintainer` | `sim` | `live_docs_smoke` | PH-SIM |
| `docs_maintainer` | `ui` | `live_docs_smoke` | easy |

**Wave P2 — candidate / partial progress**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `li-gui` | `sync_agent_kit` | easy |
| `agent_kit_maintainer` | `store.realtime` | `sync_agent_kit` | secure / infra TBD |
| `package_architect` | `li-gui` | `placement_review` | easy |
| `package_architect` | `store.realtime` | `placement_review` | secure |
| `docs_maintainer` | `sim.scientific` | `live_docs_smoke` | PH-SIM (kit ok) |
| `code_implementer` | `sim.scientific` | `register_in_catalog` | PH-SIM — kit gate met |

**Wave P3 — domain sim / physics / research (batch after P0–P2)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `sim.robotics` | `sync_agent_kit` | robotics / PH-SIM |
| `agent_kit_maintainer` | `sim.automotive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.drug_design` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `sim.additive` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.runtime` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `physics.custom` | `sync_agent_kit` | PH-SIM |
| `agent_kit_maintainer` | `world` | `sync_agent_kit` | PH-GD (drift) |
| `agent_kit_maintainer` | `mmo` | `sync_agent_kit` | gaming |
| `agent_kit_maintainer` | `research-findings` | `sync_agent_kit` | research |
| `package_architect` | `sim.robotics` | `placement_review` | robotics |
| `package_architect` | `sim.scientific` | `placement_review` | PH-SIM |

**Deferred catalog step (21 repos — enqueue after kit PRs merge; `sim.scientific` eligible now)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `code_implementer` | `*` (21 remaining) | `register_in_catalog` | ecosystem — after agent-kit gates |

**Existing known-repo hygiene (parallel — briefing heap)**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | provable — drift `1.3.3` → `1.3.5` ([PR #379](https://github.com/li-langverse/lic/pull/379)) |
| `agent_kit_maintainer` | `li-demo` | `sync_agent_kit` | platform ([PR #15](https://github.com/li-langverse/li-demo/pull/15)) |
| `docs_maintainer` | (1 repo) | `live_docs_smoke` | easy — briefing `repos_without_live_pages` |
| `org_repo_onboarder` | `benchmarks` | `embed_discovery_in_briefing` | platform — wire `org_new_repos_discovery` into `agent-briefing.py` |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lidb` | chore(agent-kit): install roadmap agent-kit @ 1.3.5 | `agent-kit`, `platform`, `PH-DB-0` |
| `lic-docs` | chore(agent-kit): install roadmap agent-kit + docs smoke | `agent-kit`, `docs`, `easy` |
| `net.httpd` | chore(agent-kit): sync org agent-kit for httpd mirror | `agent-kit`, `secure`, `platform` |
| `studio` | chore(agent-kit): align cursor stamp 1.3.3 → 1.3.5 | `agent-kit`, `PH-GD`, `easy` |
| `studio.ai` | chore(agent-kit): align cursor stamp 1.3.3 → 1.3.5 | `agent-kit`, `ai-first`, `PH-GD` |
| `proof-library` | chore(onboard): agent-kit for proof library | `agent-kit`, `provable` |
| `sim` | chore(agent-kit): align li-sim core to canonical stamp | `agent-kit`, `PH-SIM` |
| `ui` | chore(agent-kit): sync li-ui package agent-kit | `agent-kit`, `easy` |
| `render` | chore(agent-kit): sync li-render agent-kit | `agent-kit`, `PH-GD` |
| `store.realtime` | chore(onboard): agent-kit + placement review | `agent-kit`, `platform` |
| `lic` | chore(agent-kit): merge PR #379 — 1.3.3 → 1.3.5 | `agent-kit`, `drift`, `provable` |
| `li-demo` | chore(agent-kit): merge PR #15 — first kit adoption | `agent-kit`, `platform` |
| `benchmarks` | chore(preflight): embed `org_new_repos_discovery` in agent briefing | `platform`, `agent-kit` |
| `benchmarks` | chore(org): expand `collect_known_repos()` after kit wave completes | `platform`, `agent-kit` |
| `roadmap` | chore(governance): apply branch protection to newly CI-enabled repos | `ecosystem-governance` |

## Deferred

- **`code_implementer` / `register_in_catalog`** for 21 repos — blocked until agent-kit PRs merge (except `sim.scientific`, kit ok).
- **`ci_maintainer` / `add_ci_yml`** for new repos — **done on GitHub**; next step is expanding audit scope + branch protection, not re-bootstrapping CI.
- **Stale catalog pruning** — none identified.
- **Bulk P3 sim/physics wave** — defer agent-kit fan-out until P0–P1 complete to avoid swarming domain mirrors ahead of `studio` / `lidb`.
- **`docs_maintainer` live Pages** for existing known repos — separate heap task (`repos_without_live_pages`: 1).
- **Merge program / pr_branch_opener** — out of scope (`--skip-slow` briefing).
- **GraphQL rate limit** — `gh repo list` may fail; REST `orgs/{org}/repos` used for discovery (non-blocking).

## Error

**Discovery script missing on branch (resolved):** `python3 scripts/discover-new-org-repos.py` failed with `No such file or directory`. Restored script from commit `6a3b3ae`, re-ran successfully → `github=35 known=13 new=22 stale=0`.
