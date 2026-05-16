#!/usr/bin/env python3
"""Run full org PR program: merge queue plan + gate triage on all open PRs.

Writes data/latest/pr-program-run.json

Does not merge unless --execute and PR has merge-approved + gate ready.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/pr-program-run.json"
PLAN_SCRIPT = ROOT / "scripts/pr-merge-queue-plan.py"
GATE_SCRIPT = ROOT / "scripts/pr-merge-gate.py"
SWEEP_SCRIPT = ROOT / "scripts/pr-auto-merge-sweep.py"

ORG_REPOS = [
    "lic",
    "lip",
    "lit",
    "lis",
    "benchmarks",
    "roadmap",
    "li-net",
    "li-httpd",
    "li-std-core",
    "li-std-math",
    "li-demo",
    "li-language",
]

# Vision merge order (lower = earlier)
REPO_PRIORITY = {
    "li-net": 10,
    "li-httpd": 10,
    "li-std-core": 12,
    "li-std-math": 12,
    "li-demo": 12,
    "benchmarks": 20,
    "lic": 30,
    "lip": 40,
    "lit": 40,
    "lis": 45,
    "li-language": 35,
    "roadmap": 90,
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run org PR program")
    parser.add_argument("--execute", action="store_true", help="run auto-merge sweep if gates pass")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    subprocess.run([sys.executable, str(PLAN_SCRIPT)], check=False)
    plan = json.loads((ROOT / "data/latest/pr-merge-queue-plan.json").read_text(encoding="utf-8"))

    candidates: list[dict] = []
    for repo in ORG_REPOS:
        prs = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,labels,baseRefName,isDraft,statusCheckRollup",
                "--limit",
                "30",
            ]
        )
        for pr in prs or []:
            labels = {lb["name"] for lb in pr.get("labels") or []}
            ci = classify_ci(pr.get("statusCheckRollup"))
            gate = subprocess.run(
                [
                    sys.executable,
                    str(GATE_SCRIPT),
                    "--repo",
                    repo,
                    "--pr",
                    str(pr["number"]),
                    "--no-approval",
                    "--no-release-notes",
                    "--json",
                ],
                capture_output=True,
                text=True,
            )
            gate_data = json.loads(gate.stdout) if gate.stdout.strip() else {"results": []}
            gr = gate_data["results"][0] if gate_data.get("results") else {}
            has_merge_approved = "merge-approved" in labels
            priority = REPO_PRIORITY.get(repo, 50)
            if ci != "pass":
                priority += 100
            if pr.get("isDraft"):
                priority += 200
            candidates.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                    "base": pr.get("baseRefName", "main"),
                    "ci": ci,
                    "draft": bool(pr.get("isDraft")),
                    "labels": sorted(labels),
                    "merge_approved": has_merge_approved,
                    "gate_ready_with_approval": gr.get("ready", False),
                    "gate_blockers_if_approved": gr.get("blockers", []),
                    "priority_score": priority,
                }
            )

    candidates.sort(key=lambda c: (c["priority_score"], c["repo"], c["number"]))

    ci_green = [c for c in candidates if c["ci"] == "pass" and not c["draft"]]
    ready_to_merge = [c for c in candidates if c["gate_ready_with_approval"] and c["merge_approved"]]

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "merge_first": plan.get("merge_first"),
        "summary": {
            "open_prs": len(candidates),
            "ci_green": len(ci_green),
            "merge_approved": sum(1 for c in candidates if c["merge_approved"]),
            "gate_ready_labeled": len(ready_to_merge),
        },
        "recommended_merge_order": [
            {
                "rank": i + 1,
                "repo": c["repo"],
                "number": c["number"],
                "url": c["url"],
                "title": c["title"],
                "ci": c["ci"],
                "action": "add merge-approved after review"
                if c["ci"] == "pass" and not c["merge_approved"]
                else ("auto-merge ok" if c in ready_to_merge else "fix CI or review"),
            }
            for i, c in enumerate(ci_green[:20])
        ],
        "all_open": candidates,
        "plan_warnings": plan.get("warnings", [])[:15],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.execute and ready_to_merge:
        subprocess.run(
            [sys.executable, str(SWEEP_SCRIPT), "--use-plan", "--execute"],
            check=False,
        )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"wrote {OUT}")
        print(f"open={report['summary']['open_prs']} ci_green={report['summary']['ci_green']}")
        print("recommended (CI green):")
        for row in report["recommended_merge_order"][:12]:
            print(f"  {row['rank']}. {row['repo']}#{row['number']} — {row['action']}")
        if not report["summary"]["gate_ready_labeled"]:
            print("  (no PRs with merge-approved + full gate — label after review)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
