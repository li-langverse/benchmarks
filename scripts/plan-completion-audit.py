#!/usr/bin/env python3
"""Audit incomplete plans vs implementation signals across li-langverse repos.

Writes data/latest/plan-completion-audit.json (benchmarks repo).

Env:
  LIC_ROOT      — path to lic checkout (default: ../lic)
  ROADMAP_ROOT  — path to roadmap (default: ../roadmap)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIC = Path(__import__("os").environ.get("LIC_ROOT", ROOT.parent / "lic"))
ROADMAP = Path(__import__("os").environ.get("ROADMAP_ROOT", ROOT.parent / "roadmap"))

UNCHECKED = re.compile(r"^- \[ \]\s+(.+)$", re.MULTILINE)
PARTIAL_GAP = re.compile(r"\|\s*\*\*G-[^|]+\*\*\s*\|[^|]+\|[^|]+\|\s*\*\*Partial\*\*", re.MULTILINE)
MISSING_GAP = re.compile(r"\|\s*\*\*G-[^|]+\*\*\s*\|[^|]+\|[^|]+\|\s*\*\*Missing\*\*", re.MULTILINE)


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def unchecked_items(text: str, source: str) -> list[dict]:
    out: list[dict] = []
    for m in UNCHECKED.finditer(text):
        item = m.group(1).strip()
        if len(item) > 240:
            item = item[:237] + "..."
        out.append({"source": source, "item": item})
    return out


def scan_master_plan() -> list[dict]:
    path = LIC / "docs/superpowers/plans/2026-05-14-li-master-plan.md"
    text = read_text(path)
    if not text:
        return [{"source": "master_plan", "item": f"missing file: {path}"}]
    items = unchecked_items(text, "lic:master_plan")
    # Phase tracker rows only (heuristic)
    return [i for i in items if i["item"].startswith("Phase ") or i["item"].startswith("**Doc-") or i["item"].startswith("**Vision-")]


def scan_provability_gaps() -> dict:
    path = LIC / "docs/verification/provability-gaps.md"
    text = read_text(path)
    if not text:
        return {"missing_file": str(path), "partial": [], "missing": []}
    partial = [m.group(0).split("|")[1].strip() for m in PARTIAL_GAP.finditer(text)]
    missing = [m.group(0).split("|")[1].strip() for m in MISSING_GAP.finditer(text)]
    return {"partial": partial, "missing": missing}


def scan_plan_dir() -> list[dict]:
    plan_dir = LIC / "docs/superpowers/plans"
    if not plan_dir.is_dir():
        return []
    out: list[dict] = []
    for path in sorted(plan_dir.glob("*.md")):
        text = read_text(path)
        if not text:
            continue
        items = unchecked_items(text, f"lic:plans/{path.name}")
        if items:
            out.extend(items[:15])  # cap per file
    return out


def scan_physics_push() -> list[dict]:
    """Known local-only publish gaps."""
    out: list[dict] = []
    push_doc = LIC / "docs/physics/PUSH_PR.md"
    if push_doc.is_file():
        out.append(
            {
                "source": "lic:physics",
                "item": "feat/physics-module-packages branch may be unpublished — see docs/physics/PUSH_PR.md",
            }
        )
    return out


def catalog_without_lic_path() -> list[dict]:
    import tomllib

    catalog = ROOT / "catalog.toml"
    if not catalog.is_file():
        return []
    data = tomllib.loads(catalog.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in data.get("benchmark", []):
        if row.get("repo") != "lic":
            continue
        rel = row.get("path", "")
        bench_path = LIC / rel
        if not bench_path.is_dir():
            out.append(
                {
                    "source": "benchmarks:catalog.toml",
                    "item": f"catalog id={row.get('id')} path missing under LIC_ROOT: {rel}",
                }
            )
    return out


def package_stubs() -> list[dict]:
    out: list[dict] = []
    packages = LIC / "packages"
    if not packages.is_dir():
        return out
    for lib in packages.glob("li-std-physics-*/src/lib.li"):
        text = read_text(lib)
        if text and "return 0" in text and text.count("\n") < 80:
            out.append(
                {
                    "source": f"lic:{lib.parent.parent.name}",
                    "item": "package lib.li looks like scaffold-only (<80 lines, version stub)",
                }
            )
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    master = scan_master_plan()
    gaps = scan_provability_gaps()
    plans = scan_plan_dir()
    catalog = catalog_without_lic_path()
    stubs = package_stubs()
    physics = scan_physics_push()

    open_items = master + plans + catalog + stubs + physics
    for g in gaps.get("partial", []):
        open_items.append({"source": "lic:provability-gaps", "item": f"Partial: {g}"})
    for g in gaps.get("missing", []):
        open_items.append({"source": "lic:provability-gaps", "item": f"Missing: {g}"})

    report = {
        "generated_at": now,
        "roots": {"lic": str(LIC), "benchmarks": str(ROOT), "roadmap": str(ROADMAP)},
        "summary": {
            "open_tracker_items": len(master),
            "open_plan_checkboxes": len(plans),
            "provability_partial": len(gaps.get("partial", [])),
            "provability_missing": len(gaps.get("missing", [])),
            "catalog_gaps": len(catalog),
            "total_findings": len(open_items),
        },
        "master_plan_open": master,
        "plan_files_open": plans[:40],
        "provability_gaps": gaps,
        "catalog_gaps": catalog,
        "implementation_signals": stubs + physics,
        "recommended_actions": [],
    }

    if master:
        report["recommended_actions"].append(
            {
                "priority": "P1",
                "action": "Close or update master plan phase tracker rows",
                "count": len(master),
            }
        )
    if gaps.get("partial") or gaps.get("missing"):
        report["recommended_actions"].append(
            {
                "priority": "P1",
                "action": "Update provability-gaps.md when closing compiler work",
                "partial": len(gaps.get("partial", [])),
                "missing": len(gaps.get("missing", [])),
            }
        )
    if catalog:
        report["recommended_actions"].append(
            {
                "priority": "P2",
                "action": "Implement lic benchmarks for catalog rows or remove catalog entry",
                "benchmarks": [c["item"] for c in catalog],
            }
        )

    out_path = ROOT / "data/latest/plan-completion-audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({report['summary']['total_findings']} findings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
