#!/usr/bin/env python3
"""Figures for the compartments unit.  Run: python3 compartments/make-figs.py"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

_svg = svg


def svg(w, h, body):
    """Grow the canvas to hold the lowest text line."""
    import re as _re
    ys = [float(m) for m in _re.findall(r'<text x="[-\d.]+" y="([-\d.]+)"', body)]
    return _svg(w, max(h, int(max(ys) + 14)) if ys else h, body)


PALE_HOT = "#f5eae6"
PALE_TOP = "#e8eef5"
PALE_OK = "#e6f0e8"
GRID = "#dfe3e6"
A_COL, B_COL, C_COL = TOP, HOT, OK


def cap(x, y, s, size=13, fill=None, maxc=84):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(t(x, y + i * (size + 5), ln, size, fill) for i, ln in enumerate(lines))


def circ(x, y, r, fill="none", stroke=MUTE, w=1.4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'


def dots(x, y, r, col, n, seed, size=3):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = r * 0.75 * math.sqrt(rnd.random())
        out.append(dot(round(x + d * math.cos(a), 1), round(y + d * math.sin(a), 1), size, col))
    return "".join(out)


def table(x, y, colw, rowh, header, rows, size=12.5, hfill=PALE_TOP):
    out, xs = [], [x]
    for w in colw:
        xs.append(xs[-1] + w)
    for j, h in enumerate(header):
        out.append(box(xs[j], y, colw[j], rowh, h, hfill, MUTE, size, INK))
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            out.append(box(xs[j], y + (i + 1) * rowh, colw[j], rowh, c, "none", GRID, size, INK))
    return "".join(out)


def pois(l, k):
    return math.exp(-l) * l ** k / math.factorial(k)


# ------------------------------------------------------------------ 01 why

def fig_why():
    out = [t(40, 26, "A compartment is what lets a barcode say which cell a molecule came from.", 14, INK)]
    out.append(t(40, 56, "Bulk: everything mixed", 13, MUTE))
    out.append(box(40, 66, 190, 110, "", "none", MUTE))
    rnd = random.Random(1)
    for k in range(28):
        out.append(dot(round(rnd.uniform(52, 218), 1), round(rnd.uniform(78, 164), 1), 3, A_COL if k % 2 else B_COL))
    out.append(t(40, 196, "reads from cell A and B cannot be told apart", 12.5, BAD))
    out.append(t(300, 56, "Compartments: one barcode each", 13, MUTE))
    for k, (cx, col, bc) in enumerate([(350, A_COL, "barcode 1"), (500, B_COL, "barcode 2")]):
        out.append(circ(cx, 121, 52, "none", col, 1.8))
        out.append(dots(cx, 121, 52, col, 12, 10 + k))
        out.append(box(cx - 34, 188, 68, 20, bc, PALE_TOP if k == 0 else PALE_HOT, col, 11.5, col))
        out.append(line(cx, 173, cx, 188, MUTE, 1))
    out.append(t(300, 232, "every read carries its compartment's barcode, so reads regroup by origin", 12.5, OK))
    out.append(cap(40, 262, "Everything a single-cell, single-fragment or single-complex method does "
                            "is a way of keeping the barcode attached to the right molecules.", 14, HOT))
    return svg(640, 300, "".join(out))


# ------------------------------------------------------------------ 02 three things

def fig_three():
    out = [t(40, 26, "What is being kept together decides which compartment you need.", 14, INK)]
    # cell
    out.append(circ(120, 110, 56, PALE_TOP, A_COL))
    out.append(dots(120, 110, 56, A_COL, 14, 3, 3.5))
    out.append(t(120, 192, "one cell", 14, INK, anchor="middle"))
    out.append(t(120, 210, "its RNAs together", 12, MUTE, anchor="middle"))
    # fragment
    out.append(circ(360, 110, 56, PALE_HOT, B_COL))
    out.append(f'<path d="M 320 100 C 340 70, 380 150, 400 120" fill="none" stroke="{B_COL}" stroke-width="3"/>')
    out.append(line(335, 135, 385, 85, B_COL, 1, "3 3"))
    out.append(t(360, 192, "one long fragment", 14, INK, anchor="middle"))
    out.append(t(360, 210, "its pieces together", 12, MUTE, anchor="middle"))
    # complex
    out.append(circ(600, 110, 56, PALE_OK, C_COL))
    out.append(circ(600, 110, 18, C_COL, C_COL))
    for a in (0, 120, 240):
        ax = 600 + 38 * math.cos(math.radians(a))
        ay = 110 + 38 * math.sin(math.radians(a))
        out.append(line(600, 110, ax, ay, C_COL, 2))
        out.append(dot(round(ax, 1), round(ay, 1), 5, HOT))
    out.append(t(600, 192, "one complex", 14, INK, anchor="middle"))
    out.append(t(600, 210, "its bound DNA together", 12, MUTE, anchor="middle"))
    out.append(t(40, 246, "Cell: droplets, wells, nuclei.  Fragment: partitions.  Complex: split-and-pool.",
                 14, HOT))
    return svg(720, 264, "".join(out))


# ------------------------------------------------------------------ 03 bead oligo

def fig_bead():
    out = [t(40, 26, "The barcode is printed on the bead. One bead, one barcode, many UMIs.", 14, INK)]
    out.append(circ(90, 130, 56, PALE_TOP, TOP, 1.8))
    out.append(t(90, 134, "bead", 13, TOP, anchor="middle"))
    umis = ["TCA", "GAT", "CCG", "ATA"]
    cols = [("PCR handle", 90, MUTE, PALE_TOP), ("cell barcode", 110, TOP, PALE_TOP),
            ("UMI", 50, BAD, PALE_HOT), ("poly-dT", 70, OK, PALE_OK)]
    for k, u in enumerate(umis):
        y = 66 + k * 36
        x = 180
        out.append(line(146, 100 + k * 18, x, y + 10, MUTE, 1))
        for j, (lab, w, col, fill) in enumerate(cols):
            txt = {"PCR handle": "handle", "cell barcode": "AGCTTG", "UMI": u, "poly-dT": "TTTTTT"}[lab]
            out.append(box(x, y, w, 20, txt, fill, col, 12, col))
            x += w
    out.append(t(290, 54, "same per bead", 12, TOP))
    out.append(t(390, 54, "differs per oligo", 12, BAD))
    out.append(arrow(580, 160, 520, MUTE, 1.4))
    out.append(t(590, 166, "mRNA poly(A) tail", 12.5, MUTE))
    out.append(cap(180, 230, "The cell barcode names the compartment; the UMI names the molecule. "
                             "Reverse transcription writes both into the cDNA.", 13.5, HOT, 80))
    return svg(760, 274, "".join(out))


# ------------------------------------------------------------------ 04 plate

def fig_plate():
    out = [t(40, 26, "A plate: the well is the compartment, and its position is the barcode.", 14, INK)]
    for r in range(8):
        for c in range(12):
            x, y = 70 + c * 26, 62 + r * 22
            hot = (r, c) == (2, 3)
            out.append(circ(x, y, 8, PALE_HOT if hot else "none", HOT if hot else MUTE, 1.6 if hot else 1))
    for c in range(12):
        out.append(t(70 + c * 26, 50, str(c + 1), 10.5, MUTE, anchor="middle"))
    for r in range(8):
        out.append(t(48, 66 + r * 22, "ABCDEFGH"[r], 10.5, MUTE, anchor="middle"))
    out.append(arrow(400, 126, 470, MUTE, 1.4))
    out.append(box(480, 96, 230, 60, "", PALE_HOT, HOT))
    out.append(t(595, 120, "well C4", 14, HOT, anchor="middle"))
    out.append(t(595, 142, "row index C  +  column index 4", 12.5, INK, anchor="middle"))
    out.append(t(40, 258, "8 + 12 = 20 oligos label 96 wells.", 13, MUTE))
    out.append(cap(40, 280, "Plates give high-quality, full-length data and can be imaged first, but "
                            "the cell must be placed in the well, so the scale is hundreds to thousands.",
                   13.5, HOT, 90))
    return svg(740, 320, "".join(out))


# ------------------------------------------------------------------ 05 microwells

def fig_microwell():
    out = [t(40, 26, "Microwells: cells and beads settle by gravity, one well at a time.", 14, INK)]
    rnd = random.Random(5)
    for k in range(9):
        x = 60 + k * 62
        out.append(f'<path d="M {x} 80 L {x} 130 L {x+44} 130 L {x+44} 80" fill="none" stroke="{MUTE}" stroke-width="1.6"/>')
        has_cell = k in (1, 3, 4, 7)
        has_bead = k in (1, 2, 4, 7, 8)
        if has_bead:
            out.append(circ(x + 22, 118, 9, PALE_HOT, HOT, 1.6))
        if has_cell:
            out.append(circ(x + 22, 100 if has_bead else 117, 8, PALE_TOP, TOP, 1.6))
        out.append(t(x + 22, 152, ["empty", "usable", "bead only", "cell only", "usable", "", "", "usable", "bead only"][k],
                     10.5, MUTE if k not in (1, 4, 7) else OK, anchor="middle"))
    out.append(line(50, 130, 620, 130, MUTE, 1.4))
    out.append(t(40, 190, "A semi-sealed array holds them while lysis buffer is added, and each well's bead "
                          "captures its own cell's RNA.", 13.5, INK))
    out.append(cap(40, 216, "Seq-Well and Microwell-seq are examples. No pumps are needed, and "
                            "the loading is still Poisson.", 13, MUTE, 90))
    return svg(700, 254, "".join(out))


# ------------------------------------------------------------------ 06 droplets

def fig_droplet():
    out = [t(40, 26, "Droplets: a water-in-oil emulsion makes millions of private reaction vessels.", 14, INK)]
    out.append(box(40, 70, 150, 26, "cells + beads in water", PALE_TOP, TOP, 11.5, TOP))
    out.append(line(190, 83, 300, 83, TOP, 14))
    out.append(box(190, 150, 110, 26, "oil", PALE_HOT, HOT, 11.5, HOT))
    out.append(line(245, 150, 245, 96, HOT, 12))
    out.append(line(300, 83, 330, 83, TOP, 14))
    # droplets
    for k in range(8):
        cx = 360 + k * 44
        out.append(circ(cx, 83, 17, PALE_TOP if k not in (2, 5) else "none", MUTE, 1.2))
        if k in (0, 3, 6):
            out.append(circ(cx - 4, 78, 5, PALE_TOP, TOP, 1.4))
            out.append(circ(cx + 6, 90, 4, PALE_HOT, HOT, 1.4))
        elif k == 1:
            out.append(circ(cx, 83, 4, PALE_HOT, HOT, 1.4))
        elif k == 4:
            out.append(circ(cx - 4, 78, 5, PALE_TOP, TOP, 1.4))
    out.append(t(360, 126, "usable", 11.5, OK))
    out.append(t(360 + 44, 126, "bead only", 11.5, MUTE))
    out.append(t(360 + 4 * 44, 126, "cell, no bead: lost", 11.5, MUTE))
    out.append(cap(40, 206, "Inside each droplet the cell is lysed, its RNA is captured on the bead, and "
                            "reverse transcription runs. The oil keeps neighbours apart.", 13.5, INK, 90))
    out.append(t(40, 252, "Cells and beads arrive at random, so droplet contents follow Poisson statistics.",
                 14, HOT))
    return svg(740, 270, "".join(out))


# ------------------------------------------------------------------ 07 poisson bars

def fig_poisson():
    out = [t(40, 26, "How many cells does a droplet get? It depends on the mean, lambda.", 14, INK)]
    for p, l in enumerate((0.1, 0.5, 1.0)):
        x0 = 40 + p * 250
        out.append(t(x0, 56, f"lambda = {l:g}", 13.5, INK))
        vals = [pois(l, 0), pois(l, 1), pois(l, 2), 1 - pois(l, 0) - pois(l, 1) - pois(l, 2)]
        names = ["0", "1", "2", "3+"]
        cols = [MUTE, OK, BAD, BAD]
        base = 190
        for k, (v, nm, col) in enumerate(zip(vals, names, cols)):
            h = 110 * v
            out.append(f'<rect x="{x0 + k * 50}" y="{base - h:.1f}" width="34" height="{h:.1f}" fill="{col}"/>')
            out.append(t(x0 + k * 50 + 17, base + 16, nm, 12.5, INK, anchor="middle"))
            out.append(t(x0 + k * 50 + 17, base - h - 5, f"{100 * v:.1f}%", 10.5, INK, anchor="middle"))
        out.append(line(x0 - 4, base, x0 + 200, base, MUTE, 1))
    out.append(t(40, 230, "cells per droplet", 12, MUTE))
    out.append(cap(40, 258, "P(k) = e^(-lambda) lambda^k / k!   Green is the droplet you want, red is a doublet "
                            "or worse.", 13.5, HOT, 90))
    return svg(780, 292, "".join(out))


# ------------------------------------------------------------------ 08 grid of 1000 droplets

def fig_grid():
    out = [t(40, 26, "A thousand droplets at lambda = 0.1 (mean 1 cell per 10 droplets).", 14, INK)]
    l = 0.1
    n0 = round(1000 * pois(l, 0))
    n1 = round(1000 * pois(l, 1))
    n2 = 1000 - n0 - n1
    seq_ = [MUTE] * n0 + [OK] * n1 + [BAD] * n2
    rnd = random.Random(3)
    rnd.shuffle(seq_)
    for i, col in enumerate(seq_):
        r, c = divmod(i, 100)
        out.append(circ(48 + c * 7.4, 60 + r * 8, 2.8, col if col != MUTE else GRID, col if col != MUTE else MUTE, 0.8))
    out.append(t(40, 168, f"{n0} empty", 13, MUTE))
    out.append(t(190, 168, f"{n1} with one cell", 13, OK))
    out.append(t(370, 168, f"{n2} with two or more", 13, BAD))
    out.append(cap(40, 196, "Most of what you pay for is empty oil. That is the price of keeping doublets "
                            "to about 5% of the occupied droplets.", 13.5, HOT, 90))
    return svg(780, 230, "".join(out))


# ------------------------------------------------------------------ 09 trade-off

def fig_tradeoff():
    out = [t(40, 26, "Yield and doublets pull in opposite directions.", 14, INK)]
    x0, y0, W, H = 90, 210, 420, 150
    out.append(line(x0, y0, x0 + W, y0, MUTE, 1))
    out.append(line(x0, y0, x0, y0 - H, MUTE, 1))
    for v in (0, 0.5, 1, 1.5, 2):
        out.append(t(x0 + v / 2 * W, y0 + 16, f"{v:g}", 11.5, MUTE, anchor="middle"))
    out.append(t(x0 + W / 2, y0 + 34, "mean cells per droplet, lambda", 12, MUTE, anchor="middle"))
    pts1 = " ".join(f"{x0 + l / 2 * W:.0f},{y0 - H * pois(l, 1) / 0.45:.0f}" for l in [i / 50 for i in range(1, 101)])
    pts2 = " ".join(f"{x0 + l / 2 * W:.0f},{y0 - H * (1 - pois(l, 0) - pois(l, 1)) / (1 - pois(l, 0)):.0f}"
                    for l in [i / 50 for i in range(1, 101)])
    out.append(f'<polyline points="{pts1}" fill="none" stroke="{OK}" stroke-width="2.4"/>')
    out.append(f'<polyline points="{pts2}" fill="none" stroke="{BAD}" stroke-width="2.4"/>')
    out.append(t(x0 + 30, y0 - H - 6, "droplets with exactly one cell", 12, OK))
    out.append(t(x0 + 170, y0 - 22, "doublets among occupied droplets", 12, BAD))
    out.append(t(x0 - 8, y0 - 4, "0", 11.5, MUTE, anchor="end"))
    out.append(t(x0 - 8, y0 - H + 4, "100%", 11.5, MUTE, anchor="end"))
    out.append(cap(40, 262, "Loading at lambda = 1 gives the most singlets (37% of droplets) but about "
                            "42% of occupied droplets hold more than one cell. Most protocols sit near 0.1.",
                   13, INK, 90))
    return svg(640, 310, "".join(out))


# ------------------------------------------------------------------ 10 two Poissons

def fig_two():
    out = [t(40, 26, "Cells and beads are two independent Poisson draws. Both must come out right.", 14, INK)]
    l = 0.1
    pc = [pois(l, 0), pois(l, 1), 1 - pois(l, 0) - pois(l, 1)]
    pb = pc[:]
    names = ["0", "1", "2+"]
    x0, y0, cw, rh = 150, 80, 150, 40
    out.append(t(x0 + 1.5 * cw, 64, "beads per droplet", 12.5, MUTE, anchor="middle"))
    for j, nm in enumerate(names):
        out.append(box(x0 + j * cw, y0 - 6, cw, 26, nm, PALE_TOP, MUTE, 12.5))
    out.append(t(x0 - 12, y0 + 40, "cells", 12.5, MUTE, anchor="end"))
    outcome = {(1, 1): ("usable", OK, PALE_OK), (1, 0): ("lost", MUTE, "none"),
               (1, 2): ("cell split over barcodes", BAD, PALE_HOT), (2, 1): ("doublet", BAD, PALE_HOT),
               (2, 2): ("doublet", BAD, PALE_HOT), (2, 0): ("lost", MUTE, "none"),
               (0, 0): ("empty", MUTE, "none"), (0, 1): ("empty", MUTE, "none"), (0, 2): ("empty", MUTE, "none")}
    for i in range(3):
        out.append(box(x0 - 50, y0 + 26 + i * rh, 50, rh, names[i], PALE_TOP, MUTE, 12.5))
        for j in range(3):
            lab, col, fill = outcome[(i, j)]
            p = pc[i] * pb[j]
            out.append(box(x0 + j * cw, y0 + 26 + i * rh, cw, rh, "", fill, GRID))
            out.append(t(x0 + j * cw + cw / 2, y0 + 26 + i * rh + 16, f"{100 * p:.2f}%", 12.5, col, anchor="middle"))
            out.append(t(x0 + j * cw + cw / 2, y0 + 26 + i * rh + 32, lab, 10.5, col, anchor="middle"))
    out.append(cap(40, 258, "At lambda = 0.1 for both, a droplet is usable less than 1 time in 100. "
                            "Bead delivery is the reason some systems pack beads so that nearly every droplet has one.",
                   13, INK, 95))
    return svg(780, 300, "".join(out))


# ------------------------------------------------------------------ 11 barnyard

def fig_barnyard():
    out = [t(40, 26, "A species-mixing experiment makes doublets visible.", 14, INK)]
    x0, y0, S = 80, 246, 170
    out.append(line(x0, y0, x0 + S, y0, MUTE, 1))
    out.append(line(x0, y0, x0, y0 - S, MUTE, 1))
    rnd = random.Random(11)
    pts = []
    for _ in range(120):
        pts.append((rnd.uniform(0.35, 0.95), rnd.uniform(0, 0.04), A_COL))
    for _ in range(120):
        pts.append((rnd.uniform(0, 0.04), rnd.uniform(0.35, 0.95), B_COL))
    for _ in range(8):
        pts.append((rnd.uniform(0.25, 0.6), rnd.uniform(0.25, 0.6), BAD))
    for px, py, col in pts:
        out.append(dot(round(x0 + px * S, 1), round(y0 - py * S, 1), 2.6, col))
    out.append(t(x0 + S / 2, y0 + 20, "human UMIs per barcode", 12, A_COL, anchor="middle"))
    out.append(t(x0 - 14, y0 - S / 2, "mouse UMIs", 12, B_COL, anchor="end"))
    out.append(t(x0 + 70, y0 - S * 0.72, "mixed: a collision", 12, BAD))
    out.append(t(320, 80, "Mix human and mouse cells 1:1.", 13, INK))
    out.append(t(320, 102, "A barcode with both is certainly a doublet.", 13, INK))
    out.append(t(320, 124, "A doublet of two human cells is invisible.", 13, INK))
    out.append(t(320, 160, "If 3% of barcodes are mixed,", 13, HOT))
    out.append(t(320, 178, "the total doublet rate is about 6%.", 13, HOT))
    out.append(t(40, 268, "With a 1:1 mix, half of all doublets are same-species, hence unseen.", 12.5, MUTE))
    return svg(640, 288, "".join(out))


# ------------------------------------------------------------------ 12 nuclei

def fig_nucleus():
    out = [t(40, 26, "A nucleus is a ready-made compartment with its own membrane.", 14, INK)]
    out.append(circ(150, 130, 84, "none", MUTE, 1.2))
    out.append(t(150, 40, "cell", 12, MUTE, anchor="middle"))
    out.append(circ(150, 130, 46, PALE_TOP, TOP, 2.4))
    for a in range(0, 360, 40):
        out.append(dot(round(150 + 46 * math.cos(math.radians(a)), 1), round(130 + 46 * math.sin(math.radians(a)), 1), 3, MUTE))
    out.append(dots(150, 130, 46, TOP, 10, 8))
    out.append(t(150, 134, "", 1))
    out.append(t(150, 236, "cell", 12, MUTE, anchor="middle") if False else "")
    out.append(arrow(260, 130, 330, MUTE, 1.4))
    out.append(t(295, 118, "lyse the cell,", 11.5, MUTE, anchor="middle"))
    out.append(t(295, 152, "keep the nucleus", 11.5, MUTE, anchor="middle"))
    out.append(circ(420, 130, 46, PALE_TOP, TOP, 2.4))
    out.append(dots(420, 130, 46, TOP, 10, 8))
    out.append(t(420, 204, "nucleus: DNA, chromatin and", 12, INK, anchor="middle"))
    out.append(t(420, 220, "nascent RNA stay inside", 12, INK, anchor="middle"))
    out.append(t(560, 100, "Good: frozen tissue,", 12.5, OK))
    out.append(t(560, 118, "cells too fragile or large", 12.5, OK))
    out.append(t(560, 136, "to pass a channel", 12.5, OK))
    out.append(t(560, 168, "Cost: cytoplasmic RNA", 12.5, BAD))
    out.append(t(560, 186, "is left behind", 12.5, BAD))
    return svg(780, 260, "".join(out))


# ------------------------------------------------------------------ 13 fix + permeabilise

def fig_fixperm():
    out = [t(40, 26, "Fix and permeabilise: make the cell its own sealed reaction vessel.", 14, INK)]
    titles = ["1. live cell", "2. fix", "3. permeabilise, add reagents"]
    for p in range(3):
        x0 = 40 + p * 250
        cx, cy = x0 + 90, 120
        out.append(t(x0 + 90, 54, titles[p], 13, INK, anchor="middle"))
        out.append(circ(cx, cy, 52, PALE_TOP, TOP, 1.8 if p < 2 else 1.4))
        out.append(dots(cx, cy, 52, TOP, 10, 20 + p))
        if p == 1:
            for a in range(0, 360, 36):
                x = cx + 36 * math.cos(math.radians(a))
                y = cy + 36 * math.sin(math.radians(a))
                out.append(t(round(x, 1), round(y + 4, 1), "x", 10, HOT, anchor="middle"))
        if p == 2:
            for a in range(10, 360, 50):
                x = cx + 52 * math.cos(math.radians(a))
                y = cy + 52 * math.sin(math.radians(a))
                out.append(circ(round(x, 1), round(y, 1), 3.5, "#ffffff", MUTE, 1))
            out.append(arrow(cx + 100, cy - 20, cx + 48, HOT, 1.6))
            out.append(t(cx + 56, cy - 28, "barcode oligo", 11, HOT, anchor="start"))
    out.append(t(130, 196, "RNA free to leak", 12, BAD, anchor="middle"))
    out.append(t(380, 196, "RNA crosslinked in place", 12, OK, anchor="middle"))
    out.append(t(630, 196, "big molecules stay, small ones enter", 12, OK, anchor="middle"))
    out.append(cap(40, 228, "Fixation holds the molecules in; pores let the enzymes and oligos in. No "
                            "droplet is needed, and cells can be stored fixed and processed together.",
                   13.5, HOT, 90))
    return svg(780, 272, "".join(out))


# ------------------------------------------------------------------ 14 split-pool

def fig_splitpool():
    out = [t(40, 26, "Split-and-pool: the barcode is the path a cell takes, not the tube it is in.", 14, INK)]
    cells = [("cell 1", A_COL, [1, 0, 2]), ("cell 2", B_COL, [2, 0, 1]), ("cell 3", C_COL, [1, 2, 2])]
    rounds = ["round 1", "round 2", "round 3"]
    for r in range(3):
        x0 = 100 + r * 190
        out.append(t(x0 + 16, 52, rounds[r], 12.5, MUTE, anchor="middle"))
        for w in range(3):
            out.append(box(x0, 64 + w * 40, 32, 28, "ABC"[w] + "" if False else f"{r+1}{'ABC'[w]}", "none", MUTE, 11.5))
    for name, col, path in cells:
        pts = [(100 + r * 190 + 16, 78 + path[r] * 40) for r in range(3)]
        for a, b in zip(pts, pts[1:]):
            out.append(line(a[0] + 18, a[1], b[0] - 18, b[1], col, 1.6))
    out.append(t(40, 212, "pooled and redistributed between rounds", 12, MUTE))
    for k, (name, col, path) in enumerate(cells):
        code = "".join(f"{r+1}{'ABC'[path[r]]}" for r in range(3))
        out.append(t(640, 80 + k * 24, f"{name}: {code}", 13, col, family=MONO))
    out.append(cap(40, 238, "Cells 1 and 3 share wells in rounds 1 and 3 and part only in round 2, so their "
                            "barcodes still differ. 96 x 96 x 96 wells give 884,736 distinct barcodes from 288 oligos.",
                   13.5, HOT, 95))
    return svg(780, 284, "".join(out))


# ------------------------------------------------------------------ 15 collisions

def fig_collide():
    out = [t(40, 26, "Split-pool has no droplets, but cells still land on barcodes at random.", 14, INK)]
    N = 200
    n = 40
    rnd = random.Random(2)
    slots = [rnd.randrange(N) for _ in range(n)]
    cnt = {}
    for s_ in slots:
        cnt[s_] = cnt.get(s_, 0) + 1
    for i in range(N):
        r, c = divmod(i, 40)
        x, y = 50 + c * 14, 56 + r * 16
        k = cnt.get(i, 0)
        col = GRID if k == 0 else (OK if k == 1 else BAD)
        out.append(f'<rect x="{x}" y="{y}" width="10" height="10" fill="{col}"/>')
    coll = sum(1 for v in cnt.values() if v > 1)
    out.append(t(50, 150, f"{N} barcode combinations, {n} cells: {coll} combinations hold two cells.", 12.5, INK))
    out.append(t(50, 184, "Real design: 96 x 96 x 96 = 884,736 combinations, 100,000 cells.", 13, INK))
    out.append(t(50, 204, "lambda = 100,000 / 884,736 = 0.113", 13, INK, family=MONO))
    out.append(t(50, 224, "share a barcode: 1 - e^(-0.113) = 10.7%", 13, HOT, family=MONO))
    out.append(t(50, 252, "More rounds, or fewer cells, shrink the collision rate in the same way "
                          "as lowering droplet loading.", 13, MUTE))
    return svg(640, 274, "".join(out))


# ------------------------------------------------------------------ 16 in situ

def fig_insitu():
    out = [t(40, 26, "In-situ reactions: add the barcode inside the nucleus, with nothing leaving.", 14, INK)]
    for k, (cx, col, bc) in enumerate([(120, A_COL, "barcode A"), (300, B_COL, "barcode B")]):
        out.append(circ(cx, 110, 52, PALE_TOP if k == 0 else PALE_HOT, col, 2.2))
        out.append(f'<path d="M {cx-30} 100 C {cx-10} 70, {cx+10} 140, {cx+30} 110" fill="none" stroke="{MUTE}" stroke-width="2.4"/>')
        for a in (200, 280, 340):
            x = cx + 20 * math.cos(math.radians(a))
            y = 112 + 20 * math.sin(math.radians(a))
            out.append(f'<path d="M {x:.0f} {y-6:.0f} L {x-5:.0f} {y+4:.0f} L {x+5:.0f} {y+4:.0f} Z" fill="{col}"/>')
        out.append(t(cx, 186, bc + " on the enzyme", 12, col, anchor="middle"))
    out.append(t(420, 84, "Tagmentation or reverse transcription", 12.5, INK))
    out.append(t(420, 102, "runs in intact nuclei, in separate wells.", 12.5, INK))
    out.append(t(420, 130, "Nuclei are pooled afterwards; the", 12.5, INK))
    out.append(t(420, 148, "barcode already sits on every fragment", 12.5, INK))
    out.append(t(420, 166, "of its own nucleus.", 12.5, INK))
    out.append(cap(40, 222, "The nuclear membrane is the compartment, so reagents must be small enough "
                            "to enter and the product must be large enough to stay.", 13.5, HOT, 90))
    return svg(740, 262, "".join(out))


# ------------------------------------------------------------------ 17 two-stage

def fig_twostage():
    out = [t(40, 26, "Two-stage: pre-index in wells, then overload droplets on purpose.", 14, INK)]
    out.append(t(40, 56, "Stage 1: wells give each nucleus an index", 12.5, MUTE))
    cols = [A_COL, B_COL, C_COL, "#7a5aa0"]
    for k in range(4):
        out.append(box(40 + k * 60, 66, 46, 30, f"idx {k+1}", "none", cols[k], 11.5, cols[k]))
    out.append(arrow(290, 82, 350, MUTE, 1.4))
    out.append(t(320, 70, "pool", 11.5, MUTE, anchor="middle"))
    out.append(t(380, 56, "Stage 2: many nuclei per droplet", 12.5, MUTE))
    out.append(circ(450, 130, 58, "none", MUTE, 1.6))
    for k, (dx, dy) in enumerate([(-24, -16), (20, -20), (-4, 22), (30, 16), (-30, 18)]):
        c = cols[[0, 1, 2, 3, 0][k]] if k != 4 else cols[1]
        out.append(circ(450 + dx, 130 + dy, 10, "none", c, 2.2))
    out.append(box(400, 200, 100, 20, "droplet barcode", PALE_TOP, TOP, 11.5, TOP))
    out.append(t(590, 100, "Each nucleus: (index, droplet)", 12.5, INK))
    out.append(t(590, 118, "A collision needs the same", 12.5, INK))
    out.append(t(590, 136, "index in the same droplet.", 12.5, INK))
    out.append(t(590, 170, "5 nuclei per droplet,", 12.5, HOT))
    out.append(t(590, 188, "96 indexes: about 4%", 12.5, HOT))
    out.append(t(590, 206, "lost, not 96%.", 12.5, HOT))
    out.append(t(40, 236, "A nucleus can only collide with the other four, not with itself:", 13, MUTE))
    out.append(t(40, 256, "1 - e^(-4/96) = 4.1% of nuclei share a droplet with a nucleus of the same index.",
                 13, MUTE))
    return svg(800, 270, "".join(out))


# ------------------------------------------------------------------ 18 capsules

def fig_capsule():
    out = [t(40, 26, "Capsules and hydrogels: a compartment you can change the buffer around.", 14, INK)]
    out.append(t(40, 56, "Droplet: sealed by oil", 13, MUTE))
    out.append(circ(120, 130, 50, PALE_TOP, TOP, 1.8))
    out.append(dots(120, 130, 50, TOP, 8, 30))
    out.append(t(120, 202, "contents are fixed at", 12, INK, anchor="middle"))
    out.append(t(120, 218, "encapsulation", 12, INK, anchor="middle"))
    out.append(t(330, 56, "Capsule: a porous shell", 13, MUTE))
    cx = 400
    out.append(f'<circle cx="{cx}" cy="130" r="50" fill="{PALE_OK}" stroke="{OK}" stroke-width="3" stroke-dasharray="6 4"/>')
    out.append(dots(cx, 130, 50, TOP, 8, 31))
    for a in (160, 200, 340, 20):
        x = cx + 80 * math.cos(math.radians(a))
        y = 130 + 80 * math.sin(math.radians(a))
        x2 = cx + 54 * math.cos(math.radians(a))
        y2 = 130 + 54 * math.sin(math.radians(a))
        out.append(arrow(round(x, 1), round(y, 1), round(x2, 1), HOT, 1.6) if False else
                   line(round(x, 1), round(y, 1), round(x2, 1), round(y2, 1), HOT, 1.6))
        out.append(dot(round(x, 1), round(y, 1), 3.5, HOT))
    out.append(t(cx, 222, "reagents pass in and out;", 12, INK, anchor="middle"))
    out.append(t(cx, 238, "large DNA and RNA stay", 12, INK, anchor="middle"))
    out.append(cap(540, 90, "Steps with incompatible buffers, such as lysis then enzymatic "
                            "reactions, can run in sequence without re-making the compartment.",
                   12.5, INK, 40))
    out.append(cap(540, 184, "Particle-templated emulsification uses hydrogel beads to form droplets by "
                             "vortexing, without a microfluidic chip.", 12.5, MUTE, 40))
    return svg(820, 264, "".join(out))


# ------------------------------------------------------------------ 19 whitelist

def fig_whitelist():
    out = [t(40, 26, "Mapping a read back to its compartment: match to a known list, allow for errors.", 14, INK)]
    out.append(t(40, 66, "observed barcode", 13, MUTE))
    out.append(t(220, 66, "ACGTTA", 15, INK, family=MONO))
    out.append(t(330, 66, "not in the whitelist", 13, BAD))
    out.append(t(40, 106, "whitelist neighbours", 13, MUTE))
    out.append(t(220, 106, "ACGTTC", 15, OK, family=MONO))
    out.append(t(330, 106, "one base away, and the only one: correct to it", 13, OK))
    out.append(t(220, 130, "ACGTAC", 15, MUTE, family=MONO))
    out.append(t(330, 130, "two bases away: ignored", 13, MUTE))
    out.append(t(40, 170, "a different case", 13, MUTE))
    out.append(t(220, 170, "GATTCA", 15, INK, family=MONO))
    out.append(t(330, 170, "one base from two whitelisted barcodes: discard", 13, BAD))
    out.append(cap(40, 214, "Barcodes are designed to be several bases apart, so that one sequencing "
                            "error can be corrected and not mistaken for another compartment.", 13.5, HOT, 90))
    return svg(740, 256, "".join(out))


# ------------------------------------------------------------------ 20 knee

def fig_knee():
    out = [t(40, 26, "Rank the barcodes by reads: cells, then ambient RNA from empty droplets.", 14, INK)]
    x0, y0, W, H = 90, 220, 420, 160
    out.append(line(x0, y0, x0 + W, y0, MUTE, 1))
    out.append(line(x0, y0, x0, y0 - H, MUTE, 1))
    pts = []
    for i in range(0, 101):
        r = 10 ** (i / 100 * 5)             # rank 1 .. 100000
        if r < 6000:
            v = 8000 * (r / 6000) ** -0.08
        else:
            v = 7000 * (6000 / r) ** 2.2 + 60 * (6000 / r) ** 0.3
        v = max(v, 20)
        px = x0 + math.log10(r) / 5 * W
        py = y0 - (math.log10(v) - 1) / 4 * H
        pts.append(f"{px:.0f},{py:.0f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" stroke-width="2.4"/>')
    kx = x0 + math.log10(6000) / 5 * W
    out.append(line(kx, y0, kx, y0 - H, BAD, 1.2, "4 3"))
    out.append(t(kx + 6, y0 - H + 10, "the knee: keep barcodes to the left", 12, BAD))
    out.append(t(x0 + 40, y0 - 90, "cells", 12.5, TOP))
    out.append(t(x0 + 330, y0 - 36, "ambient", 12.5, MUTE))
    out.append(t(x0 + W / 2, y0 + 20, "barcode rank (log)", 12, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 - H / 2, "UMIs (log)", 12, MUTE, anchor="end"))
    out.append(cap(40, 262, "Barcodes below the knee are droplets that held free RNA, not a cell. "
                            "Fixed cells leak less, so the ambient floor is lower.", 13.5, HOT, 90))
    return svg(640, 300, "".join(out))


# ------------------------------------------------------------------ 21 fragments

def fig_fragments():
    out = [t(40, 26, "Compartments can keep a long fragment's pieces together too.", 14, INK)]
    out.append(line(40, 66, 360, 66, TOP, 4))
    out.append(t(40, 52, "long DNA molecule, 100 kb or more", 12, MUTE))
    out.append(arrow(380, 66, 430, MUTE, 1.4))
    for k, (cx, col) in enumerate([(500, A_COL), (620, B_COL)]):
        out.append(circ(cx, 100, 46, "none", col, 1.8))
        for j in range(3):
            xs = cx - 30 + j * 20
            out.append(line(xs, 80 + j * 14, xs + 16, 80 + j * 14 + 8, col, 3))
        out.append(box(cx - 40, 160, 80, 20, f"barcode {k+1}", PALE_TOP if k == 0 else PALE_HOT, col, 11.5, col))
    out.append(t(40, 120, "fragmented inside the", 12.5, INK))
    out.append(t(40, 138, "partition, each piece gets", 12.5, INK))
    out.append(t(40, 156, "the partition's barcode", 12.5, INK))
    out.append(cap(40, 214, "Short reads with the same barcode came from the same long molecule, which "
                            "recovers haplotypes. Few molecules per partition keep it unambiguous.",
                   13.5, HOT, 90))
    return svg(720, 258, "".join(out))


# ------------------------------------------------------------------ 22 complexes

def fig_complex():
    out = [t(40, 26, "Complexes: tag every piece in a complex with the same barcode string.", 14, INK)]
    for k, (cx, col, code) in enumerate([(130, A_COL, "1A-2C-3B"), (420, B_COL, "1B-2A-3C")]):
        out.append(circ(cx, 104, 40, PALE_TOP if k == 0 else PALE_HOT, col, 1.8))
        for a in (30, 150, 270):
            x = cx + 62 * math.cos(math.radians(a))
            y = 104 + 62 * math.sin(math.radians(a))
            out.append(line(cx + 38 * math.cos(math.radians(a)), 104 + 38 * math.sin(math.radians(a)), x, y, col, 2))
            out.append(dot(round(x, 1), round(y, 1), 5, col))
        out.append(t(cx, 200, code, 13, col, anchor="middle", family=MONO))
    out.append(t(250, 100, "pieces of one complex", 12, MUTE, anchor="middle"))
    out.append(t(250, 118, "share the string", 12, MUTE, anchor="middle"))
    out.append(cap(40, 238, "Crosslink, then split-pool: ligate a new tag in each round. DNA or RNA in the "
                            "same complex end up with identical barcodes; a different complex has another.",
                   13.5, HOT, 90))
    out.append(t(560, 90, "SPRITE reads which", 12.5, INK))
    out.append(t(560, 108, "regions share a complex,", 12.5, INK))
    out.append(t(560, 126, "with no droplets or", 12.5, INK))
    out.append(t(560, 144, "ligation of neighbours.", 12.5, INK))
    return svg(760, 276, "".join(out))


# ------------------------------------------------------------------ 23 compare

def fig_compare():
    out = [t(40, 26, "Choosing a compartment: orders of magnitude, not guarantees.", 14, INK)]
    header = ["compartment", "cells per run", "doublets", "needs", "strength"]
    rows = [["plate wells", "10^2 to 10^3", "none, if sorted", "sorting", "full length, imaging"],
            ["microwells", "10^3 to 10^4", "Poisson", "cheap kit", "no pumps"],
            ["droplets", "10^3 to 10^5", "Poisson", "microfluidics", "speed, ease"],
            ["split-pool", "10^4 to 10^6", "barcode collision", "fixed cells", "scale, low cost"],
            ["capsules", "10^4 or more", "Poisson", "special reagents", "buffer exchange"]]
    out.append(table(40, 40, [120, 130, 140, 140, 170], 30, header, rows, 12.5))
    out.append(t(40, 242, "The doublet rate is a design choice in every one of them.", 14, HOT))
    return svg(760, 262, "".join(out))


build(__file__, [
    ("why", fig_why),
    ("three", fig_three),
    ("bead", fig_bead),
    ("plate", fig_plate),
    ("microwell", fig_microwell),
    ("droplet", fig_droplet),
    ("poisson", fig_poisson),
    ("grid", fig_grid),
    ("tradeoff", fig_tradeoff),
    ("two-poisson", fig_two),
    ("barnyard", fig_barnyard),
    ("nucleus", fig_nucleus),
    ("fixperm", fig_fixperm),
    ("splitpool", fig_splitpool),
    ("collide", fig_collide),
    ("insitu", fig_insitu),
    ("twostage", fig_twostage),
    ("capsule", fig_capsule),
    ("whitelist", fig_whitelist),
    ("knee", fig_knee),
    ("fragments", fig_fragments),
    ("complex", fig_complex),
    ("compare", fig_compare),
])
