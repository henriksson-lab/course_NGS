#!/usr/bin/env python3
"""Figures for the single-cell unit.  Run: python3 single-cell/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PT, PH, PO = "#e8eef5", "#f5eae6", "#e6f0e8"
FILL = {TOP: PT, BOT: PT, HOT: PH, BAD: PH, OK: PO}


# ---------------------------------------------------------------- local helpers
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




def parts(x, y, items, h=26, size=12):
    """Contiguous labelled segments: items are (label, width, colour)."""
    out, cx = [], x
    for lab, w, col in items:
        out.append(box(cx, y, w, h, lab, FILL.get(col, "none"), col or MUTE, size, INK, r=2))
        cx += w
    return "".join(out), cx


def cell(x, y, r=26, col=TOP, mols=3, cols=None):
    out = [f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{MUTE}" stroke-width="1.6"/>']
    for i in range(mols):
        yy = y - r * 0.5 + i * r * 0.5
        out.append(line(x - r * 0.5, yy, x + r * 0.45, yy, (cols or [col] * mols)[i], 3))
    return "".join(out)


# ================================================================ lec.qmd: plates, droplets, microwells

def fig_barcode_principle():
    out = [t(30, 22, "The organising idea: tag every molecule with its cell of origin before the cells are mixed.", 14, INK)]
    cs = [TOP, HOT, OK]
    for i, c in enumerate(cs):
        x = 70 + i * 100
        out.append(cell(x, 100, 30, c, 3))
        out.append(t(x, 150, "cell %d" % (i + 1), 12, MUTE, anchor="middle"))
    out.append(arrow(360, 100, 420, MUTE, 1.6))
    out.append(t(390, 84, "add barcode", 11.5, MUTE, anchor="middle"))
    out.append(box(430, 60, 120, 90, "", "none", MUTE))
    k = 0
    for i, c in enumerate([TOP, HOT, OK, HOT, TOP, OK, OK, TOP, HOT]):
        yy = 72 + (i % 5) * 16
        xx = 442 + (i // 5) * 56
        out.append(f'<rect x="{xx}" y="{yy}" width="10" height="9" fill="{c}"/>')
        out.append(f'<rect x="{xx + 10}" y="{yy + 2}" width="32" height="5" fill="#c9cdd1"/>')
    out.append(t(490, 170, "one pooled library", 12, MUTE, anchor="middle"))
    out.append(arrow(560, 100, 620, MUTE, 1.6))
    out.append(t(590, 84, "sequence", 11.5, MUTE, anchor="middle"))
    for i, c in enumerate(cs):
        yy = 64 + i * 32
        out.append(f'<rect x="632" y="{yy}" width="10" height="9" fill="{c}"/>')
        out.append(f'<rect x="642" y="{yy + 2}" width="40" height="5" fill="#c9cdd1"/>')
        out.append(f'<rect x="642" y="{yy + 12}" width="30" height="5" fill="#c9cdd1"/>')
        out.append(t(700, yy + 14, "cell %d" % (i + 1), 12, c))
    out.append(t(30, 204, "Without the barcode the pooled reads are one bulk sample. With it, every read goes back to its cell.", 13.5, INK))
    return svg(800, 222, "".join(out))


def fig_compartments():
    out = [t(30, 22, "Four ways to give each cell its own compartment. The barcode is delivered differently in each.", 14, INK)]
    titles = ["plates", "droplets", "microwells", "the cell itself"]
    sub = ["primer in each well", "bead in each droplet", "bead in each well", "split and pool rounds"]
    for i in range(4):
        x0 = 30 + i * 205
        out.append(t(x0 + 90, 52, titles[i], 13.5, INK, anchor="middle", weight="bold"))
        out.append(t(x0 + 90, 184, sub[i], 12, HOT, anchor="middle"))
    # plates
    for r in range(3):
        for c in range(4):
            out.append(box(30 + 24 + c * 36, 70 + r * 36, 28, 28, "", "none", MUTE, r=3))
            out.append(dot(30 + 24 + c * 36 + 14, 70 + r * 36 + 14, 5, [TOP, HOT, OK][(r + c) % 3]))
    # droplets
    for k, (cx, cy) in enumerate([(265, 90), (325, 100), (280, 140), (340, 150)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{MUTE}" stroke-width="1.4"/>')
        out.append(dot(cx - 6, cy, 6, TOP))
        out.append(f'<circle cx="{cx + 8}" cy="{cy}" r="4" fill="{INK}"/>')
    # microwells
    out.append(f'<rect x="450" y="100" width="170" height="60" fill="#eef0f2" stroke="{MUTE}"/>')
    for k in range(4):
        wx = 462 + k * 40
        out.append(f'<rect x="{wx}" y="100" width="28" height="40" fill="#ffffff" stroke="{MUTE}"/>')
        out.append(dot(wx + 9, 128, 6, TOP) if k != 2 else "")
        out.append(f'<circle cx="{wx + 19}" cy="130" r="4" fill="{INK}"/>' if k != 2 else "")
    # cell itself
    for k, (cx, cy) in enumerate([(695, 92), (745, 100), (705, 144), (755, 150)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{MUTE}" stroke-width="1.4"/>')
        out.append(line(cx - 10, cy - 4, cx + 8, cy - 4, [TOP, HOT, OK, BAD][k], 3))
        out.append(line(cx - 10, cy + 6, cx + 8, cy + 6, [TOP, HOT, OK, BAD][k], 3))
    out.append(t(30, 212, "Plates, droplets and microwells isolate cells physically. The last one keeps cells intact and "
                 "uses the barcode path itself (next deck).", 13.5, INK))
    return svg(850, 230, "".join(out))


def fig_smartseq():
    out = [t(30, 22, "SMART-seq: one cell per well, full-length cDNA by template switching.", 14, INK)]
    s, _ = row(30, 38, ["cell sorted into lysis buffer + oligo(dT)", "RT; at the 5' end the enzyme adds Cs", "template-switch oligo (GGG) pairs"],
               ["", ""], [TOP, None, HOT], size=12)
    out.append(s)
    s, _ = row(30, 86, ["PCR with one primer on both ends", "Tn5 tagmentation", "index PCR: i5 + i7 = well"],
               ["", ""], [None, None, OK], size=12)
    out.append(s)
    s, e = parts(130, 150, [("TSO handle", 90, HOT), ("full-length cDNA", 250, None), ("oligo(dT) handle", 110, TOP)], 28)
    out.append(s)
    out.append(t(30, 168, "after RT", 12.5, MUTE))
    out.append(t(30, 204, "No barcode inside the molecule: the well index is added by PCR at the end, so each cell is a separate library.",
                 13.5, INK))
    return svg(800, 222, "".join(out))


def fig_rt_primer():
    out = [t(30, 22, "CEL-seq and MARS-seq put the cell barcode into the reverse-transcription primer, then pool.", 14, INK)]
    s, e = parts(60, 44, [("T7 promoter + handle", 140, OK), ("cell barcode", 90, HOT), ("UMI", 60, BAD), ("poly(T)", 80, TOP)], 28)
    out.append(s)
    out.append(t(60, 100, "one primer sequence per well; every primer in a well carries that well's barcode", 12, MUTE))
    for i in range(6):
        out.append(box(60 + i * 44, 120, 36, 26, "", "none", MUTE, r=3))
        out.append(dot(60 + i * 44 + 18, 133, 5, [TOP, HOT, OK, BAD, MUTE, TOP][i]))
    out.append(arrow(330, 133, 400, MUTE, 1.6))
    out.append(t(365, 118, "pool after RT", 11.5, MUTE, anchor="middle"))
    out.append(box(410, 112, 70, 44, "one tube", PT, TOP, 12))
    out.append(arrow(480, 133, 530, MUTE, 1.6))
    out.append(t(540, 130, "second strand, T7 in vitro", 12, INK))
    out.append(t(540, 148, "transcription, fragment, RT, PCR", 12, INK))
    out.append(t(30, 196, "All the expensive library steps now happen once on the pool. T7 amplification is linear, so "
                 "errors do not compound as they do in PCR.", 13.5, INK))
    return svg(820, 214, "".join(out))


def fig_umi():
    out = [t(30, 22, "A UMI turns read counts back into molecule counts. Worked example for one gene in one cell.", 14, INK)]
    data = [("AACG", 4, TOP), ("GTTC", 3, TOP), ("CCAT", 1, TOP), ("AACC", 1, BAD)]
    out.append(t(30, 54, "UMI", 12, MUTE))
    out.append(t(110, 54, "reads", 12, MUTE))
    for i, (u, n, c) in enumerate(data):
        y = 66 + i * 26
        out.append(t(30, y + 14, u, 13, c, family=MONO))
        for j in range(n):
            out.append(f'<rect x="{110 + j * 22}" y="{y}" width="18" height="16" fill="{c}"/>')
    out.append(t(330, 82, "naive count: 9 reads", 13, INK))
    out.append(t(330, 106, "distinct UMIs: 4", 13, INK))
    out.append(t(330, 130, "AACC differs from AACG by one base and has one read:", 13, BAD))
    out.append(t(330, 148, "a sequencing error, so merge it into AACG", 13, BAD))
    out.append(t(330, 176, "molecules: 3", 14, OK, weight="bold"))
    out.append(t(30, 210, "A 10-base UMI has 4^10 = 1,048,576 values. For 1,000 molecules of one gene the expected number of collisions",
                 13, INK))
    out.append(t(30, 228, "is about 1000^2 / (2 x 4^10) = 0.5, so UMIs are safe at this depth and saturate for very abundant genes.", 13, INK))
    return svg(800, 246, "".join(out))


def fig_dropseq():
    # Kept under its old build name so the figure numbering does not shift; it now
    # draws the 10x GEM, the backbone this deck traces.
    out = [t(30, 22, "A GEM: one cell and one gel bead in a droplet of oil, with the barcode on the bead's oligos.", 14, INK)]
    out.append(f'<circle cx="130" cy="120" r="84" fill="none" stroke="{MUTE}" stroke-width="2"/>')
    out.append(f'<circle cx="95" cy="120" r="30" fill="#e8eef5" stroke="{TOP}" stroke-width="1.6"/>')
    out.append(t(95, 124, "cell", 12, TOP, anchor="middle"))
    out.append(f'<circle cx="170" cy="120" r="14" fill="{INK}"/>')
    for a in range(0, 360, 40):
        x1 = 170 + 14 * math.cos(math.radians(a))
        y1 = 120 + 14 * math.sin(math.radians(a))
        out.append(line(x1, y1, 170 + 28 * math.cos(math.radians(a)), 120 + 28 * math.sin(math.radians(a)), HOT, 1.4))
    # above the bead: below it the label crossed the droplet outline
    out.append(t(170, 84, "gel bead", 12, INK, anchor="middle"))
    out.append(t(130, 224, "oil droplet, about 1 nl", 11.5, MUTE, anchor="middle"))
    out.append(t(260, 60, "oligo on the bead", 12.5, INK, weight="bold"))
    s, e = parts(260, 70, [("Read 1 primer", 100, OK), ("cell barcode", 100, HOT), ("UMI", 60, BAD), ("poly(dT)VN", 80, TOP)], 28)
    out.append(s)
    out.append(t(410, 116, "16 nt", 11, HOT, anchor="middle"))
    out.append(t(490, 116, "12 nt", 11, BAD, anchor="middle"))
    out.append(t(260, 146, "The barcode is the same on every oligo of one bead; the UMI differs between them.",
                 12.5, INK))
    out.append(t(260, 180, "The bead dissolves and frees its oligos; the mRNA primes on poly(dT)VN.", 12.5, INK))
    out.append(t(260, 200, "RT runs inside the GEM, so every cDNA carries its cell's barcode.", 12.5, INK))
    return svg(780, 244, "".join(out))


def fig_bead_synth():
    out = [t(30, 22, "Making barcoded beads: split the beads four ways, add one base, pool, repeat.", 14, INK)]
    cols = [90, 250, 410]
    path = {HOT: [0, 2, 3], TOP: [1, 1, 0]}
    chosen = {(r, p[r]): c for c, p in path.items() for r in range(3)}
    for r, x in enumerate(cols):
        out.append(t(x + 22, 50, "round %d" % (r + 1), 12, MUTE, anchor="middle"))
        for j, b in enumerate("ACGT"):
            c = chosen.get((r, j))
            out.append(box(x, 60 + j * 34, 44, 26, b, FILL.get(c, "none"), c or MUTE, 13, INK, r=3))
    for r in range(2):
        out.append(t(cols[r] + 102, 44, "pool, re-split", 11.5, MUTE, anchor="middle"))
    for c, p in path.items():
        for r in range(2):
            out.append(line(cols[r] + 44, 73 + p[r] * 34, cols[r + 1], 73 + p[r + 1] * 34, c, 2.2))
    out.append(t(500, 80, "bead 1 saw A, G, T", 12.5, HOT))
    out.append(t(500, 98, "barcode AGT on every oligo", 12.5, HOT))
    out.append(t(500, 130, "bead 2 saw C, C, A", 12.5, TOP))
    out.append(t(500, 148, "barcode CCA", 12.5, TOP))
    out.append(t(30, 214, "Three rounds give 4^3 = 64 barcodes. Twelve rounds give 4^12 = 16.8 million, enough that two beads "
                 "rarely share one.", 13.5, INK))
    return svg(780, 232, "".join(out))


def fig_poisson():
    out = [t(30, 22, "Cells land in droplets at random (Poisson). A low loading rate keeps doublets rare and wastes most droplets.", 14, INK)]
    out.append(t(30, 52, "cells per droplet", 12, MUTE))
    out.append(t(520, 52, "doublets among occupied", 12, MUTE))
    for i, lam in enumerate([0.05, 0.1, 0.3, 1.0]):
        p0 = math.exp(-lam)
        p1 = lam * p0
        p2 = 1 - p0 - p1
        y = 68 + i * 48
        out.append(t(30, y + 17, "%.2f" % lam, 13, INK))
        x = 110
        for p, c in [(p0, "#dfe3e6"), (p1, OK), (p2, BAD)]:
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(p * 380, 1.5):.1f}" height="24" fill="{c}"/>')
            x += p * 380
        out.append(t(520, y + 17, "%.1f%%" % (100 * p2 / (1 - p0)), 13, BAD))
        out.append(t(112, y + 38, "empty %.1f%%   one cell %.1f%%   two or more %.1f%%" % (100 * p0, 100 * p1, 100 * p2), 10.5, MUTE))
    out.append(t(30, 276, "Doublets among occupied droplets = P(2 or more) / (1 - P(0)). At 0.05 cells per droplet, 95% of droplets are empty.",
                 13, INK))
    return svg(780, 292, "".join(out))


def fig_bead_types():
    out = [t(30, 22, "The bead decides how well droplets are used and when the barcode is released.", 14, INK)]
    out.append(card(30, 38, 180, 150, "Drop-seq", ["rigid bead", "bead loading is random,", "so most droplets lack one", "mRNA sticks to the bead;", "RT after breaking droplets"], TOP, 11.5))
    out.append(card(220, 38, 180, 150, "inDrop", ["hydrogel bead", "beads close-pack, so almost", "every droplet gets one", "oligo freed by UV light;", "RT inside the droplet"], TOP, 11.5))
    # all four cards share one colour: OK for one vendor and BAD for another
    # would read as a verdict on four methods the deck does not rank
    out.append(card(410, 38, 180, 150, "10x Chromium", ["gel bead, dissolves", "ordered flow gives most", "droplets (GEMs) a bead", "oligo released by reducing", "agent; RT inside the GEM"], TOP, 11.5))
    out.append(card(600, 38, 180, 150, "HyDrop", ["dissolvable hydrogel bead", "made in the lab by", "split-pool barcoding", "RNA or ATAC from the", "same type of bead"], TOP, 11.5))
    return svg(800, 206, "".join(out))


def fig_tenx_construct():
    out = [t(30, 22, "10x 3' v3 as an example: the barcode and UMI sit at the start of read 1.", 14, INK)]
    out.append(t(30, 52, "bead oligo", 12, MUTE))
    s, e = parts(30, 58, [("P5", 40, TOP), ("Read 1", 70, TOP), ("16 nt cell barcode", 130, HOT), ("12 nt UMI", 90, BAD),
                          ("poly(dT)VN", 90, OK)], 26)
    out.append(s)
    out.append(t(30, 124, "library molecule", 12, MUTE))
    s, e = parts(30, 130, [("P5", 40, TOP), ("Read 1", 70, TOP), ("barcode", 80, HOT), ("UMI", 56, BAD),
                           ("cDNA insert (3' end of mRNA)", 200, None), ("Read 2", 70, BOT), ("i7", 40, BOT), ("P7", 40, BOT)], 26)
    out.append(s)
    out.append(arrow(140, 176, 276, HOT, 2.2))
    out.append(t(140, 196, "Read 1: 28 cycles = barcode + UMI", 12, HOT))
    out.append(arrow(30 + 40 + 70 + 80 + 56 + 200 + 70, 176, 30 + 40 + 70 + 80 + 56 + 10, TOP, 2.2))
    out.append(t(300, 214, "Read 2: about 90 cycles into the insert", 12, TOP))
    out.append(t(560, 176, "i7: 8 cycles, sample index", 12, MUTE))
    return svg(800, 232, "".join(out))


def fig_tenx_workflow():
    out = [t(30, 22, "Everything before the emulsion breaks is inside a droplet. After that, one bulk pool.", 14, INK)]
    s, _ = row(30, 40, ["cell + gel bead + RT mix in oil", "RT in the droplet: barcoded cDNA", "break emulsion, pool"],
               ["", ""], [TOP, HOT, None], size=12)
    out.append(s)
    out.append(line(30, 84, 800, 84, MUTE, 1, dash="3 3"))
    out.append(t(806, 88, "bulk from here", 11.5, MUTE))
    s, _ = row(30, 98, ["PCR: amplify full-length cDNA", "fragment, end repair, A-tail", "ligate Read 2 adapter"],
               ["", ""], [None, None, OK], size=12)
    out.append(s)
    s, _ = row(30, 146, ["index PCR (sample index)", "sequence"], [""], [OK, None], size=12)
    out.append(s)
    out.append(t(30, 204, "The barcode must be on the cDNA before the droplets are pooled: afterwards nothing can tell the cells apart.",
                 13.5, INK))
    return svg(900, 222, "".join(out))


def fig_knee():
    out = [t(30, 22, "Barcode rank plot (schematic): cells form a plateau, empty droplets form a tail of ambient RNA.", 14, INK)]
    x0, y0, W, H = 80, 220, 460, 170
    out.append(line(x0, y0, x0 + W, y0, INK, 1.2) + line(x0, y0, x0, y0 - H, INK, 1.2))
    pts = []
    for i in range(0, 61):
        lr = i / 10.0
        r = 10 ** lr
        c = 2 + 20000 / (1 + (r / 5000.0) ** 6) + 300 / (1 + r / 8000.0)
        ly = math.log10(c)
        pts.append("%.1f,%.1f" % (x0 + lr / 6 * W, y0 - ly / 5 * H))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{HOT}" stroke-width="2.4"/>')
    for k in range(7):
        out.append(t(x0 + k / 6 * W, y0 + 18, "1e%d" % k if k else "1", 11.5, MUTE, anchor="middle"))
    for k in range(6):
        out.append(t(x0 - 8, y0 - k / 5 * H + 4, "1e%d" % k if k else "1", 11.5, MUTE, anchor="end"))
    out.append(t(x0 + W / 2, y0 + 40, "barcodes ranked by UMI count", 12, MUTE, anchor="middle"))
    out.append(t(24, 58, "UMIs", 12, MUTE))
    out.append(t(x0 + 70, y0 - 150, "cells", 13, HOT, weight="bold"))
    out.append(t(x0 + 240, y0 - 16, "empty droplets: ambient RNA", 13, MUTE))
    out.append(line(348, 120, 370, 104, MUTE, 1))
    out.append(t(344, 124, "knee", 12, INK, anchor="end"))
    out.append(t(580, 80, "Ambient RNA is the same in every", 12.5, INK))
    out.append(t(580, 98, "droplet, so it also leaks into real", 12.5, INK))
    out.append(t(580, 116, "cells. Cells that burst early make", 12.5, INK))
    out.append(t(580, 134, "it worse.", 12.5, INK))
    return svg(820, 268, "".join(out))


def fig_barcode_correct():
    wl = ["ACGTTGCA", "TTGACCGA", "GACCATTG", "CAGTGAAC"]

    def ham(a, b):
        return sum(1 for x, y in zip(a, b) if x != y)
    for i in range(len(wl)):
        for j in range(i + 1, len(wl)):
            assert ham(wl[i], wl[j]) >= 4
    reads = ["ACGTTGCA", "ACGTAGCA", "TTGACGGA", "AAGTCCCA"]
    out = [t(30, 22, "Barcode errors: compare each read's barcode with the whitelist (8 nt shown; real ones are 16).", 14, INK)]
    out.append(t(30, 52, "whitelist", 12, MUTE))
    for i, w in enumerate(wl):
        out.append(cseq(30 + i * 130, 72, w, size=13))
    out.append(t(30, 104, "read barcode", 12, MUTE))
    out.append(t(260, 104, "closest whitelist entries", 12, MUTE))
    out.append(t(520, 104, "decision", 12, MUTE))
    for r, rd in enumerate(reads):
        y = 128 + r * 30
        dists = sorted((ham(rd, w), k) for k, w in enumerate(wl))
        best = dists[0]
        unique = len([d for d in dists if d[0] == best[0]]) == 1
        if best[0] == 0:
            dec, col = "exact match: keep", OK
            cols = {}
        elif best[0] == 1 and unique:
            dec, col = "one mismatch, unique: correct", OK
            cols = {i: BAD for i in range(8) if rd[i] != wl[best[1]][i]}
        else:
            dec, col = "no close entry: drop", BAD
            cols = {i: BAD for i in range(8) if rd[i] != wl[best[1]][i]}
        out.append(cseq(30, y, rd, cols))
        out.append(t(260, y, "distance %d to entry %d" % (best[0], best[1] + 1), 12.5, INK))
        out.append(t(520, y, dec, 12.5, col))
    out.append(t(30, 266, "A barcode is corrected only if exactly one whitelist entry is within one mismatch. Whitelists are chosen "
                 "to be far apart so that this is safe.", 13, INK))
    return svg(860, 284, "".join(out))


def fig_microwell():
    out = [t(30, 22, "Microwells: cells and beads settle by gravity into wells; no microfluidics needed.", 14, INK)]
    out.append(f'<rect x="60" y="116" width="460" height="60" fill="#eef0f2" stroke="{MUTE}"/>')
    ws = [(80, 1, 1), (150, 1, 1), (220, 0, 0), (290, 2, 1), (360, 1, 1), (430, 0, 1)]
    for x, nc, nb in ws:
        out.append(f'<rect x="{x}" y="116" width="48" height="44" fill="#ffffff" stroke="{MUTE}"/>')
        for k in range(nc):
            out.append(dot(x + 14 + k * 14, 140, 6, TOP))
        if nb:
            out.append(f'<circle cx="{x + 36}" cy="148" r="6" fill="{INK}"/>')
    out.append(line(60, 108, 520, 108, BAD, 2, dash="5 3"))
    out.append(t(540, 112, "semipermeable membrane", 12, BAD))
    out.append(t(60, 94, "lysis buffer flows in; cells lyse in place", 12, MUTE))
    out.append(arrow(150, 116, 150, MUTE, 1.2) if False else "")
    out.append(t(60, 198, "empty well", 11.5, MUTE))
    out.append(t(220, 198, "", 11))
    out.append(t(290, 198, "two cells: a doublet", 11.5, BAD))
    out.append(t(430, 198, "bead, no cell", 11.5, MUTE))
    out.append(t(30, 232, "mRNA hybridises to the bead in its own well; beads are then pooled and RT is done in bulk. Seq-Well and "
                 "Microwell-seq work this way.", 13.5, INK))
    return svg(800, 250, "".join(out))


def fig_compare_plate_droplet():
    hdr = ["", "SMART-seq2/3 plate", "CEL-seq, MARS-seq plate", "droplets, microwells"]
    rows = [["cells per experiment", "hundreds", "hundreds to thousands", "thousands to tens of thousands"],
            ["transcript coverage", "full length", "3' end", "3' end (5' variants exist)"],
            ["UMIs", "SMART-seq3 only", "yes", "yes"],
            ["cell choice", "sorted, known well", "sorted, known well", "random, no selection"],
            ["equipment", "pipette or robot", "dispenser or robot", "microfluidics, or none (microwell)"],
            ["when to pick it", "isoforms, variants", "controlled small screens", "many cells, cell atlas"]]
    s, _ = table(30, 40, [150, 170, 200, 260], 30, hdr, rows, 12.5)
    return svg(830, 40 + 30 * 7 + 18, t(30, 26, "Plates and droplets answer different questions. Numbers are typical orders of magnitude.", 14, INK) + s)


# ================================================================ lec-combinatorial.qmd

def fig_splitpool_path():
    out = [t(30, 22, "Split-pool barcoding: a cell's barcode is the path it took through the wells.", 14, INK)]
    cols = [150, 330, 510]
    for r, x in enumerate(cols):
        out.append(t(x + 22, 52, "round %d" % (r + 1), 12, MUTE, anchor="middle"))
        for j in range(3):
            out.append(box(x, 62 + j * 44, 44, 30, str(j + 1), "none", MUTE, 13, INK, r=3))
        if r < 2:
            out.append(t(x + 112, 52, "pool, re-split", 11.5, MUTE, anchor="middle"))
    routes = [((1, 2, 3), HOT), ((1, 3, 3), TOP), ((2, 2, 1), OK), ((3, 1, 2), BAD)]
    for k, (rt, c) in enumerate(routes):
        off = (k - 1.5) * 4
        for r in range(2):
            out.append(line(cols[r] + 44, 77 + (rt[r] - 1) * 44 + off, cols[r + 1], 77 + (rt[r + 1] - 1) * 44 + off, c, 2))
        out.append(t(600, 80 + k * 24, "cell %s: barcode %s" % ("abcd"[k], "-".join(map(str, rt))), 12.5, c))
    out.append(t(30, 214, "3 rounds of 3 wells give 27 barcodes. With 96 wells per round: 96^3 = 884,736, and no cell was ever isolated.",
                 13.5, INK))
    return svg(820, 232, "".join(out))


def fig_collision():
    out = [t(30, 22, "Barcode collisions: the chance a cell shares its barcode with another, 1 - exp(-n / B).", 14, INK)]
    x0, y0, W, H = 80, 210, 520, 150
    out.append(line(x0, y0, x0 + W, y0, INK, 1.2) + line(x0, y0, x0, y0 - H, INK, 1.2))
    for B, col, lab in [(9216, BAD, "96^2 = 9,216"), (884736, HOT, "96^3 = 884,736"), (84934656, OK, "96^4 = 84.9 million")]:
        pts = []
        for i in range(0, 81):
            ln = 3 + i * 4 / 80
            n = 10 ** ln
            f = 1 - math.exp(-n / B)
            pts.append("%.1f,%.1f" % (x0 + (ln - 3) / 4 * W, y0 - f * H))
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.2"/>')
    out.append(t(x0 + 60, y0 - 142, "96^2 = 9,216", 12, BAD))
    out.append(t(x0 + 250, y0 - 76, "96^3 = 884,736", 12, HOT))
    out.append(t(x0 + 400, y0 - 36, "96^4", 12, OK))
    for k in range(5):
        out.append(t(x0 + k / 4 * W, y0 + 18, "1e%d" % (3 + k), 11.5, MUTE, anchor="middle"))
    for f in (0, 0.5, 1.0):
        out.append(t(x0 - 8, y0 - f * H + 4, "%d%%" % round(f * 100), 11.5, MUTE, anchor="end"))
    out.append(line(x0, y0 - 0.1 * H, x0 + W, y0 - 0.1 * H, MUTE, 1, dash="3 3"))
    out.append(t(x0 + W + 8, y0 - 0.1 * H + 4, "10%", 11.5, MUTE))
    out.append(t(x0 + W / 2, y0 + 38, "cells in the experiment (n)", 12, MUTE, anchor="middle"))
    out.append(t(640, 120, "100,000 cells in 96^3:", 12.5, INK))
    out.append(t(640, 138, "1 - exp(-0.113) = 10.7%", 12.5, HOT))
    return svg(860, 252, "".join(out))


def fig_scirna3():
    out = [t(30, 22, "sci-RNA-seq3: three barcodes, added by RT, by ligation, and by PCR.", 14, INK)]
    s, _ = row(30, 38, ["fixed nuclei in wells", "RT with indexed oligo(dT)", "pool, redistribute"],
               ["", ""], [TOP, HOT, None], size=12)
    out.append(s)
    s, _ = row(30, 82, ["ligate indexed hairpin", "pool, sort ~25 nuclei per well", "tagment, PCR with indexed primers"],
               ["", ""], [BAD, None, OK], size=12)
    out.append(s)
    out.append(t(30, 142, "library molecule", 12, MUTE))
    s, _ = parts(30, 148, [("P5 index", 70, OK), ("ligation BC", 80, BAD), ("RT BC", 70, HOT), ("UMI", 50, None),
                           ("cDNA", 180, None), ("P7 index", 70, OK)], 26)
    out.append(s)
    out.append(t(30, 204, "Three levels of 384, 384 and 96 x 96 give more barcode combinations than nuclei, so most nuclei have a unique one.",
                 13, INK))
    return svg(860, 222, "".join(out))


def fig_splitseq():
    out = [t(30, 22, "SPLiT-seq: barcodes are ligated onto the RT primer, while the cells stay intact.", 14, INK)]
    s, _ = row(30, 38, ["round 1: RT, 48 wells, BC1", "pool, split to 96 wells", "round 2: ligate BC2"],
               ["", ""], [HOT, None, BAD], size=12)
    out.append(s)
    s, _ = row(30, 82, ["pool, split to 96 wells", "round 3: ligate BC3 + UMI", "pool, lyse, streptavidin, PCR"],
               ["", ""], [None, OK, None], size=12)
    out.append(s)
    out.append(t(30, 138, "library molecule", 12, MUTE))
    s, _ = parts(30, 144, [("cDNA", 120, None), ("BC1", 54, HOT), ("link", 40, None), ("BC2", 54, BAD), ("link", 40, None),
                           ("BC3", 54, OK), ("UMI", 50, None), ("handle", 60, TOP)], 26)
    out.append(s)
    out.append(t(30, 200, "48 x 96 x 96 = 442,368 barcode paths, multiplied by a sublibrary index added at the end. Linkers anneal each "
                 "new barcode onto the last; blocking oligos stop free adapters carrying over.", 13, INK))
    return svg(860, 218, "".join(out))


def fig_barnyard():
    import random
    rnd = random.Random(11)
    out = [t(30, 22, "The barnyard test: mix human and mouse cells. Cells with reads from both species are collisions.", 14, INK)]
    x0, y0, W, H = 80, 220, 300, 170
    out.append(line(x0, y0, x0 + W, y0, INK, 1.2) + line(x0, y0, x0, y0 - H, INK, 1.2))
    for k in range(60):
        out.append(dot(x0 + 30 + rnd.random() * 230, y0 - 4 - rnd.random() * 10, 3, TOP))
    for k in range(60):
        out.append(dot(x0 + 4 + rnd.random() * 10, y0 - 30 - rnd.random() * 130, 3, HOT))
    for k in range(7):
        out.append(dot(x0 + 70 + rnd.random() * 150, y0 - 50 - rnd.random() * 90, 3, BAD))
    out.append(t(x0 + W / 2, y0 + 24, "human UMIs per barcode", 12, MUTE, anchor="middle"))
    out.append(t(30, 100, "mouse", 12, MUTE))
    out.append(t(30, 116, "UMIs", 12, MUTE))
    out.append(t(x0 + 150, y0 - 26, "human cells", 12, TOP, anchor="middle"))
    out.append(t(x0 + 22, y0 - 150, "mouse cells", 12, HOT))
    out.append(t(x0 + 150, y0 - 70, "mixed: collisions", 12, BAD, anchor="middle"))
    out.append(t(430, 90, "Because a collision is either human+mouse (visible)", 12.5, INK))
    out.append(t(430, 108, "or same species (invisible), the observed mixed", 12.5, INK))
    out.append(t(430, 126, "fraction underestimates the real collision rate:", 12.5, INK))
    out.append(t(430, 144, "for two species, about twice the mixed rate.", 12.5, HOT))
    return svg(800, 260, "".join(out))


def fig_sciatac():
    out = [t(30, 22, "sci-ATAC-seq: Tn5 is the first barcoding step. Its adapters carry an index.", 14, INK)]
    s, _ = row(30, 38, ["nuclei in wells", "Tn5 loaded with index 1 tagments", "pool, sort ~20 nuclei per well"],
               ["", ""], [TOP, HOT, None], size=12)
    out.append(s)
    s, _ = row(30, 82, ["lyse, PCR with index 2 primers", "sequence"], [""], [OK, None], size=12)
    out.append(s)
    out.append(t(30, 138, "library molecule", 12, MUTE))
    s, _ = parts(30, 144, [("P5", 36, TOP), ("PCR index", 66, OK), ("Tn5 index", 70, HOT), ("accessible DNA", 150, None),
                           ("Tn5 index", 70, HOT), ("PCR index", 66, OK), ("P7", 36, TOP)], 26)
    out.append(s)
    out.append(t(30, 200, "Open chromatin is tagmented in place, so only accessible DNA gets adapters. Two indexes give "
                 "n x m cells; a third level (sci-ATAC-seq3) reaches hundreds of thousands.", 13, INK))
    return svg(860, 218, "".join(out))


def fig_multiome():
    out = [t(30, 22, "10x Multiome: tagment nuclei in bulk, then give both products the same bead barcode in a droplet.", 14, INK)]
    out.append(f'<circle cx="120" cy="120" r="84" fill="none" stroke="{MUTE}" stroke-width="2"/>')
    out.append(f'<circle cx="90" cy="120" r="28" fill="#e8eef5" stroke="{TOP}" stroke-width="1.6"/>')
    out.append(t(90, 124, "nucleus", 11.5, TOP, anchor="middle"))
    out.append(f'<circle cx="152" cy="120" r="14" fill="{INK}"/>')
    for a in range(0, 360, 60):
        out.append(line(152 + 14 * math.cos(math.radians(a)), 120 + 14 * math.sin(math.radians(a)),
                        152 + 28 * math.cos(math.radians(a)), 120 + 28 * math.sin(math.radians(a)), HOT if a % 120 == 0 else OK, 1.6))
    out.append(t(120, 222, "bead with two oligo types", 11.5, INK, anchor="middle"))
    out.append(t(250, 56, "RNA", 13, HOT, weight="bold"))
    s, _ = parts(250, 64, [("barcode", 70, HOT), ("UMI", 44, None), ("poly(dT) + cDNA", 130, None), ("TSO", 40, TOP)], 26)
    out.append(s)
    out.append(t(250, 126, "chromatin", 13, OK, weight="bold"))
    s, _ = parts(250, 134, [("barcode", 70, HOT), ("spacer", 54, OK), ("tagmented DNA fragment", 170, None)], 26)
    out.append(s)
    out.append(t(250, 196, "One incubation in the droplet, one pre-amplification, then the pool is split into two libraries.", 12.5, INK))
    out.append(t(250, 214, "The two libraries carry linked, but not identical, barcode sequences.", 12.5, INK))
    return svg(780, 238, "".join(out))


def fig_shareseq():
    out = [t(30, 22, "SHARE-seq: the same three-round barcode chain is built on both the chromatin and the RNA molecules.", 14, INK)]
    out.append(t(30, 56, "chromatin", 13, OK, weight="bold"))
    s, _ = parts(30, 62, [("genomic fragment", 130, None), ("Tn5 adapter", 80, TOP), ("shared arm", 74, None), ("BC1", 46, HOT), ("BC2", 46, BAD),
                          ("BC3", 46, OK)], 26)
    out.append(s)
    out.append(t(30, 124, "RNA", 13, HOT, weight="bold"))
    s, _ = parts(30, 130, [("cDNA", 70, None), ("UMI", 44, None), ("poly(dT) primer", 100, TOP), ("shared arm", 74, None), ("BC1", 46, HOT),
                           ("BC2", 46, BAD), ("BC3", 46, OK)], 26)
    out.append(s)
    out.append(t(30, 190, "Both libraries are then separated, but BC1-BC2-BC3 appears on both, so each barcode triplet is one cell in two assays.",
                 13, INK))
    return svg(860, 210, "".join(out))


def fig_citeseq():
    out = [t(30, 22, "CITE-seq: an antibody carries an oligo that looks like an mRNA to the capture chemistry.", 14, INK)]
    out.append(f'<path d="M 30 150 A 80 80 0 0 1 190 150" fill="none" stroke="{MUTE}" stroke-width="2"/>')
    for x, c, lab in [(70, HOT, "CD4"), (150, TOP, "CD8")]:
        out.append(line(x, 94, x, 74, INK, 2.2) + line(x, 74, x - 7, 62, INK, 2.2) + line(x, 74, x + 7, 62, INK, 2.2))
        out.append(line(x, 94, x, 112, c, 2.2))
        out.append(t(x, 56, lab, 12, c, anchor="middle"))
    out.append(t(110, 178, "cell surface", 11.5, MUTE, anchor="middle"))
    out.append(t(240, 50, "antibody oligo", 12.5, INK, weight="bold"))
    s, _ = parts(240, 58, [("handle", 60, OK), ("antibody barcode", 120, HOT), ("poly(A)", 70, TOP)], 26)
    out.append(s)
    out.append(t(240, 112, "bead oligo", 12.5, INK, weight="bold"))
    s, _ = parts(240, 120, [("handle", 60, OK), ("cell BC", 70, TOP), ("UMI", 50, BAD), ("poly(dT)", 70, TOP)], 26)
    out.append(s)
    out.append(t(240, 174, "poly(A) pairs with poly(dT): the antibody barcode is captured, barcoded and counted", 12.5, INK))
    out.append(t(240, 192, "exactly like an mRNA, but gives a short library separated by size.", 12.5, INK))
    return svg(800, 212, "".join(out))


def fig_hashing():
    out = [t(30, 22, "Cell hashing: label each sample with an antibody carrying a sample tag, then pool the samples.", 14, INK)]
    tags = ["tag A", "tag B", "tag C", "tag D"]
    cells = [(0, None), (1, None), (2, None), (3, None), (1, None), (0, None), (0, 2), (1, 3), (2, None), (-1, None)]
    x0, y0 = 90, 54
    for j, tg in enumerate(tags):
        out.append(t(x0 + j * 46 + 20, y0 - 4, tg, 11, MUTE, anchor="middle"))
    verdict = []
    for i, (a, b) in enumerate(cells):
        y = y0 + i * 18
        out.append(t(30, y + 13, "cell %d" % (i + 1), 11.5, MUTE))
        n_hi = 0
        for j in range(4):
            hi = j in (a, b)
            n_hi += hi
            out.append(f'<rect x="{x0 + j * 46}" y="{y}" width="40" height="15" fill="{HOT if hi else "#eef0f2"}"/>')
        v = {0: "negative", 1: "singlet", 2: "doublet"}[n_hi]
        verdict.append(v)
        out.append(t(x0 + 4 * 46 + 8, y + 13, v, 12, BAD if v != "singlet" else OK))
    out.append(t(420, 70, "Two tags on one cell mean two samples", 12.5, INK))
    out.append(t(420, 88, "were captured together: a doublet that", 12.5, INK))
    out.append(t(420, 106, "can be identified and removed.", 12.5, INK))
    out.append(t(420, 138, "Same-sample doublets stay hidden:", 12.5, INK))
    out.append(t(420, 156, "with 4 samples that is about 1 in 4", 12.5, INK))
    out.append(t(420, 174, "of all doublets.", 12.5, INK))
    out.append(t(30, 262, "Hashing lets you load more cells per lane and remove the extra doublets afterwards.", 13.5, INK))
    return svg(780, 280, "".join(out))


def fig_crispr_handles():
    out = [t(30, 22, "Three ways to read which guide a cell received: two ride the poly(A) capture, one has its own handle.", 14, INK)]
    out.append(t(30, 52, "Perturb-seq", 13, TOP, weight="bold"))
    s, _ = parts(150, 38, [("guide barcode in a Pol II transcript", 240, TOP), ("poly(A)", 60, None)], 24)
    out.append(s)
    out.append(t(470, 54, "a lookup table links barcode to guide", 12, MUTE))
    out.append(t(30, 100, "CROP-seq", 13, HOT, weight="bold"))
    s, _ = parts(150, 86, [("guide sequence inside the transcript's 3' LTR", 290, HOT), ("poly(A)", 60, None)], 24)
    out.append(s)
    out.append(t(520, 102, "guide read directly", 12, MUTE))
    out.append(t(30, 148, "direct capture", 13, OK, weight="bold"))
    s, _ = parts(150, 134, [("guide RNA with a capture sequence", 240, OK)], 24)
    out.append(s)
    out.append(t(400, 150, "bead oligo has a matching capture sequence", 12, MUTE))
    out.append(t(30, 196, "The first two route the guide through an mRNA; the last captures the guide RNA itself.", 13.5, INK))
    return svg(820, 214, "".join(out))


def fig_crop_ltr():
    out = [t(30, 22, "CROP-seq: one cassette in the 3' LTR becomes two, so a Pol II transcript carries the guide.", 14, INK)]
    s, _ = parts(60, 50, [("5' LTR: U6 + guide", 130, HOT), ("EF1a promoter", 100, None), ("PuroR", 70, None),
                          ("3' LTR: U6 + guide", 130, HOT)], 28)
    out.append(s)
    out.append(t(60, 96, "after integration both LTRs carry the guide cassette", 12, MUTE))
    out.append(arrow(60, 124, 190, HOT, 2))
    out.append(t(200, 128, "Pol III from the 5' U6: the working guide RNA, not polyadenylated", 12.5, HOT))
    out.append(arrow(290, 156, 496, TOP, 2))   # starts at EF1a, not inside the 5' LTR
    out.append(t(60, 180, "Pol II from EF1a: puro mRNA that ends in the 3' LTR copy and is polyadenylated", 12.5, TOP))
    out.append(t(30, 214, "Only the second transcript is captured by oligo(dT). It contains the guide sequence, so the cell's "
                 "perturbation is read from its own library.", 12.5, INK))
    return svg(700, 236, "".join(out))


def fig_vdj_locus():
    out = [t(30, 22, "A rearranged receptor mRNA: the variable part is far from both ends. Proportions are illustrative.", 14, INK)]
    s, e = parts(40, 52, [("5' UTR", 50, None), ("V", 190, TOP), ("CDR3", 34, HOT), ("J", 40, TOP), ("C", 280, OK), ("3' UTR", 120, None)], 28)
    out.append(s)
    out.append(t(e + 6, 70, "AAAA", 12, MUTE))
    out.append(arrow(e + 2, 100, e - 120, MUTE, 2))
    out.append(t(e - 60, 120, "3' read (about 90 nt)", 12, MUTE, anchor="middle"))
    out.append(t(e - 60, 138, "stops in the 3' UTR", 12, MUTE, anchor="middle"))
    out.append(arrow(42, 100, 130, MUTE, 2))
    out.append(t(86, 120, "short 5' read", 12, MUTE, anchor="middle"))
    out.append(t(86, 138, "ends in V", 12, MUTE, anchor="middle"))
    out.append(t(300, 112, "CDR3 spans the V(D)J junction", 12.5, HOT))
    out.append(t(300, 130, "and identifies the clone", 12.5, HOT))
    out.append(t(30, 190, "A standard 3' or 5' gene-expression library cannot reach the junction with a short read.", 13.5, INK))
    out.append(t(30, 210, "The receptor needs its own library, built by amplifying from constant-region primers.", 13.5, INK))
    return svg(780, 228, "".join(out))


def fig_vdj_capture():
    out = [t(30, 22, "5' capture puts the cell barcode at the end that carries the variable region.", 14, INK)]
    s, _ = row(30, 38, ["bead oligo: barcode + UMI + template-switch handle", "RT, template switch at the 5' cap"],
               [""], [TOP, HOT], size=12)
    out.append(s)
    out.append(t(30, 100, "barcoded cDNA", 12, MUTE))
    s, e = parts(30, 106, [("barcode + UMI", 90, HOT), ("5' UTR", 50, None), ("V", 140, TOP), ("CDR3", 36, HOT), ("J", 36, TOP),
                           ("constant region", 160, OK)], 26)
    out.append(s)
    out.append(arrow(e - 60, 150, 80, OK, 2))
    out.append(t(e - 70, 168, "constant-region primers", 12, OK, anchor="end"))
    out.append(t(30, 196, "Nested primers in the constant region amplify only receptor cDNA. T cell and B cell receptors use different "
                 "primers, and the same barcoded cDNA also gives a normal 5' gene-expression library.", 13, INK))
    return svg(800, 232, "".join(out))


def fig_libraries_one():
    out = [t(30, 22, "One barcoded cDNA pool, several libraries, separated by size or by primer.", 14, INK)]
    out.append(box(30, 70, 150, 70, "", PT, TOP))
    out.append(t(105, 100, "barcoded cDNA", 13, INK, anchor="middle"))
    out.append(t(105, 120, "one barcode per cell", 11.5, MUTE, anchor="middle"))
    items = [("5' gene expression", "fragment, adapter, index", TOP), ("V(D)J", "constant-region primers", OK),
             ("antibody / hashtag tags", "small fragments, kept apart by size", HOT),
             ("guide RNA", "guide-specific primers", BAD)]
    for i, (a, b, c) in enumerate(items):
        y = 40 + i * 46
        out.append(arrow(184, 105, 260, MUTE, 1.2) if False else "")
        out.append(line(180, 105, 250, y + 20, MUTE, 1.2))
        out.append(box(250, y, 480, 38, "", FILL.get(c, "none"), c))
        out.append(t(262, y + 16, a, 13, c, weight="bold"))
        out.append(t(262, y + 32, b, 11.5, INK))
    out.append(t(30, 236, "The cell barcode is the thread: whichever library a read comes from, it joins to the same cell.", 13.5, INK))
    return svg(760, 254, "".join(out))


def fig_compare_comb():
    hdr = ["", "droplets (10x)", "split-pool (sci, SPLiT, SHARE)"]
    rows = [["compartment", "droplet with a bead", "the cell itself, by path"],
            ["barcode comes from", "bead oligo", "RT, ligation or PCR primers"],
            ["input", "live or fixed cells, nuclei", "fixed cells or nuclei"],
            ["scale limit", "loading and cost per chip", "barcode collisions"],
            ["doublets", "Poisson loading", "barcode collisions"],
            ["instrument", "microfluidic controller", "pipettes and plates"],
            ["depth per cell", "usually higher", "usually lower"]]
    s, _ = table(30, 40, [200, 280, 360], 30, hdr, rows, 12.5)
    return svg(900, 40 + 30 * 8 + 18, t(30, 26, "Same chemistry, different compartments.", 14, INK) + s)



build(__file__, [
    # ---- lec.qmd
    ("barcode-principle", fig_barcode_principle),
    ("compartments", fig_compartments),
    ("smartseq", fig_smartseq),
    ("rt-primer", fig_rt_primer),
    ("umi", fig_umi),
    ("dropseq", fig_dropseq),
    ("bead-synth", fig_bead_synth),
    ("poisson", fig_poisson),
    ("bead-types", fig_bead_types),
    ("tenx-construct", fig_tenx_construct),
    ("tenx-workflow", fig_tenx_workflow),
    ("knee", fig_knee),
    ("barcode-correct", fig_barcode_correct),
    ("microwell", fig_microwell),
    ("compare-plate-droplet", fig_compare_plate_droplet),
    # ---- lec-combinatorial.qmd
    ("splitpool-path", fig_splitpool_path),
    ("collision", fig_collision),
    ("scirna3", fig_scirna3),
    ("splitseq", fig_splitseq),
    ("barnyard", fig_barnyard),
    ("sciatac", fig_sciatac),
    ("multiome", fig_multiome),
    ("shareseq", fig_shareseq),
    ("citeseq", fig_citeseq),
    ("hashing", fig_hashing),
    ("crispr-handles", fig_crispr_handles),
    ("crop-ltr", fig_crop_ltr),
    ("vdj-locus", fig_vdj_locus),
    ("vdj-capture", fig_vdj_capture),
    ("libraries-one", fig_libraries_one),
    ("compare-comb", fig_compare_comb),
])
