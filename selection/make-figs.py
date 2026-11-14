#!/usr/bin/env python3
"""Figures for the selection unit.  Run: python3 selection/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE = "#fbfbf9"
BLUEF = "#e8eef5"
REDF = "#f5eae6"
GREYF = "#dfe3e6"


def bead(x, y, r=20, label=""):
    s = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREYF}" stroke="{MUTE}" stroke-width="1.2"/>')
    if label:
        s += t(x, y + 4, label, 11, MUTE, anchor="middle")
    return s


def cross(x, y, c=BAD, s=6):
    return line(x - s, y - s, x + s, y + s, c, 2) + line(x - s, y + s, x + s, y - s, c, 2)


def wavy(x1, x2, y, color=TOP, w=2.2, amp=3, n=6):
    pts = []
    steps = n * 4
    for i in range(steps + 1):
        x = x1 + (x2 - x1) * i / steps
        pts.append(f"{x:.1f},{y + amp * math.sin(i * math.pi / 2):.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{w}"/>'


# ------------------------------------------------------------------ overview

def fig_map():
    out = [t(40, 26, "Four ways to keep what you want. Each one needs a property that differs.", 14, INK)]
    cols = [("Affinity", "a handle binds the wanted\nmolecule; the rest is washed",
             "biotin, antibody, oligo-dT,\nbaits", TOP, BLUEF),
            ("Depletion", "a handle marks the unwanted\nmolecule for removal",
             "RNase H, Cas9, blockers,\nDSN", BAD, REDF),
            ("Enzymatic", "an enzyme only acts on a\nparticular end or site",
             "exonucleases, MspI,\ncircularisation", OK, "#eaf2ec"),
            ("Physical", "a size, density or cell\nproperty separates them",
             "beads, FACS, gradients,\nfractionation", HOT, "#f7ede6")]
    for i, (h, a, b, c, f) in enumerate(cols):
        x = 40 + i * 168
        out.append(box(x, 44, 156, 150, "", f, c))
        out.append(t(x + 78, 70, h, 15, c, anchor="middle", weight="bold"))
        for j, ln in enumerate(a.split("\n")):
            out.append(t(x + 78, 96 + j * 15, ln, 11, INK, anchor="middle"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 78, 148 + j * 15, ln, 11, MUTE, anchor="middle"))
    out.append(t(40, 224, "Positive selection keeps the wanted; depletion removes the unwanted. "
                          "Which one you pick depends on which is easier to name.", 14, INK))
    return svg(720, 244, "".join(out))


def fig_ratio():
    out = [t(40, 26, "Selection is a ratio, not a switch: a worked example for a human exome.", 14, INK)]
    W = 560
    for i, (lab, frac, note) in enumerate([("before capture", 0.02, "about 2% of reads on target"),
                                           ("after capture", 0.65, "about 65% on target")]):
        y = 56 + i * 64
        out.append(t(40, y + 14, lab, 12.5, INK))
        out.append(f'<rect x="150" y="{y}" width="{W}" height="22" fill="{GREYF}"/>')
        out.append(f'<rect x="150" y="{y}" width="{max(3, W * frac):.0f}" height="22" fill="{HOT}"/>')
        out.append(t(150 + W + 10, y + 16, note, 12, MUTE))
    out.append(t(40, 196, "65% / 2% is roughly 30-fold. The other 35% is still off target, and "
                          "everything lost along the way is lost for good.", 14, INK))
    out.append(t(40, 220, "The exome is about 2% of the genome; the figures are illustrative, "
                          "kits differ.", 12.5, MUTE))
    return svg(760, 240, "".join(out))


# ------------------------------------------------------------------ affinity

def fig_streptavidin():
    out = [t(40, 26, "Biotin on the bait, streptavidin on the bead: hold, wash, release.", 14, INK)]
    titles = ["1. bind", "2. wash", "3. release or amplify"]
    for p in range(3):
        x0 = 40 + p * 225
        out.append(t(x0 + 90, 54, titles[p], 13, INK, anchor="middle"))
        bx, by = x0 + 70, 200
        out.append(bead(bx, by, 22, "SA"))
        if p < 2:
            out.append(line(bx, by - 22, bx, by - 70, TOP, 2.6))        # bait
            out.append(dot(bx, by - 26, 4, HOT))
            out.append(line(bx + 7, by - 70, bx + 7, by - 120, BOT, 2.4))  # target
            out.append(line(bx + 7, by - 70, bx + 7, by - 26, BOT, 2.4, dash="1 4"))
            out.append(t(bx + 18, by - 94, "target", 11.5, BOT))
            out.append(t(bx - 12, by - 44, "bait", 11.5, TOP, anchor="end"))
            out.append(t(bx + 18, by - 28, "biotin", 11.5, HOT))
        if p == 0:
            for k, (xx, yy) in enumerate([(x0 + 150, 130), (x0 + 168, 170), (x0 + 140, 190)]):
                out.append(line(xx, yy, xx + 22, yy - 8, MUTE, 2))
            out.append(t(x0 + 172, 206, "everything else", 11.5, MUTE, anchor="middle"))
        if p == 1:
            out.append(t(x0 + 160, 150, "washed", 11.5, MUTE))
            out.append(t(x0 + 160, 166, "away", 11.5, MUTE))
            out.append(arrow(x0 + 150, 138, x0 + 190, MUTE))
            out.append(f'<rect x="{x0}" y="{by + 36}" width="140" height="8" fill="{INK}" opacity="0.7"/>')
            out.append(t(x0 + 70, by + 58, "magnet", 11.5, MUTE, anchor="middle"))
        if p == 2:
            out.append(line(bx, by - 22, bx, by - 54, TOP, 2.6))
            out.append(dot(bx, by - 26, 4, HOT))
            out.append(arrow(bx + 30, by - 90, bx + 70, HOT))
            out.append(t(bx + 78, by - 86, "heat or alkali", 11.5, HOT))
            out.append(t(bx + 78, by - 70, "frees the target", 11.5, HOT))
            out.append(t(bx - 20, by + 40, "or PCR straight off the bead", 11.5, MUTE))
    out.append(t(40, 282, "The bond is so tight it is effectively permanent, so what you release is "
                          "the target, not the bait.", 14, INK))
    return svg(700, 302, "".join(out))


def fig_handles():
    out = [t(40, 26, "Other handles on the same kind of bead.", 14, INK)]
    out.append(t(40, 56, "antibody on protein A/G bead", 13, INK))
    out.append(bead(120, 220, 24, "protein A"))
    out.append(line(120, 196, 120, 150, MUTE, 3))
    out.append(line(120, 150, 104, 128, MUTE, 3))
    out.append(line(120, 150, 136, 128, MUTE, 3))
    out.append(t(150, 154, "antibody", 11.5, MUTE))
    out.append(f'<ellipse cx="120" cy="114" rx="20" ry="13" fill="{BLUEF}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(t(120, 118, "protein", 10.5, TOP, anchor="middle"))
    out.append(line(100, 108, 70, 92, BOT, 2.4))
    out.append(line(140, 108, 172, 92, BOT, 2.4))
    out.append(t(180, 92, "bound DNA", 11.5, BOT))
    out.append(t(40, 268, "binds a protein, so it keeps whatever the protein holds", 12, MUTE))
    out.append(t(380, 56, "oligo-dT bead and poly(A) RNA", 13, INK))
    out.append(bead(420, 216, 24, "bead"))
    s1, w = seq(452, 212, "TTTTTTTT", BOT)
    out.append(s1)
    check_pairing("AAAAAAAA", "TTTTTTTT")
    s2, _ = seq(452, 182, "AAAAAAAA", TOP)
    out.append(s2)
    out.append(pairs(452, 182, 212, "AAAAAAAA", "TTTTTTTT"))
    out.append(line(440, 212, 450, 212, BOT, 2))
    out.append(line(452 + w, 178, 452 + w + 50, 150, TOP, 2.4))
    out.append(t(452 + w + 56, 150, "mRNA body", 11.5, TOP))
    out.append(t(380, 100, "rRNA, tRNA: no poly(A), washed away", 11.5, BAD))
    out.append(t(40 + 340, 268, "keeps mature mRNA only; fails for degraded or non-polyadenylated RNA", 12, MUTE))
    return svg(780, 288, "".join(out))


def fig_capture():
    out = [t(40, 26, "Hybridisation capture: biotinylated baits pull on-target fragments out of the library.", 14, INK)]
    titles = ["1. hybridise", "2. pull down", "3. wash, then PCR"]
    for p in range(3):
        x0 = 40 + p * 225
        out.append(t(x0 + 90, 54, titles[p], 13, INK, anchor="middle"))
    # panel 1: on-target + off-target fragments, bait annealed
    for k, yy in enumerate([92, 128, 164]):
        on = (k == 1)
        out.append(box(60, yy - 8, 22, 14, "", BLUEF, TOP))
        out.append(line(82, yy - 1, 150, yy - 1, BOT if on else MUTE, 3))
        out.append(box(150, yy - 8, 22, 14, "", REDF, BAD))
    out.append(line(96, 112, 138, 112, HOT, 3))
    out.append(dot(96, 112, 4, HOT))
    out.append(t(104, 106, "", 10))
    out.append(t(190, 118, "bait (biotin)", 11.5, HOT))
    out.append(t(190, 98, "off target", 11.5, MUTE))
    # panel 2: bead takes the on-target only
    x0 = 265
    out.append(bead(x0 + 80, 150, 22, "bead"))
    out.append(line(x0 + 80, 128, x0 + 80, 98, HOT, 2.6))
    out.append(line(x0 + 66, 98, x0 + 98, 98, BOT, 3))
    out.append(box(x0 + 44, 90, 22, 14, "", BLUEF, TOP))
    out.append(box(x0 + 98, 90, 22, 14, "", REDF, BAD))
    out.append(t(x0 + 140, 94, "on target", 11.5, BOT))
    out.append(t(x0 + 104, 150, "the rest stays in", 11.5, MUTE))
    out.append(t(x0 + 104, 166, "the supernatant", 11.5, MUTE))
    # panel 3
    x0 = 490
    out.append(box(x0 + 20, 100, 22, 14, "", BLUEF, TOP))
    out.append(line(x0 + 42, 107, x0 + 110, 107, BOT, 3))
    out.append(box(x0 + 110, 100, 22, 14, "", REDF, BAD))
    out.append(arrow(x0 + 46, 138, x0 + 6, TOP))
    out.append(arrow(x0 + 106, 138, x0 + 146, BAD))
    out.append(t(x0 + 76, 176, "PCR with P5 and P7 primers", 11.5, MUTE, anchor="middle"))
    out.append(t(x0 + 76, 194, "the baits are not amplified", 11.5, MUTE, anchor="middle"))
    out.append(t(40, 226, "The wash is the selection step: too gentle keeps off-target DNA, too harsh "
                          "loses the on-target fragments that bind weakly.", 14, INK))
    return svg(740, 246, "".join(out))


def fig_daisy():
    out = [t(40, 26, "Adapters stick fragments together, so off-target DNA rides along. Blockers prevent it.", 14, INK)]
    ad = "AGATCGGAAGAGC"
    adc = "TCTAGCCTTCTCG"
    for p, (lab, blocked) in enumerate([("without blockers", False), ("with blocking oligos", True)]):
        y0 = 70 + p * 96
        out.append(t(40, y0 - 26, lab, 13, BAD if not blocked else OK))
        # on-target fragment (top) and off-target (bottom) share an adapter-adapter duplex
        out.append(line(60, y0 + 6, 130, y0 + 6, BOT, 3))
        out.append(t(60, y0 - 2, "on target, bait-bound", 10.5, BOT))
        if not blocked:
            b, w = duplex(130, y0 + 12, ad, adc, labels=False)
            out.append(b)
            out.append(line(130 + w, y0 + 12 - 4, 130 + w + 60, y0 + 12 - 4, BOT, 3))
            out.append(line(130 + w, y0 + 12 + 26, 130 + w + 80, y0 + 12 + 26, MUTE, 3))
            out.append(t(130 + w + 90, y0 + 42, "off-target fragment dragged along", 11.5, BAD))
        else:
            b, w = duplex(130, y0 + 12, ad, adc, labels=False, topfill=TOP, botfill=OK)
            out.append(b)
            out.append(t(130 + w + 12, y0 + 42, "blocker (3' modified) occupies the adapter", 11.5, OK))
            out.append(t(130 + w + 12, y0 + 24, "no second fragment can attach", 11.5, OK))
    out.append(t(40, 244, "Blockers are the adapter's reverse complement with the 3' end modified so "
                          "they cannot be extended. Human Cot-1 DNA does the same for repeats.", 13.5, INK))
    return svg(760, 264, "".join(out))


# ------------------------------------------------------------------ depletion

def fig_rnaseh():
    out = [t(40, 26, "RNase H cuts RNA only where a DNA oligo has paired with it.", 14, INK)]
    rna, dna = "GGAUCCGUAAGC", "CCTAGGCATTCG"
    out.append(t(40, 62, "1. tile DNA oligos along every rRNA", 13, INK))
    out.append(line(60, 90, 640, 90, TOP, 3.4))
    out.append(t(50, 94, "rRNA", 11.5, TOP, anchor="end"))
    for i in range(5):
        x = 80 + i * 112
        out.append(line(x, 100, x + 80, 100, HOT, 3))
    out.append(t(60, 130, "mRNA is not touched: no oligo matches it", 11.5, MUTE))
    out.append(line(300, 124, 600, 124, BOT, 2.4))
    out.append(t(40, 156, "2. RNase H cuts the RNA strand of every RNA:DNA hybrid", 13, INK))
    b, w = duplex(60, 188, rna, dna, ltop="5'", rtop="3'", lbot="3'", rbot="5'")
    out.append(b)
    out.append(line(60 + 6 * DX, 168, 60 + 6 * DX, 184, BAD, 2))
    out.append(t(60 + 6 * DX + 8, 174, "cut", 11.5, BAD))
    out.append(t(330, 196, "then DNase removes the DNA oligos,", 12.5, INK))
    out.append(t(330, 214, "and a bead clean-up removes the fragments", 12.5, INK))
    out.append(t(40, 252, "Works on any RNA you can name. The cost is that you need oligos for "
                          "every unwanted sequence, and RNase H must leave the mRNA alone.", 13.5, MUTE))
    return svg(720, 272, "".join(out))


def fig_dash():
    out = [t(40, 26, "DASH: cut the abundant fragments so they lose one of their two primer sites.", 14, INK)]
    out.append(t(40, 52, "library before", 12.5, INK))
    for k, (yy, abundant) in enumerate([(70, True), (96, True), (122, True), (148, False)]):
        c = MUTE if abundant else BOT
        out.append(box(60, yy - 8, 22, 14, "", BLUEF, TOP))
        out.append(line(82, yy - 1, 190, yy - 1, c, 3))
        out.append(box(190, yy - 8, 22, 14, "", REDF, BAD))
    out.append(t(222, 98, "abundant", 11.5, MUTE))
    out.append(t(222, 152, "rare, wanted", 11.5, BOT))
    out.append(arrow(430, 108, 470, HOT))
    out.append(t(440, 90, "Cas9 + guides", 11.5, HOT, anchor="middle"))
    out.append(t(500, 52, "after cutting, then PCR", 12.5, INK))
    for k, (yy, abundant) in enumerate([(70, True), (96, True), (122, True), (148, False)]):
        if abundant:
            out.append(box(500, yy - 8, 22, 14, "", BLUEF, TOP))
            out.append(line(522, yy - 1, 548, yy - 1, MUTE, 3))
            out.append(cross(558, yy - 1, HOT, 5))
            out.append(line(568, yy - 1, 594, yy - 1, MUTE, 3))
            out.append(box(594, yy - 8, 22, 14, "", REDF, BAD))
            out.append(t(630, yy + 3, "each piece has one adapter: no PCR", 11, MUTE))
        else:
            out.append(box(500, yy - 8, 22, 14, "", BLUEF, TOP))
            out.append(line(522, yy - 1, 594, yy - 1, BOT, 3))
            out.append(box(594, yy - 8, 22, 14, "", REDF, BAD))
            out.append(t(630, yy + 3, "intact: amplifies", 11.5, OK))
    out.append(t(40, 196, "Cut before amplification and the primers do the selecting for you. "
                          "Cas9 here is a sequence-specific scissors, not a gene editor.", 13.5, INK))
    out.append(t(40, 218, "Gu et al. built DASH to remove mitochondrial DNA and other abundant "
                          "species from ATAC-type libraries.", 12.5, MUTE))
    return svg(860, 238, "".join(out))


def fig_clamp():
    out = [t(40, 26, "A blocking oligo sits on the abundant allele and cannot be extended.", 14, INK)]
    wt, bl = "GGAGCTGGTGGCGTA", "CCTCGACCACCGCAT"
    out.append(t(40, 56, "wild-type template: blocker pairs perfectly, so it stays and blocks the polymerase", 12.5, INK))
    b, w = duplex(60, 80, wt, bl, ltop="5'", rtop="3'", lbot="3'", rbot="5'", labels=True)
    out.append(b)
    out.append(box(60 + w + 38, 100, 34, 18, "C3", "#f0f0f0", MUTE, 10))
    out.append(t(60 + w + 84, 114, "3' block", 11.5, MUTE))
    out.append(t(40, 156, "mutant template: one mismatch, the blocker melts off, the primer extends", 12.5, INK))
    mt = "GGAGCTGATGGCGTA"
    s1, _ = seq(60, 182, mt, TOP)
    out.append(s1)
    s2, _ = seq(60, 212, bl, BOT)
    out.append(s2)
    out.append(pairs(60, 182, 212, mt, bl))
    # mismatch at index 8: T? mt[8]='T' vs bl[8]='C'
    out.append(f'<rect x="{60 + 7 * DX - 2}" y="168" width="{DX + 2}" height="54" fill="none" stroke="{BAD}" stroke-width="1.4"/>')
    out.append(t(60 + 7 * DX + 6, 240, "mismatch", 11.5, BAD, anchor="middle"))
    out.append(t(330, 182, "the mismatch costs several degrees of Tm", 11.5, MUTE))
    out.append(t(330, 200, "LNA or PNA blockers widen the gap", 11.5, MUTE))
    return svg(640, 260, "".join(out))


def fig_dsn():
    out = [t(40, 26, "Duplex-specific nuclease: abundant sequences find partners first, and are digested.", 14, INK)]
    titles = ["1. denature", "2. re-anneal briefly", "3. DSN, then PCR"]
    for p in range(3):
        x0 = 40 + p * 225
        out.append(t(x0 + 90, 56, titles[p], 13, INK, anchor="middle"))
        out.append(box(x0, 66, 190, 118, "", PALE, MUTE))
    # abundant species (red) many, rare (blue) few
    import random
    random.seed(3)
    ab = [(14, 84), (60, 102), (34, 126), (110, 90), (140, 128), (96, 150), (150, 166), (24, 164)]
    rare = [(70, 170), (126, 108)]
    for (x, y) in ab:
        out.append(line(40 + x, y, 40 + x + 26, y + 6, BAD, 2.4))
        out.append(line(40 + x, y + 5, 40 + x + 26, y + 11, BAD, 2.4)) if False else None
    for (x, y) in rare:
        out.append(line(40 + x, y, 40 + x + 26, y + 6, BOT, 2.4))
    # panel 2: abundant as duplexes (double lines)
    for (x, y) in ab:
        out.append(line(265 + x, y, 265 + x + 26, y + 6, BAD, 2.4))
        out.append(line(265 + x, y + 4, 265 + x + 26, y + 10, BAD, 2.4))
    for (x, y) in rare:
        out.append(line(265 + x, y, 265 + x + 26, y + 6, BOT, 2.4))
    # panel 3: abundant gone
    for (x, y) in rare:
        out.append(line(490 + x, y, 490 + x + 26, y + 6, BOT, 2.4))
    out.append(t(515, 100, "digested", 11.5, MUTE))
    out.append(t(40, 212, "Reassociation speed depends on concentration, so the common sequences become "
                          "double-stranded first. DSN cuts only duplexes.", 13.5, INK))
    out.append(t(40, 234, "Used to normalise cDNA so rare transcripts are not drowned out. "
                          "Over-incubate and you start eating the rare ones too.", 12.5, MUTE))
    return svg(720, 254, "".join(out))


# ------------------------------------------------------------------ enzymatic

def fig_exo():
    out = [t(40, 26, "Exonucleases need a free end. Circles have none, so they survive.", 14, INK)]
    rows = [("ligated into a circle", "circle", OK, "survives"),
            ("linear, unligated", "linear", BAD, "digested from the ends"),
            ("linear genomic carry-over", "linear", BAD, "digested from the ends")]
    for i, (lab, kind, c, res) in enumerate(rows):
        y = 70 + i * 52
        out.append(t(40, y + 4, lab, 12.5, INK))
        if kind == "circle":
            out.append(f'<ellipse cx="300" cy="{y}" rx="46" ry="14" fill="none" stroke="{c}" stroke-width="2.8"/>')
            out.append(f'<ellipse cx="500" cy="{y}" rx="46" ry="14" fill="none" stroke="{c}" stroke-width="2.8"/>')
        else:
            out.append(line(254, y, 346, y, MUTE, 2.8))
            out.append(line(454, y, 470, y, MUTE, 2.8))
            out.append(line(470, y, 546, y, BAD, 2.8, dash="2 5"))
            out.append(cross(552, y, BAD, 5))
        out.append(arrow(360, y, 440, MUTE))
        out.append(t(580, y + 4, res, 12, c))
    out.append(t(300, 52, "before", 12, MUTE, anchor="middle"))
    out.append(t(500, 52, "after exonuclease", 12, MUTE, anchor="middle"))
    out.append(t(40, 220, "Select by topology: the only molecules that keep both a template and "
                          "an intact backbone are the ones you closed on purpose.", 13.5, INK))
    return svg(760, 240, "".join(out))


def fig_mspi():
    out = [t(40, 26, "MspI cuts CCGG whether or not the CpG is methylated. HpaII does not.", 14, INK)]
    top, bot = "TTACCGGAAT", "AATGGCCTTA"
    b, w = duplex(60, 70, top, bot, labels=False)
    out.append(b)
    # cut top between idx3|idx4, bottom between idx5|idx6
    cx_top = 60 + 4 * DX - 1
    out.append(line(cx_top, 52, cx_top, 76, HOT, 2))
    cx_bot = 60 + 6 * DX - 1
    out.append(line(cx_bot, 90, cx_bot, 112, HOT, 2))
    out.append(t(60 + w + 16, 76, "C^CGG leaves a 2-base 5' overhang", 12, HOT))
    out.append(t(40, 150, "5-methylcytosine on the inner C:", 13, INK))
    out.append(dot(60 + 4 * DX + 4, 62, 3.6, BAD))
    out.append(t(60 + 4 * DX + 4, 46, "m", 10.5, BAD, anchor="middle"))
    rows = [("MspI", "cuts", OK), ("HpaII, unmethylated", "cuts", OK), ("HpaII, methylated", "blocked", BAD)]
    for i, (e, r, c) in enumerate(rows):
        out.append(t(60, 176 + i * 22, e, 12.5, INK))
        out.append(t(260, 176 + i * 22, r, 12.5, c))
    out.append(t(380, 176, "In reduced-representation bisulfite sequencing, MspI digests the genome", 12, MUTE))
    out.append(t(380, 194, "so CpG-rich regions give short fragments with CGG ends.", 12, MUTE))
    out.append(t(380, 212, "Choosing the enzyme chooses what the library contains.", 12, MUTE))
    return svg(720, 240, "".join(out))


def fig_circularise():
    out = [t(40, 26, "Selective circularisation: only a probe that finds its target becomes a circle.", 14, INK)]
    steps = ["1. two arms anneal\nnext to a gap", "2. polymerase fills the gap,\nligase closes the circle",
             "3. exonuclease removes\nlinear probe and genomic DNA", "4. PCR across the\nlinker, tagged with a UMI"]
    for i, s in enumerate(steps):
        x0 = 40 + i * 172
        for j, ln in enumerate(s.split("\n")):
            out.append(t(x0 + 70, 52 + j * 14, ln, 11.5, INK, anchor="middle"))
        y = 130
        if i == 0:
            out.append(line(x0, y + 24, x0 + 140, y + 24, BOT, 3))
            out.append(t(x0 + 70, y + 46, "genomic target", 11, BOT, anchor="middle"))
            out.append(line(x0 + 14, y + 8, x0 + 44, y + 8, TOP, 3))
            out.append(line(x0 + 96, y + 8, x0 + 126, y + 8, TOP, 3))
            out.append(f'<path d="M {x0+14} {y+8} C {x0+14} {y-30}, {x0+126} {y-30}, {x0+126} {y+8}" '
                       f'fill="none" stroke="{HOT}" stroke-width="2.4"/>')
            out.append(t(x0 + 70, y - 34, "linker + UMI", 11, HOT, anchor="middle"))
        elif i == 1:
            out.append(line(x0, y + 24, x0 + 140, y + 24, BOT, 3))
            out.append(line(x0 + 14, y + 8, x0 + 126, y + 8, TOP, 3))
            out.append(f'<path d="M {x0+14} {y+8} C {x0+14} {y-30}, {x0+126} {y-30}, {x0+126} {y+8}" '
                       f'fill="none" stroke="{HOT}" stroke-width="2.4"/>')
            out.append(t(x0 + 70, y - 8, "filled", 11, TOP, anchor="middle"))
        elif i == 2:
            out.append(f'<ellipse cx="{x0+70}" cy="{y}" rx="40" ry="22" fill="none" stroke="{OK}" stroke-width="2.8"/>')
            out.append(line(x0 + 4, y + 50, x0 + 40, y + 50, MUTE, 2.6, dash="2 5"))
            out.append(cross(x0 + 48, y + 50, BAD, 5))
            out.append(t(x0 + 70, y + 74, "linear DNA gone", 11, MUTE, anchor="middle"))
        else:
            out.append(arrow(x0 + 10, y - 6, x0 + 60, OK))
            out.append(arrow(x0 + 130, y + 10, x0 + 80, OK))
            out.append(t(x0 + 70, y + 40, "amplicon of the", 11, MUTE, anchor="middle"))
            out.append(t(x0 + 70, y + 54, "captured region", 11, MUTE, anchor="middle"))
    out.append(t(40, 232, "The reaction closes only if both arms bind on either side of a gap of the right "
                          "length, so the ligation is the specificity step.", 13.5, INK))
    return svg(740, 252, "".join(out))


# ------------------------------------------------------------------ physical

def fig_physical():
    out = [t(40, 26, "Physical selection acts on the object, before the chemistry sees it.", 14, INK)]
    heads = ["size", "FACS", "fractionation", "density gradient"]
    for i, h in enumerate(heads):
        x0 = 40 + i * 170
        out.append(box(x0, 44, 156, 156, "", PALE, MUTE))
        out.append(t(x0 + 78, 66, h, 13.5, HOT, anchor="middle", weight="bold"))
    # size: bars of different lengths, keep middle band
    x0 = 40
    for k, L in enumerate([120, 100, 80, 60, 40, 24]):
        c = OK if 50 <= L <= 100 else MUTE
        out.append(line(x0 + 20, 86 + k * 16, x0 + 20 + L, 86 + k * 16, c, 3.2))
    out.append(t(x0 + 78, 192, "beads ratio or gel", 11, MUTE, anchor="middle"))
    # FACS: stream, cells, gate
    x0 = 210
    out.append(line(x0 + 78, 84, x0 + 78, 130, MUTE, 1.6))
    out.append(dot(x0 + 78, 96, 4, OK))
    out.append(dot(x0 + 78, 112, 4, MUTE))
    out.append(line(x0 + 78, 130, x0 + 40, 166, OK, 1.8))
    out.append(line(x0 + 78, 130, x0 + 118, 166, MUTE, 1.8))
    out.append(t(x0 + 30, 180, "kept", 11, OK, anchor="middle"))
    out.append(t(x0 + 126, 180, "waste", 11, MUTE, anchor="middle"))
    out.append(t(x0 + 78, 192, "one label per cell", 11, MUTE, anchor="middle"))
    # fractionation: three tubes
    x0 = 380
    for k, lab in enumerate(["cyto", "nuclear", "chrom."]):
        xx = x0 + 22 + k * 50
        out.append(box(xx - 12, 86, 24, 70, "", "none", MUTE, 10))
        out.append(f'<rect x="{xx-11}" y="{120 - k*8}" width="22" height="{35 + k*8}" fill="{[BLUEF, "#eaf2ec", REDF][k]}"/>')
        out.append(t(xx, 172, lab, 10.5, MUTE, anchor="middle"))
    out.append(t(x0 + 78, 192, "lyse stepwise, spin", 11, MUTE, anchor="middle"))
    # gradient
    x0 = 550
    out.append(box(x0 + 54, 80, 48, 90, "", "none", MUTE, 10))
    for k, (c, lab) in enumerate([(BLUEF, "free"), ("#eaf2ec", "ribosome"), (REDF, "polysome")]):
        out.append(f'<rect x="{x0+55}" y="{82+k*28}" width="46" height="28" fill="{c}"/>')
        out.append(t(x0 + 108, 100 + k * 28, lab, 10, MUTE))
    out.append(t(x0 + 78, 192, "separate by sedimentation", 11, MUTE, anchor="middle"))
    out.append(t(40, 232, "Spin and filter steps are not enrichment by sequence: they enrich by "
                          "what the molecule is part of.", 13.5, INK))
    return svg(740, 252, "".join(out))


# ------------------------------------------------------------------ tricks

def fig_suppression():
    out = [t(40, 26, "Suppression PCR: molecules with identical ends fold into panhandles and stop.", 14, INK)]
    # same ends
    out.append(t(40, 62, "same adapter at both ends", 13, BAD))
    out.append(line(80, 110, 260, 110, MUTE, 2.6))
    out.append(f'<path d="M 80 110 C 70 70, 120 70, 130 100" fill="none" stroke="{TOP}" stroke-width="2.6"/>')
    out.append(f'<path d="M 260 110 C 270 70, 220 70, 210 100" fill="none" stroke="{TOP}" stroke-width="2.6"/>')
    out.append(line(130, 100, 210, 100, MUTE, 2.6))
    out.append(t(170, 130, "stem forms inside one molecule", 11, MUTE, anchor="middle"))
    out.append(arrow(70, 144, 106, HOT))
    out.append(cross(114, 144, BAD, 6))
    out.append(t(130, 148, "primer cannot compete", 11.5, BAD))
    # different ends
    out.append(t(400, 62, "different adapters at the two ends", 13, OK))
    out.append(line(400, 110, 600, 110, MUTE, 2.6))
    out.append(box(400, 102, 24, 16, "A", BLUEF, TOP, 10.5))
    out.append(box(576, 102, 24, 16, "B", REDF, BAD, 10.5))
    out.append(arrow(400, 142, 450, OK))
    out.append(arrow(600, 160, 550, OK))
    out.append(t(500, 188, "both primers bind: exponential PCR", 11.5, OK, anchor="middle"))
    out.append(t(40, 232, "The effect is used to suppress the abundant, shorter or unwanted products and "
                          "to stop one-ended artefacts from amplifying.", 13.5, INK))
    return svg(720, 252, "".join(out))


def fig_endstructure():
    out = [t(40, 26, "Every step filters on ends. Together they keep one class of molecule.", 14, INK)]
    cols = ["ligation needs", "PCR needs", "flow cell needs"]
    for i, c in enumerate(cols):
        out.append(t(300 + i * 150, 54, c, 12, MUTE, anchor="middle"))
    rows = [("adapter A / adapter B", ("yes", "yes", "yes"), OK),
            ("A / A", ("yes", "yes (suppressed)", "no"), BAD),
            ("B / B", ("yes", "yes (suppressed)", "no"), BAD),
            ("one end only", ("yes", "no", "no"), BAD),
            ("no 5' phosphate on insert", ("no", "no", "no"), BAD)]
    for i, (lab, vals, c) in enumerate(rows):
        y = 84 + i * 28
        out.append(t(40, y, lab, 12.5, INK))
        for j, v in enumerate(vals):
            col = OK if v == "yes" else (HOT if "supp" in v else BAD)
            out.append(t(300 + j * 150, y, v, 12, col, anchor="middle"))
    out.append(t(40, 238, "In small-RNA cloning, the 5' phosphate does the selecting: only "
                          "processed RNAs with a 5' phosphate and 3' hydroxyl are ligated.", 13.5, INK))
    out.append(t(40, 258, "Illustrative; real protocols differ in which step does the work.", 12, MUTE))
    return svg(740, 278, "".join(out))


def fig_carrier():
    out = [t(40, 26, "Carrier: sacrificial material that covers the surfaces so the sample survives.", 14, INK)]
    for p, (lab, carrier) in enumerate([("without carrier", False), ("with carrier", True)]):
        x0 = 40 + p * 330
        out.append(t(x0 + 120, 54, lab, 13, INK, anchor="middle"))
        out.append(f'<path d="M {x0} 68 L {x0} 160 Q {x0+120} 200 {x0+240} 160 L {x0+240} 68" '
                   f'fill="none" stroke="{MUTE}" stroke-width="1.6"/>')
        # wall dots
        for k in range(7):
            yy = 80 + k * 12
            if carrier:
                out.append(dot(x0 + 3, yy, 3.2, MUTE))
                out.append(dot(x0 + 237, yy, 3.2, MUTE))
            else:
                if k % 2 == 0:
                    out.append(dot(x0 + 3, yy, 3.2, BOT))
                    out.append(dot(x0 + 237, yy, 3.2, BOT))
        # sample molecules in solution
        n = 3 if not carrier else 5
        for k in range(n):
            out.append(line(x0 + 60 + k * 26, 120 + (k % 2) * 14, x0 + 78 + k * 26, 126 + (k % 2) * 14, BOT, 2.6))
        if carrier:
            for k in range(14):
                out.append(line(x0 + 30 + (k % 7) * 28, 96 + (k // 7) * 52, x0 + 44 + (k % 7) * 28, 100 + (k // 7) * 52, MUTE, 1.6))
    out.append(t(40, 218, "Left: the few molecules you have stick to plastic and beads, and are lost.", 13, INK))
    out.append(t(40, 238, "Right: carrier takes the binding sites. It must be invisible downstream: "
                          "no usable ends, or from a source you can filter out.", 13, INK))
    return svg(720, 258, "".join(out))


def fig_spike():
    out = [t(40, 26, "A spike-in is the only ruler that does not move with the sample.", 14, INK)]
    data = {"control": (100, 100, 100), "treated": (50, 50, 100)}
    for p, (name, sub) in enumerate([("raw reads", "raw"), ("scaled to cell reads", "cells"),
                                     ("scaled to the spike-in", "spike")]):
        x0 = 40 + p * 230
        out.append(t(x0 + 90, 52, name, 13, INK, anchor="middle"))
        out.append(line(x0 + 10, 170, x0 + 180, 170, MUTE, 1))
        for k, cond in enumerate(["control", "treated"]):
            a, b, s = data[cond]
            if sub == "raw":
                h = a
            elif sub == "cells":
                h = a / (a + b) * 200
            else:
                h = a / s * 100
            bx = x0 + 30 + k * 70
            out.append(f'<rect x="{bx}" y="{170 - h * 0.9:.0f}" width="40" height="{h * 0.9:.0f}" fill="{TOP if k == 0 else HOT}" opacity="0.85"/>')
            out.append(t(bx + 20, 186, cond, 11, MUTE, anchor="middle"))
    out.append(t(40, 214, "Treatment halves transcription of both cellular genes. Scaled to cell reads, the "
                          "genes look unchanged.", 13.5, INK))
    out.append(t(40, 234, "Scaled to a fixed spike-in added per cell, the halving appears. Numbers are made up.",
                 13.5, OK))
    return svg(720, 254, "".join(out))


build(__file__, [
    ("map", fig_map),
    ("ratio", fig_ratio),
    ("streptavidin", fig_streptavidin),
    ("handles", fig_handles),
    ("capture", fig_capture),
    ("daisy", fig_daisy),
    ("rnaseh", fig_rnaseh),
    ("dash", fig_dash),
    ("clamp", fig_clamp),
    ("dsn", fig_dsn),
    ("exo", fig_exo),
    ("mspi", fig_mspi),
    ("circularise", fig_circularise),
    ("physical", fig_physical),
    ("suppression", fig_suppression),
    ("endstructure", fig_endstructure),
    ("carrier", fig_carrier),
    ("spike", fig_spike),
])
