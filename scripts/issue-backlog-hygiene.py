#!/usr/bin/env python3
"""Scan org GitHub issues for backlog hygiene: duplicates, stale, close candidates, routing.

Writes data/latest/issue-backlog-hygiene.json (consumed by agent-briefing.py and issue_hygiene agent).

Requires: gh auth for live scans. Use --self-test for offline CI (no gh).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/issue-backlog-hygiene.json"
ORG = "li-langverse"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from org_repos import org_repos_for_sweep  # noqa: E402

STALE_DAYS = 75
DUPLICATE_TITLE_RATIO = 0.88

PLANNED_LABELS = {"plan-approved", "planned", "has-plan"}
PLAN_NEEDED_LABELS = {"plan-needed", "needs-plan", "ecosystem-gap", "feature", "enhancement", "type:feature"}
CLOSE_HINT_LABELS = {"duplicate", "wontfix", "invalid", "stale"}
EXPLORER_LABEL = "explorer-finding"
AUTOMATION_LABELS = {"cursor-agent", "li-agent", "numerics-research", "autoresearch"}


def gh_json(args: list[str]) -> list | dict | None:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r"^(\[.*?\]|feat|fix|chore|docs)(\([^)]+\))?:\s*", "", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def title_similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return SequenceMatcher(None, na, nb).ratio()


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def issue_row(repo: str, issue: dict) -> dict:
    labels = {lbl["name"].lower() for lbl in issue.get("labels", [])}
    return {
        "repo": repo,
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["url"],
        "labels": sorted(labels),
        "created_at": issue.get("createdAt"),
        "updated_at": issue.get("updatedAt"),
        "comments": issue.get("comments", {}).get("totalCount", 0)
        if isinstance(issue.get("comments"), dict)
        else 0,
    }


def fetch_open_issues(repo: str, limit: int = 80) -> list[dict]:
    issues = gh_json(
        [
            "issue",
            "list",
            "--repo",
            f"{ORG}/{repo}",
            "--state",
            "open",
            "--json",
            "number,title,url,labels,createdAt,updatedAt,comments",
            "--limit",
            str(limit),
        ]
    )
    if not isinstance(issues, list):
        return []
    return [issue_row(repo, i) for i in issues]


def find_duplicate_clusters(rows: list[dict]) -> list[dict]:
    by_repo: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_repo[r["repo"]].append(r)

    clusters: list[dict] = []
    for repo, items in by_repo.items():
        used: set[int] = set()
        for i, a in enumerate(items):
            if a["number"] in used:
                continue
            group = [a]
            for b in items[i + 1 :]:
                if b["number"] in used:
                    continue
                sim = title_similarity(a["title"], b["title"])
                if sim >= DUPLICATE_TITLE_RATIO:
                    group.append(b)
            if len(group) >= 2:
                for g in group:
                    used.add(g["number"])
                keep = min(group, key=lambda x: x["number"])
                clusters.append(
                    {
                        "repo": repo,
                        "reason": "similar_titles",
                        "keep": {"number": keep["number"], "url": keep["url"], "title": keep["title"]},
                        "duplicates": [
                            {"number": g["number"], "url": g["url"], "title": g["title"]}
                            for g in group
                            if g["number"] != keep["number"]
                        ],
                        "action": "close_as_duplicate",
                    }
                )
    return clusters


def classify_routing(row: dict) -> str | None:
    labels = set(row["labels"])
    if labels & PLANNED_LABELS:
        return "route_implementer"
    if labels & PLAN_NEEDED_LABELS:
        return "route_planner"
    if EXPLORER_LABEL in labels and not (labels & PLANNED_LABELS):
        return "route_planner_or_merge"
    return None


def find_stale(rows: list[dict], now: datetime) -> list[dict]:
    cutoff = now - timedelta(days=STALE_DAYS)
    stale: list[dict] = []
    for r in rows:
        updated = parse_iso(r.get("updated_at")) or parse_iso(r.get("created_at"))
        if not updated or updated > cutoff:
            continue
        labels = set(r["labels"])
        if labels & PLANNED_LABELS:
            continue
        if labels & CLOSE_HINT_LABELS:
            continue
        stale.append(
            {
                **{k: r[k] for k in ("repo", "number", "title", "url", "labels")},
                "last_activity": updated.isoformat(),
                "action": "comment_stale_or_close",
            }
        )
    return stale


def find_explorer_spam(rows: list[dict]) -> list[dict]:
    explorer = [r for r in rows if EXPLORER_LABEL in r["labels"]]
    if len(explorer) < 4:
        return []
    by_repo: dict[str, list[dict]] = defaultdict(list)
    for r in explorer:
        by_repo[r["repo"]].append(r)
    spam: list[dict] = []
    for repo, items in by_repo.items():
        if len(items) < 3:
            continue
        spam.append(
            {
                "repo": repo,
                "count": len(items),
                "sample_urls": [i["url"] for i in items[:5]],
                "action": "merge_into_digest_issue",
                "reason": f"{len(items)} open explorer-finding issues — consolidate",
            }
        )
    return spam


def find_close_candidates(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for r in rows:
        labels = set(r["labels"])
        title = r["title"].lower()
        if labels & CLOSE_HINT_LABELS:
            out.append({**r, "action": "close_labeled", "reason": "already has close-type label"})
        elif re.search(r"\b(superseded|duplicate of|closed by|fixed in)\b", title):
            out.append({**r, "action": "close_or_comment", "reason": "title suggests resolved/superseded"})
        elif labels & AUTOMATION_LABELS and r.get("comments", 0) == 0:
            out.append({**r, "action": "review_agent_issue", "reason": "agent-opened with no discussion"})
    return out


def build_report(rows: list[dict], *, live: bool, repos: list[str] | None = None) -> dict:
    now = datetime.now(timezone.utc)
    duplicate_clusters = find_duplicate_clusters(rows)
    stale = find_stale(rows, now)
    explorer_spam = find_explorer_spam(rows)
    close_candidates = find_close_candidates(rows)

    route_planner: list[dict] = []
    route_implementer: list[dict] = []
    for r in rows:
        route = classify_routing(r)
        slim = {k: r[k] for k in ("repo", "number", "title", "url", "labels")}
        if route == "route_planner":
            route_planner.append(slim)
        elif route == "route_implementer":
            route_implementer.append(slim)

    dup_issue_count = sum(len(c["duplicates"]) for c in duplicate_clusters)

    sweep = repos or sorted({r["repo"] for r in rows})
    return {
        "generated_at": now.strftime("%Y-%m-%dT%H:%MZ"),
        "live_scan": live,
        "skill": "issue_hygiene agent — see .cursor/automations/issue-hygiene-agent.md",
        "repos_scanned": sweep,
        "summary": {
            "repos_in_org_sweep": len(sweep),
            "repos_with_open_issues": len({r["repo"] for r in rows}),
            "open_issues": len(rows),
            "duplicate_clusters": len(duplicate_clusters),
            "duplicate_issues": dup_issue_count,
            "stale_candidates": len(stale),
            "explorer_spam_repos": len(explorer_spam),
            "close_candidates": len(close_candidates),
            "route_planner": len(route_planner),
            "route_implementer": len(route_implementer),
        },
        "duplicate_clusters": duplicate_clusters[:30],
        "stale_candidates": stale[:40],
        "explorer_spam": explorer_spam,
        "close_candidates": close_candidates[:25],
        "route_to_issue_planner": route_planner[:25],
        "route_to_code_implementer": route_implementer[:25],
        "recommended_actions": _recommended_actions(
            duplicate_clusters, stale, explorer_spam, route_planner, route_implementer
        ),
    }


def _recommended_actions(
    duplicates: list,
    stale: list,
    explorer_spam: list,
    route_planner: list,
    route_implementer: list,
) -> list[dict]:
    actions: list[dict] = []
    if duplicates:
        actions.append(
            {
                "priority": "P0",
                "action": "Comment on duplicate issues; close pointing to keep issue",
                "count": sum(len(c["duplicates"]) for c in duplicates),
            }
        )
    if explorer_spam:
        actions.append(
            {
                "priority": "P1",
                "action": "Consolidate explorer-finding burst into one tracking issue per repo",
                "repos": [s["repo"] for s in explorer_spam],
            }
        )
    if stale:
        actions.append(
            {
                "priority": "P2",
                "action": "Stale triage: comment, label stale, or close with reason",
                "count": len(stale),
            }
        )
    if route_planner:
        actions.append(
            {
                "priority": "P1",
                "action": "Hand off to issue_planner (plan-needed / ecosystem-gap)",
                "count": len(route_planner),
            }
        )
    if route_implementer:
        actions.append(
            {
                "priority": "P1",
                "action": "Hand off to code_implementer (plan-approved)",
                "count": len(route_implementer),
            }
        )
    return actions


def run_self_test() -> int:
    """Offline assertions — no gh."""
    fixture_rows = [
        {
            "repo": "lic",
            "number": 10,
            "title": "feat(compiler): horner DCE",
            "url": "https://github.com/x/lic/issues/10",
            "labels": ["plan-needed"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "comments": 0,
        },
        {
            "repo": "lic",
            "number": 11,
            "title": "feat(compiler): horner dce",
            "url": "https://github.com/x/lic/issues/11",
            "labels": ["explorer-finding"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "comments": 0,
        },
        {
            "repo": "lic",
            "number": 12,
            "title": "PH-IO: implement foo",
            "url": "https://github.com/x/lic/issues/12",
            "labels": ["plan-approved"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "comments": 2,
        },
    ]
    report = build_report(fixture_rows, live=False, repos=["lic"])
    assert report["summary"]["duplicate_clusters"] >= 1, report
    assert report["summary"]["route_implementer"] >= 1, report
    assert report["summary"]["route_planner"] >= 1, report
    clusters = find_duplicate_clusters(fixture_rows)
    assert clusters and clusters[0]["keep"]["number"] == 10
    print("issue-backlog-hygiene self-test OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Issue backlog hygiene preflight")
    parser.add_argument("--self-test", action="store_true", help="run offline assertions")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required (or use --self-test)", file=sys.stderr)
        return 1

    repos = org_repos_for_sweep()
    rows: list[dict] = []
    for repo in repos:
        rows.extend(fetch_open_issues(repo))

    report = build_report(rows, live=True, repos=repos)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    s = report["summary"]
    print(
        f"wrote {OUT} "
        f"(sweep={s['repos_in_org_sweep']} open={s['open_issues']} "
        f"dup_clusters={s['duplicate_clusters']} stale={s['stale_candidates']} "
        f"route_planner={s['route_planner']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
