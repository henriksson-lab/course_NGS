#!/usr/bin/env python3
"""Figures for the chromatin unit.  Run: python3 chromatin/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE_B = "#e8eef5"
PALE_R = "#f5eae6"
PALE_G = "#e6f0e8"
GREY = "#dfe3e6"
NUCF = "#e9dcc6"
NUCS = "#a08560"
PURP = "#6b5b8a"


# ------------------------------------------------------------------ helpers

def dna(x1, x2, y, col=TOP, w=3.2):
    return line(x1, y, x2, y, col, w, cap="butt")


def nuc(x, y, r=11):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.15:.1f}" fill="{NUCF}" '
            f'stroke="{NUCS}" stroke-width="1.4"/>')


def tf(x, y, r=7, fill=HOT):
    return (f'<rect x="{x - r}" y="{y - r - 3}" width="{2 * r}" height="{2 * r}" rx="3" '
            f'fill="{fill}"/>')


def cut(x, y, col=HOT, h=9):
    return line(x - 4, y - h, x + 4, y + h, col, 2.2) + line(x + 4, y - h, x - 4, y + h, col, 2.2)


def gsum(x, peaks, base=0.0):
    return base + sum(h * math.exp(-((x - c) / s) ** 2) for c, h, s in peaks)


def track(x0, x1, ybase, peaks, col=TOP, fill=PALE_B, base=0.0, step=2):
    """Filled coverage track; peaks are (centre, height, sigma)."""
    pts = [(x, ybase - gsum(x, peaks, base)) for x in range(int(x0), int(x1) + 1, step)]
    d = f"M {x0} {ybase} " + " ".join(f"L {x} {y:.1f}" for x, y in pts) + f" L {x1} {ybase} Z"
    return (f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="1.4"/>'
            + line(x0, ybase, x1, ybase, MUTE, 1))


def rd(x1, x2, y, col=TOP, h=5):
    """A read drawn as a thick bar with an arrow head showing direction."""
    d = 1 if x2 > x1 else -1
    return (line(x1, y, x2 - d * h, y, col, 3.2, cap="butt") +
            f'<path d="M {x2} {y} L {x2 - d * h} {y - h * 0.8} L {x2 - d * h} {y + h * 0.8} Z" '
            f'fill="{col}"/>')


def step_box(x, y, w, h, head, body, fill="#fbfbf9", hcol=HOT, size=11.5):
    out = [box(x, y, w, h, "", fill, MUTE)]
    out.append(t(x + w / 2, y + 17, head, 13, hcol, anchor="middle", weight="bold"))
    for j, ln in enumerate(body.split("\n")):
        out.append(t(x + w / 2, y + 36 + j * 15, ln, size, MUTE, anchor="middle"))
    return "".join(out)


# ------------------------------------------------------------------ figures

def fig_layers():
    out = [t(30, 26, "One stretch of chromatin, three different questions.", 14, INK)]
    y = 92
    out.append(dna(30, 690, y))
    for x in (60, 98, 136):
        out.append(nuc(x, y, 12))
    out.append(tf(240, y - 12, 8))
    out.append(t(240, y - 36, "TF bound", 12, HOT, anchor="middle"))
    for x in (330, 368, 406, 444):
        out.append(nuc(x, y, 12))
    out.append(t(192, y + 40, "open DNA", 12, MUTE, anchor="middle"))
    out.append(t(552, y + 40, "open DNA", 12, MUTE, anchor="middle"))
    out.append(t(98, y - 36, "nucleosomes", 12, NUCS, anchor="middle"))
    out.append(nuc(660, y, 12))
    # question boxes
    qs = [("Is it open?", "ATAC-seq, DNase-seq", 30),
          ("Where are the nucleosomes?", "MNase-seq", 255),
          ("Who is bound?", "ChIP-seq, CUT&amp;RUN, CUT&amp;Tag", 480)]
    for q, m, x in qs:
        out.append(box(x, 150, 205, 54, "", "#fbfbf9", MUTE))
        out.append(t(x + 102, 172, q, 13, INK, anchor="middle", weight="bold"))
        out.append(t(x + 102, 192, m, 12, HOT, anchor="middle"))
    return svg(720, 222, "".join(out))


def fig_reads_mean():
    out = [t(30, 24, "A read is the address of a cut.", 14, INK)]
    y = 78
    out.append(dna(30, 690, y))
    out.append(f'<rect x="250" y="{y - 22}" width="190" height="44" rx="6" fill="{PALE_G}" '
               f'stroke="{OK}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    out.append(dna(30, 690, y))
    for x in (60, 100, 140, 180, 220):
        out.append(nuc(x, y, 11))
    for x in (480, 520, 560, 600, 640):
        out.append(nuc(x, y, 11))
    out.append(t(345, y - 28, "open: the enzyme can reach", 12, OK, anchor="middle"))
    for x in (268, 292, 311, 330, 346, 362, 381, 399, 420):
        out.append(cut(x, y, HOT, 8))
    out.append(t(150, y + 40, "wrapped: no cuts", 12, MUTE, anchor="middle"))
    out.append(t(560, y + 40, "wrapped: no cuts", 12, MUTE, anchor="middle"))
    out.append(track(30, 690, 236, [(345, 56, 55), (330, 18, 20), (400, 12, 14)], HOT, PALE_R, base=2))
    out.append(t(30, 254, "reads piled up per position", 12, MUTE))
    out.append(t(30, 146, "every read starts at a cut: align it and add it to the pile", 13, INK))
    return svg(720, 266, "".join(out))


def fig_dnase():
    out = [t(30, 24, "DNase-seq: cut open DNA, keep only the ends.", 14, INK)]
    y = 66
    out.append(dna(30, 690, y))
    for x in (50, 90, 130):
        out.append(nuc(x, y, 11))
    for x in (500, 540, 580, 620, 660):
        out.append(nuc(x, y, 11))
    out.append(cut(260, y, HOT, 9))
    out.append(cut(440, y, HOT, 9))
    out.append(t(350, y - 20, "light DNase I digestion of nuclei", 12, HOT, anchor="middle"))
    out.append(t(30, 108, "1", 13, HOT, weight="bold"))
    out.append(t(48, 108, "a double-strand break in open DNA, at either end of the open stretch", 12.5, INK))
    # linker ligation
    y2 = 150
    out.append(dna(240, 460, y2, TOP, 3.2))
    out.append(box(190, y2 - 9, 50, 18, "linker I", PALE_R, BAD, 11, BAD))
    out.append(box(460, y2 - 9, 50, 18, "linker I", PALE_R, BAD, 11, BAD))
    out.append(dot(200, y2 - 18, 4, OK))
    out.append(t(212, y2 - 22, "biotin", 11, OK))
    out.append(t(30, 154, "2", 13, HOT, weight="bold"))
    out.append(t(48, 188, "ligate a biotinylated linker, which carries an MmeI site", 12.5, INK))
    # MmeI
    y3 = 222
    out.append(box(190, y3 - 9, 50, 18, "linker I", PALE_R, BAD, 11, BAD))
    out.append(dna(240, 290, y3, TOP, 3.2))
    out.append(cut(292, y3, HOT, 8))
    out.append(t(310, y3 + 4, "MmeI cuts a fixed distance into the DNA: a short tag of the open-DNA end", 12, MUTE))
    out.append(t(30, 226, "3", 13, HOT, weight="bold"))
    out.append(t(48, 256, "capture on streptavidin, add linker II, PCR, sequence the ~20 bp tag", 12.5, INK))
    return svg(720, 272, "".join(out))


def fig_footprint():
    out = [t(30, 24, "A footprint is a hole in the pile of cuts.", 14, INK)]
    y = 66
    out.append(dna(30, 690, y))
    out.append(tf(360, y - 12, 9))
    out.append(t(360, y - 36, "TF bound here", 12, HOT, anchor="middle"))
    out.append(f'<rect x="338" y="{y + 6}" width="44" height="14" fill="{PALE_R}" stroke="none"/>')
    # cut profile
    base = 190
    pk = [(150, 48, 18), (210, 55, 22), (270, 42, 20), (460, 52, 20), (520, 44, 22),
          (310, 55, 18), (410, 56, 18)]
    pts = []
    for x in range(40, 681, 2):
        v = gsum(x, [(c, h, s) for c, h, s in pk], 4)
        v += 18 * math.exp(-((x - 360) / 40) ** 2) * 1.5
        if 340 <= x <= 380:
            v = 5
        pts.append((x, base - v))
    d = f"M 40 {base} " + " ".join(f"L {x} {yy:.1f}" for x, yy in pts) + f" L 680 {base} Z"
    out.append(f'<path d="{d}" fill="{PALE_B}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(line(40, base, 680, base, MUTE, 1))
    out.append(line(360, y + 22, 360, base - 14, HOT, 1.2, dash="3 3"))
    out.append(t(372, 112, "protected: the enzyme could not cut here", 12, HOT))
    out.append(t(40, base + 20, "cut count per base, inside one open region", 12, MUTE))
    out.append(t(30, 242, "The protein is never in the library. Its absence is: a few "
                          "tens of bases with almost no cuts.", 13, INK))
    return svg(720, 256, "".join(out))


def fig_tn5():
    out = [t(30, 24, "Tn5 cuts and ligates in one step: tagmentation.", 14, INK)]
    y = 92
    out.append(dna(30, 690, y - 5, TOP, 3.2))
    out.append(dna(30, 690, y + 5, BOT, 3.2))
    out.append(f'<ellipse cx="300" cy="{y}" rx="52" ry="22" fill="{PALE_R}" stroke="{BAD}" stroke-width="1.4"/>')
    out.append(t(300, y + 4, "Tn5 dimer", 12, BAD, anchor="middle"))
    out.append(box(250, 38, 44, 16, "adapter", PALE_B, TOP, 10.5, TOP))
    out.append(box(306, 38, 44, 16, "adapter", PALE_B, TOP, 10.5, TOP))
    out.append(t(24, y - 1, "5'", 11.5, MUTE, anchor="end"))
    out.append(t(694, y - 1, "3'", 11.5, MUTE))
    out.append(t(24, y + 9, "3'", 11.5, MUTE, anchor="end"))
    out.append(t(694, y + 9, "5'", 11.5, MUTE))
    out.append(t(30, 136, "Tn5 loaded with two adapters binds DNA and cuts both strands, staggered by 9 nt", 12.5, INK))
    y2 = 186
    out.append(dna(30, 290, y2 - 5, TOP, 3.2))
    out.append(dna(30, 290, y2 + 5, BOT, 3.2))
    out.append(dna(380, 690, y2 - 5, TOP, 3.2))
    out.append(dna(380, 690, y2 + 5, BOT, 3.2))
    # the adapter is joined to a 5' end, so the strand that overhangs is the one
    # carrying it: the bottom strand on the left product, the top strand on the right
    out.append(dna(290, 305, y2 + 5, HOT, 3.2))
    out.append(dna(365, 380, y2 - 5, HOT, 3.2))
    out.append(box(262, y2 + 18, 56, 16, "adapter", PALE_B, TOP, 10.5, TOP))
    out.append(box(352, y2 - 36, 56, 16, "adapter", PALE_B, TOP, 10.5, TOP))
    out.append(t(336, y2 + 54, "9 nt single-stranded gap on each side", 12, HOT, anchor="middle"))
    out.append(t(30, 268, "Each adapter is joined to one 5' end only. The gap is filled in later, "
                          "by the 72 °C step before PCR.", 12.5, INK))
    out.append(t(30, 290, "A Tn5 insertion is one point in the genome; the read starts next to it.", 12.5, MUTE))
    return svg(720, 306, "".join(out))


def fig_atac_flow():
    out = [t(30, 24, "ATAC-seq: everything happens in one tube of nuclei.", 14, INK)]
    steps = [("1  nuclei", "50,000 cells,\nlysed, spun"),
             ("2  tagment", "Tn5, 37 °C,\n30 min"),
             ("3  clean up", "purify DNA\nfrom the enzyme"),
             ("4  PCR", "72 °C gap fill,\nthen cycles"),
             ("5  sequence", "paired-end,\nshort reads")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 70, h, b))
        if i < 4:
            out.append(arrow(x + 120, 75, x + 134, MUTE))
    out.append(t(30, 142, "Which fragments become library?", 13, INK, weight="bold"))
    rows = [("adapter A on one end, B on the other", OK, "amplifies with both primers"),
            ("A at both ends, or B at both", BAD, "one primer fits; amplifies poorly")]
    for i, (a, c, b) in enumerate(rows):
        yy = 168 + i * 30
        out.append(box(30, yy - 11, 28, 18, "A", PALE_B, TOP, 11, TOP))
        out.append(dna(58, 150, yy - 2, MUTE, 3))
        out.append(box(150, yy - 11, 28, 18, "B" if i == 0 else "A", PALE_R if i == 0 else PALE_B,
                       BAD if i == 0 else TOP, 11, BAD if i == 0 else TOP))
        out.append(t(196, yy + 2, a, 12, INK))
        out.append(t(440, yy + 2, b, 12, c))
    return svg(720, 230, "".join(out))


def fig_atac_sizes():
    out = [t(30, 24, "Fragment length records what sat between two insertions.", 14, INK)]
    # left: three molecule classes
    rows = [("nucleosome-free", [], (70, 150)),
            ("one nucleosome", [105], (60, 150)),
            ("two nucleosomes", [90, 140], (55, 175))]
    for i, (label, nucs, (c1, c2)) in enumerate(rows):
        yy = 62 + i * 52
        out.append(dna(30, 230, yy, MUTE, 2.4))
        for nx in nucs:
            out.append(nuc(nx, yy, 12))
        out.append(cut(c1, yy, HOT, 8))
        out.append(cut(c2, yy, HOT, 8))
        out.append(t(240, yy + 4, label, 12, INK))
    # right: histogram schematic
    x0, base = 400, 210
    out.append(track(x0, 690, base, [(425, 118, 13), (485, 74, 14), (555, 40, 15), (625, 20, 15)],
                     TOP, PALE_B, base=3))
    for xx, lab in ((425, "&lt;100"), (485, "~200"), (555, "~400"), (625, "~600")):
        out.append(t(xx, base + 16, lab, 11.5, MUTE, anchor="middle"))
    out.append(t(x0 + 145, base + 33, "fragment length (bp), schematic", 12, MUTE, anchor="middle"))
    out.append(t(x0, 52, "paired reads give the length of every insert", 12.5, INK))
    out.append(t(30, 270, "Tn5 cannot cut through a nucleosome, so lengths step in units of one "
                          "nucleosome plus linker.", 12.5, INK))
    return svg(720, 286, "".join(out))


def fig_mnase():
    out = [t(30, 24, "MNase-seq: digest the linkers, sequence what is left.", 14, INK)]
    y = 70
    out.append(dna(30, 690, y, MUTE, 2.4))
    xs = [70, 130, 190, 250, 310, 370, 430, 490, 550, 610]
    for x in xs:
        out.append(nuc(x, y, 16))
    for x in (100, 160, 220, 280, 340, 400, 460, 520, 580):
        out.append(cut(x, y, HOT, 9))
    out.append(t(30, 112, "MNase prefers linker DNA; with enough digestion each nucleosome keeps ~147 bp", 12.5, INK))
    # reads
    for i, x in enumerate(xs[:6]):
        out.append(rd(x - 24, x - 2, 140 + (i % 3) * 8, TOP))
        out.append(rd(x + 24, x + 2, 140 + (i % 3) * 8, BOT))
    out.append(t(30, 178, "paired-end reads: the two ends of each protected fragment", 12.5, INK))
    # coverage
    out.append(track(30, 690, 232, [(x, 40, 17) for x in xs], HOT, PALE_R, base=3))
    out.append(t(30, 252, "pile-up centre = the nucleosome's dyad; spacing between peaks = linker length",
                 12.5, INK))
    return svg(720, 266, "".join(out))


def fig_footprinting_meth():
    out = [t(30, 24, "Mark the open DNA, then read one long molecule.", 14, INK)]
    rowsdef = [
        ("molecule 1", [(60, 200), (290, 360), (430, 500), (570, 690)]),
        ("molecule 2", [(60, 120), (190, 270), (340, 420), (500, 690)]),
    ]
    for r, (lab, opens) in enumerate(rowsdef):
        yy = 66 + r * 52
        out.append(dna(40, 690, yy, GREY, 3))
        for a, b in opens:
            out.append(dna(a, b, yy, TOP, 3))
            n = int((b - a) / 22)
            for k in range(n):
                out.append(dot(a + 10 + k * 22, yy - 9, 3.4, HOT))
        # nucleosomes in the gaps
        prev = 40
        for a, b in opens + [(690, 690)]:
            if a - prev > 50:
                out.append(nuc((prev + a) / 2, yy, 12))
            prev = b
        out.append(t(30, yy + 4, "", 10))
    out.append(t(40, 156, "Dots: methylated bases (m6A by Hia5 in Fiber-seq; GpC by M.CviPI in NOMe-seq).", 12.5, INK))
    out.append(t(40, 178, "Unmarked stretches are nucleosomes or bound proteins. Every molecule has its own pattern.", 12.5, INK))
    out.append(t(40, 204, "Bulk methods average that pattern away; this one keeps it.", 12.5, HOT))
    return svg(720, 220, "".join(out))


def fig_chip_flow():
    out = [t(30, 24, "ChIP-seq: fix, break up, pull down, release.", 14, INK)]
    steps = [("1  crosslink", "formaldehyde\nfreezes contacts"),
             ("2  fragment", "sonicate to\n200-700 bp"),
             ("3  pull down", "antibody + beads\ncatch one protein"),
             ("4  wash", "everything\nunbound leaves"),
             ("5  release", "65 °C, protease:\nreverse, free DNA")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 70, h, b))
        if i < 4:
            out.append(arrow(x + 120, 75, x + 134, MUTE))
    y = 160
    out.append(dna(30, 250, y, MUTE, 3))
    out.append(tf(140, y - 12, 8))
    out.append(t(260, y + 4, "the protein stays on the DNA through steps 2 to 4", 12.5, INK))
    out.append(dna(30, 250, y + 40, MUTE, 3))
    out.append(t(260, y + 44, "no protein here: washed away at step 4", 12.5, MUTE))
    out.append(t(30, 252, "Then end repair, A-tailing, adapter ligation and PCR: an ordinary DNA library.", 12.5, HOT))
    return svg(720, 266, "".join(out))


def fig_crosslink():
    out = [t(30, 24, "Two crosslinkers, two reaches.", 14, INK)]
    y = 130
    out.append(dna(30, 690, y, TOP, 3.2))
    out.append(tf(180, y - 16, 14, HOT))
    out.append(t(180, y - 50, "TF A (binds DNA)", 12, HOT, anchor="middle"))
    out.append(tf(300, y - 58, 14, PURP))
    out.append(t(300, y - 92 + 8, "TF B (binds A, not DNA)", 12, PURP, anchor="middle"))
    out.append(line(180, y + 0, 180, y - 22, HOT, 3))
    out.append(t(196, y + 22, "formaldehyde: ~2 Å, protein-DNA and close protein-protein", 12, HOT))
    out.append(line(194, y - 30, 288, y - 54, BAD, 2.4, dash="5 3"))
    out.append(t(330, y - 34, "DSG: 7.7 Å spacer, protein-protein only", 12, BAD))
    out.append(t(30, 204, "Formaldehyde alone often misses factors held in place by a partner; "
                          "adding DSG as well catches them.", 12.5, INK))
    out.append(t(30, 226, "Reversal: heat at 65 °C breaks the formaldehyde links; protease digests "
                          "the proteins; the DNA is free.", 12.5, INK))
    out.append(t(30, 248, "Too much crosslinking masks the epitope and makes chromatin hard to shear.", 12.5, MUTE))
    return svg(720, 262, "".join(out))


def fig_chip_reads():
    out = [t(30, 24, "ChIP reads are fragment ends, not the site itself.", 14, INK)]
    y = 62
    out.append(dna(30, 690, y, MUTE, 2.4))
    out.append(tf(360, y - 12, 8))
    # fragments
    frs = [(220, 480), (260, 430), (300, 520), (230, 400), (330, 560), (180, 380), (320, 450)]
    for i, (a, b) in enumerate(frs):
        yy = 80 + i * 10
        out.append(line(a, yy, b, yy, GREY, 5, cap="butt"))
        out.append(rd(a, a + 36, yy, TOP))
        out.append(rd(b, b - 36, yy, BOT))
    out.append(t(30, 100, "sonicated", 11.5, MUTE))
    out.append(t(30, 114, "fragments", 11.5, MUTE))
    base = 256
    out.append(track(30, 690, base, [(310, 42, 24)], TOP, PALE_B, base=2))
    out.append(track(30, 690, base, [(410, 42, 24)], BOT, "none", base=2))
    out.append(track(30, 690, base, [(360, 62, 28)], HOT, "none", base=2))
    out.append(t(262, base - 46, "forward-strand 5' ends", 11.5, TOP, anchor="end"))
    out.append(t(460, base - 46, "reverse-strand 5' ends", 11.5, BOT))
    out.append(t(360, base - 70, "extend to fragment length: peak at the site", 12, HOT, anchor="middle"))
    out.append(t(30, 282, "Two humps flank the site by about half a fragment length; "
                          "single-end reads are shifted or extended to centre them.", 12.5, INK))
    return svg(720, 296, "".join(out))


def fig_chip_background():
    out = [t(30, 24, "Without a control you cannot tell a peak from an easy-to-break region.", 14, INK)]
    labels = [("ChIP", 120, [(150, 50, 16), (320, 44, 16), (520, 58, 18)], HOT, PALE_R, 60),
              ("input DNA (no antibody)", 190, [(150, 38, 22), (320, 8, 18), (520, 12, 18)], MUTE, GREY, 140),
              ("IgG / no-target control", 252, [(150, 14, 22), (320, 6, 18), (520, 6, 18)], MUTE, GREY, 206)]
    for lab, base, pk, c, f, ly in labels:
        out.append(track(30, 690, base, pk, c, f, base=3))
        out.append(t(34, ly, lab, 12, c))
    out.append(t(150, 274, "open promoter", 11.5, MUTE, anchor="middle"))
    out.append(t(320, 274, "weak, real", 11.5, MUTE, anchor="middle"))
    out.append(t(520, 274, "strong, real", 11.5, MUTE, anchor="middle"))
    out.append(t(30, 300, "The promoter peak shows up in input too: open chromatin shears more "
                          "easily, so it is over-represented with any antibody.", 12.5, INK))
    return svg(720, 314, "".join(out))


def fig_tether():
    out = [t(30, 24, "Cut where the antibody is, not everywhere.", 14, INK)]
    # left: ChIP
    out.append(t(30, 54, "ChIP: break everything, then fish", 13, INK, weight="bold"))
    y = 150
    out.append(dna(30, 330, y, MUTE, 2.6))
    for x in (60, 120, 180, 240, 300):
        out.append(cut(x, y, MUTE, 7))
    out.append(tf(150, y - 12, 7))
    out.append(t(30, 190, "random fragmentation; the target", 12, MUTE))
    out.append(t(30, 206, "is a few fragments among all", 12, MUTE))
    # right: tethered
    out.append(t(390, 54, "Tethered enzyme: break only at the target", 13, INK, weight="bold"))
    out.append(dna(390, 690, y, MUTE, 2.6))
    out.append(tf(540, y - 12, 7))
    out.append(line(540, y - 24, 540, y - 40, TOP, 2))
    out.append(f'<path d="M 540 {y - 40} L 528 {y - 54} L 552 {y - 54} Z" fill="{PALE_B}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(t(560, y - 44, "antibody", 11.5, TOP))
    out.append(box(512, y - 84, 56, 18, "pA", PALE_G, OK, 11.5, OK))
    out.append(box(568, y - 84, 76, 18, "MNase / Tn5", PALE_R, BAD, 11.5, BAD))
    out.append(cut(500, y, HOT, 9))
    out.append(cut(580, y, HOT, 9))
    out.append(t(390, 190, "the enzyme is brought to the protein, so", 12, MUTE))
    out.append(t(390, 206, "cuts and the signal are the same thing", 12, MUTE))
    out.append(t(30, 240, "Protein A binds the antibody's Fc region, so one fusion protein works with any "
                          "rabbit or mouse antibody.", 12.5, INK))
    out.append(t(30, 262, "The enzyme swap decides the product: MNase releases a fragment; Tn5 tags it "
                          "with sequencing adapters.", 12.5, HOT))
    return svg(720, 278, "".join(out))


def fig_cutrun():
    out = [t(30, 24, "CUT&amp;RUN: cut out the protected piece, and let it diffuse away.", 14, INK)]
    steps = [("1  bind", "cells or nuclei on\nlectin beads, open\nthe membrane"),
             ("2  antibody", "primary antibody,\nthen pA-MNase,\ncold, no calcium"),
             ("3  activate", "add Ca2+: MNase\ncuts on both sides\nof the protein"),
             ("4  release", "cut piece leaves\nthe nucleus; keep\nthe supernatant"),
             ("5  library", "extract DNA,\nsmall fragments,\nstandard library")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 86, h, b, size=11))
        if i < 4:
            out.append(arrow(x + 120, 83, x + 134, MUTE))
    y = 172
    out.append(dna(30, 690, y, MUTE, 2.6))
    out.append(tf(360, y - 12, 8))
    out.append(cut(330, y, HOT, 9))
    out.append(cut(390, y, HOT, 9))
    out.append(line(333, y + 12, 387, y + 12, HOT, 4, cap="butt"))
    out.append(t(300, y + 34, "this piece is the library; the rest stays in the nucleus", 12, HOT))
    out.append(t(30, 232, "No crosslinking and no sonication in the standard protocol; "
                          "background is low because the rest of the DNA is never released.", 12.5, INK))
    return svg(720, 246, "".join(out))


def fig_cuttag():
    out = [t(30, 24, "CUT&amp;Tag: the cut and the library adapters happen together.", 14, INK)]
    steps = [("1  bind", "cells on beads,\npermeabilise"),
             ("2  antibody", "primary, secondary,\nthen pA-Tn5\n(adapters loaded)"),
             ("3  wash", "high salt keeps\npA-Tn5 only where\nthe antibody is"),
             ("4  activate", "add Mg2+: Tn5\ntagments the DNA\nnext to the protein"),
             ("5  PCR", "release DNA, 72 °C\ngap fill, indexed\nPCR")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 86, h, b, size=11))
        if i < 4:
            out.append(arrow(x + 120, 83, x + 134, MUTE))
    y = 172
    out.append(dna(30, 690, y - 4, TOP, 2.6))
    out.append(dna(30, 690, y + 4, BOT, 2.6))
    out.append(tf(360, y - 7, 8))
    for x in (330, 390):
        out.append(box(x - 14, y - 32, 28, 12, "", PALE_B, TOP))
        out.append(box(x - 14, y + 14, 28, 12, "", PALE_R, BAD))
    out.append(t(300, y + 40, "adapters are already on the ends: no repair, no ligation", 12, HOT))
    out.append(t(30, 232, "Reads are cheap because almost nothing but the target is tagged: "
                          "a few million per sample can be enough.", 12.5, INK))
    return svg(720, 246, "".join(out))


def fig_cut_reads():
    out = [t(30, 24, "The same transcription factor, three ways.", 14, INK)]
    labs = [("ChIP-seq: broad hump, more background", 100, [(360, 40, 44), (140, 12, 30), (560, 10, 30)], TOP, PALE_B),
            ("CUT&amp;RUN: narrow peak, quiet baseline", 170, [(360, 52, 14)], HOT, PALE_R),
            ("CUT&amp;Tag: narrow peak, quiet baseline", 240, [(360, 50, 14), (150, 8, 10), (590, 8, 10)], OK, PALE_G)]
    for lab, base, pk, c, f in labs:
        out.append(track(30, 690, base, pk, c, f, base=2))
        out.append(t(34, base - 54, lab, 12, c))
    out.append(t(360, 262, "binding site", 11.5, MUTE, anchor="middle"))
    out.append(t(30, 288, "CUT&amp;RUN fragments under a TF are short (under about 120 bp): "
                          "they are the footprint of the protein itself.", 12.5, INK))
    out.append(t(30, 310, "Tn5 still prefers open DNA, so small peaks at accessible sites can appear "
                          "without a real target.", 12.5, MUTE))
    return svg(720, 324, "".join(out))


def fig_damid():
    out = [t(30, 24, "DamID: the protein writes a mark; you read the mark.", 14, INK)]
    y = 90
    out.append(dna(30, 690, y, MUTE, 3))
    sites = [70, 130, 190, 250, 310, 370, 430, 490, 550, 610, 660]
    for i, x in enumerate(sites):
        near = 200 <= x <= 420
        out.append(line(x, y - 10, x, y + 10, HOT if near else MUTE, 2.4))
        if near:
            out.append(dot(x, y - 18, 3.8, HOT))
    out.append(tf(310, y + 26, 9, HOT))
    out.append(box(290, y + 40, 40, 16, "Dam", PALE_R, BAD, 11.5, BAD))
    out.append(t(30, 48, "GATC sites (ticks); methylated adenine near the fusion protein (dots)", 12, MUTE))
    out.append(t(30, 176, "1  Express Dam fused to the protein of interest, at low dose", 12.5, INK))
    out.append(t(30, 196, "2  DpnI cuts GATC only when methylated; ligate an adapter to those ends", 12.5, INK))
    out.append(t(30, 216, "3  cut with DpnII (unmethylated GATC only), then PCR from the adapter", 12.5, INK))
    out.append(t(30, 250, "No antibody and no crosslinking. A Dam-only control corrects for "
                          "where Dam goes by itself; resolution is set by GATC spacing.", 12.5, HOT))
    return svg(720, 264, "".join(out))


def fig_calling_cards():
    out = [t(30, 24, "Calling cards: the protein leaves a permanent record.", 14, INK)]
    y = 82
    out.append(dna(30, 690, y, MUTE, 3))
    out.append(tf(305, y - 12, 8))
    out.append(box(277, y - 52, 56, 18, "PB", PALE_R, BAD, 11.5, BAD))
    out.append(t(345, y - 40, "transposase fused to the TF", 12, BAD))
    for x in (230, 266, 340, 380):
        out.append(f'<path d="M {x} {y - 4} l 0 -14 l 8 0 l 0 14" fill="none" stroke="{HOT}" stroke-width="2.4"/>')
    out.append(t(305, y + 30, "new insertions cluster near the TF's sites", 12, HOT, anchor="middle"))
    out.append(t(30, 140, "1  express the TF-transposase fusion; the transposon (the 'card') inserts nearby", 12.5, INK))
    out.append(t(30, 160, "2  cells can be kept, sorted or differentiated; the insertions are in the genome for good", 12.5, INK))
    out.append(t(30, 180, "3  later, recover the junction between transposon and genome by PCR and sequence it", 12.5, INK))
    out.append(t(30, 214, "A read is a transposon insertion point. Unlike a ChIP snapshot, it integrates "
                          "binding over the time the fusion was expressed.", 12.5, HOT))
    return svg(720, 230, "".join(out))


def fig_dapseq():
    out = [t(30, 24, "DAP-seq: take the chromatin out of the question.", 14, INK)]
    steps = [("1  genomic DNA", "extract, fragment,\nadd adapters:\na library"),
             ("2  protein", "express a tagged TF\nin a test tube"),
             ("3  mix", "TF binds DNA\nin the tube"),
             ("4  pull down", "capture by the tag,\nwash, elute"),
             ("5  sequence", "reads = sequences\nthe TF can bind")]
    for i, (h, b) in enumerate(steps):
        x = 30 + i * 136
        out.append(step_box(x, 40, 118, 80, h, b))
        if i < 4:
            out.append(arrow(x + 120, 80, x + 134, MUTE))
    out.append(t(30, 158, "Nucleosomes, histone marks and competing factors are all absent, so the", 12.5, INK))
    out.append(t(30, 178, "map shows what the DNA sequence allows, not what the cell uses.", 12.5, INK))
    out.append(t(30, 210, "The 2016 paper used Arabidopsis; the logic applies to any genome. "
                          "PCR-amplified libraries lose DNA methylation.", 12.5, MUTE))
    return svg(720, 226, "".join(out))


def fig_choose():
    out = [t(30, 24, "Pick the method from the question.", 14, INK)]
    rows = [("Where is DNA open, in many samples?", "ATAC-seq / Omni-ATAC", 50),
            ("Open, and which TF motifs are occupied?", "ATAC or DNase, deep, footprints", 90),
            ("Nucleosome positions?", "MNase-seq", 130),
            ("Open vs closed on the same single molecule?", "methyltransferase footprinting", 170),
            ("Where is a histone mark, from few cells?", "CUT&amp;Tag", 210),
            ("Where is a TF, no good antibody?", "DamID, calling cards, tagged protein", 250)]
    for q, m, yy in rows:
        out.append(box(30, yy - 16, 330, 28, q, "#fbfbf9", MUTE, 12.5, INK))
        out.append(arrow(366, yy - 2, 392, MUTE))
        out.append(box(398, yy - 16, 290, 28, m, PALE_G, OK, 12.5, OK))
    return svg(720, 278, "".join(out))


def fig_reads_all():
    out = [t(30, 24, "What one read means, method by method.", 14, INK)]
    rows = [("ATAC-seq", "a Tn5 insertion, so an accessible base"),
            ("DNase-seq", "a DNase I cut, so an accessible base"),
            ("MNase-seq", "the edge of DNA a nucleosome protected"),
            ("ChIP-seq", "the end of a sonicated fragment that carried the protein"),
            ("CUT&amp;RUN", "the edge of DNA protected by a bound protein"),
            ("CUT&amp;Tag", "a Tn5 insertion beside the antibody"),
            ("DamID", "a GATC that was methylated near the fusion"),
            ("Calling cards", "a transposon insertion near where the TF had been")]
    for i, (a, b) in enumerate(rows):
        yy = 46 + i * 28
        out.append(box(30, yy - 14, 110, 22, a, PALE_B, TOP, 12, TOP))
        out.append(t(152, yy + 2, b, 12.5, INK))
    return svg(720, 270, "".join(out))


build(__file__, [
    ("layers", fig_layers),
    ("reads-mean", fig_reads_mean),
    ("dnase", fig_dnase),
    ("footprint", fig_footprint),
    ("tn5", fig_tn5),
    ("atac-flow", fig_atac_flow),
    ("atac-sizes", fig_atac_sizes),
    ("mnase", fig_mnase),
    ("methyl-footprint", fig_footprinting_meth),
    ("chip-flow", fig_chip_flow),
    ("crosslink", fig_crosslink),
    ("chip-reads", fig_chip_reads),
    ("chip-background", fig_chip_background),
    ("tether", fig_tether),
    ("cutrun", fig_cutrun),
    ("cuttag", fig_cuttag),
    ("cut-reads", fig_cut_reads),
    ("damid", fig_damid),
    ("calling-cards", fig_calling_cards),
    ("dapseq", fig_dapseq),
    ("choose", fig_choose),
    ("reads-all", fig_reads_all),
])
