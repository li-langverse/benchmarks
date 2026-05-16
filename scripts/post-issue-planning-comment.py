#!/usr/bin/env python3
"""Post planning checklist on new feature issues (GitHub Actions)."""
from __future__ import annotations

import json
import os
import sys
import urllib.request

PLAN_LABELS = {"feature", "enhancement", "plan-needed", "type:feature"}
SKIP_LABELS = {"plan-approved", "planned", "has-plan", "wontfix", "duplicate"}


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not event_path or not token or not repo:
        print("missing GITHUB_EVENT_PATH, token, or GITHUB_REPOSITORY", file=sys.stderr)
        return 1

    event = json.loads(open(event_path, encoding="utf-8").read())
    issue = event.get("issue") or event
    number = issue["number"]
    labels = {lbl["name"].lower() for lbl in issue.get("labels", [])}

    if labels & SKIP_LABELS:
        print("skip: already planned or closed-out")
        return 0
    if not (labels & PLAN_LABELS):
        print("skip: not a feature issue")
        return 0

    body = f"""## Feature planning (automated)

This issue is queued for **vision-aligned planning** per [li-langverse governance](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md).

### Before implementation

- [ ] Plan drafted (master plan **PH-***, package doc, or `docs/superpowers/plans/…` in **lic**)
- [ ] **Learned from** 2–4 references noted
- [ ] Tests / benchmarks / **G-*** provability gaps listed
- [ ] Label **`plan-approved`** added by a maintainer

### Agent resources

- Skill: `plan-feature-from-issue` (`.cursor/skills/` or agent-kit)
- Automation prompt: `.cursor/automations/issue-feature-planner.md`
- Cross-repo audit: `python3 scripts/plan-completion-audit.py` (benchmarks repo)

**Do not** expect implementation PRs until **`plan-approved`** is set.

<!-- li-agent-planning-v1 -->
"""

    # Skip if bot already commented
    api = f"https://api.github.com/repos/{repo}/issues/{number}/comments"
    req = urllib.request.Request(
        api,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        comments = json.loads(resp.read().decode())
    if any("li-agent-planning-v1" in (c.get("body") or "") for c in comments):
        print("skip: planning comment already exists")
        return 0

    data = json.dumps({"body": body}).encode()
    post = urllib.request.Request(
        api,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(post, timeout=30) as resp:
        print("posted", resp.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
