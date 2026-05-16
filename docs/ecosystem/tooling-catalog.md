# Li-langverse tooling catalog

**Ecosystem-first:** use an entry here before adding new tooling. If nothing fits, file an **[ecosystem gap](https://github.com/li-langverse/benchmarks/issues/new?template=ecosystem_gap.yml)** issue.

Maintainers: update this file when adding scripts, workflows, skills, or automations (same PR as the tooling).

---

## Philosophy & gates

| Doc / rule | Purpose |
|------------|---------|
| [ecosystem-first.md](./ecosystem-first.md) | Prefer catalog tooling; file gap issues |
| [engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md) | Mandatory gates |
| [vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) | Pillars, PH order |
| `.cursor/rules/li-ecosystem-first.mdc` | Agent rule (always on) |
| `.cursor/rules/li-ecosystem-gates.mdc` | Functionality / security / perf |

---

## Scripts (`benchmarks/scripts/` unless noted)

| Script | Use for |
|--------|---------|
| `ecosystem-audit.py` | Org PR CI, missing `ci.yml`, benchmark posture JSON |
| `issue-feature-triage.py` | Open issues needing plans |
| `plan-completion-audit.py` | Master plan / checkbox / G-* drift |
| `pr-merge-gate.py` | Merge readiness (CI, review, labels) |
| `pr-auto-merge.py` | Merge one PR when gate passes |
| `pr-auto-merge-sweep.py` | Sweep `merge-approved` PRs |
| `file-ecosystem-gap-issue.py` | File standardized gap issues |
| `post-issue-planning-comment.py` | Issue planning checklist (Actions) |
| `setup-org-labels.sh` | Create org labels (`plan-needed`, `merge-approved`, …) |
| `sync-agent-kit.sh` | Pull agent-kit from sibling `roadmap` |
| `benchmark-failures-report.sh` | Human-readable bench failures |
| `record-benchmark-history.py` | History index for dashboard |
| `render-benchmark-visuals.sh` | Visual manifest / PNG pipeline |
| `visual-manifest.py` | Visual catalog helpers |
| `regression-check.sh` | Local regression helper |
| `publish-github-pages.sh` | Pages deploy helper |
| `ingest/ingest-lic.sh` | Ingest lic CSV → summary |
| `ingest/build_summary.py` | Build `data/latest/summary.json` |

**`lic` (not duplicated here):** `./scripts/ci.sh`, `li-tests/run_all.sh`, `benchmarks/harness/bench.py`, `scripts/check-stdlib-coverage.sh`, …

**`lip` / `lit`:** `./scripts/ci.sh`, `lit test`, publish flows per repo `AGENTS.md`.

---

## GitHub Actions (`benchmarks` — critical path only)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | PR / push `main` | Ingest smoke + dashboard build |
| `pages.yml` | push `main` | GitHub Pages dashboard |
| `ingest.yml` | manual / dispatch | Ingest pipeline |
| `issue-feature-planning.yml` | issue labeled | Planning comment |
| `plan-completion-audit.yml` | `workflow_dispatch` | Plan audit artifact |
| `ecosystem-audit.yml` | `workflow_dispatch` | Audit snapshot commit |
| `pr-auto-merge.yml` | label `merge-approved` | Auto-merge when gate passes |

**No `schedule:` cron** for audits — use Cursor automations.

---

## Cursor skills (`.cursor/skills/`)

| Skill | Use when |
|-------|----------|
| `ecosystem-first` | Any task — pick catalog tool; file gap if blocked |
| `li-ecosystem-discipline` | Cross-repo / multi-pillar work |
| `plan-feature-from-issue` | Issue → vision-aligned plan |
| `audit-plan-completion` | Plan audit JSON interpretation |
| `merge-approved-pr` | Pre-merge review checklist |
| `write-li-release-notes` | Before merge-worthy PR |
| `research-li-numerics` | Physics / numerics |

Synced to other repos via **`roadmap/agent-kit`**.

---

## Cursor automations (`.cursor/automations/`)

| Prompt | Schedule (Cursor UI) |
|--------|----------------------|
| `issue-feature-planner.md` | 2×/week |
| `plan-completion-audit.md` | Weekly |
| `pr-auto-merge.md` | After review / 12h |
| `ecosystem-health.md` | Daily |
| `merge-queue-digest.md` | Daily |
| `failed-benchmarks-maintainer.md` | Weekly |
| `benchmark-visual-validation.md` | Weekly |

See [agent-automations.md](./agent-automations.md).

---

## Labels (org-wide)

| Label | Meaning |
|-------|---------|
| `plan-needed` | Needs plan (feature or gap) |
| `plan-approved` | May implement |
| `ecosystem-gap` | Missing/broken shared tooling |
| `merge-approved` | Review done; auto-merge allowed |
| `do-not-merge` | Block merge |
| `feature` | Feature planner eligible |

Created via `scripts/setup-org-labels.sh`.

---

## Agent-kit (`roadmap`)

| Path | Purpose |
|------|---------|
| `agent-kit/manifest.toml` | Version + overlays |
| `scripts/install-agent-kit.sh` | Install into target repo |
| `agent-kit/hooks/guard-*.sh` | PR-only, secrets, destructive git |

Benchmarks: `./scripts/sync-agent-kit.sh` after roadmap bumps.
