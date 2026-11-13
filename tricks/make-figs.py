#!/usr/bin/env python3
"""Figures for the trick-catalogue unit.  Run: python3 tricks/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PB, PR, PP, GR, PG, PO = "#e8eef5", "#f5eae6", "#efe9f3", "#f1f1ee", "#e6f0e8", "#f7ece5"
VIO = "#6b5b8a"
KIND = {"p5": (PB, TOP), "p7": (PR, BAD), "idx": (PP, VIO), "ins": ("none", MUTE),
        "ad": (GR, MUTE), "hot": (PO, HOT), "ok": (PG, OK)}


def chain(x, y, parts, h=22, size=11.5):
    """A row of blocks: parts = [(label, width, kind), ...]. Returns (svg, x_end)."""
    out = []
    for label, w, k in parts:
        fill, col = KIND[k]
        out.append(box(x, y, w, h, label, fill, col, size, col, r=3))
        x += w
    return "".join(out), x


def mbox(x, y, w, h, lines, fill="none", stroke=MUTE, size=12, tcol=INK):
    """Box with several centred lines of text."""
    out = [box(x, y, w, h, "", fill, stroke, r=4)]
    n = len(lines)
    for i, ln in enumerate(lines):
        out.append(t(x + w / 2, y + h / 2 + (i - (n - 1) / 2) * (size + 3) + size * 0.35, ln,
                     size, tcol, anchor="middle"))
    return "".join(out)


def cross(x, y, c=BAD, s=7):
    return line(x - s, y - s, x + s, y + s, c, 2.2) + line(x - s, y + s, x + s, y - s, c, 2.2)


def tick(x, y, c=OK, s=7):
    return line(x - s, y, x - 2, y + s - 1, c, 2.4) + line(x - 2, y + s - 1, x + s, y - s, c, 2.4)


def path(d, stroke=TOP, w=2.4, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round"{ds}/>')


# =============================================================== D1 ligation

def fig_promiscuity():
    out = [t(40, 28, "A ligase joins any 5'-phosphate to any 3'-OH it meets. It cannot tell "
                     "which ones you meant.", 14, INK)]
    rows = [("wanted", [("adapter", 56, "p5"), ("insert", 130, "ins"), ("adapter", 56, "p7")], OK),
            ("insert + insert", [("adapter", 56, "p5"), ("insert", 130, "ins"),
                                 ("insert", 130, "ins"), ("adapter", 56, "p7")], BAD),
            ("adapter + adapter", [("adapter", 56, "p5"), ("adapter", 56, "p7")], BAD)]
    y = 58
    for lab, parts, c in rows:
        out.append(t(40, y + 15, lab, 13, INK))
        s, xe = chain(230, y, parts)
        out.append(s)
        out.append(tick(xe + 24, y + 11, OK) if c == OK else cross(xe + 24, y + 11))
        y += 40
    out.append(t(40, 196, "Concatemers waste insert; adapter dimers cluster better than anything "
                          "else in the tube.", 14, MUTE))
    out.append(t(40, 220, "Each trick below removes one of the unwanted joins by changing a "
                          "chemical group, not by adding more enzyme.", 14, HOT))
    return svg(700, 240, "".join(out))


def fig_block_nick():
    out = [t(40, 28, "Block one strand of the join: the insert has no 5'-phosphate, so it can "
                     "only be joined on one strand.", 14, INK)]
    x0, y1, y2 = 60, 78, 100
    out.append(box(x0, 62, 60, 56, "", PB, TOP, r=3))
    out.append(box(x0 + 60, 62, 210, 56, "", "none", MUTE, r=3))
    out.append(box(x0 + 270, 62, 60, 56, "", PR, BAD, r=3))
    out.append(t(x0 + 30, 52, "adapter", 12, TOP, anchor="middle"))
    out.append(t(x0 + 165, 52, "insert, 5'-OH ends", 12, MUTE, anchor="middle"))
    out.append(t(x0 + 300, 52, "adapter", 12, BAD, anchor="middle"))
    out.append(line(x0 + 6, y1, x0 + 324, y1, TOP, 3))
    out.append(line(x0 + 6, y2, x0 + 54, y2, BOT, 3))
    out.append(line(x0 + 66, y2, x0 + 264, y2, BOT, 3))
    out.append(line(x0 + 276, y2, x0 + 324, y2, BOT, 3))
    for xx in (x0 + 60, x0 + 270):
        out.append(dot(xx, y2, 4.5, HOT))
    out.append(t(x0 + 60, 140, "nick", 12, HOT, anchor="middle"))
    out.append(t(x0 + 270, 140, "nick", 12, HOT, anchor="middle"))
    out.append(t(x0 + 165, 160, "top strand joined; bottom strand cannot be sealed", 12, MUTE,
                 anchor="middle"))
    xr = 470
    out.append(box(xr, 70, 80, 22, "insert", "none", MUTE, 12, MUTE, r=3))
    out.append(box(xr + 100, 70, 80, 22, "insert", "none", MUTE, 12, MUTE, r=3))
    out.append(cross(xr + 90, 81))
    out.append(t(xr + 90, 112, "no 5'-P to donate:", 12, MUTE, anchor="middle"))
    out.append(t(xr + 90, 128, "no concatemers", 12, MUTE, anchor="middle"))
    out.append(t(40, 186, "The nick is repaired later by the polymerase in the first PCR cycle, "
                          "or by the cell if the library is cloned.", 14, INK))
    return svg(700, 206, "".join(out))


def fig_at_overhang():
    out = [t(40, 26, "A single-base overhang: one A on the insert, one T on the adapter. "
                     "Only mixed pairs can anneal.", 14, INK)]
    rows = [("insert + adapter", "CTGACA", "GACTG ", " GATCG", "TCTAGC", True),
            ("insert + insert", "CTGACA", "GACTG ", " GATCG", "ACTAGC", False),
            ("adapter + adapter", "CTGACT", "GACTG ", " GATCG", "TCTAGC", False)]
    y = 66
    for lab, lt, lb, rt, rb, ok in rows:
        out.append(t(40, y + 12, lab, 13, INK))
        check_pairing(lt[:5], lb[:5])
        check_pairing(rt[1:], rb[1:])
        xl = 220
        s1, w1 = seq(xl, y, lt[:5], TOP)
        s2, _ = seq(xl, y + 28, lb, BOT)
        xr = xl + w1 + 40
        s3, w3 = seq(xr, y, rt, TOP)
        s4, _ = seq(xr + DX, y + 28, rb[1:], BOT)
        out += [s1, s2, s3, s4]
        out.append(t(xl + 5 * DX, y, lt[5], 13, HOT, family=MONO))
        out.append(t(xr, y + 28, rb[0], 13, HOT, family=MONO))
        xm = xr - 18
        out.append(t(xm, y + 14, "?", 14, MUTE, anchor="middle"))
        xe = xr + w3 + 34
        out.append(tick(xe, y + 12, OK) if ok else cross(xe, y + 12))
        out.append(t(xe + 18, y + 16, "A:T pairs, ligase can seal" if ok else
                     ("A faces A" if "insert + insert" in lab else "T faces T"), 12.5,
                     OK if ok else BAD))
        y += 62
    out.append(t(40, 252, "One base is enough because the unwanted combinations cannot anneal at "
                          "all, so the ligase never sees a substrate.", 14, MUTE))
    return svg(700, 272, "".join(out))


def fig_hairpin():
    out = [t(40, 26, "A hairpin adapter ligates intramolecularly. One cut then opens it into the "
                     "Y-shaped adapter the flow cell needs.", 14, INK)]
    out.append(t(40, 66, "1  ligate", 13, HOT))
    out.append(t(40, 84, "hairpins join both ends", 12, MUTE))
    out.append(line(300, 60, 560, 60, TOP, 3))
    out.append(line(300, 84, 560, 84, BOT, 3))
    out.append(t(430, 50, "insert", 12, MUTE, anchor="middle"))
    for xx, sg in ((300, -1), (560, 1)):
        out.append(path(f"M {xx} 60 C {xx+sg*34} 60 {xx+sg*34} 84 {xx} 84", VIO, 2.8))
        out.append(dot(xx + sg * 26, 72, 4.5, HOT))
    out.append(t(262, 50, "U in loop", 12, HOT, anchor="end"))
    out.append(t(40, 150, "2  USER enzyme mix", 13, HOT))
    out.append(t(40, 168, "cuts at the U, loop opens", 12, MUTE))
    out.append(line(340, 150, 520, 150, TOP, 3))
    out.append(line(340, 174, 520, 174, BOT, 3))
    out.append(line(340, 150, 310, 132, TOP, 3))
    out.append(line(340, 174, 310, 192, BOT, 3))
    out.append(line(520, 150, 550, 132, TOP, 3))
    out.append(line(520, 174, 550, 192, BOT, 3))
    out.append(t(300, 128, "P5 arm", 12, TOP, anchor="end"))
    out.append(t(300, 204, "unpaired", 12, MUTE, anchor="end"))
    out.append(t(560, 128, "P7 arm", 12, BAD))
    out.append(t(570, 176, "same hairpin on both ends,", 12.5, INK))
    out.append(t(570, 192, "forked only after the cut", 12.5, INK))
    return svg(700, 216, "".join(out))


def fig_splint():
    out = [t(40, 26, "A splint is a bridging oligo: it holds two ends side by side so the ligase "
                     "sees a nick, not two loose ends.", 14, INK)]
    top, bot = "ACTGGTCAGGATCCTT", "TGACCAGTCCTAGGAA"
    check_pairing(top, bot)
    x, y = 150, 80
    s1, _ = seq(x, y, top[:8], TOP)
    s2, _ = seq(x + 8 * DX, y, top[8:], HOT)
    s3, w = seq(x, y + 30, bot, BOT)
    out += [s1, s2, s3, pairs(x, y, y + 30, top, bot)]
    out.append(t(x - 10, y, "5'", 13, MUTE, anchor="end"))
    out.append(t(x - 10, y + 30, "3'", 13, MUTE, anchor="end"))
    out.append(t(x + w + 8, y + 30, "5'", 13, MUTE))
    out.append(t(x + 4 * DX, y - 22, "end of molecule 1", 12, TOP, anchor="middle"))
    out.append(t(x + 12 * DX, y - 22, "end of molecule 2 (5'-P)", 12, HOT, anchor="middle"))
    out.append(line(x + 8 * DX - 2, y - 14, x + 8 * DX - 2, y + 40, HOT, 1.6, dash="3 3"))
    out.append(t(x + 8 * DX - 2, y + 62, "nick: ligase seals it", 12.5, HOT, anchor="middle"))
    out.append(t(x + 8 * DX, y + 84, "splint (bottom strand) is complementary to both ends", 12.5,
                 BOT, anchor="middle"))
    out.append(t(40, 196, "Without it, the two ends meet only by diffusion. Used to close "
                          "libraries into circles (DNBSEQ) and to link barcodes in split-pool "
                          "protocols.", 13, MUTE))
    return svg(700, 216, "".join(out))


def fig_dilute():
    out = [t(40, 26, "Concentration decides which end a free end finds.", 14, INK)]
    out.append(t(40, 58, "concentrated", 13, BAD))
    x = 60
    for i in range(5):
        out.append(box(x, 72, 56, 14, "", PB, TOP, r=3))
        if i < 4:
            out.append(line(x + 56, 79, x + 62, 79, HOT, 2.6))
        x += 62
    out.append(t(60, 108, "neighbours are close: ends join other molecules (concatemers)",
                 12.5, MUTE))
    out.append(t(40, 150, "dilute", 13, OK))
    out.append(path("M 100 190 C 100 150 220 150 220 190 C 220 224 100 224 100 190 Z", TOP, 3))
    out.append(dot(160, 224 - 1, 4.5, HOT))
    out.append(t(240, 190, "neighbours are far; the other end of the same", 12.5, MUTE))
    out.append(t(240, 206, "molecule is nearest: it circularises", 12.5, MUTE))
    out.append(t(40, 246, "Used for Hi-C (join ends that were crosslinked together), iCLIP and "
                          "DNBSEQ (make circles).", 14, INK))
    return svg(700, 262, "".join(out))


# =============================================================== D2 killing

def fig_dimer():
    out = [t(40, 26, "An adapter dimer is a complete library with no insert, and it is "
                     "the shortest one.", 14, INK)]
    sc = 0.62
    rows = [("library", [("P5 · i5 · R1", 62, "p5"), ("insert, about 300 bp", 300 * sc, "ins"),
                         ("R2 · i7 · P7", 62, "p7")]),
            ("adapter dimer", [("P5 · i5 · R1", 62, "p5"), ("R2 · i7 · P7", 62, "p7")])]
    y = 60
    for lab, parts in rows:
        out.append(t(40, y + 15, lab, 13, INK))
        s, xe = chain(170, y, parts, h=24)
        out.append(s)
        y += 44
    out.append(t(170, 160, "about 120-130 bp", 12.5, BAD))
    out.append(t(40, 194, "Why it hurts: it amplifies and clusters more efficiently than the "
                          "library, and reads 100% adapter.", 14, INK))
    out.append(t(40, 218, "Prevent: titrate adapter to the insert, keep the ends blocked, clean up "
                          "twice. Rescue: size-select.", 14, MUTE))
    return svg(700, 238, "".join(out))


def fig_suppression():
    out = [t(40, 26, "Suppression PCR: a molecule with the same long sequence on both ends "
                     "folds on itself before a primer can bind.", 14, INK)]
    out.append(t(40, 56, "same end A ... A'", 13, BAD))
    out.append(path("M 140 150 L 140 118 C 60 118 60 66 150 66 C 240 66 240 118 160 118 L 160 150",
                    TOP, 2.6))
    out.append(line(140, 124, 160, 124, MUTE, 1.2))
    out.append(line(140, 134, 160, 134, MUTE, 1.2))
    out.append(t(140, 170, "A", 12, VIO, anchor="middle"))
    out.append(t(160, 170, "A'", 12, VIO, anchor="start"))
    out.append(t(268, 92, "stem-loop: the ends", 12.5, MUTE))
    out.append(t(268, 108, "pair with each other", 12.5, MUTE))
    out.append(arrow(30, 190, 100, HOT))
    out.append(t(108, 194, "a primer cannot compete", 12.5, HOT))
    out.append(cross(240, 150))
    out.append(t(430, 56, "different ends A ... B'", 13, OK))
    out.append(line(430, 150, 640, 150, TOP, 3))
    out.append(box(430, 130, 36, 16, "A", PB, TOP, 11, TOP, r=2))
    out.append(box(604, 130, 36, 16, "B'", PR, BAD, 11, BAD, r=2))
    out.append(arrow(430, 112, 470, OK))
    out.append(t(476, 116, "primer A binds", 12.5, OK))
    out.append(arrow(640, 94, 600, OK))
    out.append(t(640, 80, "primer B binds", 12.5, OK, anchor="end"))
    out.append(tick(668, 150))
    out.append(t(40, 232, "Used when many products carry the same end (primer by-products, "
                          "tailed cDNA): they are suppressed, the useful ones are not.",
                 13.5, INK))
    return svg(720, 252, "".join(out))


def fig_exo():
    out = [t(40, 26, "Exonuclease I eats single-stranded DNA from the 3' end and leaves "
                     "duplexes alone.", 14, INK)]
    out.append(t(40, 56, "after reverse transcription", 13, MUTE))
    out.append(line(60, 84, 220, 84, TOP, 3))
    out.append(line(60, 98, 200, 98, BOT, 3))
    out.append(t(230, 90, "cDNA:RNA hybrid, kept", 12.5, OK))
    for i in range(5):
        out.append(line(70 + i * 40, 128, 100 + i * 40, 128, HOT, 2.6))
    out.append(t(60, 152, "leftover single-stranded primers", 12.5, HOT))
    out.append(arrow(330, 112, 400, MUTE))
    out.append(t(365, 104, "Exo I", 12.5, MUTE, anchor="middle"))
    out.append(line(430, 84, 590, 84, TOP, 3))
    out.append(line(430, 98, 570, 98, BOT, 3))
    for i in range(5):
        out.append(dot(440 + i * 24, 128, 2.4, MUTE))
    out.append(t(430, 152, "primers reduced to nucleotides", 12.5, MUTE))
    out.append(t(40, 190, "Same logic on a bead (Drop-seq): primers that caught no mRNA are "
                          "removed, bead barcodes that did are protected.", 13.5, INK))
    out.append(t(40, 212, "Heat-inactivate afterwards, or the enzyme will digest the next "
                          "primer you add.", 13.5, MUTE))
    return svg(700, 232, "".join(out))


def fig_rnaseh():
    out = [t(40, 26, "Tile DNA oligos along the abundant RNA; RNase H cuts the RNA only "
                     "where it is paired to DNA.", 14, INK)]
    out.append(line(60, 70, 520, 70, TOP, 3.2))
    out.append(t(536, 74, "rRNA", 12.5, TOP))
    for i in range(6):
        xx = 74 + i * 76
        out.append(line(xx, 84, xx + 60, 84, HOT, 2.6))
        out.append(t(xx + 30, 104, "x", 12, BAD, anchor="middle"))
    out.append(t(60, 126, "DNA oligos (reverse complement of rRNA); x = RNase H cut", 12.5, HOT))
    out.append(line(60, 160, 520, 160, BOT, 3.2))
    out.append(t(536, 164, "mRNA", 12.5, BOT))
    out.append(t(60, 182, "no oligo, no hybrid, no cut: mRNA stays whole", 12.5, OK))
    out.append(t(40, 214, "Then DNase removes the oligos, and what is left is poly(A) and "
                          "non-poly(A) RNA with the rRNA gone.", 14, INK))
    out.append(t(40, 236, "Unlike oligo-dT selection this keeps non-poly(A) transcripts, and works "
                          "on degraded RNA.", 14, MUTE))
    return svg(700, 256, "".join(out))


def fig_dash():
    out = [t(40, 26, "Cut the finished library: a molecule cleaved inside the insert loses one "
                     "adapter and can no longer be amplified.", 14, INK)]
    out.append(t(40, 58, "abundant species, e.g. mitochondrial rRNA cDNA", 13, BAD))
    s, xe = chain(60, 70, [("adapter", 56, "p5"), ("abundant insert", 200, "ins"),
                           ("adapter", 56, "p7")])
    out.append(s)
    out.append(line(60 + 56 + 160, 62, 60 + 56 + 160, 104, HOT, 2.2, dash="4 3"))
    out.append(t(60 + 216, 122, "Cas9 + guide cut here", 12.5, HOT, anchor="middle"))
    out.append(arrow(xe + 14, 82, xe + 60, MUTE))
    s1, x1 = chain(xe + 76, 62, [("adapter", 56, "p5"), ("half", 96, "ins")])
    s2, x2 = chain(xe + 76, 94, [("half", 96, "ins"), ("adapter", 56, "p7")])
    out += [s1, s2]
    out.append(cross(x1 + 20, 73))
    out.append(cross(x2 + 20, 105))
    out.append(t(40, 156, "everything else in the library", 13, OK))
    s, _ = chain(60, 166, [("adapter", 56, "p5"), ("insert (rare)", 200, "ins"),
                            ("adapter", 56, "p7")])
    out.append(s)
    out.append(t(40, 218, "Both adapters are needed for exponential PCR and for clustering, so "
                          "cut molecules drop out. The guide is chosen to hit the unwanted sequence.",
                 13, INK))
    return svg(720, 238, "".join(out))


def fig_methylsens():
    out = [t(40, 26, "Restriction enzymes that read methylation: the cut itself becomes the "
                     "information.", 14, INK)]
    out.append(t(40, 66, "site", 13, MUTE))
    s, w = seq(130, 66, "CCGG", INK, 16)
    out.append(s)
    out.append(t(130 + 1 * 13.5 + 4, 46, "m", 13, HOT, anchor="middle"))
    out.append(t(190, 66, "methylated (5mC at the inner C)", 12.5, HOT))
    out.append(t(40, 106, "MspI", 13, INK))
    out.append(tick(130, 100, OK))
    out.append(t(160, 106, "cuts whether or not it is methylated", 12.5, MUTE))
    out.append(t(40, 140, "HpaII", 13, INK))
    out.append(cross(130, 135, BAD))
    out.append(t(160, 140, "blocked by the methyl group; cuts only unmethylated CCGG", 12.5, MUTE))
    out.append(t(40, 190, "RRBS uses MspI to enrich CpG-rich fragments regardless of state; "
                          "MSCC uses HpaII so that only unmethylated sites receive an adapter.",
                 13, INK))
    out.append(t(40, 212, "Compare the two digests of the same DNA and the difference is the "
                          "methylation of that site.", 13, MUTE))
    return svg(700, 232, "".join(out))


# =============================================================== D3 handles

def fig_template_switch():
    out = [t(40, 26, "Template switching: reverse transcriptase reaches the 5' end of the "
                     "RNA, adds a few Cs and jumps onto an oligo that ends in GGG.", 14, INK)]
    tso_t, tso_b = "CTGAGTGGG", "GACTCACCC"
    rna_t, cdna_b = "GAUCGAUCAAAAAAAA", "CTAGCTAGTTTTTTTT"
    top, bot = tso_t + rna_t, tso_b + cdna_b
    check_pairing(top, bot)
    x, y = 90, 90
    s1, _ = seq(x, y, tso_t, HOT)
    s2, _ = seq(x + 9 * DX, y, rna_t, TOP)
    s3, w = seq(x, y + 30, bot, BOT)
    out += [s1, s2, s3, pairs(x, y, y + 30, top, bot)]
    out.append(t(x + 4 * DX, y - 18, "template-switch oligo (adapter + GGG)", 12.5, HOT, anchor="middle"))
    out.append(t(x + 17 * DX, y - 18, "mRNA, 5' end to poly(A)", 12.5, TOP, anchor="middle"))
    out.append(t(x + 7.5 * DX, y + 54, "added C's pair with GGG", 12.5, BOT, anchor="middle"))
    out.append(t(x + 17 * DX, y + 54, "cDNA from oligo-dT", 12.5, BOT, anchor="middle"))
    out.append(t(x - 10, y + 30, "3'", 13, MUTE, anchor="end"))
    out.append(t(x + w + 8, y + 30, "5'", 13, MUTE))
    out.append(t(40, 190, "Result: the first strand ends in a known sequence on both sides, "
                          "so one primer pair amplifies every full-length cDNA.", 14, INK))
    out.append(t(40, 212, "More efficient at a cap, so it favours full-length molecules, but "
                          "it is not exclusive to caps.", 13.5, MUTE))
    return svg(700, 232, "".join(out))


def fig_tailing():
    out = [t(40, 26, "Terminal transferase adds a homopolymer tail to any 3' end. A primer "
                     "that recognises the tail then reaches the molecule.", 14, INK)]
    cdna = "GATCGATCGA"
    tail = "AAAAAAA"
    prim = "TTTTTTT"
    adapter = "AGTCTGAG"
    x, y = 120, 84
    s1, _ = seq(x, y, cdna, TOP)
    s2, _ = seq(x + 10 * DX, y, tail, HOT)
    s3, _ = seq(x + 10 * DX, y + 30, prim, BOT)
    s4, _ = seq(x + 17 * DX + 4, y + 30, adapter, MUTE)
    out += [s1, s2, s3, s4]
    out.append(pairs(x + 10 * DX, y, y + 30, tail, prim))
    out.append(t(x + 5 * DX, y - 22, "first-strand cDNA (3' end at the tail)", 12.5, TOP, anchor="middle"))
    out.append(t(x + 13.5 * DX, y - 22, "TdT tail", 12.5, HOT, anchor="middle"))
    out.append(t(x + 13.5 * DX, y + 54, "oligo-dT primer", 12.5, BOT, anchor="middle"))
    out.append(t(x + 21 * DX, y + 54, "5' adapter", 12.5, MUTE, anchor="middle"))
    out.append(t(x - 10, y, "5'", 13, MUTE, anchor="end"))
    out.append(t(40, 176, "Used in Tang 2009 (poly(A) tail on first-strand cDNA) and Quartz-Seq. "
                          "Poly(A) polymerase does the same for RNA 3' ends.", 13.5, INK))
    out.append(t(40, 198, "The cost: tail length varies, and homopolymer runs at read starts "
                          "are low-complexity.", 13.5, MUTE))
    return svg(700, 218, "".join(out))


def fig_ss_ligation():
    out = [t(40, 26, "Single-strand library preparation: convert every strand separately, so "
                     "nicks and breaks do not matter.", 14, INK)]
    steps = [("1  denature", "double strands\nbecome single\nstrands"),
             ("2  ligate to 3' end", "biotinylated adapter\njoins each strand"),
             ("3  capture, copy", "beads hold the strand;\na primer makes the\ncomplement"),
             ("4  second adapter", "blunt ligation onto\nthe new duplex end")]
    for i, (h, b) in enumerate(steps):
        x = 40 + i * 168
        out.append(box(x, 50, 150, 108, "", "#fbfbf9", MUTE))
        out.append(t(x + 75, 72, h, 13.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 75, 96 + j * 16, ln, 12, INK, anchor="middle"))
        if i < 3:
            out.append(arrow(x + 154, 104, x + 166, MUTE, head=4))
    out.append(t(40, 188, "Ancient and degraded DNA is full of single-strand breaks; a duplex "
                          "method loses everything that is nicked.", 14, INK))
    out.append(t(40, 210, "Used to sequence an archaic Denisovan genome from a finger bone: the "
                          "DNA was short and damaged.", 13.5, MUTE))
    return svg(720, 228, "".join(out))


def fig_captrap():
    out = [t(40, 26, "Cap trapping: only RNA that carries its cap and a cDNA all the way to "
                     "it survives the selection.", 14, INK)]
    out.append(t(40, 58, "full length", 13, OK))
    out.append(line(130, 62, 400, 62, TOP, 3))
    out.append(line(130, 78, 400, 78, BOT, 3))
    out.append(dot(130, 62, 6, HOT))
    out.append(t(140, 52, "cap (oxidised, biotinylated)", 12, HOT))
    out.append(t(420, 74, "hybrid fully paired: protected", 12.5, OK))
    out.append(t(40, 120, "truncated", 13, BAD))
    out.append(line(130, 124, 400, 124, TOP, 3))
    out.append(line(240, 140, 400, 140, BOT, 3))
    out.append(dot(130, 124, 6, HOT))
    out.append(cross(185, 124))
    out.append(t(420, 130, "single-stranded tail is cut by RNase,", 12.5, BAD))
    out.append(t(420, 146, "cap-biotin is lost", 12.5, BAD))
    out.append(t(40, 190, "Streptavidin beads then keep only the first kind, and the cDNA is "
                          "released: every tag now marks a real transcription start.", 14, INK))
    out.append(t(40, 212, "Used for CAGE to map promoters in human cells; periodate is what "
                          "makes the cap and 3' ribose reactive.", 13.5, MUTE))
    return svg(720, 232, "".join(out))


def fig_circularise():
    out = [t(40, 26, "Circularise, then cut elsewhere: an end that has no handle becomes an "
                     "internal position with sequence on both sides.", 14, INK)]
    out.append(t(40, 56, "1  linear cDNA", 13, HOT))
    s, xe = chain(60, 66, [("primer, barcode, cut site", 150, "hot"), ("cDNA", 170, "ins")])
    out.append(s)
    out.append(dot(xe + 8, 77, 6, BAD))
    out.append(t(xe + 20, 82, "truncated end: the informative base", 12.5, BAD))
    out.append(t(40, 128, "2  ligate ends", 13, HOT))
    out.append(path("M 110 190 C 110 140 250 140 250 190 C 250 232 110 232 110 190 Z", TOP, 3))
    out.append(dot(180, 143, 6, BAD))
    out.append(t(262, 168, "informative end now sits next to", 12.5, MUTE))
    out.append(t(262, 184, "the primer part", 12.5, MUTE))
    out.append(t(40, 258, "3  cut at the site in the primer: a new linear molecule, with the "
                          "informative base next to an adapter that PCR and the sequencer can use.",
                 13.5, INK))
    out.append(line(150, 144, 150, 134, HOT, 2.6))
    out.append(t(150, 128, "cut", 12.5, HOT, anchor="middle"))
    return svg(720, 278, "".join(out))


# =============================================================== D4 info

def fig_truncated():
    out = [t(40, 26, "Truncated adapters: carry only what the first reaction needs, and add the "
                     "rest, including the index, in a second PCR.", 14, INK)]
    out.append(t(40, 62, "round 1", 13, MUTE))
    s, _ = chain(130, 50, [("R1 stub", 62, "ad"), ("locus or tagmented insert", 220, "ins"),
                           ("R2 stub", 62, "ad")])
    out.append(s)
    out.append(t(40, 112, "round 2", 13, MUTE))
    out.append(arrow(130, 132, 200, HOT))
    out.append(t(206, 136, "index primers add i5, P5, i7, P7", 12.5, HOT))
    out.append(t(40, 176, "final", 13, MUTE))
    s, _ = chain(130, 164, [("P5", 36, "p5"), ("i5", 32, "idx"), ("R1", 40, "ad"),
                            ("insert", 190, "ins"), ("R2", 40, "ad"), ("i7", 32, "idx"),
                            ("P7", 36, "p7")])
    out.append(s)
    out.append(t(40, 214, "One set of cheap locus primers, many cheap index primers: "
                          "the combinations are made, not synthesised.", 14, INK))
    out.append(t(40, 236, "Tn5 does this as well: it inserts adapter stubs, PCR completes them "
                          "(ATAC-seq, Nextera).", 13.5, MUTE))
    return svg(700, 256, "".join(out))


def fig_inline_vs_index():
    out = [t(40, 26, "Where to put a barcode: inside a read (inline) or in its own index read.",
             14, INK)]
    out.append(t(40, 60, "inline", 13, HOT))
    s, xe = chain(130, 48, [("cell barcode", 80, "hot"), ("UMI", 44, "idx"),
                            ("polyT / cDNA, read 1", 176, "ins")])
    out.append(s)
    out.append(t(130, 90, "costs read cycles, but can be added early, before pooling, by "
                          "RT or ligation", 12.5, MUTE))
    out.append(t(40, 134, "index read", 13, HOT))
    s, xe = chain(130, 122, [("P5", 36, "p5"), ("i5", 32, "idx"), ("insert", 190, "ins"),
                             ("i7", 32, "idx"), ("P7", 36, "p7")])
    out.append(s)
    out.append(t(130, 164, "read by its own primer and cycles; costs no insert bases, but "
                          "only exists after the index PCR", 12.5, MUTE))
    out.append(t(40, 204, "Rule of thumb: many barcodes added at the start (single cells, "
                          "split-pool) go inline; sample barcodes added at the end go in the "
                          "index.", 13.5, INK))
    return svg(700, 224, "".join(out))


def fig_stagger():
    out = [t(40, 26, "Staggered primers: shift the same amplicon by a different number of "
                     "bases, so each cycle sees all four.", 14, INK)]
    shared = "GGATCAGT"
    spacers = ["", "T", "CA", "GTC"]
    col = {"A": OK, "C": TOP, "G": HOT, "T": BAD}
    y = 66
    out.append(t(40, y - 12, "shared amplicon start", 12, MUTE))
    for sp in spacers:
        x = 40 + 3 * DX - len(sp) * DX
        for i, ch in enumerate(sp):
            out.append(t(x + i * DX, y + 14, ch, 13, MUTE, family=MONO))
        for i, ch in enumerate(shared):
            out.append(t(x + len(sp) * DX + i * DX, y + 14, ch, 13, col[ch], family=MONO))
        out.append(t(40 + 3 * DX + 8 * DX + 12, y + 14, f"+{len(sp)}" if sp else "+0", 12, MUTE))
        y += 22
    out.append(t(400, 76, "cycle by cycle:", 13, INK))
    out.append(t(400, 98, "without stagger every cluster", 12.5, BAD))
    out.append(t(400, 114, "shows the same base; the camera", 12.5, BAD))
    out.append(t(400, 130, "cannot find or phase-correct them", 12.5, BAD))
    out.append(t(400, 156, "with stagger the mixture looks", 12.5, OK))
    out.append(t(400, 172, "like a normal library", 12.5, OK))
    out.append(t(40, 206, "Amplicon and CRISPR-screen readouts: the Joung protocol mixes ten "
                          "forward primers that differ in stagger. PhiX is the alternative.",
                 13.5, INK))
    return svg(720, 226, "".join(out))


# =============================================================== D5 counting

def fig_umi_concept():
    out = [t(40, 26, "Reads count amplification. Unique molecular identifiers count what you "
                     "started with.", 14, INK)]
    cols = [HOT, TOP, OK]
    out.append(t(40, 56, "start: 3 molecules", 13, MUTE))
    for i, (c, lab) in enumerate(zip(cols, ["gene A", "gene A", "gene B"])):
        x = 60 + i * 110
        out.append(dot(x, 80, 7, c))
        out.append(line(x + 12, 80, x + 74, 80, MUTE, 3))
        out.append(t(x + 42, 70, lab, 11.5, MUTE, anchor="middle"))
    out.append(arrow(400, 80, 440, MUTE))
    out.append(t(420, 66, "PCR", 12.5, MUTE, anchor="middle"))
    out.append(t(460, 56, "after PCR: reads per molecule", 13, MUTE))
    for i, (n, c) in enumerate(zip([9, 2, 4], cols)):
        for j in range(n):
            out.append(dot(470 + j * 14, 74 + i * 20, 5, c))
    out.append(t(40, 170, "count reads:  gene A = 11, gene B = 4", 14, BAD))
    out.append(t(40, 194, "count UMIs:   gene A = 2, gene B = 1  (each colour is one UMI)", 14, OK))
    out.append(t(40, 224, "The UMI must be added before any amplification, and must differ "
                          "between molecules.", 14, INK))
    return svg(700, 244, "".join(out))


def fig_umi_where():
    out = [t(40, 26, "Where the UMI goes depends on which step first touches each "
                     "molecule.", 14, INK)]
    rows = [("on the RT primer", [("cell BC", 52, "hot"), ("UMI", 40, "idx"), ("oligo-dT", 60, "ad"),
                                  ("cDNA 3' end", 150, "ins")],
             "10x, Drop-seq, CEL-seq: 3' counting"),
            ("on the TSO", [("adapter", 52, "ad"), ("UMI", 40, "idx"), ("GGG", 30, "ad"),
                            ("cDNA 5' end", 150, "ins")],
             "Smart-seq3: 5' UMI, full-length body"),
            ("on the ligated adapter", [("UMI", 40, "idx"), ("adapter", 52, "ad"),
                                        ("DNA insert", 150, "ins"), ("adapter", 52, "ad"),
                                        ("UMI", 40, "idx")],
             "Safe-SeqS, duplex methods: DNA molecules")]
    y = 52
    for lab, parts, note in rows:
        out.append(t(40, y + 15, lab, 12.5, INK))
        s, xe = chain(220, y, parts)
        out.append(s)
        out.append(t(xe + 14, y + 15, note, 12, MUTE))
        y += 46
    out.append(t(40, 204, "A UMI of L bases gives 4^L labels, but errors in it create false "
                          "molecules: allow for them when counting.", 14, INK))
    return svg(820, 224, "".join(out))


def fig_duplex():
    out = [t(40, 26, "Duplex tags: a real mutation is on both strands; a polymerase or "
                     "chemical error is on one.", 14, INK)]
    out.append(t(40, 58, "one original molecule, two strands, each tagged", 13, MUTE))
    out.append(box(60, 68, 36, 16, "a", PB, TOP, 11, TOP, r=2))
    out.append(line(96, 76, 300, 76, TOP, 3))
    out.append(box(300, 68, 36, 16, "b", PR, BAD, 11, BAD, r=2))
    out.append(box(60, 90, 36, 16, "b", PR, BAD, 11, BAD, r=2))
    out.append(line(96, 98, 300, 98, BOT, 3))
    out.append(box(300, 90, 36, 16, "a", PB, TOP, 11, TOP, r=2))
    out.append(dot(200, 76, 5, HOT))
    out.append(dot(200, 98, 5, HOT))
    out.append(t(350, 90, "mutation at the same position, both strands", 12.5, HOT))
    out.append(t(40, 140, "strand family a-b:  reads agree  -> consensus", 13, TOP))
    out.append(t(40, 162, "strand family b-a:  reads agree  -> consensus", 13, BAD))
    out.append(t(40, 190, "a variant is real only if both families carry it", 14, OK))
    out.append(t(40, 216, "an error on one strand appears in one family only: discarded. "
                          "Error rates drop by orders of magnitude.", 13.5, INK))
    out.append(t(40, 238, "NanoSeq takes the same idea further: restriction fragments and "
                          "ddNTP A-tailing so that only duplex-able molecules amplify.", 13.5, MUTE))
    return svg(720, 258, "".join(out))


def fig_rca():
    out = [t(40, 26, "Read the same molecule several times, and the errors, which fall in "
                     "different places, vote out.", 14, INK)]
    out.append(path("M 90 130 C 90 70 200 70 200 130 C 200 180 90 180 90 130 Z", TOP, 3))
    out.append(t(145, 130, "circle", 13, MUTE, anchor="middle"))
    out.append(arrow(214, 130, 262, MUTE))
    out.append(t(238, 118, "roll", 12, MUTE, anchor="middle"))
    x = 280
    errs = [[18, 60], [40, 110], [8, 90]]
    for k in range(3):
        out.append(box(x + k * 130, 112, 126, 22, "", PB, TOP, r=3))
        out.append(t(x + k * 130 + 63, 127, "copy %d" % (k + 1), 11.5, TOP, anchor="middle"))
        out.append(t(x + k * 130 + errs[k][0] * 2.4, 108, "x", 12, BAD, anchor="middle"))
    out.append(box(x, 160, 378, 22, "consensus: each error is outvoted by the other copies",
                   PG, OK, 12, OK, r=3))
    out.append(t(40, 220, "Used to correct nanopore errors on long cDNA (R2C2); PacBio circular "
                          "consensus is the same principle.", 14, INK))
    return svg(700, 240, "".join(out))


def fig_spikein():
    out = [t(40, 26, "A spike-in is a known quantity added at the start. Everything is measured "
                     "against it.", 14, INK)]
    out.append(t(40, 58, "sample 1", 13, MUTE))
    out.append(t(40, 118, "sample 2", 13, MUTE))
    for y, endo, spk in ((46, 160, 40), (106, 320, 40)):
        out.append(box(130, y, endo, 22, "", PB, TOP, r=3))
        out.append(t(130 + endo / 2, y + 15, "endogenous reads", 11.5, TOP, anchor="middle"))
        out.append(box(130 + endo + 6, y, spk, 22, "", PO, HOT, r=3))
        out.append(t(130 + endo + 6 + spk / 2, y + 15, "spike", 11, HOT, anchor="middle"))
    out.append(t(40, 176, "Spike-in reads are the same in both: the true difference in "
                          "endogenous input is 2x.", 14, INK))
    out.append(t(40, 198, "Without it, per-million normalisation hides a global change.",
                 14, BAD))
    out.append(t(40, 224, "Examples: synthetic ERCC RNA in RNA-seq, foreign chromatin in "
                          "ChIP, carry-over E. coli DNA in CUT&amp;Tag.", 13.5, MUTE))
    return svg(700, 244, "".join(out))


def fig_budget():
    out = [t(40, 26, "The molecule budget: you cannot sequence more unique molecules than you "
                     "had, however many cycles you run.", 14, INK)]
    stages = [("1 ng human DNA", 300, TOP), ("after ligation, 30% assumed", 90, BOT),
              ("after cleanup, 70% of that", 63, OK)]
    y = 54
    for lab, n, c in stages:
        out.append(box(60, y, n * 1.4, 22, "", "none", c, r=3))
        out.append(f'<rect x="60" y="{y}" width="{n*1.4}" height="22" fill="{c}" opacity="0.22"/>')
        out.append(t(60 + n * 1.4 + 10, y + 15, f"{n} copies of each locus  ({lab})", 12.5, INK))
        y += 34
    out.append(t(40, 172, "1 ng is about 300 haploid genome copies (3.3 pg each). 30x coverage "
                          "of unique molecules needs most of them.", 13.5, INK))
    out.append(t(40, 194, "More PCR cycles add reads, not information: duplicates rise "
                          "instead. PCR-free is best when input allows.", 13.5, INK))
    return svg(720, 214, "".join(out))


# =============================================================== D6 little material

def fig_preamp_split():
    out = [t(40, 26, "Pre-amplify while everything is still one tube, then split: the "
                     "scarce step is shared by every later question.", 14, INK)]
    out.append(mbox(50, 60, 110, 50, ["one cell", "lysate"], PB, TOP, 12, TOP))
    out.append(arrow(168, 85, 218, MUTE))
    out.append(t(193, 74, "RT + PCR", 12, MUTE, anchor="middle"))
    out.append(box(224, 60, 110, 50, "cDNA pool", PO, HOT, 12.5))
    for i, lab in enumerate(["sequencing library", "qPCR check of genes", "archive for later"]):
        y = 50 + i * 38
        out.append(arrow(342, 85, 400, MUTE) if i == 1 else line(342, 85, 396, y + 14, MUTE, 1.4))
        out.append(box(404, y, 170, 28, lab, "none", MUTE, 12))
    out.append(t(40, 170, "Smart-seq2 amplifies cDNA first, then tagments a small part; G&amp;T-seq "
                          "splits the RNA and DNA of one cell.", 13.5, INK))
    out.append(t(40, 192, "The price: amplification bias is baked into the pool, so check the "
                          "pool before spending it.", 13.5, MUTE))
    return svg(700, 212, "".join(out))


def fig_beads():
    out = [t(40, 26, "Keep the molecule on a bead: every buffer change is a wash, never a "
                     "tube-to-tube transfer.", 14, INK)]
    steps = ["bind", "wash", "react", "wash", "react", "elute"]
    for i, s in enumerate(steps):
        x = 50 + i * 106
        out.append(box(x, 60, 86, 44, "", "none", MUTE, r=4))
        out.append(dot(x + 43, 90, 8, HOT))
        out.append(line(x + 43, 90, x + 24, 72, TOP, 2))
        out.append(line(x + 43, 90, x + 62, 74, TOP, 2))
        out.append(t(x + 43, 124, s, 12.5, INK, anchor="middle"))
        if i < 5:
            out.append(arrow(x + 90, 82, x + 104, MUTE, head=4))
    out.append(t(40, 164, "Six transfers at 80% recovery leave 0.8^6, about 26% of the sample; "
                          "six washes on a bead lose almost none.", 14, INK))
    out.append(t(40, 188, "Used by CUT&amp;Tag (cells on concanavalin beads, one tube until PCR), "
                          "Drop-seq beads, and on-bead fragmentation in NanoSeq.", 13.5, MUTE))
    return svg(700, 208, "".join(out))


def fig_lowvol():
    out = [t(40, 26, "Rate depends on concentration. One molecule in a smaller volume is a "
                     "higher concentration.", 14, INK)]
    out.append(box(70, 56, 150, 100, "", "none", MUTE, r=5))
    out.append(dot(150, 120, 6, HOT))
    out.append(t(145, 176, "25 uL: 1 copy = 66 fM", 13, BAD, anchor="middle"))
    out.append(box(330, 106, 50, 50, "", "none", MUTE, r=5))
    out.append(dot(355, 134, 6, HOT))
    out.append(t(355, 176, "1 uL: 1 copy = 1.7 pM", 13, OK, anchor="middle"))
    out.append(t(440, 90, "25 times the concentration,", 13, INK))
    out.append(t(440, 108, "so a first-order enzymatic step", 13, INK))
    out.append(t(440, 126, "runs about 25 times faster.", 13, INK))
    out.append(t(40, 214, "Enzyme Km values for nucleic acid are far above these figures, so "
                          "rare molecules are rarely converted.", 13.5, MUTE))
    return svg(700, 234, "".join(out))


# =============================================================== D7 compartments

def fig_poisson():
    out = [t(40, 26, "Droplets: dilute the cells so that a droplet rarely has two. The "
                     "price is that most are empty.", 14, INK)]
    lam = 0.1
    ps = [math.exp(-lam) * lam ** k / math.factorial(k) for k in range(3)]
    labs = ["0 cells", "1 cell", "2 cells"]
    for i, (p, lab) in enumerate(zip(ps, labs)):
        h = max(2, p * 120)
        x = 70 + i * 100
        out.append(f'<rect x="{x}" y="{190 - h}" width="60" height="{h}" fill="{[MUTE, OK, BAD][i]}" '
                   f'opacity="0.35"/>')
        out.append(t(x + 30, 208, lab, 12.5, INK, anchor="middle"))
        out.append(t(x + 30, 184 - h, f"{p*100:.1f}%", 12.5, INK, anchor="middle"))
    occupied = 1 - ps[0]
    doublets = 1 - ps[0] - ps[1]
    out.append(t(400, 80, "average 0.1 cells per droplet (Poisson)", 13, INK))
    out.append(t(400, 106, f"occupied droplets:  {occupied*100:.2f}%", 12.5, MUTE))
    out.append(t(400, 124, f"two or more cells:  {doublets*100:.2f}%", 12.5, MUTE))
    out.append(t(400, 150, f"doublets among occupied:  {doublets/occupied*100:.1f}%", 13, BAD))
    out.append(t(40, 238, "Raise the loading and doublets climb faster than yield. Drop-seq, "
                          "inDrop and 10x all trade this off.", 13.5, MUTE))
    return svg(700, 256, "".join(out))


def fig_splitpool():
    out = [t(40, 26, "Split-and-pool: each round puts the cells into wells, adds a barcode "
                       "and pools them again.", 14, INK)]
    for i in range(3):
        x = 60 + i * 200
        out.append(box(x, 56, 120, 50, "", PB, TOP, r=4))
        out.append(t(x + 60, 76, f"round {i+1}", 13, TOP, anchor="middle"))
        out.append(t(x + 60, 94, "96 wells", 12, MUTE, anchor="middle"))
        if i < 2:
            out.append(arrow(x + 126, 81, x + 194, MUTE))
            out.append(t(x + 160, 72, "pool", 11.5, MUTE, anchor="middle"))
    out.append(t(60, 140, "96 x 96 x 96 = 884,736 combinations, and no cell ever needs its "
                          "own tube.", 14, INK))
    p = 1 - math.exp(-(10000 - 1) / 96 ** 3)
    out.append(t(60, 166, f"10,000 cells: about {p*100:.1f}% share their barcode with another "
                          "cell (a 'collision').", 13.5, BAD))
    out.append(t(60, 196, "SPLiT-seq and sci-RNA-seq3 do this on fixed cells or nuclei, so "
                          "the cells survive the pooling.", 13.5, MUTE))
    return svg(700, 216, "".join(out))


def fig_invessel():
    out = [t(40, 26, "Fix and permeabilise: the nucleus is the reaction vessel. Crosslinks "
                     "keep the molecules where they were.", 14, INK)]
    out.append(t(40, 58, "in dilute solution (original Hi-C)", 13, MUTE))
    for i in range(4):
        out.append(path(f"M {70+i*34} 96 q 12 -26 24 0", TOP, 2.4))
    out.append(t(70, 120, "ligation of crosslinked fragments in free solution: "
                          "random joins are possible", 12.5, MUTE))
    out.append(t(40, 158, "in situ (in situ Hi-C)", 13, OK))
    out.append(path("M 100 200 C 100 170 220 170 220 200 C 220 232 100 232 100 200 Z", TOP, 2.4,
                    PB))
    for i in range(3):
        out.append(dot(130 + i * 28, 202, 4.5, HOT))
    out.append(t(240, 196, "digest and ligate inside the nucleus:", 12.5, MUTE))
    out.append(t(240, 212, "pieces stay near their neighbours", 12.5, MUTE))
    out.append(t(40, 258, "Same principle in SPLiT-seq (in-cell RT) and 10x Flex (probes "
                          "hybridised in fixed cells).", 13.5, INK))
    return svg(700, 278, "".join(out))


def fig_twostage():
    out = [t(40, 26, "Two-stage encapsulation: pre-index in wells, then overload the droplets, "
                     "because the pre-index tells the cells apart.", 14, INK)]
    out.append(mbox(50, 56, 120, 52, ["nuclei in wells,", "round-1 barcode"], PB, TOP, 12, TOP))
    out.append(arrow(176, 82, 226, MUTE))
    out.append(t(201, 72, "pool", 12, MUTE, anchor="middle"))
    out.append(box(232, 50, 120, 64, "", "none", MUTE, r=30))
    for i, c in enumerate([HOT, TOP, OK, BAD, VIO]):
        out.append(dot(260 + i * 18, 70 + (i % 2) * 22, 6, c))
    out.append(t(292, 134, "droplet: many nuclei,", 12.5, MUTE, anchor="middle"))
    out.append(t(292, 150, "each from another well", 12.5, MUTE, anchor="middle"))
    out.append(t(400, 76, "droplet barcode + round-1 barcode", 13, INK))
    out.append(t(400, 96, "= unique for each nucleus", 13, INK))
    out.append(t(40, 196, "Normal droplets are kept at about 0.1 cells to avoid doublets. Here "
                          "a collision needs the same droplet and the same well.", 13.5, INK))
    out.append(t(40, 218, "scifi-RNA-seq reports this as a way to load many more cells per "
                          "run (bioRxiv preprint).", 13.5, MUTE))
    return svg(700, 238, "".join(out))


# =============================================================== D8 property -> base

def fig_bisulfite():
    out = [t(40, 26, "Chemical conversion: bisulfite turns unmethylated C into U (read as T). "
                     "5mC is protected and still reads as C.", 14, INK)]
    s0, s1 = "TCGACCGTA", "TCGATTGTA"
    x = 190
    out.append(t(40, 66, "original", 13, MUTE))
    out.append(t(40, 106, "after bisulfite", 13, MUTE))
    for i, ch in enumerate(s0):
        c = HOT if ch == "C" else INK
        out.append(t(x + i * 22, 66, ch, 18, c, family=MONO))
    out.append(t(x + 22, 46, "m", 13, HOT, anchor="middle"))
    for i, ch in enumerate(s1):
        c = INK
        if s0[i] == "C" and ch == "T":
            c = BAD
        elif ch == "C":
            c = OK
        out.append(t(x + i * 22, 106, ch, 18, c, family=MONO))
    out.append(t(x + 240, 66, "m = 5-methylcytosine", 12.5, HOT))
    out.append(t(x + 240, 106, "red: C read as T (unmethylated)", 12.5, BAD))
    out.append(t(x + 240, 126, "green: C kept (methylated)", 12.5, OK))
    out.append(t(40, 168, "The read now says which C was methylated, at base resolution. "
                          "The cost: three-letter reads (C is scarce), and DNA damage.", 14, INK))
    out.append(t(40, 190, "Enzymatic methyl-seq (EM-seq) gives the same readout without "
                          "chemical damage: TET2 protects, APOBEC deaminates.", 13.5, MUTE))
    return svg(700, 210, "".join(out))


def fig_protect_convert():
    out = [t(40, 26, "Protect, then convert: pick the chemistry whose protection step isolates "
                     "the base you want.", 14, INK)]
    cols = ["unmodified C", "5mC", "5hmC"]
    rows = [("BS-seq", ["T", "C", "C"]), ("oxBS-seq", ["T", "C", "T"]),
            ("TAB-seq", ["T", "T", "C"]), ("EM-seq", ["T", "C", "C"])]
    x0, y0 = 150, 52
    for j, c in enumerate(cols):
        out.append(t(x0 + j * 120 + 50, y0, c, 12.5, MUTE, anchor="middle"))
    for i, (lab, vals) in enumerate(rows):
        y = y0 + 12 + i * 30
        out.append(t(40, y + 20, lab, 13, INK))
        for j, v in enumerate(vals):
            fill = PG if v == "C" else PR
            out.append(box(x0 + j * 120, y, 100, 24, v, fill, OK if v == "C" else BAD, 14,
                           OK if v == "C" else BAD, r=3))
    out.append(t(40, 204, "Table shows what each cytosine reads as. Subtract BS from oxBS "
                          "to get 5hmC; TAB-seq reads 5hmC directly.", 13.5, INK))
    out.append(t(40, 226, "oxBS oxidises 5hmC away; TAB protects 5hmC and oxidises 5mC away.",
                 13.5, MUTE))
    return svg(700, 244, "".join(out))


def fig_position():
    out = [t(40, 26, "Position as information: where a read starts, stops or joins is itself "
                     "the measurement.", 14, INK)]
    panels = [("RT stop (iCLIP)", "cDNA ends one base\nbefore a crosslinked\nprotein"),
              ("Tn5 cut (ATAC-seq)", "reads start where Tn5\ncut open chromatin"),
              ("junction (Hi-C)", "a read pair spanning a\njoin links two loci"),
              ("integration (GUIDE-seq)", "a tag inserted at a\nCas9 break marks it")]
    for i, (h, b) in enumerate(panels):
        x = 40 + i * 168
        out.append(box(x, 50, 152, 112, "", "#fbfbf9", MUTE))
        out.append(t(x + 76, 72, h, 12.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 76, 128 + j * 15, ln, 11.5, INK, anchor="middle"))
        cx = x + 76
        if i == 0:
            out.append(line(cx - 50, 100, cx + 10, 100, TOP, 3))
            out.append(dot(cx + 22, 100, 7, BAD))
        elif i == 1:
            out.append(line(cx - 50, 100, cx + 50, 100, MUTE, 2))
            out.append(vtick(cx - 20, 90, 110, HOT))
            out.append(vtick(cx + 20, 90, 110, HOT))
        elif i == 2:
            out.append(path(f"M {cx-40} 104 C {cx-30} 80 {cx+30} 80 {cx+40} 104", TOP, 2.4))
            out.append(dot(cx - 40, 104, 4, HOT))
            out.append(dot(cx + 40, 104, 4, HOT))
        else:
            out.append(line(cx - 50, 100, cx + 50, 100, MUTE, 2.4))
            out.append(box(cx - 12, 92, 24, 16, "tag", PO, HOT, 10, HOT, r=2))
    out.append(t(40, 196, "No base is chemically changed: the signal is a coordinate, so the "
                          "design question is how to make the end sharp.", 14, INK))
    return svg(720, 216, "".join(out))


def fig_affinity():
    out = [t(40, 26, "Affinity: pull down the molecules that carry the modification. "
                     "Resolution is the fragment length, not the base.", 14, INK)]
    out.append(t(40, 58, "fragmented RNA, about 100 nt", 13, MUTE))
    for i in range(6):
        y = 70 + i * 12
        out.append(line(60 + (i % 3) * 20, y, 160 + (i % 3) * 20, y, MUTE, 2))
        if i in (1, 4):
            out.append(dot(110 + (i % 3) * 20, y, 4, HOT))
    out.append(arrow(240, 100, 290, MUTE))
    out.append(t(265, 90, "antibody + beads", 12, MUTE, anchor="middle"))
    out.append(line(310, 100, 410, 100, MUTE, 2))
    out.append(dot(360, 100, 4, HOT))
    out.append(line(310, 124, 410, 124, MUTE, 2))
    out.append(dot(360, 124, 4, HOT))
    out.append(t(310, 148, "only modified fragments kept", 12.5, MUTE))
    out.append(t(460, 76, "read pile-ups = peaks,", 13, INK))
    out.append(t(460, 94, "compared with input", 13, INK))
    out.append(t(40, 196, "m6A-seq uses an antibody; hmC-Seal labels 5hmC by glucosylation "
                          "and biotin click, then pulls down.", 13.5, INK))
    out.append(t(40, 218, "Cheap and works at low input, but the modified base is only "
                          "known to lie within the fragment.", 13.5, MUTE))
    return svg(700, 238, "".join(out))


def fig_native():
    out = [t(40, 26, "Native readout: no conversion. A modified base changes the signal "
                     "the instrument records.", 14, INK)]
    levels = [60, 60, 82, 82, 82, 56, 56, 90, 90]
    pts = []
    x = 80
    for lv in levels:
        pts.append(f"{x},{lv + 60}")
        x += 26
        pts.append(f"{x},{lv + 60}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" stroke-width="2"/>')
    out.append(t(80, 52, "nanopore current while one k-mer passes", 12.5, MUTE))
    mod_x = 80 + 5 * 26 + 5
    out.append(f'<rect x="{mod_x}" y="106" width="26" height="60" fill="{HOT}" opacity="0.18"/>')
    out.append(t(mod_x + 13, 186, "same k-mer,", 12, HOT, anchor="middle"))
    out.append(t(mod_x + 13, 200, "5mC: level shifts", 12, HOT, anchor="middle"))
    out.append(t(40, 232, "Methylation is called without bisulfite and with long reads, so it "
                          "can be phased to a haplotype or a read.", 14, INK))
    out.append(t(40, 254, "PacBio reads modifications from polymerase kinetics instead.", 13.5, MUTE))
    return svg(700, 274, "".join(out))


build(__file__, [
    # lec.qmd, D1-D4
    ("promiscuity", fig_promiscuity),
    ("block-nick", fig_block_nick),
    ("at-overhang", fig_at_overhang),
    ("hairpin", fig_hairpin),
    ("splint", fig_splint),
    ("dilute", fig_dilute),
    ("dimer", fig_dimer),
    ("suppression", fig_suppression),
    ("exo", fig_exo),
    ("rnaseh", fig_rnaseh),
    ("dash", fig_dash),
    ("methylsens", fig_methylsens),
    ("template-switch", fig_template_switch),
    ("tailing", fig_tailing),
    ("ss-ligation", fig_ss_ligation),
    ("captrap", fig_captrap),
    ("circularise", fig_circularise),
    ("truncated", fig_truncated),
    ("inline-vs-index", fig_inline_vs_index),
    ("stagger", fig_stagger),
    # lec-more.qmd, D5-D8
    ("umi-concept", fig_umi_concept),
    ("umi-where", fig_umi_where),
    ("duplex", fig_duplex),
    ("rca", fig_rca),
    ("spikein", fig_spikein),
    ("budget", fig_budget),
    ("preamp-split", fig_preamp_split),
    ("beads", fig_beads),
    ("lowvol", fig_lowvol),
    ("poisson", fig_poisson),
    ("splitpool", fig_splitpool),
    ("invessel", fig_invessel),
    ("twostage", fig_twostage),
    ("bisulfite", fig_bisulfite),
    ("protect-convert", fig_protect_convert),
    ("position", fig_position),
    ("affinity", fig_affinity),
    ("native", fig_native),
])
