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
LIC_HTTP_CSV = ROOT / "lic/benchmarks/results/http_tier5.csv"
HTTP_SUITE = ROOT / "vendor/lis-tier5/benchmarks/tier5_http/suite.toml"
EXPLOIT_CSV = ROOT / "vendor/lis-tier5/results/exploit_report.csv"
OUT_JSON = ROOT / "data/latest/benchmark-matrix.json"
OUT_MD = ROOT / "data/latest/benchmark-matrix.md"
OUT_HTTP_RPS_DOC = ROOT / "docs/ecosystem/http-server-rps-matrix.md"

# Canonical tier-5 HTTP scenarios (always render every row; fill Li on each httpd step).
HTTP_RPS_SCENARIOS = [
    "static_small",
    "keepalive_pipelining",
    "static_large",
    "proxy_loopback",
    "lb_round_robin",
    "lb_least_conn",
    "lb_peer_down",
]
HTTP_VERIFY_SCENARIOS = [
    "rate_limit_429",
    "https_static",
]
HTTP_BENCH_LANGS = ["li", "nginx", "apache", "lighttpd", "node", "bun"]

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


def load_http_scenario_order() -> tuple[list[str], list[str]]:
    """RPS + verify scenario order from suite.toml (fallback to built-in lists)."""
    rps = list(HTTP_RPS_SCENARIOS)
    verify = list(HTTP_VERIFY_SCENARIOS)
    if HTTP_SUITE.is_file():
        import tomllib

        data = tomllib.loads(HTTP_SUITE.read_text(encoding="utf-8"))
        prof = data.get("profiles", {}).get("nightly") or data.get("profiles", {}).get("ci") or {}
        include = list(prof.get("include") or [])
        if include:
            rps = [s for s in include if s not in HTTP_VERIFY_SCENARIOS]
            verify = [s for s in include if s in HTTP_VERIFY_SCENARIOS]
    return rps, verify


def merge_http_csv_rows() -> list[dict[str, str]]:
    """Vendor tier5 CSV plus optional supplemental lic http_tier5.csv (proxy variants)."""
    rows = parse_csv(HTTP_CSV)
    extra = parse_csv(LIC_HTTP_CSV)
    if not extra:
        return rows
    keyed: dict[tuple[str, str, str], dict[str, str]] = {}
    for r in rows:
        key = (r.get("benchmark") or "", r.get("lang") or "", r.get("metric") or "")
        keyed[key] = r
    for r in extra:
        bid = r.get("benchmark") or ""
        lang = r.get("lang") or ""
        metric = r.get("metric") or ""
        variant = r.get("variant") or ""
        key = (bid, lang, metric)
        if bid == "proxy_loopback" and lang == "li" and variant in ("li_epoll", "c_epoll"):
            try:
                sup_val = float(r.get("value") or 0)
            except (TypeError, ValueError):
                sup_val = 0.0
            prev = keyed.get(key)
            if prev is None:
                if sup_val > 0:
                    keyed[key] = r
            else:
                try:
                    prev_val = float(prev.get("value") or 0)
                except (TypeError, ValueError):
                    prev_val = 0.0
                if sup_val > prev_val:
                    keyed[key] = r
        elif key not in keyed:
            keyed[key] = r
    return list(keyed.values())


def http_perf_matrix(rows: list[dict]) -> dict[str, dict[str, float]]:
    by_bench: dict[str, dict[str, float]] = defaultdict(dict)
    for r in rows:
        if r.get("metric") != "rps":
            continue
        bid = r.get("benchmark") or ""
        lang = r.get("lang") or ""
        if lang == "harness":
            continue
        try:
            val = float(r["value"])
        except (TypeError, ValueError):
            continue
        prev = by_bench[bid].get(lang)
        if prev is None or val > prev:
            by_bench[bid][lang] = val
    return {k: dict(v) for k, v in by_bench.items()}


def http_li_status(rows: list[dict]) -> dict[str, str]:
    """Per-scenario Li status from harness verify_only / verify_fail rows."""
    notes: dict[str, str] = {}
    for r in rows:
        bid = r.get("benchmark") or ""
        lang = r.get("lang") or ""
        metric = r.get("metric") or ""
        flags = (r.get("flags") or "").strip()
        if metric == "rps" and lang == "li":
            continue
        if lang not in ("li", "harness"):
            continue
        if metric in ("verify_pass", "verify_skip"):
            notes[bid] = metric
        elif flags.startswith("verify_fail_li") or flags.startswith("wrk_parse_fail"):
            notes[bid] = flags
        elif flags.startswith("verify_fail") or flags == "no_li_httpd_bin":
            notes[bid] = flags
    return notes


def http_verify_matrix(rows: list[dict]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for r in rows:
        metric = r.get("metric") or ""
        if metric not in ("verify_pass", "verify_skip"):
            continue
        bid = r.get("benchmark") or ""
        lang = r.get("lang") or "li"
        if metric == "verify_pass":
            out[bid][lang] = "pass"
        elif metric == "verify_skip":
            out[bid][lang] = "skip"
    return dict(out)


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
    http_rows = merge_http_csv_rows()
    exploit_rows = parse_csv(EXPLOIT_CSV)
    http_perf = http_perf_matrix(http_rows)
    http_verify = http_verify_matrix(http_rows)
    http_li_notes = http_li_status(http_rows)
    rps_order, verify_order = load_http_scenario_order()
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
        "http_performance_order": rps_order,
        "http_verify": http_verify,
        "http_verify_order": verify_order,
        "http_li_status": http_li_notes,
        "http_bench_langs": HTTP_BENCH_LANGS,
        "http_exploits": {
            "profile": "see TIER5_EXPLOIT_PROFILE",
            "matrix": exploits,
            "failures": exploit_failures,
            "cells": exploit_total,
            "status": "green" if exploit_failures == 0 and exploit_total else "red" if exploit_failures else "unknown",
        },
    }


def _format_rps_cell(bid: str, lang: str, hp: dict, li_notes: dict) -> str:
    v = hp.get(bid, {}).get(lang)
    if lang == "li":
        note = li_notes.get(bid, "")
        if note.startswith("wrk_parse_fail") or note.startswith("verify_fail_li"):
            return "FAIL"
    if v is not None:
        if lang == "li" and v <= 0 and li_notes.get(bid, "").startswith("wrk_parse_fail"):
            return "FAIL"
        return f"{v:,.0f}"
    if lang == "li":
        note = li_notes.get(bid, "")
        if note.startswith("wrk_parse_fail"):
            return "FAIL"
        if note.startswith("verify_fail_li"):
            return "FAIL"
        if note == "no_li_httpd_bin":
            return "no bin"
    return "—"


def _li_nginx_ratio(bid: str, hp: dict, li_notes: dict | None = None) -> str:
    li_v = hp.get(bid, {}).get("li")
    ng_v = hp.get(bid, {}).get("nginx")
    note = (li_notes or {}).get(bid, "")
    if note.startswith("wrk_parse_fail") or note.startswith("verify_fail_li"):
        return "—"
    if li_v is None or ng_v is None or ng_v <= 0 or li_v <= 0:
        return "—"
    return f"{li_v / ng_v:.2f}×"


def render_http_rps_section(matrix: dict) -> list[str]:
    lines: list[str] = []
    hp = matrix.get("http_performance") or {}
    li_notes = matrix.get("http_li_status") or {}
    verify = matrix.get("http_verify") or {}
    rps_order = matrix.get("http_performance_order") or HTTP_RPS_SCENARIOS
    verify_order = matrix.get("http_verify_order") or HTTP_VERIFY_SCENARIOS
    langs = list(matrix.get("http_bench_langs") or HTTP_BENCH_LANGS)

    lines.append("## HTTP performance (RPS)")
    lines.append("")
    if not hp and not Path(HTTP_CSV).is_file():
        lines.append("_No tier-3 HTTP CSV — run `./scripts/run-tier5-http-bench.sh`_")
        lines.append("")
        return lines

    header = "| scenario | " + " | ".join(langs) + " | li/nginx |"
    sep = "|---|" + "|".join(["---"] * len(langs)) + "|---|"
    lines.extend([header, sep])
    for bid in rps_order:
        cells = [_format_rps_cell(bid, lang, hp, li_notes) for lang in langs]
        cells.append(_li_nginx_ratio(bid, hp, li_notes))
        lines.append("| " + bid + " | " + " | ".join(cells) + " |")
    lines.append("")
    note_bits = [f"`{k}`: {v}" for k, v in sorted(li_notes.items()) if v and k in rps_order]
    if note_bits:
        lines.append("**Li notes:** " + "; ".join(note_bits))
        lines.append("")

    lines.append("## HTTP verify / feature gates (non-RPS)")
    lines.append("")
    lines.append("| scenario | li | other oracles |")
    lines.append("|---|---|---|")
    for bid in verify_order:
        li_cell = (verify.get(bid) or {}).get("li") or li_notes.get(bid) or "—"
        extra = []
        if bid in hp:
            for lang in HTTP_BENCH_LANGS:
                v = hp[bid].get(lang)
                if v is not None:
                    extra.append(f"{lang}={v:,.0f}")
        extra_s = "; ".join(extra) if extra else "other oracles N/A"
        lines.append(f"| {bid} | {li_cell} | {extra_s} |")
    lines.append("")
    return lines


def render_http_rps_doc(matrix: dict) -> str:
    """Standalone doc for agents (also embedded in benchmark-matrix.md)."""
    lic = (matrix.get("sources") or {}).get("http_csv", str(HTTP_CSV))
    lines = [
        "# HTTP webserver RPS matrix (tier 3)",
        "",
        f"Generated: {matrix['generated_at']}",
        "",
        "**Mandatory after every li-httpd change:**",
        "`LIC_ROOT=… ./scripts/run-tier5-http-bench.sh` → `./scripts/benchmark-matrix-report.py`",
        "",
        f"Source CSV: `{lic}`",
        "",
        "Oracles: `BENCH_HTTP_ORACLES=nginx,apache,lighttpd,node,bun,li`. "
        "Proxy/LB scenarios bench **nginx + li**; static scenarios bench all oracles.",
        "",
    ]
    lines.extend(render_http_rps_section(matrix))
    lines.append("See also: [http-server-benchmark-growth.md](http-server-benchmark-growth.md), "
                 "[lic-httpd-bench-compat.md](lic-httpd-bench-compat.md).")
    lines.append("")
    return "\n".join(lines)


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
    lines.append("## HTTP exploits (tier 4)")
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

    lines.extend(render_http_rps_section(matrix))

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
    OUT_HTTP_RPS_DOC.write_text(render_http_rps_doc(matrix), encoding="utf-8")

    if not args.json_only:
        print(render_markdown(matrix))
    print(
        f"benchmark-matrix-report: wrote {OUT_JSON}, {OUT_MD}, {OUT_HTTP_RPS_DOC}",
        file=sys.stderr,
    )

    ex = matrix.get("http_exploits", {})
    if ex.get("status") == "red":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
