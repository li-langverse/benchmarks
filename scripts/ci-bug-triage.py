#!/usr/bin/env python3
"""Triage CI failures and bug issues for bug_fixer / code_implementer agents.

Writes data/latest/ci-bug-triage.json
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/ci-bug-triage.json"
LOCAL_CI = ROOT / "data/latest/local-ci-results.json"
ORG = "li-langverse"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from org_repos import org_repos_for_sweep  # noqa: E402

BUG_LABELS = {
    "bug",
    "type:bug",
    "regression",
    "ci-failure",
    "ci-fail",
    "broken-ci",
    "defect",
}


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    return json.loads(proc.stdout)


def classify_ci(rollup: list[dict] | None) -> str:
    if not rollup:
        return "none"
    for item in rollup:
        con = (item.get("conclusion") or "").upper()
        st = (item.get("status") or "").upper()
        if con in ("FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED"):
            return "fail"
        if st in ("QUEUED", "IN_PROGRESS", "PENDING", "WAITING"):
            return "pending"
    return "pass"


def local_ci_failures() -> list[dict]:
    if not LOCAL_CI.is_file():
        return []
    try:
        data = json.loads(LOCAL_CI.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out: list[dict] = []
    for row in data.get("runs") or []:
        if row.get("ok"):
            continue
        repo = row.get("repo", "")
        num = int(row.get("number") or 0)
        out.append(
            {
                "kind": "local_ci",
                "repo": repo,
                "number": num,
                "url": row.get("url") or f"https://github.com/{ORG}/{repo}/pull/{num}",
                "exit_code": row.get("exit_code"),
                "log_excerpt": (row.get("log_tail") or row.get("message") or "")[:500],
                "reason": "local-ci run failed",
            }
        )
    return out


def bug_issues() -> list[dict]:
    rows: list[dict] = []
    for repo in org_repos_for_sweep():
        issues = gh_json(
            [
                "issue",
                "list",
                "--repo",
                f"{ORG}/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,labels,body",
                "--limit",
                "30",
            ]
        )
        for issue in issues or []:
            labels = {lb["name"].lower() for lb in issue.get("labels") or []}
            if not labels & BUG_LABELS:
                continue
            rows.append(
                {
                    "kind": "issue",
                    "repo": repo,
                    "number": issue["number"],
                    "url": issue["url"],
                    "title": issue["title"],
                    "labels": sorted(labels & BUG_LABELS),
                    "reason": "open issue with bug/ci label",
                }
            )
    return rows


def gha_failing_prs() -> list[dict]:
    rows: list[dict] = []
    for repo in org_repos_for_sweep():
        prs = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"{ORG}/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,statusCheckRollup",
                "--limit",
                "15",
            ]
        )
        for pr in prs or []:
            ci = classify_ci(pr.get("statusCheckRollup"))
            if ci != "fail":
                continue
            rows.append(
                {
                    "kind": "pr_ci",
                    "repo": repo,
                    "number": pr["number"],
                    "url": pr["url"],
                    "title": pr["title"],
                    "reason": "GitHub Actions checks failing",
                }
            )
    return rows


def main() -> int:
    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    local_ci = local_ci_failures()
    issues = bug_issues()
    pr_ci = gha_failing_prs()
    work_queue = (local_ci + issues + pr_ci)[:40]

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "summary": {
            "local_ci_failures": len(local_ci),
            "bug_issues": len(issues),
            "gha_failing_prs": len(pr_ci),
            "work_queue_size": len(work_queue),
        },
        "local_ci_failures": local_ci,
        "bug_issues": issues,
        "gha_failing_prs": pr_ci,
        "work_queue": work_queue,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (queue={len(work_queue)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
