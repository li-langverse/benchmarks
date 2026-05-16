#!/usr/bin/env python3
"""Merge all org PRs labeled merge-approved that pass pr-merge-gate (dry-run by default)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "pr-merge-gate.py"
MERGE = ROOT / "scripts" / "pr-auto-merge.py"
PLAN_SCRIPT = ROOT / "scripts" / "pr-merge-queue-plan.py"
PLAN_JSON = ROOT / "data/latest/pr-merge-queue-plan.json"


def load_plan() -> dict | None:
    if not PLAN_JSON.is_file():
        return None
    return json.loads(PLAN_JSON.read_text(encoding="utf-8"))


def redundant_skip_set(plan: dict) -> set[str]:
    """PR keys (repo#num) that should not auto-merge until resolved."""
    skip: set[str] = set()
    for row in plan.get("redundant") or []:
        action = (row.get("suggested_action") or "").lower()
        if "close #" in action:
            # "close #3 after #4 merges" -> skip lower number if parseable
            m = re.search(r"close #(\d+)", action)
            if m:
                repo = row["repo"]
                skip.add(f"{repo}#{m.group(1)}")
    return skip


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="limit sweep to one repo")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--use-plan",
        action="store_true",
        help="run pr-merge-queue-plan.py; merge only merge_first; skip redundant",
    )
    parser.add_argument("--method", default="squash", choices=("squash", "merge", "rebase"))
    parser.add_argument("--allow-governance", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan: dict | None = None
    skip_redundant: set[str] = set()
    merge_first_key: str | None = None
    if args.use_plan:
        plan_proc = subprocess.run(
            [sys.executable, str(PLAN_SCRIPT)] + (["--repo", args.repo] if args.repo else []),
            capture_output=True,
            text=True,
        )
        if plan_proc.returncode != 0:
            print(plan_proc.stderr, file=sys.stderr)
            return plan_proc.returncode
        plan = load_plan()
        if plan:
            skip_redundant = redundant_skip_set(plan)
            mf = plan.get("merge_first")
            if mf:
                merge_first_key = f"{mf['repo']}#{mf['number']}"

    sweep_args = [sys.executable, str(GATE), "--sweep", "--json"]
    if args.repo:
        sweep_args.extend(["--repo", args.repo])
    proc = subprocess.run(sweep_args, capture_output=True, text=True, check=False)
    data = json.loads(proc.stdout)
    ready = data.get("ready") or []

    merged: list[dict] = []
    skipped: list[dict] = []

    for item in data.get("results") or []:
        if not item.get("ready"):
            skipped.append(item)
            continue
        key = f"{item['repo']}#{item['number']}"
        if args.use_plan and key in skip_redundant:
            skipped.append({**item, "skip_reason": "redundant per merge queue plan"})
            continue
        if args.use_plan and merge_first_key and key != merge_first_key:
            skipped.append(
                {
                    **item,
                    "skip_reason": f"not merge_first (plan says {merge_first_key} first)",
                }
            )
            continue
        merge_args = [
            sys.executable,
            str(MERGE),
            "--repo",
            item["repo"],
            "--pr",
            str(item["number"]),
            "--method",
            args.method,
        ]
        if args.execute:
            merge_args.append("--execute")
        if args.allow_governance:
            merge_args.append("--allow-governance")
        mproc = subprocess.run(merge_args, capture_output=True, text=True)
        if mproc.returncode == 0:
            merged.append(item)
        else:
            item = {**item, "merge_error": mproc.stderr.strip() or mproc.stdout.strip()}
            skipped.append(item)

    report = {
        "ready_count": len(ready),
        "merged": merged,
        "skipped": skipped,
        "merge_first": merge_first_key,
        "used_plan": bool(args.use_plan),
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"ready={len(ready)} merged={len(merged)} skipped={len(skipped)}")
        for m in merged:
            print(f"  MERGED {m['repo']}#{m['number']} {m['url']}")
        for s in skipped:
            print(f"  SKIP {s['repo']}#{s['number']}: {s.get('merge_error') or s.get('blockers')}")

    return 0 if not skipped or not args.execute else 1


if __name__ == "__main__":
    raise SystemExit(main())
