#!/usr/bin/env python3
"""Verify every li-langverse repo has .github/workflows/ci.yml on default branch.

Writes data/latest/org-repo-ci-audit.json
Exit 1 if any repo missing CI (use in CI or pre-merge checks).

GitHub API success is required for non-exempt repos; local clone fallback is
opt-in (--allow-local-fallback) so repos like lidb are not false-positive OK
when the default branch lacks workflows but a sibling checkout has ci.yml.

Usage:
  python3 scripts/ensure-org-repo-ci.py
  python3 scripts/ensure-org-repo-ci.py --repo lic
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/org-repo-ci-audit.json"
ORG = "li-langverse"
REQUIRED_WORKFLOW = "ci.yml"
DEFAULT_BRANCH_MAIN = "main"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from org_repos import IGNORE_REPOS, filter_repos  # noqa: E402

EXEMPT_REPOS: set[str] = set(IGNORE_REPOS)

# Non-main default branches: gated until human WP-H0 (lidb → main).
# See li-cursor-agents docs/plans/2026-05-25-org-hygiene-multi-agent-plan.md
NON_MAIN_DEFAULT_GATES: dict[str, str] = {
    "lidb": "WP-H0: set default branch to main before requiring ci.yml on default",
}


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def list_org_repos() -> list[str]:
    rows = gh_json(["repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"])
    if not rows:
        return []
    return sorted(r["name"] for r in rows if not r.get("isArchived"))


def default_branch(repo: str) -> str | None:
    data = gh_json(["repo", "view", f"{ORG}/{repo}", "--json", "defaultBranchRef"])
    if isinstance(data, dict):
        ref = data.get("defaultBranchRef") or {}
        name = ref.get("name")
        if name:
            return name
    return None


def local_workflow_names(repo: str) -> list[str]:
    bases = [ROOT.parent / repo, ROOT / repo]
    if repo == "benchmarks":
        bases.insert(0, ROOT)
    for base in bases:
        wf = base / ".github" / "workflows"
        if wf.is_dir():
            return sorted(p.name for p in wf.iterdir() if p.suffix in (".yml", ".yaml"))
    return []


def github_workflow_names(repo: str, ref: str) -> tuple[list[str], str | None]:
    """List workflow filenames on ``ref``. Returns (names, error_message)."""
    proc = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{ORG}/{repo}/contents/.github/workflows?ref={ref}",
            "-q",
            ".[].name",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "gh api failed").strip().splitlines()
        msg = err[-1] if err else f"gh api failed (exit {proc.returncode})"
        return [], msg
    names = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return names, None


def workflow_names(
    repo: str,
    *,
    ref: str,
    allow_local_fallback: bool,
) -> tuple[list[str], str, str | None]:
    """Return (names, source, error). source is github|local|none."""
    names, err = github_workflow_names(repo, ref)
    if err is None:
        return names, "github", None
    if allow_local_fallback:
        local = local_workflow_names(repo)
        if local:
            return local, "local", err
    return [], "none", err


def has_ci(names: list[str]) -> bool:
    return REQUIRED_WORKFLOW in names or "ci.yaml" in names


def latest_check_job(repo: str) -> str | None:
    """Return primary CI job name for branch protection hints."""
    if repo in ("lic", "li-language"):
        return "build-and-test"
    if repo == "benchmarks":
        return "ingest-smoke"
    if repo == "roadmap":
        return "verify-kit"
    if repo == "lip":
        return "bootstrap"
    if repo == "lit":
        return "test"
    if repo == "lis":
        return None  # matrix jobs — ruleset uses empty or repo-specific
    return "check"


def audit_repo(
    repo: str,
    *,
    allow_local_fallback: bool,
) -> dict:
    branch = default_branch(repo)
    gate_note = NON_MAIN_DEFAULT_GATES.get(repo)
    gated_non_main = bool(
        gate_note and branch and branch != DEFAULT_BRANCH_MAIN
    )

    if branch is None:
        return {
            "repo": repo,
            "status": "audit_incomplete",
            "default_branch": None,
            "workflows": [],
            "workflow_source": "none",
            "github_error": "could not resolve default branch (gh repo view)",
            "gated": gate_note,
        }

    names, source, gh_err = workflow_names(
        repo, ref=branch, allow_local_fallback=allow_local_fallback
    )
    entry: dict = {
        "repo": repo,
        "default_branch": branch,
        "workflows": names,
        "workflow_source": source,
        "gated": gate_note if gated_non_main else None,
    }
    if gh_err:
        entry["github_error"] = gh_err

    if gated_non_main:
        entry["status"] = "gated_non_main_default"
        entry["fix"] = gate_note
        return entry

    if gh_err and source == "none":
        entry["status"] = "audit_incomplete"
        return entry

    if has_ci(names):
        entry["status"] = "ok"
        return entry

    entry["status"] = "missing_ci"
    entry["fix"] = (
        f"Add .github/workflows/{REQUIRED_WORKFLOW} on {branch} "
        "(see lic/scripts/templates/github-repo/ci.yml)"
    )
    entry["suggested_required_check"] = latest_check_job(repo)
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit org repos for ci.yml")
    parser.add_argument("--repo", action="append", dest="repos", help="limit to repo(s)")
    parser.add_argument("--json-out", type=Path, default=OUT)
    parser.add_argument(
        "--allow-local-fallback",
        action="store_true",
        help="use sibling checkout workflows when gh api fails (dev only)",
    )
    args = parser.parse_args()

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("gh required", file=sys.stderr)
        return 1

    repos = filter_repos(args.repos if args.repos else list_org_repos())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    ok: list[str] = []
    missing: list[dict] = []
    gated: list[dict] = []
    incomplete: list[dict] = []
    workflows: dict[str, list[str]] = {}
    per_repo: dict[str, dict] = {}

    for repo in repos:
        if repo in EXEMPT_REPOS:
            ok.append(repo)
            per_repo[repo] = {"repo": repo, "status": "exempt"}
            continue

        entry = audit_repo(repo, allow_local_fallback=args.allow_local_fallback)
        per_repo[repo] = entry
        names = entry.get("workflows") or []
        workflows[repo] = names
        status = entry["status"]

        if status == "ok":
            ok.append(repo)
        elif status == "gated_non_main_default":
            gated.append(entry)
        elif status == "audit_incomplete":
            incomplete.append(entry)
        else:
            missing.append(entry)

    report = {
        "generated_at": now,
        "org": ORG,
        "required_workflow": REQUIRED_WORKFLOW,
        "default_branch_policy": DEFAULT_BRANCH_MAIN,
        "repos_ok": ok,
        "repos_missing_ci": missing,
        "repos_gated_non_main_default": gated,
        "repos_audit_incomplete": incomplete,
        "workflows": workflows,
        "per_repo": per_repo,
        "policy": "docs/ecosystem/repo-ci-required.md",
        "non_main_default_gates": NON_MAIN_DEFAULT_GATES,
        "lic_monorepo_hint": "Run lic/scripts/ensure-package-ci.sh before push-official-package-repo.sh",
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json_out}")
    print(
        f"OK: {len(ok)}  missing: {len(missing)}  "
        f"gated: {len(gated)}  incomplete: {len(incomplete)}"
    )
    for g in gated:
        print(f"  GATED {g['repo']} (default={g.get('default_branch')}): {g.get('fix')}")
    for m in missing:
        print(f"  MISSING {m['repo']}: {m.get('workflows')}")
    for i in incomplete:
        print(f"  INCOMPLETE {i['repo']}: {i.get('github_error')}")
    return 1 if missing or incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
