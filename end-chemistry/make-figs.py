#!/usr/bin/env python3
"""Figures for the end-chemistry unit.  Run: python3 end-chemistry/make-figs.py"""
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

PCOL = OK


def endmark(x, y, kind, size=6):
    """5'/3' end state glyph: P = filled green, OH = open red, block = red square."""
    if kind == "P":
        return f'<circle cx="{x}" cy="{y}" r="{size}" fill="{OK}"/>'
    if kind == "OH":
        return f'<circle cx="{x}" cy="{y}" r="{size}" fill="#fff" stroke="{BAD}" stroke-width="2"/>'
    return f'<rect x="{x-size}" y="{y-size}" width="{2*size}" height="{2*size}" fill="{BAD}"/>'


def hairpin(x, y, d, col=HB, h=26):
    """A small stem loop at x, opening toward d (+1 right, -1 left)."""
    r = h / 2
    return (f'<path d="M {x} {y-r} A {r} {r} 0 0 {1 if d > 0 else 0} {x} {y+r}" fill="none" '
            f'stroke="{col}" stroke-width="3"/>')


def table(x, y, cols, rows, widths, rowh=32, size=13, head_col=MUTE, first_bold=True, hot_col=None):
    out = []
    cx = x
    for w, c in zip(widths, cols):
        out.append(t(cx, y, c, 12.5, head_col))
        cx += w
    for i, r in enumerate(rows):
        yy = y + 14 + i * rowh
        out.append(box(x - 8, yy - 4, sum(widths) - 4, rowh - 4, "", fill="none", stroke="#d5d8da", r=3))
        cx = x
        for j, (w, c) in enumerate(zip(widths, r)):
            col = INK
            wt = "bold" if (j == 0 and first_bold) else None
            if isinstance(c, tuple):
                c, col = c
            out.append(t(cx, yy + 16, c, size, col, weight=wt))
            cx += w
    return "".join(out)


def fig_catalogue():
    rows = [
        ("5'-phosphate", ("ligation donor", OK), "kinase product; restriction, DNase I"),
        ("5'-OH", ("cannot ligate", BAD), "MNase, RNase A, alkali; or after CIP"),
        ("5'-triphosphate / cap", ("cannot ligate", BAD), "primary transcripts: pyrophosphatase or decapping"),
        ("3'-OH", ("extendable, ligation acceptor", OK), "most enzymatic cuts; the working end"),
        ("3'-phosphate", ("blocked", BAD), "MNase, damage; PNK or phosphatase removes it"),
        ("2',3'-cyclic phosphate", ("blocked", BAD), "RNase A/T1, metal-ion hydrolysis of RNA"),
        ("3'-ddN, C3, amino, inverted dT", ("blocked, permanently", BAD), "synthesised on purpose"),
    ]
    out = [table(20, 24, ["end", "what the enzymes see", "where it comes from"], rows, [250, 250, 420], rowh=34)]
    out.append(t(20, 14 + 24 + 7 * 34 + 24, "Two atoms decide it: a phosphate on a 5' end is wanted, a phosphate or block on a 3' end is not.", 14, HOT))
    return svg(940, 24 + 14 + 7 * 34 + 44, "".join(out))


def fig_sources():
    rows = [
        ("acoustic shearing", "mixed", "mixed, some damaged", "ragged, all shapes"),
        ("restriction enzyme", ("5'-P", OK), ("3'-OH", OK), "defined overhang or blunt"),
        ("DNase I", ("5'-P", OK), ("3'-OH", OK), "mostly blunt or 1-nt overhang"),
        ("micrococcal nuclease", ("5'-OH", BAD), ("3'-P", BAD), "needs repair of both ends"),
        ("Cas9 in vitro", ("5'-P", OK), ("3'-OH", OK), "mostly blunt"),
        ("Tn5 tagmentation", "adapter attached", ("3'-OH", OK), "9-nt gap on each side"),
        ("RNase A / alkali on RNA", ("5'-OH", BAD), ("2',3'-cyclic P", BAD), "needs PNK before ligation"),
    ]
    out = [table(20, 24, ["how it was cut", "5' end", "3' end", "shape"], rows, [230, 170, 190, 300], rowh=34)]
    out.append(t(20, 14 + 24 + 7 * 34 + 24, "The cutting method decides which repair steps the library preparation needs.", 14, HOT))
    return svg(940, 24 + 14 + 7 * 34 + 44, "".join(out))


def ends53(x, y, top, bot):
    """5'/3' marks around a duplex drawn by dup(): top runs 5'->3' left to right."""
    wt, wb = len(top.rstrip()) * DX, len(bot.rstrip()) * DX
    return (t(x - 9, y, "5'", 11, MUTE, anchor="end") +
            t(x + wt + 2, y, "3'", 11, MUTE) +
            t(x - 9, y + 28, "3'", 11, MUTE, anchor="end") +
            t(x + wb + 2, y + 28, "5'", 11, MUTE))


def fig_shapes():
    out = []
    items = [("5' overhang", "ATGCTTAG    ", "TACGAATCGATC", "ATGCTTAGCTAG", "TACGAATCGATC", "polymerase fills in"),
             ("3' overhang", "ATGCTTAGCTAG", "TACGAATC    ", "ATGCTTAG", "TACGAATC", "3'-5' exonuclease trims")]
    for i, (name, top, bot, top2, bot2, how) in enumerate(items):
        y = 54 + i * 112
        out.append(t(20, y - 28, name, 14, INK, weight="bold"))
        s, w = dup(30, y, top, bot)
        out.append(s)
        out.append(ends53(30, y, top, bot))
        out.append(arrow(30 + w + 20, y + 14, 30 + w + 80, HOT))
        s, w2 = dup(30 + w + 100, y, top2, bot2)
        out.append(s)
        out.append(ends53(30 + w + 100, y, top2, bot2))
        out.append(t(30 + w + 28, y + 46, how, 11.5, HOT))
    out.append(t(20, 54 + 2 * 112 - 20, "Either way the result is blunt: that is what end repair is for.", 14, HOT))
    return svg(640, 54 + 2 * 112, "".join(out))


def fig_nickgap():
    out = []
    rows = [("nick", "ATGCTTAGCCA", "TACGAATCGGT", "nick", "ligase seals it (5'-P and 3'-OH needed)"),
            ("gap", "ATGCT   CCA", "TACGAATCGGT", "gap", "polymerase fills, then ligase seals"),
            ("flap", "ATGCTTAGCCA", "TACGAATCGGT", "flap",
             "a displaced 5' end: FEN1 or a 5'-3' exonuclease trims it"),
            ]
    y = 44
    for name, top, bot, kind, how in rows:
        s, w = dup(30, y, top, bot)
        out.append(s)
        if kind == "nick":
            out.append(line(30 + 5 * DX - 3, y - 12, 30 + 5 * DX - 3, y + 4, HOT, 2))
        if kind == "flap":
            # the downstream strand is peeled off from position 7 back to position 5,
            # so its first two bases sit above the duplex with a free 5' end
            jx = 30 + 7 * DX - 3
            fx = 30 + 5 * DX
            out.append(line(jx, y - 12, jx, y + 4, HOT, 2))
            out.append(t(fx, y - 20, "T", 13, HOT, family=MONO))
            out.append(t(fx + DX, y - 20, "A", 13, HOT, family=MONO))
            out.append(t(fx - 8, y - 20, "5'", 10, HOT, anchor="end"))
            out.append(line(fx + 2 * DX - 5, y - 24, jx, y - 13, HOT, 1.4))
        out.append(t(30, y - 22, name, 13, INK, weight="bold"))
        out.append(t(30 + w + 30, y + 16, how, 13, MUTE))
        y += 76
    out.append(t(20, y - 4, "Tn5 leaves gaps; nick translation moves a nick; Taq and Bst move forward by displacing or cutting flaps.", 13, HOT))
    return svg(720, y + 14, "".join(out))


def fig_repair():
    out = [t(20, 24, "after shearing: every kind of end in one tube", 13, INK, weight="bold")]
    shapes = [("blunt, 5'-OH", "ATGCT", "TACGA", "OH", None), ("5' overhang", "ATGCT", "TACGAAT", "P", None),
              ("3' overhang", "ATGCTTA", "TACGA", "P", None), ("3'-P damaged", "ATGCT", "TACGA", "P", "block")]
    for i, (n, top, bot, five, three) in enumerate(shapes):
        x = 30 + i * 190
        top = top.ljust(7); bot = bot.ljust(7)
        s, w = dup(x, 54, top, bot, pair=False)
        out.append(s)
        out.append(endmark(x - 10, 50, five, 5))
        if three:
            out.append(endmark(x + len(top.rstrip()) * DX + 6, 50, three, 5))
        out.append(t(x, 112, n, 12, MUTE))
    out.append(t(20, 134, "marks on the 5' end of the top strand: green 5'-P, open red 5'-OH; "
                          "red square: a blocking 3'-phosphate", 11.5, MUTE))
    out.append(t(20, 162, "end-repair mix", 13, INK, weight="bold"))
    out.append(t(20, 186, "T4 DNA polymerase:  fills 5' overhangs and trims 3' overhangs", 13, INK))
    out.append(t(20, 206, "T4 polynucleotide kinase:  adds 5'-P; its phosphatase removes 3'-P", 13, INK))
    out.append(t(20, 226, "(Klenow fragment sometimes added to help fill-in)", 12, MUTE))
    out.append(t(20, 256, "after: blunt, 5'-P, 3'-OH on every molecule", 14, OK, weight="bold"))
    s, w = dup(30, 276, "ATGCTTAG", "TACGAATC")
    out.append(s)
    out.append(endmark(20, 272, "P", 5))
    return svg(780, 324, "".join(out))


def fig_blunting():
    out = [t(20, 24, "One enzyme, two opposing activities, one resting state", 14, INK, weight="bold")]
    s, w = dup(30, 70, "ATGCTTAGCT", "TACGAATC  ")
    out.append(s)
    out.append(t(30, 56, "3' overhang: the exonuclease chews back to the duplex", 12, MUTE))
    s, w2 = dup(30, 150, "ATGCTTAG  ", "TACGAATCGA")
    out.append(s)
    out.append(t(30, 136, "5' overhang: the polymerase fills in", 12, MUTE))
    out.append(t(330, 84, "3'-5' exo removes unpaired 3' bases", 12, INK))
    out.append(t(330, 164, "5'-3' polymerase adds dNTPs", 12, INK))
    out.append(t(330, 214, "A blunt end is where neither activity has anything to do.", 13, HOT))
    out.append(t(20, 214, "", 12, MUTE))
    return svg(720, 236, "".join(out))


def fig_atail():
    out = [t(20, 24, "dA-tailing", 14, INK, weight="bold")]
    s, w = dup(30, 60, " ATGCTTAG ", " TACGAATC ")
    out.append(s)
    out.append(arrow(30 + w + 30, 74, 30 + w + 150, HOT))
    out.append(t(30 + w + 24, 56, "Klenow exo-, dATP only", 12, HOT))
    s, w2 = dup(30 + w + 170, 60, " ATGCTTAGA", "ATACGAATC ", hot_top=(9,), hot_bot=(0,))
    out.append(s)
    out.append(t(20, 140, "- one A on each 3' end, then it stops: no template for the next base", 13, INK))
    out.append(t(20, 160, "- with only dATP in the tube, nothing else can be added", 13, INK))
    out.append(t(20, 180, "- an exonuclease-proficient polymerase would remove the A again: futile cycle", 13, INK))
    out.append(t(20, 200, "- the T-overhang adapter is the other half of the pair", 13, INK))
    return svg(720, 220, "".join(out))


def fig_fillin():
    out = [t(20, 24, "MspI cuts C^CGG and leaves a 5'-CG overhang", 14, INK, weight="bold")]
    s, w = dup(30, 64, "GATTAC  ", "CTAATGGC", hot_bot=(6, 7))
    out.append(s)
    out.append(arrow(30 + w + 30, 78, 30 + w + 150, HOT))
    out.append(t(30 + w + 20, 58, "polymerase + dNTPs", 12, HOT))
    s, w2 = dup(30 + w + 170, 64, "GATTACCG", "CTAATGGC", hot_top=(6, 7))
    out.append(s)
    out.append(t(20, 142, "The filled-in C and G are copied from the dNTP mix, not from the genome.", 13, INK))
    out.append(t(20, 164, "The C belongs to a CpG, so its methylation state at the cut site is overwritten.", 13, INK))
    out.append(t(20, 186, "Supplying only chosen dNTPs controls which positions are filled (RRBS, Gu et al. 2011).", 13, MUTE))
    return svg(720, 204, "".join(out))


def fig_gaprepair():
    out = [t(20, 24, "After tagmentation the new ends are not yet complete", 14, INK, weight="bold")]
    out.append(ln(40, 62, 200, 62, TOP, 3))
    out.append(ln(40, 76, 236, 76, BOT, 3))
    out.append(bx(236, 68, 100, 16, "adapter A", "A", 11))
    out.append(bx(236, 52, 100, 12, "", "A"))
    out.append(ln(202, 62, 234, 62, BAD, 2, dash="3 2"))
    out.append(t(350, 70, "1  gap of 9 nt between 3'-OH and adapter", 12, BAD))
    out.append(ln(40, 126, 232, 126, TOP, 3))
    out.append(ln(40, 140, 236, 140, BOT, 3))
    out.append(bx(236, 132, 100, 16, "adapter A", "A", 11))
    out.append(bx(236, 116, 100, 12, "", "A"))
    out.append(arrow(200, 114, 230, HOT))
    out.append(t(350, 134, "2  polymerase at 72 C extends the 3'-OH across the gap", 12, HOT))
    out.append(t(20, 190, "Until the gap is filled, the adapter strand that was never joined is held on only by base pairing,", 13, INK))
    out.append(t(20, 210, "so it is lost on denaturing and the 3'-OH strand has no handle to copy.", 13, INK))
    return svg(720, 230, "".join(out))


def fig_dephos():
    out = [t(20, 24, "Switch every pre-existing end off, then make only the ends you want", 14, INK, weight="bold")]
    def frag(y, x0, x1, l, r, label=None):
        s = ln(x0, y, x1, y, TOP, 4)
        s += endmark(x0 - 6, y, l, 5) + endmark(x1 + 6, y, r, 5)
        return s
    frags = [(40, 150), (180, 330), (360, 470)]
    out.append(t(20, 54, "1  genomic DNA, ends carry 5'-P", 12, MUTE))
    for x0, x1 in frags:
        out.append(frag(72, x0, x1, "P", "P"))
    out.append(t(20, 108, "2  phosphatase (CIP, rSAP): every 5'-P becomes 5'-OH; ends cannot ligate to anything", 12, MUTE))
    for x0, x1 in frags:
        out.append(frag(126, x0, x1, "OH", "OH"))
    out.append(t(20, 162, "3  Cas9 cuts the middle molecule: the two new ends carry 5'-P", 12, MUTE))
    out.append(frag(180, 40, 150, "OH", "OH"))
    out.append(frag(180, 180, 238, "OH", "P"))
    out.append(frag(180, 272, 330, "P", "OH"))
    out.append(frag(180, 360, 470, "OH", "OH"))
    out.append(t(20, 216, "4  adapter ligation: only the cut sites are tagged, so only they are sequenced", 12, OK))
    out.append(t(20, 250, "green: 5'-P (ligatable)    open red: 5'-OH (inert)", 12, MUTE))
    return svg(720, 268, "".join(out))


def fig_rephos():
    out = [t(20, 24, "RNA example: the order of kinase steps is the chemistry", 14, INK, weight="bold")]
    steps = [("RNA fragment", "OH", "cP", "5'-OH, 2',3'-cyclic phosphate: nothing can ligate"),
             ("PNK, no ATP", "OH", "OH", "3' phosphatase: 3'-OH; ready for the 3' adapter"),
             ("3' adapter ligated", "OH", "ad", "3' end is now the adapter"),
             ("PNK + ATP", "P", "ad", "5'-OH becomes 5'-P: ready for the 5' adapter")]
    for i, (n, f, th, note) in enumerate(steps):
        y = 56 + i * 50
        out.append(t(20, y + 4, n, 13, INK, weight="bold"))
        out.append(ln(200, y, 330, y, RNAC, 4))
        out.append(endmark(194, y, f, 5))
        if th == "ad":
            out.append(ln(330, y, 400, y, HB, 4))
        elif th == "OH":
            out.append(endmark(336, y, "OH", 5))
        else:
            out.append(endmark(336, y, "block", 5))
        out.append(t(430, y + 4, note, 12, MUTE))
    out.append(t(20, 270, "Doing the ATP step first would phosphorylate 5' ends, and the RNA could then circularise.", 13, HOT))
    return svg(820, 290, "".join(out))


def fig_blocked():
    out = [t(20, 24, "A blocked 3' end can give a ligation but cannot take one", 14, INK, weight="bold")]
    rows = [("adapter, 5'-P and 3'-OH", False), ("adapter, 5'-P and 3' block", True)]
    for i, (n, blocked) in enumerate(rows):
        y = 86 + i * 96
        out.append(t(20, y - 28, n, 13, INK, weight="bold"))
        out.append(endmark(46, y, "P", 5))
        out.append(ln(52, y, 140, y, HB, 4))
        out.append(endmark(148, y, "block" if blocked else "OH", 5))
        out.append(endmark(220, y, "P", 5))
        out.append(ln(226, y, 314, y, HB, 4))
        out.append(endmark(322, y, "block" if blocked else "OH", 5))
        out.append(t(350, y + 4, "adapter ligates to adapter: no" if blocked else "adapter-adapter dimers form", 13, OK if blocked else BAD))
    out.append(t(20, 250, "Pre-adenylated 3'-blocked adapters, splints and capture oligos all use this.", 13, HOT))
    return svg(720, 268, "".join(out))


def fig_blocks():
    rows = [("3'-ddN (dideoxy)", ("no", BAD), ("no", BAD), "no"),
            ("3' C3 spacer", ("no", BAD), ("no", BAD), "no"),
            ("3' amino modifier", ("no", BAD), ("no", BAD), "no"),
            ("inverted dT (3'-3')", ("no", BAD), ("no", BAD), "no; also resists exonucleases"),
            ("3'-phosphate", ("no", BAD), ("no", BAD), ("yes: PNK or phosphatase", OK))]
    out = [table(20, 24, ["3' group", "extension", "ligation", "removable?"], rows, [230, 120, 120, 300], rowh=34)]
    out.append(t(20, 14 + 24 + 5 * 34 + 24, "Pick the block by whether you ever want it back.", 14, HOT))
    return svg(820, 14 + 24 + 5 * 34 + 44, "".join(out))


def fig_user():
    out = [t(20, 24, "dU in a hairpin adapter: cut it open after ligation", 14, INK, weight="bold")]
    out.append(bx(150, 60, 150, 18, "insert", "I"))
    out.append(ln(60, 64, 150, 64, HB, 3)); out.append(ln(60, 74, 150, 74, HB, 3))
    out.append(ln(300, 64, 390, 64, HB, 3)); out.append(ln(300, 74, 390, 74, HB, 3))
    out.append(hairpin(60, 69, -1)); out.append(hairpin(390, 69, 1))
    out.append(dot(44, 69, 4, HOT)); out.append(dot(406, 69, 4, HOT))
    out.append(t(44, 102, "U in loop", 11, HOT, anchor="middle")); out.append(t(406, 102, "U in loop", 11, HOT, anchor="middle"))
    out.append(t(20, 128, "1  ligated: the hairpin is a closed loop, so nothing can be amplified yet", 12, MUTE))
    out.append(t(20, 150, "2  USER (UDG + endonuclease VIII) removes U and cuts: the loop opens into a fork", 12, HOT))
    out.append(bx(150, 176, 150, 18, "insert", "I"))
    out.append(ln(60, 180, 150, 180, HB, 3)); out.append(ln(60, 190, 150, 190, HB, 3))
    out.append(ln(60, 180, 30, 170, HB, 2.4)); out.append(ln(60, 190, 30, 200, HB, 2.4))
    out.append(ln(300, 180, 390, 180, HB, 3)); out.append(ln(300, 190, 390, 190, HB, 3))
    out.append(ln(390, 180, 420, 170, HB, 2.4)); out.append(ln(390, 190, 420, 200, HB, 2.4))
    out.append(t(20, 228, "One adapter and one enzyme step give the forked adapter: no strand-specific ligation needed.", 13, INK))
    return svg(720, 246, "".join(out))


def fig_methyl():
    out = [t(20, 24, "Methylated adapters survive bisulfite", 14, INK, weight="bold")]
    out.append(t(20, 52, "before: adapter carries 5mC at every C, insert carries ordinary C", 12, MUTE))
    out.append(bx(30, 62, 120, 20, "adapter: mC", "A")); out.append(bx(152, 62, 150, 20, "insert: C, mC", "I"))
    out.append(bx(304, 62, 120, 20, "adapter: mC", "B"))
    out.append(t(20, 118, "bisulfite: unmethylated C -> U (read as T); 5mC is protected", 12, HOT))
    out.append(bx(30, 130, 120, 20, "adapter: mC kept", "A")); out.append(bx(152, 130, 150, 20, "insert: T, mC", "I"))
    out.append(bx(304, 130, 120, 20, "adapter: mC kept", "B"))
    out.append(t(20, 186, "If the adapter had ordinary C, its sequence would change and the PCR primers would stop pairing.", 13, INK))
    out.append(t(20, 208, "The alternative is to tag after conversion (PBAT) and avoid methylated adapters altogether.", 13, MUTE))
    return svg(720, 226, "".join(out))


def fig_hairpin():
    out = [t(20, 24, "Hairpin adapters: close the ends, make one continuous strand", 14, INK, weight="bold")]
    out.append(ln(80, 60, 300, 60, TOP, 3)); out.append(ln(80, 74, 300, 74, BOT, 3))
    out.append(hairpin(80, 67, -1, HB, 14)); out.append(hairpin(300, 67, 1, HB, 14))
    out.append(t(190, 100, "insert, both strands", 12, MUTE, anchor="middle"))
    out.append(t(20, 130, "- a molecule with no free ends cannot be degraded by exonucleases: single-stranded or open", 13, INK))
    out.append(t(20, 150, "  molecules can be digested away, leaving only complete circles (PacBio SMRTbell)", 13, INK))
    out.append(t(20, 172, "- both strands are one read: a sequencer can read the same duplex twice", 13, INK))
    out.append(t(20, 194, "- splinkerette: one hairpin end blocks priming, so only the correct end amplifies", 13, INK))
    return svg(720, 212, "".join(out))


def fig_ssdna():
    out = [t(20, 24, "Degraded or single-stranded input", 14, INK, weight="bold")]
    out.append(t(20, 54, "single-strand ligation", 13, INK, weight="bold"))
    out.append(ln(40, 74, 160, 74, TOP, 3)); out.append(endmark(164, 74, "OH", 5))
    out.append(bx(176, 66, 60, 16, "adapter", "A", 11))
    out.append(t(250, 78, "adapter ligated to the 3'-OH of each denatured strand, then copy and ligate the second adapter", 12, MUTE))
    out.append(t(20, 124, "adaptase", 13, INK, weight="bold"))
    out.append(ln(40, 144, 160, 144, TOP, 3)); t_ = "AAAA"
    out.append(t(162, 148, "AAAA", 12, HOT, family=MONO))
    out.append(bx(212, 136, 60, 16, "adapter", "A", 11))
    out.append(t(286, 148, "template-independent tail, then the stub joins: one tube, no 3'-OH selection", 12, MUTE))
    out.append(t(20, 196, "Both skip end repair and A-tailing: they work on molecules whose ends are too damaged to ligate in duplex.", 13, INK))
    out.append(t(20, 216, "Gansauge and Meyer 2013 for the first; the second is used in snmC-seq2 (Luo et al. 2018).", 12, MUTE))
    return svg(820, 236, "".join(out))


def fig_dilute():
    out = [t(20, 24, "Concentration decides whether a DNA end finds its own other end", 14, INK, weight="bold")]
    out.append(t(30, 54, "concentrated: ends meet other molecules", 13, INK, weight="bold"))
    for i, x in enumerate([30, 130, 230, 330]):
        out.append(ln(x, 90 if i % 2 else 80, x + 80, 90 if i % 2 else 80, TOP, 3))
    out.append(t(30, 126, "chimeras and concatemers", 12, BAD))
    out.append(t(500, 54, "dilute: ends find each other", 13, INK, weight="bold"))
    out.append(f'<circle cx="570" cy="100" r="28" fill="none" stroke="{TOP}" stroke-width="3"/>')
    out.append(f'<circle cx="670" cy="100" r="28" fill="none" stroke="{TOP}" stroke-width="3"/>')
    out.append(t(500, 150, "circles (intramolecular)", 12, OK))
    out.append(t(20, 180, "- the rate between molecules scales with their concentration; within one molecule it does not", 13, INK))
    out.append(t(20, 200, "- fragments shorter than about 150 bp are too stiff to bend into a circle at all", 13, INK))
    out.append(t(20, 220, "- use it for circularisation, inverse PCR and proximity ligation; do not use it for adapters", 13, INK))
    return svg(760, 240, "".join(out))


def fig_track():
    cols = ["step", "5' ends", "3' ends", "shape"]
    rows = [("sheared DNA", "P or OH", "OH, P or damaged", "ragged"),
            ("T4 pol + PNK", ("all P", OK), ("all OH", OK), ("blunt", OK)),
            ("Klenow exo-, dATP", ("P", OK), ("OH + one A", OK), ("3' A overhang", OK)),
            ("adapter ligation", ("joined", OK), ("joined", OK), ("adapter on each end", OK))]
    out = [table(20, 24, cols, rows, [220, 170, 220, 230], rowh=36)]
    out.append(t(20, 14 + 24 + 4 * 36 + 26, "Write this table for any protocol: three columns, one row per step.", 14, HOT))
    return svg(880, 14 + 24 + 4 * 36 + 46, "".join(out))


build(__file__, [
    ("catalogue", fig_catalogue),
    ("sources", fig_sources),
    ("shapes", fig_shapes),
    ("nick-gap-flap", fig_nickgap),
    ("end-repair", fig_repair),
    ("blunting", fig_blunting),
    ("a-tail", fig_atail),
    ("track-ends", fig_track),
    ("fill-in", fig_fillin),
    ("gap-repair", fig_gaprepair),
    ("dephos", fig_dephos),
    ("rephos", fig_rephos),
    ("blocked", fig_blocked),
    ("blocks", fig_blocks),
    ("user", fig_user),
    ("methyl", fig_methyl),
    ("hairpin", fig_hairpin),
    ("ssdna", fig_ssdna),
    ("dilute", fig_dilute),
])
