#!/usr/bin/env python3
"""Figures for the design unit.  Run: python3 design/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PB, PR, PP, GR, PG, PO = "#e8eef5", "#f5eae6", "#efe9f3", "#f1f1ee", "#e6f0e8", "#f7ece5"
VIO = "#6b5b8a"


def path(d, stroke=TOP, w=2.4, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round"{ds}/>')


def mbox(x, y, w, h, lines, fill="none", stroke=MUTE, size=12, tcol=INK):
    out = [box(x, y, w, h, "", fill, stroke, r=4)]
    n = len(lines)
    for i, ln in enumerate(lines):
        out.append(t(x + w / 2, y + h / 2 + (i - (n - 1) / 2) * (size + 3) + size * 0.35, ln,
                     size, tcol, anchor="middle"))
    return "".join(out)


def cross(x, y, c=BAD, s=6):
    return line(x - s, y - s, x + s, y + s, c, 2.2) + line(x - s, y + s, x + s, y - s, c, 2.2)


def tick(x, y, c=OK, s=6):
    return line(x - s, y, x - 2, y + s - 1, c, 2.4) + line(x - 2, y + s - 1, x + s, y - s, c, 2.4)


KIND = {"p5": (PB, TOP), "p7": (PR, BAD), "idx": (PP, VIO), "ins": ("none", MUTE),
        "ad": (GR, MUTE), "hot": (PO, HOT), "ok": (PG, OK), "insB": ("#fbeee3", HOT),
        "insA": ("#e3edf7", TOP)}


def chain(x, y, parts, h=22, size=11.5):
    out = []
    for label, w, k in parts:
        fill, col = KIND[k]
        out.append(box(x, y, w, h, label, fill, col, size, col, r=3))
        x += w
    return "".join(out), x


def small(x, y, s, fill=INK, size=10):
    """Monospace text at 6 px per character; returns (svg, width)."""
    return t(x, y, s, size, fill, family=MONO), len(s) * size * 0.6


def tick(x, y, c=OK, s=6):
    return line(x - s, y, x - 2, y + s - 1, c, 2.4) + line(x - 2, y + s - 1, x + s, y - s, c, 2.4)


# ================================================================ reading a protocol

def fig_blocks():
    out = [t(40, 26, "Eight blocks cover most library preparations. Each changes the ends or "
                     "the content of the molecule.", 14, INK)]
    blocks = [("fragment", "makes ends", PB, TOP), ("end prep", "blunt, 5'-P, A-tail", PB, TOP),
              ("ligate", "adds adapter", PO, HOT), ("reverse transcribe", "RNA to cDNA", PG, OK),
              ("amplify", "copies, adds ends", PO, HOT), ("select", "size or affinity", PP, VIO),
              ("index", "adds a barcode", PP, VIO), ("pool and load", "equal moles", PB, TOP)]
    for i, (a, b, f, c) in enumerate(blocks):
        x = 40 + (i % 4) * 172
        y = 48 + (i // 4) * 72
        out.append(mbox(x, y, 156, 56, [a, b], f, c, 12.5, c))
    out.append(t(40, 212, "Write the protocol as a string of these. A step that fits none of "
                          "them is a trick: look it up.", 14, INK))
    return svg(720, 232, "".join(out))


def fig_walk_dna():
    out = [t(40, 26, "Draw the construct after every step. Genomic DNA, ligation-based "
                     "library.", 14, INK)]
    rows = [("1  shear", [("insert, ragged ends", 190, "ins")], "mixed 5'-P / 5'-OH, overhangs"),
            ("2  end repair, A-tail", [("A", 14, "hot"), ("insert, blunt, 5'-P", 190, "ins"),
                                       ("A", 14, "hot")], "3' A overhang on each end"),
            ("3  ligate", [("adapter", 52, "p5"), ("insert", 190, "ins"), ("adapter", 52, "p7")],
             "T-overhang adapters; dimers also form"),
            ("4  bead clean-up", [("adapter", 52, "p5"), ("insert", 190, "ins"),
                                  ("adapter", 52, "p7")], "free adapter removed; dimers partly"),
            ("5  PCR with index primers", [("P5 i5 R1", 64, "p5"), ("insert", 190, "ins"),
                                           ("R2 i7 P7", 64, "p7")], "indexes and flow-cell ends added")]
    for i, (lab, parts, note) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(40, y + 15, lab, 13, INK))
        s, xe = chain(240, y, parts)
        out.append(s)
        out.append(t(560, y + 15, note, 12, MUTE))
    out.append(t(40, 238, "Ask at every step: what is on each 5' and 3' end, and which end "
                          "can the next enzyme use?", 14, HOT))
    return svg(900, 258, "".join(out))


def fig_walk_rna():
    out = [t(40, 26, "Same exercise for RNA: single-cell full-length cDNA (Smart-seq2 style).",
             14, INK)]
    rows = [("1  mRNA", [("5' cap ... mRNA ...", 150, "insA"), ("AAAA", 40, "ad")], "poly(A) tail at the 3' end"),
            ("2  RT with oligo-dT", [("5' cap ... mRNA ...", 150, "insA"), ("AAAA", 40, "ad"),
                                     ("adapter", 52, "p7")], "first-strand cDNA grows toward the 5' end"),
            ("3  template switch", [("TSO", 42, "p5"), ("cDNA", 150, "ins"), ("TTTT", 40, "ad"),
                                    ("adapter", 52, "p7")], "5' adapter added by the TSO"),
            ("4  PCR (pre-amplify)", [("adapter", 52, "p5"), ("cDNA", 150, "ins"),
                                      ("adapter", 52, "p7")], "one primer pair amplifies all"),
            ("5  tagment, index PCR", [("P5 i5 R1", 64, "p5"), ("cDNA piece", 110, "ins"),
                                       ("R2 i7 P7", 64, "p7")], "Tn5 cuts the cDNA; index PCR completes")]
    for i, (lab, parts, note) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(40, y + 15, lab, 13, INK))
        s, xe = chain(240, y, parts)
        out.append(s)
        out.append(t(560, y + 15, note, 12, MUTE))
    out.append(t(40, 238, "The tricks you meet: template switching, pre-amplification, "
                          "tagmentation, truncated adapters.", 14, HOT))
    return svg(900, 258, "".join(out))


def fig_annotate():
    out = [t(40, 26, "Annotate: paste a sequence, see which known primer and adapter parts "
                     "it contains (illustration).", 14, INK)]
    parts = [("AATGATACGGCGACCACCGAGATCTACAC", TOP), ("TATAGCCT", VIO),
             ("ACACTCTTTCCCTACACGACGCTCTTCCGATCT", HOT), ("GGCATTACCGTA", MUTE)]
    x = 40
    for s, c in parts:
        sv, w = small(x, 64, s, c, 11)
        out.append(sv)
        x += w
    # table
    out.append(t(40, 104, "found", 12.5, MUTE))
    rows = [("1-29", "P5 flow-cell sequence", TOP), ("30-37", "no fixed match (an index)", VIO),
            ("38-70", "Read 1 sequencing primer site", HOT), ("71-82", "insert: no match", MUTE)]
    for i, (pos, name, c) in enumerate(rows):
        y = 124 + i * 22
        out.append(box(40, y - 13, 6, 6, "", c, c, r=1))
        out.append(t(60, y, pos, 12.5, INK))
        out.append(t(130, y, name, 12.5, c))
    out.append(t(40, 226, "Matches are exact, on both strands, and list protocols that share "
                          "the part. A shared part does not prove the protocol.", 13.5, INK))
    out.append(t(40, 248, "Use it on an unknown read, a primer from a paper, or the "
                          "start of a FASTQ file.", 13.5, MUTE))
    return svg(700, 268, "".join(out))


def fig_anneal():
    out = [t(40, 26, "Anneal: give two oligos, see where they can pair, antiparallel "
                     "(illustration).", 14, INK)]
    s1 = "ACACTCTTTCCCTACACGACGCTCTTCCGATCT"
    s2 = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"
    pair_top = s1[-13:]
    bot_p = s2[:13][::-1]
    check_pairing(pair_top, bot_p)
    rest = s2[13:][::-1]
    x, y = 90, 80
    a, wa = seq(x + DX, y, s1, TOP)
    b, wb = seq(x, y + 30, rest, MUTE)
    c, _ = seq(x + len(rest) * DX, y + 30, bot_p, BOT)
    out += [a, b, c, pairs(x + (1 + 20) * DX, y, y + 30, pair_top, bot_p) if False else ""]
    for i in range(13):
        cx = x + (21 + i) * DX + 4
        out.append(line(cx, y + 4, cx, y + 19, HOT, 1.2))
    out.append(t(x - 10, y, "5'", 13, MUTE, anchor="end"))
    out.append(t(x - 10, y + 30, "3'", 13, MUTE, anchor="end"))
    out.append(t(x + 34 * DX + 8, y + 30, "5'", 13, MUTE))
    out.append(t(x + 34 * DX + 8, y, "3'", 13, MUTE))
    out.append(t(x + 27.5 * DX, y - 22, "13 bases pair", 12.5, HOT, anchor="middle"))
    out.append(t(x + 10 * DX, y + 62, "unpaired remainder of oligo 2", 12.5, MUTE, anchor="middle"))
    out.append(t(40, 186, "Shows every antiparallel span of at least the length you set, linear "
                          "or as a padlock, and exports a drawing.", 13.5, INK))
    out.append(t(40, 208, "It reports possible pairing, not whether the enzyme will extend "
                          "or ligate it: you decide that.", 13.5, MUTE))
    return svg(700, 228, "".join(out))


def fig_samplesheet():
    out = [t(40, 26, "Sample sheet: paste the index primers, read off the index each sample "
                     "carries (illustration).", 14, INK)]
    heads = [("Sample_ID", 40), ("primer 1 (contains i7)", 140), ("index (i7)", 500),
             ("primer 2 (contains i5)", 140), ("index2 (i5)", 500)]
    out.append(t(40, 56, "Sample_ID", 12, MUTE))
    out.append(t(120, 56, "i7 oligo, 5' to 3'", 12, MUTE))
    out.append(t(570, 56, "index", 12, MUTE))
    o1 = ("CAAGCAGAAGACGGCATACGAGAT", "CGAGTAAT", "GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT")
    x = 120
    for s, c in zip(o1, (MUTE, HOT, MUTE)):
        sv, w = small(x, 82, s, c, 10)
        out.append(sv)
        x += w
    out.append(t(40, 82, "S1", 12.5, INK))
    out.append(t(570, 82, "ATTACTCG", 12.5, HOT, family=MONO))
    out.append(t(40, 120, "S2", 12.5, INK))
    out.append(t(120, 120, "i5 oligo, 5' to 3'", 12, MUTE))
    o2 = ("AATGATACGGCGACCACCGAGATCTACAC", "TATAGCCT", "ACACTCTTTCCCTACACGACGCTCTTCCGATCT")
    x = 120
    for s, c in zip(o2, (MUTE, HOT, MUTE)):
        sv, w = small(x, 142, s, c, 10)
        out.append(sv)
        x += w
    out.append(t(570, 142, "TATAGCCT or AGGCTATA", 12.5, HOT, family=MONO))
    out.append(t(40, 194, "i7 is read as the reverse complement of what sits in the oligo; "
                          "i5 depends on the instrument.", 13.5, INK))
    out.append(t(40, 216, "Pick the instrument first: the same oligo gives a different "
                          "sample-sheet entry on different machines.", 13.5, BAD))
    return svg(760, 236, "".join(out))


# ================================================================ failure modes

def fig_f_dimer():
    out = [t(40, 26, "Adapter dimer: the read starts in the adapter, and stays there.", 14, INK)]
    s, xe = chain(120, 54, [("P5 i5 R1", 80, "p5"), ("R2 i7 P7", 80, "p7")], h=26)
    out.append(s)
    out.append(arrow(120, 108, 200, HOT))
    out.append(t(206, 112, "Read 1: adapter sequence at once", 12.5, HOT))
    out.append(arrow(280, 132, 200, HOT))
    out.append(t(290, 136, "Read 2: same", 12.5, HOT))
    out.append(t(40, 170, "Signature: a 120-140 bp peak; reads that are all adapter; high "
                          "adapter content from the first base.", 13.5, INK))
    out.append(t(40, 192, "Control that tells you: a no-insert (adapter-only) reaction makes "
                          "the dimer without any sample.", 13.5, MUTE))
    return svg(700, 212, "".join(out))


def fig_f_onesided():
    out = [t(40, 26, "One-sided products cannot bridge, so qPCR misses them and the sequencer "
                     "never reads them.", 14, INK)]
    rows = [("two adapters, different", [("P5", 40, "p5"), ("insert", 150, "ins"), ("P7", 40, "p7")], "ok"),
            ("same adapter at both ends", [("P5", 40, "p5"), ("insert", 150, "ins"), ("P5", 40, "p5")], "x"),
            ("one adapter only", [("P5", 40, "p5"), ("insert", 150, "ins")], "x"),
            ("no adapter", [("insert", 150, "ins")], "x")]
    for i, (lab, parts, v) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(40, y + 15, lab, 12.5, INK))
        s, xe = chain(240, y, parts)
        out.append(s)
        out.append(tick(xe + 24, y + 12) if v == "ok" else cross(xe + 24, y + 11))
    out.append(t(40, 204, "Signature: Qubit much higher than qPCR; a clean trace that "
                          "gives too few clusters.", 13.5, INK))
    out.append(t(40, 226, "Control: quantify by qPCR, and compare with Qubit-derived molarity.",
                 13.5, MUTE))
    return svg(700, 246, "".join(out))


def fig_f_chimera():
    out = [t(40, 26, "A chimera joins pieces that were never together in the cell.", 14, INK)]
    s, xe = chain(120, 54, [("P5", 36, "p5"), ("piece A (chr 1)", 120, "insA"),
                            ("piece B (chr 7)", 120, "insB"), ("P7", 36, "p7")], h=26)
    out.append(s)
    out.append(line(120 + 36 + 120, 46, 120 + 36 + 120, 90, HOT, 1.6, dash="3 3"))
    out.append(t(120 + 156, 106, "junction: a read that maps to both", 12.5, HOT, anchor="middle"))
    out.append(t(40, 142, "Made by: ligation of two inserts; a partial PCR product priming on "
                          "another template; template switching.", 13.5, INK))
    out.append(t(40, 164, "Signature: split reads at no known breakpoint, at microhomologies, "
                          "more at higher cycles.", 13.5, INK))
    out.append(t(40, 186, "Control: mix human and mouse material before the step: a read "
                          "with both species is a chimera.", 13.5, MUTE))
    return svg(700, 206, "".join(out))


def fig_f_hopping():
    out = [t(40, 26, "Index hopping: a read gets the wrong index. Unique dual indexes make "
                     "it visible.", 14, INK)]
    for g, (title, used) in enumerate([("combinatorial dual: every cell is a sample",
                                          lambda i, j: True),
                                         ("unique dual: only the diagonal is a sample",
                                          lambda i, j: i == j)]):
        x0 = 60 + g * 330
        out.append(t(x0, 46, title, 12.5, INK))
        for i in range(3):
            for j in range(3):
                x, y = x0 + 20 + j * 40, 72 + i * 30
                if used(i, j):
                    out.append(box(x, y, 34, 24, "S", PB, TOP, 11, TOP, r=3))
                else:
                    out.append(box(x, y, 34, 24, "", "none", "#d5d8db", r=3))
        out.append(t(x0 + 8, 88, "i5", 11, MUTE))
        out.append(t(x0 + 20 + 1 * 40 + 17, 66, "i7", 11, MUTE, anchor="middle"))
    out.append(t(60, 178, "A hopped read lands in a different cell. If that cell is "
                          "another sample, you cannot tell.", 13.5, BAD))
    out.append(t(60, 198, "If it is an unused cell, the read is discarded or counted as "
                          "hopping.", 13.5, OK))
    out.append(t(40, 226, "Signature: reads in an empty well; sample-to-sample leakage.", 13.5, INK))
    out.append(t(40, 248, "Control: an empty or blank library in the pool, unique dual "
                          "indexes, remove free adapter [Costello et al. 2018].", 13.5, MUTE))
    return svg(720, 268, "".join(out))


def fig_f_lowdiv():
    out = [t(40, 26, "Low complexity: every cluster shows the same base in the same cycle.", 14, INK)]
    cols = {"A": OK, "C": TOP, "G": HOT, "T": BAD}
    for g, (title, mixed) in enumerate([("diverse library", True), ("amplicon library", False)]):
        x0 = 60 + g * 330
        out.append(t(x0, 52, title, 12.5, INK))
        shared = "GGATCAGTACGT"
        for cyc in range(12):
            x = x0 + cyc * 22
            if mixed:
                y = 62
                for b, f in zip("ACGT", (0.3, 0.2, 0.2, 0.3)):
                    out.append(f'<rect x="{x}" y="{y}" width="18" height="{f*80:.0f}" fill="{cols[b]}" opacity="0.5"/>')
                    y += f * 80
            else:
                out.append(f'<rect x="{x}" y="62" width="18" height="80" fill="{cols[shared[cyc]]}" opacity="0.5"/>')
        out.append(t(x0, 160, "cycle 1 ... 12", 11, MUTE))
    out.append(t(40, 200, "Signature: per-cycle base composition far from balanced; poor "
                          "quality and cluster loss in the first cycles.", 13.5, INK))
    out.append(t(40, 222, "Control: PhiX spike-in, staggered primers, or a mixed amplicon "
                          "pool.", 13.5, MUTE))
    return svg(720, 242, "".join(out))


def fig_f_overamp():
    out = [t(40, 26, "Over-amplification: more cycles, more duplicates, more bias "
                     "(schematic).", 14, INK)]
    x0, y0, w, h = 70, 52, 240, 110
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    pts = " ".join(f"{x0 + w*i/40:.1f},{y0 + h - h*(i/40)**2.2:.1f}" for i in range(41))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{BAD}" stroke-width="2.4"/>')
    out.append(t(x0 + w / 2, y0 + h + 22, "PCR cycles", 11, MUTE, anchor="middle"))
    out.append(t(x0 - 6, y0 + 8, "duplicates", 11, MUTE, anchor="end"))
    x1 = 400
    out.append(line(x1, y0 + h, x1 + w, y0 + h, MUTE, 1.2))
    out.append(line(x1, y0, x1, y0 + h, MUTE, 1.2))
    out.append(line(x1 + 10, y0 + 40, x1 + w - 10, y0 + 40, OK, 2.2))
    pts = " ".join(f"{x1 + 10 + (w-20)*i/40:.1f},{y0 + 40 + 40*math.sin(math.pi*i/40)*-1 + 55*abs((i-20)/20)**2:.1f}" for i in range(41))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{BAD}" stroke-width="2.4"/>')
    out.append(t(x1 + w / 2, y0 + h + 22, "GC content of the region", 11, MUTE, anchor="middle"))
    out.append(t(x1 - 6, y0 + 8, "coverage", 11, MUTE, anchor="end"))
    out.append(t(x1 + w - 4, y0 + 34, "ideal: flat", 11, OK, anchor="end"))
    out.append(t(40, 212, "Signature: high duplicate rate, bowed coverage against GC, a "
                          "high-size shoulder on the trace.", 13.5, INK))
    out.append(t(40, 234, "Control: titrate input or cycles on a reference sample; use UMIs to "
                          "separate duplicates from real depth.", 13.5, MUTE))
    return svg(720, 254, "".join(out))


def fig_f_offtarget():
    out = [t(40, 26, "Off-target ligation: the ligase joins what it likes, not what you "
                     "meant (schematic).", 14, INK)]
    x0, y0, w, h = 70, 50, 300, 100
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    effs = [0.9, 0.35, 0.6, 0.2]
    for i, (b, e) in enumerate(zip("ACGT", effs)):
        xb = x0 + 20 + i * 70
        out.append(f'<rect x="{xb}" y="{y0 + h - e*h}" width="44" height="{e*h}" fill="{TOP}" opacity="0.4"/>')
        out.append(t(xb + 22, y0 + h + 16, b, 12, INK, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 34, "base at the ligating end", 11, MUTE, anchor="middle"))
    out.append(t(x0 - 6, y0 + 8, "efficiency", 11, MUTE, anchor="end"))
    out.append(t(420, 80, "Result: abundance in the library", 13, INK))
    out.append(t(420, 98, "reflects the end sequence, not", 13, INK))
    out.append(t(420, 116, "the amount in the cell.", 13, INK))
    out.append(t(40, 208, "Also: ligation to carry-over nucleic acid, to the wrong end, or to "
                          "a second insert (chimera).", 13.5, INK))
    out.append(t(40, 230, "Control: a spike-in mix of known equimolar sequences shows the "
                          "bias; random ligating ends average it out.", 13.5, MUTE))
    return svg(720, 250, "".join(out))


def fig_controls():
    out = [t(40, 26, "Which control exposes which failure.", 14, INK)]
    cols = ["no template", "adapter only", "empty well", "reference", "spike-in / PhiX",
            "species mix", "unique dual", "UMI", "titration"]
    rows = [("adapter dimers", [0, 1]), ("one-sided products", [3]),
            ("chimeras", [3, 5]), ("index hopping", [2, 6]),
            ("low complexity", [3, 4]), ("over-amplification", [7, 8]),
            ("off-target ligation", [0, 3, 4])]
    x0 = 190
    for j, c in enumerate(cols):
        out.append(t(x0 + j * 62 + 24, 52, c.split(" ")[0], 11, MUTE, anchor="middle"))
        if " " in c:
            out.append(t(x0 + j * 62 + 24, 64, c.split(" ", 1)[1], 11, MUTE, anchor="middle"))
    for i, (r, hits) in enumerate(rows):
        y = 84 + i * 28
        out.append(t(40, y + 4, r, 13, INK))
        for j in range(len(cols)):
            out.append(line(x0, y + 12, x0 + 9 * 62, y + 12, "#eceef0", 1) if j == 0 else "")
            if j in hits:
                out.append(dot(x0 + j * 62 + 24, y, 7, OK))
            else:
                out.append(dot(x0 + j * 62 + 24, y, 2, "#c9ccd0"))
    out.append(t(40, 300, "Dots mark the controls that tell the failure apart from the "
                          "others. One control often serves several.", 13.5, INK))
    return svg(760, 320, "".join(out))


def fig_diagnosis():
    out = [t(40, 26, "From symptom to cause: the first thing to check.", 14, INK)]
    rows = [("peak at 130 bp on the trace", "adapter dimers", "adapter-only control; clean up"),
            ("Qubit high, qPCR low", "one-sided or no-adapter DNA", "trace; re-quantify by qPCR"),
            ("reads with two mappings", "chimeras", "species-mix control; fewer cycles"),
            ("reads in the empty well", "index hopping", "unique dual indexes; free adapter"),
            ("first cycles all one base", "low complexity", "PhiX; stagger the primers"),
            ("duplicates high, GC bowed", "over-amplification", "titrate cycles; add UMIs")]
    for i, (a, b, c) in enumerate(rows):
        y = 54 + i * 32
        out.append(mbox(40, y, 200, 24, [a], "none", MUTE, 11.5))
        out.append(arrow(246, y + 12, 272, MUTE, head=4))
        out.append(mbox(278, y, 170, 24, [b], PO, HOT, 12, HOT))
        out.append(arrow(454, y + 12, 480, MUTE, head=4))
        out.append(t(486, y + 16, c, 12, INK))
    out.append(t(40, 258, "One symptom can have two causes: use a second observation to "
                          "separate them before changing the protocol.", 13.5, MUTE))
    return svg(760, 278, "".join(out))


def fig_capstone():
    out = [t(40, 26, "Worked outline: which regulatory regions are open in 500 human CD34+ "
                     "cells? Closest protocol: Omni-ATAC.", 14, INK)]
    rows = [("1  nuclei", [("nucleus, chromatin intact", 230, "ins")], "permeabilise, keep nuclei"),
            ("2  Tn5 + adapters", [("R1 stub", 50, "ad"), ("open DNA", 130, "ins"), ("R2 stub", 50, "ad")],
             "tagmentation cuts and tags at once"),
            ("3  fill, 5 cycles", [("R1 stub", 50, "ad"), ("open DNA", 130, "ins"), ("R2 stub", 50, "ad")],
             "gap fill, short PCR, aliquot to qPCR"),
            ("4  index PCR", [("P5 i5 R1", 64, "p5"), ("open DNA", 130, "ins"), ("R2 i7 P7", 64, "p7")],
             "extra cycles from the qPCR"),
            ("5  read", [("R1 50", 80, "hot"), ("i7 8", 40, "idx"), ("i5 8", 40, "idx"),
                         ("R2 50", 80, "hot")], "cycles per read: 50 / 8 / 8 / 50")]
    for i, (lab, parts, note) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(40, y + 15, lab, 13, INK))
        s, xe = chain(220, y, parts)
        out.append(s)
        out.append(t(520, y + 15, note, 12, MUTE))
    out.append(t(40, 244, "Controls: no-transposase, deproteinised DNA, a reference cell line, "
                          "dual indexes. Expected failures: mitochondrial reads, over-tagmentation.",
                 13, INK))
    return svg(900, 264, "".join(out))


build(__file__, [
    ("blocks", fig_blocks),
    ("walk-dna", fig_walk_dna),
    ("walk-rna", fig_walk_rna),
    ("annotate", fig_annotate),
    ("anneal", fig_anneal),
    ("samplesheet", fig_samplesheet),
    ("f-dimer", fig_f_dimer),
    ("f-onesided", fig_f_onesided),
    ("f-chimera", fig_f_chimera),
    ("f-hopping", fig_f_hopping),
    ("f-lowdiv", fig_f_lowdiv),
    ("f-overamp", fig_f_overamp),
    ("f-offtarget", fig_f_offtarget),
    ("controls", fig_controls),
    ("diagnosis", fig_diagnosis),
    ("capstone", fig_capstone),
])
