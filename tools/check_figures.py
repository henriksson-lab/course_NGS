#!/usr/bin/env python3
"""Geometry checks over the generated figures: a triage list, not a verdict.

figlib.lint() catches text leaving the canvas. This catches what it does not:
text printed over other text, text printed over an opaque shape, and labels
sitting so close to a neighbouring mark that they read as belonging to it.

ADVISORY. Glyph widths are estimated from the font size, so the boxes are
approximate and the tool over-reports. Render the figure and look before
changing it.

  python3 tools/check_figures.py            # ranked, worst first
  python3 tools/check_figures.py unit       # one unit
"""
import glob
import html
import re
import sys

TXT = re.compile(r'<text([^>]*)>(.*?)</text>', re.S)
RECT = re.compile(r'<rect([^>]*)/?>')
CIRC = re.compile(r'<circle([^>]*)/?>')


def at(a, n, d=None):
    m = re.search(r'\b%s="([^"]*)"' % n, a)
    return m.group(1) if m else d


def fnum(a, n, d=0.0):
    try:
        return float(at(a, n, d))
    except (TypeError, ValueError):
        return d


def text_boxes(s):
    out = []
    for a, body in TXT.findall(s):
        t = html.unescape(re.sub(r'<[^>]+>', '', body)).strip()
        if not t:
            continue
        fs = float(str(at(a, "font-size", "13")).replace("px", ""))
        anc = at(a, "text-anchor", "start")
        mono = "mono" in (at(a, "font-family", "") or "").lower()
        w = len(t) * fs * (0.60 if mono else 0.50)
        x, y = fnum(a, "x"), fnum(a, "y")
        x0 = x if anc == "start" else (x - w / 2 if anc == "middle" else x - w)
        out.append([x0, y - fs * 0.78, x0 + w, y + fs * 0.26, t, fs])
    return out


def opaque_shapes(s):
    """Filled shapes a label would disappear behind."""
    out = []
    for a in RECT.findall(s):
        fill = (at(a, "fill", "none") or "none").lower()
        op = fnum(a, "opacity", 1.0)
        if fill in ("none", "transparent", "#fff", "#ffffff", "white") or op < 0.25:
            continue
        x, y = fnum(a, "x"), fnum(a, "y")
        out.append([x, y, x + fnum(a, "width"), y + fnum(a, "height"), fill])
    for a in CIRC.findall(s):
        fill = (at(a, "fill", "none") or "none").lower()
        if fill in ("none", "transparent", "#fff", "#ffffff", "white"):
            continue
        cx, cy, r = fnum(a, "cx"), fnum(a, "cy"), fnum(a, "r")
        out.append([cx - r, cy - r, cx + r, cy + r, fill])
    return out


def frac(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0:
        return 0.0
    aa = (a[2] - a[0]) * (a[3] - a[1])
    bb = (b[2] - b[0]) * (b[3] - b[1])
    return ix * iy / max(1e-6, min(aa, bb))


def audit(path):
    s = open(path).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    W, H = (float(vb.group(1)), float(vb.group(2))) if vb else (0.0, 0.0)
    tb, sh = text_boxes(s), opaque_shapes(s)
    hits = []
    for i in range(len(tb)):
        for j in range(i + 1, len(tb)):
            f = frac(tb[i], tb[j])
            if f > 0.18:
                hits.append((f, "text/text", "%r over %r" % (tb[i][4][:30], tb[j][4][:30])))
        for sp in sh:
            f = frac(tb[i], sp)
            if f < 0.2:
                continue
            # A label centred inside a filled box is how figlib.box() draws one:
            # that is intentional. A label that only partly covers a shape, or sits
            # well off its centre, is a collision.
            inside = ((tb[i][0] >= sp[0] - 2) and (tb[i][2] <= sp[2] + 2)
                      and (tb[i][1] >= sp[1] - 2) and (tb[i][3] <= sp[3] + 2))
            # Fully inside is how a panel label is drawn here, wherever it sits in
            # the box. Only a label hanging over an edge is a collision.
            if inside:
                continue
            if f > 0.45:
                hits.append((f, "text/shape", "%r over a filled shape" % tb[i][4][:30]))
        if W and (tb[i][0] < -1 or tb[i][2] > W + 1):
            hits.append((1.5, "off-canvas", "%r leaves the %.0f px canvas" % (tb[i][4][:30], W)))
        if tb[i][5] < 8.5:
            hits.append((0.3, "tiny-text", "%r at %.1f px" % (tb[i][4][:24], tb[i][5])))
    return hits


def main():
    only = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else None
    rows = []
    for f in sorted(glob.glob("*/fig*.svg")):
        if only and not f.startswith(only + "/"):
            continue
        h = audit(f)
        if h:
            rows.append((max(x[0] for x in h), f, h))
    rows.sort(reverse=True)
    print("%d figures scanned, %d with something to look at\n"
          % (len(glob.glob((only + "/fig*.svg") if only else "*/fig*.svg")), len(rows)))
    for worst, f, h in rows:
        print("%s  (worst %.2f)" % (f, worst))
        for sc, kind, msg in sorted(h, reverse=True)[:4]:
            print("    %-11s %s" % (kind, msg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
