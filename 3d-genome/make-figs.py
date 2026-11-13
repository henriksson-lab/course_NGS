#!/usr/bin/env python3
"""Figures for the 3d-genome unit.  Run: python3 3d-genome/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE_B = "#e8eef5"
PALE_R = "#f5eae6"
PALE_G = "#e6f0e8"
GREY = "#dfe3e6"
NUCF = "#e9dcc6"
NUCS = "#a08560"
PURP = "#6b5b8a"


# ------------------------------------------------------------------ helpers

def dna(x1, x2, y, col=TOP, w=3.2):
    return line(x1, y, x2, y, col, w, cap="butt")


def nuc(x, y, r=11):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.15:.1f}" fill="{NUCF}" '
            f'stroke="{NUCS}" stroke-width="1.4"/>')


def cut(x, y, col=HOT, h=9):
    return line(x - 4, y - h, x + 4, y + h, col, 2.2) + line(x + 4, y - h, x - 4, y + h, col, 2.2)


def rd(x1, x2, y, col=TOP, h=5):
    d = 1 if x2 > x1 else -1
    return (line(x1, y, x2 - d * h, y, col, 3.2, cap="butt") +
            f'<path d="M {x2} {y} L {x2 - d * h} {y - h * 0.8} L {x2 - d * h} {y + h * 0.8} Z" '
            f'fill="{col}"/>')


def step_box(x, y, w, h, head, body, fill="#fbfbf9", hcol=HOT, size=11.5):
    out = [box(x, y, w, h, "", fill, MUTE)]
    out.append(t(x + w / 2, y + 17, head, 13, hcol, anchor="middle", weight="bold"))
    for j, ln in enumerate(body.split("\n")):
        out.append(t(x + w / 2, y + 36 + j * 15, ln, size, MUTE, anchor="middle"))
    return "".join(out)


def curve(d, col=TOP, w=3.2, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round"{ds}/>')


def contact(i, j, tads=(0, 9, 18, 26), loops=((9, 17),)):
    d = abs(i - j)
    v = 1.0 / (1 + d) ** 0.85
    ti = max(k for k in range(len(tads) - 1) if tads[k] <= i)
    tj = max(k for k in range(len(tads) - 1) if tads[k] <= j)
    if ti != tj:
        v *= 0.4
    for a, b in loops:
        if (i, j) in ((a, b), (b, a)):
            v += 0.55
    return min(v, 1.0)


def blend(col, a):
    r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(255 - (255 - v) * a) for v in (r, g, b))


def matrix(x, y, n, c, col=HOT, **kw):
    out = []
    for i in range(n):
        for j in range(n):
            a = contact(i, j, **kw)
            out.append(f'<rect x="{x + j * c:.1f}" y="{y + i * c:.1f}" width="{c + 0.3:.1f}" '
                       f'height="{c + 0.3:.1f}" fill="{blend(col, a)}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{n * c:.1f}" height="{n * c:.1f}" fill="none" '
               f'stroke="{MUTE}" stroke-width="1"/>')
    return "".join(out)


# ------------------------------------------------------------------ figures

def fig_question():
    out = [t(30, 24, "Far apart along the chromosome, next to each other in the nucleus.", 14, INK)]
    y = 70
    out.append(dna(30, 690, y, MUTE, 3))
    out.append(box(140, y - 22, 66, 18, "enhancer", PALE_R, BAD, 11, BAD))
    out.append(box(520, y - 22, 66, 18, "gene", PALE_G, OK, 11, OK))
    out.append(t(360, y + 22, "300 kb of DNA in between", 12, MUTE, anchor="middle"))
    # folded
    out.append(curve("M 30 200 L 330 200 C 240 100, 480 100, 390 200 L 690 200", MUTE, 3))
    out.append(box(262, 204, 66, 18, "enhancer", PALE_R, BAD, 11, BAD))
    out.append(box(392, 204, 66, 18, "gene", PALE_G, OK, 11, OK))
    out.append(t(360, 112, "folded: the two sit side by side, and the enhancer can act", 12, TOP, anchor="middle"))
    out.append(t(30, 250, "Sequencing the genome cannot tell you this. Proximity ligation turns "
                          "\"close in space\" into a molecule.", 12.5, INK))
    return svg(720, 266, "".join(out))


def fig_junction_read():
    out = [t(30, 24, "A read pair across a junction is one observed contact.", 14, INK)]
    y = 60
    out.append(dna(30, 690, y, MUTE, 3))
    out.append(dna(140, 230, y, TOP, 5))
    out.append(dna(480, 570, y, BOT, 5))
    out.append(t(185, y - 14, "fragment A", 12, TOP, anchor="middle"))
    out.append(t(525, y - 14, "fragment B", 12, BOT, anchor="middle"))
    out.append(t(360, y + 22, "far apart on the chromosome, close in the nucleus", 12, MUTE, anchor="middle"))
    # ligated molecule
    yy = 140
    out.append(dna(250, 360, yy, TOP, 5))
    out.append(dna(360, 470, yy, BOT, 5))
    out.append(dot(360, yy, 6, HOT))
    out.append(t(360, yy + 28, "ligation junction", 12, HOT, anchor="middle"))
    out.append(rd(252, 312, yy - 14, TOP))
    out.append(rd(468, 408, yy - 14, BOT))
    out.append(line(262, yy - 20, 205, y + 6, TOP, 1.2, dash="3 3"))
    out.append(line(458, yy - 20, 505, y + 6, BOT, 1.2, dash="3 3"))
    out.append(t(30, 214, "Read 1 aligns to A and read 2 aligns to B. A normal fragment would put "
                          "both reads side by side.", 12.5, INK))
    out.append(t(30, 236, "Count such pairs between every two places in the genome: that is the "
                          "contact map.", 12.5, HOT))
    return svg(720, 252, "".join(out))


def fig_four_steps():
    out = [t(30, 24, "Proximity ligation: the block, in four moves.", 14, INK)]
    steps = [("1  crosslink", "formaldehyde holds\nneighbours together"),
             ("2  digest", "cut the DNA into\nfragments"),
             ("3  ligate", "join ends that are\nheld close together"),
             ("4  pull down", "keep the molecules\nwith a junction")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 168
        out.append(step_box(x, 40, 150, 66, h, b))
        if i < 3:
            out.append(arrow(x + 153, 73, x + 166, MUTE))
    ys = 176
    out.append(t(30, 128, "what the DNA looks like", 12, MUTE))
    out.append(curve("M 40 176 C 60 146, 100 146, 120 176", TOP, 3))
    out.append(curve("M 40 191 C 60 221, 100 221, 120 191", BOT, 3))
    out.append(dot(80, 184, 6, HOT))
    out.append(dna(210, 245, ys, TOP, 3))
    out.append(dna(255, 290, ys, TOP, 3))
    out.append(dna(210, 245, ys + 22, BOT, 3))
    out.append(dna(255, 290, ys + 22, BOT, 3))
    out.append(cut(250, ys + 11, HOT, 9))
    out.append(dna(380, 460, ys + 6, TOP, 3))
    out.append(dna(380, 460, ys + 22, BOT, 3))
    out.append(dot(420, ys + 14, 5, HOT))
    out.append(dna(560, 640, ys + 14, TOP, 3))
    out.append(dot(600, ys + 14, 5, OK))
    out.append(t(600, ys + 38, "junction kept", 12, OK, anchor="middle"))
    out.append(t(30, 252, "Every protocol below changes one of these four moves: how it is held, "
                          "what cuts, how it is joined, what is selected.", 12.5, INK))
    return svg(720, 268, "".join(out))


def fig_dilution():
    out = [t(30, 24, "Ligate what was close, not what met by chance.", 14, INK)]
    cols = ["concentrated lysate", "dilute lysate", "inside intact nuclei"]
    for k, lab in enumerate(cols):
        x0 = 30 + k * 224
        out.append(t(x0 + 100, 52, lab, 13, INK, anchor="middle", weight="bold"))
        if k == 2:
            out.append(f'<ellipse cx="{x0 + 100}" cy="122" rx="92" ry="52" fill="{PALE_B}" '
                       f'stroke="{TOP}" stroke-width="1.4"/>')
        pts = {0: [(40, 100), (70, 105), (100, 98), (130, 110), (160, 100), (60, 135), (90, 140),
                   (125, 132), (155, 140), (80, 122), (140, 122)],
               1: [(20, 90), (100, 100), (170, 90), (40, 150), (115, 145), (175, 150)],
               2: [(50, 100), (75, 110), (120, 96), (145, 112), (65, 140), (100, 136), (140, 140)]}[k]
        for j, (px, py) in enumerate(pts):
            col = TOP if j % 2 == 0 else BOT
            out.append(line(x0 + px - 10, py + 10, x0 + px + 10, py + 10, col, 4, cap="round"))
        if k == 2:
            out.append(dot(x0 + 75, 121, 4, HOT))
            out.append(dot(x0 + 120, 107, 4, HOT))
    out.append(t(30, 216, "Concentrated: ends meet at random, so most junctions are noise. "
                          "Dilute: one-molecule events, but the neighbours have drifted apart.", 12.5, INK))
    out.append(t(30, 238, "In nuclei: the crosslinked structure is still intact when ligase "
                          "acts, so random joins are rare.", 12.5, HOT))
    return svg(720, 254, "".join(out))


def fig_3c():
    out = [t(30, 24, "3C: is this one place in contact with that one?", 14, INK)]
    y = 70
    out.append(dna(40, 300, y, TOP, 5))
    out.append(dna(300, 600, y, BOT, 5))
    out.append(dot(300, y, 6, HOT))
    out.append(t(300, y - 14, "junction", 12, HOT, anchor="middle"))
    out.append(rd(150, 230, y + 24, TOP))
    out.append(rd(450, 370, y + 24, BOT))
    out.append(t(150, y + 50, "forward primer, fragment A", 12, TOP))
    out.append(t(450, y + 50, "reverse primer, fragment B", 12, BOT, anchor="end"))
    out.append(t(30, 164, "A PCR product exists only if A and B were ligated, which happened only if they were close.", 12.5, INK))
    out.append(t(30, 186, "Read out by qPCR or a gel, one pair of primers at a time: one-versus-one.", 12.5, INK))
    out.append(t(30, 212, "Dekker et al. 2002 introduced the method.", 12.5, MUTE))
    return svg(720, 226, "".join(out))


def fig_4c():
    out = [t(30, 24, "4C: fix one viewpoint, find everything it touches.", 14, INK)]
    steps = [("1  3C library", "digest with enzyme 1,\nligate, reverse"),
             ("2  cut again", "enzyme 2 shortens\nthe fragments"),
             ("3  circularise", "dilute ligation makes\nsmall circles"),
             ("4  inverse PCR", "primers in the\nviewpoint, facing out")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 168
        out.append(step_box(x, 40, 150, 66, h, b))
        if i < 3:
            out.append(arrow(x + 153, 73, x + 166, MUTE))
    cx, cy = 200, 188
    out.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<path d="M {cx - 38} {cy} A 38 38 0 0 1 {cx} {cy - 38}" fill="none" stroke="{TOP}" stroke-width="5"/>')
    out.append(f'<path d="M {cx} {cy - 38} A 38 38 0 0 1 {cx + 38} {cy}" fill="none" stroke="{BOT}" stroke-width="5"/>')
    out.append(t(cx - 46, cy - 40, "viewpoint", 12, TOP, anchor="end"))
    out.append(t(cx + 46, cy - 40, "unknown partner", 12, BOT))
    out.append(arrow(cx - 30, cy - 52, cx - 4, TOP))
    out.append(t(330, 168, "The primers lie in the known viewpoint, but read outward across the junction", 12.5, INK))
    out.append(t(330, 190, "into whatever it was ligated to. Result: one viewpoint, all partners.", 12.5, INK))
    out.append(t(330, 216, "Zhao et al. 2006; Simonis et al. 2006", 12, MUTE))
    return svg(720, 240, "".join(out))


def fig_hic_junction():
    out = [t(30, 24, "Hi-C: mark the junction with biotin so you can find it.", 14, INK)]
    X = 40
    rows = []
    # row 1: after HindIII
    out.append(t(X, 52, "HindIII cuts A^AGCTT and leaves 5' overhangs", 12.5, INK))
    s, w = seq(X + 40, 90, "GGCA", TOP)
    out.append(s)
    s, _ = seq(X + 40, 120, "CCGTTCGA", BOT)
    out.append(s)
    s, _ = seq(X + 40 + 9 * DX, 90, "AGCTTCGG", TOP)
    out.append(s)
    s, _ = seq(X + 40 + 9 * DX + 4 * DX, 120, "AGCC", BOT)
    out.append(s)
    out.append(t(X + 40 + 4 * DX, 142, "AGCT overhangs, 5' on each side", 11.5, MUTE))
    check_pairing("GGCA    ", "CCGTTCGA")
    check_pairing("    TCGG", "    AGCC")
    # row 2: fill-in
    y0 = 180
    out.append(t(X, y0 - 30, "Klenow fills in the overhangs with biotinylated nucleotide", 12.5, INK))
    s, _ = seq(X + 40, y0, "GGCA", TOP)
    out.append(s)
    s, _ = seq(X + 40 + 4 * DX, y0, "AGCT", HOT)
    out.append(s)
    s, _ = seq(X + 40, y0 + 30, "CCGTTCGA", BOT)
    out.append(s)
    s, _ = seq(X + 40 + 9 * DX, y0, "AGCTTCGG", TOP)
    out.append(s)
    s, _ = seq(X + 40 + 9 * DX, y0 + 30, "TCGA", HOT)
    out.append(s)
    s, _ = seq(X + 40 + 13 * DX, y0 + 30, "AGCC", BOT)
    out.append(s)
    check_pairing("GGCAAGCT", "CCGTTCGA")
    check_pairing("AGCTTCGG", "TCGAAGCC")
    out.append(dot(X + 40 + 5 * DX, y0 - 20, 4, OK))
    out.append(t(X + 40 + 5 * DX + 10, y0 - 17, "biotin", 11, OK))
    # row 3: ligated
    y1 = 280
    out.append(t(X, y1 - 30, "Blunt ligation joins the ends; the junction contains biotin", 12.5, INK))
    s, _ = seq(X + 40, y1, "GGCAAGCTAGCTTCGG", TOP)
    out.append(s)
    s, _ = seq(X + 40, y1 + 30, "CCGTTCGATCGAAGCC", BOT)
    out.append(s)
    check_pairing("GGCAAGCTAGCTTCGG", "CCGTTCGATCGAAGCC")
    out.append(f'<rect x="{X + 40 + 3 * DX - 3}" y="{y1 - 15}" width="{10 * DX + 6}" height="52" '
               f'fill="none" stroke="{HOT}" stroke-width="1.3" stroke-dasharray="4 3" rx="4"/>')
    out.append(t(X + 40 + 8 * DX, y1 + 64, "new site AAGCTAGCTT; it contains GCTAGC (NheI)", 12, HOT, anchor="middle"))
    out.append(t(30, y1 + 88, "The biotin sits inside the joined DNA, at the junction,", 12.5, INK))
    out.append(t(30, y1 + 108, "so streptavidin can hold the junction and nothing else.", 12.5, INK))
    return svg(720, y1 + 124, "".join(out))


def fig_pulldown():
    out = [t(30, 24, "Most DNA in the tube is not a junction.", 14, INK)]
    rows = [("junction fragment", True, OK, "kept: biotin in the middle"),
            ("unligated fragment", False, MUTE, "no biotin: washed away"),
            ("dangling end, biotin at the end", False, MUTE, "stripped or sequenced as noise")]
    for i, (lab, jn, c, note) in enumerate(rows):
        y = 70 + i * 52
        out.append(dna(40, 240, y, TOP if i == 0 else MUTE, 4))
        if i == 0:
            out.append(dna(240, 400, y, BOT, 4))
            out.append(dot(240, y, 6, OK))
        if i == 2:
            out.append(dot(40, y, 6, OK))
        out.append(t(430, y - 6, lab, 12.5, INK))
        out.append(t(430, y + 12, note, 12, c))
    out.append(box(40, 214, 230, 30, "streptavidin beads hold the biotin", PALE_G, OK, 12, OK))
    out.append(t(290, 233, "wash hard, then release the DNA for the library", 12.5, INK))
    out.append(t(30, 272, "Hi-C libraries are mostly the first kind only because of this step. "
                          "Protocols vary in how they strip biotin from unligated ends.", 12.5, MUTE))
    return svg(720, 288, "".join(out))


def fig_matrix():
    out = [t(30, 24, "Count read pairs in bins and the map appears.", 14, INK)]
    n, c = 26, 8.2
    out.append(matrix(40, 44, n, c))
    out.append(t(40 + n * c / 2, 44 + n * c + 18, "position along chromosome", 12, MUTE, anchor="middle"))
    ax = 40 + n * c + 36
    notes = [("bright diagonal", "neighbours on the same fibre touch most", 70),
             ("fading with distance", "random polymer motion", 108),
             ("squares: TADs", "stretches that touch each other more than outside", 146),
             ("a dot: a loop", "two sites far apart that touch specifically", 184)]
    for a, b, yy in notes:
        out.append(t(ax, yy, a, 13, HOT, weight="bold"))
        out.append(t(ax, yy + 17, b, 12, INK))
    return svg(720, 280, "".join(out))


def fig_artifacts():
    out = [t(30, 24, "Not every read pair is a contact: look at where and which way.", 14, INK)]
    cuts = (60, 230, 400, 570)
    rows = [("valid pair", "two different fragments, any orientation", OK),
            ("dangling end", "both reads on one fragment, facing inward: never ligated", BAD),
            ("self-circle", "both reads on one fragment, facing outward: ligated to itself", BAD)]
    for i, (lab, note, c) in enumerate(rows):
        y = 70 + i * 62
        out.append(dna(40, 640, y, GREY, 4))
        for x in cuts:
            out.append(line(x, y - 9, x, y + 9, MUTE, 1.6))
        if i == 0:
            out.append(rd(70, 130, y - 12, TOP))
            out.append(rd(580, 520, y - 12, BOT))
        elif i == 1:
            out.append(rd(240, 290, y - 12, TOP))
            out.append(rd(390, 340, y - 12, BOT))
        else:
            out.append(rd(340, 290, y - 12, TOP))
            out.append(rd(300, 350, y + 14, BOT))
        out.append(t(40, y + 34, lab, 12.5, c, weight="bold"))
        out.append(t(140, y + 34, note, 12, INK))
    out.append(t(30, 270, "Ticks are restriction sites. Pairs inside one fragment, or very close with "
                          "unusual orientation, are filtered out.", 12.5, MUTE))
    return svg(720, 286, "".join(out))


def fig_insitu():
    out = [t(30, 24, "In situ Hi-C: do every enzymatic step inside intact nuclei.", 14, INK)]
    steps = [("1  crosslink", "cells, 1%\nformaldehyde"),
             ("2  permeabilise", "mild detergent;\nnuclei stay whole"),
             ("3  MboI", "4-cutter, GATC,\nin the nucleus"),
             ("4  biotin fill-in", "mark the ends,\nin the nucleus"),
             ("5  ligate", "in the nucleus"),
             ("6  release", "reverse, shear,\nstreptavidin")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 113
        out.append(step_box(x, 40, 103, 70, h, b, size=11))
        if i < 5:
            out.append(arrow(x + 105, 75, x + 112, MUTE, head=4))
    out.append(f'<ellipse cx="360" cy="170" rx="200" ry="46" fill="{PALE_B}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(t(360, 156, "the nucleus is the reaction vessel", 12.5, TOP, anchor="middle"))
    out.append(t(360, 180, "no dilution needed: each fragment is still held in place", 12, INK, anchor="middle"))
    out.append(t(30, 240, "Compared with the original, in-solution protocol this gives fewer random "
                          "ligations and more informative pairs per read.", 12.5, INK))
    return svg(720, 256, "".join(out))


def fig_resolution():
    out = [t(30, 24, "The cutter sets how fine the map can be.", 14, INK)]
    rows = [("6-cutter, e.g. HindIII", 4096, "one cut per ~4 kb on average"),
            ("4-cutter, e.g. MboI", 256, "one cut per ~256 bp"),
            ("MNase (Micro-C)", 0, "cuts linkers: one piece per nucleosome")]
    for i, (lab, sp, note) in enumerate(rows):
        y = 64 + i * 54
        out.append(dna(40, 600, y, GREY, 4))
        if sp == 4096:
            xs = [60, 230, 380, 560]
        elif sp == 256:
            xs = list(range(52, 600, 26))
        else:
            xs = list(range(52, 600, 20))
        for x in xs:
            out.append(line(x, y - 8, x, y + 8, HOT, 1.8))
        out.append(t(612, y - 3, lab, 12, INK))
        out.append(t(612, y + 13, note, 11.5, MUTE))
    out.append(t(30, 232, "In a random sequence an n-base site occurs once per 4^n bases; real genomes "
                          "deviate, and sites cluster unevenly.", 12.5, INK))
    out.append(t(30, 254, "A fragment is the smallest unit of the map, so fragment length is the "
                          "limit on resolution.", 12.5, HOT))
    return svg(720, 270, "".join(out))


def fig_microc():
    out = [t(30, 24, "Micro-C: cut with MNase, so the unit is the nucleosome.", 14, INK)]
    steps = [("1  fix", "formaldehyde, then\nDSG as well"),
             ("2  MNase", "digest to\nmononucleosomes"),
             ("3  repair + biotin", "make blunt ends,\nlabel them"),
             ("4  ligate", "join neighbouring\nnucleosomes"),
             ("5  pull down", "streptavidin, then\nlibrary")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 70, h, b))
        if i < 4:
            out.append(arrow(x + 120, 75, x + 134, MUTE))
    y = 164
    out.append(dna(30, 690, y, MUTE, 2.4))
    for x in (70, 130, 190, 250, 310, 370, 430, 490, 550, 610):
        out.append(nuc(x, y, 14))
    out.append(t(30, 212, "No fixed restriction site, so a junction can fall between any two "
                          "nucleosomes, and the ends are mixed: repair first.", 12.5, INK))
    out.append(t(30, 234, "The result resolves features finer than a restriction digest can: "
                          "single enhancer-promoter contacts, stripes, nucleosome-scale structure.", 12.5, HOT))
    return svg(720, 250, "".join(out))


def fig_features():
    out = [t(30, 24, "What the pattern means.", 14, INK)]
    n, c = 26, 8
    # triangular plot
    out.append(f'<g transform="translate(60,196) rotate(-45) scale(1)">')
    for i in range(n):
        for j in range(i, n):
            a = contact(i, j)
            out.append(f'<rect x="{j * c}" y="{i * c}" width="{c + 0.3}" height="{c + 0.3}" '
                       f'fill="{blend(TOP, a)}"/>')
    out.append("</g>")
    out.append(t(111, 190, "TAD", 12, INK, anchor="middle"))
    out.append(t(213, 190, "TAD", 12, INK, anchor="middle"))
    out.append(t(309, 190, "TAD", 12, INK, anchor="middle"))
    out.append(t(207, 112, "loop dot", 12, HOT, anchor="middle"))
    out.append(line(207, 118, 207, 144, HOT, 1.2, dash="3 3"))
    # loop extrusion cartoon
    bx = 400
    out.append(curve(f"M {bx} 190 L {bx + 40} 190 C {bx + 60} 190, {bx + 60} 110, {bx + 120} 110 "
                     f"C {bx + 180} 110, {bx + 180} 190, {bx + 200} 190 L {bx + 290} 190", MUTE, 3))
    out.append(f'<circle cx="{bx + 120}" cy="150" r="14" fill="none" stroke="{BAD}" stroke-width="3"/>')
    out.append(t(bx + 120, 96, "cohesin extrudes the loop", 12, BAD, anchor="middle"))
    for x, d in ((bx + 40, 1), (bx + 200, -1)):
        out.append(f'<path d="M {x} 208 L {x + 14 * d} 200 L {x} 192 Z" fill="{OK}"/>')
    out.append(t(bx + 120, 232, "CTCF sites, facing each other, stop it", 12, OK, anchor="middle"))
    out.append(t(30, 256, "Compartments (not drawn) are a separate, coarser plaid pattern: active "
                          "and inactive chromatin each prefer their own kind.", 12.5, INK))
    return svg(720, 272, "".join(out))


def fig_hichip():
    out = [t(30, 24, "HiChIP: make contacts first, then select the ones a protein is part of.", 14, INK)]
    steps = [("1  contacts", "in situ: MboI,\nbiotin fill, ligate"),
             ("2  shear", "sonicate the\nnuclei"),
             ("3  ChIP", "antibody to H3K27ac,\ncohesin, a TF"),
             ("4  reverse", "free the DNA;\nbiotin capture"),
             ("5  tagment", "Tn5 on the\nbead, PCR")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 70, h, b))
        if i < 4:
            out.append(arrow(x + 120, 75, x + 134, MUTE))
    y = 164
    out.append(dna(40, 300, y, MUTE, 3))
    out.append(dna(340, 600, y, MUTE, 3))
    out.append(curve(f"M 220 {y} C 240 {y - 60}, 400 {y - 60}, 420 {y}", TOP, 3))
    out.append(box(205, y + 6, 30, 14, "", PALE_R, BAD))
    out.append(t(30, 212, "Only contacts anchored at the protein you chose survive the pull-down. "
                          "A Hi-C library has to be deep to see the same thing.", 12.5, INK))
    out.append(t(30, 234, "The map is no longer unbiased: peaks of the target protein shape the pattern.", 12.5, HOT))
    return svg(720, 250, "".join(out))


def fig_bridge():
    out = [t(30, 24, "A bridge linker makes the junction a known sequence.", 14, INK)]
    y = 64
    out.append(t(30, y - 18, "direct ligation: the junction is just two ends joined", 12.5, INK, weight="bold"))
    out.append(dna(40, 300, y + 10, TOP, 4))
    out.append(dna(300, 560, y + 10, BOT, 4))
    out.append(t(300, y + 36, "no mark", 11.5, MUTE, anchor="middle"))
    y2 = 150
    out.append(t(30, y2 - 22, "bridge linker: two ligations through a short biotinylated duplex", 12.5, INK, weight="bold"))
    out.append(dna(40, 280, y2 + 10, TOP, 4))
    out.append(box(280, y2 + 1, 70, 18, "linker", PALE_G, OK, 11.5, OK))
    out.append(dot(315, y2 - 6, 4, OK))
    out.append(dna(350, 590, y2 + 10, BOT, 4))
    out.append(t(315, y2 + 40, "biotin and a sequence we chose", 11.5, OK, anchor="middle"))
    out.append(t(30, 232, "Pull-down and junction detection no longer depend on a restriction site, "
                          "so nearly any cut will do, and the linker can carry other cargo.", 12.5, INK))
    out.append(t(30, 254, "The linker can also join DNA to something that is not DNA: an RNA, for example.", 12.5, HOT))
    return svg(720, 270, "".join(out))


def fig_rna():
    out = [t(30, 24, "RNA–chromatin contacts: the bridge carries RNA to DNA.", 14, INK)]
    y = 150
    out.append(dna(40, 700, y, MUTE, 3))
    out.append(nuc(150, y, 12))
    out.append(nuc(190, y, 12))
    # RNA, bridge, DNA read
    out.append(curve(f"M 300 {y - 30} C 330 {y - 90}, 420 {y - 90}, 440 {y - 50}", BAD, 3))
    out.append(t(350, y - 100, "chromatin-associated RNA", 12, BAD, anchor="middle"))
    out.append(box(436, y - 56, 56, 18, "bridge", PALE_G, OK, 11.5, OK))
    out.append(dot(464, y - 62, 4, OK))
    out.append(line(464, y - 38, 464, y - 2, TOP, 3))
    out.append(t(480, y - 20, "DNA nearby", 12, TOP))
    out.append(t(30, 204, "1  fragment the RNA in fixed nuclei; join its 3' end to one end of the bridge", 12.5, INK))
    out.append(t(30, 224, "2  cut the DNA and join the other end of the bridge to it", 12.5, INK))
    out.append(t(30, 244, "3  reverse-transcribe, capture the biotin, sequence: one read = RNA part + DNA part", 12.5, INK))
    out.append(t(30, 276, "ChAR-seq, GRID-seq and iMARGI differ mainly in the design of the bridge and in the enzymes used.", 12.5, MUTE))
    return svg(720, 292, "".join(out))


def fig_sprite():
    out = [t(30, 24, "SPRITE: no ligation between neighbours, only shared barcodes.", 14, INK)]
    out.append(t(30, 52, "crosslinked complexes on beads: three, each with several DNA pieces", 12.5, INK))
    comps = [(90, TOP), (260, HOT), (430, OK)]
    for cx, c in comps:
        for k in range(3):
            out.append(line(cx - 30 + k * 26, 78 + (k % 2) * 8, cx - 10 + k * 26, 78 + (k % 2) * 8, c, 4, cap="round"))
        out.append(f'<ellipse cx="{cx}" cy="84" rx="48" ry="18" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    out.append(t(30, 128, "round 1: split into 96 wells, ligate a tag; pool. Round 2: split again, tag again; pool ...", 12.5, INK))
    chains = [("A7 · B3 · C12 · D5", TOP), ("A41 · B88 · C2 · D60", HOT), ("A19 · B9 · C77 · D31", OK)]
    for i, (s, c) in enumerate(chains):
        x = 40 + i * 190
        out.append(box(x, 150, 168, 22, s, "#fbfbf9", c, 12, c))
    out.append(t(30, 204, "Every piece in one complex carries the same tag chain. Reads with the same chain "
                          "come from one complex.", 12.5, INK))
    out.append(t(30, 228, "Complexes of 2 pieces or of 200 are both captured: clusters, not pairs.", 12.5, HOT))
    return svg(720, 244, "".join(out))


def fig_gam():
    out = [t(30, 24, "GAM: slice the nucleus, sequence the slices, and count who turns up together.", 14, INK)]
    out.append(f'<circle cx="110" cy="120" r="74" fill="{PALE_B}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(f'<rect x="96" y="40" width="28" height="160" fill="{PALE_R}" stroke="{HOT}" stroke-width="1.2"/>')
    out.append(dot(110, 90, 6, TOP))
    out.append(dot(110, 120, 6, BOT))
    out.append(dot(70, 150, 6, OK))
    out.append(t(122, 92, "A", 12, TOP))
    out.append(t(122, 124, "B", 12, BOT))
    out.append(t(76, 170, "C", 12, OK))
    out.append(t(110, 214, "a thin slice through one nucleus", 12, HOT, anchor="middle"))
    # table
    x0, y0 = 300, 60
    out.append(t(x0 - 10, y0 - 12, "slice:", 12, MUTE, anchor="end"))
    pat = {"A": [1, 1, 0, 1, 1, 0, 1, 0], "B": [1, 1, 0, 1, 1, 0, 1, 0], "C": [0, 1, 1, 0, 0, 1, 0, 1]}
    cols = {"A": TOP, "B": BOT, "C": OK}
    for r, k in enumerate("ABC"):
        yy = y0 + r * 34
        out.append(t(x0 - 10, yy + 16, k, 13, cols[k], anchor="end", weight="bold"))
        for j in range(8):
            fill = cols[k] if pat[k][j] else "none"
            out.append(f'<rect x="{x0 + j * 40}" y="{yy}" width="30" height="24" rx="3" fill="{fill}" '
                       f'stroke="{MUTE}" stroke-width="1"/>')
    for j in range(8):
        out.append(t(x0 + j * 40 + 15, y0 - 12, str(j + 1), 11.5, MUTE, anchor="middle"))
    out.append(t(x0, 190, "A and B are found together in the same slices far more often than chance", 12.5, INK))
    out.append(t(x0, 210, "would give: they are close in space. C is not tied to them.", 12.5, INK))
    out.append(t(30, 250, "Each slice is cut out by laser, its DNA amplified and sequenced: no crosslinking "
                          "to ligate, no restriction enzyme, only co-detection.", 12.5, HOT))
    return svg(720, 266, "".join(out))


def fig_reads_all():
    out = [t(30, 24, "What one read, or read pair, means.", 14, INK)]
    rows = [("Hi-C", "two ends of a ligated molecule: a pairwise contact"),
            ("in situ Hi-C", "the same, with fewer random joins"),
            ("Micro-C", "the same at nucleosome resolution"),
            ("4C-seq", "one viewpoint joined to a partner"),
            ("HiChIP", "a contact, anchored at a protein-bound site"),
            ("ChAR-seq", "an RNA joined to a nearby DNA piece"),
            ("SPRITE", "a DNA piece; same barcodes = same complex"),
            ("GAM", "a window present in one slice; co-presence = contact")]
    for i, (a, b) in enumerate(rows):
        yy = 46 + i * 28
        out.append(box(30, yy - 14, 110, 22, a, PALE_B, TOP, 12, TOP))
        out.append(t(152, yy + 2, b, 12.5, INK))
    return svg(720, 270, "".join(out))


def fig_choose():
    out = [t(30, 24, "Pick the method from the question.", 14, INK)]
    rows = [("Where are TADs and compartments genome-wide?", "Hi-C or in situ Hi-C", 50),
            ("Which enhancers touch this one gene?", "4C-seq, Capture-C", 90),
            ("Fine-scale loops and stripes?", "Micro-C", 130),
            ("Contacts at active enhancers, from few cells?", "HiChIP", 170),
            ("Many-way contacts, and what is at a nuclear body?", "SPRITE, GAM", 210),
            ("Which RNAs sit on which DNA?", "ChAR-seq, GRID-seq, iMARGI", 250)]
    for q, m, yy in rows:
        out.append(box(30, yy - 16, 340, 28, q, "#fbfbf9", MUTE, 12.5, INK))
        out.append(arrow(376, yy - 2, 402, MUTE))
        out.append(box(408, yy - 16, 282, 28, m, PALE_G, OK, 12.5, OK))
    return svg(720, 278, "".join(out))


build(__file__, [
    ("question", fig_question),
    ("junction-read", fig_junction_read),
    ("four-steps", fig_four_steps),
    ("dilution", fig_dilution),
    ("3c", fig_3c),
    ("4c", fig_4c),
    ("hic-junction", fig_hic_junction),
    ("pulldown", fig_pulldown),
    ("matrix", fig_matrix),
    ("artifacts", fig_artifacts),
    ("insitu", fig_insitu),
    ("resolution", fig_resolution),
    ("microc", fig_microc),
    ("features", fig_features),
    ("hichip", fig_hichip),
    ("bridge", fig_bridge),
    ("rna", fig_rna),
    ("sprite", fig_sprite),
    ("gam", fig_gam),
    ("reads-all", fig_reads_all),
    ("choose", fig_choose),
])
