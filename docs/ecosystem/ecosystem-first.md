# Ecosystem-first (org philosophy)

Agents and humans working in **li-langverse** should **prefer existing org tooling** before inventing new scripts, workflows, or ad-hoc processes. When the ecosystem cannot do the job, **file an issue** so planner automations extend the shared toolkit — do not hide one-offs in a feature PR.

Canonical inventory: **[tooling-catalog.md](./tooling-catalog.md)**.

---

## Decision order

1. **Read** [engineering-standards.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md) and [vision-and-roadmap.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md).
2. **Search** [tooling-catalog.md](./tooling-catalog.md) for a script, skill, workflow, or automation that already solves the task.
3. **Use** the ecosystem path (same flags, same JSON outputs, same labels).
4. **If missing or broken** → `python3 scripts/file-ecosystem-gap-issue.py` (or GitHub template **Ecosystem gap**) → label **`ecosystem-gap`** + **`plan-needed`** → stop local workaround unless P0 unblock with issue linked in PR.
5. **Implement** only after **`plan-approved`** on that gap issue (or parent feature issue).

---

## Prefer (examples)

| Need | Use ecosystem |
|------|----------------|
| Org health / failing PRs | `scripts/ecosystem-audit.py` |
| Feature issue → plan | `scripts/issue-feature-triage.py` + skill `plan-feature-from-issue` |
| Stale plans / PH debt | `scripts/plan-completion-audit.py` |
| Merge after review | `scripts/pr-merge-gate.py`, label `merge-approved`, workflow `pr-auto-merge.yml` |
| Agent templates | `roadmap/agent-kit` + `./scripts/sync-agent-kit.sh` |
| Benchmark ingest | `./scripts/ingest/ingest-lic.sh`, `catalog.toml` |
| Release notes | skill `write-li-release-notes` |
| Recurring monitoring | Cursor automations in `.cursor/automations/` (not Actions cron) |

---

## Do not (without gap issue)

- Add a **new** `scripts/my-one-off.sh` in a product PR when an existing script could be extended
- Add **Actions `schedule:` cron** for audits (see [actions-budget.md](./actions-budget.md))
- Copy **agent-kit** files by hand instead of `install-agent-kit.sh` / `sync-agent-kit.sh`
- Duplicate **lic** `benchmarks/harness` into **benchmarks** repo
- Bypass **PR-only** / **merge-approved** gates
- **`git push --force`** — use [git-workflow.md](./git-workflow.md) (rebase + regular push)

---

## Ecosystem gap issues

When you hit a blocker:

```bash
python3 scripts/file-ecosystem-gap-issue.py \
  --repo benchmarks \
  --title "pr-merge-gate: support required-checks context" \
  --what-tried "Used pr-merge-gate.py on lic#4" \
  --expected "Gate reads branch protection required checks" \
  --blocked "Uses statusCheckRollup only"
```

The **issue-feature-planner** automation treats `ecosystem-gap` like other `plan-needed` work: draft a small plan to extend the catalog, then implement after `plan-approved`.

---

## Related

- [agent-automations.md](./agent-automations.md)
- [agent-coordination.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/agent-coordination.md)
- Rule **li-ecosystem-first** (`.cursor/rules/li-ecosystem-first.mdc`)
