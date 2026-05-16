#!/usr/bin/env python3
"""Validate numerics study / algorithm note artifacts before PR.

Exit 0 if all required checks pass; 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_STUDY_SECTIONS = [
    r"(?i)problem|summary",
    r"(?i)sota|learned from|reference",
    r"(?i)quality|improvement|regression",
    r"(?i)performance|bench|wall_time|ratio",
    r"(?i)stability|tier-?0|energy",
    r"(?i)visual|plot|gif|png|animation",
]

REQUIRED_ALGO_SECTIONS = [
    r"(?i)mathematical|equation|discrete",
    r"(?i)assumption",
    r"(?i)pseudocode|algorithm",
    r"(?i)sota|reference|novel",
    r"(?i)stability|accuracy",
    r"(?i)empirical|validation|performance",
    r"(?i)verification",
]

IMAGE_EXT = {".png", ".gif", ".svg", ".webp"}


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def missing_sections(text: str, patterns: list[str]) -> list[str]:
    missing = []
    for pat in patterns:
        if not re.search(pat, text):
            missing.append(pat)
    return missing


def find_linked_paths(text: str, base: Path) -> list[Path]:
    found: list[Path] = []
    for m in re.finditer(r"`([^`]+\.(?:png|gif|svg|md|toml))`", text, re.I):
        p = (base.parent / m.group(1)).resolve()
        if p.is_file():
            found.append(p)
    for m in re.finditer(r"(?:data/visuals|docs/numerics|lic/benchmarks)[^\s\)]+\.(?:png|gif)", text, re.I):
        rel = m.group(0).split(")")[0]
        p = (ROOT / rel).resolve()
        if p.is_file():
            found.append(p)
    return found


def count_visuals_under(study_path: Path) -> int:
    visuals_dir = ROOT / "data/visuals/latest"
    n = 0
    if visuals_dir.is_dir():
        n += sum(1 for p in visuals_dir.iterdir() if p.suffix.lower() in IMAGE_EXT)
    n += len(find_linked_paths(read_text(study_path), study_path))
    return n


def main() -> int:
    parser = argparse.ArgumentParser(description="Numerics evidence checklist")
    parser.add_argument("--study", type=Path, required=True, help="study markdown path")
    parser.add_argument("--algorithm", type=Path, help="algorithm note (required with --novel)")
    parser.add_argument("--novel", action="store_true", help="require algorithm note sections")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    study_path = args.study if args.study.is_absolute() else ROOT / args.study
    results: dict = {"ok": True, "checks": []}

    def record(name: str, passed: bool, detail: str = "") -> None:
        results["checks"].append({"name": name, "pass": passed, "detail": detail})
        if not passed:
            results["ok"] = False

    if not study_path.is_file():
        record("study_exists", False, f"missing {study_path}")
        print_results(results, args.json)
        return 1

    study_text = read_text(study_path)
    record("study_exists", True)

    miss = missing_sections(study_text, REQUIRED_STUDY_SECTIONS)
    record("study_sections", not miss, f"missing patterns: {miss}" if miss else "ok")

    if re.search(r"(?i)learned from", study_text):
        refs = len(re.findall(r"(?i)https?://|doi\.org|ISBN|Hairer|LeVeque|Trefethen|PETSc|Eigen", study_text))
        record("learned_from_refs", refs >= 2, f"found ~{refs} reference signals (want ≥2)")
    else:
        record("learned_from_refs", False, "no 'Learned from' section")

    visuals = count_visuals_under(study_path)
    record("visual_artifacts", visuals >= 1 or re.search(r"(?i)render-benchmark-visuals", study_text),
           f"visual files or render command ({visuals} files)")

    if re.search(r"(?i)bench\.py|ingest-lic|benchmark-failures", study_text):
        record("bench_commands", True)
    else:
        record("bench_commands", False, "mention bench.py or ingest commands")

    if args.novel:
        algo_path = args.algorithm
        if algo_path is None:
            record("algorithm_note", False, "--algorithm required with --novel")
        else:
            algo_path = algo_path if algo_path.is_absolute() else ROOT / algo_path
            if not algo_path.is_file():
                record("algorithm_note", False, f"missing {algo_path}")
            else:
                record("algorithm_note", True)
                algo_text = read_text(algo_path)
                amiss = missing_sections(algo_text, REQUIRED_ALGO_SECTIONS)
                record("algorithm_sections", not amiss, f"missing: {amiss}" if amiss else "ok")
                if not re.search(r"(?i)novel|differ|what we changed", algo_text):
                    record("novelty_claim", False, "add novelty vs SOTA table")
                else:
                    record("novelty_claim", True)

    print_results(results, args.json)
    return 0 if results["ok"] else 1


def print_results(results: dict, as_json: bool) -> None:
    if as_json:
        import json
        print(json.dumps(results, indent=2))
        return
    for c in results["checks"]:
        mark = "PASS" if c["pass"] else "FAIL"
        extra = f" — {c['detail']}" if c.get("detail") else ""
        print(f"[{mark}] {c['name']}{extra}")
    print("OK" if results["ok"] else "NOT READY")


if __name__ == "__main__":
    raise SystemExit(main())
