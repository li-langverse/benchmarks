#!/usr/bin/env python3
"""List open GitHub issues that need feature planning (org repos).

Writes data/latest/issue-feature-triage.json.

Requires: gh auth login with repo read access.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gh_util import gh_available, gh_json  # noqa: E402

# Repos that accept feature issues + planning
ORG_REPOS = [
    "lic",
    "lip",
    "lit",
    "lis",
    "benchmarks",
    "roadmap",
]

FEATURE_LABELS = {
    "feature",
    "enhancement",
    "type:feature",
    "plan-needed",
    "needs-plan",
    "ecosystem-gap",
}

PLANNED_LABELS = {
    "plan-approved",
    "planned",
    "has-plan",
}


def triage_repo(repo: str) -> dict:
    issues = gh_json(
        [
            "issue",
            "list",
            "--repo",
            f"li-langverse/{repo}",
            "--state",
            "open",
            "--json",
            "number,title,url,labels,createdAt,body",
            "--limit",
            "50",
        ],
        default=[],
    )
    if not issues:
        return {"repo": repo, "error": "no issues or gh failed", "needs_plan": [], "planned": [], "candidates": []}

    needs_plan: list[dict] = []
    planned: list[dict] = []
    candidates: list[dict] = []

    for issue in issues:
        labels = {lbl["name"].lower() for lbl in issue.get("labels", [])}
        row = {
            "number": issue["number"],
            "title": issue["title"],
            "url": issue["url"],
            "labels": sorted(labels),
            "created_at": issue.get("createdAt"),
        }
        if labels & PLANNED_LABELS:
            planned.append(row)
            continue
        if labels & FEATURE_LABELS:
            needs_plan.append(row)
            continue
        # Heuristic: title keywords without plan label
        title = issue["title"].lower()
        if any(k in title for k in ("feat", "feature", "add ", "implement", "support ")):
            candidates.append(row)

    return {
        "repo": repo,
        "needs_plan": needs_plan,
        "planned": planned,
        "candidates": candidates,
    }


def main() -> int:
    if not gh_available():
        print("gh required", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    by_repo = [triage_repo(r) for r in ORG_REPOS]
    total_needs = sum(len(r.get("needs_plan", [])) for r in by_repo)
    total_candidates = sum(len(r.get("candidates", [])) for r in by_repo)

    report = {
        "generated_at": now,
        "vision_url": "https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md",
        "skill": "plan-feature-from-issue (see .cursor/skills/)",
        "summary": {
            "repos_scanned": len(ORG_REPOS),
            "needs_plan": total_needs,
            "candidates": total_candidates,
        },
        "repos": by_repo,
        "recommended_actions": [],
    }

    if total_needs or total_candidates:
        report["recommended_actions"].append(
            {
                "priority": "P1",
                "action": "Run issue-feature-planner automation or comment planning checklist on issues",
                "needs_plan": total_needs,
                "candidates": total_candidates,
            }
        )

    out_path = ROOT / "data/latest/issue-feature-triage.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} (needs_plan={total_needs}, candidates={total_candidates})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
