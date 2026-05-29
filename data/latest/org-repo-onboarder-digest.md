# Org repo onboarder digest — 2026-05-29

**Source:** proactive sweep · briefing `2026-05-29T12:56Z` (`5e33136ea5a928e8`) · discovery refreshed `2026-05-29T14:07Z`

## Executive summary

- **Discovery refreshed** via `scripts/discover-new-org-repos.py` → `github=33 known=33 new=0 stale=0`.
- **0 new** GitHub repos vs ecosystem known set; **0 stale** catalog entries (no archive/delete candidates).
- **33 / 33** non-archived org repos aligned between `gh repo list` and audit-derived `known_repos`.
- **No net-new onboarding handoffs** — do not add catalog rows without CI + agent-kit path.
- **Highest platform risk (existing repos):** `lidb` gated on non-`main` default (`feat/ph-db-2-liorm-liq`); **28** repos missing/drifted agent-kit (canonical `1.3.5+6018e18bf2ed91f4`); **10** without live docs.
- **CI audit degraded:** GitHub API rate limit at preflight (`12:48Z`) — **30** repos `audit_incomplete`, only `research-findings` confirmed OK; re-run `ensure-org-repo-ci.py` after limit reset before trusting missing-CI counts.
- **No unclassified *new* repos** — highest-risk bucket activates only when `new_repos` is non-empty (enqueue `package_architect` for `unclassified` / `candidate_official`).
- **Control plane:** no `queued_agent_tasks` rows for briefing `5e33136ea5a928e8`; heap still recommends `agent_kit_maintainer`, `ci_maintainer`, `docs_maintainer`.

## Deliverable / findings

### Org repo discovery (`org_new_repos_discovery`)

| Metric | Count |
|--------|------:|
| GitHub (non-archived) | 33 |
| Known (audits + core list) | 33 |
| **New** | **0** |
| **Stale known** | **0** |

Preflight artifacts: `data/latest/org-new-repos-discovery.json`, `org-repo-ci-audit.json`, `org-agent-kit-audit.json`

### New repos (classification + handoffs)

*None this cycle.*

| Repo | Classification | Recommended handoffs |
|------|----------------|----------------------|
| — | — | — |

### Stale catalog entries

*None this cycle.* No archive/delete candidates without human approval.

### Catalog sync (all GitHub repos — reference classification)

Per `classify_new_repo()` in `scripts/discover-new-org-repos.py` (applies when a repo appears in `new_repos`):

| Bucket | Repos |
|--------|-------|
| **core_tooling** | `lic`, `li-language`, `lip`, `lit`, `lis`, `benchmarks`, `roadmap`, `li-cursor-agents` |
| **official_mirror** | `li-net`, `li-httpd`, `li-std-core`, `li-std-math`, `li-demo`, `net.httpd` |
| **candidate_official** | `li-gui`, `li-local-ci`, `lidb` |
| **unclassified** (domain packages) | `sim*`, `physics.*`, `render`, `studio`, `studio.ai`, `ui`, `world`, `mmo`, `store.realtime`, `research-findings` |

### Onboarding plan (existing repos — hygiene, not “new repo”)

Downstream agents own isolated clone PRs; onboarder does **not** open PRs or edit sibling working trees.

| Repo / scope | Agent | Action | Notes |
|--------------|-------|--------|-------|
| 28 repos (see handoff queue) | `agent_kit_maintainer` | `sync_agent_kit` | 25 `missing_kit`, 3 `drift` (`lic`, `lis`, `roadmap`) |
| `lidb` | `ci_maintainer` | `wp_h0_main_default` | Set default branch `main` before enforcing `ci.yml` on default |
| 10 repos | `docs_maintainer` | `live_docs_smoke` | `lic`, `lip`, `lit`, `lis`, `li-demo`, `li-httpd`, `li-net`, `li-std-*`, `roadmap` |
| `li-gui` | `agent_kit_maintainer` | `sync_agent_kit` | `missing_local_clone` in audit — clone workspace before kit PR |
| `research-findings` | — | — | CI-exempt per org policy; optional docs/kit only |

### Handoff queue (control plane)

**New-repo onboarding (`org_repo_onboarding`):** *empty* — `new_repo_entries` is `[]`.

**Explicit rows to enqueue (onboarder recommendation — briefing `5e33136ea5a928e8`):**

| agent_id | repo | action | north_star_fit |
|----------|------|--------|----------------|
| `ci_maintainer` | `lidb` | `wp_h0_main_default` | platform / secure — default-branch gate before proof CI |
| `agent_kit_maintainer` | `lic` | `sync_agent_kit` | drift → align canonical stamp |
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
| `docs_maintainer` | `lic` | `live_docs_smoke` | provable / easy — handbook visibility |
| `docs_maintainer` | `lip` | `live_docs_smoke` | platform |
| `docs_maintainer` | `lit` | `live_docs_smoke` | platform |
| `docs_maintainer` | `lis` | `live_docs_smoke` | platform |
| `docs_maintainer` | `li-demo` | `live_docs_smoke` | easy |
| `docs_maintainer` | `li-httpd` | `live_docs_smoke` | secure / web |
| `docs_maintainer` | `li-net` | `live_docs_smoke` | secure / web |
| `docs_maintainer` | `li-std-core` | `live_docs_smoke` | provable std surface |
| `docs_maintainer` | `li-std-math` | `live_docs_smoke` | PH-2i math surface |
| `docs_maintainer` | `roadmap` | `live_docs_smoke` | org vision / standards |

**If a repo appears in `new_repos` next cycle**, enqueue per `onboarding_steps_for_repo`:

| agent_id | action |
|----------|--------|
| `ci_maintainer` | `add_ci_yml` |
| `agent_kit_maintainer` | `sync_agent_kit` |
| `docs_maintainer` | `live_docs_smoke` |
| `package_architect` | `placement_review` (if `unclassified` or `candidate_official`) |
| `code_implementer` | `register_in_catalog` (after CI + kit) |

## Recommended issues/PRs

| Repo | Title (suggested) | Labels |
|------|-------------------|--------|
| `lidb` | WP-H0: set default branch to `main` before org CI gate | `platform`, `ci` |
| `li-demo` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `li-httpd` | chore(agent-kit): sync roadmap cursor policy | `agent-kit`, `chore` |
| `studio` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore` |
| `sim` | chore(agent-kit): install canonical cursor rules | `agent-kit`, `chore` |
| `lic` | chore(agent-kit): align cursor stamp to canonical | `agent-kit`, `drift` |
| `roadmap` | docs: enable GitHub Pages / live handbook smoke | `docs`, `platform` |
| `benchmarks` | chore(ci): re-audit org workflows after gh rate-limit reset | `platform`, `ci` |

*(Open agent-kit PRs with failing CI — route to `bug_fixer` / `ci_maintainer`, not onboarder self-merge.)*

## Deferred

- **Catalog pruning:** no stale entries; no archive/delete without human sign-off.
- **New repo catalog registration:** blocked until a repo appears in `new_repos` with CI + kit path complete.
- **Org CI audit refresh:** deferred until GitHub API rate limit clears (`org-repo-ci-audit.json` mostly `audit_incomplete`).
- **Explorer / plan_audit / ci_bug_triage:** skipped in preflight (`--skip-slow`).
- **Merge program:** 95 open PRs / 35 failed CI — out of onboarder scope.

## Error

**Partial preflight — CI audit unreliable this cycle.** `ensure-org-repo-ci.py` hit GitHub API rate limit (`HTTP 403`) for 30/33 repos; `repos_missing_ci` is empty because audits did not complete, not because CI is green org-wide. Discovery and agent-kit audit (local-only) succeeded.
