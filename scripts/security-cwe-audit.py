#!/usr/bin/env python3
"""Org security posture vs CVE/CWE catalog (lic security/cve-catalog.json).

Writes data/latest/security-cwe-audit.json for security_auditor agent.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/security-cwe-audit.json"
LIC = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
_li_repo = ROOT.parent.parent / "li"
CATALOG = LIC / "security" / "cve-catalog.json"
if not CATALOG.is_file() and (_li_repo / "security" / "cve-catalog.json").is_file():
    CATALOG = _li_repo / "security" / "cve-catalog.json"
    LIC = _li_repo
LI_TESTS = LIC / "li-tests"
ORG = "li-langverse"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from org_repos import ORG_REPOS  # noqa: E402


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def load_catalog() -> list[dict]:
    if not CATALOG.is_file():
        return []
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("entries") or data.get("cves") or []
    return []


def security_tests() -> list[str]:
    manifest = LI_TESTS / "manifest.toml"
    if not manifest.is_file():
        return []
    names: list[str] = []
    for path in LI_TESTS.rglob("*.li"):
        if "security" in path.parts:
            names.append(str(path.relative_to(LIC)))
    return sorted(names)[:80]


def repo_has_security_workflow(repo: str) -> bool:
    data = gh_json(
        [
            "api",
            f"repos/{ORG}/{repo}/contents/.github/workflows",
            "--jq",
            ".[].name",
        ]
    )
    if not isinstance(data, list):
        return False
    return any("security" in str(n).lower() or "cve" in str(n).lower() for n in data)


def main() -> int:
    catalog = load_catalog()
    gaps: list[dict] = []
    for entry in catalog:
        cwe = entry.get("cwe") or entry.get("CWE") or entry.get("cwe_id")
        cve = entry.get("cve") or entry.get("id") or entry.get("cve_id")
        test_path = entry.get("li_test") or entry.get("test")
        if not test_path and cwe:
            gaps.append(
                {
                    "cwe": cwe,
                    "cve": cve,
                    "reason": "catalog row missing li-tests path",
                    "severity": entry.get("severity", "unknown"),
                }
            )

    repo_rows: list[dict] = []
    for repo in ORG_REPOS:
        has_wf = repo_has_security_workflow(repo)
        repo_rows.append(
            {
                "repo": repo,
                "security_workflow": has_wf,
                "action": None if has_wf else "add cve-catalog.yml or security gate workflow",
            }
        )

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "catalog_path": str(CATALOG) if CATALOG.is_file() else None,
        "summary": {
            "catalog_entries": len(catalog),
            "catalog_gaps": len(gaps),
            "security_test_files": len(security_tests()),
            "repos_without_security_workflow": sum(1 for r in repo_rows if not r["security_workflow"]),
        },
        "catalog_gaps": gaps[:30],
        "security_tests": security_tests(),
        "repos": repo_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (catalog={len(catalog)} gaps={len(gaps)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
