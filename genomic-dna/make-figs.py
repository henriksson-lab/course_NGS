#!/usr/bin/env python3
"""Figures for the genomic-dna unit.  Run: python3 genomic-dna/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE = "#eef2f6"
PALE_HOT = "#f7e7dd"
PALE_OK = "#e3efe6"
PALE_BAD = "#f4e0dc"
ADA = "#c98a2b"      # adapter colour


def path(d, stroke=INK, w=1.6, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def rect(x, y, w, h, fill, stroke="none", r=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def flow(x, y, labels, w, h, gap, fill=PALE, size=13):
    out = []
    for i, lab in enumerate(labels):
        xi = x + i * (w + gap)
        out.append(box(xi, y, w, h, lab, fill=fill, size=size))
        if i < len(labels) - 1:
            out.append(arrow(xi + w + 3, y + h / 2, xi + w + gap - 3, MUTE))
    return "".join(out)


# ------------------------------------------------------------------ figures

def fig_recipe():
    out = [t(30, 26, "Every genomic library is the same five blocks; the sample decides which variant of each.", 14)]
    labels = ["1 Fragment", "2 End chemistry", "3 Handle", "4 Amplify?", "5 QC"]
    notes = [("size, randomness", "shear / enzyme / Tn5"),
             ("blunt, 5'-P, A-tail", "or none (Tn5)"),
             ("ligate adapter", "or transpose it in"),
             ("PCR cycles: 0 to 15", "or whole-genome amp."),
             ("size, yield, dup. rate", "GC curve, coverage")]
    out.append(flow(30, 46, labels, 132, 42, 26))
    for i, (a, b) in enumerate(notes):
        cx = 30 + i * 158 + 66
        out.append(t(cx, 112, a, 12, MUTE, anchor="middle"))
        out.append(t(cx, 128, b, 12, MUTE, anchor="middle"))
    return svg(800, 146, "".join(out))


def fig_input_scale():
    out = [t(20, 24, "How much DNA you have decides the route (log scale, mass of DNA per library).", 14)]
    x0, perdec = 310, 62.0
    y_axis = 214

    def X(pg):
        return x0 + math.log10(pg) * perdec
    out.append(line(x0, y_axis, X(1e7), y_axis, MUTE, 1.2))
    for pg, lab in [(1, "1 pg"), (10, "10 pg"), (100, "100 pg"), (1e3, "1 ng"), (1e4, "10 ng"),
                    (1e5, "100 ng"), (1e6, "1 µg"), (1e7, "10 µg")]:
        out.append(line(X(pg), y_axis - 4, X(pg), y_axis + 4, MUTE, 1.2))
        out.append(t(X(pg), y_axis + 20, lab, 12, MUTE, anchor="middle"))
    rows = [
        ("one human cell, about 6.5 pg", 6.5, 6.5, HOT, "whole-genome amplification"),
        ("Nextera XT (designed around 1 ng)", 1e3, 1e3, ADA, ""),
        ("Illumina DNA Prep, 1 to 500 ng", 1e3, 5e5, ADA, ""),
        ("NEBNext Ultra II FS PCR-free, 100 to 500 ng", 1e5, 5e5, OK, ""),
        ("TruSeq DNA PCR-free, about 1 to 2 µg", 1e6, 2e6, OK, ""),
    ]
    for i, (lab, lo, hi, col, note) in enumerate(rows):
        y = 52 + i * 31
        out.append(t(x0 - 12, y + 4, lab, 12.5, INK, anchor="end"))
        if lo == hi:
            out.append(dot(X(lo), y, 6, col))
            if note:
                out.append(t(X(lo) + 14, y + 4, note, 12.5, col))
        else:
            out.append(rect(X(lo), y - 7, X(hi) - X(lo), 14, col))
    out.append(line(X(1e5), 40, X(1e5), y_axis, MUTE, 1, dash="3 4"))
    out.append(t(X(1e5) + 6, 40, "PCR-free is possible from here", 12, OK))
    return svg(780, 246, "".join(out))


def frag_row(x, y, cuts, length, col, tag=False, ragged=False):
    out = []
    edges = [0] + cuts + [length]
    for a, b in zip(edges[:-1], edges[1:]):
        g = 3
        s, e = x + a + (g if a else 0), x + b - (g if b < length else 0)
        out.append(line(s, y, e, y, TOP, 3))
        if tag:
            if a:
                out.append(rect(s - 5, y - 5, 5, 10, ADA))
            if b < length:
                out.append(rect(e, y - 5, 5, 10, ADA))
        if ragged:
            if a:
                out.append(line(s, y, s + 5, y + 5, BAD, 1.5))
            if b < length:
                out.append(line(e, y, e - 5, y - 5, BAD, 1.5))
    return "".join(out)


def fig_fragmentation():
    out = [t(20, 24, "Three ways to cut genomic DNA to size, and what each leaves on the ends.", 14)]
    cuts = [70, 150, 190, 290]
    rows = [("Acoustic shearing (Covaris)", dict(ragged=True),
             "random breaks, ragged ends: needs end repair + A-tailing", BAD),
            ("Enzymatic (e.g. NEBNext FS)", dict(),
             "ends repaired and A-tailed in the same tube", OK),
            ("Tn5 tagmentation", dict(tag=True),
             "cut and adapter attached in one step", ADA)]
    for i, (name, kw, note, col) in enumerate(rows):
        y = 78 + i * 62
        out.append(t(20, y - 22, name, 13, INK, weight="bold"))
        out.append(frag_row(40, y, cuts, 340, TOP, **kw))
        out.append(t(400, y + 4, note, 12.5, col))
    return svg(780, 232, "".join(out))


def fig_ligation_library():
    out = [t(20, 24, "Ligation library: repair, A-tail, then ligate a forked adapter.", 14)]
    # insert
    out.append(line(220, 92, 440, 92, TOP, 3))
    out.append(line(220, 106, 440, 106, BOT, 3))
    out.append(t(444, 97, "A", 15, HOT, family=MONO, weight="bold"))
    out.append(t(206, 112, "A", 15, HOT, family=MONO, weight="bold", anchor="end"))
    out.append(t(330, 130, "insert, ends repaired, one A on each 3' end", 12.5, MUTE, anchor="middle"))
    # adapters: Y shape with T overhang
    for sign, x in ((-1, 196), (1, 468)):
        out.append(line(x, 92, x + sign * 22, 92, ADA, 3))
        out.append(line(x, 106, x + sign * 22, 106, ADA, 3))
        out.append(line(x + sign * 22, 92, x + sign * 50, 66, ADA, 3))
        out.append(line(x + sign * 22, 106, x + sign * 50, 132, ADA, 3))
    out.append(t(176, 100, "T", 15, HOT, family=MONO, weight="bold", anchor="end"))
    out.append(t(484, 100, "T", 15, HOT, family=MONO, weight="bold"))
    out.append(t(100, 62, "forked adapter", 12.5, ADA, anchor="middle"))
    out.append(t(100, 160, "arms stay unpaired: the fork", 12.5, MUTE, anchor="middle"))
    out.append(t(20, 190, "A/T overhangs stop insert-insert and adapter-adapter joining. Each fragment gets "
                          "an adapter at both ends.", 13.5, INK))
    out.append(t(20, 210, "A full-length adapter (P5/P7 and index already present) makes PCR unnecessary.", 13.5, INK))
    return svg(640, 226, "".join(out))


def fig_tagmentation():
    out = [t(20, 24, "Tagmentation: a loaded Tn5 dimer cuts and joins adapters to the 5' ends.", 14)]
    # panel A
    out.append(line(30, 70, 340, 70, TOP, 3))
    out.append(line(30, 84, 340, 84, BOT, 3))
    out.append(rect(150, 48, 70, 58, PALE_HOT, HOT, 8))
    out.append(t(185, 80, "Tn5", 14, HOT, anchor="middle", weight="bold"))
    out.append(t(185, 124, "dimer, adapters loaded", 12, MUTE, anchor="middle"))
    out.append(line(160, 40, 160, 48, HOT, 1.5))
    out.append(line(210, 106, 210, 114, HOT, 1.5))
    out.append(t(20, 50, "cut", 11.5, HOT))
    out.append(arrow(360, 78, 400, MUTE))
    # panel B: result, one fragment
    y1, y2 = 62, 96
    out.append(line(420, y1, 640, y1, TOP, 3))
    out.append(line(432, y2, 652, y2, BOT, 3))
    out.append(rect(404, y1 - 5, 16, 10, ADA))
    out.append(rect(652, y2 - 5, 16, 10, ADA))
    out.append(line(420, y2, 432, y2, BAD, 1.5, dash="2 3"))
    out.append(line(640, y1, 652, y1, BAD, 1.5, dash="2 3"))
    out.append(t(412, 52, "adapter", 11.5, ADA))
    out.append(t(536, 124, "9 nt gap on each side", 12, BAD, anchor="middle"))
    out.append(t(536, 140, "filled by polymerase at 72 °C", 12, MUTE, anchor="middle"))
    out.append(t(20, 180, "No end repair, no A-tail, no ligase: fragmentation and adapter attachment are one reaction. "
                          "The price is a sequence preference.", 13.5, INK))
    return svg(700, 198, "".join(out))


def fig_gc_curve():
    out = [t(20, 24, "Relative coverage by GC content of the fragment (schematic).", 14)]
    x0, y0, w, h = 60, 50, 380, 160
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    out.append(t(x0 + w / 2, y0 + h + 30, "GC content of fragment", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 12, "1", 12, MUTE, anchor="end"))
    out.append(t(x0, y0 + h + 16, "0%", 12, MUTE, anchor="middle"))
    out.append(t(x0 + w, y0 + h + 16, "100%", 12, MUTE, anchor="middle"))
    ymid = y0 + h * 0.4
    out.append(line(x0, ymid, x0 + w, ymid, MUTE, 1, dash="4 4"))
    # PCR-free: gentle
    pts1, pts2 = [], []
    for i in range(0, 41):
        u = i / 40.0
        g = (u - 0.45)
        pts1.append((x0 + u * w, ymid + 18 * (g * g * 4) - 2))
        pts2.append((x0 + u * w, ymid + 60 * (g * g * 4) * (1.0 if u > 0.45 else 0.55) - 6))
    out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts1), OK, 2.4))
    out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts2), BAD, 2.4))
    out.append(t(x0 + w + 12, ymid + 26, "PCR-free: close to flat", 13, OK))
    out.append(t(x0 + w + 12, ymid + 74, "PCR-amplified: dips at", 13, BAD))
    out.append(t(x0 + w + 12, ymid + 90, "high and low GC", 13, BAD))
    return svg(700, 270, "".join(out))


def fig_compounding():
    out = [t(20, 24, "A small efficiency difference per cycle compounds (illustrative: 90% vs 80% per cycle).", 14)]
    cyc = [0, 4, 8, 12]
    x0, base = 70, 200
    scale = 150.0 / math.log10(2300.0)
    for j, n in enumerate(cyc):
        xg = x0 + j * 140
        va, vb = 1.9 ** n, 1.8 ** n
        ha = max(2, math.log10(va) * scale) if n else 2
        hb = max(2, math.log10(vb) * scale) if n else 2
        out.append(rect(xg, base - ha, 34, ha, TOP))
        out.append(rect(xg + 40, base - hb, 34, hb, HOT))
        out.append(t(xg + 37, base + 18, f"{n} cycles", 12.5, MUTE, anchor="middle"))
        out.append(t(xg + 17, base - ha - 5, f"{va:.0f}x", 11.5, TOP, anchor="middle"))
        out.append(t(xg + 57, base - hb - 5, f"{vb:.0f}x", 11.5, HOT, anchor="middle"))
    out.append(line(x0 - 10, base, x0 + 3 * 140 + 84, base, MUTE, 1.2))
    out.append(rect(640, 60, 12, 12, TOP))
    out.append(t(658, 71, "90% per cycle", 12.5))
    out.append(rect(640, 82, 12, 12, HOT))
    out.append(t(658, 93, "80% per cycle", 12.5))
    out.append(t(640, 130, "After 12 cycles the first", 12.5, INK))
    out.append(t(640, 146, f"is {1.9**12 / 1.8**12:.1f} times the second.", 12.5, INK))
    out.append(t(640, 170, "(bars on a log scale)", 11.5, MUTE))
    return svg(800, 234, "".join(out))


def fig_duplicates():
    out = [t(20, 24, "Reads piled on a reference: which stacks are real?", 14)]
    out.append(line(40, 190, 700, 190, INK, 2))
    out.append(t(24, 194, "ref", 11.5, MUTE, anchor="end"))
    groups = [
        (70, "PCR duplicates", "one molecule, several copies;|identical start and end", BAD, 4),
        (270, "chance coincidence", "two molecules cut at|the same place", HOT, 2),
        (470, "distinct molecules", "different start and end:|independent evidence", OK, 1),
    ]
    for x, name, note, col, n in groups:
        if col == OK:
            for k, (a, b) in enumerate([(0, 90), (30, 130), (60, 120)]):
                out.append(line(x + a, 170 - k * 14, x + b, 170 - k * 14, col, 5))
        else:
            for k in range(n):
                out.append(line(x, 170 - k * 14, x + 90, 170 - k * 14, col, 5))
        out.append(t(x, 90, name, 13.5, col, weight="bold"))
        for k, ln in enumerate(note.split("|")):
            out.append(t(x, 108 + k * 14, ln, 12, MUTE))
    out.append(t(20, 226, "Marking duplicates by coordinates cannot tell the first two apart. "
                          "A random UMI can.", 13.5, INK))
    return svg(760, 244, "".join(out))


def fig_complexity():
    out = [t(20, 24, "Fraction of reads that are new molecules, by sequencing depth relative to library complexity.", 14)]
    x0, y0, w, h = 70, 50, 400, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    xmax = 4.0
    pts = []
    for i in range(1, 81):
        x = xmax * i / 80
        f = (1 - math.exp(-x)) / x
        pts.append((x0 + x / xmax * w, y0 + h - f * h))
    out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), TOP, 2.4))
    for xv in (0.1, 1.0, 3.0):
        f = (1 - math.exp(-xv)) / xv
        px, py = x0 + xv / xmax * w, y0 + h - f * h
        out.append(dot(px, py, 5, HOT))
        out.append(t(px + 8, py - 8, f"{xv:g}x: {f*100:.0f}% unique", 12.5, HOT))
    out.append(t(x0 + w / 2, y0 + h + 30, "reads sequenced / distinct molecules in the library", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 6, "100%", 11.5, MUTE, anchor="end"))
    out.append(t(x0 - 8, y0 + h, "0", 11.5, MUTE, anchor="end"))
    for xv in (0, 1, 2, 3, 4):
        out.append(t(x0 + xv / xmax * w, y0 + h + 16, str(xv), 11.5, MUTE, anchor="middle"))
    out.append(t(500, 110, "unique = (1 - e^-x) / x", 13, INK, family=MONO))
    out.append(t(500, 132, "for x reads per molecule", 12.5, MUTE))
    return svg(780, 262, "".join(out))


def fig_adapter_types():
    out = [t(20, 24, "Why PCR-free adapters are full length.", 14)]
    def construct(y, stub):
        parts = [("P5", 40, ADA), ("i5", 30, HOT), ("R1", 50, BOT), ("insert", 150, TOP),
                 ("R2", 50, BOT), ("i7", 30, HOT), ("P7", 40, ADA)]
        x = 40
        o = []
        for name, wd, col in parts:
            ghost = stub and name in ("P5", "i5", "i7", "P7")
            o.append(rect(x, y, wd - 2, 24, "none" if ghost else col, MUTE if ghost else "none"))
            o.append(t(x + wd / 2 - 1, y + 16, name, 11.5, MUTE if ghost else "#ffffff", anchor="middle"))
            x += wd
        return "".join(o)
    out.append(t(40, 54, "PCR-free: everything is ligated on", 13, OK, weight="bold"))
    out.append(construct(62, False))
    out.append(t(40, 130, "With PCR: stub adapters, the primers add the rest (dashed)", 13, BAD, weight="bold"))
    out.append(construct(138, True))
    out.append(t(520, 82, "goes straight to the flow cell,", 12.5, MUTE))
    out.append(t(520, 98, "must be quantified by qPCR", 12.5, MUTE))
    out.append(t(520, 158, "amplification also rescues", 12.5, MUTE))
    out.append(t(520, 174, "low input, but adds bias", 12.5, MUTE))
    return svg(760, 196, "".join(out))


def fig_damage():
    out = [t(20, 24, "Ancient DNA: C to T changes pile up at the ends of reads (schematic).", 14)]
    x0, w = 60, 250
    for k, (name, both) in enumerate([("double-stranded library", False), ("single-stranded library", True)]):
        xo = x0 + k * 360
        y0, h = 56, 120
        out.append(line(xo, y0 + h, xo + w, y0 + h, MUTE, 1.2))
        out.append(line(xo, y0, xo, y0 + h, MUTE, 1.2))
        out.append(t(xo + w / 2, y0 - 12, name, 13, INK, anchor="middle", weight="bold"))
        out.append(t(xo + w / 2, y0 + h + 28, "position in read", 12, MUTE, anchor="middle"))
        out.append(t(xo, y0 + h + 14, "5' end", 11.5, MUTE, anchor="middle"))
        out.append(t(xo + w, y0 + h + 14, "3' end", 11.5, MUTE, anchor="middle"))
        out.append(t(xo - 8, y0 + 8, "high", 11.5, MUTE, anchor="end"))
        pts = [(xo + i / 50 * w, y0 + h - (h * 0.8) * math.exp(-i / 6.0) - 2) for i in range(51)]
        out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), BAD, 2.4))
        if both:
            pts = [(xo + w - i / 50 * w, y0 + h - (h * 0.8) * math.exp(-i / 6.0) - 2) for i in range(51)]
            out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), BAD, 2.4))
            out.append(t(xo + w / 2, y0 + 40, "C to T at both ends", 12.5, BAD, anchor="middle"))
        else:
            pts = [(xo + w - i / 50 * w, y0 + h - (h * 0.8) * math.exp(-i / 6.0) - 2) for i in range(51)]
            out.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), HOT, 2.4, dash="5 4"))
            out.append(t(xo + w / 2, y0 + 40, "C to T at 5', G to A at 3'", 12.5, BAD, anchor="middle"))
    return svg(780, 250, "".join(out))


def fig_udg():
    out = [t(20, 24, "Uracil from deamination, and what UDG treatment leaves (schematic, one read).", 14)]
    rows = [("untreated", "all damage kept", [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
            ("full UDG", "damage removed everywhere", [0] * 16),
            ("partial UDG", "damage kept at the ends only", [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])]
    for i, (nm, note, marks) in enumerate(rows):
        y = 62 + i * 46
        out.append(t(130, y + 5, nm, 13.5, INK, anchor="end", weight="bold"))
        out.append(line(146, y, 146 + 16 * 20, y, TOP, 3))
        for j, m in enumerate(marks):
            if m:
                out.append(dot(156 + j * 20, y, 5.5, BAD))
        out.append(t(146 + 16 * 20 + 14, y + 5, note, 12.5, MUTE))
    out.append(t(20, 214, "Full UDG gives clean variant calls but removes the signal that proves the DNA is ancient. "
                          "Partial UDG keeps it at the ends.", 13.5, INK))
    out.append(t(20, 234, "Methylated CpG deaminates to T, not U, so UDG cannot remove those changes.", 13.5, INK))
    return svg(780, 250, "".join(out))


def fig_ss_library():
    out = [t(20, 24, "Single-stranded library: every strand is a template, nicked or not.", 14)]
    steps = [("1 Denature", "duplex becomes two\nsingle strands"),
             ("2 Ligate adapter 1", "to each 3' end\n(on streptavidin beads)"),
             ("3 Copy strand", "primer extension\nmakes a duplex"),
             ("4 Ligate adapter 2", "blunt, to the copy;\nrelease, then PCR")]
    for i, (h, body) in enumerate(steps):
        x = 30 + i * 190
        out.append(t(x, 52, h, 13.5, INK, weight="bold"))
        y = 90
        if i == 0:
            out.append(line(x, y, x + 120, y, TOP, 3))
            out.append(line(x, y + 22, x + 120, y + 22, BOT, 3))
            out.append(path(f"M {x+20} {y+52} L {x+80} {y+52}", TOP, 3))
            out.append(path(f"M {x+40} {y+74} L {x+100} {y+74}", BOT, 3))
        elif i == 1:
            out.append(line(x, y, x + 90, y, TOP, 3))
            out.append(rect(x + 90, y - 4, 24, 8, ADA))
            out.append(dot(x + 126, y, 6, HOT))
            out.append(line(x, y + 40, x + 70, y + 40, BOT, 3))
            out.append(rect(x + 70, y + 36, 24, 8, ADA))
            out.append(dot(x + 106, y + 40, 6, HOT))
        elif i == 2:
            out.append(line(x, y, x + 90, y, TOP, 3))
            out.append(rect(x + 90, y - 4, 24, 8, ADA))
            out.append(dot(x + 126, y, 6, HOT))
            out.append(line(x + 6, y + 14, x + 114, y + 14, BOT, 3))
            out.append(line(x, y + 54, x + 70, y + 54, TOP, 3))
            out.append(rect(x + 70, y + 50, 24, 8, ADA))
            out.append(dot(x + 106, y + 54, 6, HOT))
            out.append(line(x + 6, y + 68, x + 94, y + 68, BOT, 3))
        else:
            out.append(rect(x - 10, y - 4, 20, 8, ADA))
            out.append(line(x + 10, y, x + 100, y, TOP, 3))
            out.append(rect(x + 100, y - 4, 24, 8, ADA))
            out.append(line(x + 10, y + 14, x + 100, y + 14, BOT, 3))
            out.append(rect(x + 100, y + 10, 24, 8, "none", ADA))
        for k, ln in enumerate(body.split("\n")):
            out.append(t(x, 196 + k * 15, ln, 12, MUTE))
        if i < 3:
            out.append(arrow(x + 150, 120, x + 182, MUTE))
    out.append(t(20, 244, "Ancient DNA is short, nicked and often lacks usable duplex ends: ligating to single strands "
                          "recovers more of it.", 13.5, INK))
    return svg(800, 260, "".join(out))


def fig_single_cell():
    out = [t(20, 24, "One cell, two copies of every locus: three ways amplification misleads.", 14)]
    cols = [("Both alleles copied", "heterozygous call", OK, (1, 1), False),
            ("One allele not copied", "allelic dropout: false homozygote", BAD, (1, 0), False),
            ("Early copying error", "error in 1 of 2 copies: false variant", HOT, (1, 1), True)]
    for i, (h, body, col, (a, b), err) in enumerate(cols):
        x = 30 + i * 250
        out.append(t(x, 52, h, 13.5, col, weight="bold"))
        out.append(t(x, 70, "cell", 11.5, MUTE))
        out.append(line(x + 34, 66, x + 94, 66, TOP, 4))
        out.append(line(x + 34, 82, x + 94, 82, BOT, 4))
        out.append(arrow(x + 100, 74, x + 126, MUTE))
        out.append(t(x, 112, "reads", 11.5, MUTE))
        for k in range(6):
            va = a if k < 3 else 0
            for n in range(3):
                pass
        # read pile: allele A (top) and allele B
        na = 6 if a else 0
        nb = 6 if b else 0
        for k in range(na):
            out.append(rect(x + 34 + k * 9, 100, 6, 6, TOP))
        for k in range(nb):
            out.append(rect(x + 34 + k * 9, 112, 6, 6, BOT))
        if err:
            for k in range(3):
                out.append(rect(x + 34 + (k + 3) * 9, 112, 6, 6, BAD))
        out.append(t(x, 150, body, 12.5, col))
    out.append(t(20, 190, "A tube of 6.5 pg cannot be sequenced; it must be amplified roughly a million-fold, "
                          "and the errors scale with it.", 13.5, INK))
    return svg(790, 208, "".join(out))


def fig_mda():
    out = [t(20, 24, "MDA: phi29 displaces the strand ahead of it, and the displaced copy is primed again.", 14)]
    y = 130
    out.append(line(40, y, 380, y, TOP, 3))
    for x in (90, 180, 270):
        out.append(line(x, y - 6, x + 36, y - 6, HOT, 2.5))
        out.append(dot(x, y - 6, 3.5, HOT))
    # displaced branch
    out.append(path("M 126 124 C 150 100 170 88 200 82", HOT, 2.5))
    out.append(path("M 216 124 C 240 100 260 88 290 82", HOT, 2.5))
    out.append(path("M 200 82 C 215 70 230 64 255 60", BOT, 2))
    out.append(path("M 200 82 C 215 92 228 96 252 98", BOT, 2))
    out.append(t(396, 112, "random primers anneal everywhere", 12.5, MUTE))
    out.append(t(396, 130, "isothermal, about 30 °C", 12.5, MUTE))
    out.append(t(396, 148, "products up to tens of kb, hyperbranched", 12.5, MUTE))
    out.append(t(40, 190, "Long, high-fidelity copies; but coverage is uneven and chimeras form where branches "
                          "re-prime on each other.", 13.5, INK))
    return svg(780, 208, "".join(out))


def fig_malbac():
    out = [t(20, 24, "MALBAC: copies close into loops and stop being templates.", 14)]
    out.append(t(30, 56, "random primer", 12.5, MUTE))
    out.append(rect(30, 64, 92, 12, ADA))
    out.append(rect(122, 64, 56, 12, HOT))
    out.append(t(76, 94, "27 nt common tag", 11.5, ADA, anchor="middle"))
    out.append(t(150, 110, "8 random nt", 11.5, HOT, anchor="middle"))
    out.append(line(210, 70, 270, 70, TOP, 3))
    out.append(t(240, 56, "genomic template", 12, MUTE, anchor="middle"))
    out.append(arrow(290, 70, 320, MUTE))
    out.append(t(330, 56, "full amplicon: tag at both ends", 12.5, MUTE))
    out.append(rect(330, 64, 40, 12, ADA))
    out.append(line(370, 70, 520, 70, TOP, 3))
    out.append(rect(520, 64, 40, 12, "none", ADA))
    out.append(arrow(580, 70, 610, MUTE))
    out.append(path("M 630 70 L 650 70 C 680 70 690 30 720 30 C 750 30 760 70 790 70 L 810 70", TOP, 3))
    out.append(rect(630, 64, 20, 12, ADA))
    out.append(rect(790, 64, 20, 12, "none", ADA))
    out.append(t(720, 20, "loop: the two ends anneal", 12.5, HOT, anchor="middle"))
    out.append(t(30, 150, "Only five cycles, so yield grows roughly linearly with cycle number, not "
                          "doubling each time.", 13.5, INK))
    out.append(t(30, 170, "Looped products cannot be copied again, which limits the bias that exponential "
                          "amplification builds up.", 13.5, INK))
    out.append(t(30, 190, "Then ordinary PCR on the common tag makes the library.", 13.5, INK))
    return svg(830, 208, "".join(out))


def fig_pta():
    out = [t(20, 24, "PTA: terminating nucleotides keep every copy a copy of the original.", 14)]
    out.append(t(30, 52, "MDA", 13.5, BAD, weight="bold"))
    out.append(line(30, 70, 330, 70, TOP, 3))
    for k, (x, ln) in enumerate([(50, 180), (110, 200), (170, 120)]):
        out.append(line(x, 82 + k * 10, x + ln, 82 + k * 10, HOT, 2.5))
    out.append(path("M 240 100 C 260 108 270 120 300 124", BAD, 2, dash="4 3"))
    out.append(t(350, 90, "copies of copies: errors spread", 12.5, BAD))
    out.append(t(30, 160, "PTA", 13.5, OK, weight="bold"))
    out.append(line(30, 178, 330, 178, TOP, 3))
    for k, (x, ln) in enumerate([(50, 70), (130, 90), (200, 60), (250, 70)]):
        yy = 190 + (k % 2) * 10
        out.append(line(x, yy, x + ln, yy, HOT, 2.5))
        out.append(rect(x + ln, yy - 5, 5, 10, BAD))
    out.append(t(350, 194, "short products end in a blocked 3' end:", 12.5, OK))
    out.append(t(350, 210, "they cannot be extended or used as templates", 12.5, OK))
    out.append(t(30, 252, "Alpha-thio-ddNTPs are mixed with dNTPs; each terminated copy is exonuclease-resistant, so "
                          "phi29 cannot repair it.", 13.5, INK))
    return svg(800, 270, "".join(out))


def fig_wga_compare():
    out = [t(20, 24, "Single-cell whole-genome amplification: what each method trades.", 14)]
    cols = ["", "MDA (phi29)", "MALBAC", "PTA"]
    rows = [("mode", "isothermal, exponential", "5 quasi-linear cycles, then PCR", "limited, terminated copies"),
            ("strength", "long, accurate copies", "more even depth: copy number", "even depth: SNV calls"),
            ("weakness", "uneven, chimeras", "polymerase errors", "newer, fewer benchmarks")]
    cw = [90, 210, 250, 220]
    xs = [20]
    for w in cw[:-1]:
        xs.append(xs[-1] + w)
    for j, c in enumerate(cols):
        out.append(t(xs[j] + 6, 52, c, 13.5, INK, weight="bold"))
    out.append(line(20, 60, 790, 60, MUTE, 1))
    for i, r in enumerate(rows):
        y = 86 + i * 34
        for j, c in enumerate(r):
            out.append(t(xs[j] + 6, y, c, 12.5, MUTE if j == 0 else INK))
    out.append(t(20, 202, "Claims about error rates are from the papers' own benchmarks: compare "
                          "like with like before choosing.", 13, INK))
    return svg(800, 220, "".join(out))


def fig_qc():
    out = [t(20, 24, "Fragment-size traces: what to read before sequencing.", 14)]
    def trace(x, title, peaks, col):
        o = [line(x, 160, x + 220, 160, MUTE, 1.2)]
        o.append(t(x + 110, 52, title, 13, col, anchor="middle", weight="bold"))
        pts = []
        for i in range(221):
            v = 0
            for c, hgt, sd in peaks:
                v += hgt * math.exp(-((i - c) / sd) ** 2)
            pts.append((x + i, 160 - v))
        o.append(path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), col, 2))
        o.append(t(x, 178, "100 bp", 11, MUTE))
        o.append(t(x + 220, 178, "1000 bp", 11, MUTE, anchor="end"))
        return "".join(o)
    out.append(trace(30, "good", [(100, 85, 28)], OK))
    out.append(trace(290, "adapter dimers", [(100, 55, 28), (14, 85, 6)], BAD))
    out.append(trace(550, "over-amplified", [(95, 70, 25), (165, 40, 12)], HOT))
    out.append(t(30, 200, "sharp small peak", 12, BAD))
    out.append(t(290, 200, "dimer peak near 130 bp: more bead cleanup", 12, BAD))
    out.append(t(550, 200, "second, larger peak: strands annealed through", 12, HOT))
    out.append(t(550, 216, "their ends. Re-do with fewer cycles", 12, HOT))
    return svg(800, 232, "".join(out))


def fig_field_table():
    out = [t(20, 24, "Four real protocols, same blocks (details from the vendor guides in the collection).", 14)]
    cols = ["", "TruSeq PCR-free", "NEBNext Ultra II FS PCR-free", "Illumina DNA Prep", "Nextera XT"]
    cw = [100, 150, 230, 180, 150]
    xs = [20]
    for w in cw[:-1]:
        xs.append(xs[-1] + w)
    rows = [("fragment", "Covaris", "enzymatic, with end prep", "bead-linked Tn5", "Tn5"),
            ("input", "about 1 to 2 µg", "100 to 500 ng", "1 to 500 ng", "1 ng"),
            ("handle", "ligate full-length", "ligate full-length", "transposed + PCR", "transposed + PCR"),
            ("PCR", "none", "none", "5 to 12 cycles", "12 cycles"),
            ("sizing", "bead size selection", "bead size selection", "double-sided beads", "bead clean-up"),
            ("quant.", "qPCR required", "see guide", "bead-normalised", "bead-normalised")]
    for j, c in enumerate(cols):
        out.append(t(xs[j] + 4, 50, c, 12.5, INK, weight="bold"))
    out.append(line(20, 58, 810, 58, MUTE, 1))
    for i, r in enumerate(rows):
        y = 80 + i * 26
        for j, c in enumerate(r):
            col = MUTE if j == 0 else (OK if c.startswith("none") else INK)
            out.append(t(xs[j] + 4, y, c, 12.5, col))
    return svg(830, 240, "".join(out))


def fig_decision():
    out = [t(20, 24, "From sample to library: a decision sketch.", 14)]
    rows = [("100 ng or more, intact", "fragment, ligate full-length adapters, no PCR", OK),
            ("1 to 100 ng, intact", "tagmentation or ligation, few PCR cycles", ADA),
            ("short, nicked, damaged", "single-stranded library; consider partial UDG", HOT),
            ("one cell, or picograms", "whole-genome amplification first (MDA, MALBAC, PTA)", BAD)]
    for i, (a, b, col) in enumerate(rows):
        y = 44 + i * 52
        out.append(box(20, y, 210, 36, a, fill=PALE, size=12.5))
        out.append(arrow(236, y + 18, 276, col))
        out.append(box(282, y, 430, 36, b, fill=PALE, stroke=col, size=12.5))
    return svg(730, 256, "".join(out))


build(__file__, [
    ("recipe", fig_recipe),
    ("input-scale", fig_input_scale),
    ("fragmentation", fig_fragmentation),
    ("ligation-library", fig_ligation_library),
    ("tagmentation", fig_tagmentation),
    ("adapter-types", fig_adapter_types),
    ("compounding", fig_compounding),
    ("gc-curve", fig_gc_curve),
    ("duplicates", fig_duplicates),
    ("complexity", fig_complexity),
    ("damage", fig_damage),
    ("udg", fig_udg),
    ("ss-library", fig_ss_library),
    ("single-cell", fig_single_cell),
    ("mda", fig_mda),
    ("malbac", fig_malbac),
    ("pta", fig_pta),
    ("wga-compare", fig_wga_compare),
    ("field-table", fig_field_table),
    ("qc", fig_qc),
    ("decision", fig_decision),
])
