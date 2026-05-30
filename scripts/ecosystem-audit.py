#!/usr/bin/env python3
"""Audit org docs, CI on main, open PR health, and benchmark posture vs vision (PH-5b/PH-7e)."""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def list_org_repos() -> list[str]:
    """All non-archived li-langverse repos (dynamic)."""
    proc = subprocess.run(
        ["gh", "repo", "list", "li-langverse", "--limit", "100", "--json", "name,isArchived"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return [
            "lic",
            "li-language",
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
        ]
    rows = json.loads(proc.stdout)
    return sorted(r["name"] for r in rows if not r.get("isArchived"))


ORG_REPOS: list[str] = []  # filled in main()
LIVE_DOCS = {
    "benchmarks": "https://li-langverse.github.io/benchmarks/",
    "li-language": "https://li-langverse.github.io/li-language/",
}

# Org package mirrors + compiler hub — HEAD-checked each audit run
HANDBOOK_PAGES: dict[str, str] = {
    "lic": "https://li-langverse.github.io/lic/",
    "lip": "https://li-langverse.github.io/lip/",
    "lit": "https://li-langverse.github.io/lit/",
    "lis": "https://li-langverse.github.io/lis/",
    "li-net": "https://li-langverse.github.io/li-net/",
    "li-httpd": "https://li-langverse.github.io/li-httpd/",
    "li-std-core": "https://li-langverse.github.io/li-std-core/",
    "li-std-math": "https://li-langverse.github.io/li-std-math/",
    "li-demo": "https://li-langverse.github.io/li-demo/",
    "roadmap": "https://li-langverse.github.io/roadmap/development-overview/",
}
VISION = {
    "master_plan": "https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md",
    "benchmark_goal": "Li ≤1.2× cpp (tier-1/2); beat HPC SOTA everywhere — PH-5b, PH-7e pure-Li codegen",
    "package_ci": "Official mirrors need ci.yml on main before Dependabot merges",
    "merge_order": "P0 package CI PRs → benchmarks#1 → lic dev→main",
}


def gh_json(args: list[str]) -> list[dict] | dict | None:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
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


def _has_ci_on_main_graphql(repo: str) -> bool | None:
    """GraphQL fallback when REST contents API is rate-limited."""
    q = (
        "query($owner:String!,$name:String!) {"
        " repository(owner:$owner,name:$name) {"
        ' ci: object(expression:"main:.github/workflows/ci.yml") { ... on Blob { oid } }'
        ' ci2: object(expression:"main:.github/workflows/ci.yaml") { ... on Blob { oid } }'
        " } }"
    )
    proc = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={q}", "-f", "owner=li-langverse", "-f", f"name={repo}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None
    repo_node = (data.get("data") or {}).get("repository") or {}
    return bool((repo_node.get("ci") or {}).get("oid") or (repo_node.get("ci2") or {}).get("oid"))


def has_ci_on_main(repo: str) -> bool:
    proc = subprocess.run(
        [
            "gh",
            "api",
            f"repos/li-langverse/{repo}/contents/.github/workflows",
            "-q",
            ".[].name",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").lower()
        if "rate limit" in err:
            gql = _has_ci_on_main_graphql(repo)
            if gql is not None:
                return gql
        return False
    names = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return any(n.endswith(".yml") or n.endswith(".yaml") for n in names)


def head_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=12) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def load_benchmark_summary() -> dict | None:
    path = ROOT / "data/latest/summary.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def benchmark_posture(summary: dict) -> dict:
    rows = summary.get("rows", [])
    reds = [r for r in rows if r.get("status") == "red"]
    yellows = [r for r in rows if r.get("status") == "yellow"]
    greens = [r for r in rows if r.get("status") == "green"]
    near = sorted(
        [r for r in greens if r.get("ratio_vs_cpp") and r["ratio_vs_cpp"] > 1.0],
        key=lambda r: r["ratio_vs_cpp"],
        reverse=True,
    )
    return {
        "generated_at": summary.get("generated_at"),
        "red": [{"id": r["benchmark"], "ratio_vs_cpp": r.get("ratio_vs_cpp"), "ph_ids": r.get("ph_ids", [])} for r in reds],
        "yellow": [r["benchmark"] for r in yellows],
        "green_count": len(greens),
        "near_threshold": [
            {"id": r["benchmark"], "ratio_vs_cpp": r["ratio_vs_cpp"]} for r in near[:5]
        ],
        "unknown": [r["benchmark"] for r in rows if r.get("status") == "unknown"],
    }


def collect_prs() -> list[dict]:
    out: list[dict] = []
    for repo in ORG_REPOS:
        rows = gh_json(
            [
                "pr",
                "list",
                "--repo",
                f"li-langverse/{repo}",
                "--state",
                "open",
                "--json",
                "number,title,url,isDraft,statusCheckRollup,baseRefName",
                "--limit",
                "30",
            ]
        )
        if not rows:
            continue
        for pr in rows:
            ci = classify_ci(pr.get("statusCheckRollup"))
            out.append(
                {
                    "repo": repo,
                    "number": pr["number"],
                    "title": pr["title"],
                    "url": pr["url"],
                    "base": pr.get("baseRefName", "main"),
                    "ci": ci,
                    "draft": bool(pr.get("isDraft")),
                    "ready": ci == "pass" and not pr.get("isDraft"),
                }
            )
    return out


def main() -> int:
    if not subprocess.run(["which", "gh"], capture_output=True).returncode == 0:
        print("gh required", file=sys.stderr)
        return 1

    global ORG_REPOS
    ORG_REPOS = list_org_repos()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    prs = collect_prs()
    failed = [p for p in prs if p["ci"] == "fail"]
    ready = [p for p in prs if p["ready"]]

    missing_ci = [r for r in ORG_REPOS if not has_ci_on_main(r)]
    all_live_urls = {**LIVE_DOCS, **HANDBOOK_PAGES}
    missing_docs = [r for r, url in HANDBOOK_PAGES.items() if not head_ok(url)]
    live_docs_missing = [r for r, url in all_live_urls.items() if not head_ok(url)]
    live_docs_ok = [r for r, url in all_live_urls.items() if head_ok(url)]

    summary = load_benchmark_summary()
    bench = benchmark_posture(summary) if summary else {"error": "no summary.json — run ingest"}

    plan_audit_path = ROOT / "data/latest/plan-completion-audit.json"
    plan_audit: dict | None = None
    if plan_audit_path.is_file():
        try:
            plan_audit = json.loads(plan_audit_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            plan_audit = {"error": "invalid plan-completion-audit.json"}

    actions = []
    if failed:
        actions.append(
            {
                "priority": "P0",
                "action": "Fix failing PR CI before new feature work",
                "prs": [f"{p['repo']}#{p['number']}" for p in failed],
            }
        )
    if missing_ci:
        actions.append(
            {
                "priority": "P0",
                "action": "Add ci.yml on main (lic/scripts/templates/github-repo/ci.yml); run ensure-org-repo-ci.py",
                "repos": missing_ci,
            }
        )
    if bench.get("red"):
        actions.append(
            {
                "priority": "P1",
                "action": "Compiler/benchmark work in lic (not dashboards-only)",
                "benchmarks": bench["red"],
            }
        )
    if plan_audit and plan_audit.get("summary", {}).get("total_findings", 0) > 0:
        actions.append(
            {
                "priority": "P1",
                "action": "Plan completion debt — run plan-completion-audit automation",
                "total_findings": plan_audit["summary"]["total_findings"],
                "master_open": plan_audit["summary"].get("open_tracker_items"),
            }
        )
    if ready:
        actions.append(
            {
                "priority": "P2",
                "action": "Human review merge queue (do not self-merge)",
                "count": len(ready),
            }
        )

    report = {
        "generated_at": now,
        "vision": VISION,
        "metrics": {
            "open_prs": len(prs),
            "failed_prs": len(failed),
            "ready_prs": len(ready),
            "repos_missing_ci_main": len(missing_ci),
            "repos_without_live_pages": len(missing_docs),
            "repos_with_live_pages": len(live_docs_ok),
        },
        "failed_prs": failed,
        "ready_prs": ready,
        "missing_ci_on_main": missing_ci,
        "repos_without_live_docs": missing_docs,
        "live_docs_down": live_docs_missing,
        "benchmarks": bench,
        "plan_completion": plan_audit,
        "recommended_actions": actions,
    }

    out_dir = ROOT / "data/latest"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ecosystem-audit.json"
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
