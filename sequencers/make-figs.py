#!/usr/bin/env python3
"""Figures for the sequencers unit.  Run: python3 sequencers/make-figs.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

# ---------------------------------------------------------------- A2a figures

def fig_sanger():
    out = []
    out.append(t(40, 30, "one template, one primer", 13.5, MUTE))
    out.append(line(60, 56, 300, 56, TOP, 2.4))
    out.append(t(50, 60, "3'", 11.5, MUTE, anchor="end"))
    out.append(line(60, 44, 110, 44, HOT, 2.4))
    out.append(t(85, 34, "primer", 11.5, HOT, anchor="middle"))
    # terminated products of increasing length
    for i, c in enumerate([OK, HOT, BOT, TOP, OK, HOT]):
        y = 84 + i * 15
        out.append(line(60, y, 118 + i * 28, y, MUTE, 2))
        out.append(dot(118 + i * 28, y, 4.5, c))
    out.append(t(40, 190, "every chain stops at one ddNTP", 13.5, MUTE))
    # chromatogram
    bx = 360
    out.append(t(bx, 30, "separate by length, read the colours", 13.5, MUTE))
    import math
    pts = []
    cols = [OK, HOT, BOT, TOP, OK, HOT]
    for i, c in enumerate(cols):
        cx = bx + 20 + i * 36
        p = " ".join(f"{cx-16+j*2.0:.0f},{120-26*math.exp(-((j-16)/5.0)**2):.0f}" for j in range(33))
        out.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="2"/>')
        out.append(t(cx, 140, "ACGT"[i % 4], 13, c, anchor="middle", family=MONO))
    out.append(line(bx, 120, bx + 230, 120, MUTE, 1))
    out.append(t(bx, 190, "700-1000 bases, one molecule species", 13.5, MUTE))
    out.append(t(40, 224, "A mixture would give overlapping peaks: Sanger needs every molecule "
                          "in the tube to be the same.", 14, INK))
    return svg(660, 244, "".join(out))


def fig_universal_ends():
    out = [t(40, 28, "Unknown inserts, identical ends — so one primer reads them all.", 14, INK)]
    for i, w in enumerate([150, 95, 210]):
        y = 62 + i * 46
        x = 60
        out.append(box(x, y, 52, 20, "P5", "#e8eef5", TOP, 12, TOP))
        out.append(box(x + 52, y, w, 20, "insert " + "ABC"[i], "none", MUTE, 12, MUTE))
        out.append(box(x + 52 + w, y, 52, 20, "P7", "#f5eae6", BAD, 12, BAD))
        out.append(arrow(x + 16, y + 32, x + 62, HOT))
        out.append(t(x + 52 + w + 64, y + 15, "same primer, same site", 12, MUTE))
    out.append(t(40, 212, "This is the whole reason a library exists: the sequencer only knows "
                          "how to read the ends you gave it.", 14, HOT))
    return svg(680, 232, "".join(out))


def fig_flowcell():
    out = [t(40, 28, "The flow cell is a lawn of two oligos.", 14, INK)]
    y = 150
    out.append(f'<rect x="40" y="{y}" width="600" height="14" fill="#dfe3e6"/>')
    for i in range(24):
        x = 52 + i * 25
        c = TOP if i % 2 == 0 else BAD
        out.append(vtick(x, y, y - 26, c, 2.6))
    out.append(t(52, y + 32, "P5", 12.5, TOP))
    out.append(t(77, y + 32, "P7", 12.5, BAD))
    out.append(t(120, y + 32, "grafted by their 5' ends, so the 3' ends are free to be extended",
                 12.5, MUTE))
    # library molecule
    out.append(line(220, 62, 420, 62, MUTE, 3))
    out.append(box(176, 52, 46, 20, "P5'", "#e8eef5", TOP, 12, TOP))
    out.append(box(418, 52, 46, 20, "P7'", "#f5eae6", BAD, 12, BAD))
    out.append(t(320, 44, "insert", 12.5, MUTE, anchor="middle"))
    out.append(arrow(200, 96, 200, TOP))
    out.append(f'<path d="M 199 80 L 199 112" stroke="{TOP}" stroke-width="1.4" '
               f'stroke-dasharray="4 3"/>')
    out.append(t(214, 104, "anneals to a P5 lawn oligo", 12.5, TOP))
    out.append(t(40, 214, "A molecule with the same end at both ends, or with only one, "
                          "cannot bridge — and never forms a cluster.", 14, HOT))
    return svg(680, 234, "".join(out))


def fig_bridge():
    out = []
    titles = ["1. copy, keep the copy", "2. bend over and bridge", "3. repeat → a cluster"]
    for p in range(3):
        x0 = 36 + p * 215
        out.append(t(x0 + 95, 28, titles[p], 13, INK, anchor="middle"))
        out.append(f'<rect x="{x0}" y="150" width="190" height="10" fill="#dfe3e6"/>')
        if p == 0:
            out.append(vtick(x0 + 40, 150, 70, TOP, 2.6))
            out.append(t(x0 + 46, 64, "copied strand, now attached", 11.5, MUTE))
        elif p == 1:
            out.append(f'<path d="M {x0+40} 150 C {x0+40} 80, {x0+140} 80, {x0+140} 150" '
                       f'fill="none" stroke="{TOP}" stroke-width="2.6"/>')
            out.append(vtick(x0 + 140, 150, 142, BAD, 2.6))
            out.append(t(x0 + 90, 92, "free end finds a", 11.5, MUTE, anchor="middle"))
            out.append(t(x0 + 90, 106, "P7 oligo nearby", 11.5, MUTE, anchor="middle"))
        else:
            for i in range(9):
                xx = x0 + 18 + i * 19
                out.append(vtick(xx, 150, 150 - (34 + (i % 3) * 8),
                                 TOP if i % 2 else BAD, 2.4))
            out.append(t(x0 + 95, 70, "~1000 copies, all identical", 11.5, MUTE, anchor="middle"))
    out.append(t(36, 196, "Amplification is local: the copies stay where they were made, which "
                          "is why one cluster gives one read.", 14, INK))
    return svg(690, 216, "".join(out))


def fig_linearise():
    out = [t(40, 28, "Before reading, make every strand in the cluster point the same way.",
             14, INK)]
    y = 120
    for panel, lab in enumerate(["mixed orientations", "cut and wash away one kind",
                                 "anneal the Read 1 primer"]):
        x0 = 40 + panel * 215
        out.append(f'<rect x="{x0}" y="{y}" width="190" height="10" fill="#dfe3e6"/>')
        out.append(t(x0 + 95, 54, lab, 12.5, INK, anchor="middle"))
        for i in range(8):
            xx = x0 + 16 + i * 22
            fwd = i % 2 == 0
            if panel == 0 or fwd:
                out.append(vtick(xx, y, y - 40, TOP if fwd else BAD, 2.4))
            if panel == 1 and not fwd:
                out.append(t(xx, y - 14, "×", 13, BAD, anchor="middle"))
        if panel == 2:
            out.append(arrow(x0 + 150, y - 48, x0 + 178, HOT))
            out.append(t(x0 + 95, y - 56, "R1 primer", 12, HOT, anchor="middle"))
    out.append(t(40, 196, "Only one strand is read at a time. Everything else is removed or "
                          "blocked at its 3' end.", 14, MUTE))
    return svg(690, 216, "".join(out))


def fig_sbs():
    out = [t(40, 28, "One cycle = one base, on every cluster at once.", 14, INK)]
    steps = [("add", "all four bases,\neach dye-labelled and\n3'-blocked"),
             ("image", "one colour per cluster\ntells you the base"),
             ("cleave", "remove the dye and\nthe 3' block"),
             ("repeat", "next cycle adds\nexactly one more base")]
    for i, (h, b) in enumerate(steps):
        x = 42 + i * 160
        out.append(box(x, 56, 132, 96, "", "#fbfbf9", MUTE))
        out.append(t(x + 66, 80, h, 14.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 66, 102 + j * 16, ln, 11.5, MUTE, anchor="middle"))
        if i < 3:
            out.append(arrow(x + 136, 104, x + 156, MUTE))
    out.append(t(40, 182, "The 3' block is what makes it stepwise: without it a polymerase "
                          "would run to the end and you would see nothing.", 14, INK))
    out.append(t(40, 206, "Read length is limited by how well the block and dye are removed — "
                          "errors accumulate, so quality falls with cycle number.", 13.5, MUTE))
    return svg(700, 226, "".join(out))


def fig_read_order():
    out = [t(36, 26, "Four reads, four primers, one molecule — in this order.", 14, INK)]
    y = 92
    segs = [("P5", 48, "#e8eef5", TOP), ("i5", 40, "#efe9f3", "#6b5b8a"),
            ("R1 site", 70, "#f1f1ee", MUTE), ("insert", 150, "none", MUTE),
            ("R2 site", 70, "#f1f1ee", MUTE), ("i7", 40, "#efe9f3", "#6b5b8a"),
            ("P7", 48, "#f5eae6", BAD)]
    x = 60
    pos = {}
    for name, w, fill, col in segs:
        out.append(box(x, y, w, 24, name, fill, col, 11.5, col))
        pos[name] = (x, w)
        x += w
    end = x
    # read arrows
    rx, rw = pos["R1 site"]
    out.append(arrow(rx + rw, y + 44, rx + rw + 120, HOT))
    out.append(t(rx + rw + 4, y + 62, "1  Read 1 → into the insert", 12, HOT))
    ix, iw = pos["i7"]
    out.append(arrow(ix + iw, y - 16, ix, "#6b5b8a"))
    out.append(t(ix + iw + 6, y - 12, "2  Index 1 (i7)", 12, "#6b5b8a"))
    jx, jw = pos["i5"]
    out.append(arrow(jx, y - 16, jx + jw, "#6b5b8a"))
    out.append(t(60, y - 28, "3  Index 2 (i5)", 12, "#6b5b8a"))
    sx, sw = pos["R2 site"]
    out.append(arrow(sx, y + 44, sx - 120, HOT))
    out.append(t(sx - 124, y + 62, "4  Read 2 ← from the other end", 12, HOT))
    out.append(t(36, 188, "The indexes are read because they are sequence like any other — "
                          "that is why a sample index must sit next to a primer site.", 14, INK))
    return svg(end + 60, 208, "".join(out))


def fig_pe_turnaround():
    out = [t(40, 26, "How the sequencer gets to the other end of the insert.", 14, INK)]
    steps = ["Read 1 and both\nindex reads are done",
             "strip the new strand;\nthe template bridges again",
             "copy it, then remove\nthe strand just read",
             "Read 2 primer anneals\nand reads the other end"]
    for i, s in enumerate(steps):
        x = 40 + i * 162
        out.append(box(x, 52, 142, 86, "", "#fbfbf9", MUTE))
        for j, ln in enumerate(s.split("\n")):
            out.append(t(x + 71, 86 + j * 17, ln, 11.5, INK, anchor="middle"))
        out.append(t(x + 71, 66, str(i + 1), 13, HOT, anchor="middle", weight="bold"))
        if i < 3:
            out.append(arrow(x + 146, 95, x + 164, MUTE))
    out.append(t(40, 168, "Read 2 is a fresh copy of the opposite strand — it is not the same "
                          "molecule read backwards.", 14, INK))
    out.append(t(40, 192, "This costs time and chemistry, which is why paired-end runs cost "
                          "more than single-end.", 13.5, MUTE))
    return svg(720, 212, "".join(out))


def fig_i5_orientation():
    out = [t(40, 26, "The i5 index is read in one of two directions, depending on the "
                     "instrument.", 14, INK)]
    rows = [("forward-strand workflow", "AGGATAGG", "AGGATAGG",
             "MiSeq, HiSeq 2000/2500, NovaSeq 6000 v1.0"),
            ("reverse-complement workflow", "AGGATAGG", "CCTATCCT",
             "iSeq, MiniSeq, NextSeq, HiSeq 3000/4000/X, NovaSeq 6000 v1.5, NovaSeq X")]
    for i, (name, written, read, instr) in enumerate(rows):
        y = 64 + i * 78
        out.append(t(50, y, name, 13.5, HOT, weight="bold"))
        out.append(t(50, y + 22, "ordered:", 12, MUTE))
        out.append(t(130, y + 22, written, 13.5, INK, family=MONO))
        out.append(t(250, y + 22, "sample sheet needs:", 12, MUTE))
        out.append(t(400, y + 22, read, 13.5, OK if written == read else BAD, family=MONO))
        out.append(t(50, y + 42, instr, 11.5, MUTE))
    out.append(t(40, 224, "The sample sheet is the file that tells the instrument which "
                          "index belongs to which sample.", 13, MUTE))
    out.append(t(40, 248, "Get this wrong and the run looks empty: every read lands in "
                          "Undetermined, the bin for reads matching no index.", 14, HOT))
    out.append(t(40, 272, "Always check the current instrument documentation — the lists "
                          "change with reagent versions.", 13, MUTE))
    return svg(700, 292, "".join(out))


def fig_readthrough():
    out = [t(40, 26, "If the insert is shorter than the read, the read runs into the adapter.",
             14, INK)]
    for i, (ins, lab) in enumerate([(230, "insert longer than the read — fine"),
                                    (90, "insert shorter — read-through")]):
        y = 70 + i * 86
        out.append(box(60, y, 60, 22, "adapter", "#f1f1ee", MUTE, 11, MUTE))
        out.append(box(120, y, ins, 22, "insert", "none", MUTE, 11.5, MUTE))
        out.append(box(120 + ins, y, 60, 22, "adapter", "#f1f1ee", MUTE, 11, MUTE))
        out.append(arrow(120, y + 38, 120 + 170, HOT))
        out.append(t(124, y + 56, "read, 150 bases", 11.5, HOT))
        if ins < 170:
            out.append(f'<rect x="{120+ins}" y="{y+30}" width="{170-ins}" height="16" '
                       f'fill="{BAD}" opacity="0.18"/>')
            out.append(t(120 + ins + 66, y + 56, "adapter bases — must be trimmed off",
                         11.5, BAD))
        out.append(t(330 if i == 0 else 350, y + 15, lab, 12.5, OK if i == 0 else BAD))
    out.append(t(40, 246, "Adapter content in a QC report is this, and it tells you your "
                          "fragment size, not your sequencing quality.", 14, INK))
    return svg(700, 266, "".join(out))


def fig_index_hopping():
    out = [t(40, 26, "Free adapter in the pool can give a read the wrong sample index.", 14, INK)]
    out.append(box(50, 54, 150, 56, "", "#fbfbf9", MUTE))
    out.append(t(125, 76, "pooled libraries", 12.5, INK, anchor="middle"))
    out.append(t(125, 96, "sample A  +  sample B", 12, MUTE, anchor="middle"))
    out.append(t(125, 128, "+ leftover free adapter", 12, BAD, anchor="middle"))
    out.append(arrow(210, 86, 250, MUTE))
    out.append(box(260, 54, 180, 56, "", "#fbfbf9", MUTE))
    out.append(t(350, 78, "on the flow cell the free", 12, INK, anchor="middle"))
    out.append(t(350, 96, "index primes a molecule", 12, INK, anchor="middle"))
    out.append(arrow(450, 86, 490, MUTE))
    out.append(box(500, 54, 150, 56, "", "#fdf3f0", BAD))
    out.append(t(575, 78, "sample A read filed", 12, BAD, anchor="middle"))
    out.append(t(575, 96, "under sample B", 12, BAD, anchor="middle"))
    out.append(t(40, 162, "Worse on patterned flow cells with ExAmp chemistry. "
                          "Typically 0.1–2% of reads.", 13.5, MUTE))
    out.append(t(40, 192, "Fix: unique dual indexes — a hopped read then carries a pair that "
                          "belongs to no sample, so it can be discarded.", 14, OK))
    out.append(t(40, 216, "And clean up thoroughly: free adapter is the fuel.", 13.5, MUTE))
    return svg(700, 236, "".join(out))


def fig_diversity():
    out = [t(40, 26, "The instrument needs all four colours in the first cycles.", 14, INK)]
    import random
    random.seed(7)
    cols = {"A": OK, "C": TOP, "G": HOT, "T": BOT}
    for panel, (lab, kind) in enumerate([("a varied library", "mixed"),
                                         ("an amplicon library", "same")]):
        x0 = 60 + panel * 320
        out.append(t(x0 + 110, 56, lab, 13, INK, anchor="middle"))
        for c in range(10):
            x = x0 + c * 22
            y = 150
            if kind == "mixed":
                fr = [0.25] * 4
            else:
                fr = [1.0, 0, 0, 0] if c < 6 else [0.25] * 4
            for b, f in zip("ACGT", fr):
                h = f * 72
                if h > 0:
                    out.append(f'<rect x="{x}" y="{y-h:.0f}" width="16" height="{h:.0f}" '
                               f'fill="{cols[b]}" opacity="0.85"/>')
                y -= h
            out.append(t(x + 8, 166, str(c + 1), 10, MUTE, anchor="middle"))
        out.append(t(x0 + 110, 186, "cycle", 11.5, MUTE, anchor="middle"))
    out.append(t(40, 216, "All-identical early bases blind the instrument: it cannot tell "
                          "clusters apart or set its colour thresholds.", 14, INK))
    out.append(t(40, 240, "Fixes: spike in PhiX, order primers with 0–3 extra bases so "
                          "libraries are out of phase, or use a varied index set.", 13.5, OK))
    return svg(700, 260, "".join(out))


# ---------------------------------------------------------------- A2b figures

def fig_dnbseq():
    out = [t(40, 26, "MGI: make a circle, copy it hundreds of times into one ball.", 14, INK)]
    steps = [("adapters +\nsplint", "ligate the ends\ntogether"),
             ("ssDNA circle", "exonuclease removes\nanything still linear"),
             ("rolling circle", "phi29 copies round\nand round"),
             ("DNA nanoball", "one head-to-tail\nconcatemer, folded up")]
    for i, (h, b) in enumerate(steps):
        x = 42 + i * 162
        out.append(box(x, 52, 140, 100, "", "#fbfbf9", MUTE))
        out.append(t(x + 70, 76, h.split("\n")[0], 13, HOT, anchor="middle", weight="bold"))
        if "\n" in h:
            out.append(t(x + 70, 92, h.split("\n")[1], 13, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 70, 114 + j * 16, ln, 11.5, MUTE, anchor="middle"))
        if i < 3:
            out.append(arrow(x + 144, 102, x + 160, MUTE))
    out.append(t(40, 182, "No PCR on the flow cell, so no PCR duplicates from clustering and "
                          "no index hopping of the Illumina kind.", 14, OK))
    out.append(t(40, 206, "The balls sit on a patterned array and are read by probe-anchor "
                          "ligation: an anchor oligo binds the", 13.5, MUTE))
    out.append(t(40, 224, "adapter, then a labelled probe is ligated beside it — no "
                          "polymerase copies the template.", 13.5, MUTE))
    return svg(710, 244, "".join(out))


def fig_other_shortread():
    out = [t(30, 26, "Three other ways to read a short library.", 14, INK)]

    panels = [
        ("Element AVITI \u2014 avidity",
         ["a probe carrying many copies of one base",
          "grips a polony: a clonal cluster of copies"],
         ["bright signal from little reagent;",
          "binding is separated from incorporation"]),
        ("Ultima \u2014 flow-based, no terminator",
         ["beads on an open wafer; one base flows",
          "at a time and adds until it runs out"],
         ["signal height counts homopolymer length,",
          "so homopolymers are the weak spot"]),
        ("Ion Torrent \u2014 no optics at all",
         ["each well sits on a transistor that senses",
          "the H+ released when a base is added"],
         ["bases also flow one at a time, so it shares",
          "Ultima's homopolymer problem"]),
    ]
    for i, (title, mute, ink) in enumerate(panels):
        x = 30 + i * 318
        out.append(box(x, 50, 300, 118, "", "#fbfbf9", MUTE))
        c = x + 150
        out.append(t(c, 74, title, 12.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(mute):
            out.append(t(c, 98 + j * 16, ln, 11, MUTE, anchor="middle"))
        for j, ln in enumerate(ink):
            out.append(t(c, 138 + j * 16, ln, 11, INK, anchor="middle"))

    out.append(t(30, 198, "All three read short, accurate reads, and all three want the same "
                          "thing from you: a library with the platform's own ends.", 14, INK))
    out.append(t(30, 222, "The chemistry differs; the library design problem does not.",
                 13.5, MUTE))
    return svg(1000, 242, "".join(out))


def fig_smrtbell():
    out = [t(40, 26, "PacBio: close the duplex into a loop so it can be read forever.", 14, INK)]
    b, w = duplex(120, 70, "ATGCTTAGCCA", "TACGAATCGGT", labels=False)
    out.append(b)
    for xx, d in ((120, -1), (120 + w, 1)):
        out.append(f'<path d="M {xx} 70 C {xx + d*44} 70, {xx + d*44} 100, {xx} 100" '
                   f'fill="none" stroke="{HOT}" stroke-width="2.6"/>')
    out.append(t(76, 126, "hairpin", 12, HOT, anchor="middle"))
    out.append(t(120 + w + 44, 126, "hairpin", 12, HOT, anchor="middle"))
    out.append(t(120 + w / 2, 142, "insert", 12, MUTE, anchor="middle"))
    out.append(t(40, 176, "Both strands and both adapters are now one covalently closed "
                          "single-stranded circle.", 14, INK))
    out.append(t(40, 200, "The polymerase can go round it as many times as the insert is "
                          "short enough to allow.", 13.5, MUTE))
    out.append(t(40, 230, "A nick anywhere in the insert ends the read: input DNA quality "
                          "matters more here than for short reads.", 13.5, HOT))
    return svg(660, 250, "".join(out))


def fig_zmw():
    out = [t(40, 26, "One polymerase, watched in real time.", 14, INK)]
    out.append(f'<rect x="60" y="56" width="150" height="96" fill="#eceff1" stroke="{MUTE}"/>')
    out.append(f'<rect x="96" y="56" width="78" height="96" fill="#ffffff" stroke="{MUTE}"/>')
    out.append(t(135, 48, "zero-mode waveguide", 11.5, MUTE, anchor="middle"))
    out.append(dot(135, 140, 9, TOP))
    out.append(t(135, 168, "polymerase fixed at the bottom", 11.5, MUTE, anchor="middle"))
    out.append(t(135, 184, "only this tiny volume is lit", 11.5, MUTE, anchor="middle"))
    # trace
    x0 = 260
    out.append(line(x0, 140, x0 + 360, 140, MUTE, 1))
    import math
    for i, (c, w) in enumerate([(OK, 16), (HOT, 15), (TOP, 16), (BOT, 15), (OK, 44), (HOT, 16)]):
        cx = x0 + 34 + i * 58 + (0 if i < 4 else 14)
        p = " ".join(f"{cx-w/2+j*(w/16.0):.0f},{140-42*math.exp(-((j-8)/3.2)**2):.0f}"
                     for j in range(17))
        out.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="2.2"/>')
    out.append(t(x0, 60, "each base gives a flash of its own colour", 12, INK))
    out.append(t(x0 + 250, 96, "a long gap", 11.5, HOT))
    out.append(t(x0 + 250, 112, "before this one", 11.5, HOT))
    out.append(t(40, 196, "The timing between flashes is data too: a modified base on the "
                          "template slows the polymerase down.", 14, INK))
    out.append(t(40, 220, "That is how PacBio calls 5mC and 6mA without any conversion "
                          "chemistry at all.", 13.5, OK))
    return svg(700, 240, "".join(out))


def fig_ccs():
    out = [t(40, 26, "Accuracy comes from reading the same molecule many times.", 14, INK)]
    cx, cy, r = 110, 108, 44
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TOP}" '
               f'stroke-width="2.6"/>')
    out.append(t(cx, cy + 5, "one insert", 11.5, MUTE, anchor="middle"))
    out.append(arrow(cx + r + 10, cy, cx + r + 46, HOT))
    for i in range(4):
        y = 70 + i * 24
        out.append(line(230, y, 420, y, MUTE, 2))
        for j in range(2):
            out.append(dot(258 + ((i * 37 + j * 91) % 150), y, 3.2, BAD))
    out.append(t(230, 56, "passes, each with random errors", 12, MUTE))
    out.append(arrow(436, 106, 470, MUTE))
    out.append(line(486, 106, 676, 106, OK, 3))
    out.append(t(486, 88, "consensus: the errors do not agree, the sequence does", 12, OK))
    out.append(t(40, 186, "A short insert gets many passes and very high accuracy; a long "
                          "insert gets few passes and less.", 14, INK))
    out.append(t(40, 210, "So on PacBio, insert length and accuracy are the same decision — "
                          "and size selection is how you make it.", 13.5, HOT))
    return svg(700, 230, "".join(out))


def fig_nanopore():
    out = [t(40, 26, "No polymerase, no copying: the molecule itself is the signal.", 14, INK)]
    out.append(f'<rect x="60" y="96" width="330" height="12" fill="#dfe3e6"/>')
    out.append(t(60, 88, "membrane", 11.5, MUTE))
    out.append(f'<path d="M 216 96 L 204 78 L 248 78 L 236 96 L 236 108 L 248 126 L 204 126 '
               f'L 216 108 Z" fill="#eef1f3" stroke="{TOP}" stroke-width="1.6"/>')
    out.append(t(226, 146, "pore", 11.5, TOP, anchor="middle"))
    out.append(f'<path d="M 120 52 C 170 52, 180 70, 226 78" fill="none" stroke="{MUTE}" '
               f'stroke-width="2.4"/>')
    out.append(dot(150, 56, 8, HOT))
    out.append(t(150, 40, "motor protein ratchets the strand through", 11.5, HOT))
    out.append(line(226, 126, 226, 160, MUTE, 2.4))
    # squiggle
    import math
    pts = []
    for i in range(170):
        x = 420 + i * 1.5
        y = 96 + 20 * math.sin(i / 3.0) + 10 * math.sin(i / 7.0 + 1)
        pts.append(f"{x:.0f},{y:.0f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" '
               f'stroke-width="1.8"/>')
    out.append(t(420, 58, "current through the pore", 12, INK))
    out.append(t(420, 142, "a neural network turns the squiggle into bases", 11.5, MUTE))
    out.append(t(40, 190, "Read length is simply how long the molecule was — so how you "
                          "pipette becomes how long your reads are.", 14, INK))
    out.append(t(40, 214, "Modified bases change the current too, so they can be called "
                          "from the same signal, with no conversion step.", 13.5, OK))
    return svg(700, 234, "".join(out))


def fig_ont_kits():
    out = [t(40, 26, "Three ways to attach the motor adapter.", 14, INK)]
    rows = [("ligation", "end-repair, dA-tail, ligate the adapter",
             "best yield and read length; most handling", OK),
            ("rapid", "a transposase inserts the adapter sequence",
             "ten minutes, but tagmentation — cut and tag in one — shortens the DNA", HOT),
            ("ultra-long", "very gentle, very high molecular weight input",
             "reads in the hundreds of kilobases", TOP)]
    for i, (name, how, trade, col) in enumerate(rows):
        y = 62 + i * 46
        out.append(t(60, y, name, 13.5, col, weight="bold"))
        out.append(t(170, y, how, 12.5, INK))
        out.append(t(170, y + 17, trade, 11.5, MUTE))
    out.append(t(40, 212, "Whatever the route, the molecule ends up with a motor protein on "
                          "one end — that end goes into the pore first.", 14, INK))
    out.append(t(40, 236, "Barcodes are ligated before the motor adapter, so a barcode is "
                          "read at the start of every read.", 13.5, MUTE))
    return svg(700, 256, "".join(out))


def fig_platform_compare():
    out = [t(40, 26, "What each platform is actually good at.", 14, INK)]
    x0, y0, w, h = 90, 56, 420, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    out.append(t(x0 + w / 2, y0 + h + 36, "read length  →", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 12, y0 + 8, "accuracy", 12.5, MUTE, anchor="end"))
    out.append(t(x0 - 12, y0 + 24, "↑", 12.5, MUTE, anchor="end"))
    pts = [("Illumina", 0.10, 0.80, TOP), ("MGI", 0.16, 0.82, TOP),
           ("AVITI", 0.13, 0.90, TOP), ("Ultima", 0.09, 0.66, MUTE),
           ("PacBio HiFi", 0.62, 0.93, OK), ("Nanopore", 0.92, 0.58, HOT)]
    for name, fx, fy, c in pts:
        px, py = x0 + fx * w, y0 + h - fy * h
        out.append(dot(px, py, 6, c))
        out.append(t(px, py - 14, name, 11.5, c, anchor="middle"))
    out.append(t(x0 + 10, y0 + h + 18, "150 bp", 11, MUTE))
    out.append(t(x0 + w - 10, y0 + h + 18, "100 kb +", 11, MUTE, anchor="end"))
    out.append(t(40, 248, "There is no best platform. There is a question, a sample, and a "
                          "budget — and those pick the platform.", 14, INK))
    out.append(t(40, 272, "Positions here are schematic, and they move every year.", 12.5, MUTE))
    return svg(700, 292, "".join(out))


def fig_error_profiles():
    out = [t(40, 26, "Each platform fails in its own way.", 14, INK)]
    rows = [("Illumina / MGI / AVITI", "substitutions, rising with cycle number", 0.9, TOP),
            ("Ultima", "homopolymer length: AAAAA read as AAAA", 0.5, MUTE),
            ("PacBio HiFi", "few, random, mostly indels — and consensus removes them", 0.95, OK),
            ("Nanopore", "indels, worst in homopolymers; improving each chemistry", 0.6, HOT)]
    for i, (name, how, acc, col) in enumerate(rows):
        y = 62 + i * 44
        out.append(t(56, y, name, 13, col, weight="bold"))
        out.append(t(56, y + 18, how, 11.5, MUTE))
        bx = 330
        out.append(f'<rect x="{bx}" y="{y-11}" width="200" height="12" fill="#eceff1"/>')
        out.append(f'<rect x="{bx}" y="{y-11}" width="{200*acc:.0f}" height="12" '
                   f'fill="{col}" opacity="0.8"/>')
    out.append(t(330, 44, "accuracy of a single raw read", 11.5, MUTE))
    out.append(t(40, 246, "This decides whether you need UMIs or consensus reads, and "
                          "whether a variant call can be trusted.", 14, INK))
    out.append(t(40, 270, "A library cannot fix a platform's error mode — but it can give "
                          "you a second copy of the molecule to check against.", 13.5, MUTE))
    return svg(700, 290, "".join(out))


build(__file__, [
    ("sanger", fig_sanger),
    ("universal-ends", fig_universal_ends),
    ("flowcell", fig_flowcell),
    ("bridge", fig_bridge),
    ("linearise", fig_linearise),
    ("sbs", fig_sbs),
    ("read-order", fig_read_order),
    ("pe-turnaround", fig_pe_turnaround),
    ("i5-orientation", fig_i5_orientation),
    ("readthrough", fig_readthrough),
    ("index-hopping", fig_index_hopping),
    ("diversity", fig_diversity),
    ("dnbseq", fig_dnbseq),
    ("other-shortread", fig_other_shortread),
    ("smrtbell", fig_smrtbell),
    ("zmw", fig_zmw),
    ("ccs", fig_ccs),
    ("nanopore", fig_nanopore),
    ("ont-kits", fig_ont_kits),
    ("error-profiles", fig_error_profiles),
    ("platform-compare", fig_platform_compare),
])
