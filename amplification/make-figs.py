#!/usr/bin/env python3
"""Figures for the amplification unit.  Run: python3 amplification/make-figs.py"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE = "#e8eef4"
WARM = "#f6e6dc"
GREENP = "#e3efe6"
REDP = "#f3dedb"


# ---------------------------------------------------------------- local helpers

def R(x, y, w, h, fill="none", stroke=MUTE, sw=1.2, r=3, op=None):
    o = f' fill-opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"/>')


def C(x, y, r, fill="none", stroke=MUTE, sw=1.2):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def poly(pts, stroke=INK, w=2.0, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d}/>')


def varrow(x, y1, y2, color=HOT, w=1.6, head=5):
    d = 1 if y2 > y1 else -1
    return (line(x, y1, x, y2 - d * head, color, w) +
            f'<path d="M {x} {y2} L {x - head*0.7} {y2 - d*head} L {x + head*0.7} {y2 - d*head} Z" '
            f'fill="{color}"/>')


def DNA(x1, x2, y, col=TOP, w=3.0):
    return line(x1, y, x2, y, col, w)


def comp(s):
    m = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return "".join(m.get(c, " ") for c in s)


def gel(x, y, w, h, nlanes, lane_w=26, gap=14):
    """Returns (svg, [lane x centres])."""
    out = [R(x, y, w, h, "#f1f1ee", MUTE, 1.2)]
    xs = []
    for i in range(nlanes):
        cx = x + 16 + lane_w / 2 + i * (lane_w + gap)
        xs.append(cx)
        out.append(R(cx - lane_w / 2, y + 5, lane_w, 5, "#c9c9c4", "none", 0))
    return "".join(out), xs


def band(cx, y, lw=26, col=INK, op=0.85, h=3.2):
    return R(cx - lw / 2, y - h / 2, lw, h, col, "none", 0, 1.5, op)


def smear(cx, y1, y2, lw=26, col=INK, op=0.28):
    return R(cx - lw / 2, y1, lw, y2 - y1, col, "none", 0, 3, op)


def ylog(size, y0, h, smin, smax):
    return y0 + h * math.log(smax / size) / math.log(smax / smin)


# ---------------------------------------------------------------- figures


def axes(x0, y0, w, h):
    return line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2) + line(x0, y0, x0, y0 + h, MUTE, 1.2)


def fig_curve():
    out = [t(30, 24, "Copies against cycle, from 1 ng of human DNA (about 150 cells), log scale.", 14, INK)]
    x0, y0, w, h = 80, 44, 560, 170
    out.append(axes(x0, y0, w, h))
    lo, hi = 1e2, 1e14
    def yp(v):
        return y0 + h * (1 - math.log10(v / lo) / math.log10(hi / lo))
    def xp(c):
        return x0 + w * c / 40
    ideal = [(xp(c), yp(max(lo, 300 * 2 ** c))) for c in range(0, 40) if 300 * 2 ** c <= hi]
    out.append(poly(ideal, MUTE, 1.6, dash="4 4"))
    n, pts = 300.0, [(xp(0), yp(300))]
    for c in range(1, 41):
        n = n * (1 + 0.95 * (1 - n / 1e12))
        pts.append((xp(c), yp(n)))
    out.append(poly(pts, HOT, 2.6))
    for c in (10, 20, 30, 40):
        out.append(line(xp(c), y0 + h, xp(c), y0 + h + 5, MUTE, 1.2))
        out.append(t(xp(c), y0 + h + 20, str(c), 12, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 38, "cycle", 12.5, MUTE, anchor="middle"))
    for v, lab in ((1e3, "1e3"), (1e6, "1e6"), (1e9, "1e9"), (1e12, "1e12")):
        out.append(t(x0 - 8, yp(v) + 4, lab, 12, MUTE, anchor="end"))
    out.append(t(xp(2), yp(1e12), "exponential: every copy is a template", 12.5, HOT))
    out.append(t(xp(24), yp(1e7), "plateau: primers and polymerase run out,", 12.5, HOT))
    out.append(t(xp(24), yp(1e7) + 16, "products anneal to each other", 12.5, HOT))
    out.append(t(xp(2), yp(1e12) + 18, "dashed: perfect doubling", 12.5, MUTE))
    out.append(t(30, y0 + h + 66, "Past the knee of the curve extra cycles add almost no product, and "
                                  "all the damage.", 14, INK))
    return svg(760, y0 + h + 80, "".join(out))


def fig_fidelity():
    out = [t(30, 24, "An error made in cycle k is inherited by about 1 in 2^(k+1) of the final strands.", 14, INK)]
    x0, y0, w, h = 70, 44, 330, 130
    out.append(axes(x0, y0, w, h))
    for k in range(1, 9):
        v = 2 ** -(k + 1)
        bh = max(2, v * h / 0.25)
        bx = x0 + 10 + (k - 1) * 39
        out.append(R(bx, y0 + h - bh, 28, bh, HOT if k <= 2 else TOP, "none", 0, 2, 0.85))
        out.append(t(bx + 14, y0 + h + 18, str(k), 12, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 36, "cycle in which the error occurs", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 8, "25 %", 12, MUTE, anchor="end"))
    out.append(t(430, 70, "Early errors are the expensive ones:", 13.5, INK, weight="bold"))
    out.append(t(430, 92, "they reach a large share of the product.", 13.5, INK))
    out.append(t(430, 126, "Expected errors per molecule is roughly", 13.5, INK))
    out.append(t(430, 148, "rate x length x doublings / 2.", 13.5, INK))
    out.append(t(430, 182, "Polymerases without proofreading: 10 to", 13.5, MUTE))
    out.append(t(430, 202, "several hundred times more errors.", 13.5, MUTE))
    out.append(t(30, 236, "Fewer cycles is the cheapest way to improve fidelity, because it cuts "
                          "the doublings.", 14, INK))
    return svg(760, 252, "".join(out))


def bubble(x, y, w, depth, col):
    return (f'<path d="M {x} {y} C {x + w * 0.2} {y - depth}, {x + w * 0.8} {y - depth}, {x + w} {y}" '
            f'fill="none" stroke="{col}" stroke-width="2.4"/>')


def fig_overamp():
    out = [t(30, 24, "When primers run out, products anneal to each other instead.", 14, INK)]
    x0 = 80
    # two different molecules sharing adapter ends
    out.append(t(30, 60, "insert X", 12.5, TOP))
    out.append(line(x0, 62, x0 + 90, 62, HOT, 3))
    out.append(line(x0 + 90, 62, x0 + 300, 62, TOP, 3))
    out.append(line(x0 + 300, 62, x0 + 390, 62, HOT, 3))
    out.append(t(30, 116, "insert Y", 12.5, BOT))
    out.append(line(x0, 114, x0 + 90, 114, HOT, 3))
    out.append(line(x0 + 90, 114, x0 + 300, 114, BOT, 3))
    out.append(line(x0 + 300, 114, x0 + 390, 114, HOT, 3))
    out.append(t(x0 + 430, 90, "denature, cool, the ends match", 13, INK))
    out.append(t(x0 + 430, 110, "and the middle does not", 13, INK))
    # heteroduplex bubble
    y = 190
    out.append(line(x0, y, x0 + 90, y, HOT, 3))
    out.append(line(x0, y + 8, x0 + 90, y + 8, HOT, 3))
    out.append(line(x0 + 300, y, x0 + 390, y, HOT, 3))
    out.append(line(x0 + 300, y + 8, x0 + 390, y + 8, HOT, 3))
    out.append(bubble(x0 + 90, y, 210, 26, TOP))
    out.append(bubble(x0 + 90, y + 8, 210, -26, BOT))
    out.append(t(x0 + 195, y - 40, "bubble", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 + 430, y - 6, "heteroduplex: runs high on a gel,", 13, BAD))
    out.append(t(x0 + 430, y + 14, "can be extended into a chimera", 13, BAD))
    out.append(t(30, 262, "Symptoms: a smear above the expected peak, a quantity that falls short of the "
                          "fluorescence, and swapped barcodes.", 13.5, INK))
    out.append(t(30, 282, "Remedy: fewer cycles, or one extra cycle with fresh primers and polymerase to "
                          "convert the bubbles back.", 13.5, INK))
    return svg(760, 298, "".join(out))


def fig_bias():
    out = [t(30, 24, "PCR does not copy every fragment at the same rate (illustrative shapes).", 14, INK)]
    for k, (name, x0) in enumerate((("coverage against GC content", 60), ("yield against fragment length", 410))):
        y0, w, h = 52, 280, 140
        out.append(axes(x0, y0, w, h))
        out.append(t(x0, y0 - 10, name, 13, INK, weight="bold"))
        out.append(line(x0, y0 + h * 0.4, x0 + w, y0 + h * 0.4, MUTE, 0.8, dash="3 4"))
        pts_a, pts_b = [], []
        for i in range(0, 41):
            u = i / 40
            if k == 0:
                free = 0.4 + 0.10 * math.sin(u * 6) * 0.5
                pcr = 0.4 - 0.5 * (u - 0.5) ** 2 * 3.2 + 0.08
                pcr = max(0.03, 0.55 - 2.4 * (u - 0.45) ** 2)
                pts_a.append((x0 + u * w, y0 + h * (1 - free * 1.3)))
                pts_b.append((x0 + u * w, y0 + h * (1 - pcr)))
            else:
                free = 0.5
                pcr = 0.85 - 0.6 * u
                pts_a.append((x0 + u * w, y0 + h * (1 - free)))
                pts_b.append((x0 + u * w, y0 + h * (1 - pcr)))
        out.append(poly(pts_a, TOP, 2.2))
        out.append(poly(pts_b, HOT, 2.6))
        lbls = ("20 %", "50 %", "80 %") if k == 0 else ("100 bp", "500 bp", "1 kb")
        for u, lab in zip((0.05, 0.5, 0.95), lbls):
            out.append(t(x0 + u * w, y0 + h + 18, lab, 12, MUTE, anchor="middle"))
        out.append(t(x0 + w - 4, y0 + 14, "PCR-free" if k == 0 else "", 12, TOP, anchor="end"))
    out.append(t(60, 252, "blue: no amplification, red: after many cycles. GC-rich and AT-rich ends are "
                          "lost first; short beats long.", 13.5, INK))
    out.append(t(60, 272, "Different polymerases and buffers reshape the curve. Cutting the cycles "
                          "flattens it.", 13.5, INK))
    return svg(760, 288, "".join(out))


def fig_dups():
    out = [t(30, 24, "Unique reads against reads sequenced, for three library complexities.", 14, INK)]
    x0, y0, w, h = 80, 44, 540, 170
    out.append(axes(x0, y0, w, h))
    maxm = 100.0
    for N, col in ((5, HOT), (20, TOP), (80, OK)):
        pts = []
        for i in range(0, 61):
            m = maxm * i / 60
            u = N * (1 - math.exp(-m / N))
            pts.append((x0 + w * m / maxm, y0 + h * (1 - u / 80)))
        out.append(poly(pts, col, 2.4))
        out.append(t(x0 + w + 6, pts[-1][1] + 4, f"{N} M", 12.5, col))
    out.append(line(x0, y0, x0 + w, y0 + h * (1 - 100 / 80), MUTE, 0.8, dash="3 4") if False else "")
    for m in (0, 25, 50, 75, 100):
        out.append(line(x0 + w * m / maxm, y0 + h, x0 + w * m / maxm, y0 + h + 5, MUTE, 1.2))
        out.append(t(x0 + w * m / maxm, y0 + h + 20, str(m), 12, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 38, "reads sequenced (millions)", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 6, "80 M", 12, MUTE, anchor="end"))
    out.append(t(x0 - 8, y0 + h, "0", 12, MUTE, anchor="end"))
    out.append(t(30, y0 + h + 66, "A library of N distinct molecules saturates at N: after that, more reads "
                                  "are copies of reads you already have.", 13.5, INK))
    return svg(760, y0 + h + 80, "".join(out))


def fig_cycles():
    out = [t(30, 24, "Cycles needed against input (target 100 ng library, 25 % conversion, 90 % efficiency).", 14, INK)]
    rows = [(1000, "1 ug"), (100, "100 ng"), (10, "10 ng"), (1, "1 ng"), (0.1, "100 pg"), (0.01, "10 pg")]
    x0, sc = 120, 24
    for i, (ng, lab) in enumerate(rows):
        y = 52 + i * 28
        out.append(t(30, y + 5, lab, 13.5, INK))
        yld = ng * 0.25
        cyc = 0.0 if yld >= 100 else math.log(100 / yld) / math.log(1.9)
        out.append(R(x0, y - 7, max(3, cyc * sc), 14, OK if cyc < 1 else HOT if cyc > 12 else TOP, "none", 0, 3, 0.85))
        out.append(t(x0 + max(3, cyc * sc) + 8, y + 5, "none: PCR-free" if cyc < 1 else f"about {round(cyc)} cycles", 13, MUTE))
    out.append(t(30, 52 + 6 * 28 + 14, "Every ten-fold drop in input costs about 3.6 cycles. Hence the rule: "
                                       "use the input you have, then the fewest cycles.", 13.5, INK))
    return svg(760, 52 + 6 * 28 + 30, "".join(out))


def gauss(x, mu, sd, a):
    return a * math.exp(-0.5 * ((math.log(x) - math.log(mu)) / sd) ** 2)


def fig_dimer():
    out = [t(30, 24, "A library trace with adapter dimer, before and after a bead clean-up.", 14, INK)]
    for k, (name, y0, dimer) in enumerate((("before", 44, 1.0), ("after clean-up", 154, 0.18))):
        x0, w, h = 70, 560, 80
        out.append(axes(x0, y0, w, h))
        out.append(t(x0 + w + 12, y0 + 16, name, 12.5, MUTE))
        pts = []
        for i in range(0, 121):
            s = 50 * (1500 / 50) ** (i / 120)
            v = gauss(s, 350, 0.30, 0.45) + gauss(s, 125, 0.035, dimer * 0.95)
            pts.append((x0 + w * i / 120, y0 + h - v * h))
        out.append(poly(pts, TOP if k else HOT, 2.2))
    for s, lab in ((100, "100"), (300, "300"), (1000, "1 kb")):
        xx = 70 + 560 * math.log(s / 50) / math.log(1500 / 50)
        out.append(t(xx, 154 + 80 + 18, lab, 12, MUTE, anchor="middle"))
    out.append(t(215, 62, "adapter dimer, ~120 bp, sharp", 12.5, HOT))
    out.append(t(470, 80, "insert library, broad", 12.5, TOP))
    out.append(t(30, 276, "The dimer is a perfect little amplicon, so it takes a larger share of the "
                          "clusters than its mass suggests.", 13.5, INK))
    return svg(760, 292, "".join(out))


def fig_preamp():
    out = [t(30, 24, "Pre-amplify a few cycles, then split: every tube gets the same templates.", 14, INK)]
    out.append(R(30, 80, 130, 50, PALE, TOP, 1.4))
    out.append(t(95, 100, "one low-input", 13, INK, anchor="middle"))
    out.append(t(95, 118, "sample", 13, INK, anchor="middle"))
    out.append(arrow(160, 105, 214, MUTE))
    out.append(R(214, 74, 150, 62, WARM, HOT, 1.4))
    out.append(t(289, 98, "pre-amplification", 13, HOT, anchor="middle"))
    out.append(t(289, 118, "8 to 12 cycles", 13, HOT, anchor="middle"))
    for i, lab in enumerate(("panel A", "panel B", "index set C", "reserve")):
        y = 40 + i * 46
        out.append(line(364, 105, 440, y + 16, MUTE, 1.4))
        out.append(R(440, y, 130, 32, GREENP if i < 3 else PALE, OK if i < 3 else MUTE, 1.3))
        out.append(t(505, y + 20, lab, 13, INK, anchor="middle"))
    out.append(t(590, 80, "each tube: its own", 13, INK))
    out.append(t(590, 100, "primers, few cycles", 13, INK))
    out.append(t(30, 252, "A limited first round keeps the pool representative; the second round, in separate "
                          "tubes, is specific.", 13.5, INK))
    out.append(t(30, 272, "Used in single-cell and low-input work, for example the cDNA pre-amplification "
                          "step of Smart-seq2.", 13.5, INK))
    return svg(760, 288, "".join(out))


def fig_uracil():
    out = [t(30, 24, "A uracil in the template stops some polymerases and not others.", 14, INK)]
    top = "GATCTUAGCCTAGG"
    for k, (name, y, stop) in enumerate((("proofreading, family B (for example Pfu-type)", 66, True),
                                         ("uracil-tolerant polymerase", 160, False))):
        out.append(t(30, y - 26, name, 13.5, INK, weight="bold"))
        x0 = 90
        for i, ch in enumerate(top):
            col = HOT if ch == "U" else TOP
            out.append(t(x0 + i * DX, y, ch, 13, col, family=MONO, weight="bold" if ch == "U" else None))
        n = 5 if stop else len(top)
        cp = comp(top.replace("U", "A"))
        for i in range(n):
            out.append(t(x0 + i * DX, y + 24, cp[i], 13, BOT, family=MONO))
        out.append(t(x0 - 10, y, "3'", 12, MUTE, anchor="end"))
        px = x0 + n * DX + 6
        out.append(R(px, y + 8, 60, 28, GREENP if not stop else REDP, OK if not stop else BAD, 1.3))
        out.append(t(px + 30, y + 27, "pol", 12.5, OK if not stop else BAD, anchor="middle"))
        if stop:
            out.append(t(px + 74, y + 27, "stalls before the U", 13, BAD))
        else:
            out.append(t(px + 74, y + 27, "copies on through it", 13, OK))
    out.append(t(30, 234, "Matters for dUTP strand marking and for USER adapters: remove the uracil first, "
                          "or choose the right enzyme.", 13.5, INK))
    return svg(760, 250, "".join(out))


def fig_ivt():
    out = [t(30, 24, "In vitro transcription: one DNA template, hundreds of RNA copies, none copied from a copy.", 14, INK)]
    out.append(DNA(60, 300, 100, TOP, 4))
    out.append(DNA(60, 300, 108, BOT, 4))
    out.append(R(60, 90, 40, 28, WARM, HOT, 1.4))
    out.append(t(80, 108, "T7", 12.5, HOT, anchor="middle"))
    out.append(t(60, 78, "T7 promoter + template", 12.5, MUTE))
    for i in range(7):
        y = 60 + i * 12
        x1 = 130 + 40 + i * 24
        out.append(line(110, 100 + (i - 3) * 0, 110, 100, MUTE, 0) if False else "")
    for i in range(6):
        y = 142 + i * 14
        out.append(line(104, 108, 104 + 8, y, MUTE, 0.6, dash="2 3"))
        out.append(arrow(104 + 8, y, 104 + 150 + i * 6, OK, 2.0))
    out.append(t(104 + 8, 142 + 6 * 14 + 12, "RNA copies, antisense to the original mRNA", 12.5, OK))
    out.append(t(350, 90, "Round 1: oligo-dT primer carrying the T7", 13.5, INK))
    out.append(t(350, 110, "promoter makes cDNA, then double strand.", 13.5, INK))
    out.append(t(350, 142, "Round 2: T7 polymerase copies the DNA", 13.5, INK))
    out.append(t(350, 162, "repeatedly. Errors do not compound.", 13.5, INK))
    out.append(t(350, 194, "Used in CEL-seq for single cells; the", 13.5, MUTE))
    out.append(t(350, 214, "product is RNA, so it is 3'-biased.", 13.5, MUTE))
    out.append(t(30, 270, "The cost: more steps, the 3' bias of a poly-dT primer, and a first strand that "
                          "still limits yield.", 13.5, INK))
    return svg(760, 286, "".join(out))


def fig_lam():
    out = [t(30, 24, "LAM-PCR: a one-primer reaction reads from a known end into unknown DNA.", 14, INK)]
    cols = [(30, "1. linear copying"), (270, "2. capture and second strand"), (510, "3. cut, ligate, nested PCR")]
    for x, name in cols:
        out.append(t(x, 52, name, 13.5, INK, weight="bold"))
    # step 1
    out.append(DNA(30, 230, 100, TOP, 4))
    out.append(R(30, 92, 80, 16, WARM, HOT, 1.2))
    out.append(t(70, 104, "provirus end", 10.5, HOT, anchor="middle"))
    for i in range(4):
        y = 124 + i * 14
        out.append(arrow(62, y, 200 + i * 5, OK, 2.0))
        out.append(dot(62, y, 3, HOT))
    out.append(t(30, 196, "biotinylated primer, many cycles:", 12, MUTE))
    out.append(t(30, 212, "copies of the template only", 12, MUTE))
    # step 2
    out.append(C(300, 106, 12, "#caa780", "#7a5a3a", 1.4))
    out.append(t(300, 110, "SA", 9.5, "#fff", anchor="middle"))
    out.append(line(312, 106, 330, 106, HOT, 2.4))
    out.append(DNA(330, 480, 106, OK, 3))
    out.append(DNA(330, 480, 114, BOT, 3))
    out.append(t(270, 196, "streptavidin beads keep only", 12, MUTE))
    out.append(t(270, 212, "the copied strand", 12, MUTE))
    # step 3
    out.append(DNA(510, 700, 106, OK, 3))
    out.append(DNA(510, 700, 114, BOT, 3))
    out.append(R(510, 98, 26, 24, WARM, HOT, 1.2))
    out.append(R(684, 98, 26, 24, PALE, BOT, 1.2))
    out.append(line(676, 94, 676, 126, HOT, 2))
    out.append(t(510, 196, "after the cut, a linker marks", 12, MUTE))
    out.append(t(510, 212, "the unknown end", 12, MUTE))
    out.append(t(30, 252, "Linear copying first means every product comes from a real genomic template "
                          "and the background is low.", 13.5, INK))
    out.append(t(30, 272, "The human application: where in the genome did a lentiviral vector land?", 13.5, INK))
    return svg(760, 288, "".join(out))


def fig_rca_mda():
    out = [t(30, 24, "Phi29 copies by strand displacement at 30 degrees, with no thermal cycling.", 14, INK)]
    out.append(t(40, 56, "rolling circle (RCA)", 13.5, INK, weight="bold"))
    out.append(C(100, 120, 34, "none", TOP, 3))
    out.append(dot(134, 120, 4, HOT))
    out.append(t(100, 124, "circle", 12, MUTE, anchor="middle"))
    out.append(arrow(134, 120, 340, OK, 3))
    for x in (170, 206, 242, 278, 314):
        out.append(line(x, 112, x, 128, WARM if False else "#fff", 2.4))
    out.append(t(240, 150, "one long strand of repeats", 12.5, OK, anchor="middle"))
    out.append(t(400, 56, "multiple displacement (MDA)", 13.5, INK, weight="bold"))
    out.append(DNA(400, 700, 120, TOP, 3))
    for x in (420, 500, 580):
        out.append(arrow(x, 110, x + 60, OK, 2.0))
        out.append(dot(x, 110, 3, HOT))
    for x in (470, 560):
        out.append(arrow(x, 94, x + 60, BOT, 1.8))
        out.append(dot(x, 94, 3, HOT))
    out.append(t(550, 150, "random primers; displaced copies are primed again", 12.5, OK, anchor="middle"))
    out.append(t(30, 200, "High processivity (tens of kb) and low error make it good for few-cell DNA. The "
                          "copy-of-copy branching", 13.5, INK))
    out.append(t(30, 220, "makes the coverage uneven, and chimeras form where a branch is re-primed.", 13.5, INK))
    return svg(760, 236, "".join(out))


def tree(cx, y0, depth, spread, fan, col):
    out, nodes = [], [(cx, y0)]
    gen = [(cx, y0)]
    for d in range(depth):
        nxt = []
        for (x, y) in gen:
            for j in range(fan):
                nx = x + (j - (fan - 1) / 2) * spread / (d + 1)
                ny = y + 28
                out.append(line(x, y, nx, ny, col, 1.2))
                nxt.append((nx, ny))
        gen = nxt
        nodes += nxt
    for x, y in nodes:
        out.append(dot(x, y, 3.2, col))
    return "".join(out)


def fig_trees():
    out = [t(30, 24, "Who is a copy of whom: the shape of the copying decides the bias.", 14, INK)]
    names = ["MDA", "MALBAC", "PTA"]
    for k, nm in enumerate(names):
        cx = 130 + k * 250
        out.append(t(cx, 52, nm, 14, INK, anchor="middle", weight="bold"))
        out.append(dot(cx, 74, 6, HOT))
        if k == 0:
            out.append(tree(cx, 74, 4, 70, 2, TOP))
            out.append(dot(cx, 74, 6, HOT))
            out.append(t(cx, 214, "copies of copies,", 12.5, MUTE, anchor="middle"))
            out.append(t(cx, 232, "some lineages dominate", 12.5, MUTE, anchor="middle"))
        elif k == 1:
            for j in range(-3, 4):
                out.append(line(cx, 74, cx + j * 22, 102, TOP, 1.2))
                out.append(dot(cx + j * 22, 102, 3.2, TOP))
            for j in range(-3, 4):
                for s in (-6, 6):
                    out.append(line(cx + j * 22, 102, cx + j * 22 + s, 130, MUTE, 1))
                    out.append(dot(cx + j * 22 + s, 130, 2.6, MUTE))
            out.append(t(cx, 214, "first rounds copy the", 12.5, MUTE, anchor="middle"))
            out.append(t(cx, 232, "original; then PCR", 12.5, MUTE, anchor="middle"))
        else:
            for j in range(-5, 6):
                out.append(line(cx, 74, cx + j * 14, 102, TOP, 1.2))
                out.append(dot(cx + j * 14, 102, 3.2, TOP))
            out.append(t(cx, 214, "terminators stop the", 12.5, MUTE, anchor="middle"))
            out.append(t(cx, 232, "copies: all from the original", 12.5, MUTE, anchor="middle"))
    out.append(t(30, 268, "Orange: the original template. Fewer generations between original and copy "
                          "means more even coverage.", 13.5, INK))
    return svg(760, 284, "".join(out))


def fig_lamp():
    out = [t(30, 24, "LAMP: four to six primers make a self-priming dumbbell at one temperature.", 14, INK)]
    y = 90
    out.append(DNA(50, 400, y, TOP, 4))
    spans = [("F3", 50, 90), ("F2", 120, 160), ("F1c", 190, 230), ("B1c", 220, 260), ("B2c", 280, 320), ("B3c", 360, 400)]
    for nm, a, b in (("F3", 50, 80), ("F2", 100, 135), ("F1", 150, 185), ("B1", 215, 250), ("B2", 265, 300), ("B3", 340, 375)):
        out.append(R(a, y - 12, b - a, 24, PALE, BOT, 1.2))
        out.append(t((a + b) / 2, y + 4, nm, 11.5, INK, anchor="middle"))
    out.append(t(50, y - 22, "target region (for example a viral sequence in human saliva)", 12, MUTE))
    # dumbbell
    out.append(line(500, 190, 640, 190, TOP, 4))
    out.append(line(500, 198, 640, 198, BOT, 4))
    out.append(C(486, 194, 20, "none", TOP, 2.4))
    out.append(C(654, 194, 20, "none", BOT, 2.4))
    out.append(t(570, 224, "stem", 12, MUTE, anchor="middle"))
    out.append(t(486, 164, "loop", 12, HOT, anchor="middle"))
    out.append(t(654, 164, "loop", 12, HOT, anchor="middle"))
    out.append(t(50, 150, "Bst polymerase, 60-65 C: it displaces strands", 13, INK))
    out.append(t(50, 172, "as it goes, so no denaturation step is needed.", 13, INK))
    out.append(t(50, 204, "Loop primers speed the reaction; the product", 13, INK))
    out.append(t(50, 226, "is a ladder of stem-loop repeats.", 13, INK))
    out.append(t(30, 256, "Used as a diagnostic readout from patient samples, and, with barcodes, as a "
                          "library prep (LAMP-Seq).", 13.5, INK))
    return svg(760, 272, "".join(out))


def fig_sda():
    out = [t(30, 24, "Nicking-enzyme SDA: nick, extend with displacement, repeat, at one temperature.", 14, INK)]
    ys = [78, 148, 238]
    heads = ["1. primer carrying a nicking site binds, a copy is made",
             "2. the nicking enzyme cuts the new strand only",
             "3. polymerase (exo-minus) extends from the nick and displaces the strand"]
    # step 3 keeps its heading where the even spacing would put it and drops the
    # drawing lower, so the long heading clears the "displaced strand" label.
    for nm, y, off in zip(heads, ys, (32, 32, 52)):
        out.append(t(30, y - off, nm, 13, INK, weight="bold"))
    out.append(DNA(60, 400, ys[0], TOP, 3))
    out.append(DNA(60, 400, ys[0] + 8, BOT, 3))
    out.append(R(60, ys[0] - 10, 60, 28, WARM, HOT, 1.2))
    out.append(t(90, ys[0] + 8, "site", 11.5, HOT, anchor="middle"))
    out.append(DNA(60, 400, ys[1], TOP, 3))
    out.append(DNA(60, 400, ys[1] + 8, BOT, 3))
    out.append(R(60, ys[1] - 10, 60, 28, WARM, HOT, 1.2))
    out.append(t(90, ys[1] + 8, "site", 11.5, HOT, anchor="middle"))
    out.append(line(140, ys[1] - 12, 140, ys[1] + 4, HOT, 2.8))
    out.append(t(148, ys[1] - 14, "nick", 12, HOT))
    out.append(DNA(60, 140, ys[2], TOP, 3))
    out.append(DNA(60, 400, ys[2] + 8, BOT, 3))
    out.append(arrow(140, ys[2], 400, OK, 3))
    out.append(poly([(240, ys[2]), (270, ys[2] - 24), (330, ys[2] - 24)], TOP, 3))
    out.append(t(340, ys[2] - 26, "displaced strand", 12.5, TOP))
    out.append(t(440, 80, "The displaced strand binds the", 13, INK))
    out.append(t(440, 100, "opposite primer and the cycle", 13, INK))
    out.append(t(440, 120, "repeats on both strands: growth", 13, INK))
    out.append(t(440, 140, "is exponential, without heat.", 13, INK))
    out.append(t(30, 282, "Walker et al. made the nick with a restriction enzyme and modified "
                          "nucleotides; nicking enzymes do the same without them.", 13.5, MUTE))
    return svg(760, 298, "".join(out))


def arc(cx, cy, r, a0, a1, col):
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    sweep = 1 if a1 > a0 else 0
    ang = a1 + (math.pi / 2 if sweep else -math.pi / 2)
    hx = [x1 + 7 * math.cos(ang), y1 + 7 * math.sin(ang)]
    tri = (f'<path d="M {x1:.1f} {y1:.1f} L {x1 + 7*math.cos(ang) + 4*math.cos(ang+1.57):.1f} '
           f'{y1 + 7*math.sin(ang) + 4*math.sin(ang+1.57):.1f} L {x1 + 7*math.cos(ang) - 4*math.cos(ang+1.57):.1f} '
           f'{y1 + 7*math.sin(ang) - 4*math.sin(ang+1.57):.1f} Z" fill="{col}"/>')
    return (f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 {sweep} {x1:.1f} {y1:.1f}" fill="none" '
            f'stroke="{col}" stroke-width="2.2"/>' + tri)


def fig_inverse():
    out = [t(30, 24, "Inverse PCR: read outward from a known stretch into DNA you know nothing about.", 14, INK)]
    out.append(t(30, 56, "1. cut with an enzyme", 13, INK, weight="bold"))
    out.append(t(30, 74, "absent from the vector", 13, INK, weight="bold"))
    out.append(DNA(30, 270, 110, BOT, 3))
    out.append(R(100, 102, 100, 16, WARM, HOT, 1.2))
    out.append(t(150, 114, "known vector", 11.5, HOT, anchor="middle"))
    for x in (60, 240):
        out.append(line(x, 94, x, 126, TOP, 2.4))
        out.append(t(x, 142, "cut", 12, MUTE, anchor="middle"))
    out.append(t(330, 56, "2. dilute and ligate", 13, INK, weight="bold"))
    out.append(t(330, 74, "the fragment closes", 13, INK, weight="bold"))
    out.append(C(400, 130, 32, "none", BOT, 3))
    out.append(R(380, 94, 40, 10, WARM, HOT, 1.2))
    out.append(t(400, 184, "junction now inside", 12, MUTE, anchor="middle"))
    out.append(t(560, 56, "3. primers point outward", 13, INK, weight="bold"))
    out.append(t(560, 74, "from the known part", 13, INK, weight="bold"))
    out.append(C(630, 130, 32, "none", BOT, 3))
    out.append(R(610, 94, 40, 10, WARM, HOT, 1.2))
    out.append(arc(630, 130, 40, -math.pi / 2 - 0.25, -math.pi / 2 - 1.5, OK))
    out.append(arc(630, 130, 40, -math.pi / 2 + 0.25, -math.pi / 2 + 1.5, OK))
    out.append(t(30, 214, "The product contains the unknown flank, with known sequence at both ends. "
                          "First used for transposon flanks;", 13.5, INK))
    out.append(t(30, 234, "the same trick maps a transgene or provirus in human cells.", 13.5, INK))
    return svg(760, 250, "".join(out))


def fig_nested():
    out = [t(30, 24, "Nested PCR: a second, inner primer pair re-selects the true product.", 14, INK)]
    y1 = 70
    out.append(t(30, y1 + 4, "round 1", 13, MUTE))
    out.append(DNA(120, 700, y1, TOP, 4))
    out.append(arrow(120, y1 - 14, 190, OK, 2.2))
    out.append(arrow(700, y1 + 16, 630, OK, 2.2))
    out.append(t(155, y1 - 20, "outer F", 11.5, OK, anchor="middle"))
    out.append(t(665, y1 + 34, "outer R", 11.5, OK, anchor="middle"))
    out.append(t(30, 150, "round 2", 13, MUTE))
    y2 = 148
    out.append(DNA(220, 600, y2, TOP, 4))
    out.append(arrow(220, y2 - 14, 290, HOT, 2.2))
    out.append(arrow(600, y2 + 16, 530, HOT, 2.2))
    out.append(t(255, y2 - 20, "inner F", 11.5, HOT, anchor="middle"))
    out.append(t(565, y2 + 34, "inner R", 11.5, HOT, anchor="middle"))
    out.append(t(30, 222, "A wrong product from round 1 is unlikely to carry the inner sites, so the "
                          "mispriming is not amplified.", 13.5, INK))
    out.append(t(30, 244, "Anchored PCR: if one end is unknown, add the second primer site yourself with "
                          "a linker or a tail.", 13.5, INK))
    return svg(760, 260, "".join(out))


def fig_splink():
    out = [t(30, 24, "A splinkerette has a hairpin on one strand: its primer site is created only by a real read-through.", 14, INK)]
    y = 90
    out.append(R(40, y - 8, 90, 16, WARM, HOT, 1.2))
    out.append(t(85, y + 4, "known end", 11.5, HOT, anchor="middle"))
    out.append(DNA(130, 520, y, TOP, 3))
    out.append(DNA(130, 520, y + 8, BOT, 3))
    out.append(R(520, y - 8, 70, 24, PALE, BOT, 1.2))
    out.append(line(590, y, 612, y, TOP, 3))
    out.append(C(626, y - 6, 14, "none", TOP, 2.6))
    out.append(line(590, y + 8, 640, y + 8, BOT, 3))
    out.append(t(570, y + 44, "splinkerette: hairpin on the top strand", 12, BOT, anchor="middle"))
    out.append(arrow(50, y - 20, 110, OK, 2.2))
    out.append(t(80, y - 28, "vector primer", 11.5, OK, anchor="middle"))
    out.append(t(30, 168, "1. Vector primer copies across the junction into the adapter.", 13.5, INK))
    out.append(t(30, 190, "2. Only that copy contains the adapter-primer site, so the adapter primer can bind.", 13.5, INK))
    out.append(t(30, 212, "3. A fragment with adapters on both ends has no vector primer site, so it is "
                          "never primed.", 13.5, INK))
    out.append(t(30, 244, "Compare: a plain linker lets the linker primer copy both ends of any fragment, "
                          "which is one-sided background.", 13.5, MUTE))
    return svg(760, 260, "".join(out))


def fig_tiled():
    out = [t(30, 24, "Tiled amplicons: overlapping products split across two tubes, so neighbours never compete.", 14, INK)]
    x0, w = 60, 640
    out.append(DNA(x0, x0 + w, 110, TOP, 5))
    out.append(t(x0, 100, "mitochondrial genome, 16.6 kb (human)", 12.5, MUTE))
    n = 8
    L = w / n
    for i in range(n):
        a = x0 + i * L - (6 if i else 0)
        b = x0 + (i + 1) * L + (6 if i < n - 1 else 0)
        pool = i % 2
        y = 52 if pool == 0 else 150
        col = HOT if pool == 0 else OK
        out.append(R(a, y, b - a, 10, col, "none", 0, 3, 0.85))
        out.append(t((a + b) / 2, y + (-4 if pool == 0 else 24), str(i + 1), 11.5, col, anchor="middle"))
    out.append(t(x0 + w + 6, 62, "pool 1", 12, HOT))
    out.append(t(x0 + w + 6, 160, "pool 2", 12, OK))
    out.append(t(30, 214, "Overlaps make sure every base is covered; alternate pools stop an amplicon's "
                          "primer landing inside its neighbour's product.", 13.5, INK))
    out.append(t(30, 236, "A dropped amplicon shows as a gap in coverage: the primer scheme is the "
                          "first thing to check.", 13.5, INK))
    return svg(760, 252, "".join(out))


def fig_emulsion():
    out = [t(30, 24, "Emulsion PCR: one bead and, ideally, one template in each droplet.", 14, INK)]
    cases = [("empty", 0), ("one template: a clonal bead", 1), ("two templates: a mixed bead", 2)]
    for k, (nm, n) in enumerate(cases):
        cx = 100 + k * 240
        out.append(C(cx, 110, 52, "#eef3f7", BOT, 1.6))
        out.append(C(cx, 110, 14, "#caa780", "#7a5a3a", 1.4))
        for j in range(n):
            ang = j * 3.1 + 0.8
            out.append(poly([(cx + 24 * math.cos(ang), 110 + 24 * math.sin(ang)),
                             (cx + 36 * math.cos(ang + 0.3), 110 + 32 * math.sin(ang + 0.3)),
                             (cx + 30 * math.cos(ang + 0.6), 110 + 40 * math.sin(ang + 0.6))], TOP if j == 0 else HOT, 2.2))
        if n == 1:
            for j in range(10):
                a2 = j * 0.63
                out.append(line(cx + 14 * math.cos(a2), 110 + 14 * math.sin(a2),
                                cx + 22 * math.cos(a2), 110 + 22 * math.sin(a2), TOP, 1.6))
        if n == 2:
            for j in range(10):
                a2 = j * 0.63
                out.append(line(cx + 14 * math.cos(a2), 110 + 14 * math.sin(a2),
                                cx + 22 * math.cos(a2), 110 + 22 * math.sin(a2), TOP if j % 2 else HOT, 1.6))
        out.append(t(cx, 184, nm, 12.5, OK if n == 1 else BAD if n else MUTE, anchor="middle"))
    out.append(t(30, 222, "At 0.3 templates per droplet on average, Poisson gives 74 % empty, 22 % single, "
                          "4 % two or more.", 13.5, INK))
    out.append(t(30, 242, "Dilution is a trade: fewer mixed beads, more empty droplets, and the sequencer "
                          "enriches beads that carry DNA.", 13.5, INK))
    return svg(760, 258, "".join(out))


def fig_rcc():
    out = [t(30, 24, "Rolling-circle consensus: read the same molecule several times and take the majority.", 14, INK)]
    truth = "ACGTTCAGGCTA"
    reads = [("ACGTTCAGGCTA", None), ("ACGATCAGGCTA", 3), ("ACGTTCAGGCTT", 11)]
    out.append(t(30, 60, "circle", 13, MUTE))
    out.append(C(120, 56, 16, "none", TOP, 2.6))
    out.append(arrow(140, 56, 190, MUTE))
    for r, (s, bad) in enumerate(reads):
        y = 86 + r * 28
        out.append(t(30, y, f"copy {r + 1}", 12.5, MUTE))
        for i, ch in enumerate(s):
            out.append(t(120 + i * DX, y, ch, 13, BAD if i == bad else TOP, family=MONO,
                         weight="bold" if i == bad else None))
    y = 86 + 3 * 28 + 6
    out.append(line(112, y - 14, 112 + len(truth) * DX + 8, y - 14, MUTE, 1))
    out.append(t(30, y + 6, "consensus", 12.5, OK, weight="bold"))
    for i, ch in enumerate(truth):
        out.append(t(120 + i * DX, y + 6, ch, 13, OK, family=MONO, weight="bold"))
    out.append(t(340, 100, "A sequencing or polymerase error", 13, INK))
    out.append(t(340, 120, "shows in one copy of three,", 13, INK))
    out.append(t(340, 140, "a real variant in all of them.", 13, INK))
    out.append(t(340, 172, "Errors made while the circle is copied", 13, MUTE))
    out.append(t(340, 192, "in the first round cannot be removed.", 13, MUTE))
    out.append(t(30, 240, "Applied to somatic mutations in human tissue: a variant in 1 of 1000 molecules "
                          "is below raw error, above consensus error.", 13.5, INK))
    return svg(760, 256, "".join(out))


build(__file__, [
    ("curve", fig_curve),
    ("fidelity", fig_fidelity),
    ("overamp", fig_overamp),
    ("bias", fig_bias),
    ("duplicates", fig_dups),
    ("cycles", fig_cycles),
    ("dimer", fig_dimer),
    ("preamp", fig_preamp),
    ("uracil", fig_uracil),
    ("ivt", fig_ivt),
    ("lam", fig_lam),
    ("rca-mda", fig_rca_mda),
    ("trees", fig_trees),
    ("lamp", fig_lamp),
    ("sda", fig_sda),
    ("inverse", fig_inverse),
    ("nested", fig_nested),
    ("splinkerette", fig_splink),
    ("tiled", fig_tiled),
    ("emulsion", fig_emulsion),
    ("rcc", fig_rcc),
])
