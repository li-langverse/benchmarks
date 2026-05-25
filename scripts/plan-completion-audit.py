#!/usr/bin/env python3
"""Audit incomplete plans vs implementation signals across li-langverse repos.

Writes data/latest/plan-completion-audit.json (benchmarks repo).

Env:
  LIC_ROOT      — path to lic checkout (default: ../lic; CI: ${{ github.workspace }}/lic)
  LIS_ROOT      — path to lis checkout (default: ../lis; tier-5 uses vendor/lis-tier5 when present)
  ROADMAP_ROOT  — path to roadmap (default: ../roadmap)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_OS = __import__("os")
LIC = Path(_OS.environ.get("LIC_ROOT", ROOT.parent / "lic"))
LIS = Path(_OS.environ.get("LIS_ROOT", ROOT.parent / "lis"))
ROADMAP = Path(_OS.environ.get("ROADMAP_ROOT", ROOT.parent / "roadmap"))

UNCHECKED = re.compile(r"^- \[ \]\s+(.+)$", re.MULTILINE)
TRACKER_LINE = re.compile(r"^- \[(x| )\] (.+)$", re.MULTILINE)
PARTIAL_GAP = re.compile(r"\|\s*\*\*G-[^|]+\*\*\s*\|[^|]+\|[^|]+\|\s*\*\*Partial\*\*", re.MULTILINE)
MISSING_GAP = re.compile(r"\|\s*\*\*G-[^|]+\*\*\s*\|[^|]+\|[^|]+\|\s*\*\*Missing\*\*", re.MULTILINE)

TRACKER_MARKER = "## Phase completion tracker"
TRACKER_END_MARKERS = ("\n**Dashboards", "\n## v1 compiler")
MASTER_PLAN_NAME = "2026-05-14-li-master-plan.md"

# Sub-plan filename → tracker phase id(s) that must all be [x] to suppress stale `- [ ]` rows.
PLAN_FILE_COVERED_PHASES: dict[str, list[str]] = {
    "2026-05-14-phase-00-bootstrap.md": ["0"],
    "2026-05-14-phase-01-lexer-parser.md": ["1"],
    "2026-05-14-phase-02-typechecker.md": ["2a", "2b", "2c", "2d"],
    "2026-05-14-phase-03-mir-codegen.md": ["3"],
    "2026-05-14-phase-04-runtime-stdlib.md": ["4"],
    "2026-05-14-phase-05-tetris.md": ["5"],
    "2026-05-14-benchmarks-and-simulations.md": ["5b"],
}

# Implementation task lists kept for history; only exit-gate boxes are actionable when phases are done.
STALE_SPEC_IMPLEMENTATION_PLANS = frozenset({"2026-05-14-phase-02-typechecker.md"})
EXIT_GATE_HEADING = re.compile(r"^#{2,3} Phase .*exit gate", re.IGNORECASE | re.MULTILINE)


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_item_key(item: str) -> str:
    return re.sub(r"\s+", " ", item.strip().lower())[:120]


def unchecked_items(text: str, source: str) -> list[dict]:
    out: list[dict] = []
    for m in UNCHECKED.finditer(text):
        item = m.group(1).strip()
        if len(item) > 240:
            item = item[:237] + "..."
        out.append({"source": source, "item": item})
    return out


def extract_tracker_phase_id(line: str) -> str | None:
    if line.startswith("**Vision-LLM**"):
        return "Vision-LLM"
    m = re.match(r"^Phase\s+([0-9]+[a-z]?|Doc-[a-z]|8[a-z-]+|Pkg|H)\b", line, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def parse_phase_tracker(master_text: str) -> tuple[set[str], list[dict]]:
    """Return (completed_phase_ids, open_tracker_rows)."""
    idx = master_text.find(TRACKER_MARKER)
    if idx < 0:
        return set(), []
    section = master_text[idx:]
    for end_marker in TRACKER_END_MARKERS:
        end = section.find(end_marker)
        if end > 0:
            section = section[:end]
            break

    completed: set[str] = set()
    open_rows: list[dict] = []
    for m in TRACKER_LINE.finditer(section):
        line = m.group(2).strip()
        phase_id = extract_tracker_phase_id(line)
        if not phase_id:
            continue
        if m.group(1) == "x":
            completed.add(phase_id)
            continue
        if line.startswith("Phase ") or line.startswith("**Vision-"):
            item = line
            if len(item) > 240:
                item = item[:237] + "..."
            open_rows.append({"source": "lic:master_plan", "item": item, "phase_id": phase_id})
    return completed, open_rows


def infer_plan_phases(filename: str) -> list[str]:
    if filename in PLAN_FILE_COVERED_PHASES:
        return PLAN_FILE_COVERED_PHASES[filename]
    m = re.match(r"2026-05-14-phase-(\d+)", filename)
    if m:
        return [m.group(1)]
    return []


def split_exit_gate_section(text: str) -> tuple[str, str]:
    m = EXIT_GATE_HEADING.search(text)
    if not m:
        return text, ""
    return text[: m.start()], text[m.start() :]


def scan_master_plan() -> tuple[list[dict], set[str]]:
    path = LIC / "docs/superpowers/plans" / MASTER_PLAN_NAME
    text = read_text(path)
    if not text:
        return [{"source": "master_plan", "item": f"missing file: {path}"}], set()
    completed, open_rows = parse_phase_tracker(text)
    return open_rows, completed


def scan_provability_gaps() -> dict:
    path = LIC / "docs/verification/provability-gaps.md"
    text = read_text(path)
    if not text:
        return {"missing_file": str(path), "partial": [], "missing": []}
    partial = [m.group(0).split("|")[1].strip() for m in PARTIAL_GAP.finditer(text)]
    missing = [m.group(0).split("|")[1].strip() for m in MISSING_GAP.finditer(text)]
    return {"partial": partial, "missing": missing}


def scan_plan_dir(completed_phases: set[str], tracker_open_keys: set[str]) -> tuple[list[dict], list[dict], list[dict]]:
    plan_dir = LIC / "docs/superpowers/plans"
    if not plan_dir.is_dir():
        return [], [], []

    open_plans: list[dict] = []
    suppressed: list[dict] = []
    stale_spec: list[dict] = []

    for path in sorted(plan_dir.glob("*.md")):
        if path.name == MASTER_PLAN_NAME:
            continue
        text = read_text(path)
        if not text:
            continue

        source = f"lic:plans/{path.name}"
        covered = infer_plan_phases(path.name)
        phase_done = bool(covered) and all(p in completed_phases for p in covered)

        body, exit_gate = split_exit_gate_section(text)
        is_stale_spec_plan = path.name in STALE_SPEC_IMPLEMENTATION_PLANS

        def classify_chunk(chunk: str, *, section: str) -> None:
            if not chunk.strip():
                return
            for row in unchecked_items(chunk, source):
                key = normalize_item_key(row["item"])
                if key in tracker_open_keys:
                    suppressed.append(
                        {**row, "reason": "duplicate_tracker_open", "kind": "suppressed"}
                    )
                    continue
                if (
                    is_stale_spec_plan
                    and section == "implementation_tasks"
                    and all(p in completed_phases for p in covered)
                ):
                    stale_spec.append(
                        {
                            **row,
                            "reason": "normative_implementation_checklist",
                            "kind": "stale_spec",
                        }
                    )
                    continue
                if phase_done and section != "exit_gate":
                    suppressed.append(
                        {**row, "reason": "tracker_phase_complete", "kind": "suppressed", "phases": covered}
                    )
                    continue
                open_plans.append({**row, "kind": "plan_gate"})

        if is_stale_spec_plan:
            classify_chunk(body, section="implementation_tasks")
            classify_chunk(exit_gate, section="exit_gate")
        else:
            classify_chunk(text, section="full")

        if len(open_plans) > 200:
            break

    return open_plans[:40], suppressed[:20], stale_spec[:15]


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


def _catalog_repo_root(repo: str) -> Path | None:
    """Resolve checkout root for catalog path checks."""
    if repo == "lic":
        return LIC
    if repo == "lis":
        vendor = ROOT / "vendor/lis-tier5"
        if vendor.is_dir():
            return vendor
        return LIS if LIS.is_dir() else None
    if repo == "benchmarks":
        return ROOT
    return None


def catalog_without_repo_path() -> list[dict]:
    import tomllib

    catalog = ROOT / "catalog.toml"
    if not catalog.is_file():
        return []
    data = tomllib.loads(catalog.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in data.get("benchmark", []):
        rel = str(row.get("path", "")).strip()
        if not rel or rel == "unknown":
            continue
        if row.get("catalog_lifecycle") == "planned":
            continue
        repo = str(row.get("repo", "lic"))
        root = _catalog_repo_root(repo)
        if root is None:
            continue
        bench_path = root / rel
        if bench_path.is_dir() or bench_path.is_file():
            continue
        out.append(
            {
                "source": "benchmarks:catalog.toml",
                "item": (
                    f"catalog id={row.get('id')} path missing under {repo} root "
                    f"({root.name}): {rel}"
                ),
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
    master, completed_phases = scan_master_plan()
    tracker_open_keys = {normalize_item_key(i["item"]) for i in master}
    gaps = scan_provability_gaps()
    plans, suppressed, stale_spec = scan_plan_dir(completed_phases, tracker_open_keys)
    catalog = catalog_without_repo_path()
    stubs = package_stubs()
    physics = scan_physics_push()

    open_items = master + plans + catalog + stubs + physics
    for g in gaps.get("partial", []):
        open_items.append({"source": "lic:provability-gaps", "item": f"Partial: {g}"})
    for g in gaps.get("missing", []):
        open_items.append({"source": "lic:provability-gaps", "item": f"Missing: {g}"})

    report = {
        "generated_at": now,
        "roots": {
            "lic": str(LIC),
            "lis": str(LIS),
            "benchmarks": str(ROOT),
            "roadmap": str(ROADMAP),
        },
        "summary": {
            "open_tracker_items": len(master),
            "open_plan_checkboxes": len(plans),
            "plan_checkboxes_suppressed": len(suppressed),
            "stale_spec_checklists": len(stale_spec),
            "provability_partial": len(gaps.get("partial", [])),
            "provability_missing": len(gaps.get("missing", [])),
            "catalog_gaps": len(catalog),
            "total_findings": len(open_items),
            "tracker_phases_complete": len(completed_phases),
        },
        "master_plan_open": master,
        "plan_files_open": plans,
        "plan_files_suppressed": suppressed,
        "stale_spec_checklists": stale_spec,
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
    if stale_spec:
        report["recommended_actions"].append(
            {
                "priority": "P3",
                "action": "Archive or check off stale implementation task lists in sub-plans (normative spec, not gates)",
                "count": len(stale_spec),
                "files": sorted({r["source"] for r in stale_spec}),
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
