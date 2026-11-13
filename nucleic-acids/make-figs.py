#!/usr/bin/env python3
"""Figures for the nucleic-acids unit.  Run: python3 nucleic-acids/make-figs.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

# ---------------------------------------------------------------- figures

def fig_polarity():
    top = "ATGCTTAGCCA"
    bot = "TACGAATCGGT"
    b, w = duplex(90, 70, top, bot, ltop="5'-P", rtop="OH-3'",
                  lbot="HO-3'", rbot="P-5'")
    out = [b]
    # direction arrows
    out.append(arrow(90, 40, 90 + w, TOP))
    out.append(t(90 + w / 2, 32, "a polymerase can only add here", 13, TOP, anchor="middle"))
    out.append(arrow(90 + w, 142, 90, BOT))
    out.append(t(90 + w / 2, 160, "and here on the other strand", 13, BOT, anchor="middle"))
    out.append(t(50, 196, "Phosphate at 5', hydroxyl at 3', and the two strands antiparallel.",
                 14, INK))
    return svg(600, 214, "".join(out))


def fig_end_types():
    panels = [
        ("blunt", "ATGCTTAG", "TACGAATC", 0, 0),
        ("5' overhang", "ATGCTTAG", "  CGAATC", 0, 0),
        ("3' overhang", "  GCTTAG", "TACGAATC", 0, 0),
    ]
    out = []
    y = 55
    for i, (name, top, bot, _, _) in enumerate(panels):
        x = 50 + i * 165
        b, w = duplex(x, y, top, bot, labels=False)
        out.append(b)
        out.append(t(x + w / 2, y - 24, name, 14, INK, anchor="middle"))
        out.append(t(x - 8, y, "5'", 11.5, MUTE, anchor="end"))
        out.append(t(x - 8, y + 30, "3'", 11.5, MUTE, anchor="end"))
    out.append(t(50, 150, "The shape of the end decides which ligation is possible, and how "
                          "specific it is.", 14, INK))
    return svg(620, 170, "".join(out))


def fig_end_chemistry():
    out = []
    items = [
        ("5'-P", "ligatable donor", OK),
        ("5'-OH", "ligase cannot use it", BAD),
        ("3'-OH", "extendable, ligatable", OK),
        ("3'-P / 3'-C3", "blocked: nothing happens", BAD),
    ]
    for i, (lab, note, col) in enumerate(items):
        x, y = 60, 48 + i * 40
        five = lab.startswith("5")
        out.append(line(x, y, x + 60, y, TOP, 2.4))
        out.append(f'<circle cx="{x if five else x+60}" cy="{y}" r="5.5" fill="{col}"/>')
        out.append(t(x - 10, y + 4, "5'" if five else "3'", 11.5, MUTE, anchor="end"))
        out.append(t(x + 76, y + 5, lab, 14.5, col, weight="bold", family=MONO))
        out.append(t(x + 230, y + 5, note, 13.5, MUTE))
    out.append(t(50, 48 + len(items) * 40 + 20,
                 "Two atoms decide almost everything: is there a phosphate at 5', "
                 "and is the 3' free?", 14, INK))
    return svg(620, 48 + len(items) * 40 + 40, "".join(out))


def fig_nick_gap():
    out = []
    rows = [
        ("intact duplex", "ATGCTTAGCCA", "TACGAATCGGT", None),
        ("nick: backbone cut, no base missing", "ATGCTTAGCCA", "TACGAATCGGT", 5),
        ("gap: a base is actually missing", "ATGCT AGCCA", "TACGAATCGGT", None),
    ]
    y = 46
    for name, top, bot, nick in rows:
        b, w = duplex(60, y, top, bot, labels=False)
        out.append(b)
        if nick is not None:
            nx = 60 + nick * DX - 3
            out.append(line(nx, y - 12, nx, y + 4, HOT, 2))
        out.append(t(60 + w + 24, y + 16, name, 13, MUTE))
        y += 72
    out.append(t(50, y + 4, "A nick can be sealed by a ligase. A gap must be filled in by a "
                            "polymerase first.", 14, INK))
    return svg(620, y + 24, "".join(out))


def fig_ligation():
    out = []
    # works
    b, w = duplex(60, 56, "ATGCTTAGCCA", "TACGAATCGGT", labels=False)
    out.append(b)
    out.append(line(60 + 5 * DX - 3, 44, 60 + 5 * DX - 3, 60, OK, 2))
    nick = 60 + 5 * DX
    out.append(t(nick - 66, 34, "3'-OH", 12.5, OK, anchor="end", family=MONO))
    out.append(line(nick - 62, 30, nick - 4, 48, OK, 1, dash="3 3"))
    out.append(t(nick + 66, 34, "5'-P", 12.5, OK, family=MONO))
    out.append(line(nick + 62, 30, nick + 6, 48, OK, 1, dash="3 3"))
    out.append(t(60 + w + 30, 72, "ligase seals it", 14, OK))
    # fails
    b2, w2 = duplex(60, 150, "ATGCTTAGCCA", "TACGAATCGGT", labels=False)
    out.append(b2)
    out.append(line(60 + 5 * DX - 3, 138, 60 + 5 * DX - 3, 154, BAD, 2))
    out.append(t(nick - 66, 128, "3'-OH", 12.5, MUTE, anchor="end", family=MONO))
    out.append(line(nick - 62, 124, nick - 4, 142, MUTE, 1, dash="3 3"))
    out.append(t(nick + 66, 128, "5'-OH", 12.5, BAD, family=MONO))
    out.append(line(nick + 62, 124, nick + 6, 142, BAD, 1, dash="3 3"))
    out.append(t(60 + w2 + 30, 166, "nothing happens", 14, BAD))
    out.append(t(50, 236, "Same geometry, different chemistry. A missing 5'-phosphate is a "
                          "classic silent failure.", 14, INK))
    return svg(640, 256, "".join(out))


def fig_tm():
    out = []
    x0, y0, w, h = 70, 40, 230, 120
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    pts = []
    import math
    for i in range(61):
        f = i / 60
        x = x0 + f * w
        y = y0 + h / (1 + math.exp(-(f - 0.5) * 12))
        pts.append(f"{x:.1f},{y:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" stroke-width="2.2"/>')
    out.append(line(x0 + w / 2, y0 + h, x0 + w / 2, y0 + h / 2, HOT, 1.4, dash="4 3"))
    out.append(line(x0, y0 + h / 2, x0 + w / 2, y0 + h / 2, HOT, 1.4, dash="4 3"))
    out.append(t(x0 + w / 2, y0 + h + 18, "Tm", 14, HOT, anchor="middle"))
    out.append(t(x0 + w / 2 + 8, y0 + h / 2 - 6, "half open", 12, HOT))
    out.append(t(x0 - 10, y0 + 6, "paired", 12, MUTE, anchor="end"))
    out.append(t(x0 - 10, y0 + h, "melted", 12, MUTE, anchor="end"))
    out.append(t(x0 + w / 2, y0 + h + 40, "temperature", 13, MUTE, anchor="middle"))
    # factors
    fx = x0 + w + 60
    out.append(t(fx, y0 + 14, "raises Tm", 14, OK))
    for i, s in enumerate(["more bases", "more G and C", "more salt"]):
        out.append(t(fx + 10, y0 + 36 + i * 20, "· " + s, 13, INK))
    out.append(t(fx, y0 + 112, "lowers Tm", 14, BAD))
    for i, s in enumerate(["mismatches", "formamide, DMSO"]):
        out.append(t(fx + 10, y0 + 134 + i * 20, "· " + s, 13, INK))
    return svg(560, 210, "".join(out))


def fig_hairpin_dimer():
    out = []
    # hairpin
    out.append(t(90, 34, "hairpin", 14, INK, anchor="middle"))
    out.append(f'<path d="M 40 60 L 110 60 A 18 18 0 0 1 110 96 L 40 96" fill="none" '
               f'stroke="{TOP}" stroke-width="2.4"/>')
    for i in range(5):
        out.append(line(48 + i * 14, 64, 48 + i * 14, 92, MUTE, 1))
    out.append(t(90, 124, "the oligo folds on itself;", 12, MUTE, anchor="middle"))
    out.append(t(90, 140, "the primer site is hidden", 12, MUTE, anchor="middle"))
    # self dimer
    out.append(t(265, 34, "primer dimer", 14, INK, anchor="middle"))
    b, w = duplex(215, 60, "ATGCCGTA", "TACGGCAT", labels=False)
    out.append(b)
    out.append(t(265, 124, "two primers anneal to each other", 12, MUTE, anchor="middle"))
    out.append(t(265, 140, "and get copied all run", 12, MUTE, anchor="middle"))
    # adapter dimer
    out.append(t(450, 34, "adapter dimer", 14, INK, anchor="middle"))
    out.append(line(392, 70, 442, 70, TOP, 3))
    out.append(line(448, 70, 498, 70, BOT, 3))
    out.append(f'<circle cx="445" cy="70" r="4" fill="{BAD}"/>')
    out.append(t(445, 96, "two adapters, no insert", 12, BAD, anchor="middle"))
    out.append(t(445, 124, "short, amplifies beautifully,", 12, MUTE, anchor="middle"))
    out.append(t(445, 140, "wastes the whole run", 12, MUTE, anchor="middle"))
    return svg(560, 160, "".join(out))


def fig_revcomp():
    out = []
    b, w = duplex(80, 60, "ATGGCTTAC", "TACCGAATG")
    out.append(b)
    out.append(t(80, 130, "One molecule, two ways to write it:", 14, INK))
    out.append(t(96, 156, "5'-ATGGCTTAC-3'", 14, TOP, family=MONO))
    out.append(t(96, 178, "5'-GTAAGCCAT-3'", 14, BOT, family=MONO))
    out.append(t(260, 156, "top strand, read left to right", 12, MUTE))
    out.append(t(260, 178, "same molecule, bottom strand", 12, MUTE))
    out.append(t(80, 208, "Half of all protocol confusion is forgetting which strand is "
                          "being written down.", 14, HOT))
    return svg(560, 226, "".join(out))


def fig_iupac():
    codes = [("N", "A C G T", "anything — UMIs, random primers"),
             ("V", "A C G", "'not T' — blocks the poly(A) tail"),
             ("B", "C G T", "'not A'"),
             ("W", "A T", "weak (2 H-bonds)"),
             ("S", "C G", "strong (3 H-bonds)"),
             ("R", "A G", "purines"),
             ("Y", "C T", "pyrimidines")]
    out = [t(50, 34, "code", 13, MUTE), t(110, 34, "means", 13, MUTE),
           t(230, 34, "used for", 13, MUTE)]
    for i, (c, m, u) in enumerate(codes):
        y = 60 + i * 24
        out.append(t(50, y, c, 15, HOT, weight="bold", family=MONO))
        out.append(t(110, y, m, 14, INK, family=MONO))
        out.append(t(230, y, u, 13, MUTE))
    out.append(t(50, 60 + len(codes) * 24 + 16,
                 "Degenerate positions are ordered as a mixture: one tube, many sequences.",
                 14, INK))
    return svg(560, 60 + len(codes) * 24 + 34, "".join(out))


def fig_oligo_mods():
    out = []
    y = 86
    out.append(line(160, y, 530, y, TOP, 3))
    out.append(t(148, y + 5, "5'", 13, MUTE, anchor="end"))
    out.append(t(542, y + 5, "3'", 13, MUTE))
    marks = [(160, "biotin", "grabs streptavidin beads", -1),
             (250, "phosphate", "lets a ligase use this end", 1),
             (350, "dU", "cut out later by USER", -1),
             (440, "phosphorothioate", "survives exonucleases", 1),
             (530, "C3 / ddC / inv-dT", "3' blocked: no extension", -1)]
    for x, lab, note, side in marks:
        yy = y - 34 if side < 0 else y + 34
        out.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{HOT}"/>')
        out.append(line(x, y + (-6 if side < 0 else 6), x, yy + (10 if side < 0 else -10),
                        MUTE, 1, dash="3 3"))
        anc = "middle"
        out.append(t(x, yy + (0 if side < 0 else 12), lab, 13, HOT, anchor=anc, weight="bold"))
        out.append(t(x, yy + (16 if side < 0 else 28), note, 11.5, MUTE, anchor=anc))
    out.append(t(50, 196, "An oligo is not just a sequence: its modifications decide what "
                          "enzymes can do to it.", 14, INK))
    return svg(680, 214, "".join(out))


def fig_rna_ends():
    out = []
    y = 74
    out.append(line(110, y, 420, y, TOP, 3.2))
    out.append(f'<circle cx="104" cy="{y}" r="9" fill="{HOT}"/>')
    out.append(t(104, y + 4, "m7G", 8.5, "#fff", anchor="middle", weight="bold"))
    out.append(t(104, y - 20, "cap", 13, HOT, anchor="middle"))
    out.append(t(265, y - 20, "coding and untranslated sequence", 13, MUTE, anchor="middle"))
    s, w = seq(424, y + 5, "AAAAAAAAAA", BOT)
    out.append(s)
    out.append(t(424 + w / 2, y - 20, "poly(A)", 13, BOT, anchor="middle"))
    out.append(t(50, 136, "Other 5' ends you will meet:", 14, INK))
    for i, (a, b) in enumerate([("5'-PPP", "primary transcript, uncapped"),
                                ("5'-P", "cleaved — a ligase can use it"),
                                ("5'-OH", "cleaved another way — ligase cannot")]):
        out.append(t(70, 160 + i * 22, a, 13, HOT, family=MONO))
        out.append(t(150, 160 + i * 22, b, 13, MUTE))
    out.append(t(360, 136, "And 3' ends:", 14, INK))
    for i, (a, b) in enumerate([("3'-OH", "ready to ligate"),
                                ("2',3'-cyclic P", "must be opened first")]):
        out.append(t(380, 160 + i * 22, a, 13, HOT, family=MONO))
        out.append(t(510, 160 + i * 22, b, 13, MUTE))
    out.append(t(50, 236, "Which end an RNA has decides how you can attach anything to it.",
                 14, INK))
    return svg(700, 254, "".join(out))


def fig_dna_rna():
    out = []
    out.append(t(50, 34, "DNA", 15, TOP, weight="bold"))
    out.append(t(50, 58, "2'-H · thymine · stable", 13, MUTE))
    out.append(t(50, 96, "RNA", 15, HOT, weight="bold"))
    out.append(t(50, 120, "2'-OH · uracil · self-cleaves above pH 8, "
                          "degraded by RNases everywhere", 13, MUTE))
    out.append(t(50, 162, "RNA:DNA hybrid", 15, BOT, weight="bold"))
    b, w = duplex(50, 190, "AUGCUUAGCCA", "TACGAATCGGT", topfill=HOT, botfill=TOP,
                  ltop="5'", rtop="3'", lbot="3'", rbot="5'")
    out.append(b)
    out.append(t(50 + w + 50, 206, "RNase H cuts only the RNA strand here", 13, MUTE))
    out.append(t(50 + w + 50, 226, "— the basis of rRNA depletion and of", 13, MUTE))
    out.append(t(50 + w + 50, 244, "second-strand synthesis", 13, MUTE))
    return svg(560, 272, "".join(out))


def fig_end_to_enzyme():
    out = []
    rows = [("free 3'-OH", "polymerase can extend it", OK),
            ("free 3'-OH + 5'-P across a nick", "ligase can seal it", OK),
            ("5'-OH", "kinase (T4 PNK) must add a phosphate first", HOT),
            ("3'-P or 3'-C3 spacer", "nothing extends: deliberate dead end", BAD),
            ("recessed 3' end", "polymerase fills in, or exonuclease chews back", HOT)]
    out.append(t(50, 32, "what the end is", 13, MUTE))
    out.append(t(376, 32, "what can happen to it", 13, MUTE))
    for i, (a, b, c) in enumerate(rows):
        y = 60 + i * 30
        out.append(t(50, y, a, 13.5, INK, family=MONO))
        out.append(arrow(340, y - 5, 366, c))
        out.append(t(376, y, b, 14, c))
    out.append(t(50, 60 + len(rows) * 30 + 14,
                 "Read any protocol step as: which end state goes in, which comes out.",
                 14, INK))
    return svg(760, 60 + len(rows) * 30 + 32, "".join(out))


build(__file__, [
    ("polarity", fig_polarity),
    ("end-chemistry", fig_end_chemistry),
    ("end-types", fig_end_types),
    ("nick-gap", fig_nick_gap),
    ("ligation-requirements", fig_ligation),
    ("end-to-enzyme", fig_end_to_enzyme),
    ("tm", fig_tm),
    ("hairpin-dimer", fig_hairpin_dimer),
    ("revcomp", fig_revcomp),
    ("iupac", fig_iupac),
    ("oligo-mods", fig_oligo_mods),
    ("dna-vs-rna", fig_dna_rna),
    ("rna-ends", fig_rna_ends),
])
