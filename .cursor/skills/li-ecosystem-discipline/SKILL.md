---
name: li-ecosystem-discipline
description: >-
  Cross-repo Li work — vision placement, engineering gates, CVE, Learned from,
  downstream pins, agent coordination. Use for httpd/lis, lip, lit, security,
  governance, or any change touching multiple repos or pillars.
---

# Li ecosystem discipline

Use when work spans **`lic`**, **`lip`**, **`lit`**, **`lis`**, or official **`li-*`** packages.

**First:** skill **`ecosystem-first`** — pick catalog tooling; file gap issues if blocked.

## Before coding

0. [tooling-catalog.md](../../../docs/ecosystem/tooling-catalog.md) — existing scripts/skills/workflows
1. [engineering-standards.md](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md)
2. [vision-and-roadmap.md](../../../docs/ecosystem/vision-and-roadmap.md)
3. [agent-coordination.md](../../../docs/ecosystem/agent-coordination.md) — update `.li-agent-coord.json`
4. [lic master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) — current **PH-**
5. [Benchmarks dashboard](https://li-langverse.github.io/benchmarks/) — after perf work
6. [release-notes.md](../../../docs/ecosystem/release-notes.md) — before PR

## Per task checklist

- [ ] **Ecosystem-first** — used catalog tool or filed `ecosystem-gap` issue (`file-ecosystem-gap-issue.py`)
- [ ] Vision in correct doc (master plan vs roadmap proposal vs package)
- [ ] **Learned from** 2–4 references documented
- [ ] **Functionality** — tests + spec ids
- [ ] **Security** — CVE catalog / exploit TOML row for attack surface
- [ ] **Performance** — bench or N/A; check benchmarks dashboard
- [ ] **Coverage tier** — std 100% / publish 80%
- [ ] Downstream `li-toolchain.toml` if `lic` API changed
- [ ] **PR opened** — normal `git push` to feature branch (no force); do not self-merge
- [ ] **Release notes** — `docs/release-notes/YYYY-MM-DD-*.md` + CHANGELOG (`write-li-release-notes`)

## Related skills (in `lic` after sync)

- `create-li-package` — new packages
- `build-li-master-plan` — compiler phases
- `write-li-release-notes` — before every merge-worthy PR

## Do not

- Add one-off scripts/workflows without an **ecosystem-gap** issue when catalog has no fit
- Hide ecosystem vision only in a package README
- Skip CVE tests to merge faster
- Push to `main`/`dev`, **force-push**, or merge your own PR
- Edit `docs/**` / `proposals/**` without expecting human review
