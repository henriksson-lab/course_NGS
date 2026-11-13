#!/usr/bin/env python3
"""Figures for the fragmentation unit.  Run: python3 fragmentation/make-figs.py"""
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

def fig_why():
    out = [t(30, 26, "A genome is a few billion bases; a read is a few hundred. Something has to cut.",
             14, INK)]
    out.append(t(30, 62, "chromosome", 13, MUTE))
    out.append(DNA(120, 720, 58, TOP, 4))
    for x in (190, 255, 330, 392, 470, 540, 610, 668):
        out.append(line(x, 46, x, 70, HOT, 1.6))
    out.append(arrow(420, 78, 420, 100) if False else "")
    out.append(t(30, 112, "fragments", 13, MUTE))
    xs = [120, 190, 255, 330, 392, 470, 540, 610, 668, 720]
    for a, b in zip(xs, xs[1:]):
        out.append(DNA(a + 4, b - 4, 108, TOP, 4))
    out.append(t(30, 158, "one library", 13, MUTE))
    x0, x1 = 200, 620
    out.append(R(x0 - 34, 146, 34, 16, WARM, HOT, 1))
    out.append(R(x1, 146, 34, 16, WARM, HOT, 1))
    out.append(R(x0, 150, x1 - x0, 8, PALE, TOP, 1, 1))
    out.append(t(x0 - 17, 158, "P5", 11, HOT, anchor="middle"))
    out.append(t(x1 + 17, 158, "P7", 11, HOT, anchor="middle"))
    out.append(arrow(x0, 184, x0 + 150, OK, 2.2))
    out.append(arrow(x1, 184, x1 - 150, OK, 2.2))
    out.append(t(x0, 206, "read 1", 12.5, OK))
    out.append(t(x1 - 50, 206, "read 2", 12.5, OK))
    out.append(t((x0 + x1) / 2, 136, "insert: the part you actually want to know about", 13,
                 INK, anchor="middle"))
    out.append(t(30, 238, "The size of the insert is a design parameter, not an accident of the "
                          "cutting method.", 14, INK))
    return svg(760, 254, "".join(out))


def fig_methods():
    rows = [
        ("Acoustic shear", "bubble collapse snaps the backbone", "ragged, damaged", "near-random"),
        ("Enzymatic (FS-type)", "paired nicks become a break", "ragged, repaired in kit", "mild sequence bias"),
        ("Tagmentation", "transposase cuts and tags", "adapter already on", "ratio sets size; bias"),
        ("Restriction enzyme", "recognition site", "defined, 5'-P 3'-OH", "set by the genome"),
        ("MNase", "linker DNA between nucleosomes", "5'-OH, 3'-P", "A/T-preferring"),
        ("DNase I", "accessible DNA", "5'-P, 3'-OH", "reports openness"),
        ("Hydrolysis (RNA)", "2'-OH attacks the backbone", "2',3'-cyclic P, 5'-OH", "near-random"),
    ]
    out = []
    cols = [30, 190, 430, 600]
    heads = ["method", "what cuts", "ends left behind", "bias"]
    for x, h in zip(cols, heads):
        out.append(t(x, 24, h, 13, MUTE, weight="bold"))
    out.append(line(30, 32, 740, 32, MUTE, 1))
    for i, r in enumerate(rows):
        y = 56 + i * 31
        out.append(dot(20, y - 4, 4, HOT if i < 3 else TOP if i < 6 else OK))
        out.append(t(cols[0], y, r[0], 14, INK, weight="bold"))
        for x, s in zip(cols[1:], r[1:]):
            out.append(t(x, y, s, 13.5, INK))
    out.append(t(30, 56 + 7 * 31 + 6, "The first three are used to make libraries from anything; the "
                                      "last four also tell you about the sample.", 13.5, INK))
    return svg(760, 56 + 7 * 31 + 24, "".join(out))


def fig_acoustic():
    out = [t(30, 26, "Focused ultrasound: bubbles form, collapse, and the shear snaps the DNA.", 14, INK)]
    # left: DNA with bubble
    out.append(poly([(40, 100), (90, 98), (150, 102), (210, 98), (260, 100)], TOP, 3))
    out.append(C(150, 88, 14, "#dde8f1", BOT, 1.4))
    out.append(t(150, 62, "cavitation bubble", 12, MUTE, anchor="middle"))
    out.append(varrow(150, 132, 112, HOT))
    out.append(t(150, 146, "collapse: local shear", 12, HOT, anchor="middle"))
    out.append(poly([(40, 190), (80, 188), (95, 192)], TOP, 3))
    out.append(poly([(112, 190), (160, 188), (190, 192)], TOP, 3))
    out.append(poly([(206, 190), (260, 190)], TOP, 3))
    out.append(t(150, 214, "ragged, damaged ends", 12, MUTE, anchor="middle"))
    # right: mean size vs time
    x0, y0, w, h = 360, 52, 330, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    pts = []
    for i in range(0, 61):
        x = i / 60
        s = 150 + 3850 * math.exp(-4.2 * x)
        pts.append((x0 + x * w, ylog(s, y0, h, 120, 4200)))
    out.append(poly(pts, HOT, 2.4))
    out.append(t(x0 + w / 2, y0 + h + 22, "treatment time or energy", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 8, "mean size", 12, MUTE, anchor="end"))
    out.append(t(x0 + w + 6, ylog(150, y0, h, 120, 4200) + 4, "floor", 12, MUTE))
    out.append(t(x0 + w * 0.42, y0 + 30, "size falls fast, then flattens", 12.5, INK))
    out.append(t(30, 246, "Size is set by time and energy; the distribution is a smear, not a line, "
                          "and sub-150 bp is expensive to reach.", 14, INK))
    return svg(760, 262, "".join(out))


def fig_enzymatic():
    out = [t(30, 26, "Two nicks on opposite strands, close together, make a double-strand break.", 14, INK)]
    seqtop = "ATGCTTAGCCATGGATCCTAAG"
    seqbot = comp(seqtop)
    cut_t, cut_b = 8, 11
    b, w = duplex(60, 72, seqtop, seqbot, labels=False)
    out.append(b)
    out.append(line(60 + cut_t * DX - 3, 52, 60 + cut_t * DX - 3, 76, HOT, 2.4))
    out.append(line(60 + cut_b * DX - 3, 96, 60 + cut_b * DX - 3, 118, HOT, 2.4))
    out.append(t(60 + cut_t * DX - 8, 46, "nick, top strand", 12, HOT, anchor="end"))
    out.append(t(60 + cut_b * DX + 6, 130, "nick, bottom strand", 12, HOT))
    out.append(varrow(200, 144, 168, MUTE))
    # result: two pieces
    gx = 24
    lt, lb = seqtop[:cut_t], seqbot[:cut_b]
    rt, rb = " " * (cut_t - cut_t) + seqtop[cut_t:], " " * (cut_b - cut_t) + seqbot[cut_b:]
    b1, w1 = duplex(60, 196, lt, lb, labels=False)
    out.append(b1)
    rt2 = " " * 0 + seqtop[cut_t:]
    rb2 = " " * (cut_b - cut_t) + seqbot[cut_b:]
    b2, w2 = duplex(60 + w1 + 60 - (cut_b - cut_t) * DX + (cut_b - cut_t) * DX, 196,
                    rt2, rb2, labels=False)
    out.append(b2)
    out.append(t(60 + w1 + 30, 244, "short overhangs: end repair and A-tailing come next", 12.5, MUTE))
    out.append(t(30, 276, "The break is a chemical event, so it follows the sequence a little: "
                          "expect mild composition bias.", 14, INK))
    return svg(640, 292, "".join(out))


def fig_tagmentation():
    out = [t(30, 26, "Tn5 cuts the target and joins an adapter to each new end in one step.", 14, INK)]
    # target with two transposomes
    out.append(DNA(40, 700, 90, TOP, 4))
    out.append(DNA(40, 700, 98, BOT, 4))
    for cx in (230, 480):
        out.append(R(cx - 26, 46, 52, 30, GREENP, OK, 1.4))
        out.append(t(cx, 66, "Tn5", 13, OK, anchor="middle"))
        out.append(line(cx - 10, 76, cx - 10, 88, OK, 2))
        out.append(line(cx + 10, 76, cx + 10, 88, OK, 2))
    out.append(varrow(370, 116, 144, MUTE))
    # result
    y = 178
    out.append(DNA(40, 214, y, TOP, 4))
    out.append(DNA(40, 214, y + 8, BOT, 4))
    out.append(R(34, y - 8, 14, 24, WARM, HOT, 1))
    out.append(R(206, y - 8, 14, 24, PALE, BOT, 1))
    out.append(DNA(254, 464, y, TOP, 4))
    out.append(DNA(254, 464, y + 8, BOT, 4))
    out.append(R(248, y - 8, 14, 24, PALE, BOT, 1))
    out.append(R(456, y - 8, 14, 24, WARM, HOT, 1))
    out.append(t(222, y + 44, "9 nt gaps either side of each", 12.5, MUTE))
    out.append(t(222, y + 60, "cut: polymerase fills them at 72 C", 12.5, MUTE))
    out.append(t(500, y + 4, "adapters A and B ends already", 13, INK))
    out.append(t(500, y + 22, "present: fragmentation and", 13, INK))
    out.append(t(500, y + 40, "adapter ligation are one step", 13, INK))
    out.append(t(30, 276, "The two adapters arrive at random: only the A+B fragments can be "
                          "amplified with a primer pair.", 14, INK))
    return svg(760, 292, "".join(out))


def fig_tag_ratio():
    out = [t(30, 26, "More transposase per DNA means more cuts and shorter fragments.", 14, INK)]
    g, xs = gel(60, 44, 280, 190, 5, 30, 18)
    out.append(g)
    sizes = [(3000, 400), (1800, 200), (1000, 150), (500, 100), (300, 80)]
    for cx, (hi, lo) in zip(xs, sizes):
        out.append(smear(cx, ylog(hi, 52, 176, 60, 6000), ylog(lo, 52, 176, 60, 6000), 30))
    out.append(band(xs[0] - 0, 0, 0, INK, 0) if False else "")
    for lbl, cx in zip(["low", "", "", "", "high"], xs):
        out.append(t(cx, 252, lbl, 12, MUTE, anchor="middle"))
    out.append(t(200, 270, "enzyme : DNA", 12.5, MUTE, anchor="middle"))
    out.append(t(380, 90, "Too little DNA for the enzyme: over-tagmented,", 13.5, INK))
    out.append(t(380, 110, "fragments too short, many below read length.", 13.5, INK))
    out.append(t(380, 146, "Too much DNA: under-tagmented, long fragments", 13.5, INK))
    out.append(t(380, 166, "that cluster poorly.", 13.5, INK))
    out.append(t(380, 204, "So the DNA input must be measured, and measured", 13.5, HOT))
    out.append(t(380, 224, "by fluorescence, not by absorbance.", 13.5, HOT))
    return svg(760, 284, "".join(out))


def fig_restriction():
    random.seed(11)
    n = 16000
    dna = "".join(random.choice("ACGT") for _ in range(n))
    def sites(motif):
        out, i = [], dna.find(motif)
        while i >= 0:
            out.append(i)
            i = dna.find(motif, i + 1)
        return out
    four = sorted(set(sites("CCGG")))
    six = sorted(set(sites("GAATTC")))
    out = [t(30, 26, "A restriction digest cuts where the genome says, not where you would like.", 14, INK)]
    x0, w = 120, 580
    for k, (name, cuts, y) in enumerate((("4-cutter", four, 70), ("6-cutter", six, 130))):
        out.append(t(30, y + 4, name, 13.5, INK, weight="bold"))
        out.append(DNA(x0, x0 + w, y, TOP, 4))
        for c in cuts:
            out.append(line(x0 + c / n * w, y - 14, x0 + c / n * w, y + 14, HOT, 1.8))
        out.append(t(x0 + w + 10, y + 4, f"{len(cuts)} cuts", 13, MUTE))
    out.append(t(x0, 168, "16 kb of random sequence. A 4-cutter (CCGG) cuts about every 256 bases, a 6-cutter "
                          "(GAATTC) about every 4 kb.", 12.5, MUTE))
    out.append(t(30, 204, "Fragments pile up near the mean, but a few are very long and many are tiny.", 14, INK))
    out.append(t(30, 228, "Useful when you want the same ends in every cell (RRBS, Hi-C, ddRAD).", 14, INK))
    return svg(760, 246, "".join(out))


def fig_nuclease():
    out = [t(30, 26, "Nucleases cut where the chromatin lets them: the fragments report on the sample.", 14, INK)]
    # chromatin
    y = 88
    out.append(DNA(30, 480, y, TOP, 2.4))
    nuc = [60, 140, 220, 400]
    for cx in nuc:
        out.append(C(cx, y, 20, PALE, BOT, 1.6))
    out.append(t(300, y - 34, "DNase I", 12.5, HOT, anchor="middle"))
    out.append(line(300, y - 26, 300, y - 4, HOT, 2.4))
    for cx in (100, 180):
        out.append(line(cx, y + 20, cx, y + 38, TOP, 2))
    out.append(t(140, y + 56, "MNase cuts the linker", 12.5, TOP, anchor="middle"))
    out.append(t(300, y + 56, "DNase I cuts the open gap", 12.5, HOT, anchor="middle"))
    # ladder gel
    g, xs = gel(530, 44, 190, 150, 4, 26, 10)
    out.append(g)
    for cx, n_ in zip(xs, (1, 2, 3, 4)):
        pass
    ys = [ylog(s, 52, 136, 100, 1200) for s in (147, 300, 450, 600, 750)]
    for k, cx in enumerate(xs):
        for j, yy in enumerate(ys):
            if k == 0 and j == 0:
                out.append(band(cx, yy, 26, INK, 0.9))
            elif k == 1 and j <= 1:
                out.append(band(cx, yy, 26, INK, 0.85 if j == 0 else 0.5))
            elif k == 2 and j <= 3:
                out.append(band(cx, yy, 26, INK, 0.85 - j * 0.18))
            elif k == 3 and j <= 4:
                out.append(band(cx, yy, 26, INK, 0.7 - j * 0.1))
    out.append(t(625, 214, "MNase titration", 12.5, MUTE, anchor="middle"))
    out.append(t(30, 196, "Mono-nucleosomes run at about 147 bp plus a little linker.", 14, INK))
    out.append(t(30, 218, "More enzyme or more time: the ladder collapses to one band.", 14, INK))
    return svg(760, 238, "".join(out))


def fig_hydrolysis():
    out = [t(30, 26, "RNA carries its own scissors: the 2'-OH. DNA does not.", 14, INK)]
    def chain(x, y, ribose):
        o = []
        for i in range(3):
            cx = x + i * 92
            o.append(C(cx, y, 15, PALE, BOT, 1.4))
            o.append(t(cx, y + 4, "sugar", 10.5, MUTE, anchor="middle"))
            o.append(R(cx - 10, y + 24, 20, 16, "#dde8f1", BOT, 1))
            o.append(line(cx, y + 15, cx, y + 24, BOT, 1.4))
            if i < 2:
                o.append(line(cx + 15, y, cx + 77, y, TOP, 2))
                o.append(C(cx + 46, y, 5.5, "#fff", TOP, 1.4))
                o.append(t(cx + 46, y - 10, "P", 10.5, TOP, anchor="middle"))
            if ribose and i == 1:
                o.append(line(cx + 6, y - 14, cx + 18, y - 34, HOT, 1.8))
                o.append(t(cx + 22, y - 38, "2'-OH", 12, HOT))
        return "".join(o)
    out.append(t(30, 66, "RNA", 14, INK, weight="bold"))
    out.append(chain(110, 96, True))
    out.append(arrow(200, 70, 232, HOT) if False else "")
    out.append(t(330, 100, "Mg2+ or Zn2+ with heat, or alkali: 2'-OH attacks the", 13, HOT))
    out.append(t(330, 118, "next phosphate, the chain breaks", 13, HOT))
    out.append(t(330, 138, "2',3'-cyclic phosphate + 5'-OH", 13, INK, family=MONO))
    out.append(t(30, 186, "DNA", 14, INK, weight="bold"))
    out.append(chain(110, 214, False))
    out.append(t(330, 214, "no 2'-OH, nothing to attack with: alkali denatures", 13, INK))
    out.append(t(330, 232, "DNA but does not cut it", 13, INK))
    out.append(t(30, 286, "This is why RNA is fragmented by hydrolysis, and DNA needs a physical or "
                          "enzymatic cut.", 14, INK))
    return svg(760, 302, "".join(out))


def fig_targets():
    out = [t(30, 24, "What the sequencer wants sets the target (typical working ranges, log scale).", 14, INK)]
    x0, x1 = 230, 730
    lo, hi = 15, 3e6
    def xp(s):
        return x0 + (x1 - x0) * math.log(s / lo) / math.log(hi / lo)
    rows = [
        ("small RNA", 18, 30, OK),
        ("cell-free DNA (native)", 140, 200, MUTE),
        ("Illumina, PE150 insert", 250, 600, TOP),
        ("PacBio HiFi", 10e3, 25e3, HOT),
        ("nanopore, ligation", 5e3, 60e3, HOT),
        ("nanopore, ultra-long", 100e3, 1.5e6, BAD),
    ]
    for i, (name, a, b, col) in enumerate(rows):
        y = 52 + i * 30
        out.append(t(30, y + 5, name, 13.5, INK))
        out.append(R(xp(a), y - 6, max(6, xp(b) - xp(a)), 12, col, "none", 0, 3, 0.85))
    ya = 52 + len(rows) * 30 - 10
    out.append(line(x0, ya, x1, ya, MUTE, 1.2))
    for s, lab in ((20, "20"), (100, "100"), (1e3, "1 kb"), (1e4, "10 kb"), (1e5, "100 kb"), (1e6, "1 Mb")):
        out.append(line(xp(s), ya, xp(s), ya + 5, MUTE, 1.2))
        out.append(t(xp(s), ya + 20, lab, 12, MUTE, anchor="middle"))
    out.append(t(30, ya + 48, "Short-read machines need you to cut; long-read machines mostly need you "
                              "not to.", 14, INK))
    return svg(760, ya + 62, "".join(out))


def fig_insert_vs_read():
    out = [t(30, 24, "Read length against insert length: three outcomes with 2 x 150 reads.", 14, INK)]
    cases = [(560, "insert 500: gap between reads", OK),
             (240, "insert 240: reads overlap", OK),
             (80, "insert 80: reads enter the adapter", BAD)]
    s = 0.9
    for i, (ins, label, col) in enumerate(cases):
        y = 60 + i * 64
        x0 = 60
        out.append(R(x0 - 26, y - 5, 26, 10, WARM, HOT, 1))
        out.append(R(x0, y - 4, ins * s * 0.8, 8, PALE, TOP, 1, 1))
        xe = x0 + ins * s * 0.8
        out.append(R(xe, y - 5, 26, 10, WARM, HOT, 1))
        r1 = 150 * s * 0.8
        out.append(arrow(x0, y - 14, x0 + r1, OK, 2.2))
        out.append(arrow(xe, y + 16, xe - r1, OK, 2.2))
        if ins < 150:
            out.append(line(xe, y - 14, x0 + r1, y - 14, BAD, 3.2))
            out.append(line(xe - r1, y + 16, x0, y + 16, BAD, 3.2))
        out.append(t(520, y + 5, label, 13, col))
    out.append(t(30, 256, "Below the read length the sequencer reads your adapter: easy to trim, "
                          "but output is wasted.", 13.5, INK))
    return svg(760, 272, "".join(out))


def fig_spri_mechanism():
    out = [t(30, 24, "SPRI beads bind DNA only when PEG crowds it onto the surface.", 14, INK)]
    panels = [("low PEG", 0), ("medium PEG", 1), ("high PEG", 2)]
    for name, k in panels:
        cx = 120 + k * 240
        out.append(t(cx, 54, name, 14, INK, anchor="middle", weight="bold"))
        out.append(C(cx, 140, 34, "#caa780", "#7a5a3a", 1.5))
        out.append(t(cx, 144, "COO-", 11, "#fff", anchor="middle"))
        # long and short dna
        long_bound = k >= 1
        short_bound = k >= 2
        def squiggle(ax, ay, bx, by, col):
            return poly([(ax, ay), ((ax + bx) / 2 - 4, (ay + by) / 2 - 7),
                         ((ax + bx) / 2 + 4, (ay + by) / 2 + 7), (bx, by)], col, 2)
        if long_bound:
            out.append(poly([(cx - 30, 118), (cx - 52, 102), (cx - 70, 118), (cx - 54, 134)], TOP, 2.2))
            out.append(poly([(cx + 30, 118), (cx + 52, 98), (cx + 76, 110), (cx + 60, 130)], TOP, 2.2))
        else:
            out.append(poly([(cx - 100, 84), (cx - 70, 70), (cx - 50, 88)], TOP, 2.2))
            out.append(poly([(cx + 60, 74), (cx + 90, 88), (cx + 100, 70)], TOP, 2.2))
        if short_bound:
            out.append(poly([(cx - 22, 172), (cx - 14, 190)], BOT, 2.6))
            out.append(poly([(cx + 22, 172), (cx + 14, 190)], BOT, 2.6))
        else:
            out.append(poly([(cx - 54, 204), (cx - 40, 196)], BOT, 2.6))
            out.append(poly([(cx + 40, 206), (cx + 54, 198)], BOT, 2.6))
        for px, py in ((cx - 90, 160), (cx + 88, 168), (cx - 70, 190)) if k >= 1 else ():
            out.append(C(px, py, 3, MUTE, MUTE, 1))
        if k == 2:
            for px, py in ((cx + 60, 190), (cx - 100, 140), (cx + 104, 130), (cx + 70, 210)):
                out.append(C(px, py, 3, MUTE, MUTE, 1))
    out.append(C(690, 40, 3, MUTE, MUTE, 1))
    out.append(t(698, 44, "PEG", 11.5, MUTE))
    out.append(t(120, 232, "nothing binds", 13, MUTE, anchor="middle"))
    out.append(t(360, 232, "long DNA binds, short stays free", 13, OK, anchor="middle"))
    out.append(t(600, 232, "everything binds", 13, HOT, anchor="middle"))
    out.append(t(30, 262, "Long DNA collapses at lower PEG than short DNA. The ratio you choose is a PEG "
                          "concentration.", 14, INK))
    return svg(760, 278, "".join(out))


def fig_spri_curve():
    out = [t(30, 24, "Fraction of DNA retained by the beads, by fragment size (illustrative).", 14, INK)]
    x0, y0, w, h = 80, 44, 560, 170
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    smin, smax = 40, 6000
    def xp(s):
        return x0 + w * math.log(s / smin) / math.log(smax / smin)
    curves = [("0.6x", 520, TOP), ("0.8x", 300, OK), ("1.0x", 170, HOT), ("1.8x", 70, BAD)]
    for name, mid, col in curves:
        pts = []
        for i in range(0, 81):
            s = smin * (smax / smin) ** (i / 80)
            f = 1 / (1 + math.exp(-(math.log(s / mid)) * 3.2))
            pts.append((xp(s), y0 + h - f * h))
        out.append(poly(pts, col, 2.4))
        out.append(t(xp(mid * 2.6), y0 + h - 0.72 * h - (0 if name != "1.8x" else 0), name, 13, col, weight="bold") if False else "")
        out.append(t(xp(mid) + 8, y0 + h - 0.5 * h + 20 + 0, name, 13, col, weight="bold"))
    for s, lab in ((50, "50"), (100, "100"), (300, "300"), (1000, "1 kb"), (5000, "5 kb")):
        out.append(line(xp(s), y0 + h, xp(s), y0 + h + 5, MUTE, 1.2))
        out.append(t(xp(s), y0 + h + 20, lab, 12, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 38, "fragment length (bp)", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 6, "100 %", 12, MUTE, anchor="end"))
    out.append(t(x0 - 8, y0 + h, "0", 12, MUTE, anchor="end"))
    out.append(line(x0, y0 + h / 2, x0 + w, y0 + h / 2, MUTE, 0.8, dash="3 4"))
    out.append(t(x0 + w + 6, y0 + h / 2 + 4, "50 %", 12, MUTE))
    out.append(t(30, y0 + h + 66, "Lower ratio: higher cut-off, keeps only the long. The edge is a slope, "
                                  "not a wall. Midpoints here are illustrative; calibrate.", 13.5, INK))
    return svg(760, y0 + h + 80, "".join(out))


def fig_double_sided():
    out = [t(30, 24, "Double-sided selection: two bead additions, and keep the middle.", 14, INK)]
    def hist(x, y, bars, col_map):
        o = []
        for i, (hgt, c) in enumerate(zip(bars, col_map)):
            o.append(R(x + i * 14, y - hgt, 11, hgt, c, "none", 0, 1))
        return "".join(o)
    # three stages
    big, mid, small = TOP, OK, HOT
    cm = [big, big, mid, mid, mid, small, small]
    full = [14, 24, 34, 38, 30, 26, 18]
    out.append(t(30, 56, "50 ul sample", 13, INK, weight="bold"))
    out.append(hist(30, 120, full, cm))
    out.append(arrow(130, 98, 190, MUTE))
    out.append(t(160, 86, "+30 ul beads", 12.5, MUTE, anchor="middle"))
    out.append(t(200, 56, "0.6x: beads bind the long", 13, INK, weight="bold"))
    out.append(hist(200, 120, [14, 24, 0, 0, 0, 0, 0], cm))
    out.append(t(200, 138, "bound: discard", 12, BAD))
    out.append(hist(310, 120, [0, 0, 34, 38, 30, 26, 18], cm))
    out.append(t(310, 138, "supernatant: keep", 12, OK))
    out.append(arrow(420, 98, 480, MUTE))
    out.append(t(450, 86, "+10 ul beads", 12.5, MUTE, anchor="middle"))
    out.append(t(490, 56, "0.8x total: beads bind the middle", 13, INK, weight="bold"))
    out.append(hist(490, 120, [0, 0, 34, 38, 30, 0, 0], cm))
    out.append(t(490, 138, "bound: keep, elute", 12, OK))
    out.append(hist(600, 120, [0, 0, 0, 0, 0, 26, 18], cm))
    out.append(t(600, 138, "supernatant: discard", 12, BAD))
    out.append(t(30, 158, "long", 12, TOP))
    out.append(t(60, 158, "target", 12, OK))
    out.append(t(104, 158, "short", 12, HOT))
    out.append(R(20, 176, 700, 66, "none", MUTE, 1))
    out.append(t(34, 198, "The second addition is counted against the original sample volume:", 13.5, INK))
    out.append(t(34, 218, "0.8x of 50 ul is 40 ul of beads in total, and 30 ul is already in, so add 10 ul.",
                 13.5, INK))
    out.append(t(34, 236, "Do not recompute from the 80 ul supernatant.", 13.5, HOT))
    return svg(760, 258, "".join(out))


def fig_peg():
    out = [t(30, 24, "A bead ratio is a final PEG concentration (bead stock assumed 20 % PEG).", 14, INK)]
    rows = []
    for r in (0.6, 0.8, 1.0, 1.8):
        rows.append((f"{r}x in water", 20 * r / (1 + r), TOP))
    rows.append(("0.8x in 5 % PEG buffer", (5 + 20 * 0.8) / 1.8, BAD))
    x0, sc = 220, 36
    for i, (name, v, col) in enumerate(rows):
        y = 52 + i * 30
        out.append(t(30, y + 5, name, 13.5, INK))
        out.append(R(x0, y - 7, v * sc, 14, col, "none", 0, 3, 0.85))
        out.append(t(x0 + v * sc + 8, y + 5, f"{v:.1f} %", 13, MUTE))
    out.append(t(30, 52 + 5 * 30 + 12, "The last row behaves like a 1.4x clean-up: the PEG carried in the "
                                       "sample counts too.", 13.5, BAD))
    out.append(t(30, 52 + 5 * 30 + 36, "Ligation mixes often contain PEG. Check the datasheet before "
                                       "a size-selective clean-up.", 13.5, INK))
    return svg(760, 52 + 5 * 30 + 52, "".join(out))


def fig_gel_page():
    out = [t(30, 24, "Gel and PAGE: slower, sharper, and you can see what you are cutting.", 14, INK)]
    g, xs = gel(40, 40, 170, 170, 3, 30, 14)
    out.append(g)
    for yy in (ylog(s, 48, 156, 100, 5000) for s in (3000, 1000, 500, 300, 150)):
        out.append(band(xs[0], yy, 30, INK, 0.8))
    out.append(smear(xs[1], ylog(900, 48, 156, 100, 5000), ylog(130, 48, 156, 100, 5000), 30, INK, 0.3))
    out.append(R(xs[1] - 20, ylog(500, 48, 156, 100, 5000), 40, ylog(250, 48, 156, 100, 5000) - ylog(500, 48, 156, 100, 5000),
                 "none", HOT, 1.6, 2))
    out.append(band(xs[2], ylog(330, 48, 156, 100, 5000), 30, INK, 0.8))
    out.append(t(125, 232, "agarose: cut the 250-500 bp slice", 12.5, MUTE, anchor="middle"))
    g2, xs2 = gel(300, 40, 170, 170, 3, 30, 14)
    out.append(g2)
    for yy in (ylog(s, 48, 156, 40, 400) for s in (300, 200, 150, 100, 75, 50)):
        out.append(band(xs2[0], yy, 30, INK, 0.8))
    out.append(band(xs2[1], ylog(120, 48, 156, 40, 400), 30, BAD, 0.8))
    out.append(band(xs2[1], ylog(147, 48, 156, 40, 400), 30, INK, 0.8))
    out.append(R(xs2[1] - 20, ylog(165, 48, 156, 40, 400), 40, ylog(135, 48, 156, 40, 400) - ylog(165, 48, 156, 40, 400),
                 "none", HOT, 1.6, 2))
    out.append(t(385, 232, "PAGE: small RNA library, product above dimer", 12.5, MUTE, anchor="middle"))
    out.append(t(520, 70, "Exact windows: a few bp for PAGE.", 13.5, INK))
    out.append(t(520, 94, "Costs: losses (often half or more),", 13.5, INK))
    out.append(t(520, 114, "an hour or two, a blade and a stain.", 13.5, INK))
    out.append(t(520, 150, "Use when beads cannot separate product", 13.5, INK))
    out.append(t(520, 170, "from contaminant: a 22 nt insert gives", 13.5, INK))
    out.append(t(520, 190, "~145 bp, the adapter dimer ~120 bp.", 13.5, INK))
    return svg(760, 250, "".join(out))


def fig_order():
    out = [t(30, 24, "RNA-seq: fragment the RNA before reverse transcription, or the cDNA after?", 14, INK)]
    for k, (name, cov, y) in enumerate((("RNA fragmented, then primed with random hexamers", "even", 50),
                                        ("oligo-dT on whole mRNA, then cDNA fragmented", "3p", 150))):
        out.append(t(30, y, name, 13.5, INK, weight="bold"))
        out.append(DNA(40, 700, y + 54, TOP, 3))
        out.append(R(676, y + 49, 24, 10, OK, "none", 0, 1, 0.9))
        out.append(t(706, y + 58, "AAAA", 11, MUTE))
        n = 44
        for i in range(n):
            x = 44 + i * (650 / n)
            if cov == "even":
                v = 24 + 5 * math.sin(i * 0.7)
            else:
                v = 6 + 34 * (i / n) ** 4
            out.append(R(x, y + 44 - v, 650 / n - 1, v, col_for(cov), "none", 0, 0, 0.8))
    out.append(t(30, 264, "Same mRNA, different order of steps, different answer: the second order "
                          "piles coverage at the 3' end.", 13.5, INK))
    out.append(t(30, 284, "Other orders that matter: Hi-C digests before ligating and shears after; "
                          "bisulfite fragments by itself.", 13.5, INK))
    return svg(760, 300, "".join(out))


def col_for(cov):
    return OK if cov == "even" else HOT


def fig_partial():
    out = [t(30, 24, "Partial digestion: stop the reaction before it reaches the endpoint.", 14, INK)]
    g, xs = gel(40, 40, 300, 180, 6, 28, 16)
    out.append(g)
    ys = [ylog(s, 48, 166, 100, 4000) for s in (3500, 2400, 1500, 900, 450, 250, 147)]
    # time course lanes: fraction at each ladder rung
    prof = [
        [0.9, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.7, 0.5, 0.3, 0.1, 0.0, 0.0, 0.0],
        [0.4, 0.5, 0.5, 0.4, 0.2, 0.0, 0.0],
        [0.1, 0.2, 0.4, 0.5, 0.5, 0.3, 0.1],
        [0.0, 0.0, 0.1, 0.2, 0.4, 0.6, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.9],
    ]
    for cx, p in zip(xs, prof):
        for yy, v in zip(ys, p):
            if v > 0.05:
                out.append(band(cx, yy, 28, INK, 0.2 + 0.7 * v))
    out.append(t(190, 244, "time or enzyme  ->", 12.5, MUTE, anchor="middle"))
    out.append(t(380, 80, "Run a titration, not a single point.", 14, INK, weight="bold"))
    out.append(t(380, 108, "Lane 1-2: mostly uncut, long ends.", 13.5, INK))
    out.append(t(380, 130, "Lane 3-4: a ladder of partial products;", 13.5, INK))
    out.append(t(380, 150, "each rung is a different number of sites cut.", 13.5, INK))
    out.append(t(380, 172, "Lane 6: one band, every site cut.", 13.5, INK))
    out.append(t(380, 204, "Choose the lane by what you want to read.", 13.5, HOT))
    return svg(760, 262, "".join(out))


def fig_endpoints():
    random.seed(5)
    out = [t(30, 24, "Random shear points are free molecular labels: one read per cell, one length each.", 14, INK)]
    x0 = 150
    for k, (name, y0, n_mol) in enumerate((("few cells carry this integration", 50, 7),
                                           ("a big clone: lengths repeat", 185, 24))):
        out.append(t(30, y0 - 8, name, 13.5, INK, weight="bold"))
        out.append(DNA(x0 - 90, x0 + 560, y0 + 74, MUTE, 3))
        out.append(line(x0, y0 + 64, x0, y0 + 84, HOT, 2.6))
        out.append(t(x0 - 8, y0 + 98, "integration site", 11.5, HOT, anchor="end"))
        seen = set()
        for i in range(n_mol):
            L = random.randint(60, 520) if k == 0 else random.choice([120, 160, 200, 240, 280, 320, 360])
            col = BAD if L in seen else TOP
            seen.add(L)
            yy = y0 + 4 + (i % 10) * 5.5
            out.append(line(x0, yy, x0 + L, yy, col, 2.6))
    out.append(t(30, 322, "Blue: a length seen once, counted as one cell. Red: a repeated length, which "
                          "cannot be told from PCR copies.", 13, INK))
    out.append(t(30, 342, "Few cells: count the lengths. Big clone: model the collisions (Berry 2012), "
                          "or dilute and split.", 13, INK))
    return svg(760, 358, "".join(out))


def fig_typeIIS():
    out = [t(30, 24, "Type IIS and IIG enzymes cut a fixed distance away from where they bind.", 14, INK)]
    y = 84
    out.append(DNA(190, 700, y, TOP, 3))
    out.append(DNA(190, 700, y + 8, BOT, 3))
    out.append(R(40, y - 12, 150, 32, WARM, HOT, 1.4))
    out.append(t(115, y + 8, "TCCRAC", 12.5, HOT, anchor="middle", family=MONO))
    out.append(t(115, y - 20, "linker with MmeI site", 12, HOT, anchor="middle"))
    out.append(R(190, y - 10, 170, 28, GREENP, OK, 1.2, 2, 0.8))
    out.append(t(275, y + 8, "20 bp of genome", 12, OK, anchor="middle"))
    out.append(line(360, y - 22, 360, y + 32, HOT, 2.6))
    out.append(t(360, y - 28, "cut", 12, HOT, anchor="middle"))
    out.append(t(30, 160, "The enzyme binds to the linker, which you control, and cuts into the", 14, INK))
    out.append(t(30, 182, "genome, which you do not. Every molecule yields a tag of the same length.", 14, INK))
    out.append(t(30, 214, "SAGE (about 10 bp tags from human transcripts), DNase-seq (20 bp, MmeI) and", 13.5, MUTE))
    out.append(t(30, 234, "CAGE (27 nt, EcoP15I) all rest on this: short tags, cheap to read, one per molecule.", 13.5, MUTE))
    return svg(760, 250, "".join(out))


def fig_long():
    out = [t(30, 24, "To read long, do not cut. Every handling step is a cut (illustrative).", 14, INK)]
    steps = [("lysed cells, gentle", 2.0e6, OK), ("wide-bore pipetting", 5e5, OK),
             ("vortex", 6e4, BAD), ("column clean-up", 3e4, BAD), ("syringe or g-TUBE", 1e4, HOT)]
    x0, x1 = 230, 720
    lo, hi = 3e3, 3e6
    for i, (name, v, col) in enumerate(steps):
        y = 54 + i * 30
        out.append(t(30, y + 5, name, 13.5, INK))
        out.append(R(x0, y - 7, (x1 - x0) * math.log(v / lo) / math.log(hi / lo), 14, col, "none", 0, 3, 0.85))
    ya = 54 + 5 * 30 - 8
    out.append(line(x0, ya, x1, ya, MUTE, 1.2))
    for s, lab in ((1e4, "10 kb"), (1e5, "100 kb"), (1e6, "1 Mb")):
        xx = x0 + (x1 - x0) * math.log(s / lo) / math.log(hi / lo)
        out.append(line(xx, ya, xx, ya + 5, MUTE, 1.2))
        out.append(t(xx, ya + 20, lab, 12, MUTE, anchor="middle"))
    out.append(t(30, ya + 46, "Bar lengths show the idea, not measurements. Rapid kits use low-ratio "
                              "transposase to cut once or twice.", 13.5, INK))
    return svg(760, ya + 60, "".join(out))


build(__file__, [
    ("why", fig_why),
    ("methods", fig_methods),
    ("acoustic", fig_acoustic),
    ("enzymatic", fig_enzymatic),
    ("tagmentation", fig_tagmentation),
    ("tag-ratio", fig_tag_ratio),
    ("restriction", fig_restriction),
    ("nuclease", fig_nuclease),
    ("hydrolysis", fig_hydrolysis),
    ("targets", fig_targets),
    ("insert-vs-read", fig_insert_vs_read),
    ("spri-mechanism", fig_spri_mechanism),
    ("spri-curve", fig_spri_curve),
    ("double-sided", fig_double_sided),
    ("peg", fig_peg),
    ("gel-page", fig_gel_page),
    ("order", fig_order),
    ("partial", fig_partial),
    ("endpoints", fig_endpoints),
    ("type-iis", fig_typeIIS),
    ("long", fig_long),
])
