#!/usr/bin/env python3
"""Shared drawing primitives for the course figures.

Course-internal build tool; students never run or read code. Standard library only.
Each unit has its own `make-figs.py` that imports this and calls `build()`:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
    from figlib import *

    def fig_something():
        out = [t(40, 26, "a caption", 14, INK)]
        return svg(600, 200, "".join(out))

    build(__file__, [("something", fig_something)])

`build` numbers the files in order: fig01-something.svg, fig02-....svg, next to the
script. Every drawn duplex is checked for real base pairing, every canvas is widened
to fit its labels, and labels that still leave the box raise an error.
"""
import os
import re



MONO = 'ui-monospace, "DejaVu Sans Mono", "Courier New", monospace'
SERIF = '"Palatino Linotype", "Book Antiqua", Palatino, FreeSerif, serif'

INK = "#23282d"       # main text
TOP = "#1f3b57"       # top strand
BOT = "#4a6b8a"       # bottom strand
HOT = "#b4532a"       # the thing being pointed at
OK = "#2e6b3f"
BAD = "#a33a28"
MUTE = "#8a8f94"

DX = 13.5             # per-base advance, matches 13px monospace


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family=\'{SERIF}\' fill="{INK}">\n'
        f'<rect width="{w}" height="{h}" fill="none"/>\n{body}\n</svg>\n'
    )


def t(x, y, s, size=15, fill=None, anchor="start", family=None, weight=None, style=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    f = f' fill="{fill}"' if fill else ""
    fam = f" font-family='{family}'" if family else ""
    w = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" font-size="{size}"{a}{f}{fam}{w}{st}>{s}</text>'


def seq(x, y, s, fill=INK, size=13):
    """A run of bases in monospace, returns (svg, width)."""
    out = []
    for i, ch in enumerate(s):
        if ch != " ":
            out.append(t(x + i * DX, y, ch, size=size, fill=fill, family=MONO))
    return "".join(out), len(s) * DX


def line(x1, y1, x2, y2, stroke=INK, w=1.4, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linecap="{cap}"{d}/>')


COMP = {"AT", "TA", "GC", "CG", "AU", "UA", "GU", "UG"}


def check_pairing(top, bot):
    """Guard: aligned bases must actually pair. A wrong duplex in teaching material
    is worse than no figure, so this raises instead of drawing it."""
    for i, (a, b) in enumerate(zip(top, bot)):
        if a != " " and b != " " and a + b not in COMP:
            raise AssertionError(f"position {i}: {a} cannot pair with {b}\n  {top}\n  {bot}")


def pairs(x, ytop, ybot, top, bot):
    """Vertical pairing ticks where both strands have a base."""
    out = []
    for i, (a, b) in enumerate(zip(top, bot)):
        if a != " " and b != " ":
            cx = x + i * DX + 4
            out.append(line(cx, ytop + 4, cx, ybot - 11, stroke=MUTE, w=1))
    return "".join(out)


def duplex(x, y, top, bot, ltop="5'", rtop="3'", lbot="3'", rbot="5'",
           topfill=TOP, botfill=BOT, show_pairs=True, labels=True):
    """Draw a duplex. top/bot are strings, spaces = no base there."""
    check_pairing(top, bot)
    ytop, ybot = y, y + 30
    s1, w = seq(x, ytop, top, topfill)
    s2, _ = seq(x, ybot, bot, botfill)
    out = [s1, s2]
    if show_pairs:
        out.append(pairs(x, ytop, ybot, top, bot))
    if labels:
        out.append(t(x - 10, ytop, ltop, 13, MUTE, anchor="end"))
        out.append(t(x + w + 8, ytop, rtop, 13, MUTE))
        out.append(t(x - 10, ybot, lbot, 13, MUTE, anchor="end"))
        out.append(t(x + w + 8, ybot, rbot, 13, MUTE))
    return "".join(out), w


def arrow(x1, y, x2, color=HOT, w=1.6, head=5):
    d = 1 if x2 > x1 else -1
    return (line(x1, y, x2 - d * head, y, color, w) +
            f'<path d="M {x2} {y} L {x2 - d*head} {y - head*0.7} L {x2 - d*head} '
            f'{y + head*0.7} Z" fill="{color}"/>')


def brace_label(x, y, text, color=HOT, size=13, anchor="middle"):
    return t(x, y, text, size, color, anchor=anchor)


PROBLEMS = []


def lint(name, content):
    """Catch text that runs off the canvas.

    Figures are checked in and reviewed in a browser, but a browser is not always
    available, so estimate each label's extent and complain if it leaves the box.
    """
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
    W, H = float(m.group(1)), float(m.group(2))
    bad = []
    for mt in re.finditer(r'<text x="([-\d.]+)" y="([-\d.]+)" font-size="([\d.]+)"'
                          r'([^>]*)>([^<]*)</text>', content):
        x, y, size, attrs, txt = (float(mt.group(1)), float(mt.group(2)),
                                  float(mt.group(3)), mt.group(4), mt.group(5))
        w = len(txt) * size * 0.50
        if 'text-anchor="middle"' in attrs:
            x0, x1 = x - w / 2, x + w / 2
        elif 'text-anchor="end"' in attrs:
            x0, x1 = x - w, x
        else:
            x0, x1 = x, x + w
        if x0 < -2 or x1 > W + 2 or y > H or y < 8:
            bad.append(f'    "{txt[:46]}" at x={x:.0f} y={y:.0f} '
                       f'(extends to {x1:.0f}, canvas {W:.0f}x{H:.0f})')
    if bad:
        PROBLEMS.append("  %s\n%s" % (name, "\n".join(bad)))


def fit(content):
    """Widen the canvas so no label is clipped.

    Captions are written as single lines; rather than hand-tuning every canvas,
    measure the labels and grow the box to fit them.
    """
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
    W, H = float(m.group(1)), float(m.group(2))
    need = W
    for mt in re.finditer(r'<text x="([-\d.]+)" y="[-\d.]+" font-size="([\d.]+)"'
                          r'([^>]*)>([^<]*)</text>', content):
        x, size, attrs, txt = (float(mt.group(1)), float(mt.group(2)),
                               mt.group(3), mt.group(4))
        w = len(txt) * size * 0.50
        if 'text-anchor="middle"' in attrs:
            x1 = x + w / 2
        elif 'text-anchor="end"' in attrs:
            x1 = x
        else:
            x1 = x + w
        need = max(need, x1 + 14)
    if need > W:
        content = content.replace(f'viewBox="0 0 {m.group(1)} {m.group(2)}" '
                                  f'width="{m.group(1)}"',
                                  f'viewBox="0 0 {need:.0f} {m.group(2)}" width="{need:.0f}"')
    return content


# ---------------------------------------------------------------- boxes and marks

def box(x, y, w, h, label="", fill="none", stroke=MUTE, size=13, tcol=INK, r=4):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="1.2"/>')
    if label:
        s += t(x + w / 2, y + h / 2 + size * 0.35, label, size, tcol, anchor="middle")
    return s


def dot(x, y, r=5, fill=HOT):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def vtick(x, y0, y1, color=TOP, w=2.2):
    return line(x, y0, x, y1, color, w)


def build(script, figures):
    """Write each figure as figNN-<name>.svg next to the calling script."""
    d = os.path.dirname(os.path.abspath(script))
    for i, (name, fn) in enumerate(figures, start=1):
        fname = "fig%02d-%s.svg" % (i, name)
        content = fit(fn())
        lint(fname, content)
        with open(os.path.join(d, fname), "w") as fh:
            fh.write(content)
        print("wrote", os.path.basename(d) + "/" + fname)
    if PROBLEMS:
        print("\ntext leaves the canvas:")
        print("\n".join(PROBLEMS))
        raise SystemExit(1)
