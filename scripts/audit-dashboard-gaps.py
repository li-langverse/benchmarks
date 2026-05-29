#!/usr/bin/env python3
"""Audit data/latest/summary.json for dashboard completeness gaps (P0 / P1).

P0: missing size, unknown validity/status without reason, missing SOTA, missing macOS/Windows
     rows per benchmark base, harness-only perf for tier<=2.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
OUT = ROOT / "data/latest/dashboard-gap-report.json"
REQUIRED_OS = ("linux", "macos", "windows")
OK_VALIDITY = frozenset({"pass", "fail", "skip", "advisory"})
OK_STATUS = frozenset({"green", "yellow", "red", "skip"})


def normalize_chart_os(raw: str | None) -> str:
    if not raw:
        return ""
    os = str(raw).strip().lower()
    if os in ("darwin", "osx"):
        return "macos"
    return os


def load_summary(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"audit-dashboard-gaps: missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def collect_charts(summary: dict) -> list[dict]:
    charts: list[dict] = []
    for _cat, cdata in (summary.get("categories") or {}).items():
        charts.extend(cdata.get("charts") or [])
    return charts


def audit(summary: dict) -> dict:
    charts = collect_charts(summary)
    rows = summary.get("rows") or []

    def chart_base(ch: dict) -> str:
        bid = str(ch.get("base_id") or ch.get("id") or "")
        return bid.split("@", 1)[0]

    by_base: dict[str, list[dict]] = defaultdict(list)
    for ch in charts:
        by_base[chart_base(ch)].append(ch)

    p0: list[dict] = []
    p1: list[dict] = []
    counts = Counter()

    def add(severity: str, code: str, base: str, detail: str, chart_id: str | None = None) -> None:
        entry = {"severity": severity, "code": code, "base_id": base, "detail": detail}
        if chart_id:
            entry["chart_id"] = chart_id
        (p0 if severity == "P0" else p1).append(entry)
        counts[code] += 1

    for base, group in sorted(by_base.items()):
        oss = {normalize_chart_os(c.get("os")) for c in group if c.get("os")}
        missing_os = [o for o in REQUIRED_OS if o not in oss]
        if missing_os:
            add("P0", "missing_os", base, f"missing platforms: {missing_os}; have {sorted(oss)}")

        for ch in group:
            cid = ch.get("id") or base
            sl = ch.get("size_label")
            if sl in (None, "", "-", "harness pending", "pending"):
                add("P0", "bad_size_label", base, f"size_label={sl!r}", cid)
            if ch.get("problem_size") is None and sl in (None, "", "-", "harness pending"):
                add("P1", "problem_size_null", base, "problem_size is null", cid)

            vs = ch.get("validity_status")
            if vs not in OK_VALIDITY:
                add("P0", "validity_unknown", base, f"validity_status={vs!r}", cid)

            st = ch.get("status")
            if st not in OK_STATUS:
                if st in (None, "", "unknown") and not ch.get("pending"):
                    add("P0", "status_unknown", base, f"status={st!r}", cid)
                elif st in (None, "", "unknown"):
                    add("P1", "status_unknown_pending", base, f"status={st!r}", cid)

            if not ch.get("sota_lang") and ch.get("sota_value") is None:
                if st in ("green", "yellow", "red") and not ch.get("pending"):
                    add("P0", "sota_empty", base, "no sota_lang/sota_value", cid)

            tier = ch.get("tier")
            if tier is None:
                for r in rows:
                    if r.get("benchmark") == base or r.get("benchmark") == cid:
                        tier = r.get("tier")
                        break
            series = ch.get("series") or []
            if tier in (0, 1, 2, "0", "1", "2") and any(
                s.get("lang") == "harness" for s in series
            ):
                add("P0", "harness_lang_tier12", base, "tier<=2 chart has lang=harness", cid)

            if ch.get("pending"):
                add("P1", "chart_pending", base, "chart marked pending", cid)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary_path": str(SUMMARY.relative_to(ROOT)),
        "benchmark_bases": len(by_base),
        "chart_rows": len(charts),
        "table_rows": len(rows),
        "p0_count": len(p0),
        "p1_count": len(p1),
        "issue_counts": dict(counts),
        "p0": p0[:500],
        "p1": p1[:200],
    }
    return report


def main() -> int:
    summary = load_summary(SUMMARY)
    report = audit(summary)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        f"audit-dashboard-gaps: bases={report['benchmark_bases']} "
        f"P0={report['p0_count']} P1={report['p1_count']}"
    )
    print(f"  wrote {OUT.relative_to(ROOT)}")
    for code, n in sorted(report["issue_counts"].items(), key=lambda x: -x[1])[:12]:
        print(f"  {code}: {n}")

    return 1 if report["p0_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
