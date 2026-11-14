#!/usr/bin/env python3
"""Figures for the library-molecule unit.  Run: python3 library-molecule/make-figs.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

# ---------------------------------------------------------------- real sequences
# TruSeq adapter arms (Illumina Adapter Sequences, as printed in the TruSeq DNA PCR-free
# notes of the protocol collection).  Indexes are shown as placeholders.
P5 = "AATGATACGGCGACCACCGAGATCTACAC"
R1_SITE = "ACACTCTTTCCCTACACGACGCTCTTCCGATCT"
R2_SITE_TOP = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"     # as it sits on the top strand
P7_LAWN = "CAAGCAGAAGACGGCATACGAGAT"
P7_TOP = "ATCTCGTATGCCGTCTTCTGCTTG"
# Nextera / Tn5
ME = "AGATGTGTATAAGAGACAG"
TAIL_A = "TCGTCGGCAGCGTC"
TAIL_B = "GTCTCGTGGGCTCGG"


def rc(s):
    return s[::-1].translate(str.maketrans("ACGT", "TGCA"))


# guards: a wrong sequence in teaching material is worse than none
assert rc(P7_LAWN) == P7_TOP
assert rc(R1_SITE[-13:]) == R2_SITE_TOP[:13]          # the 12 bp stem plus the T / A
assert rc(ME) == "CTGTCTCTTATACACATCT"
assert rc(TAIL_B) == "CCGAGCCCACGAGAC"
assert len(P5) == 29 and len(R1_SITE) == 33 and len(R2_SITE_TOP) == 34 and len(P7_TOP) == 24

# ---------------------------------------------------------------- styles

IDXF, IDXC = "#efe9f3", "#6b5b8a"
SITEF = "#f1f1ee"
BCF, BCC = "#e6f0e8", OK
UMIF, UMIC = "#f7eedc", "#8a6a1f"
P5F, P7F = "#e8eef5", "#f5eae6"

KIND = {
    "p5": (P5F, TOP), "p7": (P7F, BAD), "idx": (IDXF, IDXC), "site": (SITEF, MUTE),
    "ins": ("none", MUTE), "bc": (BCF, BCC), "umi": (UMIF, UMIC), "dt": ("#f4f4f4", MUTE),
    "me": ("#eef0e4", "#6f7a3a"),
}


def row(x, y, segs, h=26, size=12):
    """A row of labelled boxes. segs = [(label, width, kind)]. Returns (svg, end_x, boxes)
    where boxes[i] = (x0, x1)."""
    out, boxes = [], []
    for label, w, kind in segs:
        fill, col = KIND[kind]
        if label and len(label) * size * 0.52 > w - 4:
            raise AssertionError(f"label '{label}' does not fit a {w}px box")
        out.append(box(x, y, w, h, label, fill, col, size, col if kind != "ins" else MUTE))
        boxes.append((x, x + w))
        x += w
    return "".join(out), x, boxes


def mono(x, y, pieces, size=11):
    """Coloured monospace runs on one line: pieces = [(text, colour)]. Returns (svg, end_x)."""
    cw = size * 0.602
    out = []
    for s, col in pieces:
        out.append(t(x, y, s, size, col, family=MONO))
        x += len(s) * cw
    return "".join(out), x


def cross(x, y, col=BAD):
    return t(x, y, "&#215;", 18, col, anchor="middle")


# ---------------------------------------------------------------- the molecule

def fig_construct():
    out = [t(40, 26, "The molecule every Illumina library must end up as, drawn on one strand, 5′ to 3′.",
             14, INK)]
    segs = [("P5", 84, "p5"), ("i5", 60, "idx"), ("Read 1 site", 100, "site"),
            ("insert", 200, "ins"), ("Read 2 site", 100, "site"), ("i7", 60, "idx"),
            ("P7", 84, "p7")]
    x0 = 60
    s, end, boxes = row(x0, 52, segs, 32, 13)
    out.append(s)
    out.append(arrow(x0, 100, end, MUTE))
    out.append(t(x0, 118, "5′", 12, MUTE))
    out.append(t(end, 118, "3′", 12, MUTE, anchor="end"))
    for i, (a, b) in enumerate(boxes):
        out.append(t((a + b) / 2, 118, str(i + 1), 13, HOT, anchor="middle", weight="bold"))
    legend = [
        "1  P5 · the same letters as the P5 lawn oligo, so the other strand's copy can grab the lawn",
        "2  i5 · sample index, read as Index 2",
        "3  Read 1 site · where the Read 1 primer anneals; the read starts just after it",
        "4  insert · the sample's DNA or cDNA, the only part of the molecule nobody designed",
        "5  Read 2 site · where the Read 2 primer anneals, from the other end",
        "6  i7 · sample index, read as Index 1",
        "7  P7 · pairs with the P7 lawn oligo, so the other end can bridge",
    ]
    for i, ln in enumerate(legend):
        out.append(t(60, 148 + i * 19, ln, 13, INK if i != 3 else HOT))
    return svg(end + 60, 292, "".join(out))


def fig_strands():
    out = [t(40, 26, "A library is double-stranded; each read primer sits on one strand and "
                     "copies the other.", 14, INK)]
    names_top = [("P5", 60, "p5"), ("i5", 44, "idx"), ("R1 site", 76, "site"),
                 ("insert", 150, "ins"), ("R2 site′", 76, "site"), ("i7", 44, "idx"),
                 ("P7′", 60, "p7")]
    names_bot = [("P5′", 60, "p5"), ("i5′", 44, "idx"), ("R1 site′", 76, "site"),
                 ("insert′", 150, "ins"), ("R2 site", 76, "site"), ("i7′", 44, "idx"),
                 ("P7", 60, "p7")]
    x0, yt, yb = 70, 84, 128
    s, end, bx = row(x0, yt, names_top, 26, 12)
    out.append(s)
    s2, _, _ = row(x0, yb, names_bot, 26, 12)
    out.append(s2)
    out.append(t(x0 - 8, yt + 18, "5′", 12, MUTE, anchor="end"))
    out.append(t(end + 8, yt + 18, "3′", 12, MUTE))
    out.append(t(x0 - 8, yb + 18, "3′", 12, MUTE, anchor="end"))
    out.append(t(end + 8, yb + 18, "5′", 12, MUTE))
    out.append(t(end + 34, yt + 18, "top strand", 12.5, TOP))
    out.append(t(end + 34, yb + 18, "bottom strand", 12.5, BOT))
    r1l, r1r = bx[2]
    r2l, r2r = bx[4]
    il, ir = bx[5]
    insl, insr = bx[3]
    # Read 1: primer on the bottom strand, extends rightwards
    out.append(arrow(r1l, yb + 44, insr - 4, HOT, 2.2))
    out.append(t(r1l, yb + 62, "Read 1: anneals to the bottom strand, so it reads the top-strand "
                               "sequence", 12.5, HOT))
    # Index 1: same template, further along
    out.append(arrow(r2l, yb + 84, ir, IDXC, 2.2))
    out.append(t(r2l - 6, yb + 88, "Index 1 (i7)", 12.5, IDXC, anchor="end"))
    # Read 2: primer on the top strand, extends leftwards
    out.append(arrow(r2l + 76, yt - 18, r1l + 6, BAD, 2.2))
    out.append(t(r2l + 76, yt - 28, "Read 2: anneals to the top strand and reads leftwards, "
                                    "from the other end", 12.5, BAD, anchor="end"))
    out.append(t(40, yb + 128, "The two ends of the top strand pair with the lawn: P7′ at its 3′ end "
                               "with a P7 oligo, and the bottom strand's P5′ with a P5 oligo.", 13.5, INK))
    out.append(t(40, yb + 148, "Index 2 (i5) is read in the turnaround between Index 1 and Read 2; "
                               "which way round it comes out depends on the instrument.", 13.5, MUTE))
    return svg(end + 150, yb + 168, "".join(out))


def fig_sequences():
    out = [t(40, 26, "The TruSeq arms, base by base (the index is shown as a placeholder).", 14, INK)]
    rows = [
        ("P5", [(P5, TOP)], "same as the P5 lawn oligo", 29),
        ("i5", [("[ 8 nt ]", IDXC)], "chosen per sample", 8),
        ("Read 1 site", [(R1_SITE[:-13], MUTE), (R1_SITE[-13:], HOT)], "ends in the stem (orange)", 33),
        ("insert", [("&#8230; your DNA or cDNA &#8230;", MUTE)], "", 0),
        ("Read 2 site", [(R2_SITE_TOP[:13], HOT), (R2_SITE_TOP[13:], MUTE)],
         "starts with the stem; the first A is the insert's own A-tail", 34),
        ("i7", [("[ 8 nt ]", IDXC)], "chosen per sample", 8),
        ("P7′", [(P7_TOP, BAD)], "reverse complement of the P7 lawn oligo", 24),
    ]
    y = 62
    for name, pieces, note, n in rows:
        out.append(t(130, y, name, 13.5, INK, anchor="end"))
        s, ex = mono(150, y, pieces, 13)
        out.append(s)
        out.append(t(450, y, (f"{n} nt · " if n else "") + note, 12.5, MUTE))
        y += 28
    out.append(t(40, y + 14, "Orange: the 12 bp stem of the Y adapter, and the same 13 letters "
                             "you see when a trimmer reports adapter content.", 13.5, INK))
    out.append(t(40, y + 36, "Both ends are the lawn oligos in disguise: P5 as written, P7 "
                             "reverse-complemented.", 13.5, MUTE))
    return svg(960, y + 54, "".join(out))


# ---------------------------------------------------------------- the TruSeq adapter

def fig_yadapter():
    out = [t(40, 26, "A Y adapter on each end of an A-tailed insert.", 14, INK)]
    yt, yb = 112, 128
    xs0, xs1, xi0, xi1, xe0, xe1 = 190, 270, 270, 510, 510, 590
    out.append(line(xs1, yt, xe0, yt, MUTE, 3))
    out.append(line(xs1, yb, xe0, yb, MUTE, 3))
    out.append(t((xi0 + xi1) / 2, yt - 12, "insert, 3′ A overhangs", 12.5, MUTE, anchor="middle"))
    # left Y
    out.append(line(xs0, yt, xs1, yt, TOP, 3))
    out.append(line(xs0, yb, xs1, yb, BAD, 3))
    out.append(line(xs0, yt, 120, 66, TOP, 3))
    out.append(line(xs0, yb, 120, 174, BAD, 3))
    # right Y
    out.append(line(xe0, yt, xe1, yt, BAD, 3))
    out.append(line(xe0, yb, xe1, yb, TOP, 3))
    out.append(line(xe1, yt, 660, 66, BAD, 3))
    out.append(line(xe1, yb, 660, 174, TOP, 3))
    for x in (xs1, xe0):
        out.append(line(x, yt - 8, x, yb + 8, HOT, 2.4))
    out.append(t(xs1, yb + 26, "ligation", 12, HOT, anchor="middle"))
    out.append(t(xe0, yb + 26, "ligation", 12, HOT, anchor="middle"))
    out.append(t(230, yb + 26 + 0, "", 12))
    out.append(t(230, yt - 14, "12 bp stem", 12.5, MUTE, anchor="middle"))
    out.append(t(30, 54, "P5 arm: i5 + Read 1 site", 12.5, TOP))
    out.append(t(30, 196, "P7 arm: Read 2 site + i7", 12.5, BAD))
    out.append(t(670, 62, "P7 arm", 12.5, BAD))
    out.append(t(670, 182, "P5 arm", 12.5, TOP))
    out.append(t(126, 80, "5′", 12, MUTE, anchor="end"))
    out.append(t(654, 80, "3′", 12, MUTE))
    out.append(t(126, 166, "3′", 12, MUTE, anchor="end"))
    out.append(t(654, 166, "5′", 12, MUTE))
    out.append(t(40, 226, "The two arms are not complementary, so they stay single-stranded. Whichever way "
                          "round the insert went in, each strand reads", 13.5, INK))
    out.append(t(40, 246, "5′ P5 arm … insert … P7 arm 3′, and the adapter's own 3′ T pairs with the "
                          "insert's 3′ A.", 13.5, INK))
    return svg(700, 264, "".join(out))


def fig_same_end():
    out = [t(40, 26, "Why the adapter is forked: the flow cell needs different ends.", 14, INK)]
    # row 1: straight adapter, same at both ends
    out.append(t(40, 58, "One straight adapter, ligated to both ends", 13.5, INK))
    s, e, _ = row(40, 68, [("P5 adapter", 90, "p5"), ("insert", 150, "ins"),
                           ("P5 adapter′", 90, "p5")], 24, 12)
    out.append(s)
    out.append(cross(e + 24, 86))
    out.append(t(e + 44, 85, "P5-type at both ends: cannot bridge, no cluster", 13, BAD))
    # row 2: forked adapter
    out.append(t(40, 128, "A forked adapter, ligated to both ends", 13.5, INK))
    s, e, _ = row(40, 138, [("P5 arm", 90, "p5"), ("insert", 150, "ins"),
                            ("P7′ arm", 90, "p7")], 24, 12)
    out.append(s)
    out.append(t(e + 24, 156, "&#10003;", 18, OK, anchor="middle"))
    out.append(t(e + 44, 155, "P5 at one end, P7 at the other, on every strand", 13, OK))
    # row 3: two straight adapters mixed
    out.append(t(40, 198, "Two straight adapters, A and B, ligated at random", 13.5, INK))
    x = 40
    for lab, k1, k2, share, ok in [("A / A", "p5", "p5", "25 %", False),
                                   ("A / B", "p5", "p7", "50 %", True),
                                   ("B / B", "p7", "p7", "25 %", False)]:
        s, e, _ = row(x, 208, [(lab[0], 36, k1), ("insert", 80, "ins"), (lab[-1], 36, k2)], 24, 12)
        out.append(s)
        out.append(t(x, 252, f"{lab}  {share}", 12.5, OK if ok else BAD))
        x += 200
    out.append(t(x + 10, 228, "half is wasted", 13, BAD))
    return svg(x + 140, 270, "".join(out))


# ---------------------------------------------------------------- Nextera / Tn5

def fig_tagmentation():
    out = [t(40, 26, "Tagmentation: Tn5 cuts and tags in one step, and leaves a 9-nt gap.", 14, INK)]
    TA, TB = TOP, BAD
    titles = ["1  Tn5 on the DNA", "2  cut and tagged", "3  72 °C fill-in"]
    yt, yb = 118, 134
    for p in range(3):
        x0 = 30 + p * 290
        out.append(t(x0 + 120, 56, titles[p], 13.5, INK, anchor="middle"))
        if p == 0:
            out.append(line(x0, yt, x0 + 250, yt, MUTE, 2.6))
            out.append(line(x0, yb, x0 + 250, yb, MUTE, 2.6))
            for cx in (x0 + 70, x0 + 180):
                out.append(f'<ellipse cx="{cx}" cy="126" rx="22" ry="30" fill="#f3e3d9" '
                           f'stroke="{HOT}" stroke-width="1.4"/>')
                out.append(t(cx, 130, "Tn5", 12, HOT, anchor="middle"))
            out.append(t(x0 + 125, 190, "each dimer holds two", 12, MUTE, anchor="middle"))
            out.append(t(x0 + 125, 206, "transposon ends", 12, MUTE, anchor="middle"))
        else:
            a, b = x0 + 70, x0 + 180
            for (u0, u1) in ((x0, x0 + 40), (x0 + 210, x0 + 250)):
                out.append(line(u0, yt, u1, yt, "#c9ccd0", 2.6))
                out.append(line(u0, yb, u1, yb, "#c9ccd0", 2.6))
            out.append(line(a, yt, b - 18, yt, MUTE, 2.6))            # top strand
            out.append(line(a + 18, yb, b, yb, MUTE, 2.6))            # bottom strand
            out.append(line(a - 34, yt, a, yt, TA, 4))                # tag A, 5' of top
            out.append(line(b, yb, b + 34, yb, TB, 4))                # tag B, 5' of bottom
            if p == 1:
                out.append(line(a, yb + 8, a + 18, yb + 8, HOT, 1.6))
                out.append(t(a + 9, yb + 24, "gap", 12, HOT, anchor="middle"))
                out.append(line(b - 18, yt - 8, b, yt - 8, HOT, 1.6))
                out.append(t(b - 9, yt - 14, "gap", 12, HOT, anchor="middle"))
                out.append(t(x0 + 125, 196, "tags are on the 5′ ends only", 12, MUTE, anchor="middle"))
            else:
                out.append(line(b - 18, yt, b + 34, yt, TB, 4, dash="3 3"))    # copy of tag B
                out.append(line(a + 18, yb, a - 34, yb, TA, 4, dash="3 3"))    # copy of tag A
                out.append(t(b + 34, yt - 10, "copy of B", 12, TB, anchor="end"))
                out.append(t(a - 34, yb + 22, "copy of A", 12, TA))
                out.append(t(x0 + 125, 196, "dashed: new strand copied across the gap", 12, MUTE, anchor="middle"))
                out.append(t(x0 + 125, 212, "and the other end's tag", 12, MUTE, anchor="middle"))
            out.append(t(a - 17, yt - 12, "tag A", 12, TA, anchor="middle"))
            out.append(t(b + 17, yb + 22, "tag B", 12, TB, anchor="middle"))
        if p < 2:
            out.append(arrow(x0 + 258, 126, x0 + 286, MUTE))
    return svg(890, 232, "".join(out))


def fig_tag_combos():
    out = [t(40, 26, "Tn5 puts tag A or tag B on each end at random; only A at one end and B at "
                     "the other can become P5 … P7.", 14, INK)]
    y = 54
    for lab, ka, kb, share, ok, note in [
            ("A / B", "p5", "p7", "50 %", True, "i5 primer binds tag A, i7 primer binds tag B: P5 … P7"),
            ("A / A", "p5", "p5", "25 %", False, "only the i5 primer fits: P5 … P5, cannot bridge"),
            ("B / B", "p7", "p7", "25 %", False, "only the i7 primer fits: P7 … P7, cannot bridge")]:
        s, e, _ = row(40, y, [("tag " + lab[0], 70, ka), ("insert", 150, "ins"),
                              ("tag " + lab[-1] + "′", 70, kb)], 26, 12)
        out.append(s)
        out.append(t(e + 16, y + 18, share, 13, OK if ok else BAD, weight="bold"))
        out.append(t(e + 62, y + 18, note, 13, OK if ok else BAD))
        y += 44
    out.append(t(40, y + 12, "Tag A = 14-nt tail + mosaic end; tag B = 15-nt tail + the same mosaic end. "
                             "The tails are what the index primers recognise.", 13.5, INK))
    return svg(900, y + 30, "".join(out))


def fig_nextera_molecule():
    out = [t(40, 26, "The finished Nextera / Tn5 molecule: the Read 1 and Read 2 sites are built "
                     "from tail + mosaic end.", 14, INK)]
    segs = [("P5", 66, "p5"), ("i5", 50, "idx"), ("tail A", 56, "site"), ("ME", 52, "me"),
            ("insert", 150, "ins"), ("ME′", 52, "me"), ("tail B′", 56, "site"),
            ("i7", 50, "idx"), ("P7", 66, "p7")]
    x0, y = 50, 100
    s, end, b = row(x0, y, segs, 30, 12.5)
    out.append(s)
    # brackets
    for (l, r, label, col) in [(b[2][0], b[3][1], "Read 1 site", TOP), (b[5][0], b[6][1], "Read 2 site", BAD)]:
        out.append(line(l, y - 12, r, y - 12, col, 1.6))
        out.append(line(l, y - 12, l, y - 6, col, 1.6))
        out.append(line(r, y - 12, r, y - 6, col, 1.6))
        out.append(t((l + r) / 2, y - 18, label, 13, col, anchor="middle"))
    out.append(line(b[3][0], y + 42, b[3][1], y + 42, "#6f7a3a", 1.6))
    out.append(line(b[5][0], y + 42, b[5][1], y + 42, "#6f7a3a", 1.6))
    out.append(t(b[3][0] + 26, y + 58, "the Tn5 part", 12, "#6f7a3a", anchor="middle"))
    out.append(t(b[5][0] + 26, y + 58, "the Tn5 part", 12, "#6f7a3a", anchor="middle"))
    y2 = 186
    out.append(t(50, y2, "mosaic end (ME) " + ME + "  · 19 nt, the sequence Tn5 binds", 13, INK, family=None))
    out.append(t(50, y2 + 22, "tail A " + TAIL_A + "   tail B " + TAIL_B, 13, INK))
    out.append(t(50, y2 + 48, "Same idea as TruSeq: P5 … P7 at the ends, an index inside each, a primer site next "
                              "to the insert. Different part: the primer sites contain the Tn5 end.", 13.5, MUTE))
    return svg(end + 60, y2 + 68, "".join(out))


# ---------------------------------------------------------------- full versus truncated

def fig_full_vs_truncated():
    out = []
    xs = 60

    def whole(y, with_all=True):
        segs = [("P5", 60, "p5"), ("i5", 44, "idx"), ("R1 site", 76, "site"),
                ("insert", 150, "ins"), ("R2 site′", 76, "site"), ("i7", 44, "idx"),
                ("P7′", 60, "p7")]
        return row(xs, y, segs, 24, 12)

    out.append(t(40, 26, "Full adapters: the ligation delivers the whole molecule.", 14, INK))
    s, end, _ = whole(36)
    out.append(s)
    out.append(t(end + 18, 54, "PCR-free is possible (TruSeq DNA PCR-free)", 12.5, MUTE))

    out.append(t(40, 106, "Truncated adapters: ligation delivers only the primer sites ...", 14, INK))
    segs = [("", 120, "ins"), ("R1 site", 76, "site"), ("insert", 150, "ins"), ("R2 site′", 76, "site")]
    # use ghost boxes for alignment
    out.append(box(xs + 104, 116, 76, 24, "R1 site", SITEF, MUTE, 12, MUTE))
    out.append(box(xs + 180, 116, 150, 24, "insert", "none", MUTE, 12, MUTE))
    out.append(box(xs + 330, 116, 76, 24, "R2 site′", SITEF, MUTE, 12, MUTE))

    out.append(t(40, 170, "... and two tailed primers add the rest during index PCR.", 14, INK))
    # left primer: P5 + i5 tail, R1 anneal part
    out.append(box(xs, 180, 60, 22, "P5", P5F, TOP, 12, TOP))
    out.append(box(xs + 60, 180, 44, 22, "i5", IDXF, IDXC, 12, IDXC))
    out.append(box(xs + 104, 180, 76, 22, "R1 site", SITEF, MUTE, 12, MUTE))
    out.append(arrow(xs + 100, 214, xs + 190, HOT))
    out.append(t(xs + 104, 230, "primer: tail + 3′ part that pairs", 12, HOT))
    # right primer
    out.append(box(xs + 330, 180, 76, 22, "R2 site′", SITEF, MUTE, 12, MUTE))
    out.append(box(xs + 406, 180, 44, 22, "i7", IDXF, IDXC, 12, IDXC))
    out.append(box(xs + 450, 180, 60, 22, "P7′", P7F, BAD, 12, BAD))
    out.append(arrow(xs + 336, 214, xs + 246, HOT))
    # second line, so this label cannot be read as belonging to the left-hand arrow
    out.append(t(xs + 291, 250, "its own tailed primer", 12, HOT, anchor="middle"))
    out.append(t(xs + 530, 197, "cost: needs PCR", 12.5, BAD))
    out.append(t(xs + 530, 133, "adapters can be generic", 12.5, OK))
    return svg(xs + 680, 268, "".join(out))


def fig_tailed_primer():
    out = [t(40, 26, "A tailed primer works in three stages.", 14, INK)]
    titles = ["cycle 1: only the 3′ part pairs", "cycle 2: the copy carries the tail",
              "cycle 3 on: the whole primer pairs"]
    for p in range(3):
        x0 = 30 + p * 290
        out.append(t(x0 + 110, 56, titles[p], 13, INK, anchor="middle"))
        yt = 130
        out.append(line(x0 + 60, yt, x0 + 230, yt, MUTE, 2.6))
        out.append(t(x0 + 54, yt + 4, "3′", 11.5, MUTE, anchor="end"))
        # annealing part
        a0, a1 = x0 + 100, x0 + 180
        for i in range(8):
            xx = a0 + 5 + i * 9.5
            out.append(line(xx, yt - 3, xx, yt - 14, MUTE, 1))
        out.append(line(a0, yt - 18, a1, yt - 18, INK, 3))
        out.append(arrow(a1 - 2, yt - 18, a1 + 12, INK, 3, 5))
        if p == 0:
            out.append(line(a0, yt - 18, x0 + 62, yt - 52, HOT, 3))
            out.append(t(x0 + 56, yt - 58, "tail", 12, HOT, anchor="middle"))
            out.append(t(x0 + 110, yt + 30, "the tail hangs free", 12, MUTE, anchor="middle"))
        elif p == 1:
            # the copy now has the tail
            out.append(line(x0 + 60, yt + 14, x0 + 230, yt + 14, BOT, 2.6))
            out.append(line(x0 + 60, yt + 14, x0 + 20, yt + 14, HOT, 3.2, dash="4 3"))
            out.append(t(x0 + 38, yt + 34, "tail, now in the DNA", 12, HOT, anchor="middle"))
            out.append(t(x0 + 140, yt + 52, "the opposite primer copies this strand", 12, MUTE,
                         anchor="middle"))
        else:
            out.append(line(a0, yt - 18, x0 + 62, yt - 18, HOT, 3))
            for i in range(6):
                xx = x0 + 68 + i * 5.2
                out.append(line(xx, yt - 3, xx, yt - 14, HOT, 1))
            out.append(t(x0 + 110, yt + 30, "full-length products amplify", 12, MUTE, anchor="middle"))
            out.append(t(x0 + 110, yt + 48, "with the whole primer pairing", 12, MUTE, anchor="middle"))
    out.append(t(40, 214, "Only molecules made from cycle 2 onward carry both tails; after a few more cycles "
                          "they dominate the tube, which is why index PCR needs only a handful of cycles.",
                 13, MUTE))
    return svg(920, 232, "".join(out))


# ---------------------------------------------------------------- information

def fig_read_structures():
    out = [t(40, 26, "Where the information sits in the four example protocols.", 14, INK)]
    cols = [("Read 1", 40, 190), ("Index 1 (i7)", 240, 110), ("Index 2 (i5)", 360, 110),
            ("Read 2", 480, 190)]
    for name, x, w in cols:
        out.append(t(x + w / 2, 54, name, 13.5, INK, anchor="middle", weight="bold"))
    protos = [
        ("TruSeq DNA PCR-free", ["ins", "i7 · 8", "i5 · 8", "ins"]),
        ("Nextera XT", ["ins", "i7 · 8", "i5 · 8", "ins"]),
        ("Illumina DNA Prep (UD indexes)", ["ins", "i7 · 10", "i5 · 10", "ins"]),
        ("10x 3′ v3", ["bcumi", "i7 · 8", "none", "cDNA 91"]),
    ]
    y = 70
    for pname, cells in protos:
        out.append(t(40, y + 15, pname, 13, INK))
        y += 24
        for (name, x, w), c in zip(cols, cells):
            if c == "ins":
                out.append(box(x, y, w, 26, "insert (your choice of length)", "none", MUTE, 12, MUTE))
            elif c == "bcumi":
                out.append(box(x, y, 118, 26, "cell barcode 16", BCF, BCC, 12, BCC))
                out.append(box(x + 118, y, 72, 26, "UMI 12", UMIF, UMIC, 12, UMIC))
            elif c == "none":
                out.append(box(x, y, w, 26, "not read", "none", "#c9ccd0", 12, MUTE))
            elif c.startswith("cDNA"):
                out.append(box(x, y, w, 26, "cDNA insert 91", "none", MUTE, 12, MUTE))
            else:
                out.append(box(x, y, w, 26, c, IDXF, IDXC, 12, IDXC))
        y += 38
    out.append(t(40, y + 6, "10x specifies its read lengths (28 / 8 / 0 / 91); for the three Illumina kits the "
                            "insert reads are chosen by you.", 13, MUTE))
    return svg(700, y + 24, "".join(out))


def fig_barcode_placement():
    out = [t(40, 26, "Three places to put a label, and what each one costs.", 14, INK)]
    rows = [
        ("In an index read",
         [("P5", 50, "p5"), ("i5", 40, "idx"), ("R1 site", 64, "site"), ("insert", 120, "ins"),
          ("R2 site", 64, "site"), ("i7", 40, "idx"), ("P7", 50, "p7")],
         "added by the adapter or index PCR, the last step; read separately, so no insert cycles are used"),
        ("At the start of Read 1",
         [("P5", 50, "p5"), ("R1 site", 64, "site"), ("barcode", 60, "bc"), ("UMI", 44, "umi"),
          ("insert", 140, "ins"), ("R2 site", 64, "site"), ("i7", 40, "idx"), ("P7", 50, "p7")],
         "added by the RT primer, the first step, so cells can be pooled early; costs read cycles"),
        ("In-line, next to the insert",
         [("P5", 50, "p5"), ("R1 site", 64, "site"), ("bc", 36, "bc"), ("insert", 150, "ins"),
          ("R2 site", 64, "site"), ("P7", 50, "p7")],
         "added by a barcoded adapter; no index primer needed, but few barcodes means low diversity"),
    ]
    y = 46
    for title, segs, note in rows:
        out.append(t(40, y + 10, title, 13.5, INK, weight="bold"))
        s, e, _ = row(40, y + 18, segs, 26, 11.5)
        out.append(s)
        out.append(t(40, y + 62, note, 12.5, MUTE))
        y += 86
    out.append(t(40, y + 6, "The earlier in the protocol a label is added, the earlier samples can share one tube.",
                 13.5, HOT))
    return svg(900, y + 24, "".join(out))


def fig_10x():
    out = [t(40, 26, "10x 3′ v3: the cell barcode and UMI are read first, the transcript second.", 14, INK)]
    segs = [("P5", 50, "p5"), ("R1 site", 66, "site"), ("cell barcode 16", 112, "bc"),
            ("UMI 12", 70, "umi"), ("poly(dT)", 64, "dt"), ("cDNA insert", 160, "ins"),
            ("R2 site", 66, "site"), ("i7", 46, "idx"), ("P7", 52, "p7")]
    x0, y = 50, 100
    s, end, b = row(x0, y, segs, 28, 12)
    out.append(s)
    # Read 1
    out.append(arrow(b[1][1], y - 20, b[3][1], HOT, 2.2))
    out.append(t(b[1][1], y - 30, "Read 1 · 28 cycles = 16 + 12", 12.5, HOT))
    # index 1, drawn above: below the molecule it crowds the Read 2 label
    out.append(arrow(b[6][1], y - 20, b[7][1], IDXC, 2.2))
    out.append(t((b[6][1] + b[7][1]) / 2, y - 30, "Index 1 · 8 cycles", 12.5, IDXC,
                 anchor="middle"))
    # Read 2
    out.append(arrow(b[6][0], y + 40, b[5][0] + 30, BAD, 2.2))
    out.append(t(b[6][0] - 4, y + 60, "Read 2 · 91 cycles into the cDNA", 12.5, BAD, anchor="end"))
    out.append(t(50, y + 96, "Index 2 · 0 cycles: this library has no i5, so the flow-cell P5 end sits directly "
                              "beside the Read 1 site.", 13, INK))
    out.append(t(50, y + 118, "Read 2 starts where the cDNA was fragmented, so it reads the transcript's own strand "
                              "from the 3′ region inwards.", 13, MUTE))
    return svg(end + 60, y + 138, "".join(out))


def fig_strand():
    out = [t(40, 26, "Which strand does Read 1 read? It depends on how the orientation is fixed.", 14, INK)]
    rows = [
        ("Y adapters ligated to ds cDNA", "nothing fixes it", "random"),
        ("dUTP second strand, then Y adapters", "only the first strand survives", "antisense"),
        ("barcoded oligo(dT) priming (10x 3′)", "the primer defines the end", "fixed"),
    ]
    out.append(t(560, 54, "transcript 5′ → 3′", 12, MUTE, anchor="middle"))
    y = 70
    for lab, how, mode in rows:
        out.append(t(40, y + 18, lab, 13, INK))
        out.append(t(40, y + 36, how, 12, MUTE))
        fx0, fx1 = 480, 640
        out.append(arrow(fx0, y + 10, fx1, MUTE, 1.4))
        out.append(line(fx0, y + 26, fx1, y + 26, "#c9ccd0", 6))
        # HOT and BAD are too close in hue to tell apart at this size, so each
        # arrow carries its own tag as well
        def leftward(col, lab, short=False):
            out.append(arrow(fx1 - 4, y + 40, fx1 - (36 if short else 54), col, 2.2))
            out.append(t(fx1 + 6, y + 44, lab, 11.5, col))

        def rightward(col, lab):
            out.append(arrow(fx0 + 4, y + 40, fx0 + 54, col, 2.2))
            out.append(t(fx0 - 6, y + 44, lab, 11.5, col, anchor="end"))

        if mode == "random":
            rightward(HOT, "R1")
            leftward(BAD, "R2")
            out.append(t(fx1 + 34, y + 28, "or the other way round: R1 on either strand", 12.5, BAD))
        elif mode == "antisense":
            leftward(HOT, "R1")
            rightward(BAD, "R2")
            out.append(t(fx1 + 34, y + 28, "R1 antisense, R2 sense, every time", 12.5, OK))
        else:
            leftward(HOT, "R1", short=True)
            rightward(BAD, "R2")
            out.append(t(fx1 + 34, y + 28, "R1 reads barcode + UMI; R2 sense", 12.5, OK))
        y += 62
    out.append(t(40, y + 10, "Arrows: Read 1 and Read 2, tagged R1 and R2, drawn on a fragment cut "
                             "from the transcript.", 12.5, MUTE))
    return svg(920, y + 28, "".join(out))


# ---------------------------------------------------------------- what fails

def fig_gallery():
    out = [t(40, 26, "Six molecules in one tube. Only one of them is what you wanted.", 14, INK)]
    rows = [
        ([("P5", 54, "p5"), ("insert  300 bp", 150, "ins"), ("P7′", 54, "p7")],
         "clusters and reads", OK),
        ([("P5", 54, "p5"), ("insert", 150, "ins"), ("P5′", 54, "p5")],
         "same end twice: cannot bridge, no cluster", BAD),
        ([("P5", 54, "p5"), ("insert", 150, "ins")],
         "one end only: washes away", BAD),
        ([("P5 arm", 54, "p5"), ("P7′ arm", 54, "p7")],
         "adapter dimer: ~135 bp, clusters very well, reads only adapter", BAD),
        ([("P5", 54, "p5"), ("insert  1.5 kb", 250, "ins"), ("P7′", 54, "p7")],
         "too long: bridges poorly and is outcompeted by short molecules", BAD),
        ([("P5", 54, "p5"), ("ins 20", 50, "ins"), ("P7′", 54, "p7")],
         "clusters, but a 100-cycle read runs through into the adapter", UMIC),
    ]
    y = 44
    for segs, verdict, col in rows:
        s, e, _ = row(40, y, segs, 24, 12)
        out.append(s)
        out.append(t(450, y + 17, verdict, 13, col))
        y += 34
    return svg(780, y + 10, "".join(out))


def fig_readthrough():
    out = [t(40, 26, "When the insert is shorter than the read, the read keeps going into the adapter.",
             14, INK)]
    px = 5.0
    ins = 30
    r1 = [(ins, "insert 30", "ins"), (len(R2_SITE_TOP), "Read 2 site", "site"), (8, "i7", "idx"),
          (len(P7_TOP), "P7′", "p7")]
    r2 = [(ins, "insert 30", "ins"), (len(R1_SITE), "Read 1 site′", "site"), (8, "i5′", "idx"),
          (len(P5), "P5′", "p5")]
    for k, (lab, parts) in enumerate([("Read 1 (100 cycles)", r1), ("Read 2 (100 cycles)", r2)]):
        y = 52 + k * 82
        out.append(t(40, y + 14, lab, 13.5, INK, weight="bold"))
        x = 190
        for n, name, kind in parts:
            w = n * px
            fill, col = KIND[kind]
            out.append(box(x, y, w, 22, name if len(name) * 6.2 < w - 2 else "", fill, col, 11, col))
            x += w
        used = sum(n for n, _, _ in parts)
        out.append(line(190 + 100 * px, y - 4, 190 + 100 * px, y + 26, HOT, 1.6))
        out.append(t(190 + 100 * px + 6, y + 15, f"cycle 100; molecule ends at {used}", 12, HOT))
    # sequences
    y = 112
    s, _ = mono(190 + ins * px, y, [("AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC", MUTE), ("[i7]", IDXC),
                                    ("ATCTCGTATGCCGTCTTCTGCTTG", BAD)], 10.5)
    out.append(s)
    y = 194
    s, _ = mono(190 + ins * px, y, [(rc(R1_SITE), MUTE), ("[i5′]", IDXC), (rc(P5), TOP)], 10.5)
    out.append(s)
    out.append(t(40, 228, "Both reads start the same way, AGATCGGAAGAGC, then diverge: that is how a "
                          "trimmer knows which read it is looking at.", 13, INK))
    out.append(t(40, 248, "R1's read-through also contains the i7 index, in the same orientation as "
                          "the Index 1 read.", 13, MUTE))
    return svg(190 + 100 * px + 260, 266, "".join(out))


# ---------------------------------------------------------------- reading a construct

def fig_derive():
    out = [t(40, 26, "From construct to read structure: read the arrows off the drawing.", 14, INK)]
    segs = [("P5", 50, "p5"), ("i5 · 10", 62, "idx"), ("R1 site", 66, "site"), ("UMI 9", 56, "umi"),
            ("insert", 170, "ins"), ("R2 site", 66, "site"), ("i7 · 10", 62, "idx"), ("P7", 52, "p7")]
    x0, y = 50, 104
    s, end, b = row(x0, y, segs, 28, 12)
    out.append(s)
    out.append(arrow(b[2][1], y - 20, b[4][0] + 80, HOT, 2.2))
    out.append(t(b[2][1], y - 30, "Read 1: 9 UMI + 75 insert = 84", 12.5, HOT))
    out.append(arrow(b[5][1], y + 46, b[6][1], IDXC, 2.2))
    out.append(t(b[6][1] + 6, y + 62, "Index 1: 10", 12.5, IDXC, anchor="middle"))
    out.append(arrow(b[1][0], y + 46, b[1][1], IDXC, 2.2))
    out.append(t(b[1][0] + 30, y + 62, "Index 2: 10", 12.5, IDXC, anchor="middle"))
    out.append(arrow(b[5][0], y + 78, b[4][0] + 60, BAD, 2.2))
    out.append(t(b[5][0] - 4, y + 94, "Read 2: 75 insert", 12.5, BAD, anchor="end"))
    out.append(t(50, y + 128, "Read structure:   84 / 10 / 10 / 75", 20, INK, weight="bold"))
    out.append(t(50, y + 152, "Read 1 starts with 9 bases that are not genome; the pipeline must cut them off "
                              "and keep them as the UMI.", 13, MUTE))
    return svg(end + 60, y + 172, "".join(out))


build(__file__, [
    ("construct", fig_construct),
    ("strands", fig_strands),
    ("sequences", fig_sequences),
    ("y-adapter", fig_yadapter),
    ("same-end", fig_same_end),
    ("tagmentation", fig_tagmentation),
    ("tag-combos", fig_tag_combos),
    ("nextera-molecule", fig_nextera_molecule),
    ("full-vs-truncated", fig_full_vs_truncated),
    ("tailed-primer", fig_tailed_primer),
    ("read-structures", fig_read_structures),
    ("barcode-placement", fig_barcode_placement),
    ("tenx", fig_10x),
    ("strand", fig_strand),
    ("gallery", fig_gallery),
    ("readthrough", fig_readthrough),
    ("derive", fig_derive),
])
