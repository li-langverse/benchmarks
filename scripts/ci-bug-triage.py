#!/usr/bin/env python3
"""Triage CI failures and bug issues for bug_fixer / code_implementer agents.

Writes data/latest/ci-bug-triage.json with org-wide and swarm-scoped queues.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/ci-bug-triage.json"
LOCAL_CI = ROOT / "data/latest/local-ci-results.json"
ORG = "li-langverse"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from org_repos import ORG_REPOS  # noqa: E402

BUG_LABELS = {
    "bug",
    "type:bug",
    "regression",
    "ci-failure",
    "ci-fail",
    "broken-ci",
    "defect",
}

_AGENT_LABEL_TO_ID = {
    "numerics-research": "numerics_researcher",
    "autoresearch": "autoresearch",
}


_AGENT_LABELS = frozenset({"cursor-agent", "li-agent", "numerics-research", "autoresearch"})


def _is_likely_agent_pr(pr: dict) -> bool:
    """Match pr-merge-gate.py agent PR heuristics."""
    labels = {lb["name"] for lb in pr.get("labels") or []}
    if labels & _AGENT_LABELS:
        return True
    head = pr.get("headRefName") or ""
    if re.match(r"^(chore|feat|fix)\(agent", head, re.I) or head.startswith("chore/agent-"):
        return True
    body = pr.get("body") or ""
    if "<!-- li-agent -->" in body or "## Agent deliverable" in body:
        return True
    return False


def bug_fixer_swarm_only() -> bool:
    v = os.environ.get("LI_BUG_FIXER_SWARM_ONLY", "1").strip().lower()
    if v in ("0", "false", "off", "no"):
        return False
    return True


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    data = json.loads(proc.stdout)
    if isinstance(data, list):
        return data
    return data if isinstance(data, dict) else []


def fetch_pr(repo: str, number: int) -> dict | None:
    if number <= 0:
        return None
    row = gh_json(
        [
            "pr",
            "view",
            str(number),
            "--repo",
            f"{ORG}/{repo}",
            "--json",
            "number,title,url,headRefName,labels,body",
        ]
    )
    return row if isinstance(row, dict) else None


def _originating_agent_id(pr: dict, head_ref: str) -> str | None:
    head = head_ref or pr.get("headRefName") or ""
    m = re.match(r"^chore/agent-([a-z0-9_]+)-", head, re.I)
    if m:
        return m.group(1)
    m = re.match(r"^(?:chore|feat|fix)\(agent[/_-]?([^)/]+)", head, re.I)
    if m:
        return m.group(1).strip()
    if head.startswith("cursor/"):
        parts = head.split("/")
        if len(parts) > 1 and parts[1]:
            return parts[1]
    body = pr.get("body") or ""
    for pattern in (
        r"^originating_agent(?:_id)?:\s*(\S+)",
        r"^agent_id:\s*(\S+)",
        r"<!--\s*li-agent:\s*(\S+)\s*-->",
    ):
        m = re.search(pattern, body, re.M | re.I)
        if m:
            return m.group(1)
    labels = {lb["name"] for lb in pr.get("labels") or []}
    for label, agent_id in _AGENT_LABEL_TO_ID.items():
        if label in labels:
            return agent_id
    return None


def _goal_id_from_pr(pr: dict) -> str | None:
    body = pr.get("body") or ""
    m = re.search(r"^research_goal_id:\s*(\S+)", body, re.M)
    return m.group(1) if m else None


def enrich_row(row: dict, pr: dict | None) -> dict:
    out = dict(row)
    if pr:
        head_ref = pr.get("headRefName") or ""
        is_agent = _is_likely_agent_pr(pr)
        out["head_ref"] = head_ref
        out["is_agent_pr"] = is_agent
        if is_agent:
            oid = _originating_agent_id(pr, head_ref)
            if oid:
                out["originating_agent_id"] = oid
            gid = _goal_id_from_pr(pr)
            if gid:
                out["goal_id"] = gid
    else:
        out.setdefault("is_agent_pr", False)
    return out


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
        base = {
            "kind": "local_ci",
            "repo": repo,
            "number": num,
            "url": row.get("url") or f"https://github.com/{ORG}/{repo}/pull/{num}",
            "exit_code": row.get("exit_code"),
            "log_excerpt": (row.get("log_tail") or row.get("message") or "")[:500],
            "reason": "local-ci run failed",
        }
        pr = fetch_pr(repo, num) if num else None
        out.append(enrich_row(base, pr))
    return out


def bug_issues() -> list[dict]:
    rows: list[dict] = []
    for repo in ORG_REPOS:
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
            if not isinstance(issue, dict):
                continue
            labels = {lb["name"].lower() for lb in issue.get("labels") or []}
            if not labels & BUG_LABELS:
                continue
            rows.append(
                enrich_row(
                    {
                        "kind": "issue",
                        "repo": repo,
                        "number": issue["number"],
                        "url": issue["url"],
                        "title": issue["title"],
                        "labels": sorted(labels & BUG_LABELS),
                        "reason": "open issue with bug/ci label",
                    },
                    None,
                )
            )
    return rows


def gha_failing_prs() -> list[dict]:
    rows: list[dict] = []
    for repo in ORG_REPOS:
        prs = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"{ORG}/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,statusCheckRollup,headRefName,labels,body",
                "--limit",
                "15",
            ]
        )
        for pr in prs or []:
            if not isinstance(pr, dict):
                continue
            ci = classify_ci(pr.get("statusCheckRollup"))
            if ci != "fail":
                continue
            rows.append(
                enrich_row(
                    {
                        "kind": "pr_ci",
                        "repo": repo,
                        "number": pr["number"],
                        "url": pr["url"],
                        "title": pr["title"],
                        "reason": "GitHub Actions checks failing",
                    },
                    pr,
                )
            )
    return rows


def build_queues(
    local_ci: list[dict], issues: list[dict], pr_ci: list[dict]
) -> tuple[list[dict], list[dict], list[dict]]:
    org_work_queue = (local_ci + issues + pr_ci)[:40]
    swarm_work_queue = [
        r for r in org_work_queue if r.get("is_agent_pr") and r.get("kind") in ("pr_ci", "local_ci")
    ][:40]
    swarm_only = bug_fixer_swarm_only()
    if swarm_only and swarm_work_queue:
        work_queue = swarm_work_queue
    elif swarm_only:
        work_queue = org_work_queue
    else:
        work_queue = org_work_queue
    return org_work_queue, swarm_work_queue, work_queue


def main() -> int:
    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    local_ci = local_ci_failures()
    issues = bug_issues()
    pr_ci = gha_failing_prs()
    org_work_queue, swarm_work_queue, work_queue = build_queues(local_ci, issues, pr_ci)
    swarm_only = bug_fixer_swarm_only()

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "bug_fixer_swarm_only": swarm_only,
        "summary": {
            "local_ci_failures": len(local_ci),
            "bug_issues": len(issues),
            "gha_failing_prs": len(pr_ci),
            "org_work_queue_size": len(org_work_queue),
            "swarm_work_queue_size": len(swarm_work_queue),
            "work_queue_size": len(work_queue),
            "agent_prs_in_queue": sum(1 for r in org_work_queue if r.get("is_agent_pr")),
        },
        "local_ci_failures": local_ci,
        "bug_issues": issues,
        "gha_failing_prs": pr_ci,
        "org_work_queue": org_work_queue,
        "swarm_work_queue": swarm_work_queue,
        "work_queue": work_queue,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT} "
        f"(org={len(org_work_queue)} swarm={len(swarm_work_queue)} "
        f"bug_fixer_queue={len(work_queue)} swarm_only={swarm_only})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
