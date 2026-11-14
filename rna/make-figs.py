#!/usr/bin/env python3
"""Figures for the RNA unit.  Run: python3 rna/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

RNA = "#7a3b5e"      # RNA strands
CDNA = TOP           # first-strand cDNA
NEW = HOT            # newly synthesised / the thing to look at
TB, TR, TG, TY = "#e8eef5", "#f5eae6", "#e9f1ea", "#f6f0e0"


def lab(x, y, s, size=12, col=MUTE, anchor="start"):
    return t(x, y, s, size, col, anchor=anchor)


def strand(x1, x2, y, col=RNA, w=3.2):
    return line(x1, y, x2, y, col, w, cap="butt")


def polya(x, y, n=5, col=RNA):
    return t(x, y + 4, "A" * n, 11, col, family=MONO)


def capdot(x, y):
    return dot(x, y, 4.5, HOT)


def scissors(x, y, col=BAD):
    return (line(x - 5, y - 6, x + 5, y + 6, col, 1.8) + line(x - 5, y + 6, x + 5, y - 6, col, 1.8))


# ------------------------------------------------------------------ deck 1

def fig_classes():
    rows = [
        ("rRNA (28S, 18S, 5.8S, 5S)", "0.12 to 5 kb", "no", "no", 0.80, "~80%"),
        ("tRNA", "70 to 90 nt", "no", "no", 0.12, "~10%"),
        ("mRNA", "0.5 to 10 kb", "yes", "yes", 0.04, "1 to 5%"),
        ("histone mRNA", "~0.5 kb", "yes", "no", 0.01, "small"),
        ("lncRNA", "0.2 to >10 kb", "yes", "mostly", 0.01, "small"),
        ("miRNA", "21 to 23 nt", "no", "no", 0.005, "under 1%"),
        ("circRNA", "100 nt to kb", "no", "no", 0.005, "small"),
    ]
    out = [t(40, 26, "Total RNA from a mammalian cell: what is there, and which handles it carries.",
             14, INK)]
    xs = [40, 250, 370, 440, 520]
    for x, h in zip(xs, ["class", "length", "5' cap", "poly(A)", "share of total RNA (approximate)"]):
        out.append(lab(x, 52, h, 12.5, MUTE))
    out.append(line(40, 58, 740, 58, MUTE, 1))
    for i, (n, ln, c, p, share, lbl) in enumerate(rows):
        y = 82 + i * 28
        hot = n == "mRNA"
        out.append(t(40, y, n, 13.5, HOT if hot else INK, weight="bold" if hot else None))
        out.append(t(250, y, ln, 13, INK))
        for x, v in ((370, c), (440, p)):
            out.append(t(x, y, v, 13, OK if v == "yes" else (BAD if v == "no" else HOT)))
        out.append(f'<rect x="520" y="{y - 11}" width="{max(3, share * 190):.0f}" height="13" '
                   f'fill="{HOT if hot else BOT}" opacity="0.8"/>')
        out.append(t(520 + max(3, share * 190) + 8, y, lbl, 12, MUTE))
    out.append(t(40, 294, "Poly(A) selection keeps one row and loses every 'no' in the poly(A) column; "
                          "depletion keeps them all.", 14, HOT))
    return svg(760, 312, "".join(out))


def fig_removal():
    out = []
    titles = ["1. oligo-dT capture", "2. RNase H depletion", "3. probes and beads", "4. Cas9 on cDNA"]
    for p in range(4):
        x0 = 30 + p * 225
        out.append(t(x0 + 100, 26, titles[p], 13.5, INK, anchor="middle", weight="bold"))
        out.append(box(x0, 38, 200, 124, "", "#fbfbf9", MUTE))
    # panel 1: bead holds mRNA through its poly(A)
    x0 = 30
    out.append(f'<circle cx="{x0+34}" cy="100" r="16" fill="{TB}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(lab(x0 + 34, 104, "dT", 11, TOP, "middle"))
    out.append(strand(x0 + 52, x0 + 160, 100))
    out.append(t(x0 + 140, 90, "AAAA", 10, RNA, family=MONO))
    out.append(lab(x0 + 104, 124, "mRNA held", 11.5, OK, "middle"))
    out.append(strand(x0 + 70, x0 + 180, 148, MUTE, 2.4))
    out.append(lab(x0 + 22, 152, "rRNA", 11.5, BAD))
    out.append(lab(x0 + 100, 70, "rRNA washed away", 11.5, BAD, "middle"))
    # panel 2: DNA oligos + RNase H
    x0 = 255
    out.append(strand(x0 + 14, x0 + 186, 70, MUTE, 3))
    out.append(lab(x0 + 100, 56, "rRNA", 11.5, MUTE, "middle"))
    for i in range(6):
        out.append(line(x0 + 18 + i * 28, 78, x0 + 38 + i * 28, 78, CDNA, 3))
    out.append(lab(x0 + 100, 100, "tiled DNA oligos", 11.5, CDNA, "middle"))
    for i in range(1, 6):
        out.append(scissors(x0 + 15 + i * 28, 128))
    out.append(strand(x0 + 14, x0 + 186, 128, MUTE, 3))
    out.append(lab(x0 + 100, 152, "RNase H cuts the RNA", 11.5, BAD, "middle"))
    # panel 3: biotin probes + bead
    x0 = 480
    out.append(strand(x0 + 14, x0 + 120, 76, MUTE, 3))
    out.append(line(x0 + 40, 76, x0 + 40, 92, CDNA, 1.6))
    out.append(line(x0 + 80, 76, x0 + 80, 92, CDNA, 1.6))
    out.append(f'<circle cx="{x0+160}" cy="96" r="16" fill="{TG}" stroke="{OK}" stroke-width="1.4"/>')
    out.append(lab(x0 + 160, 100, "strept.", 9.5, OK, "middle"))
    out.append(line(x0 + 40, 92, x0 + 144, 96, CDNA, 1.2, dash="3 3"))
    out.append(lab(x0 + 100, 58, "biotinylated probes on rRNA", 11, MUTE, "middle"))
    out.append(strand(x0 + 14, x0 + 100, 138, RNA, 3))
    out.append(lab(x0 + 100, 156, "everything else stays", 11.5, OK, "middle"))
    out.append(lab(x0 + 14, 124, "pulled down with the bead", 11.5, BAD))
    # panel 4: Cas9 on cDNA
    x0 = 705
    out.append(box(x0 + 12, 70, 20, 12, "", TB, TOP))
    out.append(strand(x0 + 32, x0 + 160, 76, MUTE, 3))
    out.append(box(x0 + 160, 70, 20, 12, "", TR, BAD))
    out.append(scissors(x0 + 96, 76, HOT))
    out.append(lab(x0 + 100, 58, "adapter-flanked rRNA cDNA", 10.5, MUTE, "middle"))
    out.append(box(x0 + 12, 104, 20, 12, "", TB, TOP))
    out.append(strand(x0 + 32, x0 + 160, 110, RNA, 3))
    out.append(box(x0 + 160, 104, 20, 12, "", TR, BAD))
    out.append(lab(x0 + 100, 132, "mRNA cDNA is not cut", 11.5, OK, "middle"))
    out.append(lab(x0 + 100, 152, "cut ones cannot be PCR'd", 11.5, BAD, "middle"))
    for p, (k, l) in enumerate([("keeps", "polyadenylated RNA only"),
                                ("keeps", "any RNA without a probe site"),
                                ("keeps", "any RNA without a probe site"),
                                ("keeps", "decided after RT, before PCR")]):
        x0 = 30 + p * 225
        out.append(lab(x0 + 100, 184, l, 11.5, INK, "middle"))
    out.append(t(30, 218, "All four remove the same 80 to 90% of reads. They differ in what else "
                          "they take and at which step they act.", 14, HOT))
    return svg(920, 236, "".join(out))


def fig_rnaseh():
    out = [t(40, 26, "RNase H depletion: DNA oligos define the target; only RNA in an RNA:DNA hybrid is cut.",
             14, INK)]
    steps = ["1. anneal DNA oligos tiled along the rRNA", "2. RNase H cuts the RNA strand",
             "3. DNase removes the oligos; beads clean up"]
    for i, s in enumerate(steps):
        y = 74 + i * 62
        out.append(lab(40, y - 22, s, 12.5, INK))
        out.append(strand(60, 660, y, MUTE, 3.2))
        out.append(lab(40, y + 4, "5'", 11, MUTE, "end"))
        out.append(lab(670, y + 4, "3'", 11, MUTE))
        out.append(lab(700, y + 4, "rRNA", 12, MUTE))
        if i < 2:
            for k in range(10):
                out.append(line(66 + k * 60, y + 7, 112 + k * 60, y + 7, CDNA, 3.2, cap="butt"))
        if i == 1:
            for k in range(1, 10):
                out.append(scissors(63 + k * 60, y - 12))
        if i == 2:
            for k in range(1, 10):
                out.append(f'<rect x="{60 + k*60 - 3}" y="{y - 6}" width="6" height="12" fill="#ffffff"/>')
    out.append(strand(60, 660, 262, RNA, 3.2))
    out.append(lab(700, 266, "mRNA", 12, RNA))
    out.append(lab(60, 286, "no oligo anneals, so no hybrid forms and RNase H leaves it alone", 12, OK))
    out.append(lab(60, 308, "Oligos must cover the whole rRNA: a gap leaves a fragment that survives and is still sequenced.",
                   13, HOT))
    return svg(780, 322, "".join(out))


def fig_dash():
    out = [t(40, 26, "Cas9 depletion acts on cDNA: cut what you do not want between RT and PCR.", 14, INK)]
    out.append(lab(40, 74, "1. adapter-flanked cDNA library,", 12.5, INK))
    out.append(lab(40, 92, "rRNA-derived molecules are most of it", 12.5, MUTE))
    y1, y2 = 72, 112
    out.append(box(300, y1 - 8, 22, 16, "", TB, TOP))
    out.append(strand(322, 520, y1, MUTE, 3))
    out.append(box(520, y1 - 8, 22, 16, "", TR, BAD))
    out.append(lab(560, y1 + 4, "rRNA cDNA", 12, MUTE))
    out.append(box(300, y2 - 8, 22, 16, "", TB, TOP))
    out.append(strand(322, 520, y2, RNA, 3))
    out.append(box(520, y2 - 8, 22, 16, "", TR, BAD))
    out.append(lab(560, y2 + 4, "mRNA cDNA", 12, RNA))
    out.append(lab(40, 158, "2. Cas9 with guides against rRNA", 12.5, INK))
    out.append(lab(40, 176, "cuts inside the insert", 12.5, MUTE))
    out.append(box(300, 148, 22, 16, "", TB, TOP))
    out.append(strand(322, 400, 156, MUTE, 3))
    out.append(scissors(411, 156, HOT))
    out.append(strand(422, 520, 156, MUTE, 3))
    out.append(box(520, 148, 22, 16, "", TR, BAD))
    out.append(lab(560, 160, "two pieces, each with one adapter", 12, BAD))
    out.append(lab(40, 212, "3. PCR with adapter primers", 12.5, INK))
    out.append(lab(40, 230, "needs an adapter at both ends", 12.5, MUTE))
    out.append(box(300, 202, 22, 16, "", TB, TOP))
    out.append(strand(322, 520, 210, RNA, 3))
    out.append(box(520, 202, 22, 16, "", TR, BAD))
    out.append(lab(560, 214, "amplified", 12, OK))
    out.append(lab(40, 254, "Cut pieces fail to amplify exponentially. No oligo, no hybrid, no bead: the target "
                            "is defined by the guide RNAs.", 13, HOT))
    return svg(800, 272, "".join(out))


def _cov(x0, y0, w, h, f, col, n=60):
    pts = [(x0 + w * i / n, y0 - h * f(i / n)) for i in range(n + 1)]
    d = "M %.1f %.1f " % (x0, y0) + " ".join("L %.1f %.1f" % p for p in pts) + " L %.1f %.1f Z" % (x0 + w, y0)
    return f'<path d="{d}" fill="{col}" opacity="0.75"/>'


def fig_bias():
    out = [t(40, 26, "Coverage along a transcript (5' to 3'): what the enrichment does to degraded RNA.",
             14, INK)]
    panels = [
        ("intact RNA, poly(A) selected", lambda x: 0.8 + 0.1 * math.sin(7 * x), OK),
        ("intact RNA, rRNA depleted", lambda x: 0.8 + 0.1 * math.sin(5 * x + 1), OK),
        ("degraded RNA, poly(A) selected", lambda x: 0.05 + 0.9 * x ** 4, BAD),
        ("degraded RNA, rRNA depleted", lambda x: 0.55 + 0.25 * math.sin(6 * x), OK),
    ]
    for i, (n, f, c) in enumerate(panels):
        x0 = 40 + (i % 2) * 330
        y0 = 120 + (i // 2) * 110
        out.append(lab(x0, y0 - 66, n, 12.5, INK))
        out.append(line(x0, y0, x0 + 280, y0, MUTE, 1))
        out.append(_cov(x0, y0, 280, 50, f, c))
        out.append(lab(x0, y0 + 14, "5'", 11, MUTE))
        out.append(lab(x0 + 270, y0 + 14, "3' AAAA", 11, MUTE))
    out.append(t(40, 262, "A fragment without a poly(A) tail is removed by the selection. If the RNA is cut, "
                          "only the 3' piece is kept.", 13.5, HOT))
    return svg(700, 280, "".join(out))


def fig_priming():
    out = [t(40, 26, "Where the first-strand primer anneals decides which part of the RNA becomes cDNA.",
             14, INK)]
    rows = ["oligo-dT, anchored", "random hexamers", "gene-specific"]
    for i, r in enumerate(rows):
        y = 70 + i * 66
        out.append(lab(40, y + 4, r, 13, INK))
        out.append(strand(220, 620, y, RNA, 3.2))
        out.append(capdot(216, y))
        out.append(t(626, y + 4, "AAAAAAAA", 10.5, RNA, family=MONO))
    # oligo-dT: primer on poly(A), cDNA extends 5'-ward
    out.append(line(626, 64, 704, 64, CDNA, 3.2, cap="butt"))
    out.append(t(706, 68, "TTTTVN", 10.5, CDNA, family=MONO))
    out.append(arrow(626, 58, 420, NEW))
    out.append(lab(520, 48, "one cDNA per mRNA, from the 3' end", 11.5, NEW, "middle"))
    # random hexamers
    ys = 136
    for k, xx in enumerate([250, 310, 380, 440, 500, 570]):
        out.append(line(xx, ys - 6, xx + 18, ys - 6, CDNA, 3.2, cap="butt"))
        out.append(arrow(xx, ys - 6, xx - 44, NEW, 1.4, 4))
    out.append(lab(420, ys + 22, "many short cDNAs, spread along the whole RNA", 11.5, NEW, "middle"))
    # gene-specific
    yg = 202
    out.append(line(420, yg - 6, 442, yg - 6, CDNA, 3.2, cap="butt"))
    out.append(arrow(420, yg - 6, 300, NEW))
    out.append(lab(420, yg + 22, "only the gene you asked about", 11.5, NEW, "middle"))
    out.append(t(40, 256, "VN anchor: without it, oligo-dT can anneal anywhere along the poly(A) tail "
                          "and the cDNA begins with a variable run of A.", 13, MUTE))
    out.append(t(40, 278, "Oligo-dT needs a tail. Hexamers do not, but they also prime on rRNA, "
                          "so total RNA gives rRNA reads.", 13, HOT))
    return svg(820, 296, "".join(out))


def fig_second():
    out = [t(40, 26, "Second strand: use the RNA you have as its own primer.", 14, INK)]
    titles = ["1. RNA:DNA hybrid", "2. RNase H nicks the RNA", "3. DNA Pol I extends and replaces",
              "4. ligase seals: ds cDNA"]
    for p in range(4):
        x0 = 36 + p * 200
        out.append(lab(x0, 56, titles[p], 12, INK))
        out.append(strand(x0, x0 + 170, 110, CDNA, 3.2))
        if p == 0:
            out.append(strand(x0, x0 + 170, 90, RNA, 3.2))
        elif p == 1:
            for a, b in ((0, 38), (44, 90), (98, 128), (134, 170)):
                out.append(strand(x0 + a, x0 + b, 90, RNA, 3.2))
            for xx in (41, 94, 131):
                out.append(scissors(x0 + xx, 78))
        elif p == 2:
            out.append(strand(x0, x0 + 38, 90, RNA, 3.2))
            out.append(strand(x0 + 38, x0 + 170, 90, NEW, 3.2))
            out.append(arrow(x0 + 38, 78, x0 + 150, NEW, 1.4))
        else:
            out.append(strand(x0, x0 + 170, 90, NEW, 3.2))
        if p == 3:
            out.append(lab(x0, 138, "cDNA now double-stranded", 11.5, OK))
    out.append(lab(40, 176, "RNA fragments left by RNase H act as primers (Gubler and Hoffman). "
                            "Pol I's 5' to 3' exonuclease replaces them.", 12.5, MUTE))
    out.append(t(40, 212, "The product carries the first-strand sequence on one strand and its complement on "
                          "the other, with no way to tell which was which.", 14, HOT))
    return svg(840, 232, "".join(out))


def fig_whystrand():
    out = [t(40, 26, "Two genes overlap on opposite strands. Which one made this read?", 14, INK)]
    out.append(lab(40, 62, "genome", 12, MUTE))
    out.append(strand(120, 660, 62, MUTE, 1.5))
    out.append(strand(220, 520, 80, TOP, 8))
    out.append(arrow(500, 80, 524, TOP, 1.6, 6))
    out.append(lab(224, 100, "gene A, sense strand", 11.5, TOP))
    out.append(strand(380, 640, 120, HOT, 8))
    out.append(arrow(400, 120, 376, HOT, 1.6, 6))
    out.append(lab(420, 140, "gene B, antisense, overlapping", 11.5, HOT))
    out.append(lab(40, 178, "unstranded", 12.5, INK))
    for k, xx in enumerate([410, 440, 470, 500]):
        out.append(strand(xx, xx + 26, 174, BAD, 5))
    out.append(lab(540, 178, "reads in the overlap: A or B? counted for both, or neither", 12, BAD))
    out.append(lab(40, 216, "stranded", 12.5, INK))
    for xx in (410, 440):
        out.append(strand(xx, xx + 26, 212, TOP, 5))
    for xx in (470, 500):
        out.append(strand(xx, xx + 26, 212, HOT, 5))
    out.append(lab(540, 216, "orientation of the read gives the gene", 12, OK))
    out.append(t(40, 252, "Many human genes have an overlapping antisense partner, "
                          "so this is not a corner case.", 13.5, MUTE))
    return svg(820, 270, "".join(out))


def fig_dutp():
    out = [t(40, 26, "dUTP in the second strand: the library remembers which strand was the RNA's complement.",
             14, INK)]
    out.append(lab(40, 62, "1. first strand: dATP dCTP dGTP dTTP (plus actinomycin D)", 12.5, INK))
    out.append(strand(60, 340, 82, RNA, 3.2))
    out.append(strand(60, 340, 96, CDNA, 3.2))
    out.append(lab(350, 90, "RNA + first-strand cDNA", 11.5, MUTE))
    out.append(lab(40, 128, "2. second strand: dUTP replaces dTTP", 12.5, INK))
    out.append(strand(60, 340, 148, CDNA, 3.2))
    out.append(strand(60, 340, 162, NEW, 3.2))
    for xx in range(80, 340, 38):
        out.append(t(xx, 175, "U", 9.5, HOT, family=MONO))
    out.append(lab(350, 156, "U-containing second strand", 11.5, HOT))
    out.append(lab(40, 198, "3. ligate adapters, then stop the U strand from being amplified", 12.5, INK))
    out.append(box(60, 206, 18, 30, "", TB, TOP))
    out.append(strand(78, 300, 214, CDNA, 3.2))
    out.append(box(300, 206, 18, 30, "", TR, BAD))
    out.append(strand(78, 300, 228, NEW, 3.2))
    out.append(lab(330, 222, "only the first-strand copy templates PCR", 11.5, OK))
    # right: read geometry
    out.append(lab(560, 62, "4. what the reads look like", 12.5, INK))
    out.append(strand(560, 800, 90, RNA, 4))
    out.append(lab(560, 78, "mRNA, sense", 11, RNA))
    out.append(strand(580, 800, 120, CDNA, 3.2))
    out.append(arrow(700, 140, 600, CDNA, 1.8))
    out.append(lab(710, 144, "read 1: antisense to mRNA", 11.5, CDNA))
    out.append(arrow(640, 170, 740, HOT, 1.8))
    out.append(lab(560, 190, "read 2: sense", 11.5, HOT))
    out.append(lab(560, 218, "TruSeq Stranded mRNA and NEBNext Ultra II", 11.5, MUTE))
    out.append(lab(560, 234, "Directional give this orientation", 11.5, MUTE))
    return svg(840, 244, "".join(out))


def fig_twoways():
    out = [t(40, 26, "Two ways to silence the U-marked strand after adapter ligation.", 14, INK)]
    for p, (title, sub, col) in enumerate([
            ("TruSeq Stranded mRNA", "polymerase cannot read through dU", TG),
            ("NEBNext Ultra II Directional", "USER enzyme cuts at the dU", TB)]):
        x0 = 40 + p * 400
        out.append(box(x0, 40, 360, 160, "", col, MUTE))
        out.append(t(x0 + 180, 62, title, 13.5, INK, anchor="middle", weight="bold"))
        out.append(box(x0 + 30, 84, 16, 12, "", TB, TOP))
        out.append(strand(x0 + 46, x0 + 300, 90, CDNA, 3.2))
        out.append(box(x0 + 300, 84, 16, 12, "", TR, BAD))
        out.append(strand(x0 + 46, x0 + 300, 110, NEW, 3.2))
        for xx in (90, 150, 210, 260):
            out.append(t(x0 + xx, 124, "U", 9.5, HOT, family=MONO))
        if p == 0:
            out.append(lab(x0 + 180, 150, "PCR primers anneal to adapters", 11.5, MUTE, "middle"))
            out.append(lab(x0 + 180, 170, "the enzyme stalls at U on the marked strand", 11.5, BAD, "middle"))
            out.append(lab(x0 + 180, 188, "the unmarked strand copies fully", 11.5, OK, "middle"))
        else:
            for xx in (115, 235):
                out.append(scissors(x0 + xx, 110, BAD))
            out.append(lab(x0 + 180, 150, "cut strand cannot be amplified end to end", 11.5, BAD, "middle"))
            out.append(lab(x0 + 180, 170, "done in the ligation tube, before PCR", 11.5, MUTE, "middle"))
            out.append(lab(x0 + 180, 188, "the unmarked strand is untouched", 11.5, OK, "middle"))
    out.append(t(40, 228, "Both give the same orientation in the data; the choice is a matter of "
                          "enzymes and workflow, not of result.", 14, HOT))
    return svg(820, 246, "".join(out))


# ------------------------------------------------------------------ deck 2

def fig_smallends():
    out = [t(40, 26, "A small RNA is ligation-ready only if its ends are the ones a ligase wants.", 14, INK)]
    X = 330
    rows = [("miRNA, siRNA", 70, "5' P", "3' OH", OK, OK, "Dicer product: ready to ligate"),
            ("piRNA", 100, "5' P", "3' 2'-O-methyl", OK, BAD, "blocked 3' end: ligates poorly with some enzymes"),
            ("tRNA fragments, RNase products", 100, "5' OH", "3' cyclic P", BAD, BAD,
             "a 3' phosphate blocks the ligase"),
            ("ribosome footprint (Ribo-seq)", 90, "5' OH", "3' P", BAD, BAD, "needs T4 PNK repair first")]
    for i, (n, w, l5, l3, c5, c3, note) in enumerate(rows):
        y = 62 + i * 40
        out.append(t(40, y + 4, n, 13, INK))
        out.append(strand(X, X + w, y, RNA, 5))
        out.append(lab(X - 10, y + 4, l5, 11.5, c5, "end"))
        out.append(lab(X + w + 8, y + 4, l3, 11.5, c3))
        out.append(lab(X + 200, y + 4, note, 11.5, c3 if c3 == BAD else OK))
    out.append(t(40, 238, "The library has to ligate to whatever ends the sample has. Ends that fail are "
                          "invisible in the data, not just weak.", 14, HOT))
    return svg(860, 256, "".join(out))


def fig_lig3():
    out = [t(40, 26, "Step 1: a pre-adenylated 3' adapter is ligated with no ATP in the tube.", 14, INK)]
    out.append(strand(60, 200, 90, RNA, 4))
    out.append(lab(50, 94, "5' P", 11.5, MUTE, "end"))
    out.append(lab(206, 94, "3' OH", 11.5, OK))
    out.append(lab(60, 70, "small RNA", 12, RNA))
    out.append(strand(290, 470, 90, MUTE, 3.2))
    out.append(box(284, 80, 14, 20, "", TY, HOT))
    out.append(lab(291, 114, "App", 11, HOT, "middle"))
    out.append(box(466, 80, 14, 20, "", TR, BAD))
    out.append(lab(473, 114, "3' block", 11, BAD, "middle"))
    out.append(lab(380, 70, "3' adapter, 5' adenylated", 12, MUTE, "middle"))
    out.append(arrow(500, 90, 560, NEW))
    out.append(lab(530, 76, "T4 Rnl2 (truncated)", 11.5, NEW, "middle"))
    out.append(strand(580, 700, 90, RNA, 4))
    out.append(strand(700, 800, 90, MUTE, 3.2))
    out.append(box(796, 80, 14, 20, "", TR, BAD))
    out.append(lab(640, 70, "RNA", 11.5, RNA, "middle"))
    out.append(lab(750, 70, "adapter", 11.5, MUTE, "middle"))
    out.append(lab(40, 152, "Why it works: the adenylate that ligation normally needs ATP to make is already on the "
                            "adapter.", 12.5, INK))
    out.append(lab(40, 174, "Truncated Rnl2 cannot adenylate its own substrates, so the RNA does not circularise "
                            "and cannot join other RNAs.", 12.5, INK))
    out.append(lab(40, 196, "The 3' block on the adapter stops it from ligating to itself.", 12.5, INK))
    out.append(t(40, 238, "Without this design, T4 RNA ligase with ATP would make circles and concatemers "
                          "of the sample as well as products.", 14, HOT))
    return svg(840, 256, "".join(out))


def fig_lig5():
    out = [t(40, 26, "Step 2: a 5' RNA adapter is added with T4 RNA ligase 1 and ATP, then RT and PCR.", 14, INK)]
    rows = [("after step 1", 70, [(60, 160, RNA), (160, 250, MUTE)]),
            ("5' adapter ligated", 112, [(50, 98, NEW), (98, 198, RNA), (198, 288, MUTE)]),
            ("RT primer anneals to the 3' adapter", 154, [(50, 98, NEW), (98, 198, RNA), (198, 288, MUTE)])]
    for n, y, segs in rows:
        out.append(lab(340, y + 4, n, 12, INK))
        for a, b, c in segs:
            out.append(strand(a, b, y, c, 4))
    out.append(strand(220, 288, 172, CDNA, 3.2))
    out.append(arrow(220, 172, 70, CDNA, 1.6))
    out.append(lab(340, 176, "first-strand cDNA, now carrying both adapter sequences", 12, CDNA))
    out.append(lab(40, 214, "T4 Rnl1 joins the adapter's 3' OH to the small RNA's 5' phosphate. "
                            "The RNA's 3' end is already taken by the first adapter.", 12.5, INK))
    out.append(lab(40, 234, "Only RNAs that carry a 3' adapter can be reverse transcribed, "
                            "so they are the ones that end up in the library.", 12.5, INK))
    out.append(t(40, 270, "Order matters: the 3' adapter goes on first so the 5' step can only act "
                          "on molecules that already carry one.", 14, HOT))
    return svg(820, 288, "".join(out))


def fig_dimer():
    out = [t(40, 26, "The 5' adapter ligates to any 3' adapter left over, and the product is an adapter dimer.",
             14, INK)]
    out.append(strand(60, 130, 80, NEW, 4))
    out.append(strand(130, 220, 80, MUTE, 3.2))
    out.append(lab(40, 84, "5'", 11, MUTE, "end"))
    out.append(lab(240, 84, "dimer: no insert, only a few tens of bp shorter than the true product", 12, BAD))
    out.append(strand(60, 130, 130, NEW, 4))
    out.append(strand(130, 160, 130, RNA, 4))
    out.append(strand(160, 250, 130, MUTE, 3.2))
    out.append(lab(270, 134, "the product you want: insert in between", 12, OK))
    out.append(lab(40, 178, "Countermeasures, and where each acts", 13, INK, "start"))
    for i, (a, b) in enumerate([("less adapter", "fewer leftovers, but less ligation"),
                                ("enzymatic removal of free 3' adapter", "before the 5' ligation"),
                                ("size selection", "after PCR; the dimer is only slightly shorter"),
                                ("RT primer blocks excess adapter", "kit-specific; mechanism not always published")]):
        y = 202 + i * 20
        out.append(t(60, y, a, 12, TOP))
        out.append(t(330, y, b, 12, MUTE))
    return svg(780, 300, "".join(out))


def fig_sizesel():
    out = [t(40, 26, "The size window is narrow, so the dimer peak sits right beside the miRNA peak.", 14, INK)]
    out.append(line(60, 190, 700, 190, MUTE, 1))
    for xx, lbl in [(120, "100"), (220, "125"), (320, "150"), (420, "175"), (520, "200"), (620, "225")]:
        out.append(line(xx, 190, xx, 195, MUTE, 1))
        out.append(lab(xx, 208, lbl, 11, MUTE, "middle"))
    out.append(lab(380, 226, "library size (bp), schematic", 11.5, MUTE, "middle"))

    def peak(cx, h, col, wd=16):
        pts = " ".join(f"{cx - 3*wd + j*wd/8:.0f},{190 - h*math.exp(-((j-24)/(8))**2):.0f}" for j in range(49))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2"/>'
    out.append(peak(190, 120, BAD))
    out.append(peak(240, 90, OK))
    out.append(peak(280, 28, HOT))
    out.append(peak(520, 30, MUTE, 30))
    out.append(lab(190, 62, "adapter dimer", 12, BAD, "middle"))
    out.append(lab(250, 92, "miRNA", 12, OK, "start"))
    out.append(lab(300, 146, "piRNA, tRF", 11.5, HOT, "start"))
    out.append(lab(520, 120, "longer, unwanted RNA", 11.5, MUTE, "middle"))
    out.append(lab(40, 250, "Bead cleanup separates 20 bp poorly. Kits split the problem: a high-percentage gel, or two bead "
                            "ratios (NEBNext 8A) in sequence.", 12.5, INK))
    out.append(t(40, 276, "Rule: look at the trace before you load. A small dimer peak becomes a large share "
                          "of the reads.", 13.5, HOT))
    return svg(780, 294, "".join(out))


def fig_ribofoot():
    out = [t(40, 26, "Ribo-seq: freeze the ribosomes, digest what they do not cover, sequence the footprints.",
             14, INK)]
    out.append(lab(40, 62, "1. lysate: mRNA with ribosomes on the ORF", 12.5, INK))
    out.append(strand(60, 640, 100, RNA, 3.2))
    out.append(capdot(56, 100))
    out.append(t(646, 104, "AAAA", 10.5, RNA, family=MONO))
    for xx in (200, 300, 400):
        out.append(f'<ellipse cx="{xx}" cy="96" rx="26" ry="20" fill="{TY}" stroke="{HOT}" stroke-width="1.3" opacity="0.9"/>')
    out.append(lab(40, 148, "2. RNase I digests exposed RNA", 12.5, INK))
    out.append(strand(60, 172, 180, RNA, 2, ))
    for xx in (200, 300, 400):
        out.append(f'<ellipse cx="{xx}" cy="176" rx="26" ry="20" fill="{TY}" stroke="{HOT}" stroke-width="1.3"/>')
        out.append(strand(xx - 15, xx + 15, 176, RNA, 5))
        out.append(scissors(xx - 40, 176))
        out.append(scissors(xx + 40, 176))
    out.append(lab(40, 224, "3. purify monosomes, release the ~28 nt footprints", 12.5, INK))
    for k, xx in enumerate((200, 300, 400)):
        out.append(strand(xx - 15, xx + 15, 250, RNA, 5))
    out.append(lab(450, 254, "footprints, 5' OH and 3' P, with rRNA fragments among them", 12, BAD))
    out.append(lab(40, 290, "Position of the 5' end gives the reading frame: three-base periodicity "
                            "along the coding sequence.", 13, MUTE))
    out.append(t(40, 316, "Much of what you purify is rRNA fragments. How well you remove them sets "
                          "how many reads you waste.", 13.5, HOT))
    return svg(780, 334, "".join(out))


def fig_riboconstruct():
    out = [t(40, 26, "From footprint to library: repair, ligate, copy, circularise, amplify.", 14, INK)]
    steps = [("PNK: 5' P, 3' OH", 60), ("3' linker (adenylated)", 160), ("RT with linker primer", 260),
             ("circularise cDNA", 360), ("PCR from inside the circle", 460)]
    for i, (n, y) in enumerate(steps):
        pass
    y0 = 70
    # row 1: repaired
    out.append(lab(40, y0, "1. T4 PNK repair, then 3' linker ligation", 12.5, INK))
    out.append(strand(60, 120, y0 + 24, RNA, 5))
    out.append(strand(120, 220, y0 + 24, MUTE, 3.2))
    out.append(lab(240, y0 + 28, "footprint + 3' linker", 11.5, MUTE))
    out.append(lab(40, y0 + 64, "2. RT from a primer on the linker; the cDNA runs to the 5' end of the footprint",
                   12.5, INK))
    out.append(strand(60, 120, y0 + 88, RNA, 5))
    out.append(strand(120, 220, y0 + 88, MUTE, 3.2))
    out.append(strand(60, 220, y0 + 102, CDNA, 3.2))
    out.append(lab(240, y0 + 106, "gel-purify the full-length cDNA", 11.5, MUTE))
    out.append(lab(440, y0, "3. circularise with CircLigase", 12.5, INK))
    out.append(f'<circle cx="530" cy="{y0+56}" r="32" fill="none" stroke="{CDNA}" stroke-width="3.2"/>')
    out.append(lab(530, y0 + 56, "ss cDNA", 11, CDNA, "middle"))
    out.append(lab(590, y0 + 40, "the end with no adapter on it", 11.5, MUTE))
    out.append(lab(590, y0 + 56, "now sits beside the linker", 11.5, MUTE))
    out.append(lab(440, y0 + 104, "4. PCR with primers pointing outwards", 12.5, INK))
    out.append(arrow(515, y0 + 126, 470, CDNA, 1.6))
    out.append(arrow(545, y0 + 126, 590, HOT, 1.6))
    out.append(t(40, 252, "Circularisation joins the unadapted end to the linker, so no second ligation is needed "
                          "and one primer pair reads across the junction.", 13.5, HOT))
    return svg(820, 270, "".join(out))


def fig_ts():
    out = [t(40, 26, "Template switching: the RT finishes the RNA, adds a few extra bases, and jumps.", 14, INK)]
    titles = ["1. RT reaches the cap", "2. adds extra C, not templated", "3. the TSO pairs and RT copies it"]
    for p in range(3):
        x0 = 40 + p * 270
        out.append(lab(x0, 56, titles[p], 12, INK))
        out.append(strand(x0 + 30, x0 + 230, 100, RNA, 3.2))
        out.append(capdot(x0 + 26, 100))
        out.append(strand(x0 + 70, x0 + 230, 116, CDNA, 3.2))
        out.append(lab(x0 + 12, 90, "5'", 11, MUTE, "end"))
        if p >= 1:
            out.append(t(x0 + 52, 128, "CCC", 11, NEW, family=MONO, anchor="middle"))
        if p == 2:
            out.append(strand(x0 + 4, x0 + 34, 146, NEW, 3.2))
            out.append(box(x0 - 6, 139, 12, 14, "", TB, TOP))
            out.append(t(x0 + 52, 150, "GGG", 11, NEW, family=MONO, anchor="middle"))
            out.append(lab(x0 + 100, 158, "TSO", 11, NEW))
    out.append(lab(40, 186, "At the end of the template the RT adds a few non-templated Cs, most often at a capped "
                            "5' end.", 12, INK))
    out.append(lab(40, 206, "TSO: a primer with a handle and a 3' run of G (often riboG or LNA-G) that pairs with "
                            "the extra C.", 12, INK))
    out.append(lab(40, 226, "The cDNA now has a known sequence at both ends; one PCR primer pair "
                            "amplifies it without ligation.", 12, INK))
    out.append(t(40, 262, "Where to be careful: an RNA fragment with no cap also receives extra C, so template "
                          "switching alone does not prove full length.", 13.5, HOT))
    return svg(860, 280, "".join(out))


def fig_tso():
    out = [t(40, 26, "A TSO is a short oligo with four parts, and each part has a job.", 14, INK)]
    x = 60
    parts = [("5' biotin or blocker", 120, TR, BAD), ("PCR handle", 120, TB, TOP),
             ("barcode / UMI", 110, TY, HOT), ("GGG (rG or LNA)", 120, TG, OK)]
    for n, w, f, c in parts:
        out.append(box(x, 80, w, 36, n, f, c, 11.5, c))
        x += w
    out.append(lab(60, 140, "blocks 5' end", 11, BAD))
    out.append(lab(180, 140, "shared primer site", 11, TOP))
    out.append(lab(300, 140, "identity information", 11, HOT))
    out.append(lab(412, 140, "binds the C-overhang", 11, OK))
    out.append(lab(40, 186, "Smart-seq3 puts a UMI and a tag in the TSO, so each 5' end is counted once "
                            "and 5' reads can be told apart.", 12.5, INK))
    out.append(lab(40, 208, "Failure to watch: the TSO can also be copied by the RT, giving a strand-invasion "
                            "artefact, and can prime on A-rich internal sites.", 12.5, INK))
    out.append(t(40, 244, "A TSO is part of the primer budget: too little leaves cDNA without a handle, "
                          "too much makes by-products.", 13.5, HOT))
    return svg(800, 262, "".join(out))


def fig_ss2():
    out = [t(40, 26, "SMART-seq2 for one cell: five reactions in one tube, then a library by tagmentation.", 14, INK)]
    steps = [("lyse, oligo-dT-ISPCR\nprimer anneals", TB), ("RT + template\nswitching (TSO)", TG),
             ("pre-amplify by PCR,\nISPCR primer only", TY), ("bead cleanup,\ncheck full length", TB),
             ("Tn5 tagmentation,\nindex PCR", TR)]
    for i, (n, f) in enumerate(steps):
        x = 40 + i * 156
        out.append(box(x, 50, 132, 90, "", f, MUTE))
        for j, ln in enumerate(n.split("\n")):
            out.append(t(x + 66, 88 + j * 18, ln, 12, INK, anchor="middle"))
        out.append(t(x + 66, 70, str(i + 1), 13, HOT, anchor="middle", weight="bold"))
        if i < 4:
            out.append(arrow(x + 136, 95, x + 152, MUTE))
    out.append(lab(40, 174, "Result: reads across the whole transcript, so isoforms, SNPs and splice junctions are visible.",
                   12.5, INK))
    out.append(lab(40, 196, "Price: no UMIs, because Tn5 cuts the cDNA and PCR duplicates cannot be separated from "
                            "real ones.", 12.5, INK))
    out.append(t(40, 232, "Pre-amplifying from one cell to nanograms is what makes it possible to "
                          "fragment and index at all.", 13.5, HOT))
    return svg(880, 250, "".join(out))


def fig_ivt():
    out = [t(40, 26, "Linear amplification by in vitro transcription: one template, many RNA copies.", 14, INK)]
    out.append(lab(40, 62, "1. RT with an oligo-dT primer carrying a T7 promoter, then second strand", 12.5, INK))
    out.append(box(60, 76, 70, 18, "T7 promoter", TY, HOT, 10.5, HOT))
    out.append(strand(130, 330, 85, CDNA, 3.2))
    out.append(strand(60, 330, 99, NEW, 3.2))
    out.append(lab(340, 92, "ds cDNA with a promoter at the 3' end", 11.5, MUTE))
    out.append(lab(40, 134, "2. T7 RNA polymerase transcribes the antisense strand, over and over", 12.5, INK))
    for k in range(5):
        y = 150 + k * 10
        out.append(arrow(110, y, 180 + k * 40, RNA, 1.8, 4))
    out.append(lab(430, 160, "many aRNA copies, each made from the original template", 11.5, RNA))
    out.append(lab(40, 224, "Why linear matters: each copy comes from the starting molecule, so an early error is "
                            "not itself copied again and again.", 12.5, INK))
    out.append(lab(40, 246, "PCR gives exponential growth; its small efficiency differences compound into "
                            "ratio bias. IVT trades yield for faithfulness.", 12.5, INK))
    out.append(t(40, 282, "Price: early protocols needed repeated rounds, and coverage is biased to the 3' end. "
                          "CEL-Seq2 uses one round.", 13.5, HOT))
    return svg(800, 300, "".join(out))


def fig_constructs():
    out = [t(40, 26, "Where the barcode sits, and which end of the RNA is read.", 14, INK)]
    rows = [("CEL-Seq2", "3' tag; barcode in the RT primer", "3"),
            ("STRT-seq", "5' tag; barcode in the TSO", "5"),
            ("SMART-seq2", "full length; no barcode in the RT", "f")]
    P3 = {"3": [("dT", 36, TB, TOP), ("UMI", 40, TR, BAD), ("cell BC", 60, TG, OK),
                ("adapter", 60, TB, TOP), ("T7", 40, TY, HOT)],
          "f": [("dT30VN", 66, TB, TOP), ("ISPCR", 60, TB, TOP)]}
    for i, (n, sub, k) in enumerate(rows):
        y = 56 + i * 72
        out.append(t(40, y + 20, n, 13.5, INK, weight="bold"))
        out.append(lab(40, y + 38, sub, 11.5, MUTE))
        if k == "5":
            x = 260
            for lbl, w, f, c in [("adapter", 60, TB, TOP), ("cell BC", 60, TG, OK), ("GGG", 40, TB, TOP)]:
                out.append(box(x, y + 6, w, 28, lbl, f, c, 10.5, c))
                x += w
            out.append(strand(x, x + 260, y + 20, RNA, 4))
            out.append(capdot(x + 2, y + 20))
            out.append(t(x + 266, y + 24, "AAAA 3'", 10.5, RNA, family=MONO))
        else:
            x = 260
            out.append(strand(x, x + 260, y + 20, RNA, 4))
            out.append(capdot(x + 2, y + 20))
            x += 260
            out.append(t(x + 6, y + 24, "AAAA", 10.5, RNA, family=MONO))
            x += 46
            for lbl, w, f, c in P3[k]:
                out.append(box(x, y + 6, w, 28, lbl, f, c, 10.5, c))
                x += w
    out.append(lab(40, 280, "The UMI marks a single starting molecule; the cell barcode lets many cells "
                            "share a tube from the RT onwards. STRT-C1 added a UMI.", 12, INK))
    out.append(t(40, 304, "Barcode in the first primer means pooling before amplification: "
                          "cheaper, but reads only one end.", 13.5, HOT))
    return svg(860, 322, "".join(out))


def fig_tagfl():
    out = [t(40, 26, "Where the reads land on one four-exon transcript.", 14, INK)]
    rows = [("3' tag (CEL-Seq2)", "3"), ("5' tag (STRT-seq)", "5"), ("full length (SMART-seq2)", "f")]
    for i, (n, k) in enumerate(rows):
        y = 70 + i * 70
        out.append(t(40, y + 4, n, 13, INK))
        out.append(strand(250, 690, y, MUTE, 1.4))
        for a, b in ((250, 310), (370, 420), (490, 540), (610, 690)):
            out.append(f'<rect x="{a}" y="{y-9}" width="{b-a}" height="18" fill="none" stroke="{MUTE}"/>')
        if k == "3":
            for xx in range(630, 690, 6):
                out.append(line(xx, y - 9, xx, y - 24 + (xx % 11), HOT, 2))
        elif k == "5":
            for xx in range(252, 312, 6):
                out.append(line(xx, y - 9, xx, y - 24 + (xx % 11), HOT, 2))
        else:
            for xx in range(256, 690, 14):
                if not (312 < xx < 368 or 422 < xx < 488 or 544 < xx < 608):
                    out.append(line(xx, y - 9, xx, y - 24 + (xx % 9), HOT, 2))
    out.append(lab(40, 262, "A tag count says how much; only full-length reads can say which exon "
                            "combination, which variant, which junction.", 12.5, INK))
    out.append(t(40, 288, "Depth: a tag protocol puts all reads on one short window, so it needs far fewer reads "
                          "per cell than full length.", 13.5, MUTE))
    return svg(780, 306, "".join(out))


def fig_tn5():
    out = [t(40, 26, "Tn5 can fragment and tag an RNA:DNA hybrid, so the second strand is not needed.", 14, INK)]
    out.append(lab(40, 62, "1. RT gives an RNA:cDNA hybrid; the usual route would now synthesise a second strand",
                   12.5, INK))
    out.append(strand(60, 400, 96, RNA, 3.2))
    out.append(strand(60, 400, 110, CDNA, 3.2))
    out.append(lab(40, 148, "2. Tn5, loaded with adapters, cuts the hybrid and attaches its adapters", 12.5,
                   INK))
    out.append(strand(60, 400, 176, RNA, 3.2))
    out.append(strand(60, 400, 190, CDNA, 3.2))
    for xx in (150, 280):
        out.append(f'<ellipse cx="{xx}" cy="183" rx="20" ry="17" fill="{TY}" stroke="{HOT}"/>')
        out.append(lab(xx, 187, "Tn5", 11, HOT, "middle"))
    out.append(lab(40, 240, "3. complete the adapters and amplify the library by PCR", 12.5, INK))
    out.append(lab(440, 96, "Saves a second-strand reaction and its cleanup", 12, OK))
    out.append(lab(440, 116, "Caveat: Tn5 prefers some sequences,", 12, MUTE))
    out.append(lab(440, 134, "so insert-size distribution reflects the enzyme", 12, MUTE))
    out.append(t(40, 276, "Di et al. 2020 show that Tn5 accepts RNA/DNA hybrids as a substrate.", 13, HOT))
    return svg(780, 294, "".join(out))


def fig_captrap():
    out = [t(40, 26, "Cap trapping: biotin on the cap survives only where the cDNA reached it.", 14, INK)]
    steps = ["1. RT: some cDNAs reach the cap, some stop early", "2. oxidise the cap diol and attach biotin",
             "3. RNase I digests RNA that is not paired", "4. streptavidin beads keep what still has biotin"]
    out.append(lab(60, 56, "full-length cDNA", 12, OK))
    out.append(lab(470, 56, "cDNA that stopped early", 12, BAD))
    for i, s_ in enumerate(steps):
        y = 80 + i * 52
        out.append(lab(40, y, s_, 12.5, INK))
        for x0, full in ((60, True), (470, False)):
            if i == 2 and not full:
                out.append(strand(x0, x0 + 90, y + 18, RNA, 3.2))
                out.append(strand(x0 + 110, x0 + 330, y + 18, RNA, 3.2))
                out.append(scissors(x0 + 100, y + 18, BAD))
                out.append(strand(x0 + 110, x0 + 330, y + 32, CDNA, 3.2))
                out.append(capdot(x0 - 4, y + 18))
                out.append(dot(x0 - 4, y + 8, 3, OK))
                continue
            if i == 3 and not full:
                out.append(strand(x0 + 110, x0 + 330, y + 18, RNA, 3.2))
                out.append(strand(x0 + 110, x0 + 300, y + 32, CDNA, 3.2))
                out.append(lab(x0 + 20, y + 22, "washed away", 11.5, BAD))
                continue
            out.append(strand(x0, x0 + 330, y + 18, RNA, 3.2))
            out.append(capdot(x0 - 4, y + 18))
            out.append(strand(x0 if full else x0 + 110, x0 + 300, y + 32, CDNA, 3.2))
            if i >= 1:
                out.append(dot(x0 - 4, y + 8, 3, OK))
            if i == 3 and full:
                out.append(f'<circle cx="{x0-26}" cy="{y+20}" r="9" fill="{TG}" stroke="{OK}"/>')
    out.append(lab(40, 300, "A fragment with no cap never carries biotin. A cDNA that stopped early leaves the cap "
                            "on a single-stranded tail that RNase I removes.", 12, INK))
    out.append(t(40, 324, "Result: reads that start at transcription start sites. CAGE counts them; "
                          "CapTrap-seq makes them long reads.", 13.5, HOT))
    return svg(860, 342, "".join(out))


# ---- the construct-walk idiom, as used in design/fig03-walk-rna.svg ----
PB, PR, PP, GR, PG, PO = "#e8eef5", "#f5eae6", "#efe9f3", "#f1f1ee", "#e6f0e8", "#f7ece5"
PRNA = "#f3e7ec"
KIND = {"p5": (PB, TOP), "p7": (PR, BAD), "ins": ("none", MUTE), "ad": (GR, MUTE),
        "hot": (PO, HOT), "ok": (PG, OK), "rna": (PRNA, RNA), "cdna": (PB, CDNA)}


def chain(x, y, parts, h=22, size=11.5):
    out = []
    for label, w, k in parts:
        fill, col = KIND[k]
        out.append(box(x, y, w, h, label, fill, col, size, col, r=3))
        x += w
    return "".join(out), x


def fig_walk_truseq():
    """TruSeq Stranded mRNA: the molecule after every step."""
    out = [t(40, 26, "TruSeq Stranded mRNA: the molecule after every step. 100 ng of total RNA.",
             14, INK)]
    rows = [
        ("1  oligo-dT beads, twice",
         [("cap", 34, "ok"), ("mRNA, intact", 212, "rna"), ("AAAA", 44, "ad")],
         "rRNA and everything untailed is washed away"),
        ("2  heat + Mg2+, with hexamers",
         [("mRNA fragment, a few hundred nt", 260, "rna")],
         "the RNA is cut, not the cDNA: this sets the insert"),
        ("3  first strand, actinomycin D",
         [("first-strand cDNA on its RNA template", 260, "cdna")],
         "the RT copies RNA only, so the strand is remembered"),
        ("4  second strand, dUTP for dTTP",
         [("double-stranded cDNA, U in one strand", 260, "hot")],
         "RNase H nicks the RNA, Pol I replaces it; blunt"),
        ("5  dA-tail",
         [("A", 14, "hot"), ("blunt ds cDNA, U-marked", 232, "ins"), ("A", 14, "hot")],
         "one 3' A, so only a T-overhang can ligate"),
        ("6  ligate the indexed adapter",
         [("P5 i5 R1", 66, "p5"), ("insert, U-marked strand", 228, "ins"),
          ("R2 i7 P7", 66, "p7")],
         "the index is on before PCR, not added by it"),
        ("7  PCR, 15 cycles",
         [("P5 i5 R1", 66, "p5"), ("only the first strand is copied", 228, "hot"),
          ("R2 i7 P7", 66, "p7")],
         "the U strand is not a template: one orientation left"),
        ("8  the finished molecule",
         [("P5 i5 R1", 66, "p5"), ("insert", 228, "ins"), ("R2 i7 P7", 66, "p7")],
         "read 1 lands antisense to the mRNA"),
    ]
    for i, (name, parts, note) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(40, y + 15, name, 12, INK))
        s, _ = chain(270, y, parts)
        out.append(s)
        out.append(t(680, y + 15, note, 11.5, MUTE))
    out.append(t(40, 52 + 8 * 34 + 16, "Cutting the RNA sets the insert size; marking the second "
                 "strand with U is what makes the library stranded.", 13.5, HOT))
    return svg(1000, 52 + 8 * 34 + 36, "".join(out))


build(__file__, [
    ("classes", fig_classes),
    ("removal", fig_removal),
    ("rnaseh", fig_rnaseh),
    ("dash", fig_dash),
    ("bias", fig_bias),
    ("priming", fig_priming),
    ("second", fig_second),
    ("whystrand", fig_whystrand),
    ("dutp", fig_dutp),
    ("twoways", fig_twoways),
    ("smallends", fig_smallends),
    ("lig3", fig_lig3),
    ("lig5", fig_lig5),
    ("dimer", fig_dimer),
    ("sizesel", fig_sizesel),
    ("ribofoot", fig_ribofoot),
    ("riboconstruct", fig_riboconstruct),
    ("ts", fig_ts),
    ("tso", fig_tso),
    ("ss2", fig_ss2),
    ("ivt", fig_ivt),
    ("constructs", fig_constructs),
    ("tagfl", fig_tagfl),
    ("tn5", fig_tn5),
    ("captrap", fig_captrap),
    ("walk-truseq", fig_walk_truseq),
])
