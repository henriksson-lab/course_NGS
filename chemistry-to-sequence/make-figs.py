#!/usr/bin/env python3
"""Figures for the chemistry-to-sequence unit.  Run: python3 chemistry-to-sequence/make-figs.py"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

_svg = svg


def svg(w, h, body):
    """Grow the canvas to hold the lowest text line."""
    import re as _re
    ys = [float(m) for m in _re.findall(r'<text x="[-\d.]+" y="([-\d.]+)"', body)]
    return _svg(w, max(h, int(max(ys) + 14)) if ys else h, body)


PALE_HOT = "#f5eae6"
PALE_TOP = "#e8eef5"
PALE_OK = "#e6f0e8"
GRID = "#dfe3e6"


def cs(x, y, s, colors=None, default=INK, size=13):
    """Monospace run with a colour per position (dict index -> colour)."""
    colors = colors or {}
    out = []
    for i, ch in enumerate(s):
        if ch != " ":
            out.append(t(x + i * DX, y, ch, size, colors.get(i, default), family=MONO))
    return "".join(out)


def cap(x, y, s, size=13, fill=None, maxc=84):
    """A caption wrapped onto several lines so it does not stretch the canvas."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(t(x, y + i * (size + 5), ln, size, fill) for i, ln in enumerate(lines))


def table(x, y, colw, rowh, header, rows, size=12.5, hfill=PALE_TOP, cellcol=None):
    """A plain grid of boxes. rows is a list of lists of strings."""
    out = []
    xs = [x]
    for w in colw:
        xs.append(xs[-1] + w)
    for j, h in enumerate(header):
        out.append(box(xs[j], y, colw[j], rowh, h, hfill, MUTE, size, INK))
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            col = (cellcol(i, j, c) if cellcol else None) or INK
            out.append(box(xs[j], y + (i + 1) * rowh, colw[j], rowh, c, "none", GRID, size, col))
    return "".join(out)


# ------------------------------------------------------------------ 01 three routes

def fig_routes():
    out = [t(40, 28, "The sequencer reads bases and read ends. A property must become one of them.",
             14, INK)]
    rows = [
        ("methylated C, newly made RNA", "a base change", 70),
        ("protein footprint, cut site, stalled enzyme", "an end", 128),
        ("two loci in contact, a barcode on a cell", "a ligation junction", 186),
    ]
    for lab, name, y in rows:
        out.append(t(40, y + 6, lab, 13, MUTE))
        out.append(arrow(300, y, 340, MUTE, 1.4))
        out.append(t(640, y + 6, name, 15, HOT, anchor="middle", weight="bold"))
    # illustrations
    out.append(cs(352, 76, "ACGT", {1: HOT}))
    out.append(arrow(410, 70, 436, MUTE, 1.4))
    out.append(cs(442, 76, "ATGT", {1: BAD}))
    out.append(line(352, 134, 440, 134, TOP, 3))
    out.append(vtick(440, 124, 144, BAD, 3))
    out.append(t(448, 138, "read starts here", 11.5, MUTE))
    out.append(box(352, 174, 44, 18, "locus A", PALE_TOP, TOP, 11, TOP))
    out.append(box(396, 174, 44, 18, "locus B", PALE_HOT, HOT, 11, HOT))
    out.append(cap(40, 232, "Illumina copies and reads. Anything the copy does not carry across "
                          "is lost unless chemistry first writes it into the sequence.", 14, INK))
    return svg(780, 252, "".join(out))


# ------------------------------------------------------------------ 02 what the polymerase copies

def panel_copy(x, y, tmpl, copy, tcol, ccol, note):
    out = []
    out.append(box(x, y, 110, 120, "", "none", GRID))
    out.append(t(x + 55, y + 46, tmpl, 26, tcol, anchor="middle", family=MONO))
    out.append(t(x + 55, y + 14, "template", 11, MUTE, anchor="middle"))
    out.append(line(x + 55, y + 54, x + 55, y + 70, MUTE, 1.3))
    out.append(f'<path d="M {x+55} {y+74} L {x+51} {y+66} L {x+59} {y+66} Z" fill="{MUTE}"/>')
    out.append(t(x + 55, y + 98, copy, 26, ccol, anchor="middle", family=MONO))
    out.append(t(x + 55, y + 114, "polymerase puts", 11, MUTE, anchor="middle"))
    out.append(t(x + 55, y + 136, note, 11.5, MUTE, anchor="middle"))
    return "".join(out)


def fig_copy():
    out = [t(40, 28, "A polymerase reads the base it meets. It cannot read a methyl group.", 14, INK)]
    out.append(t(40, 52, "Before conversion", 13, MUTE))
    out.append(panel_copy(40, 62, "C", "G", BOT, BOT, "unmodified"))
    out.append(panel_copy(170, 62, "mC", "G", HOT, BOT, "modified: same copy"))
    out.append(t(330, 118, "indistinguishable", 13, BAD))
    out.append(t(330, 136, "in the sequence", 13, BAD))
    out.append(t(520, 52, "After conversion", 13, MUTE))
    out.append(panel_copy(520, 62, "U", "A", BAD, BAD, "C was converted"))
    out.append(panel_copy(650, 62, "mC", "G", HOT, BOT, "protected, still C"))
    out.append(t(780, 118, "the property is now", 13, OK))
    out.append(t(780, 136, "a base difference", 13, OK))
    out.append(cap(40, 226, "Conversion chemistry is a way of changing the template so that the copy differs.", 14, HOT))
    return svg(960, 246, "".join(out))


# ------------------------------------------------------------------ 03 bisulfite

S3 = "ATCGTCCGATACGCTCATCCGA"
M3 = {3, 7, 12}   # methylated C positions (a C followed by G)


def convert_bs(s, meth):
    return "".join(("C" if i in meth else "T") if ch == "C" else ch for i, ch in enumerate(s))


def cs_colors(s, meth, converted=None):
    col = {}
    for i, ch in enumerate(s):
        if converted and converted[i] != s[i]:
            col[i] = BAD
        elif ch == "C":
            col[i] = HOT if i in meth else BOT
    return col


def fig_bisulfite():
    # indexes of C positions in S3 that are methylated (CpG): find by CG
    meth = {i for i, ch in enumerate(S3) if ch == "C" and S3[i + 1:i + 2] == "G"}
    meth = set(sorted(meth)[:2])
    conv = convert_bs(S3, meth)
    out = [t(40, 28, "Bisulfite deaminates unmethylated C to U. Methylated C survives.", 14, INK)]
    x0 = 200
    rows = [("genomic DNA", S3, cs_colors(S3, meth)),
            ("after bisulfite", S3.replace("C", "U"), None),
            ("after PCR", conv, cs_colors(S3, meth, conv))]
    # row 2: unmethylated C -> U, methylated stays C
    s2 = "".join(("C" if i in meth else "U") if ch == "C" else ch for i, ch in enumerate(S3))
    c2 = {i: (HOT if i in meth else BAD) for i, ch in enumerate(S3) if ch == "C"}
    rows[1] = ("after bisulfite", s2, c2)
    for k, (lab, s, col) in enumerate(rows):
        y = 74 + k * 44
        out.append(t(x0 - 14, y, lab, 13, MUTE, anchor="end"))
        out.append(cs(x0, y, s, col))
    for i in meth:
        out.append(t(x0 + i * DX + 4, 56, "m", 11.5, HOT, anchor="middle"))
    out.append(t(x0 + 22 * DX + 24, 118, "U is copied as A,", 12.5, MUTE))
    out.append(t(x0 + 22 * DX + 24, 134, "so the product has T", 12.5, MUTE))
    out.append(t(x0, 192, "Read C: was methylated.   Read T: was not.", 14, HOT))
    out.append(cap(x0, 214, "Every C without an m has become U, then T; the two methylated ones are "
                          "still C.", 13, MUTE))
    return svg(760, 214, "".join(out))


# ------------------------------------------------------------------ 04 aligning converted reads

def fig_align():
    meth = {i for i, ch in enumerate(S3) if ch == "C" and S3[i + 1:i + 2] == "G"}
    meth = set(sorted(meth)[:2])
    conv = convert_bs(S3, meth)
    out = [t(40, 28, "Align against a reference in which C and T are allowed to match.", 14, INK)]
    x0 = 170
    out.append(t(x0 - 14, 70, "reference", 13, MUTE, anchor="end"))
    out.append(cs(x0, 70, S3, {i: BOT for i, c in enumerate(S3) if c == "C"}))
    out.append(t(x0 - 14, 100, "read", 13, MUTE, anchor="end"))
    out.append(cs(x0, 100, conv, cs_colors(S3, meth, conv)))
    out.append(t(x0 - 14, 130, "call", 13, MUTE, anchor="end"))
    for i, ch in enumerate(S3):
        if ch == "C":
            if conv[i] == "C":
                out.append(t(x0 + i * DX, 130, "M", 13, HOT, family=MONO, weight="bold"))
            else:
                out.append(t(x0 + i * DX, 130, "u", 13, BAD, family=MONO))
    for i in range(len(S3)):
        cx = x0 + i * DX + 4
        out.append(line(cx, 74, cx, 88, MUTE, 0.8))
    out.append(cap(x0, 168, "M = methylated, u = unmethylated. A read C opposite a reference T is an error; "
                          "a read T opposite a reference C is information.", 13, INK))
    out.append(cap(x0, 212, "Only three bases are left in the converted strand, so reads place less "
                          "uniquely.", 13, MUTE))
    return svg(760, 206, "".join(out))


# ------------------------------------------------------------------ 05 controls

def bars(x, y, w, h, pct, col, label, note, axis_top="100%"):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{GRID}"/>']
    bh = max(2, h * pct / 100)
    out.append(f'<rect x="{x}" y="{y + h - bh}" width="{w}" height="{bh}" fill="{col}"/>')
    out.append(t(x + w / 2, y + h + 18, label, 12.5, INK, anchor="middle"))
    out.append(t(x + w / 2, y + h + 34, note, 11.5, MUTE, anchor="middle"))
    out.append(t(x + w / 2, y - 6, f"{pct:g}% read as C", 12.5, col, anchor="middle"))
    return "".join(out)


def fig_controls():
    out = [t(40, 26, "Spike in two DNAs of known state. They tell you how far to trust every other number.",
             14, INK)]
    out.append(bars(70, 60, 70, 110, 0.6, BAD, "unmethylated spike-in", "e.g. phage lambda DNA"))
    out.append(bars(250, 60, 70, 110, 98, OK, "methylated spike-in", "fully methylated control"))
    out.append(bars(430, 60, 70, 110, 1.0, MUTE, "human non-CpG C", "almost never methylated"))
    out.append(t(560, 84, "Unmethylated spike-in read as C:", 12.5, INK))
    out.append(t(560, 102, "conversion failed, so false methylation.", 12.5, BAD))
    out.append(t(560, 126, "Methylated spike-in read as T:", 12.5, INK))
    out.append(t(560, 144, "the chemistry destroyed real signal.", 12.5, BAD))
    out.append(t(560, 168, "Values shown are an example of a good run.", 12, MUTE))
    out.append(cap(40, 236, "Conversion rate = T / (T + C) at spike-in cytosines: 99.4% here, so about 0.6% "
                          "false methylation.", 14, HOT))
    return svg(900, 256, "".join(out))


# ------------------------------------------------------------------ 06 matrix

def fig_matrix():
    out = [t(40, 26, "What each kind of cytosine is read as after PCR.", 14, INK)]
    header = ["method", "C", "5mC", "5hmC", "reads C means"]
    rows = [
        ["bisulfite", "T", "C", "C", "5mC or 5hmC"],
        ["oxBS-seq", "T", "C", "T", "5mC only"],
        ["TAB-seq", "T", "T", "C", "5hmC only"],
        ["EM-seq", "T", "C", "C", "5mC or 5hmC"],
        ["TAPS", "C", "T", "T", "unmodified C"],
    ]

    def cc(i, j, c):
        # Orange marks the cells the last column is about; blue is an ordinary base.
        # Not BAD: a T here is a successful conversion, and for TAPS it is the signal.
        if j in (1, 2, 3):
            return HOT if c == "C" else TOP
        return None
    out.append(table(40, 40, [120, 80, 80, 80, 200], 30, header, rows, 13, cellcol=cc))
    out.append(cap(40, 244, "5mC = 5-methylcytosine, 5hmC = 5-hydroxymethylcytosine. TAPS inverts the "
                          "logic: a T marks a modification.", 13, MUTE))
    return svg(640, 262, "".join(out))


# ------------------------------------------------------------------ 07-09 flows

def flow(title, heads, enz, stages, foot, W=860):
    """heads: stage names; enz: labels over arrows; stages: list of 3-tuples per stage."""
    out = [t(40, 26, title, 14, INK)]
    names = ["C", "5mC", "5hmC"]
    x0, colw = 40, 150
    out.append(t(x0, 70, "starting base", 12, MUTE))
    for k, nm in enumerate(names):
        out.append(t(x0, 100 + k * 34, nm, 13, INK, family=MONO))
    for s, st in enumerate(stages):
        x = x0 + 70 + s * colw
        out.append(t(x + 40, 58, heads[s], 12, MUTE, anchor="middle"))
        for k, (lab, col) in enumerate(st):
            out.append(t(x + 40, 100 + k * 34, lab, 14, col, anchor="middle", family=MONO))
        if s < len(stages) - 1:
            out.append(arrow(x + 84, 94, x + colw - 4, MUTE, 1.2, 4))
            out.append(t(x + 84 + (colw - 88) / 2, 84, enz[s], 11.5, MUTE, anchor="middle"))
    out.append(t(x0, 100 + 3 * 34 + 24, foot, 14, HOT))
    return svg(W, 100 + 3 * 34 + 44, "".join(out))


def fig_tab():
    st = [[("C", BOT), ("5mC", HOT), ("5hmC", HOT)],
          [("C", BOT), ("5mC", HOT), ("5gmC", OK)],
          [("C", BOT), ("5caC", HOT), ("5gmC", OK)],
          [("U", BAD), ("U", BAD), ("5gmC", OK)],
          [("T", BAD), ("T", BAD), ("C", OK)]]
    return flow("TAB-seq: protect 5hmC, oxidise 5mC to a convertible form, then convert.",
                ["start", "glucosylate", "oxidise", "bisulfite", "read after PCR"],
                ["T4-BGT", "TET", "bisulfite", "PCR"], st,
                "Only the protected 5hmC reads as C. Protect first, then convert.")


def fig_em():
    st = [[("C", BOT), ("5mC", HOT), ("5hmC", HOT)],
          [("C", BOT), ("5caC", HOT), ("5gmC", OK)],
          [("U", BAD), ("5caC", HOT), ("5gmC", OK)],
          [("T", BAD), ("C", OK), ("C", OK)]]
    return flow("EM-seq: the same logic as bisulfite, done with enzymes at low temperature.",
                ["start", "protect", "deaminate", "read after PCR"],
                ["TET2 + T4-BGT", "APOBEC3A", "PCR"], st,
                "Same readout as bisulfite, without the harsh chemistry that fragments DNA.", 740)


def fig_taps():
    st = [[("C", BOT), ("5mC", HOT), ("5hmC", HOT)],
          [("C", BOT), ("5caC", HOT), ("5caC", HOT)],
          [("C", BOT), ("DHU", BAD), ("DHU", BAD)],
          [("C", BOT), ("T", BAD), ("T", BAD)]]
    return flow("TAPS: convert only the modified bases. A T now marks a modification.",
                ["start", "oxidise", "reduce", "read after PCR"],
                ["TET", "pyridine borane", "PCR"], st,
                "Unmodified C is never touched, so the genome stays four-letter.", 740)


# ------------------------------------------------------------------ 10 reads under BS and TAPS

def fig_reads():
    ref = "ACCTGCGATCCATCGTCCAGCTACC"
    meth = {i for i, ch in enumerate(ref) if ch == "C" and ref[i + 1:i + 2] == "G"}
    bs = convert_bs(ref, meth)
    taps = "".join("T" if (ch == "C" and i in meth) else ch for i, ch in enumerate(ref))
    out = [t(40, 26, "The same molecule, read after each chemistry.", 14, INK)]
    x0 = 150
    rows = [("reference", ref, {i: (HOT if i in meth else BOT) for i, c in enumerate(ref) if c == "C"}),
            ("bisulfite", bs, cs_colors(ref, meth, bs)),
            ("TAPS", taps, cs_colors(ref, set(), taps))]
    for k, (lab, s, col) in enumerate(rows):
        y = 66 + k * 36
        out.append(t(x0 - 14, y, lab, 13, MUTE, anchor="end"))
        out.append(cs(x0, y, s, col))
    nc = ref.count("C")
    nb = sum(1 for a, b in zip(ref, bs) if a != b)
    nt = sum(1 for a, b in zip(ref, taps) if a != b)
    out.append(t(x0 + len(ref) * DX + 20, 66 + 36, f"{nb} of {nc} C changed", 13, BAD))
    out.append(t(x0 + len(ref) * DX + 20, 66 + 72, f"{nt} of {nc} C changed", 13, BAD))
    out.append(cap(40, 190, "Orange C carries a methyl group. In bisulfite most of the read changes; in TAPS "
                          "only the marked bases do.", 13, MUTE))
    out.append(cap(40, 236, "A read that is still four-letter aligns almost as well as an ordinary one.", 14, HOT))
    return svg(760, 228, "".join(out))


# ------------------------------------------------------------------ 11 RNA conversions

def fig_rna_conv():
    rna = "GGACUAGACAU"
    m = 2   # m6A at index 2
    out = [t(40, 26, "The same trick on RNA: make the modified base behave differently in the copy.", 14, INK)]
    x0 = 190
    out.append(t(40, 60, "RNA with one m6A", 13, MUTE))
    out.append(cs(x0, 60, rna, {m: HOT}))
    out.append(t(x0 + m * DX + 4, 42, "m6A", 11.5, HOT, anchor="middle"))
    # GLORI: unmodified A -> I (read G); m6A stays
    glori = "".join(("A" if i == m else "G") if ch == "A" else ch for i, ch in enumerate(rna))
    gcol = {i: (HOT if i == m else BAD) for i, ch in enumerate(rna) if ch == "A"}
    out.append(t(40, 104, "GLORI: nitrite", 13, MUTE))
    out.append(t(40, 120, "deaminates A to I", 12, MUTE))
    out.append(cs(x0, 108, glori.replace("U", "T"), gcol))
    out.append(t(x0 + 12 * DX + 16, 108, "A read as G: not modified. A still read as A: m6A.", 12.5, INK))
    # DART: C right after m6A edited
    dart = "".join("T" if i == m + 1 else ch for i, ch in enumerate(rna.replace("U", "T")))
    out.append(t(40, 164, "DART-seq: a deaminase", 13, MUTE))
    out.append(t(40, 180, "tethered to m6A", 12, MUTE))
    out.append(cs(x0, 168, dart, {m: HOT, m + 1: BAD}))
    out.append(t(x0 + 12 * DX + 16, 168, "C next to m6A read as T: marks a nearby m6A.", 12.5, INK))
    out.append(cap(40, 220, "GLORI works on every adenosine and counts the fraction modified. DART-seq edits "
                          "only beside a bound m6A reader.", 13, MUTE))
    return svg(780, 238, "".join(out))


# ------------------------------------------------------------------ 12 metabolic label

def fig_slam():
    out = [t(40, 26, "A label in newly made RNA, converted so the read shows it.", 14, INK)]
    x0 = 200
    rna_old = "AUGUUCUAUGC"
    out.append(t(x0 - 14, 66, "pre-existing RNA", 13, MUTE, anchor="end"))
    out.append(cs(x0, 66, rna_old))
    new = {1: 1, 3: 1, 6: 1}
    out.append(t(x0 - 14, 116, "new RNA (4sU fed)", 13, MUTE, anchor="end"))
    out.append(cs(x0, 116, rna_old, {i: HOT for i in new}))
    for i in new:
        out.append(t(x0 + i * DX + 4, 98, "4sU", 10.5, HOT, anchor="middle"))
    out.append(t(x0 + 11 * DX + 24, 116, "iodoacetamide alkylates 4sU", 12.5, MUTE))
    seq_old = rna_old.replace("U", "T")
    seq_new = "".join("C" if i in new else ch for i, ch in enumerate(seq_old))
    out.append(t(x0 - 14, 166, "read, old", 13, MUTE, anchor="end"))
    out.append(cs(x0, 166, seq_old))
    out.append(t(x0 - 14, 196, "read, new", 13, MUTE, anchor="end"))
    out.append(cs(x0, 196, seq_new, {i: BAD for i in new}))
    out.append(t(x0 + 11 * DX + 24, 196, "reverse transcriptase pairs G opposite", 12.5, MUTE))
    out.append(t(x0 + 11 * DX + 24, 212, "the alkylated base, so T reads as C", 12.5, MUTE))
    out.append(cap(40, 244, "T to C mismatches within a read are the age of that molecule. "
                          "The label is read, not enriched.", 14, HOT))
    return svg(780, 262, "".join(out))


# ------------------------------------------------------------------ 13 click

def fig_click():
    out = [t(40, 26, "Click chemistry turns a small tag into a handle you can pull on.", 14, INK)]
    # RNA strand with ethynyl uridines
    out.append(line(40, 90, 250, 90, TOP, 3))
    for x in (90, 160, 220):
        out.append(dot(x, 90, 5, HOT))
        out.append(line(x, 90, x, 66, HOT, 1.5))
    out.append(t(145, 56, "alkyne-labelled nucleoside", 12, HOT, anchor="middle"))
    out.append(t(145, 116, "in newly made RNA", 12, MUTE, anchor="middle"))
    out.append(arrow(260, 90, 330, MUTE, 1.5))
    out.append(box(336, 74, 110, 32, "azide-biotin", PALE_OK, OK, 13, OK))
    out.append(t(391, 126, "covalent triazole link", 11.5, MUTE, anchor="middle"))
    out.append(arrow(456, 90, 520, MUTE, 1.5))
    out.append(f'<circle cx="580" cy="90" r="34" fill="{PALE_TOP}" stroke="{TOP}" stroke-width="1.4"/>')
    out.append(t(580, 86, "streptavidin", 11.5, TOP, anchor="middle"))
    out.append(t(580, 101, "bead", 11.5, TOP, anchor="middle"))
    out.append(t(580, 148, "keep what was labelled,", 12, MUTE, anchor="middle"))
    out.append(t(580, 164, "wash the rest away", 12, MUTE, anchor="middle"))
    out.append(cap(40, 204, "This is enrichment by a covalent tag. It survives stringent washes that would "
                          "strip an antibody.", 14, HOT))
    return svg(720, 224, "".join(out))


# ------------------------------------------------------------------ 14 position is information

def fig_position():
    out = [t(40, 26, "Three ways to write a position into a read.", 14, INK)]
    titles = ["1. an enzyme stalls", "2. an enzyme cuts", "3. a ligase joins"]
    for p in range(3):
        x0 = 40 + p * 270
        out.append(t(x0, 58, titles[p], 13.5, INK))
        out.append(line(x0, 100, x0 + 230, 100, TOP, 3))
        if p == 0:
            out.append(dot(x0 + 90, 100, 7, HOT))
            out.append(line(x0 + 230, 118, x0 + 90, 118, BOT, 2.4))
            out.append(vtick(x0 + 90, 112, 124, BAD, 3))
            out.append(t(x0, 146, "extension stops at a lesion,", 12, MUTE))
            out.append(t(x0, 162, "so the cDNA end marks it", 12, MUTE))
        elif p == 1:
            for cx in (70, 100, 130):
                out.append(line(x0 + cx, 86, x0 + cx, 114, HOT, 2))
            out.append(t(x0 + 100, 76, "cuts only where accessible", 11.5, HOT, anchor="middle"))
            out.append(t(x0, 146, "each fragment end is a", 12, MUTE))
            out.append(t(x0, 162, "cut, hence a position", 12, MUTE))
        else:
            out.append(box(x0 + 40, 90, 70, 20, "A", PALE_TOP, TOP, 12, TOP))
            out.append(box(x0 + 110, 90, 70, 20, "B", PALE_HOT, HOT, 12, HOT))
            out.append(t(x0 + 110, 84, "junction", 11.5, BAD, anchor="middle"))
            out.append(t(x0, 146, "the read crosses from A to B,", 12, MUTE))
            out.append(t(x0, 162, "so A and B were together", 12, MUTE))
    out.append(cap(40, 200, "In each case the base sequence is ordinary. The information is where the "
                          "read starts or ends.", 14, HOT))
    return svg(840, 218, "".join(out))


# ------------------------------------------------------------------ 15 iCLIP truncation

def fig_iclip():
    out = [t(40, 26, "Crosslinked protein stops reverse transcriptase one base short of the contact.",
             14, INK)]
    y = 94
    out.append(line(60, y, 560, y, TOP, 3))
    out.append(t(48, y + 4, "5'", 12, MUTE, anchor="end"))
    out.append(t(570, y + 4, "3'", 12, MUTE))
    # protein
    out.append(f'<circle cx="300" cy="{y-30}" r="20" fill="{PALE_HOT}" stroke="{HOT}" stroke-width="1.4"/>')
    out.append(t(300, y - 26, "RBP", 12, HOT, anchor="middle"))
    out.append(line(300, y - 10, 300, y, HOT, 2.2, "3 2"))
    out.append(t(328, y - 12, "UV crosslink", 11.5, HOT))
    # cDNAs
    for k, (end, thru) in enumerate([(298, False), (298, False), (298, False), (298, False), (120, True)]):
        yy = y + 22 + k * 11
        out.append(line(end, yy, 540, yy, BOT, 2.2))
        if not thru:
            out.append(vtick(end, yy - 4, yy + 4, BAD, 2.6))
    out.append(t(570, y + 40, "cDNA", 12, MUTE))
    out.append(t(570, y + 70, "read-through", 11.5, MUTE))
    # histogram, clear of the cDNA stack above it
    out.append(line(60, 212, 560, 212, MUTE, 1))
    out.append(f'<rect x="293" y="{212-42}" width="9" height="42" fill="{BAD}"/>')
    out.append(f'<rect x="110" y="{212-5}" width="180" height="5" fill="{MUTE}"/>')
    out.append(t(312, 204, "read starts pile up", 12, BAD))
    out.append(cap(60, 234, "Read 5' ends, one count per molecule. The peak is the binding site at "
                          "single-nucleotide resolution.", 13, INK))
    return svg(780, 252, "".join(out))


# ------------------------------------------------------------------ 16 PAR-CLIP

def fig_parclip():
    out = [t(40, 26, "PAR-CLIP: a label that crosslinks, and leaves a mutation as its signature.", 14, INK)]
    ref = "GAUUCGAUUAGCUUCAUGGUC".replace("U", "T")
    x0 = 70
    out.append(cs(x0, 66, ref, {i: HOT for i, c in enumerate(ref) if c == "T"}))
    out.append(t(x0, 46, "4-thiouridine replaces U in living cells (orange)", 12, HOT))
    site = 8          # must be a T: the mismatch is a crosslinked 4sU read as C
    assert ref[site] == "T"
    random.seed(4)
    for k in range(6):
        y = 96 + k * 14
        out.append(line(x0 + random.randint(0, 6) * DX, y, x0 + random.randint(15, 21) * DX, y, BOT, 4))
        out.append(f'<rect x="{x0 + site * DX}" y="{y-4}" width="{DX-2}" height="8" fill="{BAD}"/>')
    out.append(t(x0 + 22 * DX + 16, 108, "T to C at the", 12.5, BAD))
    out.append(t(x0 + 22 * DX + 16, 124, "crosslinked base in", 12.5, BAD))
    out.append(t(x0 + 22 * DX + 16, 140, "most reads", 12.5, BAD))
    out.append(cap(x0, 206, "Crosslinked 4sU is read as C. An ordinary T to C mismatch elsewhere is background; "
                          "a pile of them at one base is the site.", 13, INK))
    return svg(780, 224, "".join(out))


# ------------------------------------------------------------------ 17 probing

def fig_probing():
    stem1, loop, stem2 = "GGACGUA", "AACAAC", "UACGUCC"
    check_pairing(stem1, stem2[::-1])
    full = stem1 + loop + stem2
    out = [t(40, 26, "A reagent marks the bases that are free to react. The copy records the mark.", 14, INK)]
    x0 = 120
    out.append(t(x0 - 14, 150, "RNA", 13, MUTE, anchor="end"))
    col = {}
    for i, ch in enumerate(full):
        if len(stem1) <= i < len(stem1) + len(loop) and ch in "AC":
            col[i] = HOT
    out.append(cs(x0, 150, full, col))
    out.append(t(x0 + 4, 172, "stem", 11.5, MUTE))
    out.append(t(x0 + len(stem1) * DX, 172, "loop: unpaired", 11.5, HOT))
    out.append(t(x0 + (len(stem1) + len(loop)) * DX + 4, 172, "stem", 11.5, MUTE))
    out.append(line(x0 - 4, 126, x0 + len(full) * DX, 126, MUTE, 1))
    for i, ch in enumerate(full):
        h = 4
        if len(stem1) <= i < len(stem1) + len(loop) and ch in "AC":
            h = 70
        elif ch in "AC":
            h = 8
        out.append(f'<rect x="{x0 + i * DX + 1}" y="{126 - h}" width="{DX - 4}" height="{h}" '
                   f'fill="{HOT if h > 20 else GRID}"/>')
    out.append(t(x0 - 14, 100, "mutations", 12, MUTE, anchor="end"))
    out.append(t(x0 - 14, 114, "per read", 12, MUTE, anchor="end"))
    out.append(cap(40, 204, "DMS methylates unpaired A and C. A group II intron reverse transcriptase reads "
                          "through and mis-copies them.", 13, INK))
    return svg(780, 222, "".join(out))


# ------------------------------------------------------------------ 18 cuts

def fig_cuts():
    out = [t(40, 26, "An enzyme that cuts only where it can reach turns accessibility into read starts.",
             14, INK)]
    y = 92
    out.append(line(40, y, 700, y, TOP, 3))
    nuc = [60, 120, 180, 480, 540, 600, 660]
    for cx in nuc:
        out.append(f'<ellipse cx="{cx}" cy="{y}" rx="23" ry="15" fill="{PALE_TOP}" stroke="{TOP}" '
                   f'stroke-width="1.2"/>')
    out.append(t(120, y + 38, "nucleosomes protect DNA", 12, MUTE, anchor="middle"))
    out.append(t(340, y + 38, "open region", 12, HOT, anchor="middle"))
    for cx in (250, 290, 320, 340, 370, 420):
        out.append(line(cx, y - 24, cx, y - 4, HOT, 2))
    out.append(t(340, y - 32, "Tn5, DNase I or MNase cut here", 12, HOT, anchor="middle"))
    out.append(line(40, 196, 700, 196, MUTE, 1))
    for cx, h in [(250, 22), (290, 34), (320, 44), (340, 52), (370, 40), (420, 20)]:
        out.append(f'<rect x="{cx - 4}" y="{196 - h}" width="8" height="{h}" fill="{BAD}"/>')
    out.append(t(40, 216, "read-start count per base", 12, MUTE))
    out.append(cap(40, 242, "Cuts inside nucleosomes are rare, so the read track is the accessibility map.", 14, HOT))
    return svg(740, 260, "".join(out))


# ------------------------------------------------------------------ 19 junctions

def fig_junction():
    out = [t(40, 26, "Proximity ligation turns contact into a chimeric read.", 14, INK)]
    # chromatin loop
    # the protein first, so the loop feet sit inside it: the label needs a subject
    out.append(f'<ellipse cx="140" cy="120" rx="88" ry="15" fill="{PALE_TOP}" stroke="{TOP}" '
               f'stroke-width="1.2"/>')
    out.append(f'<path d="M 60 120 C 60 50, 220 50, 220 120" fill="none" stroke="{TOP}" stroke-width="3"/>')
    out.append(line(20, 120, 60, 120, TOP, 3))
    out.append(line(220, 120, 330, 120, TOP, 3))
    out.append(dot(60, 120, 7, HOT))
    out.append(dot(220, 120, 7, BAD))
    out.append(t(60, 148, "locus A", 12, HOT, anchor="middle"))
    out.append(t(220, 148, "locus B", 12, BAD, anchor="middle"))
    # short enough to sit inside the loop without the arc crossing it
    out.append(t(140, 96, "held by protein", 11.5, MUTE, anchor="middle"))
    out.append(arrow(340, 90, 400, MUTE, 1.5))
    out.append(t(370, 80, "cut, ligate", 11.5, MUTE, anchor="middle"))
    out.append(box(420, 76, 70, 22, "A", PALE_HOT, HOT, 13, HOT))
    out.append(box(490, 76, 70, 22, "B", "#f3e3df", BAD, 13, BAD))
    out.append(t(490, 70, "junction", 11.5, MUTE, anchor="middle"))
    out.append(t(420, 126, "one read, two alignments:", 12, INK))
    out.append(t(420, 144, "chr1 at A, and chr1 800 kb away at B", 12, MUTE))
    out.append(cap(40, 194, "The ligase writes the contact into a single molecule. No property is measured; "
                          "the join is the measurement.", 14, HOT))
    return svg(720, 212, "".join(out))


# ------------------------------------------------------------------ 20 antibody

def fig_antibody():
    out = [t(40, 26, "An antibody pulls out modified fragments. Nothing is converted.", 14, INK)]
    random.seed(7)
    y = 80
    for k in range(10):
        x = 40 + k * 46
        out.append(line(x, y, x + 34, y, TOP, 3))
        if k in (1, 4, 5, 8):
            out.append(dot(x + 17, y, 5, HOT))
            out.append(t(x + 17, y - 12, "Y", 13, OK, anchor="middle", weight="bold"))
    out.append(t(40, 50, "fragmented DNA, some carrying 5mC", 12, MUTE))
    out.append(arrow(500, y, 560, MUTE, 1.5))
    out.append(t(530, y - 10, "pull down", 11.5, MUTE, anchor="middle"))
    for k, x in enumerate((580, 628)):
        out.append(line(x, y, x + 34, y, TOP, 3))
        out.append(dot(x + 17, y, 5, HOT))
    out.append(t(580, y + 22, "enriched fragments", 11.5, MUTE))
    # coverage: two tracks, so the input line is not drawn underneath the IP curve
    out.append(line(40, 190, 700, 190, MUTE, 1))
    pts = " ".join(f"{40 + i * 4},{190 - (46 * math.exp(-((i * 4 - 200) / 45) ** 2) + 3)}"
                   for i in range(0, 166))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{BAD}" stroke-width="2"/>')
    out.append(t(330, 152, "IP: a peak about one fragment wide", 12, BAD))
    out.append(line(40, 228, 700, 228, MUTE, 1))
    pts2 = " ".join(f"{40 + i * 4},{228 - 3}" for i in range(0, 166))
    out.append(f'<polyline points="{pts2}" fill="none" stroke="{MUTE}" stroke-width="2" stroke-dasharray="4 3"/>')
    out.append(t(40, 248, "input control: flat, no peak", 12, MUTE))
    out.append(cap(40, 274, "The signal is a region, not a base, and it scales with how many modified bases "
                          "sit in the fragment.", 13, INK))
    return svg(740, 292, "".join(out))


# ------------------------------------------------------------------ 21 trade-offs

def fig_tradeoff():
    out = [t(40, 26, "Three readouts, three kinds of answer.", 14, INK)]
    header = ["readout", "answers", "resolution", "input", "main weakness"]
    rows = [["conversion", "which base, how often", "one base", "ng to pg", "a read is mostly one chemistry"],
            ["antibody", "where it is enriched", "100 to 500 bp", "ng, more for IP", "antibody specificity, density bias"],
            ["native", "which base, per molecule", "one base", "ug of DNA", "needs trained basecalling"]]
    out.append(table(40, 40, [110, 160, 110, 130, 300], 34, header, rows, 12.5))
    out.append(cap(40, 206, "Pick the readout by the question: a map of where, a fraction at a base, or "
                          "a pattern along one molecule.", 13, MUTE))
    return svg(880, 224, "".join(out))


# ------------------------------------------------------------------ 22 PacBio kinetics

def fig_pacbio():
    out = [t(40, 26, "The polymerase pauses at a modified base. The pause is the signal.", 14, INK)]
    bases = "GATCGATCGGA"
    x0 = 260
    for row, (lab, slow) in enumerate([("unmodified template", None), ("template with a modification", 3)]):
        y = 90 + row * 80
        out.append(t(40, y - 20, lab, 12.5, MUTE))
        x = x0
        for i, b in enumerate(bases):
            gap = 52 if i == slow else 26
            out.append(vtick(x, y - 28, y, BAD if i == slow else TOP, 3))
            out.append(t(x, y + 16, b, 13, HOT if i == slow else INK, anchor="middle", family=MONO))
            x += gap
        if slow is not None:
            xs = x0 + slow * 26 + 26
            out.append(line(xs - 26 + 3, y - 36, xs - 26 + 52 - 3, y - 36, HOT, 1.2))
            out.append(t(xs, y - 44, "longer inter-pulse duration", 11.5, HOT, anchor="middle"))
    out.append(cap(40, 222, "Each pulse is a base being incorporated. Averaged over many passes of a circular "
                          "molecule, the delay calls the base.", 13, INK))
    return svg(780, 240, "".join(out))


# ------------------------------------------------------------------ 23 nanopore

def fig_nanopore():
    out = [t(40, 26, "In a pore, a modified base shifts the current for every k-mer it sits in.", 14, INK)]
    levels = [60, 80, 50, 72, 40, 66, 54, 78]
    for row, (lab, shifted) in enumerate([("unmodified", set()), ("5mC present", {3, 4, 5})]):
        x0 = 60 + row * 360
        out.append(t(x0, 52, lab, 13, INK))
        out.append(line(x0, 160, x0 + 300, 160, GRID, 1))
        x = x0
        for i, lv in enumerate(levels):
            v = lv + (16 if i in shifted else 0)
            col = BAD if i in shifted else TOP
            out.append(line(x, 160 - v, x + 36, 160 - v, col, 3))
            if i < len(levels) - 1:
                nv = levels[i + 1] + (16 if (i + 1) in shifted else 0)
                out.append(line(x + 36, 160 - v, x + 36, 160 - nv, MUTE, 1))
            x += 36
    out.append(t(60, 182, "time, one level per k-mer in the pore", 11.5, MUTE))
    out.append(cap(60, 220, "A model trained on known modified DNA reads the shift as 5mC or C. "
                          "The read is the molecule itself, no copy.", 13, INK))
    return svg(760, 238, "".join(out))


# ------------------------------------------------------------------ 24 reduced representation

def fig_rrbs():
    out = [t(40, 26, "Cut at a CpG-containing site, keep only small fragments: read where it matters.", 14, INK)]
    y = 76
    out.append(line(40, y, 700, y, TOP, 3))
    out.append(box(110, y - 14, 70, 28, "", PALE_OK, OK))
    out.append(box(420, y - 14, 110, 28, "", PALE_OK, OK))
    out.append(t(145, y - 22, "CpG island", 11.5, OK, anchor="middle"))
    out.append(t(475, y - 22, "CpG island", 11.5, OK, anchor="middle"))
    cuts = [70, 100, 130, 150, 170, 250, 330, 440, 460, 480, 500, 520, 610, 650]
    for cx in cuts:
        out.append(vtick(cx, y - 10, y + 10, HOT, 2))
    out.append(t(40, y + 32, "MspI sites (CCGG), dense in CpG islands", 12, HOT))
    out.append(line(40, 150, 700, 150, MUTE, 1))
    out.append(t(40, 140, "fragments, 40 to 220 bp kept", 12, MUTE))
    kept = [(70, 100), (100, 130), (130, 150), (150, 170), (440, 460), (460, 480), (480, 500), (500, 520)]
    for a, b in kept:
        out.append(f'<rect x="{a + 2}" y="156" width="{b - a - 4}" height="9" fill="{BAD}"/>')
    for a, b in [(170, 250), (250, 330), (330, 440), (520, 610), (610, 650)]:
        out.append(f'<rect x="{a + 2}" y="156" width="{b - a - 4}" height="9" fill="{GRID}"/>')
    out.append(t(310, 190, "long fragments are discarded", 12, MUTE, anchor="middle"))
    out.append(cap(40, 224, "A small, CpG-rich fraction of the genome, read deeply, for a fraction of the "
                          "sequencing cost.", 14, HOT))
    return svg(740, 242, "".join(out))


# ------------------------------------------------------------------ 25 controls summary

def fig_ctrl_table():
    out = [t(40, 26, "Every readout has a control that measures its false positives.", 14, INK)]
    header = ["readout", "control", "what it tells you"]
    rows = [["conversion", "unmethylated and methylated spike-ins", "conversion rate, over-conversion"],
            ["metabolic label", "same cells, no label", "background T to C from errors and SNPs"],
            ["crosslinking", "size-matched input, no-UV sample", "what sticks without the protein"],
            ["antibody", "input and non-specific IgG", "fragment bias, sticky background"],
            ["probing", "no reagent, DMSO only", "reverse transcriptase error rate"],
            ["native", "amplified unmodified DNA", "the signal with no modification"]]
    out.append(table(40, 40, [140, 280, 340], 30, header, rows, 12.5))
    out.append(cap(40, 278, "Run the control in the same tube series. A control run on another day measures "
                          "the day, not the method.", 13, MUTE))
    return svg(820, 270, "".join(out))


build(__file__, [
    ("routes", fig_routes),
    ("copy", fig_copy),
    ("bisulfite", fig_bisulfite),
    ("align", fig_align),
    ("controls", fig_controls),
    ("matrix", fig_matrix),
    ("tab-seq", fig_tab),
    ("em-seq", fig_em),
    ("taps", fig_taps),
    ("reads", fig_reads),
    ("rna-conversion", fig_rna_conv),
    ("slam", fig_slam),
    ("click", fig_click),
    ("position", fig_position),
    ("iclip", fig_iclip),
    ("parclip", fig_parclip),
    ("probing", fig_probing),
    ("cuts", fig_cuts),
    ("junction", fig_junction),
    ("antibody", fig_antibody),
    ("tradeoff", fig_tradeoff),
    ("pacbio", fig_pacbio),
    ("nanopore", fig_nanopore),
    ("rrbs", fig_rrbs),
    ("ctrl-table", fig_ctrl_table),
])
