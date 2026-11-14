#!/usr/bin/env python3
"""Figures for the spatial unit.  Run: python3 spatial/make-figs.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

BLUE, RED, GREEN, TAN, GREY = "#e8eef5", "#f5eae6", "#e6f0e8", "#f3ecd9", "#eceff1"
PAL = [TOP, HOT, OK, BOT, BAD, "#7a5c99", "#b08a1e", "#2c7d83"]


def comp(s):
    return "".join({"A": "T", "T": "A", "G": "C", "C": "G"}[c] for c in s)


def lines3(x, y, rows, size=12.5, fill=MUTE, step=17, anchor="start"):
    return "".join(t(x, y + i * step, r, size, fill, anchor=anchor) for i, r in enumerate(rows))


# ---------------------------------------------------------------- 1. three routes
def fig_three_routes():
    out = [t(30, 26, "Three ways to put position into a sequence.", 14, INK),
           '<g transform="translate(0,26)">']
    xs = [30, 280, 530]
    # route 1: array capture
    x0 = xs[0]
    out.append(f'<rect x="{x0}" y="30" width="200" height="34" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    for i in range(8):
        out.append(dot(x0 + 15 + i * 24.3, 106, 7, PAL[i]))
        out.append(line(x0 + 15 + i * 24.3, 68, x0 + 15 + i * 24.3, 94, MUTE, 1.1, "3 3"))
    out.append(t(x0, 140, "1  Capture on an array", 14, HOT))
    out.append(lines3(x0, 160, ["RNA leaves the section and is", "caught by oligos whose barcode", "is the coordinate"]))
    # route 2: barcode in the tissue
    x0 = xs[1]
    out.append(f'<rect x="{x0}" y="30" width="200" height="90" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    for i in range(5):
        out.append(line(x0, 40 + i * 18, x0 + 200, 40 + i * 18, TOP, 5, cap="butt").replace('stroke-linecap="butt"', 'stroke-linecap="butt" opacity="0.45"'))
        out.append(line(x0 + 20 + i * 40, 30, x0 + 20 + i * 40, 120, HOT, 5, cap="butt").replace('stroke-linecap="butt"', 'stroke-linecap="butt" opacity="0.45"'))
    out.append(t(x0, 140, "2  Barcode inside the tissue", 14, HOT))
    out.append(lines3(x0, 160, ["Two perpendicular flows tag", "each pixel with a row and a", "column barcode"]))
    # route 3: read in place
    x0 = xs[2]
    out.append(f'<rect x="{x0}" y="30" width="200" height="90" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    for (cx, cy) in [(50, 60), (110, 85), (160, 55), (75, 100), (140, 100)]:
        out.append(f'<circle cx="{x0+cx}" cy="{cy+0}" r="17" fill="none" stroke="{MUTE}"/>')
    for k, (cx, cy) in enumerate([(45, 55), (58, 66), (105, 82), (118, 92), (155, 50), (166, 60), (70, 98), (140, 98)]):
        out.append(dot(x0 + cx, cy, 3.4, PAL[k % 4 + 1]))
    out.append(t(x0, 140, "3  Read it where it sits", 14, HOT))
    out.append(lines3(x0, 160, ["Copy the RNA in the cell, amplify", "it in place, and sequence it", "under a microscope"]))
    out.append(t(30, 236, "Routes 1 and 2 turn position into sequence before the library is made; "
                          "route 3 skips the library.", 14, INK))
    out.append("</g>")
    return svg(760, 288, "".join(out))


# ---------------------------------------------------------------- 2. capture oligo
def fig_capture_oligo():
    out = [t(30, 26, "One capture oligo on the slide. Every spot carries millions, all with the same barcode.", 14, INK)]
    parts = [("handle", 120, BLUE, TOP, "Read 1 site", "same everywhere"),
             ("spatial barcode", 170, RED, BAD, "16 nt", "differs per spot: where"),
             ("UMI", 130, GREEN, OK, "12 nt", "differs per molecule"),
             ("poly(T) VN", 160, TAN, HOT, "30 T + anchor", "catches poly(A)")]
    x, y = 70, 60
    out.append(line(x - 40, y + 13, x, y + 13, INK, 3))
    out.append(t(x - 40, y - 8, "slide", 12.5, MUTE))
    out.append(t(x + 2, y - 8, "5'", 12.5, MUTE))
    for lab, w, f, s_, a, b in parts:
        out.append(box(x, y, w, 26, lab, f, s_, 13, s_))
        out.append(t(x + w / 2, y + 100, a, 12.5, MUTE, anchor="middle"))
        out.append(t(x + w / 2, y + 117, b, 12.5, s_, anchor="middle"))
        if lab.startswith("poly"):
            px = x
        x += w
    out.append(t(x + 6, y - 8, "3'", 12.5, MUTE))
    for i in range(0, 160, 16):
        out.append(line(px + i + 8, y + 30, px + i + 8, y + 42, MUTE, 1))
    # the mRNA runs antiparallel to the oligo, so its 3' poly(A) end lies under the
    # 5' side of the poly(T) and the body continues past the VN anchor, to the right
    out.append(line(px - 10, y + 48, x + 10, y + 48, BOT, 2.6))
    out.append(t(px - 16, y + 52, "poly(A) tail", 12.5, BOT, anchor="end"))
    out.append(t(x + 16, y + 52, "mRNA", 12.5, BOT))
    out.append(t(30, 222, "RNA is reverse transcribed from the oligo, so the cDNA inherits barcode and UMI in one step.", 14, HOT))
    return svg(640, 242, "".join(out))


# ---------------------------------------------------------------- 3. sandwich
def fig_sandwich():
    out = []
    out.append(t(30, 24, "Side view: the section lies on the array, and RNA must travel down, not sideways.", 14, INK))
    out.append(f'<rect x="40" y="46" width="560" height="44" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    for i in range(9):
        out.append(f'<ellipse cx="{80 + i*62}" cy="68" rx="22" ry="14" fill="none" stroke="{MUTE}"/>')
    out.append(t(606, 72, "tissue", 12.5, MUTE))
    # array spots
    for i in range(7):
        x = 56 + i * 80
        out.append(f'<rect x="{x}" y="170" width="68" height="12" fill="{PAL[i]}" opacity="0.8"/>')
        out.append(t(x + 34, 200, "spot %d" % (i + 1), 11.5, MUTE, anchor="middle"))
    out.append(f'<rect x="40" y="182" width="560" height="8" fill="#cfd4d8"/>')
    out.append(t(606, 190, "slide", 12.5, MUTE))
    sx = 296  # source cell
    out.append(dot(sx, 70, 5, INK))
    out.append(line(sx, 76, sx, 166, OK, 2.2))
    out.append(t(sx + 8, 160, "right spot", 11.5, OK))
    out.append(line(sx - 4, 76, sx - 95, 166, BAD, 2, "5 3"))
    out.append(line(sx + 4, 76, sx + 150, 166, BAD, 2, "5 3"))
    out.append(t(195, 160, "wrong spot", 11.5, BAD, anchor="end"))
    out.append(t(452, 160, "wrong spot", 11.5, BAD))
    out.append(t(30, 232, "Release the RNA, but do not let it wander.", 14, HOT))
    return svg(660, 250, "".join(out))


# ---------------------------------------------------------------- 4. permeabilisation
def fig_permeabilisation():
    out = []
    panels = [("too short", [1, 1, 3, 1, 1], "RNA stays in the cells.", "Weak, biased to easy transcripts."),
              ("right", [0.4, 1, 9, 1, 0.4], "RNA drops straight down.", "Signal sits under its cell."),
              ("too long", [4, 5, 6, 5, 4], "RNA spreads sideways.", "Signal smeared over neighbours.")]
    for k, (ttl, hs, a, b) in enumerate(panels):
        x0 = 30 + k * 240
        out.append(t(x0, 28, ttl, 15, HOT, weight="bold"))
        out.append(f'<rect x="{x0}" y="40" width="200" height="16" rx="4" fill="{TAN}" stroke="{MUTE}"/>')
        out.append(dot(x0 + 100, 48, 4, INK))
        out.append(line(x0 + 100, 62, x0 + 100, 74, MUTE, 1.2, "3 3"))
        for i, h in enumerate(hs):
            bx = x0 + 10 + i * 38
            out.append(f'<rect x="{bx}" y="{170 - h * 9}" width="30" height="{h * 9}" fill="{PAL[1] if i == 2 else BOT}" opacity="0.85"/>')
        out.append(line(x0, 170, x0 + 200, 170, INK, 1.2))
        out.append(t(x0 + 100, 188, "five adjacent spots", 11.5, MUTE, anchor="middle"))
        out.append(t(x0, 210, a, 12.5, INK))
        out.append(t(x0, 227, b, 12.5, MUTE))
    out.append(t(30, 252, "Bar height = reads for one gene in each spot.", 14, INK))
    return svg(740, 270, "".join(out))


# ---------------------------------------------------------------- 5. fixation
def fig_fixation():
    out = [t(30, 26, "The same transcript, three tissue histories", 14, INK)]
    rows = [("Fresh frozen", "intact mRNA, poly(A) tail free", "capture with oligo-dT"),
            ("Formalin, paraffin (FFPE)", "crosslinked and fragmented, tails often lost", "capture with probe pairs"),
            ("Fixed on purpose (in situ)", "crosslinked to a protein mesh on purpose", "copy it, anchor it, read it")]
    for r, (a, b, c) in enumerate(rows):
        y = 46 + r * 62
        out.append(t(30, y + 22, a, 13.5, HOT, weight="bold"))
        x = 250
        if r == 0:
            out.append(line(x, y + 18, x + 118, y + 18, BOT, 2.6))
            out.append(t(x + 122, y + 22, "AAAA", 12, BOT, family=MONO))
        elif r == 1:
            for i, (s, e) in enumerate([(0, 40), (52, 90), (104, 150)]):
                out.append(line(x + s, y + 18, x + e, y + 18, BOT, 2.6))
            for xx in (46, 97):
                out.append(t(x + xx, y + 10, "x", 14, BAD, anchor="middle"))
                out.append(line(x + xx, y + 22, x + xx, y + 36, MUTE, 1, "2 2"))
        else:
            for i in range(6):
                out.append(line(x + i * 26, y + 4, x + i * 26, y + 38, "#c9ced2", 1.2))
            out.append(line(x, y + 14, x + 150, y + 14, "#c9ced2", 1.2))
            out.append(line(x, y + 30, x + 150, y + 30, "#c9ced2", 1.2))
            out.append(line(x + 10, y + 21, x + 140, y + 21, BOT, 2.4))
            for xx in (26, 78, 130):
                out.append(dot(x + xx, y + 21, 3.4, BAD))
        out.append(t(430, y + 15, b, 12.5, INK))
        out.append(t(430, y + 33, c, 12.5, OK))
    out.append(t(30, 244, "Fixation is not a preliminary. It decides which RNA is still there to be captured, and how.", 14, HOT))
    return svg(760, 262, "".join(out))


# ---------------------------------------------------------------- 6. workflow
def fig_workflow():
    out = [t(30, 26, "The Visium workflow, in order.", 14, INK),
           '<g transform="translate(0,22)">']
    steps = [["section on slide"], ["fix, stain, image"], ["permeabilise"], ["reverse transcribe", "on the slide"],
             ["second strand"], ["KOH release"], ["cDNA PCR"], ["fragment, adapter,", "index PCR"]]
    bw, bh = 150, 44
    for i, ls in enumerate(steps):
        r, c = divmod(i, 4)
        x, y = 30 + c * 175, 30 + r * 80
        hot = ls[0] == "permeabilise"
        out.append(box(x, y, bw, bh, "", RED if hot else BLUE, HOT if hot else TOP))
        for j, l in enumerate(ls):
            yy = y + 27 if len(ls) == 1 else y + 19 + j * 15
            # number the boxes, so "step 6" in the note below can be checked
            out.append(t(x + bw / 2, yy, ("%d  %s" % (i + 1, l)) if j == 0 else l, 13, INK, anchor="middle"))
        if c < 3:
            out.append(arrow(x + bw + 3, y + bh / 2, x + bw + 22, MUTE, 1.5, 5))
    out.append(t(30, 186, "The slide is discarded after step 6: from there on it is an ordinary bulk cDNA library in a tube.", 14, INK))
    out.append(t(30, 210, "Everything that matters spatially happens in the first four boxes.", 14, HOT))
    out.append("</g>")
    return svg(740, 252, "".join(out))


# ---------------------------------------------------------------- 7. read layout
def fig_read_layout():
    out = [t(30, 26, "Final library and how it is read (Visium read structure 28 / 10 / 10 / 90)", 14, INK)]
    seg = [("P5", 34, BLUE, TOP), ("i5", 34, GREEN, OK), ("R1", 34, BLUE, TOP), ("barcode 16", 80, RED, BAD),
           ("UMI 12", 60, GREEN, OK), ("cDNA insert", 170, GREY, MUTE), ("R2", 34, BLUE, TOP),
           ("i7", 34, GREEN, OK), ("P7", 34, BLUE, TOP)]
    x = 40
    pos = {}
    for lab, w, f, s in seg:
        out.append(box(x, 52, w, 28, lab, f, s, 12, s))
        pos[lab] = (x, w)
        x += w
    bx, bw = pos["barcode 16"][0], pos["barcode 16"][1] + pos["UMI 12"][1]
    out.append(arrow(bx, 110, bx + bw, HOT)); out.append(t(bx, 132, "Read 1: 28 cycles", 12.5, HOT))
    ix, iw = pos["cDNA insert"]
    out.append(arrow(ix + iw, 110, ix + 10, OK)); out.append(t(ix + iw, 132, "Read 2: 90 cycles", 12.5, OK, anchor="end"))
    for lab, nm in (("i5", "i5: 10"), ("i7", "i7: 10")):
        px, pw = pos[lab]
        out.append(arrow(px, 160, px + pw, MUTE)); out.append(t(px + pw / 2, 180, nm, 12, MUTE, anchor="middle"))
    out.append(t(30, 214, "Read 1 carries position and molecule identity; Read 2 carries the biology.", 14, HOT))
    return svg(720, 232, "".join(out))


# ---------------------------------------------------------------- 8. resolution ladder
def fig_resolution():
    import math
    out = [t(30, 26, "Spot or pixel size on a log scale (micrometres)", 14, INK)]
    x0, x1, y = 60, 680, 150
    lo, hi = math.log10(0.1), math.log10(1000)
    X = lambda v: x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)
    out.append(line(x0, y, x1, y, INK, 1.4))
    for v in (0.1, 1, 10, 100, 1000):
        out.append(line(X(v), y - 4, X(v), y + 4, INK, 1.2))
        out.append(t(X(v), y + 20, ("%g" % v), 12.5, MUTE, anchor="middle"))
    out.append(f'<rect x="{X(8):.0f}" y="{y-92}" width="{X(14)-X(8):.0f}" height="92" fill="{TAN}" opacity="0.8"/>')
    out.append(t(X(10), y - 98, "a cell, ~10", 12, MUTE, anchor="middle"))
    items = [("Stereo-seq", 0.5, 0), ("HDST", 2, 1), ("Slide-seq", 10, 0), ("DBiT-seq", 20, 1),
             ("Visium", 55, 0), ("GeoMx region", 300, 1)]
    for name, v, lvl in items:
        yy = y - 22 - lvl * 26
        out.append(dot(X(v), y, 5, HOT))
        out.append(line(X(v), y - 5, X(v), yy + 3, MUTE, 1))
        out.append(t(X(v), yy, name, 12.5, INK, anchor="middle"))
    out.append(t(30, 200, "Stereo-seq pitch 0.5; HDST bead 2; Slide-seq bead 10; DBiT 10 to 50;", 12.5, MUTE))
    out.append(t(30, 216, "Visium spot 55 (100 centre to centre); GeoMx: the area you draw.", 12.5, MUTE))
    out.append(t(30, 242, "Smaller spots do not mean more RNA: each one catches proportionally less.", 14, HOT))
    return svg(720, 260, "".join(out))


# ---------------------------------------------------------------- 9. array making
def fig_array_making():
    out = []
    # printed
    x0 = 30
    out.append(t(x0, 26, "Printed (Visium)", 14, HOT, weight="bold"))
    for i in range(5):
        for j in range(4):
            out.append(dot(x0 + 20 + i * 36, 56 + j * 30, 11, PAL[(i + j * 2) % 8]))
    out.append(lines3(x0, 186, ["Barcode at each spot is", "known from manufacture"], 12.5, MUTE))
    # beads
    x0 = 270
    out.append(t(x0, 26, "Beads (Slide-seq, HDST)", 14, HOT, weight="bold"))
    import random
    rnd = random.Random(4)
    for k in range(22):
        out.append(dot(x0 + 12 + rnd.random() * 190, 48 + rnd.random() * 108, 6, PAL[rnd.randrange(8)]))
    out.append(lines3(x0, 186, ["Poured on, then positions found", "by sequencing the beads in place"], 12.5, MUTE))
    # DNB
    x0 = 540
    out.append(t(x0, 26, "DNB chip (Stereo-seq)", 14, HOT, weight="bold"))
    for i in range(10):
        for j in range(8):
            out.append(dot(x0 + 10 + i * 20, 52 + j * 14, 3.2, PAL[(i * 3 + j * 5) % 8]))
    out.append(lines3(x0, 186, ["Patterned nanoballs; barcode", "decoded before the tissue arrives"], 12.5, MUTE))
    out.append(t(30, 240, "Three answers to one question: how does a barcode get a coordinate?", 14, INK))
    return svg(760, 258, "".join(out))


# ---------------------------------------------------------------- 10. DNB molecule
def fig_dnb():
    out = [t(30, 26, "Stereo-seq: build the array first, decode it, then add the part that catches RNA", 14, INK)]
    steps = [("1", "CID circle", "rolling-circle amplify", "into a nanoball (DNB)"),
             ("2", "decode", "sequence the CID of", "every DNB: map = position"),
             ("3", "ligate capture", "add MID and poly(T)", "to each DNB oligo"),
             ("4", "tissue on top", "RNA caught, RT,", "library for DNBSEQ")]
    for i, (n, a, b, c) in enumerate(steps):
        x = 30 + i * 180
        out.append(box(x, 50, 150, 34, f"{n}  {a}", BLUE if i != 2 else RED, TOP if i != 2 else HOT, 13))
        out.append(t(x, 108, b, 12.5, MUTE))
        out.append(t(x, 125, c, 12.5, MUTE))
        if i < 3:
            out.append(arrow(x + 152, 67, x + 176, MUTE, 1.4, 5))
    out.append(line(60, 190, 560, 190, INK, 3))
    out.append(box(60, 160, 180, 26, "CID  (coordinate)", RED, BAD, 13, BAD))
    out.append(box(240, 160, 100, 26, "MID  (UMI)", GREEN, OK, 13, OK))
    out.append(box(340, 160, 140, 26, "poly(T)", TAN, HOT, 13, HOT))
    out.append(t(30, 218, "The coordinate is a sequence that is read twice: once to build the map, once with the sample.", 14, HOT))
    return svg(740, 236, "".join(out))


# ---------------------------------------------------------------- 11. DBiT grid
def fig_dbit_grid():
    out = []
    n = 5
    def tissue(x0, title):
        out.append(t(x0, 26, title, 14, HOT, weight="bold"))
        out.append(f'<rect x="{x0}" y="40" width="170" height="170" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    # flow A
    tissue(30, "Flow A, horizontal")
    for i in range(n):
        out.append(f'<rect x="30" y="{48 + i*34}" width="170" height="20" fill="{TOP}" opacity="{0.25 + 0.12*i:.2f}"/>')
        out.append(t(26, 63 + i * 34, "A%d" % (i + 1), 11.5, MUTE, anchor="end"))
    # flow B
    tissue(270, "Flow B, vertical")
    for i in range(n):
        out.append(f'<rect x="{278 + i*34}" y="40" width="20" height="170" fill="{HOT}" opacity="{0.25 + 0.12*i:.2f}"/>')
        out.append(t(288 + i * 34, 226, "B%d" % (i + 1), 11.5, MUTE, anchor="middle"))
    # result
    out.append(t(510, 26, "Each crossing is a pixel", 14, HOT, weight="bold"))
    out.append(f'<rect x="510" y="40" width="170" height="170" rx="6" fill="{TAN}" stroke="{MUTE}"/>')
    for i in range(n):
        for j in range(n):
            sel = (i, j) == (2, 1)
            out.append(f'<rect x="{514 + j*33.5}" y="{44 + i*33.5}" width="29" height="29" fill="{HOT if sel else "none"}" '
                       f'stroke="{MUTE}" stroke-width="0.8" opacity="{1 if sel else 0.9}"/>')
    out.append(t(514 + 1 * 33.5 + 14, 44 + 2 * 33.5 + 19, "A3B2", 10.5, "#ffffff", anchor="middle"))
    out.append(t(30, 252, "50 x 50 channels give 2,500 pixels. The tissue itself is the array; no slide with barcodes "
                          "is needed.", 14, INK))
    return svg(720, 270, "".join(out))


# ---------------------------------------------------------------- 12. DBiT linker
def fig_dbit_linker():
    out = [t(30, 26, "Why barcode B ends up next to barcode A: a splint holds both beside one nick", 14, INK)]
    top = "CGAATGCTCTGGCCT" + "CTCAAGCACGTGGAT"
    a, b = comp(top[:15]), comp(top[15:])
    x = 170
    s1, w = seq(x, 96, top, TOP)
    out.append(s1)
    out.append(t(x - 10, 96, "5'", 12.5, MUTE, anchor="end")); out.append(t(x + w + 6, 96, "3'", 12.5, MUTE))
    out.append(t(x + w + 34, 96, "universal linker", 12.5, MUTE))
    out.append(seq(x, 132, a, OK)[0]); out.append(seq(x + 15 * DX, 132, b, HOT)[0])
    out.append(pairs(x, 96, 132, top, a + b))
    out.append(line(x + 15 * DX - 1, 120, x + 15 * DX - 1, 142, BAD, 2.2))
    out.append(t(x + 15 * DX - 1, 160, "nick: 5' phosphate meets 3'-OH", 12.5, BAD, anchor="middle"))
    out.append(arrow(x - 4, 128, x - 60, OK, 2)); out.append(t(x - 64, 118, "barcode A,", 12, OK, anchor="end"))
    out.append(t(x - 64, 133, "oligo-dT, cDNA", 12, OK, anchor="end"))
    out.append(arrow(x + 30 * DX + 4, 128, x + 30 * DX + 60, HOT, 2))
    out.append(t(x + 30 * DX + 66, 118, "barcode B, UMI,", 12, HOT)); out.append(t(x + 30 * DX + 66, 133, "biotin handle", 12, HOT))
    out.append(t(30, 200, "T4 DNA ligase seals the nick. Without the splint the two oligos would not meet.", 14, HOT))
    return svg(760, 218, "".join(out))


# ---------------------------------------------------------------- 13. GeoMx concept
def fig_geomx_concept():
    out = [t(30, 26, "GeoMx: probes carry photocleavable tags; light decides which tags are released", 14, INK)]
    out.append(f'<rect x="30" y="44" width="250" height="150" rx="8" fill="{TAN}" stroke="{MUTE}"/>')
    rois = [(80, 100, 30, False), (170, 80, 26, True), (200, 150, 24, False)]
    for cx, cy, r, on in rois:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{"#f6d9c9" if on else "none"}" stroke="{HOT if on else MUTE}" '
                   f'stroke-width="{2 if on else 1.2}"{"" if on else " stroke-dasharray='4 3'"}/>')
    for k in range(7):
        out.append(dot(150 + (k % 4) * 11, 68 + (k // 4) * 12 + 4, 2.6, BAD))
    out.append(t(212, 72, "UV", 13, HOT, anchor="middle", weight="bold"))
    out.append(line(170, 60, 170, 50, HOT, 2))
    out.append(t(30, 214, "tag + UV-cleavable linker + probe", 12.5, MUTE))
    out.append(arrow(290, 120, 370, HOT, 1.8))
    out.append(t(330, 110, "collect", 12.5, MUTE, anchor="middle"))
    for i in range(3):
        x = 380 + i * 70
        out.append(box(x, 90, 52, 60, "", BLUE if i != 1 else RED, TOP if i != 1 else HOT))
        out.append(t(x + 26, 125, "well %d" % (i + 1), 12, INK, anchor="middle"))
    out.append(t(380, 176, "one aspirate per region,", 12.5, MUTE)); out.append(t(380, 193, "Seq Code primers per well", 12.5, MUTE))
    out.append(t(30, 240, "Resolution is the region you draw, not a grid.", 14, HOT))
    return svg(640, 258, "".join(out))


# ---------------------------------------------------------------- 14. GeoMx construct
def fig_geomx_construct():
    out = [t(30, 26, "The released tag is already a short barcode; PCR only adds the sequencer handles", 14, INK)]
    k = 3.4
    def row(x, y, parts):
        for lab, n, f, s in parts:
            out.append(box(x, y, n * k, 28, lab if n * k > 38 else "", f, s, 11.5, s))
            if n * k <= 38:
                out.append(t(x + n * k / 2, y + 42, lab, 11, s, anchor="middle"))
            x += n * k
    out.append(t(30, 66, "released tag", 12.5, MUTE))
    row(150, 50, [("SPR1 20", 20, BLUE, TOP), ("UMI+ID 26", 26, GREEN, OK), ("SPR2 20", 20, BLUE, TOP)])
    out.append(t(30, 142, "after PCR", 12.5, MUTE))
    row(110, 126, [("P5 29", 29, BLUE, TOP), ("i5 8", 8, GREEN, OK), ("SPR1 33", 33, BLUE, TOP), ("UMI 14", 14, GREEN, OK),
                   ("ID 12", 12, RED, HOT), ("SPR2 34", 34, BLUE, TOP), ("i7 8", 8, GREEN, OK), ("P7 24", 24, BLUE, TOP)])
    out.append(t(110, 200, "162 bp in all. The 12-nt RTS ID names the target gene or antibody; the well's index names the region.", 12.5, MUTE))
    out.append(t(30, 232, "Short paired-end reads are enough, because what is read is an identifier, not a transcript.", 14, HOT))
    return svg(720, 250, "".join(out))


# ---------------------------------------------------------------- 15. FISSEQ
def fig_fisseq():
    out = []
    cols = [("1  RT in situ", ["random primer,", "aminoallyl-dUTP"]),
            ("2  Crosslink", ["cDNA amines to", "cell protein"]),
            ("3  Circularise", ["CircLigase joins", "the cDNA ends"]),
            ("4  Rolling circle", ["phi29: a 'rolony'", "of repeated cDNA"]),
            ("5  Read", ["sequencing by", "ligation, imaged"])]
    for i, (h, ls) in enumerate(cols):
        x = 30 + i * 145
        out.append(t(x, 28, h, 13.5, HOT, weight="bold"))
        cx, cy = x + 55, 90
        if i == 0:
            out.append(line(x + 5, cy, x + 105, cy, BOT, 2.6))
            out.append(line(x + 15, cy + 8, x + 80, cy + 8, TOP, 2.2, "4 2"))
        elif i == 1:
            for g in range(4):
                out.append(line(x + 10 + g * 30, cy - 28, x + 10 + g * 30, cy + 28, "#c9ced2", 1.4))
            out.append(line(x + 10, cy, x + 100, cy, TOP, 2.2))
            for g in (1, 2):
                out.append(dot(x + 10 + g * 30, cy, 3.6, BAD))
        elif i == 2:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{TOP}" stroke-width="2.4"/>')
            out.append(dot(cx + 26, cy, 4, HOT))
        elif i == 3:
            for r in (12, 20, 28):
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TOP}" stroke-width="1.6" opacity="0.7"/>')
            out.append(dot(cx, cy, 4, HOT))
        else:
            for g, c in enumerate([OK, HOT, BAD, TOP]):
                out.append(dot(x + 20 + g * 22, cy, 9, c))
            out.append(t(cx, cy + 36, "A  C  T  G", 12, MUTE, anchor="middle", family=MONO))
        out.append(lines3(x, 150, ls, 12.5, MUTE))
    out.append(t(30, 212, "Step 2 is the point: the amplicon must stay where the RNA was, through every wash.", 14, HOT))
    return svg(760, 230, "".join(out))


# ---------------------------------------------------------------- 16. STARmap
def fig_starmap():
    out = [t(30, 26, "STARmap: two probes read adjacent RNA bases; only a correct pair closes a circle", 14, INK)]
    out.append(line(40, 56, 600, 56, BOT, 3))
    out.append(t(34, 48, "5'", 12, MUTE)); out.append(t(606, 60, "3'", 12, MUTE)); out.append(t(630, 60, "mRNA", 12.5, BOT))
    out.append(line(110, 78, 290, 78, TOP, 4))
    out.append(t(200, 100, "primer probe", 12.5, TOP, anchor="middle"))
    out.append(line(296, 78, 420, 78, HOT, 4))
    for xx in (130, 170, 210, 250, 310, 350, 390):
        out.append(line(xx, 60, xx, 74, MUTE, 1))
    out.append(f'<path d="M 296 80 C 280 190, 440 190, 420 80" fill="none" stroke="{HOT}" stroke-width="3"/>')
    out.append(t(358, 128, "padlock probe", 12.5, HOT, anchor="middle"))
    out.append(t(358, 144, "gene code", 12.5, HOT, anchor="middle"))
    # the tail belongs to the primer, so it is drawn in the primer's colour, not in BAD
    out.append(line(262, 90, 330, 90, TOP, 3))
    out.append(t(446, 96, "12-nt tail of the primer pairs", 12.5, TOP))
    out.append(t(446, 113, "with both padlock ends", 12.5, TOP))
    out.append(t(446, 136, "T4 ligase then closes the circle:", 12.5, MUTE))
    out.append(t(446, 153, "no match at the junction, no circle", 12.5, MUTE))
    out.append(t(30, 222, "Phi29 copies the circle from the primer, the amplicon is cast in a gel, and the code is read in rounds.", 14, HOT))
    return svg(720, 240, "".join(out))


def fig_imaging_code():
    """Combinatorial hybridisation rounds as an error-robust barcode."""
    out = [t(20, 24, "No sequencer: the identity is a code read out over rounds of hybridisation.", 14, INK)]
    genes = [("gene A", [1, 1, 0, 1, 0, 0, 1, 0]),
             ("gene B", [1, 0, 1, 0, 1, 1, 0, 0]),
             ("gene C", [0, 1, 1, 0, 0, 1, 1, 0])]
    x0, y0, dx, dy = 110, 64, 42, 34
    for r in range(8):
        out.append(t(x0 + r * dx, y0 - 14, str(r + 1), 11, MUTE, anchor="middle"))
    out.append(t(x0 - 70, y0 - 14, "round", 11, MUTE))
    for i, (name, bits) in enumerate(genes):
        y = y0 + i * dy
        out.append(t(x0 - 70, y + 5, name, 12, INK))
        for r, b in enumerate(bits):
            if b:
                out.append(dot(x0 + r * dx, y, 9, HOT))
            else:
                out.append('<circle cx="%d" cy="%d" r="9" fill="none" stroke="%s" '
                           'stroke-width="1.2"/>' % (x0 + r * dx, y, MUTE))
    yb = y0 + 3 * dy + 10
    out.append(t(20, yb + 16, "Filled: the gene lights up in that round. Each gene gets its own on/off pattern, "
                              "and the patterns are chosen", 12.5, INK))
    out.append(t(20, yb + 34, "far apart, so one missed or spurious round still points at one gene — the "
                              "edit-distance idea, in colours rather than bases.", 12.5, INK))
    out.append(t(20, yb + 58, "Nothing is amplified, nothing is sequenced, and the panel is fixed before "
                              "the experiment starts.", 12.5, MUTE))
    return svg(x0 + 8 * dx + 20, yb + 72, "".join(out))


build(__file__, [
    ("three-routes", fig_three_routes),
    ("capture-oligo", fig_capture_oligo),
    ("sandwich", fig_sandwich),
    ("permeabilisation", fig_permeabilisation),
    ("fixation", fig_fixation),
    ("workflow", fig_workflow),
    ("read-layout", fig_read_layout),
    ("resolution", fig_resolution),
    ("array-making", fig_array_making),
    ("dnb", fig_dnb),
    ("dbit-grid", fig_dbit_grid),
    ("dbit-linker", fig_dbit_linker),
    ("geomx-concept", fig_geomx_concept),
    ("geomx-construct", fig_geomx_construct),
    ("fisseq", fig_fisseq),
    ("starmap", fig_starmap),
    ("imaging-code", fig_imaging_code),
])
