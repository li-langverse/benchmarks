#!/usr/bin/env python3
"""Render tier-5 HTTP (nginx oracle) bar charts into data/visuals/latest/.

Reads ``data/latest/summary.json`` (http category) or ``lis/results/latest.csv``.
Does not require lic; safe to run after ``bench_http.py`` in lis.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/visuals/latest"
LANG_COLORS = {
    "nginx": "#009639",
    "li": "#5c4ee5",
    "harness": "#888888",
    "cpp": "#00599c",
}


def load_from_summary(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    http = (data.get("categories") or {}).get("http") or {}
    charts = http.get("charts") or []
    out: list[dict] = []
    for ch in charts:
        series = ch.get("series") or []
        if not series:
            continue
        out.append(
            {
                "id": ch["id"],
                "title": ch.get("title") or ch["id"],
                "reference_lang": ch.get("reference_lang") or "nginx",
                "metric": ch.get("metric") or "rps",
                "unit": ch.get("unit") or "req/s",
                "series": series,
                "ratio": ch.get("ratio_vs_reference"),
                "status": ch.get("status") or "unknown",
            }
        )
    return out


def load_from_lis_csv(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_bench: dict[str, list[dict]] = {}
    for r in rows:
        if r.get("metric") != "rps":
            continue
        by_bench.setdefault(r["benchmark"], []).append(
            {
                "lang": r["lang"],
                "value": float(r["value"]),
                "unit": r.get("unit") or "req/s",
                "variant": r.get("variant") or "",
            }
        )
    out: list[dict] = []
    for bid, series in sorted(by_bench.items()):
        out.append(
            {
                "id": bid,
                "title": bid.replace("_", " "),
                "reference_lang": "nginx",
                "metric": "rps",
                "unit": "req/s",
                "series": series,
                "ratio": None,
                "status": "unknown",
            }
        )
    return out


def render_charts(charts: list[dict], out_dir: Path) -> list[Path]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("plot_http_benchmarks: skip (matplotlib not installed)", file=sys.stderr)
        return []

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for ch in charts:
        series = ch["series"]
        if not series:
            continue
        langs = [s["lang"] for s in series]
        vals = [float(s["value"]) for s in series]
        colors = [LANG_COLORS.get(lang, "#444444") for lang in langs]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.bar(langs, vals, color=colors, edgecolor="#222", linewidth=0.5)
        ax.set_ylabel(f"{ch['metric']} ({ch['unit']})")
        ax.set_title(f"{ch['title']} — tier-5 HTTP (ref: {ch['reference_lang']})")
        for bar, v in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{v:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )
        if ch.get("ratio") is not None:
            ax.text(
                0.02,
                0.98,
                f"li/nginx ratio: {ch['ratio']:.3f}",
                transform=ax.transAxes,
                va="top",
                fontsize=9,
            )
        elif all(s["lang"] != "li" for s in series):
            ax.text(
                0.02,
                0.98,
                "nginx baseline only (li-httpd not wired)",
                transform=ax.transAxes,
                va="top",
                fontsize=8,
                color="#666",
            )
        fig.tight_layout()
        path = out_dir / f"http_{ch['id']}_rps.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        written.append(path)
        print(f"wrote {path}")

    if len(charts) >= 2:
        fig, ax = plt.subplots(figsize=(7, 4))
        ids = [c["id"] for c in charts]
        nginx_vals = []
        for c in charts:
            nv = next(
                (s["value"] for s in c["series"] if s["lang"] == "nginx"),
                None,
            )
            nginx_vals.append(float(nv) if nv is not None else 0.0)
        x = range(len(ids))
        ax.bar(x, nginx_vals, color=LANG_COLORS["nginx"], label="nginx")
        ax.set_xticks(list(x))
        ax.set_xticklabels([i.replace("_", "\n") for i in ids], fontsize=8)
        ax.set_ylabel("rps (req/s)")
        ax.set_title("Tier-5 HTTP — nginx baseline (CI profile)")
        ax.legend(loc="upper right")
        fig.tight_layout()
        overview = out_dir / "http_tier5_overview.png"
        fig.savefig(overview, dpi=120)
        plt.close(fig)
        written.append(overview)
        print(f"wrote {overview}")

    return written


def main() -> int:
    p = argparse.ArgumentParser(description="Plot HTTP tier-5 benchmarks")
    p.add_argument("--summary", type=Path, default=ROOT / "data/latest/summary.json")
    p.add_argument("--lis-csv", type=Path, default=None)
    p.add_argument("--out", type=Path, default=OUT)
    args = p.parse_args()

    charts: list[dict] = []
    if args.lis_csv and args.lis_csv.is_file():
        charts = load_from_lis_csv(args.lis_csv)
    elif args.summary.is_file():
        charts = load_from_summary(args.summary)

    if not charts:
        print("plot_http_benchmarks: no HTTP rps data", file=sys.stderr)
        return 0

    written = render_charts(charts, args.out)
    if written:
        manifest_script = ROOT / "scripts/visual-manifest.py"
        if manifest_script.is_file():
            import subprocess

            subprocess.run(
                [sys.executable, str(manifest_script), str(args.out)],
                check=False,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
