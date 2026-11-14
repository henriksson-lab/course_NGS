#!/usr/bin/env python3
"""Figures for the handles unit.  Run: python3 handles/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

# palette for this unit: handle A, handle B, insert, RNA, index
HA, HB = HOT, "#5b4b8a"
FA, FB, FI = "#f3dccf", "#e1dcef", "#eceeef"
RNAC = "#8a5a2b"
IDX, FIDX = "#9a7b14", "#f1e6b8"
GREY = "#6b7075"


def bx(x, y, w, h, label, kind, size=12):
    fill, stroke = {"A": (FA, HA), "B": (FB, HB), "I": (FI, MUTE), "X": (FIDX, IDX),
                    "R": ("#efe0cc", RNAC), "K": ("#d9dde0", GREY)}[kind]
    return box(x, y, w, h, label, fill=fill, stroke=stroke, size=size, r=3)


def run(x, y, h, segs, gap=0):
    """A row of boxes: segs = (width, label, kind). Returns (svg, end_x)."""
    out = []
    for w, lab, k in segs:
        out.append(bx(x, y, w, h, lab, k))
        x += w + gap
    return "".join(out), x


def dup(x, y, top, bot, hot_top=(), hot_bot=(), pair=True):
    """Duplex with chosen bases highlighted. Checks base pairing."""
    check_pairing(top, bot)
    out = []
    for i, c in enumerate(top):
        if c != " ":
            out.append(t(x + i * DX, y, c, 13, HOT if i in hot_top else TOP, family=MONO))
    for i, c in enumerate(bot):
        if c != " ":
            out.append(t(x + i * DX, y + 28, c, 13, HOT if i in hot_bot else BOT, family=MONO))
    if pair:
        out.append(pairs(x, y, y + 28, top, bot))
    return "".join(out), len(top) * DX


def ln(x1, y1, x2, y2, col=INK, w=2.4, dash=None):
    return line(x1, y1, x2, y2, col, w, dash)


def arc(cx, cy, r, a0, a1, col, w=7):
    """Circular arc from angle a0 to a1 (degrees, 0 = right, clockwise on screen)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f}" '
            f'fill="none" stroke="{col}" stroke-width="{w}"/>')


def tick(x, y, ok=True):
    col = OK if ok else BAD
    if ok:
        return ln(x, y, x + 5, y + 6, col, 2.4) + ln(x + 5, y + 6, x + 15, y - 8, col, 2.4)
    return ln(x, y - 7, x + 12, y + 5, col, 2.4) + ln(x, y + 5, x + 12, y - 7, col, 2.4)


# ---------------------------------------------------------------- figures

def fig_problem():
    out = [t(30, 26, "What you have: molecules of unknown sequence and length", 14, INK)]
    for x, w in [(40, 90), (160, 150), (340, 60), (430, 120)]:
        out.append(bx(x, 40, w, 24, "?", "I", 14))
    out.append(t(30, 100, "What an enzyme, a polymerase and a sequencer need: the same known sequence on every molecule",
                 14, INK))
    s, x = run(40, 118, 28, [(46, "P5", "A"), (36, "index", "X"), (56, "read 1", "A"),
                               (170, "unknown insert", "I"),
                               (56, "read 2", "B"), (36, "index", "X"), (46, "P7", "B")], gap=2)
    out.append(s)
    out.append(t(40, 172, "handle", 13, HA))
    out.append(t(x - 54, 172, "handle", 13, HB, anchor="end"))
    out.append(t(30, 204, "Handles let you prime on it, amplify it, read it, count it and know which sample it came from.",
                 14, INK))
    out.append(t(30, 226, "Everything else in a library preparation exists to put them there.", 14, HOT))
    return svg(720, 244, "".join(out))


def fig_five():
    rows = [
        ("1  DNA ligation", "join something on", "T4 DNA ligase, adapters", "dsDNA ends"),
        ("2  RNA ligation", "join something on", "T4 RNA ligases, adapters", "RNA ends"),
        ("3  Primer tails", "copy with something attached", "any polymerase; the primer is the handle", "copies"),
        ("4  Transposition", "insert while cutting", "Tn5 cuts and tags in one step", "dsDNA, anywhere"),
        ("5  Template switching", "copy with something attached", "RT adds the handle at the cDNA end", "5' end of RNA"),
    ]
    out = [t(20, 24, "way", 13, MUTE), t(240, 24, "picture", 13, MUTE), t(480, 24, "what does the work", 13, MUTE)]
    for i, (name, idea, enz, _) in enumerate(rows):
        y = 56 + i * 48
        out.append(t(20, y + 10, name, 15, INK, weight="bold"))
        out.append(t(20, y + 28, idea, 11, HOT))
        x0 = 240
        if i == 0:
            out += [bx(x0, y, 40, 18, "A", "A"), bx(x0 + 42, y, 90, 18, "insert", "I"), bx(x0 + 134, y, 40, 18, "B", "B")]
            out += [ln(x0 + 41, y - 4, x0 + 41, y + 22, HOT, 1.6), ln(x0 + 133, y - 4, x0 + 133, y + 22, HOT, 1.6)]
        elif i == 1:
            out += [bx(x0, y, 40, 18, "5' ad", "A"), bx(x0 + 42, y, 90, 18, "RNA", "R"), bx(x0 + 134, y, 40, 18, "3' ad", "B")]
        elif i == 2:
            out += [bx(x0 + 42, y + 12, 90, 8, "", "I"), bx(x0, y, 38, 9, "", "A"), bx(x0 + 38, y, 24, 9, "", "K"),
                    bx(x0 + 112, y + 22, 24, 9, "", "K"), bx(x0 + 136, y + 22, 38, 9, "", "B")]
        elif i == 3:
            for k, off in enumerate([0, 70, 140]):
                out.append(bx(x0 + off, y, 56, 18, "", "I"))
            out += [bx(x0 + 56, y, 6, 18, "", "A"), bx(x0 + 62, y, 6, 18, "", "B"),
                    bx(x0 + 126, y, 6, 18, "", "A"), bx(x0 + 132, y, 6, 18, "", "B")]
        else:
            out += [bx(x0 + 34, y, 140, 8, "", "R"), bx(x0, y + 14, 34, 8, "", "A"), bx(x0 + 34, y + 14, 140, 8, "", "I")]
        out.append(t(480, y + 16, enz, 14, INK))
    out.append(t(20, 56 + 5 * 48 + 12,
                 "Also: circularisation (join), homopolymer tailing (copy), topoisomerase and recombination (join).",
                 13, MUTE))
    return svg(820, 56 + 5 * 48 + 28, "".join(out))


def fig_ligation_kinds():
    out = []
    # blunt
    x, y = 30, 50
    out.append(t(x, y - 24, "blunt: any end joins any end", 14, INK, weight="bold"))
    s, w = dup(x, y, "ATGCTTAG", "TACGAATC")
    out.append(s)
    s2, w2 = dup(x + w + 40, y, "CCTGAGTC", "GGACTCAG")
    out.append(s2)
    out.append(t(x + w + 8, y + 18, "+", 18, MUTE))
    # TA
    x2 = 480
    out.append(t(x2, y - 24, "TA: a 3' A meets a 3' T", 14, INK, weight="bold"))
    s, w = dup(x2, y, "ATGCTTAGA", "TACGAATC ", hot_top=(8,))
    out.append(s)
    s2, w2 = dup(x2 + w + 40, y, " CCTGAGT", "TGGACTCA", hot_bot=(0,))
    out.append(s2)
    out.append(t(x2 + w + 8, y + 18, "+", 18, MUTE))
    # cohesive
    y2 = 170
    out.append(t(x, y2 - 24, "cohesive: matching 5' overhangs (BamHI, GATC)", 14, INK, weight="bold"))
    s, w = dup(x, y2, "ATGCTG    ", "TACGACCTAG", hot_bot=(6, 7, 8, 9))
    out.append(s)
    s2, w2 = dup(x + w + 40, y2, "GATCCTCA", "    GAGT", hot_top=(0, 1, 2, 3))
    out.append(s2)
    out.append(t(x + w + 8, y2 + 18, "+", 18, MUTE))
    # splinted
    out.append(t(x2, y2 - 24, "splinted: a third oligo holds two ends together", 14, INK, weight="bold"))
    a, wa = dup(x2, y2 - 6, "GATCCA      ", "            ", pair=False)
    top = "GATCCA"
    s = "".join(t(x2 + i * DX, y2, c, 13, TOP, family=MONO) for i, c in enumerate(top))
    s += "".join(t(x2 + (6 + i) * DX + 6, y2, c, 13, HOT, family=MONO) for i, c in enumerate("TTGACG"))
    bot = "CTAGGTAACTGC"
    check_pairing(top + "TTGACG", bot)
    s += "".join(t(x2 + i * DX + (6 if i >= 6 else 0), y2 + 28, c, 13, BAD if False else BOT, family=MONO)
                 for i, c in enumerate(bot))
    out.append(s)
    out.append(line(x2 + 6 * DX + 2, y2 - 14, x2 + 6 * DX + 2, y2 + 4, OK, 2))
    out.append(t(x2, y2 + 66, "the nick is sealed; the splint is not (3' blocked)", 12, MUTE))
    out.append(t(30, 262, "Blunt is unselective. The other three buy selectivity by requiring a match.", 14, HOT))
    return svg(880, 280, "".join(out))


def fig_concat():
    out = []
    cols = [("blunt adapter, blunt insert", 30, False), ("T-tailed adapter, A-tailed insert", 440, True)]
    for name, x0, ta in cols:
        out.append(t(x0, 26, name, 14, INK, weight="bold"))
        rows = [("insert + adapter", "wanted", True, 1),
                ("insert + insert", "chimera", not ta, 2),
                ("adapter + adapter", "dimer", not ta, 3)]
        for i, (lab, res, joins, kind) in enumerate(rows):
            y = 50 + i * 52
            def piece(x, k):
                if k == "ins":
                    s = bx(x, y, 70, 18, "insert", "I")
                    if ta:
                        s += t(x + 74, y + 14, "A", 13, HOT, family=MONO, weight="bold")
                        s += t(x - 14, y + 14, "A", 13, HOT, family=MONO, weight="bold")
                    return s
                s = bx(x, y, 52, 18, "adapter", "A")
                if ta:
                    s += t(x - 14, y + 14, "T", 13, HB, family=MONO, weight="bold")
                    s += t(x + 56, y + 14, "T", 13, HB, family=MONO, weight="bold")
                return s
            a, b = {"insert + adapter": ("ins", "ad"), "insert + insert": ("ins", "ins"),
                    "adapter + adapter": ("ad", "ad")}[lab]
            wa = 70 if a == "ins" else 52
            out.append(piece(x0 + 14, a))
            out.append(piece(x0 + 14 + wa + 28, b))
            ok = (kind == 1) or joins
            out.append(tick(x0 + 14 + wa + 5, y + 14, True) if False else "")
            out.append(t(x0 + 290, y + 14, lab, 13, MUTE))
            if kind == 1:
                out.append(tick(x0 + 220, y + 14, True))
            elif joins:
                out.append(tick(x0 + 220, y + 14, False))
                out.append(t(x0 + 240, y + 31, res + " forms", 12, BAD))
            else:
                out.append(t(x0 + 218, y + 31, "ends do not match: no joining", 12, OK))
    out.append(t(30, 222, "The overhang does not make the joint stronger. It makes the wrong joints impossible.", 14, HOT))
    return svg(860, 240, "".join(out))


def fig_yadapter():
    out = [t(30, 26, "two adapters, A and B, mixed", 14, INK, weight="bold")]
    combos = [("A", "A", "25%", False), ("A", "B", "50%", True), ("B", "B", "25%", False)]
    for i, (l, r, p, ok) in enumerate(combos):
        y = 48 + i * 40
        out.append(bx(30, y, 36, 20, l, l))
        out.append(bx(68, y, 100, 20, "insert", "I"))
        out.append(bx(170, y, 36, 20, r, r))
        out.append(t(222, y + 15, p + (" has both ends" if ok else " same at both ends"), 13, OK if ok else BAD))
    out.append(t(30, 186, "half of the molecules are wasted", 13, BAD))
    x0 = 520
    out.append(t(x0, 26, "one forked (Y) adapter", 14, INK, weight="bold"))
    # insert
    out.append(bx(x0 + 60, 70, 120, 18, "insert", "I"))
    # left fork
    for xs, d, base in [(x0 + 58, -1, x0 + 58), (x0 + 182, 1, x0 + 182)]:
        out.append(bx(xs - (24 if d < 0 else -2), 64, 24, 30, "", "K"))
        out.append(ln(xs - (24 if d < 0 else -26), 70, xs - (60 if d < 0 else -62), 52, HA, 2.6))
        out.append(ln(xs - (24 if d < 0 else -26), 88, xs - (60 if d < 0 else -62), 106, HB, 2.6))
    out.append(t(x0 - 10, 46, "arm A", 12, HA))
    out.append(t(x0 - 10, 124, "arm B", 12, HB))
    out.append(t(x0 + 250, 46, "arm A", 12, HA))
    out.append(t(x0 + 250, 124, "arm B", 12, HB))
    out.append(t(x0, 170, "same adapter at both ends; after the first copy,", 13, MUTE))
    out.append(t(x0, 188, "one strand ends in A and the other in B", 13, OK))
    out.append(t(30, 222, "Y adapters make asymmetry from a single oligo pair: no wasted combinations.", 14, HOT))
    return svg(900, 240, "".join(out))


def fig_splint():
    out = [t(30, 26, "Splinted ligation: ligase seals a nick, so give it a nick to seal", 14, INK)]
    # molecule 1 and 2 as bars on top strand; splint beneath
    out.append(bx(40, 50, 170, 18, "target, 3'-OH", "I"))
    out.append(bx(214, 50, 150, 18, "adapter, 5'-P", "A"))
    out.append(bx(150, 76, 130, 14, "", "K"))
    out.append(bx(150, 76, 130, 14, "splint (3' blocked)", "K", 11))
    out.append(ln(212, 44, 212, 74, OK, 2.4))
    out.append(t(212, 40, "nick", 12, OK, anchor="middle"))
    out.append(t(150, 106, "half of the splint pairs with each partner", 12, MUTE))
    out.append(t(30, 150, "Why use it:", 14, INK, weight="bold"))
    out.append(t(30, 172, "- only molecules that pair with the splint are joined: the splint carries the selectivity", 13, INK))
    out.append(t(30, 192, "- split-and-pool barcoding adds one barcode per round, each round bridged by its own splint", 13, INK))
    out.append(t(30, 212, "- a degenerate splint end (N) lets one adapter capture any single-stranded 3' end", 13, INK))
    return svg(720, 232, "".join(out))


def fig_rna3():
    out = [t(30, 26, "3' adapter ligation to RNA", 14, INK, weight="bold")]
    out.append(t(30, 64, "5'-P", 12, MUTE))
    out.append(ln(62, 60, 250, 60, RNAC, 4))
    out.append(t(256, 64, "OH-3'", 12, MUTE))
    out.append(t(310, 64, "5'-App", 12, HOT))
    out.append(ln(354, 60, 470, 60, HB, 4))
    out.append(box(470, 52, 16, 16, "", fill=BAD, stroke=BAD, r=2))
    out.append(t(494, 64, "3' block", 12, BAD))
    out.append(t(62, 92, "RNA", 13, RNAC))
    out.append(t(354, 92, "pre-adenylated DNA adapter", 13, HB))
    out.append(arrow(280, 112, 280, 142 + 0, MUTE) if False else "")
    out.append(t(30, 128, "truncated T4 RNA ligase 2, no ATP in the tube", 13, INK))
    out.append(arrow(30, 140, 130, MUTE))
    out.append(t(30, 176, "5'-P", 12, MUTE))
    out.append(ln(62, 172, 250, 172, RNAC, 4))
    out.append(ln(250, 172, 366, 172, HB, 4))
    out.append(box(366, 164, 16, 16, "", fill=BAD, stroke=BAD, r=2))
    out.append(t(30, 210, "- the adapter carries the energy (App), so the reaction needs no ATP", 13, INK))
    out.append(t(30, 230, "- no ATP: the RNA cannot adenylate and circularise itself", 13, INK))
    out.append(t(30, 250, "- blocked 3' end: adapter cannot ligate to another adapter or to RNA", 13, INK))
    return svg(720, 268, "".join(out))


def fig_rna5():
    out = [t(30, 26, "5' adapter ligation (after the 3' adapter is on)", 14, INK, weight="bold")]
    out.append(ln(40, 60, 140, 60, HA, 4))
    out.append(t(40, 52, "5' adapter (RNA), 3'-OH", 12, HA))
    out.append(t(150, 64, "+", 16, MUTE))
    out.append(t(170, 52, "5'-P", 12, OK))
    out.append(ln(200, 60, 300, 60, RNAC, 4))
    out.append(ln(300, 60, 380, 60, HB, 4))
    out.append(t(280, 80, "RNA + 3' adapter", 12, MUTE))
    out.append(t(30, 118, "T4 RNA ligase 1, ATP", 13, INK))
    out.append(arrow(30, 128, 130, MUTE))
    out.append(ln(40, 162, 140, 162, HA, 4))
    out.append(ln(140, 162, 240, 162, RNAC, 4))
    out.append(ln(240, 162, 320, 162, HB, 4))
    out.append(t(340, 166, "both handles on, ready for RT", 13, OK))
    out.append(t(30, 204, "Failure mode: free 3' adapter left in the tube also has a 5'-P end,", 13, BAD))
    out.append(t(30, 224, "so the 5' adapter joins it: a 5' + 3' adapter dimer that amplifies better than any insert.", 13, BAD))
    return svg(720, 242, "".join(out))


def fig_circ():
    out = [t(30, 26, "Circularisation: one primer supplies both handles", 14, INK, weight="bold")]
    s, x = run(30, 44, 22, [(34, "H1a", "A"), (22, "cut", "X"), (34, "H1b", "A"), (150, "cDNA", "I")], gap=0)
    out.append(s)
    out.append(t(30, 40, "5'-P", 11, MUTE))
    out.append(t(x + 4, 60, "3'-OH", 11, MUTE))
    out.append(t(30, 90, "primer with 5' phosphate; cDNA ends where RT stopped", 12, MUTE))
    cx, cy, r = 150, 190, 46
    out.append(arc(cx, cy, r, 200, 270, HA))
    out.append(arc(cx, cy, r, 275, 300, IDX))
    out.append(arc(cx, cy, r, 305, 340, HA))
    out.append(arc(cx, cy, r, 345, 190, MUTE))
    out.append(t(cx, cy + 5, "circle", 12, INK, anchor="middle"))
    out.append(t(cx + r + 20, cy + 4, "ligase joins the cDNA 3' end to the primer 5' end", 12, MUTE))
    out.append(t(cx + r + 20, cy + 22, "(dilute: the two ends are on the same molecule)", 12, MUTE))
    s, x = run(30, 264, 22, [(34, "H1b", "A"), (150, "cDNA", "I"), (34, "H1a", "A")], gap=0)
    out.append(s)
    out.append(t(x + 12, 280, "cut at the site: handle on each side", 12, OK))
    out.append(t(30, 312, "iCLIP: the cDNA 3' end is where RT stopped at the crosslinked nucleotide.", 13, INK))
    return svg(720, 330, "".join(out))


def fig_primertail():
    out = []
    # row 1
    def row(y, title):
        return t(30, y - 26, title, 13, INK, weight="bold")
    out.append(row(50, "cycle 1: only the 3' part of the primer pairs; the tail hangs free"))
    out.append(ln(60, 70, 520, 70, GREY, 3))
    out.append(ln(160, 96, 230, 96, TOP, 4))
    out.append(ln(110, 96, 160, 96, HA, 4))
    out.append(arrow(230, 96, 400, TOP, w=2))
    out.append(t(60, 118, "5' tail (handle)", 11, HA))
    out.append(t(170, 118, "annealing part", 11, TOP))
    out.append(row(170, "cycle 2: the copy carries the tail, so the complete primer now pairs along its full length"))
    out.append(ln(110, 190, 520, 190, HA, 0.1))
    out.append(ln(110, 190, 160, 190, HA, 3))
    out.append(ln(160, 190, 400, 190, GREY, 3))
    out.append(ln(110, 214, 160, 214, HA, 4))
    out.append(ln(160, 214, 230, 214, TOP, 4))
    out.append(arrow(230, 214, 400, TOP, w=2))
    out.append(row(290, "product: new sequence at the end of every molecule, in whatever order the primers dictate"))
    s, x = run(100, 300, 22, [(60, "handle A", "A"), (28, "gene", "K"), (150, "target", "I"), (28, "gene", "K"), (60, "handle B", "B")])
    out.append(s)
    out.append(t(30, 352, "The tail does not need to match anything. Tm only matters for the annealing part.", 13, HOT))
    return svg(720, 370, "".join(out))


def fig_rtprimer():
    out = [t(30, 26, "The RT primer is the handle", 14, INK, weight="bold")]
    out.append(t(30, 64, "5'", 12, MUTE))
    out.append(ln(46, 60, 420, 60, RNAC, 4))
    out.append(t(260, 54 - 14, "mRNA", 12, RNAC))
    for i in range(8):
        out.append(t(424 + i * 9, 64, "A", 11, RNAC, family=MONO))
    out.append(t(498, 64, "3'", 12, MUTE))
    # primer under poly(A)
    out.append(ln(424, 92, 496, 92, TOP, 4))
    out.append(t(424, 114, "T T T T T T T T", 11, TOP, family=MONO))
    s, x = run(496, 82, 22, [(70, "UMI", "X"), (60, "barcode", "X"), (90, "handle", "A")])
    out.append(s)
    out.append(arrow(424, 92, 240, TOP, w=2.4))
    out.append(ln(240, 92, 424, 92, GREY, 3))
    out.append(t(250, 120, "RT writes cDNA from the primer", 12, MUTE))
    out.append(t(30, 160, "First-strand cDNA starts with handle, barcode and UMI, then T's, then the transcript.", 13, INK))
    out.append(t(30, 182, "CEL-Seq, Drop-seq, 10x 3' and most 3'-end methods use this; no ligation step is needed.", 13, INK))
    out.append(t(30, 204, "A 'VN' at the primer 3' end anchors it to the start of the poly(A), not inside it.", 13, MUTE))
    return svg(790, 222, "".join(out))


def fig_randomprimer():
    out = [t(30, 26, "Tagged random priming: the handle rides on a random primer", 14, INK, weight="bold")]
    out.append(t(30, 64, "5'", 12, MUTE))
    out.append(ln(46, 60, 560, 60, GREY, 3))
    out.append(t(566, 64, "3'", 12, MUTE))
    for px in (110, 330):
        out.append(ln(px, 90, px + 40, 90, TOP, 4))
        out.append(ln(px + 40, 90, px + 84, 90, HA, 4))
        out.append(arrow(px, 90, px - 60 if False else px - 30, TOP, w=2) if False else "")
    out.append(t(110, 112, "N9", 11, TOP))
    out.append(t(150, 112, "tail", 11, HA))
    out.append(t(330, 112, "N9", 11, TOP))
    out.append(t(370, 112, "tail", 11, HA))
    out.append(t(30, 150, "the primer anneals wherever its random end finds a match; extension copies the template", 12, MUTE))
    out.append(t(30, 190, "Second round: a primer with tail B primes on those copies, so every product has A at one end and B at the other.",
                 12, MUTE))
    s, x = run(100, 204, 22, [(70, "tail A", "A"), (24, "N9", "K"), (170, "copied DNA", "I"), (24, "N9", "K"), (70, "tail B", "B")])
    out.append(s)
    out.append(t(30, 258, "Used after bisulfite (PBAT, scBS-seq, snmC-seq2): bisulfite already fragmented the DNA, so adapters go on after.", 13, INK))
    return svg(720, 278, "".join(out))


def fig_tn5():
    out = [t(30, 26, "Tn5 transposome: two adapter oligos loaded on one enzyme dimer", 14, INK, weight="bold")]
    out.append(ln(40, 62, 330, 62, TOP, 3))
    out.append(ln(40, 76, 330, 76, BOT, 3))
    out.append(f'<ellipse cx="185" cy="69" rx="44" ry="22" fill="none" stroke="{HA}" stroke-width="2" stroke-dasharray="4 3"/>')
    out.append(t(185, 106, "transposome binds, cuts both strands 9 nt apart", 12, HA, anchor="middle"))
    out.append(ln(160, 52, 160, 68, HA, 2))
    out.append(ln(214, 70, 214, 86, HA, 2))
    out.append(t(30, 146, "left fragment: 3'-OH recessed, adapter on the 5' end", 13, INK, weight="bold"))
    out.append(ln(40, 170, 160, 170, TOP, 3))
    out.append(ln(40, 184, 214, 184, BOT, 3))
    out.append(bx(214, 176, 80, 16, "adapter A", "A", 11))
    out.append(bx(214 + 0, 160, 80, 14, "", "A") if False else "")
    out.append(bx(214, 160, 80, 14, "", "FA" if False else "A"))
    out.append(t(160, 156, "3'-OH", 11, MUTE, anchor="middle"))
    out.append(t(187, 214, "9-nt gap", 12, BAD, anchor="middle"))
    out.append(ln(163, 205, 211, 205, BAD, 2, dash="3 2"))
    out.append(t(30, 252, "right fragment: the mirror image; the 9 nt in between now appear at both new ends", 13, INK, weight="bold"))
    out.append(ln(360, 270, 480, 270, TOP, 3) if False else "")
    out.append(ln(160, 276, 280, 276, BOT, 3))
    out.append(ln(106, 262, 280, 262, TOP, 3))
    out.append(bx(26, 268, 80, 16, "adapter A", "A", 11))
    out.append(bx(26, 252 + 12, 80, 0.1, "", "A") if False else "")
    out.append(t(30, 306, "no ligase involved: the transposase itself joins the adapter to the target's 5' end", 13, INK))
    out.append(t(30, 328, "Before PCR a polymerase at 72 C must fill the gap, which also displaces the non-transferred strand.", 13, HOT))
    return svg(720, 346, "".join(out))


def fig_tagment():
    out = [t(30, 26, "One long molecule, many cuts: each fragment gets its two ends independently", 14, INK, weight="bold")]
    out.append(bx(40, 44, 600, 14, "", "I"))
    for x in (160, 270, 380, 520):
        out.append(ln(x, 38, x, 64, HOT, 2))
    frags = [(40, 160, "A", "B"), (160, 270, "A", "A"), (270, 380, "B", "B"), (380, 520, "B", "A"), (520, 640, "A", "B")]
    y = 94
    for (a, b, l, r) in frags:
        w = b - a
        out.append(bx(a + 2, y, 12, 20, l, l, 11))
        out.append(bx(a + 16, y + 3, w - 34, 14, "", "I"))
        out.append(bx(b - 14, y, 12, 20, r, r, 11))
        ok = l != r
        out.append(tick(a + w / 2 - 6, y + 52, ok))
        out.append(t(a + w / 2 + 14, y + 53, "amplifies" if ok else "does not", 11, OK if ok else BAD))
    out.append(t(30, 196, "With A and B loaded in equal amounts, half the fragments carry A and B: about 50%.", 13, INK))
    out.append(t(30, 216, "More enzyme per DNA means more cuts and shorter fragments; the insert size is set by the ratio.", 13, INK))
    return svg(700, 236, "".join(out))


def fig_ts():
    out = [t(30, 26, "Template switching: the RT adds the handle by itself", 14, INK, weight="bold")]
    x0, x1 = 60, 440
    # row 1
    out.append(t(30, 56, "1", 14, HOT, weight="bold"))
    out.append(ln(x0, 52, x1, 52, RNAC, 4))
    out.append(arrow(x1, 66, x0, TOP, w=2.4))
    out.append(t(x1 + 12, 70, "oligo-dT primes, RT copies to the 5' end of the RNA", 12, MUTE))
    out.append(t(30, 112, "2", 14, HOT, weight="bold"))
    out.append(ln(x0, 108, x1, 108, RNAC, 4))
    out.append(ln(x0, 122, x1, 122, GREY, 3))
    out.append(t(x0 - 28, 126, "CCC", 12, HOT, family=MONO, weight="bold"))
    out.append(t(x1 + 12, 126, "at the end, RT adds 2-4 non-templated C", 12, MUTE))
    out.append(t(30, 184, "3", 14, HOT, weight="bold"))
    out.append(ln(x0, 180, x1, 180, RNAC, 4))
    out.append(ln(x0, 194, x1, 194, GREY, 3))
    out.append(bx(x0 - 90, 160, 70, 18, "handle", "A", 11))
    out.append(t(x0 - 18, 174, "rGrGrG", 11, HOT, family=MONO, anchor="start") if False else "")
    out.append(bx(x0 - 20, 160, 36, 18, "GGG", "K", 11))
    out.append(t(x1 + 12, 198, "the TSO (GGG at its 3' end) pairs with the C's", 12, MUTE))
    out.append(t(30, 256, "4", 14, HOT, weight="bold"))
    out.append(ln(x0, 252, x1, 252, RNAC, 4))
    out.append(ln(x0 - 90, 266, x1, 266, GREY, 3))
    out.append(bx(x0 - 90, 262, 70, 8, "", "A", 11))
    out.append(t(x1 + 12, 270, "RT switches template and copies the handle: it is on the cDNA now", 12, OK))
    out.append(t(30, 296, "No ligase, no extra step: the handle is added in the same tube as RT.", 13, INK))
    return svg(820, 314, "".join(out))


def fig_tailing():
    out = [t(30, 26, "Homopolymer tailing: make a known sequence, then use it", 14, INK, weight="bold")]
    out.append(t(30, 62, "DNA", 13, TOP, weight="bold"))
    out.append(ln(80, 58, 260, 58, TOP, 4))
    out.append(t(262, 62, "AAAAAAAA", 12, HOT, family=MONO))
    out.append(t(380, 62, "TdT + dATP adds a tail to every 3'-OH", 12, MUTE))
    out.append(t(30, 100, "RNA", 13, RNAC, weight="bold"))
    out.append(ln(80, 96, 260, 96, RNAC, 4))
    out.append(t(262, 100, "AAAAAAAA", 12, HOT, family=MONO))
    out.append(t(380, 100, "poly(A) polymerase + ATP does the same on RNA", 12, MUTE))
    out.append(t(30, 150, "then", 13, INK, weight="bold"))
    out.append(t(262, 154, "TTTTTTTT", 12, TOP, family=MONO))
    s, x = run(100, 140, 20, [(60, "handle", "A")])
    out.append(bx(150, 140, 110, 20, "handle", "A"))
    out.append(arrow(262, 168, 100, TOP, w=2) if False else "")
    out.append(t(380, 154, "oligo-dT primer with the handle on its 5' end", 12, MUTE))
    out.append(t(30, 204, "- length of the tail is random, a few dozen to hundreds of nt: sets a limit to read-through", 13, INK))
    out.append(t(30, 224, "- the handle sits on the primer, so the tail only has to be pairable", 13, INK))
    out.append(t(30, 244, "- the tail must not be at the end where you need the insert read: plan the read direction", 13, INK))
    return svg(720, 262, "".join(out))


def fig_topo():
    out = [t(30, 26, "Topoisomerase TA cloning", 14, INK, weight="bold")]
    out.append(ln(40, 62, 200, 62, TOP, 3))
    out.append(ln(40, 76, 200, 76, BOT, 3))
    out.append(f'<circle cx="212" cy="62" r="11" fill="{HA}"/>')
    out.append(t(230, 66, "Topo I on 3'-P of vector", 11, HA))
    out.append(t(212, 66, "T", 10, "#fff", anchor="middle", family=MONO) if False else "")
    out.append(t(40, 102, "vector: 3' T overhang, enzyme bound to the 3' phosphate", 12, MUTE))
    out.append(ln(40, 140, 200, 140, GREY, 3))
    out.append(ln(40, 154, 200, 154, GREY, 3))
    out.append(t(206, 144, "A", 13, HOT, family=MONO, weight="bold"))
    out.append(t(40, 180, "insert (PCR product): 3' A overhang and 5'-OH", 12, MUTE))
    out.append(t(30, 218, "5'-OH attacks the enzyme-DNA bond: strand ligated, enzyme released, no ligase or ATP", 12, OK))
    x0 = 460
    out.append(t(x0, 26, "Site-specific recombination (Gateway-type)", 14, INK, weight="bold"))
    out.append(bx(x0, 54, 30, 20, "attB", "A", 11))
    out.append(bx(x0 + 32, 54, 110, 20, "insert", "I"))
    out.append(bx(x0 + 144, 54, 30, 20, "attB", "A", 11))
    out.append(t(x0, 100, "att sites come on the PCR primers (a primer tail)", 12, MUTE))
    out.append(bx(x0, 130, 30, 20, "attP", "B", 11))
    out.append(bx(x0 + 32, 130, 110, 20, "vector", "K"))
    out.append(bx(x0 + 144, 130, 30, 20, "attP", "B", 11))
    out.append(t(x0, 176, "integrase + IHF swap the segments between matching sites", 12, MUTE))
    out.append(t(x0, 218, "mostly a cloning tool; NGS uses it to build libraries", 12, INK))
    return svg(900, 240, "".join(out))


def fig_indexpcr():
    out = [t(30, 26, "Truncated adapters: ligate the part every library shares, add the rest by PCR", 14, INK, weight="bold")]
    s, x = run(100, 46, 22, [(60, "read 1 site", "A"), (170, "insert", "I"), (60, "read 2 site", "B")])
    out.append(s)
    out.append(t(30, 62, "ligated", 12, MUTE))
    out.append(t(100, 90, "the stub is short and identical for every sample", 12, MUTE))
    s, x = run(60, 124, 20, [(46, "P5", "A"), (40, "i5", "X"), (60, "read 1 site", "A")])
    out.append(s)
    out.append(arrow(60 + 146 + 4, 134, 60 + 146 + 54, TOP, w=2) if False else "")
    s, x = run(300, 160, 20, [(60, "read 2 site", "B"), (40, "i7", "X"), (46, "P7", "B")])
    out.append(s)
    out.append(t(30, 140, "PCR", 12, MUTE))
    out.append(t(60, 118, "index primer: 3' end pairs with the stub, 5' tail adds the rest", 12, MUTE))
    out.append(t(30, 212, "result:", 13, INK, weight="bold"))
    s, x = run(100, 198, 22, [(46, "P5", "A"), (40, "i5", "X"), (60, "read 1", "A"), (150, "insert", "I"),
                               (60, "read 2", "B"), (40, "i7", "X"), (46, "P7", "B")], gap=1)
    out.append(s)
    out.append(t(30, 250, "One adapter stock serves every sample. Index choice is a PCR decision, not a ligation one.", 13, HOT))
    return svg(720, 268, "".join(out))


def fig_twostep():
    out = [t(30, 26, "Two-step PCR: do the specific work first, then add the long tails", 14, INK, weight="bold")]
    out.append(box(30, 48, 190, 90, "", fill="none", stroke=MUTE))
    out.append(t(125, 68, "step 1: few cycles", 13, INK, anchor="middle", weight="bold"))
    s, x = run(46, 82, 16, [(30, "U1", "A"), (28, "gene", "K"), (58, "target", "I"), (28, "gene", "K"), (30, "U2", "B")])
    out.append(s)
    out.append(t(125, 124, "short primers with universal tails", 11, MUTE, anchor="middle"))
    out.append(t(244, 96, "clean up", 12, MUTE))
    out.append(arrow(240, 100, 290, MUTE) if False else "")
    out.append(ln(240, 104, 290, 104, MUTE, 1.5))
    out.append(box(300, 48, 270, 90, "", fill="none", stroke=MUTE))
    out.append(t(435, 68, "step 2: indexing primers", 13, INK, anchor="middle", weight="bold"))
    s, x = run(310, 82, 16, [(30, "P5", "A"), (30, "i5", "X"), (30, "U1", "A"), (30, "gene", "K"), (30, "ins", "I"), (30, "gene", "K"), (30, "U2", "B"), (30, "i7", "X")], gap=0)
    out.append(s)
    out.append(t(435, 124, "universal primers only: nothing target-specific can mispair", 11, MUTE, anchor="middle"))
    out.append(t(30, 172, "- long chimeric primers (tail + gene) are the main source of primer dimers; step 1 keeps them out", 13, INK))
    out.append(t(30, 192, "- clean-up between steps removes step-1 primers, so step 2 cannot re-prime on them", 13, INK))
    out.append(t(30, 212, "- indexes are added once, in the second step: fewer expensive primers and less index swapping", 13, INK))
    return svg(720, 230, "".join(out))


def fig_nested():
    out = [t(30, 26, "Nested handles: each round primes on the previous round's handle", 14, INK, weight="bold")]
    rows = [("round 1", [(34, "H1", "A"), (150, "target", "I"), (34, "H1'", "B")]),
            ("round 2", [(34, "H2", "X"), (34, "H1", "A"), (150, "target", "I"), (34, "H1'", "B"), (34, "H2'", "X")]),
            ("round 3", [(34, "H3", "K"), (34, "H2", "X"), (34, "H1", "A"), (150, "target", "I"),
                         (34, "H1'", "B"), (34, "H2'", "X"), (34, "H3'", "K")])]
    for i, (name, segs) in enumerate(rows):
        y = 50 + i * 48
        out.append(t(30, y + 15, name, 13, INK))
        s, x = run(110, y, 22, segs, gap=1)
        out.append(s)
    out.append(t(30, 210, "A product that lacks H1 cannot be primed in round 2, so background from round 1 stops here.", 13, INK))
    out.append(t(30, 230, "Used for rare targets (5' RACE, TCR/BCR libraries) and to extend a short handle in steps.", 13, INK))
    return svg(720, 248, "".join(out))


def fig_bead():
    out = [t(30, 26, "Bead-bound handles: the handle is already on a solid support", 14, INK, weight="bold")]
    out.append(f'<circle cx="90" cy="120" r="34" fill="{FI}" stroke="{MUTE}" stroke-width="1.5"/>')
    out.append(t(90, 124, "bead", 12, INK, anchor="middle"))
    for ang in (-40, 0, 40):
        a = math.radians(ang)
        x1, y1 = 90 + 34 * math.cos(a), 120 + 34 * math.sin(a)
        out.append(ln(x1, y1, x1 + 40, y1, GREY, 2))
    s, x = run(150, 71, 18, [(52, "handle", "A"), (62, "barcode", "X"), (38, "UMI", "K"), (36, "T...T", "B")], gap=0)
    out.append(s)
    out.append(t(150, 62, "same barcode on every oligo of one bead", 12, MUTE))
    out.append(t(150, 114, "...", 14, MUTE))
    s, x = run(150, 136, 18, [(52, "handle", "A"), (62, "barcode", "X"), (38, "UMI", "K"), (36, "T...T", "B")], gap=0)
    out.append(s)
    out.append(t(150, 168, "a different UMI on every oligo", 12, MUTE))
    out.append(t(30, 210, "- the polyA of a lysed cell's mRNA hybridises to the bead's T-run; RT extends it", 13, INK))
    out.append(t(30, 230, "- barcode is chemically attached at synthesis: no ligation, no mixing between beads", 13, INK))
    out.append(t(30, 250, "- streptavidin beads can also hold a biotinylated adapter during library steps", 13, INK))
    return svg(720, 268, "".join(out))


def fig_decide():
    rows = [("intact dsDNA, ng to ug", "end repair + A-tail + adapter ligation", "ligation"),
            ("dsDNA, tens of ng or less, speed", "tagmentation", "transposition"),
            ("a known region", "tailed primers, then index PCR", "primer tails"),
            ("full-length mRNA, low input", "RT with template switching", "template switching"),
            ("small RNA", "3' App adapter + 5' RNA adapter", "RNA ligation"),
            ("degraded or single-stranded DNA", "single-strand ligation or tailing", "tailing / ssDNA ligation")]
    out = [t(20, 24, "starting material", 13, MUTE), t(300, 24, "what you do", 13, MUTE), t(600, 24, "family", 13, MUTE)]
    for i, (a, b, c) in enumerate(rows):
        y = 44 + i * 36
        out.append(box(16, y - 4, 800, 30, "", fill="none", stroke="#d5d8da", r=3))
        out.append(t(26, y + 16, a, 14, INK))
        out.append(t(300, y + 16, b, 14, INK))
        out.append(t(600, y + 16, c, 14, HOT, weight="bold"))
    return svg(830, 44 + 6 * 36 + 20, "".join(out))


def fig_tn5():
    out = [t(30, 26, "Tn5: one enzyme dimer cuts the target and attaches adapter A to both new 5' ends", 14, INK, weight="bold")]
    out.append(ln(40, 62, 380, 62, TOP, 3))
    out.append(ln(40, 76, 380, 76, BOT, 3))
    out.append(f'<ellipse cx="210" cy="69" rx="52" ry="24" fill="none" stroke="{HA}" stroke-width="2" stroke-dasharray="4 3"/>')
    out.append(ln(190, 52, 190, 69, HA, 2.4))
    out.append(ln(230, 69, 230, 86, HA, 2.4))
    out.append(t(400, 66, "top strand cut here, bottom strand cut 9 nt away", 12, HA))
    # product: left fragment end
    out.append(t(30, 124, "left fragment, right-hand end", 13, INK, weight="bold"))
    out.append(ln(40, 148, 200, 148, TOP, 3))
    out.append(ln(40, 162, 236, 162, BOT, 3))
    out.append(bx(236, 154, 90, 16, "adapter A", "A", 11))
    out.append(bx(236, 138, 90, 12, "", "A"))
    out.append(t(200, 138, "3'-OH", 11, MUTE, anchor="middle"))
    out.append(t(236, 140, "5'-P", 11, MUTE, anchor="end"))
    out.append(ln(202, 148, 234, 148, BAD, 2, dash="3 2"))
    out.append(t(218, 190, "9-nt gap", 12, BAD, anchor="middle"))
    out.append(t(400, 160, "adapter joined to the bottom strand's 5' end", 12, MUTE))
    out.append(t(30, 226, "right fragment, left-hand end: the mirror image, on the other strand", 13, INK, weight="bold"))
    out.append(ln(120, 250, 330, 250, TOP, 3))
    out.append(ln(156, 264, 330, 264, BOT, 3))
    out.append(bx(30, 242, 90, 16, "adapter A", "A", 11))
    out.append(bx(30, 266, 90, 12, "", "A"))
    out.append(t(30, 292, "The 9 nt between the cuts end up at both new ends: the target duplication.", 12, MUTE))
    out.append(t(30, 320, "No ligase: the transposase joins the adapter. A polymerase at 72 C must fill the gap before PCR.", 13, HOT))
    return svg(720, 338, "".join(out))


def fig_ts():
    out = [t(30, 26, "Template switching: the RT adds the handle by itself", 14, INK, weight="bold")]
    x0, x1 = 170, 540
    labs = {1: 52, 2: 112, 3: 184, 4: 256}
    for n, y in labs.items():
        out.append(t(30, y + 4, str(n), 14, HOT, weight="bold"))
    out.append(t(50, 40, "RNA 5'", 11, MUTE)); out.append(t(x1 - 10, 40, "3' AAAA", 11, MUTE))
    out.append(ln(x0, 52, x1, 52, RNAC, 4))
    out.append(arrow(x1 - 4, 66, x0, TOP, w=2.4))
    out.append(t(x1 + 20, 70, "oligo-dT primes; RT copies to the RNA 5' end", 12, MUTE))
    out.append(ln(x0, 112, x1, 112, RNAC, 4))
    out.append(ln(x0 - 28, 126, x1 - 4, 126, GREY, 3))
    out.append(t(x0 - 48, 130, "CCC", 12, HOT, family=MONO, weight="bold"))
    out.append(t(x1 + 20, 130, "RT adds a few non-templated C", 12, MUTE))
    out.append(ln(x0, 184, x1, 184, RNAC, 4))
    out.append(ln(x0 - 28, 198, x1 - 4, 198, GREY, 3))
    out.append(bx(x0 - 130, 176, 100, 18, "handle", "A", 11))
    out.append(bx(x0 - 30, 176, 30, 18, "GGG", "K", 11))
    out.append(t(x1 + 20, 198, "TSO pairs through its GGG", 12, MUTE))
    out.append(ln(x0, 256, x1, 256, RNAC, 4))
    out.append(ln(x0 - 130, 270, x1 - 4, 270, GREY, 3))
    out.append(bx(x0 - 130, 266, 100, 8, "", "A"))
    out.append(t(x1 + 20, 274, "RT switches template, copies the handle", 12, OK))
    out.append(t(30, 306, "No ligase, no extra step: the handle is added in the same tube as RT.", 13, INK))
    return svg(820, 324, "".join(out))


build(__file__, [
    ("problem", fig_problem),
    ("five-ways", fig_five),
    ("ligation-kinds", fig_ligation_kinds),
    ("concatemers", fig_concat),
    ("y-adapter", fig_yadapter),
    ("splint", fig_splint),
    ("rna-3prime", fig_rna3),
    ("rna-5prime", fig_rna5),
    ("circularise", fig_circ),
    ("primer-tail", fig_primertail),
    ("rt-primer", fig_rtprimer),
    ("random-primer", fig_randomprimer),
    ("tn5", fig_tn5),
    ("tagment", fig_tagment),
    ("template-switch", fig_ts),
    ("tailing", fig_tailing),
    ("topo-recomb", fig_topo),
    ("index-pcr", fig_indexpcr),
    ("two-step", fig_twostep),
    ("nested", fig_nested),
    ("bead", fig_bead),
    ("decide", fig_decide),
])
