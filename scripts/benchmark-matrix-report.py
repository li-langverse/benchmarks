#!/usr/bin/env python3
"""Emit full benchmark + HTTP exploit matrix (stdout + data/latest/benchmark-matrix.json).

Run after every full suite / ingest. Agents should read the JSON or this script's output.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
CATALOG = ROOT / "catalog.toml"
HTTP_CSV = ROOT / "vendor/lis-tier5/results/latest.csv"
EXPLOIT_CSV = ROOT / "vendor/lis-tier5/results/exploit_report.csv"
OUT_JSON = ROOT / "data/latest/benchmark-matrix.json"
OUT_MD = ROOT / "data/latest/benchmark-matrix.md"

CATEGORY_ORDER = [
    "correctness",
    "micro",
    "physics",
    "http",
    "security",
    "tooling",
]
HTTP_LANG_ORDER = ["li", "nginx", "apache", "lighttpd", "node", "bun", "harness"]
EXPLOIT_LANG_ORDER = ["li", "nginx", "apache", "lighttpd", "caddy", "node", "bun"]


def load_catalog() -> dict[str, dict]:
    import tomllib

    out: dict[str, dict] = {}
    raw = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    for b in raw.get("benchmark", []):
        out[b["id"]] = b
    return out


def parse_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def http_perf_matrix(rows: list[dict]) -> dict[str, dict[str, float | str]]:
    by_bench: dict[str, dict[str, float]] = defaultdict(dict)
    for r in rows:
        if r.get("metric") != "rps":
            continue
        bid = r.get("benchmark") or ""
        lang = r.get("lang") or ""
        try:
            by_bench[bid][lang] = float(r["value"])
        except (TypeError, ValueError):
            continue
    return {k: dict(v) for k, v in by_bench.items()}


def exploit_matrix(rows: list[dict]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for r in rows:
        eid = r.get("exploit") or ""
        lang = r.get("lang") or ""
        passed = r.get("pass") == "1"
        flags = r.get("flags") or ""
        out[eid][lang] = "pass" if passed else f"FAIL({flags})"
    return dict(out)


def build_matrix(summary: dict, catalog: dict[str, dict]) -> dict:
    http_rows = parse_csv(HTTP_CSV)
    exploit_rows = parse_csv(EXPLOIT_CSV)
    http_perf = http_perf_matrix(http_rows)
    exploits = exploit_matrix(exploit_rows)

    summary_by_id = {r["benchmark"]: r for r in summary.get("rows", [])}
    sections: dict[str, list[dict]] = defaultdict(list)

    for bid, cfg in sorted(catalog.items(), key=lambda x: (x[1].get("tier", 99), x[0])):
        cat = cfg.get("category", "micro")
        row = summary_by_id.get(bid, {})
        entry = {
            "id": bid,
            "tier": cfg.get("tier"),
            "repo": cfg.get("repo"),
            "category": cat,
            "metric": cfg.get("metric"),
            "status": row.get("status", "unknown"),
            "ratio_vs_reference": row.get("ratio_vs_cpp"),
            "reference_lang": cfg.get("compare_oracle", "cpp"),
            "li_value": row.get("li_value"),
            "ph_ids": cfg.get("ph_ids", []),
        }
        if cat == "http" and bid in http_perf:
            entry["rps_by_lang"] = {
                lang: http_perf[bid].get(lang)
                for lang in HTTP_LANG_ORDER
                if lang in http_perf[bid]
            }
        sections[cat].append(entry)

    exploit_failures = sum(
        1 for e in exploits.values() for v in e.values() if v != "pass"
    )
    exploit_total = sum(len(v) for v in exploits.values())

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "summary_json": str(SUMMARY),
            "catalog_toml": str(CATALOG),
            "http_csv": str(HTTP_CSV),
            "exploit_csv": str(EXPLOIT_CSV),
        },
        "tier_counts": summary.get("tier_counts", {}),
        "sections": {k: sections[k] for k in CATEGORY_ORDER if k in sections},
        "http_performance": http_perf,
        "http_exploits": {
            "profile": "see TIER5_EXPLOIT_PROFILE",
            "matrix": exploits,
            "failures": exploit_failures,
            "cells": exploit_total,
            "status": "green" if exploit_failures == 0 and exploit_total else "red" if exploit_failures else "unknown",
        },
    }


def render_markdown(matrix: dict) -> str:
    lines = [
        "# Benchmark matrix (full)",
        "",
        f"Generated: {matrix['generated_at']}",
        "",
        "Run: `./scripts/run-full-benchmark-suite.sh` then `./scripts/benchmark-matrix-report.py`",
        "",
    ]
    ex = matrix.get("http_exploits", {})
    lines.append("## HTTP exploits (tier 5)")
    lines.append("")
    lines.append(f"Status: **{ex.get('status', 'unknown')}** — {ex.get('failures', 0)} failures / {ex.get('cells', 0)} cells")
    lines.append("")
    em = ex.get("matrix") or {}
    if em:
        langs = []
        for row in em.values():
            for lang in row:
                if lang not in langs:
                    langs.append(lang)
        for lang in EXPLOIT_LANG_ORDER:
            if lang in langs:
                pass
        langs = [l for l in EXPLOIT_LANG_ORDER if l in langs] + [
            l for l in sorted(langs) if l not in EXPLOIT_LANG_ORDER
        ]
        header = "| exploit | " + " | ".join(langs) + " |"
        sep = "|---|" + "|".join(["---"] * len(langs)) + "|"
        lines.extend([header, sep])
        for eid in sorted(em.keys()):
            cells = [em[eid].get(l, "—") for l in langs]
            lines.append("| " + eid + " | " + " | ".join(cells) + " |")
        lines.append("")
    else:
        lines.append("_No exploit_report.csv — run `./scripts/run-tier5-http-exploits.sh`_")
        lines.append("")

    lines.append("## HTTP performance (RPS)")
    lines.append("")
    hp = matrix.get("http_performance") or {}
    if hp:
        langs: list[str] = []
        for row in hp.values():
            for lang in row:
                if lang not in langs:
                    langs.append(lang)
        langs = [l for l in HTTP_LANG_ORDER if l in langs] + [
            l for l in sorted(langs) if l not in HTTP_LANG_ORDER
        ]
        header = "| scenario | " + " | ".join(langs) + " |"
        sep = "|---|" + "|".join(["---"] * len(langs)) + "|"
        lines.extend([header, sep])
        for bid in sorted(hp.keys()):
            cells = []
            for lang in langs:
                v = hp[bid].get(lang)
                cells.append(f"{v:,.0f}" if v is not None else "—")
            lines.append("| " + bid + " | " + " | ".join(cells) + " |")
        lines.append("")
    else:
        lines.append("_No tier-5 HTTP CSV — run tier5 bench in full suite_")
        lines.append("")

    for cat, label in [
        ("correctness", "Correctness"),
        ("micro", "Micro"),
        ("physics", "Physics"),
        ("http", "HTTP catalog gates"),
        ("security", "Security"),
        ("tooling", "Tooling"),
    ]:
        rows = (matrix.get("sections") or {}).get(cat) or []
        if not rows:
            continue
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| benchmark | tier | status | ratio | repo |")
        lines.append("|---|---|---|---|---|")
        for r in rows:
            ratio = r.get("ratio_vs_reference")
            rs = f"{ratio:.3f}×" if ratio is not None else "—"
            lines.append(
                f"| {r['id']} | {r.get('tier')} | {r.get('status')} | {rs} | {r.get('repo')} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="full benchmark matrix report")
    p.add_argument("--json-only", action="store_true")
    p.add_argument("--md-only", action="store_true")
    args = p.parse_args()

    if not SUMMARY.is_file():
        print(f"benchmark-matrix-report: missing {SUMMARY}", file=sys.stderr)
        return 1

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    catalog = load_catalog()
    matrix = build_matrix(summary, catalog)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(matrix), encoding="utf-8")

    if not args.json_only:
        print(render_markdown(matrix))
    print(f"benchmark-matrix-report: wrote {OUT_JSON} and {OUT_MD}", file=sys.stderr)

    ex = matrix.get("http_exploits", {})
    if ex.get("status") == "red":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
