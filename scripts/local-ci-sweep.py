#!/usr/bin/env python3
"""Run li-local-ci on open org PRs; write data/latest/local-ci-results.json.

Used when GitHub Actions quota is exceeded — merge gate reads these results
instead of (or in addition to) statusCheckRollup.

  python3 scripts/local-ci-sweep.py
  python3 scripts/local-ci-sweep.py --repo lic --pr 14
  python3 scripts/local-ci-sweep.py --merge-candidates-only
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/local-ci-results.json"
ORG = "li-langverse"

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
    "li-cursor-agents",
]


def local_ci_bin() -> Path:
    env = os.environ.get("LI_LOCAL_CI_ROOT")
    if env:
        p = Path(env) / "bin/li-local-ci"
        if p.is_file():
            return p
    for candidate in (
        ROOT.parent / "li-local-ci" / "bin/li-local-ci",
        ROOT.parent.parent / "li-local-ci" / "bin/li-local-ci",
    ):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "li-local-ci not found — clone li-langverse/li-local-ci sibling or set LI_LOCAL_CI_ROOT"
    )


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


def run_one(bin_path: Path, repo: str, number: int) -> dict:
    proc = subprocess.run(
        [str(bin_path), "run-pr", "--repo", repo, "--pr", str(number), "--out", str(OUT)],
        cwd=bin_path.parent.parent,
        text=True,
        capture_output=False,
    )
    return {"repo": repo, "number": number, "exit_code": proc.returncode}


def load_results() -> dict:
    if not OUT.is_file():
        return {"runs": [], "generated_at": ""}
    return json.loads(OUT.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Sweep local CI for open PRs")
    parser.add_argument("--repo")
    parser.add_argument("--pr", type=int)
    parser.add_argument(
        "--merge-candidates-only",
        action="store_true",
        help="only PRs with merge-approved label and non-pass GHA CI",
    )
    parser.add_argument("--limit", type=int, default=5, help="max PRs per sweep (disk/time)")
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    try:
        bin_path = local_ci_bin()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    targets: list[tuple[str, int]] = []
    if args.repo and args.pr:
        targets = [(args.repo, args.pr)]
    else:
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
                    "number,labels,statusCheckRollup",
                    "--limit",
                    "20",
                ]
            )
            for pr in prs or []:
                labels = {lb["name"] for lb in pr.get("labels") or []}
                ci = classify_ci(pr.get("statusCheckRollup"))
                if args.merge_candidates_only:
                    if "merge-approved" not in labels:
                        continue
                    if ci == "pass":
                        continue
                elif ci == "pass":
                    continue
                targets.append((repo, int(pr["number"])))
        targets = targets[: args.limit]

    if not targets:
        print("No PRs need local CI")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"local-ci sweep: {len(targets)} PR(s) via {bin_path}")
    failed = 0
    for repo, num in targets:
        print(f"--- {repo}#{num}")
        row = run_one(bin_path, repo, num)
        if row["exit_code"] != 0:
            failed += 1

    data = load_results()
    data["sweep_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(data.get('runs', []))} run(s) on file)")

    # Refresh pr-program snapshot so agent-briefing / merge gate see local-ci ci_green
    pr_prog = ROOT / "scripts/run-pr-program.py"
    if pr_prog.is_file():
        print("==> refresh pr-program-run.json")
        subprocess.run([sys.executable, str(pr_prog)], cwd=ROOT, check=False)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
