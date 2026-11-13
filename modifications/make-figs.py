#!/usr/bin/env python3
"""Figures for the modifications unit.  Run: python3 modifications/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PT, PH, PO = "#e8eef5", "#f5eae6", "#e6f0e8"
FILL = {TOP: PT, BOT: PT, HOT: PH, BAD: PH, OK: PO}

# Long captions below y=100 are wrapped so they do not widen the canvas.
_t, _svg = t, svg
MAXW = 760
_last = [0]


def t(x, y, s, size=15, fill=None, anchor="start", family=None, weight=None, style=None):
    if y < 100 or anchor != "start" or x > 40 or family:
        return _t(x, y, s, size, fill, anchor, family, weight, style)
    lh = size * 1.4
    if y < _last[0] + lh:
        y = _last[0] + lh
    maxc = int((MAXW - x) / (size * 0.5))
    lines, cur = [], ""
    for w in s.split(" "):
        if len(cur) + len(w) + 1 > maxc and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    _last[0] = y + (len(lines) - 1) * lh
    return "".join(_t(x, y + i * lh, ln, size, fill, anchor, family, weight, style)
                   for i, ln in enumerate(lines))


def svg(w, h, body):
    import re as _re
    _last[0] = 0
    ys = [float(m) for m in _re.findall(r'<text x="[-\d.]+" y="([-\d.]+)"', body)]
    return _svg(w, max(h, int(max(ys) + 14)) if ys else h, body)


# ---------------------------------------------------------------- local helpers

def row(x, y, items, arrows=None, cols=None, h=28, size=12.5, gap=30):
    """Boxes joined by labelled arrows. Returns (svg, end x)."""
    out, cx = [], x
    for i, s in enumerate(items):
        w = max(34, len(s) * size * 0.5 + 16)
        c = cols[i] if cols and cols[i] else MUTE
        out.append(box(cx, y, w, h, s, FILL.get(c, "none"), c, size, INK))
        cx += w
        if i < len(items) - 1:
            a = arrows[i] if arrows and arrows[i] else ""
            g = max(gap, len(a) * 5.4 + 16)
            out.append(arrow(cx + 3, y + h / 2, cx + g - 3, MUTE, 1.3, 5))
            if a:
                out.append(t(cx + g / 2, y + h / 2 - 7, a, 10.5, MUTE, anchor="middle"))
            cx += g
    return "".join(out), cx


def table(x, y, colw, rowh, header, rows, size=12.5, colors=None):
    """Plain ruled table. Raises if a cell would not fit its column."""
    out = []
    W = sum(colw)
    out.append(line(x, y, x + W, y, INK, 1.2))
    cy = y + rowh
    allrows = [header] + rows
    for r, cells in enumerate(allrows):
        cx = x
        for c, s in enumerate(cells):
            if len(s) * size * 0.5 > colw[c] - 10:
                raise AssertionError("cell too wide: %r (col %d)" % (s, c))
            col = INK
            if colors and (r - 1, c) in colors and r > 0:
                col = colors[(r - 1, c)]
            out.append(t(cx + 6, cy - rowh * 0.3, s, size, col,
                         weight="bold" if r == 0 else None))
            cx += colw[c]
        out.append(line(x, cy, x + W, cy, MUTE if r else INK, 1.0 if r else 1.2))
        cy += rowh
    return "".join(out), cy - rowh


def card(x, y, w, h, title, lines, col=TOP, size=12):
    out = [box(x, y, w, h, "", FILL.get(col, "none"), col)]
    out.append(t(x + 10, y + 22, title, 13.5, col, weight="bold"))
    for i, s in enumerate(lines):
        if len(s) * size * 0.5 > w - 20:
            raise AssertionError("card line too wide: %r" % s)
        out.append(t(x + 10, y + 44 + i * 18, s, size, INK))
    return "".join(out)


def cseq(x, y, s, cols=None, size=13):
    """Monospace run with per-character colours."""
    out = []
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        c = (cols or {}).get(i, INK)
        out.append(t(x + i * DX, y, ch, size, c, family=MONO))
    return "".join(out)


def hexagon(cx, cy, r):
    pts = []
    for a in (-90, -30, 30, 90, 150, 210):
        pts.append("%.1f,%.1f" % (cx + r * math.cos(math.radians(a)),
                                  cy + r * math.sin(math.radians(a))))
    return '<polygon points="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (" ".join(pts), TOP)


# ---------------------------------------------------------------- DNA methylation

def fig_cytosine_family():
    names = [("C", "H", INK), ("5mC", "CH3", HOT), ("5hmC", "CH2OH", HOT),
             ("5fC", "CHO", HOT), ("5caC", "COOH", HOT)]
    out = [t(30, 26, "Five forms of cytosine. The edge that pairs with guanine is the same in all of them.",
             14, INK)]
    for i, (n, r, col) in enumerate(names):
        cx, cy, rad = 90 + i * 150, 112, 26
        out.append(hexagon(cx, cy, rad))
        out.append(line(cx, cy - rad, cx, cy - rad - 20, col, 2))
        out.append(t(cx, cy - rad - 26, r, 14, col, anchor="middle", weight="bold"))
        out.append(line(cx + rad * 0.866, cy - rad / 2, cx + rad * 0.866 + 16, cy - rad / 2 - 10, TOP, 1.6))
        out.append(t(cx + rad * 0.866 + 18, cy - rad / 2 - 8, "NH2", 11.5, TOP))
        out.append(t(cx, cy + rad + 20, n, 14, col, anchor="middle", weight="bold"))
    out.append(t(30, 196, "Position 5 carries the mark and points away from the base-pairing edge, so a polymerase "
                 "copies every one of them as C.", 13.5, HOT))
    return svg(760, 214, "".join(out))


def fig_bisulfite_chem():
    out = [t(30, 26, "Bisulfite chemistry: only unmethylated cytosine is deaminated.", 14, INK)]
    s, _ = row(30, 50, ["C", "C-6 sulfonate", "U-6 sulfonate", "U", "T"],
               ["HSO3- adds", "deamination", "alkali removes SO3", "PCR copies as"],
               [None, None, None, BAD, BAD])
    out.append(s)
    s, _ = row(30, 118, ["5mC", "slow to sulfonate", "stays 5mC", "C"],
               ["methyl hinders", "(no deamination)", "PCR copies as"],
               [HOT, None, HOT, OK])
    out.append(s)
    out.append(t(30, 184, "Sequence consequence: C in the final read = was methylated; T = was not.",
                 14, HOT))
    return svg(720, 204, "".join(out))


def _bs_read(ref, meth):
    """Bisulfite readout of a top strand: C stays only at methylated CpG."""
    out = []
    for i, ch in enumerate(ref):
        if ch == "C":
            cpg = i + 1 < len(ref) and ref[i + 1] == "G"
            out.append("C" if (cpg and i in meth) else "T")
        else:
            out.append(ch)
    return "".join(out)


def fig_bs_example():
    ref = "ATCGTCCGATACGTTCAG"
    cpgs = [i for i in range(len(ref) - 1) if ref[i:i + 2] == "CG"]
    cells = [("cell 1: all CpG methylated", set(cpgs)),
             ("cell 2: first CpG methylated", {cpgs[0]}),
             ("cell 3: none methylated", set())]
    out = [t(30, 26, "One locus, three cells. After bisulfite and PCR the read says which C were methylated.",
             14, INK)]
    x0 = 210
    out.append(t(x0 - 12, 62, "reference", 12.5, MUTE, anchor="end"))
    out.append(cseq(x0, 62, ref, {i: TOP for i in cpgs} | {i + 1: TOP for i in cpgs}))
    for r, (name, m) in enumerate(cells):
        y = 96 + r * 30
        rd = _bs_read(ref, m)
        out.append(t(x0 - 12, y, name, 12.5, MUTE, anchor="end"))
        cols = {i: HOT for i in range(len(rd)) if rd[i] == "C"}
        out.append(cseq(x0, y, rd, cols))
    out.append(t(x0 + len(ref) * DX + 24, 62, "blue: CpG", 12, TOP))
    out.append(t(x0 + len(ref) * DX + 24, 96, "orange C: kept, so methylated", 12, HOT))
    out.append(t(x0 + len(ref) * DX + 24, 126, "C outside CpG is always read as T", 12, MUTE))
    out.append(t(30, 204, "Reading strand-by-strand, the methylation level of a CpG is C / (C + T) over all reads at it.",
                 13.5, INK))
    return svg(780, 222, "".join(out))


def fig_bs_adapter():
    ad = "ACACGACGCTCTTCCGATCT"
    conv = ad.replace("C", "T")
    out = [t(30, 26, "Adapters ligated before bisulfite must survive it.", 14, INK)]
    out.append(t(30, 66, "unmethylated adapter", 12.5, MUTE))
    out.append(cseq(190, 66, ad))
    out.append(t(190 + len(ad) * DX + 18, 66, "after bisulfite:", 12.5, MUTE))
    out.append(cseq(190 + len(ad) * DX + 120, 66, conv, {i: BAD for i, c in enumerate(ad) if c == "C"}))
    out.append(t(190, 90, "every C became T: the primer no longer matches, and the library cannot be amplified",
                 12.5, BAD))
    out.append(t(30, 134, "5mC-containing adapter", 12.5, MUTE))
    out.append(cseq(190, 134, ad, {i: HOT for i, c in enumerate(ad) if c == "C"}))
    out.append(t(190 + len(ad) * DX + 18, 134, "after bisulfite:", 12.5, MUTE))
    out.append(cseq(190 + len(ad) * DX + 120, 134, ad, {i: HOT for i, c in enumerate(ad) if c == "C"}))
    out.append(t(190, 158, "5-methylcytosine resists conversion, so the adapter reads the same before and after",
                 12.5, OK))
    out.append(t(30, 204, "Consequence: the adapter's C positions carry no information, and the insert is flanked by "
                 "sequence that is deliberately 'methylated'.", 13.5, INK))
    return svg(800, 222, "".join(out))


def fig_bs_threeletter():
    a, b = "GTCCATTCAG", "GTTTATTTAG"
    ca, cb = a.replace("C", "T"), b.replace("C", "T")
    assert ca == cb
    out = [t(30, 26, "After conversion, two different loci can have the same sequence.", 14, INK)]
    out.append(t(30, 66, "locus X (genome)", 12.5, MUTE))
    out.append(cseq(190, 66, a, {i: HOT for i, c in enumerate(a) if c == "C"}))
    out.append(t(30, 96, "locus Y (genome)", 12.5, MUTE))
    out.append(cseq(190, 96, b))
    out.append(arrow(340, 66, 400, MUTE))
    out.append(t(410, 66, "X, all C unmethylated:", 12.5, MUTE))
    out.append(cseq(570, 66, ca, {i: HOT for i, c in enumerate(a) if c == "C"}))
    out.append(t(410, 96, "Y, unchanged:", 12.5, MUTE))
    out.append(cseq(570, 96, cb))
    out.append(t(30, 150, "The aligner converts reads and genome in silico (C to T on one strand, G to A on the other) "
                 "and aligns in a three-letter alphabet.", 13.5, INK))
    out.append(t(30, 172, "Fewer letters means less unique sequence: repeats multiply, mapping rates fall, and "
                 "some loci can no longer be told apart.", 13.5, HOT))
    return svg(780, 192, "".join(out))


def fig_readout_matrix():
    hdr = ["method", "unmodified C", "5mC", "5hmC", "a C in the read marks"]
    rows = [["BS-seq", "T", "C", "C", "5mC or 5hmC"],
            ["oxBS-seq", "T", "C", "T", "5mC only"],
            ["TAB-seq", "T", "T", "C", "5hmC only"],
            ["EM-seq", "T", "C", "C", "5mC or 5hmC"],
            ["TAPS", "C", "T", "T", "unmodified C"],
            ["TAPS with beta-glucosyltransferase", "C", "T", "C", "unmodified C and 5hmC"]]
    colors = {}
    for r, rw in enumerate(rows):
        for c in (1, 2, 3):
            colors[(r, c)] = HOT if rw[c] == "C" else TOP
    s, _ = table(30, 40, [250, 110, 70, 70, 220], 30, hdr, rows, 13, colors)
    out = [t(30, 26, "What each base reads as in the sequence data after the method has been applied.", 14, INK), s]
    out.append(t(30, 40 + 30 * 7 + 22, "Subtract oxBS from BS and what is left is 5hmC. TAPS inverts the logic: the "
                 "modified base is the one that changes.", 13.5, INK))
    return svg(780, 40 + 30 * 7 + 40, "".join(out))


def fig_oxbs_tab():
    out = [t(30, 24, "Two ways to tell 5hmC from 5mC while keeping bisulfite as the final step.", 14, INK)]
    out.append(t(30, 52, "oxBS-seq", 13.5, TOP, weight="bold"))
    s, _ = row(30, 62, ["5mC", "KRuO4 oxidation: no effect", "5mC", "reads as C"],
               ["", "bisulfite", ""], [HOT, None, HOT, OK], size=12)
    out.append(s)
    s, _ = row(30, 100, ["5hmC", "KRuO4 oxidation: becomes 5fC", "5fC", "reads as T"],
               ["", "bisulfite deaminates", ""], [HOT, None, BAD, BAD], size=12)
    out.append(s)
    out.append(t(30, 168, "TAB-seq", 13.5, TOP, weight="bold"))
    s, _ = row(30, 178, ["5hmC", "beta-glucosyltransferase: protected", "5gmC", "reads as C"],
               ["", "TET, bisulfite", ""], [HOT, None, HOT, OK], size=12)
    out.append(s)
    s, _ = row(30, 216, ["5mC", "TET oxidises: becomes 5caC", "5caC", "reads as T"],
               ["", "bisulfite deaminates", ""], [HOT, None, BAD, BAD], size=12)
    out.append(s)
    return svg(820, 258, "".join(out))


def fig_emseq():
    out = [t(30, 24, "EM-seq replaces the harsh chemistry with enzymes. The deaminase only sees what was left unprotected.",
             14, INK)]
    heads = ["", "1. TET2 and T4-BGT", "2. APOBEC deaminase", "3. PCR"]
    rows = [("C", [("C", None), ("C", None), ("U", BAD), ("T", BAD)]),
            ("5mC", [("5mC", HOT), ("5caC", HOT), ("5caC", HOT), ("C", OK)]),
            ("5hmC", [("5hmC", HOT), ("5gmC", HOT), ("5gmC", HOT), ("C", OK)])]
    xs = [60, 170, 330, 490]
    for j, h in enumerate(heads):
        if h:
            out.append(t(xs[j] + 20, 52, h, 12.5, MUTE))
    for r, (name, cells) in enumerate(rows):
        y = 66 + r * 40
        out.append(t(30, y + 19, name, 13, INK, anchor="start", weight="bold"))
        for j, (lab, col) in enumerate(cells):
            x = xs[j] + 20
            out.append(box(x, y, 70, 28, lab, FILL.get(col, "none"), col or MUTE, 12.5, INK))
            if j < 3:
                out.append(arrow(x + 74, y + 14, xs[j + 1] + 16, MUTE, 1.2, 5))
    out.append(t(30, 204, "No strand breakage and no conversion of 5mC: longer fragments, better coverage of GC-rich "
                 "DNA, usable at lower input.", 13.5, OK))
    return svg(720, 222, "".join(out))


def fig_taps():
    out = [t(30, 24, "TAPS: oxidise the modified bases, then reduce them to a base that PCR reads as T.", 14, INK)]
    xs = [60, 190, 350, 510]
    heads = ["", "1. TET oxidation", "2. pyridine borane", "3. PCR"]
    rows = [("C", [("C", None), ("C", None), ("C", None), ("C", OK)]),
            ("5mC", [("5mC", HOT), ("5caC", HOT), ("DHU", BAD), ("T", BAD)]),
            ("5hmC", [("5hmC", HOT), ("5caC", HOT), ("DHU", BAD), ("T", BAD)])]
    for j, h in enumerate(heads):
        if h:
            out.append(t(xs[j] + 20, 52, h, 12.5, MUTE))
    for r, (name, cells) in enumerate(rows):
        y = 66 + r * 40
        out.append(t(30, y + 19, name, 13, INK, weight="bold"))
        for j, (lab, col) in enumerate(cells):
            x = xs[j] + 20
            out.append(box(x, y, 70, 28, lab, FILL.get(col, "none"), col or MUTE, 12.5, INK))
            if j < 3:
                out.append(arrow(x + 74, y + 14, xs[j + 1] + 16, MUTE, 1.2, 5))
    out.append(t(30, 204, "Only the minority of bases (modified C) are changed, and the DNA is not degraded. "
                 "DHU: dihydrouracil.", 13.5, OK))
    return svg(720, 222, "".join(out))


def fig_spikein():
    out = [t(30, 26, "Spike-in controls: unmethylated lambda DNA measures how much unmethylated C survives as C.",
             14, INK)]
    nonconv = 0.005
    out.append(t(30, 52, "Suppose 0.5% of unmethylated C stays C (conversion 99.5%).", 13, MUTE))
    out.append(t(30, 76, "true level", 12, MUTE))
    out.append(t(150, 76, "apparent level", 12, MUTE))
    for i, tr in enumerate([0.02, 0.20, 0.80]):
        ap = tr + (1 - tr) * nonconv
        y = 90 + i * 34
        out.append(t(30, y + 14, "%d%%" % round(tr * 100), 12.5, INK))
        out.append(f'<rect x="150" y="{y}" width="{tr * 400:.1f}" height="11" fill="{TOP}"/>')
        out.append(f'<rect x="150" y="{y + 13}" width="{ap * 400:.1f}" height="11" fill="{HOT}"/>')
        out.append(t(150 + ap * 400 + 8, y + 22, "%.1f%%" % (ap * 100), 12, HOT))
    out.append(t(30, 206, "At a 2% site the error is a quarter of the signal; at 80% it hardly matters. "
                 "The same control in reverse (CpG-methylated pUC19) checks that protection worked.", 13.5, INK))
    return svg(780, 224, "".join(out))


def fig_rrbs():
    import random
    rnd = random.Random(7)
    xs = [40]
    # islands: dense CCGG; elsewhere sparse
    for x in range(40, 700):
        pass
    sites = []
    for a, b, step in [(40, 110, 70), (110, 170, 11), (170, 330, 78), (330, 420, 14),
                       (420, 560, 62), (560, 640, 12), (640, 700, 66)]:
        x = a + rnd.randint(2, 6)
        while x < b:
            sites.append(x)
            x += step + rnd.randint(-3, 3)
    out = [t(30, 26, "RRBS: MspI cuts C^CGG whatever the methylation, so fragment ends sit in CpG-rich DNA.", 14, INK)]
    out.append(line(40, 70, 700, 70, MUTE, 3))
    for s in sites:
        out.append(vtick(s, 56, 84, TOP, 1.6))
    out.append(t(40, 48, "genome (CCGG sites in blue)", 12, MUTE))
    out.append(t(75, 104, "CpG island", 11.5, HOT, anchor="middle"))
    out.append(t(375, 104, "CpG island", 11.5, HOT, anchor="middle"))
    out.append(t(600, 104, "CpG island", 11.5, HOT, anchor="middle"))
    out.append(t(40, 138, "fragments (kept = 40-220 bp by size selection; 5 bp per pixel here)", 12, MUTE))
    edges = [40] + sites + [700]
    for i in range(len(edges) - 1):
        L = (edges[i + 1] - edges[i]) * 5
        keep = 40 <= L <= 220
        out.append(f'<rect x="{edges[i] + 1}" y="150" width="{edges[i + 1] - edges[i] - 2}" height="14" '
                   f'fill="{OK if keep else "#d8dbde"}"/>')
    out.append(t(40, 196, "Green fragments go to the library. Most of the genome is long fragments and never "
                 "sequenced, which is the point: a few percent of the genome, yet it still includes most CpG islands.", 13, INK))
    return svg(760, 214, "".join(out))


# ---------------------------------------------------------------- damage

def _piece(x, y, w, capL=None, capR=None, faded=False, tcol=TOP, bcol=BOT):
    c1, c2 = ("#c9cdd1", "#c9cdd1") if faded else (tcol, bcol)
    out = [line(x, y, x + w, y, c1, 2.4, cap="butt"), line(x, y + 7, x + w, y + 7, c2, 2.4, cap="butt")]
    for cap, xx, d in ((capL, x, -1), (capR, x + w, 1)):
        if cap:
            out.append(f'<rect x="{xx + (0 if d > 0 else -12)}" y="{y - 3}" width="12" height="13" '
                       f'fill="{cap}" opacity="0.9"/>')
    return "".join(out)


def fig_endseq():
    out = [t(30, 22, "END-seq: the first adapter goes on in the agarose plug, before any fragmenting.", 14, INK)]
    px = [30, 190, 350, 510, 670]
    titles = ["1. cells in agarose", "2. blunt, A-tail, hairpin 1", "3. sonicate", "4. streptavidin",
              "5. hairpin 2, USER, PCR"]
    for i, ttl in enumerate(titles):
        out.append(t(px[i], 46, ttl, 12.5, INK, weight="bold"))
    # 1: break
    out.append(_piece(px[0], 84, 55) + _piece(px[0] + 75, 84, 55))
    out.append(t(px[0] + 65, 118, "break", 11.5, HOT, anchor="middle"))
    # 2
    out.append(_piece(px[1], 84, 50, capR=HOT) + _piece(px[1] + 84, 84, 50, capL=HOT))
    out.append(dot(px[1] + 56, 79, 3.5, BAD) + dot(px[1] + 78, 79, 3.5, BAD))
    out.append(t(px[1] + 67, 118, "biotin", 11.5, BAD, anchor="middle"))
    # 3
    out.append(_piece(px[2], 84, 30, capR=HOT) + _piece(px[2] + 34, 84, 22) + _piece(px[2] + 76, 84, 22)
               + _piece(px[2] + 102, 84, 28, capL=HOT))
    out.append(t(px[2] + 65, 118, "new ends, no biotin", 11.5, MUTE, anchor="middle"))
    # 4
    out.append(_piece(px[3], 74, 30, capR=HOT) + _piece(px[3] + 80, 74, 28, capL=HOT))
    out.append(_piece(px[3] + 34, 100, 22, faded=True) + _piece(px[3] + 60, 100, 22, faded=True))
    out.append(t(px[3] + 65, 134, "unlabelled pieces washed off", 11.5, MUTE, anchor="middle"))
    # 5
    out.append(_piece(px[4], 84, 40, capL=HOT, capR=OK) + _piece(px[4] + 66, 84, 40, capL=OK, capR=HOT))
    out.append(t(px[4] + 65, 118, "read 1 starts at the break", 11.5, HOT, anchor="middle"))
    out.append(t(30, 172, "Each library molecule has the break on one end (hairpin 1, orange) and a random sonication end on the "
                 "other (hairpin 2, green).", 13.5, INK))
    out.append(t(30, 194, "Without biotin selection, sonication ends outnumber breaks by many orders of magnitude.", 13.5, HOT))
    return svg(830, 212, "".join(out))


def fig_resection():
    out = [t(30, 18, "Resection moves the end away from the break. END-seq reads start at the end that is left.", 14, INK)]
    bx0 = 340
    out.append(line(bx0, 50, bx0, 130, HOT, 1.2, dash="4 3"))
    out.append(t(bx0, 44, "original break", 11.5, HOT, anchor="middle"))
    # processed ends
    out.append(t(30, 66, "after resection", 12, MUTE))
    out.append(line(40, 70, 340, 70, TOP, 2.4, cap="butt") + line(40, 78, 260, 78, BOT, 2.4, cap="butt"))
    out.append(line(340, 70, 640, 70, TOP, 2.4, cap="butt") if False else "")
    out.append(line(420, 70, 640, 70, TOP, 2.4, cap="butt") + line(340, 78, 640, 78, BOT, 2.4, cap="butt"))
    out.append(t(300, 98, "3' overhang", 11, MUTE, anchor="middle"))
    out.append(t(380, 98, "3' overhang", 11, MUTE, anchor="middle"))
    # trimmed
    out.append(t(30, 150, "ExoVII + ExoT remove the overhang", 12, MUTE))
    out.append(line(40, 156, 260, 156, TOP, 2.4, cap="butt") + line(40, 164, 260, 164, BOT, 2.4, cap="butt"))
    out.append(line(420, 156, 640, 156, TOP, 2.4, cap="butt") + line(420, 164, 640, 164, BOT, 2.4, cap="butt"))
    out.append(arrow(258, 186, 170, HOT, 2))
    out.append(arrow(422, 186, 510, HOT, 2))
    out.append(t(215, 206, "read 1", 12, HOT, anchor="middle"))
    out.append(t(465, 206, "read 1", 12, HOT, anchor="middle"))
    out.append(line(260, 176, 260, 224, MUTE, 1, dash="2 3") + line(420, 176, 420, 224, MUTE, 1, dash="2 3"))
    out.append(line(262, 222, 418, 222, OK, 1.6))
    out.append(t(340, 240, "gap = resected DNA on both sides", 12, OK, anchor="middle"))
    return svg(700, 252, "".join(out))


def fig_guideseq():
    out = [t(30, 22, "GUIDE-seq: a blunt double-stranded tag integrates into breaks in living cells and marks them.",
             14, INK)]
    out.append(line(40, 62, 700, 62, MUTE, 3))
    for x, lab in [(150, "on-target"), (360, "off-target 1"), (560, "off-target 2")]:
        out.append(box(x - 8, 55, 16, 14, "", PH, HOT))
        out.append(t(x, 46, lab, 11.5, HOT, anchor="middle"))
    out.append(t(40, 92, "Cas9 + guide cut; the dsODN tag (orange) is joined into each break by NHEJ", 12, MUTE))
    out.append(t(40, 128, "shear, ligate adapters, PCR from the tag outward:", 12.5, INK, weight="bold"))
    out.append(line(60, 160, 200, 160, TOP, 3) + line(290, 160, 430, 160, TOP, 3))
    out.append(box(200, 152, 90, 16, "tag", PH, HOT, 12))
    out.append(arrow(196, 182, 70, TOP, 1.8))
    out.append(arrow(294, 182, 420, TOP, 1.8))
    out.append(t(133, 200, "read into genome", 11.5, TOP, anchor="middle"))
    out.append(t(357, 200, "read into genome", 11.5, TOP, anchor="middle"))
    out.append(t(480, 150, "Only molecules that contain the tag", 12.5, INK))
    out.append(t(480, 168, "are amplified: background cuts and", 12.5, INK))
    out.append(t(480, 186, "unbroken DNA give nothing.", 12.5, INK))
    return svg(740, 216, "".join(out))


def fig_offtarget_handles():
    out = [t(30, 22, "Three ways of finding where a nuclease cuts. Each one has a different handle.", 14, INK)]
    out.append(card(30, 38, 245, 150, "GUIDE-seq", ["where: living cells", "handle: dsODN integrated at breaks",
                                                    "needs: transfection of the tag", "misses: cells that do not take",
                                                    "up the tag; tag bias at sites"], TOP))
    out.append(card(285, 38, 245, 150, "CHANGE-seq", ["where: naked genomic DNA", "handle: circle opened by Cas9",
                                                       "needs: no cells at all", "misses: chromatin context,",
                                                       "so reports potential sites"], HOT))
    out.append(card(540, 38, 245, 150, "DISCOVER-seq", ["where: cells or tissue in vivo", "handle: MRE11 ChIP-seq",
                                                         "needs: no tag, no delivery", "misses: sites repaired before",
                                                         "the factor is captured"], OK))
    return svg(800, 206, "".join(out))


def fig_repair_outcomes():
    L, M, X, R = "TCAGGCTA", "TGAC", "GGCCAT", "AACGTCTA"
    ref = L + M + X + M + R
    cut = len(L + M) + 3
    dele = L + M + R
    ins = (L + M + X[:3] + "T" + X[3:] + M + R)
    mh = set(range(len(L), len(L + M))) | set(range(len(L + M + X), len(L + M + X + M)))
    out = [t(30, 24, "The same cut, different repair. Microhomology (orange) on both sides lets one copy and the DNA between be lost.",
             14, INK)]
    x0 = 230
    out.append(t(x0 - 12, 62, "intact target", 12.5, MUTE, anchor="end"))
    out.append(cseq(x0, 62, ref, {i: HOT for i in mh}))
    out.append(line(x0 + cut * DX - 1, 44, x0 + cut * DX - 1, 72, BAD, 1.6))
    out.append(t(x0 + cut * DX, 40, "Cas9 cut", 11.5, BAD, anchor="middle"))
    out.append(t(x0 - 12, 104, "end joining, +1 base", 12.5, MUTE, anchor="end"))
    cols = {len(L + M + X[:3]): BAD} | {i: HOT for i in range(len(L), len(L + M))} | \
           {i + 1: HOT for i in range(len(L + M + X) , len(L + M + X + M))}
    out.append(cseq(x0, 104, ins, cols))
    out.append(t(x0 - 12, 146, "microhomology-mediated", 12.5, MUTE, anchor="end"))
    out.append(cseq(x0, 146, dele, {i: HOT for i in range(len(L), len(L + M))}))
    out.append(t(x0 + len(dele) * DX + 14, 146, "%d bp deleted" % (len(ref) - len(dele)), 12.5, BAD))
    out.append(t(x0 - 12, 188, "perfect re-joining", 12.5, MUTE, anchor="end"))
    out.append(cseq(x0, 188, ref, {i: HOT for i in mh}))
    out.append(t(x0 + len(ref) * DX + 14, 188, "invisible: the cut can recur", 12.5, MUTE))
    out.append(t(30, 226, "The amplicon spectrum is a readout of which repair pathway acted.", 13.5, INK))
    return svg(820, 244, "".join(out))


def fig_repair_seq():
    out = [t(30, 22, "Repair-seq: knock down one repair gene per cell, cut one fixed site, read the outcomes.", 14, INK)]
    s, _ = row(30, 40, ["pool of cells, one knockdown each", "Cas9 cuts the same target",
                        "amplicon: knockdown barcode + outcome"], ["", ""], [TOP, HOT, OK], size=12)
    out.append(s)
    cols = [("control", [0.55, 0.30, 0.15]), ("knockdown A", [0.20, 0.55, 0.25]),
            ("knockdown B", [0.70, 0.10, 0.20])]
    out.append(t(30, 104, "outcome spectrum per knockdown (schematic)", 12.5, MUTE))
    for i, (n, v) in enumerate(cols):
        x = 40 + i * 120
        y = 112
        for j, f in enumerate(v):
            c = [HOT, TOP, "#c9cdd1"][j]
            out.append(f'<rect x="{x}" y="{y}" width="60" height="{f * 90:.0f}" fill="{c}"/>')
            y += f * 90
        out.append(t(x + 30, 222, n, 11.5, INK, anchor="middle"))
    out.append(f'<rect x="440" y="116" width="12" height="12" fill="{HOT}"/>')
    out.append(t(458, 127, "short insertions", 12, INK))
    out.append(f'<rect x="440" y="138" width="12" height="12" fill="{TOP}"/>')
    out.append(t(458, 149, "deletions with microhomology", 12, INK))
    out.append(f'<rect x="440" y="160" width="12" height="12" fill="#c9cdd1"/>')
    out.append(t(458, 171, "other / unedited", 12, INK))
    out.append(t(440, 200, "A change in the mix, not the total, tells you", 12, INK))
    out.append(t(440, 218, "what the knocked-down gene does.", 12, INK))
    return svg(720, 240, "".join(out))


def fig_repli_seq():
    out = [t(30, 22, "Repli-seq: label new DNA with BrdU, sort cells by position in S phase, sequence the labelled DNA.",
             14, INK)]
    # cell cycle bar
    out.append(box(40, 40, 120, 26, "G1", "none", MUTE))
    out.append(box(160, 40, 140, 26, "early S", PH, HOT))
    out.append(box(300, 40, 140, 26, "late S", PT, TOP))
    out.append(box(440, 40, 100, 26, "G2/M", "none", MUTE))
    out.append(t(230, 86, "BrdU pulse, then sort by DNA content", 11.5, MUTE, anchor="middle"))
    # profile
    out.append(line(40, 220, 540, 220, MUTE, 1.2))
    vals = [0.8, 0.9, 1.0, 0.9, 0.2, -0.7, -0.9, -0.8, -0.3, 0.6, 0.9, 1.0, 0.7, 0.0, -0.8, -1.0, -0.9, -0.2, 0.7, 0.9]
    pts = []
    for i, v in enumerate(vals):
        pts.append("%.0f,%.0f" % (40 + i * 25.5, 175 - v * 40))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="2"/>')
    out.append(line(40, 175, 540, 175, MUTE, 1, dash="3 3"))
    out.append(t(34, 179, "0", 11.5, MUTE, anchor="end"))
    out.append(t(580, 134, "log2(early / late)", 12.5, INK))
    out.append(t(120, 128, "early-replicating domain", 11.5, HOT, anchor="middle"))
    out.append(t(210, 232, "late-replicating domain", 11.5, TOP, anchor="middle"))
    out.append(t(40, 252, "chromosome position", 11.5, MUTE))
    out.append(t(580, 156, "Domains of hundreds of kb to Mb;", 12, INK))
    out.append(t(580, 172, "stable between cell types, with", 12, INK))
    out.append(t(580, 188, "differentiation-linked exceptions.", 12, INK))
    return svg(800, 264, "".join(out))


def fig_repli_order():
    out = [t(30, 22, "E/L Repli-seq builds the library first and selects the labelled DNA afterwards.", 14, INK)]
    s, _ = row(30, 40, ["sorted early or late S cells", "lyse, sonicate", "end-prep, ligate adapter, USER"],
               ["", ""], [TOP, None, OK], size=12)
    out.append(s)
    s, _ = row(30, 100, ["denature", "anti-BrdU immunoprecipitation", "release, index PCR"],
               ["", ""], [None, HOT, OK], size=12)
    out.append(s)
    out.append(t(30, 168, "Why this order: BrdU is only a handle for pulling DNA down. The adapters are already on, so the", 13, INK))
    out.append(t(30, 186, "pulled-down strands can be amplified directly. Adapters cannot easily be added to single-stranded DNA.", 13, INK))
    return svg(780, 206, "".join(out))


def fig_cn_timing():
    out = [t(30, 22, "No label needed: in S phase, early-replicating DNA has already been copied, so its copy number is higher.",
             14, INK)]
    regs = [(90, 140, "early", HOT), (230, 140, "late", TOP), (370, 140, "early", HOT), (510, 140, "late", TOP)]
    out.append(t(30, 62, "G1", 12.5, INK, weight="bold"))
    out.append(t(30, 128, "mid-S", 12.5, INK, weight="bold"))
    for x, w, n, c in regs:
        out.append(t(x + w / 2, 46, n, 11.5, c, anchor="middle"))
        out.append(line(x, 60, x + w - 8, 60, MUTE, 3, cap="butt") + line(x, 68, x + w - 8, 68, MUTE, 3, cap="butt"))
        k = 4 if n == "early" else 2
        for j in range(k):
            out.append(line(x, 110 + j * 8, x + w - 8, 110 + j * 8, c, 3, cap="butt"))
    out.append(t(30, 196, "Coverage ratio S / G1: about 2 in early regions, about 1 in late regions.", 13.5, INK))
    out.append(t(30, 218, "Single cells work the same way: one S-phase cell gives a binary early/late map per bin.", 13.5, INK))
    return svg(720, 236, "".join(out))


def fig_summary():
    hdr = ["question", "the handle", "protocols"]
    rows = [["Which C is methylated?", "a base change that depends on the mark", "BS-seq, EM-seq, TAPS"],
            ["5mC or 5hmC?", "protect one, convert the other", "oxBS-seq, TAB-seq"],
            ["Which CpG, cheaply?", "restriction enzyme enrichment", "RRBS"],
            ["Where is DNA broken?", "the free end is the handle", "END-seq, BLESS"],
            ["Where does a nuclease cut?", "tag the break, or open a circle", "GUIDE-seq, CHANGE-seq"],
            ["How was it repaired?", "sequence across the cut", "Repair-seq"],
            ["When does it replicate?", "label the new strand, or count copies", "E/L Repli-seq"]]
    s, _ = table(30, 40, [230, 330, 250], 30, hdr, rows, 13)
    return svg(860, 40 + 30 * 8 + 14, t(30, 26, "Every method is a way of turning a chemical difference into a sequence difference.", 14, INK) + s)


# ================================================================ RNA deck

def fig_marks_rt():
    hdr = ["mark", "what reverse transcriptase does", "what you can do about it"]
    rows = [["m6A", "copies it as A (reads straight through)", "antibody, or chemistry that treats A and m6A differently"],
            ["inosine (A-to-I)", "copies it as G", "read the A-to-G mismatch directly"],
            ["m5C", "copies it as C", "bisulfite works on RNA as on DNA"],
            ["pseudouridine", "copies it as U", "chemical adduct that stops the enzyme"],
            ["m1A", "stalls or misreads (blocks pairing)", "use the stop or the mismatch"]]
    colors = {(1, 0): HOT, (4, 0): HOT}
    s, _ = table(30, 40, [150, 330, 440], 30, hdr, rows, 12.5, colors)
    return svg(960, 40 + 30 * 6 + 40, t(30, 26, "RNA marks are mostly silent to the enzyme that makes the library.", 14, INK) + s
               + t(30, 40 + 30 * 6 + 24, "Orange: marks that show up without any special treatment.", 13, HOT))


def fig_m6a_seq():
    out = [t(30, 22, "m6A-seq (MeRIP): fragment the RNA, pull down m6A-containing pieces, compare with the input.", 14, INK)]
    out.append(line(40, 70, 700, 70, INK, 2.4))
    for x, w in [(40, 140), (230, 190), (480, 220)]:
        out.append(f'<rect x="{x}" y="62" width="{w}" height="16" fill="#dfe3e6" stroke="{MUTE}"/>')
    out.append(t(40, 52, "transcript (exons grey)", 11.5, MUTE))
    for x in (385, 640):
        out.append(dot(x, 70, 5, HOT))
    out.append(t(390, 54, "m6A", 11.5, HOT, anchor="middle"))
    out.append(t(645, 54, "m6A", 11.5, HOT, anchor="middle"))
    # tracks
    out.append(t(40, 112, "input", 12, INK))
    out.append(f'<polyline points="40,150 700,150" stroke="{MUTE}" stroke-width="1"/>')
    pts = []
    for i in range(0, 661, 10):
        x = 40 + i
        pts.append("%d,%.1f" % (x, 148 - 10 - 4 * math.sin(i / 25)))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{MUTE}" stroke-width="2"/>')
    out.append(t(40, 172, "IP (anti-m6A)", 12, INK))
    out.append(f'<polyline points="40,214 700,214" stroke="{MUTE}" stroke-width="1"/>')
    pts = []
    for i in range(0, 661, 10):
        x = 40 + i
        y = 212 - 10 - 4 * math.sin(i / 25) - 34 * math.exp(-((x - 385) / 28) ** 2) - 28 * math.exp(-((x - 640) / 28) ** 2)
        pts.append("%d,%.1f" % (x, y))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{HOT}" stroke-width="2"/>')
    out.append(t(385, 236, "peak, about 100-200 nt wide", 11.5, HOT, anchor="middle"))
    out.append(t(40, 262, "The peak is as wide as the fragments, so the antibody locates a region, not a nucleotide.", 13.5, INK))
    return svg(740, 280, "".join(out))


def fig_miclip():
    out = [t(30, 22, "miCLIP: UV crosslinks the antibody to the m6A, so reverse transcription leaves a mark at the site.", 14, INK)]
    rna = "GGACUAGC"
    out.append(t(30, 66, "RNA, 5' to 3'", 12.5, MUTE))
    cols = {2: HOT}
    out.append(cseq(190, 66, rna, cols))
    out.append(t(190 + 2 * DX + 4, 46, "m6A", 11.5, HOT, anchor="middle"))
    out.append(t(190 + 2 * DX + 4, 90, "crosslinked antibody fragment", 11.5, HOT))
    out.append(t(30, 134, "truncation", 12.5, INK, weight="bold"))
    out.append(arrow(190 + 8 * DX, 130, 190 + 3 * DX - 6, TOP, 2))
    out.append(t(190 + 8 * DX + 14, 134, "cDNA stops at the adduct; read starts one base downstream", 12, MUTE))
    out.append(t(30, 176, "mutation", 12.5, INK, weight="bold"))
    mut = "GGACUAGC"
    out.append(cseq(190, 176, "GGAUUAGC", {3: BAD}))
    out.append(t(190 + 8 * DX + 14, 176, "read-through with C changed to T at the +1 position", 12, MUTE))
    out.append(t(30, 218, "Both marks are scored against a motif: m6A lives in DRACH sequences, so a call away from one is suspect.",
                 13.5, INK))
    return svg(820, 236, "".join(out))


def fig_clip_flow():
    out = [t(30, 22, "The CLIP family: freeze the protein on the RNA, then read the footprint.", 14, INK)]
    s, _ = row(30, 40, ["UV crosslink in cells", "lyse, trim RNA", "immunoprecipitate protein",
                        "ligate 3' adapter"], ["", "", ""], [TOP, None, None, OK], size=12)
    out.append(s)
    s, _ = row(30, 100, ["gel, cut RNA-protein band", "proteinase K", "reverse transcribe", "5' adapter, PCR"],
               ["", "", ""], [None, HOT, HOT, OK], size=12)
    out.append(s)
    out.append(t(30, 164, "UV makes a zero-length bond, so only RNA touching the protein survives the washes. Proteinase K leaves",
                 13, INK))
    out.append(t(30, 183, "a peptide stub on the nucleotide that was crosslinked, and that stub is what the enzyme reacts to.",
                 13, INK))
    return svg(800, 202, "".join(out))


def fig_trunc_vs_mut():
    out = [t(30, 22, "Two ways the crosslink shows in the reads. Orange marks the crosslinked nucleotide.", 14, INK)]
    ref = "UUGUGAUCUUAG"
    x0 = 200
    k = 6
    out.append(t(30, 56, "iCLIP: truncation", 12.5, INK, weight="bold"))
    out.append(cseq(x0, 56, ref, {k: HOT}))
    for i, (st, en) in enumerate([(k + 1, 12), (k + 1, 11), (k + 1, 10)]):
        y = 70 + i * 10
        out.append(f'<rect x="{x0 + st * DX}" y="{y}" width="{(en - st) * DX}" height="6" fill="{TOP}"/>')
    out.append(t(x0 + 12 * DX + 18, 86, "all reads start one base after the crosslink", 12, MUTE))
    out.append(t(30, 142, "PAR-CLIP: mutation", 12.5, INK, weight="bold"))
    ref2 = "UUGUGAUUUUAG"
    out.append(cseq(x0, 142, ref2, {k: HOT}))
    for i, (st, en) in enumerate([(2, 10), (3, 12), (4, 9)]):
        y = 156 + i * 10
        out.append(f'<rect x="{x0 + st * DX}" y="{y}" width="{(en - st) * DX}" height="6" fill="{TOP}"/>')
        out.append(f'<rect x="{x0 + k * DX}" y="{y - 1}" width="{DX}" height="8" fill="{BAD}"/>')
    out.append(t(x0 + 12 * DX + 18, 172, "T to C in every read that covers the 4-thiouridine", 12, MUTE))
    out.append(t(30, 210, "Truncation needs the enzyme to stop and the library to keep the truncated molecules.", 13.5, INK))
    out.append(t(30, 230, "Mutation needs the enzyme to read through and miscopy. The two are often both present.", 13.5, INK))
    return svg(780, 246, "".join(out))


def fig_eclip():
    out = [t(30, 22, "eCLIP: every IP gets a size-matched input from the same lysate, so background can be subtracted.", 14, INK)]
    out.append(t(30, 56, "IP", 13, INK, weight="bold"))
    s, _ = row(60, 40, ["anti-protein IP", "3' adapter on bead", "gel, membrane", "RT"], ["", "", ""],
               [HOT, None, None, None], size=12)
    out.append(s)
    out.append(t(30, 112, "input", 13, INK, weight="bold"))
    s, _ = row(80, 96, ["2% of lysate", "same gel region as IP", "3' adapter", "RT"], ["", "", ""],
               [TOP, None, None, None], size=12)
    out.append(s)
    s, _ = row(30, 152, ["ligate 5' adapter to the cDNA", "PCR", "peaks = IP over input"], ["", ""],
               [OK, OK, OK], size=12)
    out.append(s)
    out.append(t(30, 212, "The input shows what is abundant and sticky in that gel region, so a peak must beat it.", 13.5, INK))
    return svg(800, 232, "".join(out))


def fig_labelling():
    out = [t(30, 22, "Metabolic labelling: add 4-thiouridine (4sU) for a short time; only RNA made in that window carries it.", 14, INK)]
    out.append(t(30, 54, "enrich", 13, HOT, weight="bold"))
    s, _ = row(30, 62, ["4sU pulse", "extract, fragment", "biotinylate the thiol", "streptavidin pull-down"],
               ["", "", ""], [HOT, None, None, OK], size=12)
    out.append(s)
    out.append(t(30, 128, "convert", 13, HOT, weight="bold"))
    s, _ = row(30, 136, ["4sU pulse", "alkylate (iodoacetamide)", "reverse transcribe", "4sU read as C"],
               ["", "", ""], [HOT, None, None, OK], size=12)
    out.append(s)
    out.append(t(30, 200, "Enrichment: separate new from old RNA physically (TT-seq, with fragmentation first). Conversion: no", 13, INK))
    out.append(t(30, 219, "separation, the new RNA is the reads with T-to-C mismatches (SLAM-seq, TimeLapse-seq).", 13, INK))
    return svg(800, 238, "".join(out))


def fig_tc_time():
    out = [t(30, 22, "Fraction of an RNA that is labelled after t hours of 4sU: 1 - 2^(-t / half-life).", 14, INK)]
    x0, y0, W, H = 70, 210, 420, 150
    out.append(line(x0, y0, x0 + W, y0, INK, 1.2) + line(x0, y0, x0, y0 - H, INK, 1.2))
    for hl, col in [(1, HOT), (4, TOP), (12, MUTE)]:
        pts = []
        for i in range(0, 81):
            tt = i / 10
            f = 1 - 2 ** (-tt / hl)
            pts.append("%.1f,%.1f" % (x0 + tt / 8 * W, y0 - f * H))
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.2"/>')
        out.append(t(x0 + W + 8, y0 - (1 - 2 ** (-8 / hl)) * H + 4, "half-life %d h" % hl, 12, col))
    for tt in (0, 2, 4, 6, 8):
        out.append(t(x0 + tt / 8 * W, y0 + 18, str(tt), 12, MUTE, anchor="middle"))
    for f in (0, 0.5, 1.0):
        out.append(t(x0 - 8, y0 - f * H + 4, "%d%%" % round(f * 100), 12, MUTE, anchor="end"))
    out.append(line(x0 + W / 8, y0, x0 + W / 8, y0 - H, MUTE, 1, dash="3 3"))
    out.append(t(x0 + W / 2, y0 + 38, "hours of 4sU", 12, MUTE, anchor="middle"))
    out.append(t(x0 + W / 8 + 6, y0 - H - 6, "1 h: 50%, 16%, 6%", 12, INK))
    return svg(720, 250, "".join(out))


def fig_runon():
    out = [t(30, 22, "GRO-seq: isolate nuclei, let the engaged polymerases run on briefly with labelled nucleotides.", 14, INK)]
    out.append(line(40, 90, 700, 90, MUTE, 3))
    out.append(t(60, 78, "promoter", 11.5, MUTE))
    out.append(arrow(100, 108, 180, MUTE, 1.4))
    out.append(t(190, 112, "direction of transcription", 11, MUTE))
    for x, ln, lab in [(170, 28, ""), (330, 60, ""), (520, 44, "")]:
        out.append(dot(x, 90, 8, TOP))
        out.append(line(x, 98, x - ln, 126, INK, 1.6))
        out.append(line(x - ln, 126, x - ln - 6, 130, HOT, 4.0))
    out.append(t(190, 150, "labelled run-on RNA (orange), extended from where each polymerase was", 12, HOT))
    out.append(t(40, 186, "anti-BrdU beads capture labelled RNA only", 12.5, INK))
    out.append(t(40, 206, "Reads are strand-specific, so each polymerase is placed on one strand.", 12.5, INK))
    out.append(t(40, 226, "Promoters show a sense peak (pausing) and an antisense peak (divergent transcription).", 12.5, INK))
    return svg(740, 244, "".join(out))


def fig_proseq():
    out = [t(30, 22, "PRO-seq: one biotin nucleotide is added, so the read's 3' end is the polymerase's position.", 14, INK)]
    seqs = "AUGGCUAGC"
    out.append(t(30, 66, "nascent RNA in a polymerase", 12.5, MUTE))
    out.append(cseq(230, 66, seqs[:-1]))
    out.append(cseq(230 + 8 * DX, 66, seqs[-1], {0: HOT}))
    out.append(dot(230 + 8 * DX + 4, 46, 5, HOT))
    out.append(t(230 + 8 * DX + 14, 44, "biotin-NTP", 12, HOT))
    out.append(t(230 + 9 * DX + 24, 66, "polymerase stops: the biotin nucleotide is a poor", 12, MUTE))
    out.append(t(230 + 9 * DX + 24, 84, "substrate for the next addition", 12, MUTE))
    out.append(t(30, 128, "read maps with its 3' end at", 12.5, INK))
    out.append(arrow(230 + 8 * DX + 4, 118, 230 + 8 * DX + 4, HOT) if False else "")
    out.append(line(230, 134, 230 + 9 * DX, 134, TOP, 3))
    out.append(dot(230 + 9 * DX, 134, 4, HOT))
    out.append(t(230 + 9 * DX + 14, 138, "single-nucleotide position of the active site", 12, HOT))
    out.append(t(30, 184, "GRO-seq (BrUTP) labels a longer stretch, so its 3' end is less precise. PRO-cap adds enrichment of", 13, INK))
    out.append(t(30, 203, "capped 5' ends, which maps start sites of the transcripts that polymerases have just begun.", 13, INK))
    return svg(760, 222, "".join(out))


def fig_netseq():
    out = [t(30, 22, "Two handles on the same object, the engaged polymerase.", 14, INK)]
    out.append(card(30, 38, 330, 150, "run-on (GRO-seq, PRO-seq)", ["label: nucleotides the polymerase adds",
                                                                    "read: the labelled RNA", "needs: polymerase able to extend",
                                                                    "caveat: only active polymerases", "contribute to the signal"], HOT))
    out.append(card(380, 38, 330, 150, "NET-seq, mNET-seq", ["label: none; IP of the polymerase",
                                                               "read: 3' end of RNA inside the complex",
                                                               "needs: a good Pol II antibody",
                                                               "caveat: includes polymerases", "that are paused or backtracked"], TOP))
    return svg(750, 206, "".join(out))


def fig_tss():
    out = [t(30, 22, "Finding transcription start sites: keep only RNA that still has its cap.", 14, INK)]
    out.append(t(30, 56, "capped, full-length", 12.5, INK))
    out.append(dot(200, 52, 6, HOT))
    out.append(line(206, 52, 520, 52, INK, 2.4))
    out.append(t(30, 86, "broken, no cap", 12.5, INK))
    out.append(line(300, 82, 520, 82, MUTE, 2.4))
    out.append(t(540, 56, "5' end of read = start site", 12, HOT))
    out.append(t(540, 86, "5' end = a cut, not a start", 12, MUTE))
    s, _ = row(30, 116, ["periodate-oxidise cap and 3' end", "biotinylate", "RNase I trims", "streptavidin keeps capped"],
               ["", "", ""], [None, None, None, OK], size=12)
    out.append(s)
    s, _ = row(30, 164, ["or: reverse transcriptase adds Cs at a cap", "template-switch oligo (GGG) pairs", "5' end enters the library"],
               ["", ""], [None, HOT, OK], size=12)
    out.append(s)
    out.append(t(30, 222, "CAGE: cap trapping. Template switching: the enzyme adds extra Cs preferentially at a cap.", 13.5, INK))
    return svg(820, 240, "".join(out))


def fig_probing():
    out = [t(30, 22, "Structure probing: a reagent modifies the bases that are free to react.", 14, INK)]
    out.append(t(30, 60, "RNA with adduct (orange)", 12.5, MUTE))
    out.append(line(230, 56, 450, 56, INK, 2.4))
    out.append(dot(340, 56, 6, HOT))
    out.append(t(30, 112, "truncation", 12.5, INK, weight="bold"))
    out.append(arrow(450, 108, 348, TOP, 2.2))
    out.append(t(470, 112, "stops one base before: DMS-seq, icSHAPE", 12, MUTE))
    out.append(t(30, 154, "mutation", 12.5, INK, weight="bold"))
    out.append(arrow(450, 150, 230, TOP, 2.2))
    out.append(dot(340, 150, 5, BAD))
    out.append(t(470, 154, "reads through, miscopies: SHAPE-MaP, DMS-MaPseq", 12, MUTE))
    out.append(t(30, 204, "DMS methylates unpaired A and C. SHAPE reagents acylate the 2'-OH of flexible nucleotides.", 13.5, INK))
    out.append(t(30, 224, "Mutational profiling keeps full-length reads, so one molecule shows several modified positions.", 13.5, INK))
    return svg(780, 242, "".join(out))


def fig_hairpin():
    seq = "GGCGAAAGCC"
    react = [0.0, 0.0, 0.1, 0.0, 0.9, 1.0, 0.8, 0.0, 0.1, 0.1]
    out = [t(30, 22, "Reading a DMS reactivity profile: stems protect, loops react.", 14, INK)]
    x0 = 120
    # arcs for pairs 0-9, 1-8, 2-7
    for a, b in [(0, 9), (1, 8), (2, 7)]:
        xa, xb = x0 + a * 34 + 6, x0 + b * 34 + 6
        out.append(f'<path d="M {xa} 74 Q {(xa + xb) / 2} {74 - 10 - (b - a) * 5} {xb} 74" fill="none" '
                   f'stroke="{OK}" stroke-width="1.6"/>')
    for i, ch in enumerate(seq):
        out.append(t(x0 + i * 34 + 6, 96, ch, 16, INK, anchor="middle", family=MONO))
    for i, r in enumerate(react):
        h = r * 70
        out.append(f'<rect x="{x0 + i * 34 - 6}" y="{190 - h}" width="24" height="{max(h, 1):.0f}" fill="{HOT if r > 0.5 else MUTE}"/>')
    out.append(t(110, 190, "DMS signal", 12, MUTE, anchor="end"))
    out.append(t(110, 106, "sequence", 12, MUTE, anchor="end"))
    out.append(t(x0 + 370, 170, "G and U give no signal: DMS acts on A and C only", 12, MUTE))
    out.append(t(30, 222, "Loop A residues are high; stem C residues are low. A sequence that is paired in the model but reactive in the data is a clue the model is wrong.",
                 13, INK))
    return svg(800, 240, "".join(out))


def fig_three_readouts():
    out = [t(30, 22, "Three ways a reverse transcriptase can report a mark.", 14, INK)]
    hdr = ["readout", "what the enzyme does", "needs", "examples"]
    rows = [["stop", "cDNA ends before the adduct", "keep truncated cDNA", "iCLIP, icSHAPE"],
            ["mismatch", "reads through, miscopies", "a tolerant enzyme", "PAR-CLIP, SHAPE-MaP"],
            ["conversion", "the base itself has changed", "a chemical that spares the mark", "GLORI, bisulfite"]]
    s, _ = table(30, 40, [110, 230, 250, 190], 32, hdr, rows, 13)
    return svg(800, 40 + 32 * 4 + 40, "".join(out) + s +
               t(30, 40 + 32 * 4 + 24, "The same enzyme-and-chemistry reasoning applies to a CLIP footprint, a structure probe or a base modification.", 13.5, INK))


def fig_glori():
    out = [t(30, 24, "GLORI: the RNA counterpart of bisulfite. Unmodified A is deaminated, m6A resists.", 14, INK)]
    xs = [60, 190, 350, 510]
    heads = ["", "1. glyoxal protects G", "2. nitrite deaminates", "3. RT and PCR"]
    rows = [("A", [("A", None), ("A", None), ("I", BAD), ("G", BAD)]),
            ("m6A", [("m6A", HOT), ("m6A", HOT), ("m6A", HOT), ("A", OK)])]
    for j, h in enumerate(heads):
        if h:
            out.append(t(xs[j] + 20, 52, h, 12.5, MUTE))
    for r, (name, cells) in enumerate(rows):
        y = 66 + r * 40
        out.append(t(30, y + 19, name, 13, INK, weight="bold"))
        for j, (lab, col) in enumerate(cells):
            x = xs[j] + 20
            out.append(box(x, y, 70, 28, lab, FILL.get(col, "none"), col or MUTE, 12.5, INK))
            if j < 3:
                out.append(arrow(x + 74, y + 14, xs[j + 1] + 16, MUTE, 1.2, 5))
    out.append(t(30, 168, "At each site, the fraction of A reads is the methylation level: an absolute number, not a peak height.", 13.5, OK))
    return svg(720, 186, "".join(out))


def fig_m6a_compare():
    hdr = ["method", "handle", "resolution", "antibody", "quantitative"]
    rows = [["m6A-seq (MeRIP)", "IP of fragments", "100-200 nt", "yes", "relative"],
            ["miCLIP", "crosslinked antibody", "single base", "yes", "relative"],
            ["MAZTER-seq", "MazF cuts unmethylated ACA", "ACA sites only", "no", "yes"],
            ["GLORI", "deamination of A", "single base", "no", "yes, absolute"],
            ["nanopore direct RNA", "current signal, no RT", "statistical", "no", "model-dependent"]]
    s, _ = table(30, 40, [190, 260, 150, 100, 160], 30, hdr, rows, 12.5)
    return svg(930, 40 + 30 * 6 + 36, t(30, 26, "Five answers to 'where is m6A?', each paying a different price.", 14, INK) + s)


def fig_rna_summary():
    hdr = ["question", "the handle", "protocols"]
    rows = [["Where is a mark?", "antibody, or chemistry that spares it", "m6A-seq, miCLIP, GLORI"],
            ["Where does a protein bind?", "UV crosslink, then read the stub", "HITS-CLIP, PAR-CLIP, iCLIP, eCLIP"],
            ["What was made just now?", "label with 4sU, enrich or convert", "TT-seq, SLAM-seq"],
            ["Where are polymerases?", "run-on labelling, or IP of Pol II", "GRO-seq, PRO-seq, NET-seq"],
            ["Where do transcripts start?", "keep the cap", "CAGE, PRO-cap"],
            ["Which bases are paired?", "modify the unpaired ones", "DMS-seq, icSHAPE, SHAPE-MaP"]]
    s, _ = table(30, 40, [230, 330, 330], 30, hdr, rows, 13)
    return svg(930, 40 + 30 * 7 + 14, t(30, 26, "RNA marks and dynamics: each protocol is a handle plus a readout.", 14, INK) + s)



build(__file__, [
    ("cytosine-family", fig_cytosine_family),
    ("bisulfite-chem", fig_bisulfite_chem),
    ("bs-read-example", fig_bs_example),
    ("bs-adapter", fig_bs_adapter),
    ("bs-threeletter", fig_bs_threeletter),
    ("readout-matrix", fig_readout_matrix),
    ("oxbs-tab", fig_oxbs_tab),
    ("emseq", fig_emseq),
    ("taps", fig_taps),
    ("spikein", fig_spikein),
    ("rrbs", fig_rrbs),
    ("endseq", fig_endseq),
    ("resection", fig_resection),
    ("guideseq", fig_guideseq),
    ("offtarget-handles", fig_offtarget_handles),
    ("repair-outcomes", fig_repair_outcomes),
    ("repair-seq", fig_repair_seq),
    ("repli-seq", fig_repli_seq),
    ("repli-order", fig_repli_order),
    ("cn-timing", fig_cn_timing),
    ("summary", fig_summary),
    # ---- lec-rna.qmd
    ("rna-marks-rt", fig_marks_rt),
    ("m6a-seq", fig_m6a_seq),
    ("miclip", fig_miclip),
    ("clip-flow", fig_clip_flow),
    ("trunc-vs-mut", fig_trunc_vs_mut),
    ("eclip", fig_eclip),
    ("labelling", fig_labelling),
    ("tc-time", fig_tc_time),
    ("runon", fig_runon),
    ("proseq", fig_proseq),
    ("netseq", fig_netseq),
    ("tss", fig_tss),
    ("probing", fig_probing),
    ("hairpin", fig_hairpin),
    ("three-readouts", fig_three_readouts),
    ("glori", fig_glori),
    ("m6a-compare", fig_m6a_compare),
    ("rna-summary", fig_rna_summary),
])
