"""PH-5b catalog path honesty — classify gaps and propose repo/path fixes."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIC = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
LIS_VENDOR = ROOT / "vendor" / "lis-tier5"
WORKLOADS = ROOT / "benchmarks" / "workloads"

TIER_DIRS = (
    "tier0_correctness",
    "tier1_micro",
    "tier1_stdlib",
    "tier2_physics",
    "tier3_ecosystem",
)


def repo_root(repo: str) -> Path | None:
    if repo == "lic":
        return LIC if LIC.is_dir() else None
    if repo == "benchmarks":
        return ROOT
    if repo == "lis":
        if LIS_VENDOR.is_dir():
            return LIS_VENDOR
        lis = Path(os.environ.get("LIS_ROOT", ROOT.parent / "lis"))
        return lis if lis.is_dir() else None
    return None


def path_exists(repo: str, rel: str) -> bool:
    root = repo_root(repo)
    if root is None or not rel:
        return False
    p = root / rel
    return p.is_dir() or p.is_file()


def workload_mirror_path(bid: str, base_id: str | None = None) -> str | None:
    """Return benchmarks/workloads/... path when a mirror harness exists."""
    stems = [bid]
    if base_id and base_id not in stems:
        stems.append(base_id)
    for stem in stems:
        for tier in TIER_DIRS:
            if (WORKLOADS / tier / stem).is_dir():
                return f"benchmarks/workloads/{tier}/{stem}"
    return None


def vendor_tier5_path(rel: str) -> str | None:
    if not rel.startswith("benchmarks/workloads/tier5_http/scenarios/"):
        return None
    stem = rel.rstrip("/").split("/")[-1]
    candidate = f"vendor/lis-tier5/benchmarks/tier5_http/scenarios/{stem}"
    return candidate if (ROOT / candidate).is_dir() else None


def classify_row(row: dict) -> dict:
    """Classify one catalog row for PH-5b triage."""
    bid = str(row.get("id", ""))
    rel = str(row.get("path", "")).strip()
    lifecycle = str(row.get("catalog_lifecycle") or "").lower()
    repo = str(row.get("repo", "lic"))
    base_id = str(row.get("base_id") or "").strip() or None

    if lifecycle == "planned" or not rel or rel == "unknown":
        return {"id": bid, "action": "skip", "reason": "planned_or_unknown_path"}

    if path_exists(repo, rel):
        return {"id": bid, "action": "ok", "repo": repo, "path": rel}

    mirror = workload_mirror_path(bid, base_id)
    if mirror and path_exists("benchmarks", mirror):
        path_stem = rel.rstrip("/").split("/")[-1]
        if path_stem != bid and path_stem != (base_id or bid):
            return {
                "id": bid,
                "action": "fix_path",
                "reason": "bogus_vertical_remap",
                "repo": "benchmarks",
                "path": mirror,
                "was_repo": repo,
                "was_path": rel,
            }
        return {
            "id": bid,
            "action": "fix_repo",
            "reason": "benchmarks_mirror_only",
            "repo": "benchmarks",
            "path": rel if path_exists("benchmarks", rel) else mirror,
            "was_repo": repo,
            "was_path": rel,
        }

    vendor = vendor_tier5_path(rel)
    if vendor:
        return {
            "id": bid,
            "action": "fix_path",
            "reason": "lis_vendor_mirror",
            "repo": "benchmarks",
            "path": vendor,
            "was_repo": repo,
            "was_path": rel,
        }

    return {
        "id": bid,
        "action": "defer_planned",
        "reason": "no_harness_on_disk",
        "was_repo": repo,
        "was_path": rel,
    }


def triage_catalog(rows: list[dict]) -> dict:
    out: list[dict] = []
    counts: dict[str, int] = {}
    for row in rows:
        item = classify_row(row)
        out.append(item)
        counts[item["action"]] = counts.get(item["action"], 0) + 1
    actionable = [
        i
        for i in out
        if i["action"] not in ("skip", "ok", "defer_planned")
        and i["action"] in ("fix_path", "fix_repo")
    ]
    defer = [i for i in out if i["action"] == "defer_planned"]
    return {
        "summary": {
            **counts,
            "actionable_fixes": len(actionable),
            "defer_planned": len(defer),
        },
        "items": out,
        "actionable": actionable,
        "defer_planned": defer,
    }
