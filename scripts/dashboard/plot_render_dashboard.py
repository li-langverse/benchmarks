#!/usr/bin/env python3
"""PH-IO-5 — static dashboard HTML+SVG from summary.json (Li std.plot bridge)."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def svg_bar_chart(chart: dict, width: int = 320, height: int = 120) -> str:
    series = chart.get("series") or []
    if not series:
        return (
            f'<svg class="chart-svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
            f'<text x="8" y="24" fill="#888">pending</text></svg>'
        )
    vals = [float(p.get("value") or 0) for p in series if float(p.get("value") or 0) > 0]
    max_v = max(vals) if vals else 1.0
    bar_w = max(12, (width - 40) // max(len(series), 1))
    parts = [
        f'<svg class="chart-svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(chart.get("title", chart.get("id", "")))}">'
    ]
    x0 = 24
    for i, p in enumerate(series):
        v = float(p.get("value") or 0)
        h = int((v / max_v) * (height - 36)) if max_v > 0 else 0
        h = max(h, 2)
        x = x0 + i * bar_w
        y = height - 20 - h
        lang = esc(p.get("lang", "?"))
        parts.append(
            f'<rect x="{x}" y="{y}" width="{bar_w - 4}" height="{h}" fill="#3b82f6" />'
            f'<text x="{x}" y="{height - 4}" font-size="9" fill="#ccc">{lang}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def render_html(summary: dict) -> str:
    sections = []
    for cat_key, cat in (summary.get("categories") or {}).items():
        cards = []
        for chart in cat.get("charts") or []:
            title = esc(chart.get("title") or chart.get("id", ""))
            status = esc(chart.get("status", "unknown"))
            svg = svg_bar_chart(chart)
            cards.append(
                f'<article class="chart-card" data-status="{status}">'
                f"<h3>{title}</h3><span class=\"badge {status}\">{status}</span>{svg}</article>"
            )
        if not cards:
            continue
        label = esc(cat.get("label") or cat_key)
        sections.append(
            f'<section class="chart-section" id="cat-{esc(cat_key)}">'
            f"<h2>{label}</h2><div class=\"chart-grid\">{''.join(cards)}</div></section>"
        )
    body = "\n".join(sections) if sections else "<p>No charts in summary.json</p>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Li Benchmarks (static)</title>
  <link rel="stylesheet" href="assets/style.css" />
</head>
<body>
  <header><h1>Li Benchmarks</h1></header>
  <main>{body}</main>
</body>
</html>
"""


def write_assets(out_dir: Path) -> None:
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    css = assets / "style.css"
    css.write_text(
        """body{font-family:system-ui,sans-serif;background:#0f1419;color:#e6edf3;margin:0;padding:1rem;}
.chart-grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));}
.chart-card{border:1px solid #30363d;border-radius:8px;padding:0.75rem;}
.badge{font-size:0.75rem;padding:0.1rem 0.4rem;border-radius:4px;}
.badge.green{background:#238636;color:#fff;}
.badge.red{background:#da3633;color:#fff;}
.badge.yellow{background:#9e6a03;color:#fff;}
.chart-svg{display:block;margin-top:0.5rem;}
""",
        encoding="utf-8",
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: plot_render_dashboard.py <summary.json> <index.html>", file=sys.stderr)
        return 2
    summary_path = Path(sys.argv[1])
    html_path = Path(sys.argv[2])
    if not summary_path.is_file():
        print(f"plot_render_dashboard: missing {summary_path}", file=sys.stderr)
        return 1
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(summary), encoding="utf-8")
    write_assets(html_path.parent)
    print(f"wrote {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
