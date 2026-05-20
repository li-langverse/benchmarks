#!/usr/bin/env python3
"""Render Li source as a dark-editor PNG with syntax highlighting (Pygments + Pillow).

Examples live under docs/language/examples/*.li. Regenerate shareables:

  python3 scripts/render-li-code-image.py --all

Requires: pygments, pillow (`pip install -r scripts/requirements-docs-visual.txt`).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pygments import lexers
from pygments.formatter import Formatter
from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Token

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "docs/language/examples"
DEFAULT_ASSETS = ROOT / "docs/language/assets"

COLORS = {
    Comment: "#6A9955",
    Keyword: "#569CD6",
    Keyword.Type: "#4EC9B0",
    Name: "#9CDCFE",
    Name.Function: "#DCDCAA",
    Name.Decorator: "#DCDCAA",
    Name.Builtin: "#4EC9B0",
    Number: "#B5CEA8",
    String: "#CE9178",
    Operator: "#D4D4D4",
    Punctuation: "#D4D4D4",
    Token: "#D4D4D4",
}

BG = "#1e1e1e"
GUTTER_BG = "#252526"
GUTTER_FG = "#858585"
TAB_BG = "#2d2d2d"
TAB_FG = "#cccccc"
BORDER = "#3c3c3c"
ACCENT = "#007acc"

# Tight card for social — shrink font until content fits
DEFAULT_MAX_WIDTH_PX = 520
DEFAULT_FONT_SIZE = 14


class LiLexer(RegexLexer):
    """Minimal Li highlighter for docs shareables (not the compiler lexer)."""

    name = "Li"
    aliases = ["li"]
    filenames = ["*.li"]
    mimetypes = ["text/x-li"]

    tokens = {
        "root": [
            (r"#[^\n]*", Comment.Single),
            (r"@[a-zA-Z_][\w.]*(?:\([^)]*\))?", Name.Decorator),
            (
                r"\b(def|proc|type|object|import|return|var|if|else|while|for|parallel|in|"
                r"requires|ensures|decreases|raises|public|private|protected|true|false)\b",
                Keyword,
            ),
            (r"\b(int|int64|float|f64|ptr|str|unit|array)\b", Keyword.Type),
            (r"\b[a-zA-Z_][\w]*\b", Name),
            (r"\b\d+(\.\d+)?\b", Number),
            (r"[<>=!+\-*/.:]+", Operator),
            (r"[\[\](),]", Punctuation),
            (r"\s+", Token),
        ],
    }


lexers.LiLexer = LiLexer  # type: ignore[attr-defined]


def prepare_source(code: str, *, strip_comments: bool, trim_trailing: bool) -> str:
    """Normalize to compiler-style layout: no banner comments, no trailing spaces."""
    lines = code.splitlines()
    out: list[str] = []
    for line in lines:
        if strip_comments and re.match(r"^\s*#", line):
            continue
        if trim_trailing:
            line = line.rstrip()
        out.append(line)
    # Drop leading/trailing blank lines
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out) + ("\n" if out else "")


class EditorImageFormatter(Formatter):
    """Draw highlighted source onto a PNG (editor chrome + line numbers)."""

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.source_text = options.get("source_text", "")
        self.tab_title = options.get("tab_title", "example.li")
        self.font_size = int(options.get("font_size", DEFAULT_FONT_SIZE))
        self.line_height = int(options.get("line_height", 20))
        self.pad_x = int(options.get("pad_x", 12))
        self.gutter_w = int(options.get("gutter_w", 44))
        self.tab_h = int(options.get("tab_h", 32))
        self.max_width_px = int(options.get("max_width_px", DEFAULT_MAX_WIDTH_PX))

    def _measure(self, lines: list[list[tuple[str, str]]], font) -> tuple[int, object]:
        from PIL import Image, ImageDraw

        draw_probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        line_widths = []
        for row in lines:
            w = self.pad_x * 2
            for text, _ in row:
                w += int(draw_probe.textlength(text, font=font))
            line_widths.append(w)
        content_w = max(line_widths, default=self.pad_x * 2)
        return content_w, draw_probe

    def format(self, tokensource, outfile):
        from PIL import Image, ImageDraw, ImageFont

        # Re-split on physical source lines (lexer token stream can omit \n boundaries).
        raw = self.source_text
        source_lines = raw.splitlines() if raw else []
        lines: list[list[tuple[str, str]]] = []
        lexer = LiLexer()
        for physical in source_lines:
            row: list[tuple[str, str]] = []
            for ttype, value in lexer.get_tokens(physical):
                value = value.replace("\n", "")
                if not value:
                    continue
                color = COLORS.get(ttype, COLORS[Token])
                row.append((value, color))
            if not row:
                row = [("", COLORS[Token])]
            lines.append(row)

        if not lines:
            lines = [[("", COLORS[Token])]]

        font_size = self.font_size
        content_w = 0
        draw_probe = None
        while font_size >= 11:
            try:
                font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()
            content_w, draw_probe = self._measure(lines, font)
            if self.gutter_w + content_w + 2 <= self.max_width_px:
                break
            font_size -= 1
        else:
            try:
                font = ImageFont.truetype("DejaVuSansMono.ttf", 11)
            except OSError:
                font = ImageFont.load_default()
            content_w, draw_probe = self._measure(lines, font)

        width = self.gutter_w + content_w + 2
        height = self.tab_h + len(lines) * self.line_height + self.pad_x * 2 + 2

        img = Image.new("RGB", (width, height), BG)
        draw = ImageDraw.Draw(img)

        draw.rectangle([0, 0, width, self.tab_h], fill=TAB_BG)
        draw.rectangle([0, self.tab_h - 2, width, self.tab_h], fill=ACCENT)
        draw.text((12, 8), self.tab_title, fill=TAB_FG, font=font)

        y0 = self.tab_h
        draw.rectangle([0, y0, width, height], outline=BORDER, width=1)
        draw.rectangle([0, y0, self.gutter_w, height], fill=GUTTER_BG)

        nlines = len(lines)
        gutter_digits = len(str(nlines))

        for i, row in enumerate(lines):
            y = y0 + self.pad_x + i * self.line_height
            ln = str(i + 1).rjust(gutter_digits)
            draw.text((8, y), ln, fill=GUTTER_FG, font=font)
            x = self.gutter_w + self.pad_x
            for text, color in row:
                draw.text((x, y), text, fill=color, font=font)
                x += int(draw_probe.textlength(text, font=font))

        img.save(outfile, format="PNG", optimize=True)


PRESETS: list[tuple[str, str, str]] = [
    ("object_encapsulation.li", "li-code-encapsulation-editor.png", "object_encapsulation.li"),
    ("parallel_with_disjoint.li", "li-code-decorators-editor.png", "parallel_with_disjoint.li"),
    ("csv_ingest_smoke.li", "li-code-ingest-editor.png", "csv_ingest_smoke.li"),
]


def render_file(
    src: Path,
    dest: Path,
    tab: str | None = None,
    *,
    strip_comments: bool = True,
    max_width_px: int = DEFAULT_MAX_WIDTH_PX,
) -> None:
    raw = src.read_text(encoding="utf-8")
    code = prepare_source(raw, strip_comments=strip_comments, trim_trailing=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    lexer = LiLexer()
    formatter = EditorImageFormatter(
        tab_title=tab or src.name,
        max_width_px=max_width_px,
        source_text=code,
    )
    with open(dest, "wb") as out:
        formatter.format(lexer.get_tokens(code), out)
    from PIL import Image as PilImage

    with PilImage.open(dest) as im:
        px_w = im.size[0]
    print(f"wrote {dest} ({dest.stat().st_size // 1024} KiB, {px_w}px wide)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Li .li source as editor-style PNG")
    parser.add_argument("-i", "--input", type=Path, help="Source .li file")
    parser.add_argument("-o", "--output", type=Path, help="Output .png path")
    parser.add_argument("--tab", default=None, help="Tab bar title (default: input basename)")
    parser.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH_PX, help="Max image width in px")
    parser.add_argument(
        "--keep-comments",
        action="store_true",
        help="Keep # comment lines (default: strip for narrower cards)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"Render presets from {DEFAULT_EXAMPLES} → {DEFAULT_ASSETS}",
    )
    args = parser.parse_args()

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("render-li-code-image: install pillow — pip install pillow", file=sys.stderr)
        return 1

    if args.all:
        for name, out_name, tab in PRESETS:
            src = DEFAULT_EXAMPLES / name
            if not src.is_file():
                print(f"missing example: {src}", file=sys.stderr)
                return 1
            render_file(
                src,
                DEFAULT_ASSETS / out_name,
                tab=tab,
                strip_comments=not args.keep_comments,
                max_width_px=args.max_width,
            )
        return 0

    if not args.input or not args.output:
        parser.error("use --all or both -i and -o")
    if not args.input.is_file():
        print(f"not found: {args.input}", file=sys.stderr)
        return 1
    render_file(
        args.input,
        args.output,
        tab=args.tab,
        strip_comments=not args.keep_comments,
        max_width_px=args.max_width,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
