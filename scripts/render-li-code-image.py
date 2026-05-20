#!/usr/bin/env python3
"""Render Li source as a dark-editor PNG with syntax highlighting (Pygments + Pillow).

Examples live under docs/language/examples/*.li. Regenerate shareables:

  python3 scripts/render-li-code-image.py --all
  python3 scripts/render-li-code-image.py -i docs/language/examples/object_encapsulation.li \\
      -o docs/language/assets/li-code-encapsulation-editor.png --tab object_encapsulation.li

Requires: pygments (stdlib on many images), pillow (`pip install pillow`).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pygments import lexers, highlight
from pygments.formatter import Formatter
from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Token

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "docs/language/examples"
DEFAULT_ASSETS = ROOT / "docs/language/assets"

# VS Code Dark+–style token colors (hex)
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


class LiLexer(RegexLexer):
    """Minimal Li highlighter for docs shareables (not the compiler lexer)."""

    name = "Li"
    aliases = ["li"]
    filenames = ["*.li"]
    mimetypes = ["text/x-li"]

    tokens = {
        "root": [
            (r"#[^\n]*", Comment.Single),
            (r"@[a-zA-Z_][\w.]*", Name.Decorator),
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


class EditorImageFormatter(Formatter):
    """Draw highlighted source onto a PNG (editor chrome + line numbers)."""

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.tab_title = options.get("tab_title", "example.li")
        self.font_size = int(options.get("font_size", 15))
        self.line_height = int(options.get("line_height", 22))
        self.pad_x = int(options.get("pad_x", 16))
        self.gutter_w = int(options.get("gutter_w", 52))
        self.tab_h = int(options.get("tab_h", 36))

    def format(self, tokensource, outfile):
        from PIL import Image, ImageDraw, ImageFont

        lines: list[list[tuple[str, str]]] = [[]]
        for ttype, value in tokensource:
            color = COLORS.get(ttype, COLORS[Token])
            for part in value.split("\n"):
                if part:
                    lines[-1].append((part, color))
                if value.endswith("\n"):
                    lines.append([])

        if lines and not lines[-1]:
            lines.pop()
        if not lines:
            lines = [[("", COLORS[Token])]]

        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", self.font_size)
        except OSError:
            font = ImageFont.load_default()

        draw_probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        char_w = max(draw_probe.textlength("M", font=font), 8)

        max_cols = max(
            sum(len(text) for text, _ in row) for row in lines
        )
        content_w = int(max_cols * char_w) + self.pad_x * 2
        content_h = len(lines) * self.line_height + self.pad_x * 2

        width = self.gutter_w + content_w + 2
        height = self.tab_h + content_h + 2

        img = Image.new("RGB", (width, height), BG)
        draw = ImageDraw.Draw(img)

        # Tab bar
        draw.rectangle([0, 0, width, self.tab_h], fill=TAB_BG)
        draw.rectangle([0, self.tab_h - 2, width, self.tab_h], fill=ACCENT)
        draw.text((14, 10), self.tab_title, fill=TAB_FG, font=font)

        y0 = self.tab_h
        draw.rectangle([0, y0, width, height], outline=BORDER, width=1)

        # Gutter
        draw.rectangle([0, y0, self.gutter_w, height], fill=GUTTER_BG)

        for i, row in enumerate(lines):
            y = y0 + self.pad_x + i * self.line_height
            ln = str(i + 1).rjust(len(str(len(lines))))
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


def render_file(src: Path, dest: Path, tab: str | None = None) -> None:
    code = src.read_text(encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    lexer = LiLexer()
    formatter = EditorImageFormatter(tab_title=tab or src.name)
    with open(dest, "wb") as out:
        highlight(code, lexer, formatter, out)
    print(f"wrote {dest} ({dest.stat().st_size // 1024} KiB)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Li .li source as editor-style PNG")
    parser.add_argument("-i", "--input", type=Path, help="Source .li file")
    parser.add_argument("-o", "--output", type=Path, help="Output .png path")
    parser.add_argument("--tab", default=None, help="Tab bar title (default: input basename)")
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
            render_file(src, DEFAULT_ASSETS / out_name, tab=tab)
        return 0

    if not args.input or not args.output:
        parser.error("use --all or both -i and -o")
    if not args.input.is_file():
        print(f"not found: {args.input}", file=sys.stderr)
        return 1
    render_file(args.input, args.output, tab=args.tab)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
