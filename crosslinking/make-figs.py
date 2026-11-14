#!/usr/bin/env python3
"""Figures for the crosslinking unit.  Run: python3 crosslinking/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

_svg = svg


def svg(w, h, body):
    """Grow the canvas to hold the lowest text line."""
    import re as _re
    ys = [float(m) for m in _re.findall(r'<text x="[-\d.]+" y="([-\d.]+)"', body)]
    return _svg(w, max(h, int(max(ys) + 14)) if ys else h, body)


PALE = "#eef2f6"
PALE_HOT = "#f7e7dd"
PALE_OK = "#e3efe6"
PALE_BAD = "#f4e0dc"
PALE_VIO = "#ece7f3"
VIO = "#6b4e8f"
GRID = "#dfe3e6"


def cap(x, y, s, size=13, fill=None, maxc=96):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(t(x, y + i * (size + 5), ln, size, fill) for i, ln in enumerate(lines))


def circ(x, y, r, fill="none", stroke=MUTE, w=1.4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'


def path(d, stroke=INK, w=1.6, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def table(x, y, colw, rowh, header, rows, size=12, hfill=PALE):
    out, xs = [], [x]
    for w in colw:
        xs.append(xs[-1] + w)
    for j, h in enumerate(header):
        out.append(box(xs[j], y, colw[j], rowh, h, hfill, MUTE, size, INK))
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            out.append(box(xs[j], y + (i + 1) * rowh, colw[j], rowh, c, "none", GRID, size, INK))
    return "".join(out)


KIND = {"cell": (PALE, TOP), "ins": ("none", MUTE), "hot": (PALE_HOT, HOT),
        "ok": (PALE_OK, OK), "bad": (PALE_BAD, BAD), "vio": (PALE_VIO, VIO)}


def chain(x, y, parts, h=22, size=11.5):
    out = []
    for label, w, k in parts:
        fill, col = KIND[k]
        out.append(box(x, y, w, h, label, fill, col, size, col, r=3))
        x += w
    return "".join(out), x


def dna(x, y, w, col=TOP):
    """A short stretch of duplex drawn as two rails with rungs."""
    out = [line(x, y, x + w, y, col, 2.0), line(x, y + 12, x + w, y + 12, col, 2.0)]
    n = int(w // 11)
    for i in range(1, n):
        out.append(line(x + i * 11, y + 1, x + i * 11, y + 11, MUTE, 0.9))
    return "".join(out)


def prot(x, y, r=17, label="TF", fill=PALE_OK, col=OK):
    return circ(x, y, r, fill, col, 1.8) + t(x, y + 4.5, label, 11.5, col, anchor="middle")


# ------------------------------------------------------------------ 01 why

def fig_why():
    out = [t(30, 26, "An association is not a molecule. Every step after lysis is a chance to lose it.",
             14, INK)]
    # left: no crosslink
    out.append(t(30, 56, "No crosslink", 13, MUTE))
    out.append(dna(30, 86, 180))
    out.append(prot(100, 78, 17, "TF"))
    out.append(t(30, 128, "in the cell: bound", 12, MUTE))
    out.append(arrow(225, 92, 268, MUTE))
    out.append(t(246, 76, "lyse", 11.5, MUTE, anchor="middle"))
    out.append(dna(280, 86, 180))
    out.append(prot(430, 50, 17, "TF"))
    out.append(t(280, 128, "in the tube: gone", 12, BAD))
    # right: crosslinked
    out.append(t(30, 176, "Formaldehyde first", 13, MUTE))
    out.append(dna(30, 206, 180))
    out.append(prot(100, 198, 17, "TF"))
    out.append(line(100, 215, 100, 206, HOT, 2.6))
    out.append(dot(100, 206, 3.5, HOT))
    out.append(t(30, 248, "covalent bond, 1 atom wide", 12, HOT))
    out.append(arrow(225, 212, 268, MUTE))
    out.append(t(246, 196, "lyse", 11.5, MUTE, anchor="middle"))
    out.append(dna(280, 206, 180))
    out.append(prot(350, 198, 17, "TF"))
    out.append(line(350, 215, 350, 206, HOT, 2.6))
    out.append(t(280, 248, "still bound: now one molecule", 12, OK))
    out.append(cap(30, 282, "Crosslinking turns a transient contact into a covalent bond, so the "
                            "sample can be taken apart without the answer falling apart.", 14, HOT))
    return svg(620, 310, "".join(out))


# ------------------------------------------------------------------ 02 what it survives

def fig_gauntlet():
    out = [t(30, 26, "The bond is asked to hold through every step that destroys the cell.", 14, INK)]
    steps = [("lyse", "detergent"), ("shear", "sonication"), ("wash", "0.5 M salt"),
             ("elute", "1% SDS, 65 °C"), ("reverse", "on purpose")]
    for i, (a, b) in enumerate(steps):
        x = 36 + i * 118
        fill = PALE_HOT if i == 4 else PALE
        col = HOT if i == 4 else TOP
        out.append(box(x, 56, 100, 46, "", fill, col))
        out.append(t(x + 50, 76, a, 13.5, col, anchor="middle"))
        out.append(t(x + 50, 93, b, 11.5, MUTE, anchor="middle"))
        if i < 4:
            out.append(arrow(x + 103, 79, x + 115, MUTE))
    out.append(t(36, 132, "A non-covalent contact survives none of these.", 13, BAD))
    out.append(t(36, 154, "A covalent bond survives the first four, which is why the fifth has to be "
                 "a step of its own.", 13, OK))
    out.append(cap(36, 186, "This is the whole argument for the block: the bond is not the point, "
                            "surviving the workup is.", 14, HOT))
    return svg(640, 216, "".join(out))


# ------------------------------------------------------------------ 03 formaldehyde chemistry

def fig_formaldehyde():
    out = [t(30, 26, "Formaldehyde joins two amines in two steps, through a one-carbon bridge.",
             14, INK)]
    y = 78
    out.append(box(26, y - 22, 150, 44, "", PALE, MUTE))
    out.append(t(101, y - 6, "lysine side chain", 11.5, MUTE, anchor="middle"))
    out.append(t(101, y + 12, "Pro–NH2", 13.5, OK, anchor="middle"))
    out.append(t(196, y + 4, "+", 14, MUTE))
    out.append(box(216, y - 22, 96, 44, "", PALE_HOT, HOT))
    out.append(t(264, y - 6, "formaldehyde", 11.5, MUTE, anchor="middle"))
    out.append(t(264, y + 12, "H2C=O", 13.5, HOT, anchor="middle"))
    out.append(arrow(322, y, 368, MUTE))
    out.append(t(345, y - 10, "fast", 11, MUTE, anchor="middle"))
    out.append(box(376, y - 22, 170, 44, "", PALE_HOT, HOT))
    out.append(t(461, y - 6, "methylol adduct, reversible", 11.5, MUTE, anchor="middle"))
    out.append(t(461, y + 12, "Pro–NH–CH2–OH", 13.5, HOT, anchor="middle"))

    y2 = 162
    out.append(t(26, y2 - 24, "then the adduct finds a second amine that is already touching it:",
                 13, INK))
    out.append(box(26, y2 - 4, 170, 44, "", PALE_HOT, HOT))
    out.append(t(111, y2 + 12, "Pro–NH–CH2–OH", 13.5, HOT, anchor="middle"))
    out.append(t(216, y2 + 22, "+", 14, MUTE))
    out.append(box(236, y2 - 4, 150, 44, "", PALE, MUTE))
    out.append(t(311, y2 + 12, "H2N–cytosine", 13.5, TOP, anchor="middle"))
    out.append(t(311, y2 + 30, "or a second lysine", 11, MUTE, anchor="middle"))
    out.append(arrow(396, y2 + 18, 442, MUTE))
    out.append(t(419, y2 + 8, "slow", 11, MUTE, anchor="middle"))
    out.append(box(450, y2 - 4, 210, 44, "", PALE_OK, OK))
    out.append(t(555, y2 + 12, "Pro–NH–CH2–NH–cytosine", 13, OK, anchor="middle"))
    out.append(t(555, y2 + 30, "methylene bridge, plus water", 11, MUTE, anchor="middle"))
    out.append(cap(26, y2 + 68, "The bridge is one carbon long, so the two amines must already be "
                                "in contact. Heating hydrolyses it again, which is why formaldehyde "
                                "is the reversible case.", 14, HOT))
    return svg(690, 262, "".join(out))


# ------------------------------------------------------------------ 04 reach

def fig_reach():
    out = [t(30, 26, "What a reagent can join is set by how far its arms reach.", 14, INK)]
    arms = [("UV, 254 nm", 0, "no linker at all", VIO),
            ("formaldehyde", 2.3, "one carbon", HOT),
            ("DSG", 7.7, "glutarate", TOP),
            ("DSS", 11.4, "suberate", TOP),
            ("EGS", 16.1, "ethylene glycol bis", TOP)]
    for i, (nm, a, note, col) in enumerate(arms):
        y = 62 + i * 34
        out.append(t(36, y + 5, nm, 13, INK))
        out.append(line(176, y, 176, y + 1, MUTE, 1))
        w = a * 13
        if w > 0:
            out.append(line(176, y, 176 + w, y, col, 5))
        out.append(dot(176, y, 4, col))
        out.append(dot(176 + w, y, 4, col))
        out.append(t(400, y + 5, ("%.1f Å" % a) if a else "0 Å", 12.5, col))
        out.append(t(452, y + 5, note, 11.5, MUTE))
    out.append(t(36, 242, "Spacer-arm figures are the lengths quoted on crosslinker datasheets; "
                 "the formaldehyde value is the bridge itself.", 12, MUTE))
    out.append(cap(36, 268, "A short arm reports contact. A long arm reports a neighbourhood, and "
                            "cannot tell you which protein was touching which.", 14, HOT))
    return svg(660, 296, "".join(out))


# ------------------------------------------------------------------ 05 dose

def fig_dose():
    out = [t(30, 26, "Dose and time: more crosslinking is more signal until it is less of everything else.",
             14, INK)]
    x0, y0, w, h = 60, 56, 320, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    # signal rises and saturates
    pts = []
    for i in range(41):
        f = i / 40.0
        pts.append((x0 + f * w, y0 + h - h * (1 - math.exp(-3.2 * f))))
    out.append(path("M " + " L ".join("%.1f %.1f" % p for p in pts), OK, 2.2))
    # shearing and epitope access fall
    pts2 = []
    for i in range(41):
        f = i / 40.0
        pts2.append((x0 + f * w, y0 + h - h * math.exp(-2.4 * f)))
    out.append(path("M " + " L ".join("%.1f %.1f" % p for p in pts2), BAD, 2.2, dash="5 4"))
    out.append(t(x0 + w / 2, y0 + h + 22, "formaldehyde dose × time", 12.5, MUTE, anchor="middle"))
    out.append(line(x0 + 92, y0, x0 + 92, y0 + h, HOT, 1.4, dash="3 3"))
    out.append(t(x0 + 96, y0 + h - 8, "the window", 12, HOT))
    out.append(line(x0, y0 + h + 44, x0 + 24, y0 + h + 44, OK, 2.2))
    out.append(t(x0 + 32, y0 + h + 48, "specific signal recovered", 12, OK))
    out.append(line(x0 + 180, y0 + h + 44, x0 + 204, y0 + h + 44, BAD, 2.2, dash="5 4"))
    out.append(t(x0 + 212, y0 + h + 48, "shearing and epitope access", 12, BAD))
    bx = 420
    out.append(t(bx, 62, "A common chromatin starting point", 13, INK))
    for i, s in enumerate(["1% formaldehyde, 10 min, room temperature",
                           "quench with 125 mM glycine, which stops it",
                           "sonicate to a few hundred base pairs",
                           "reverse at 65 °C, then proteinase K"]):
        out.append(t(bx, 86 + i * 22, "– " + s, 12.5, MUTE))
    out.append(t(bx, 190, "Crosslinking does not stop when the clock does.", 12.5, BAD))
    out.append(t(bx, 210, "It stops when the quench goes in.", 12.5, BAD))
    out.append(cap(36, 292, "Fixation is not an on/off step but a titration, and the right point "
                            "depends on the target, the cell type and the shearing that follows.",
                   14, HOT, maxc=86))
    return svg(720, 320, "".join(out))


# ------------------------------------------------------------------ 06 DSG

def fig_dsg():
    out = [t(30, 26, "Why a second reagent: the factor you want may never touch the DNA.", 14, INK)]
    # panel 1: formaldehyde alone
    out.append(t(30, 56, "Formaldehyde alone", 13, MUTE))
    out.append(dna(30, 150, 230))
    out.append(prot(80, 142, 17, "A"))
    out.append(line(80, 159, 80, 150, HOT, 2.6))
    out.append(prot(150, 104, 19, "B"))
    out.append(t(30, 188, "A is held to the DNA", 12, OK))
    out.append(t(30, 206, "B touches A, not the DNA, and is", 12, BAD))
    out.append(t(30, 224, "lost in the first wash", 12, BAD))
    # panel 2: DSG then formaldehyde
    out.append(t(330, 56, "DSG first, then formaldehyde", 13, MUTE))
    out.append(dna(330, 150, 230))
    out.append(prot(380, 142, 17, "A"))
    out.append(line(380, 159, 380, 150, HOT, 2.6))
    out.append(prot(450, 104, 19, "B"))
    out.append(line(395, 131, 434, 114, TOP, 3.2))
    out.append(dot(395, 131, 3.5, TOP))
    out.append(dot(434, 114, 3.5, TOP))
    out.append(t(330, 188, "DSG bridges amine to amine over", 12, OK))
    out.append(t(330, 206, "7.7 Å, so B is tethered to A", 12, OK))
    out.append(t(330, 224, "An antibody against B now pulls A's DNA", 12, OK))
    out.append(cap(30, 258, "Two reagents, two jobs: the long arm holds the protein assembly "
                            "together, the short arm pins it to the nucleic acid. Heat does not "
                            "break the DSG bond, but proteinase K digests the proteins it joined.",
                   14, HOT))
    return svg(640, 310, "".join(out))


# ------------------------------------------------------------------ 07 datasheet

def fig_family():
    out = [t(30, 26, "A crosslinker datasheet answers four questions, and they decide the protocol.", 14, INK)]
    header = ["reagent", "joins", "arm", "cell permeable", "reversed by"]
    rows = [["formaldehyde", "amine to amine", "2.3 Å", "yes", "heat, 65 °C"],
            ["DSG", "amine to amine", "7.7 Å", "yes", "nothing (protease)"],
            ["DSS", "amine to amine", "11.4 Å", "yes", "nothing (protease)"],
            ["DSP", "amine to amine", "12.0 Å", "yes", "a reducing agent"],
            ["UV 254 nm", "base to side chain", "0 Å", "no reagent", "nothing"]]
    out.append(table(30, 50, [116, 136, 58, 104, 136], 27, header, rows))
    out.append(t(30, 232, "Charged NHS esters such as BS3 do not cross a membrane, so they label "
                 "surfaces rather than nuclei.", 12, MUTE))
    out.append(cap(30, 258, "Four questions answer themselves from the table: can it reach, can it "
                            "get in, what will it hit, and can you get rid of it afterwards.",
                   14, HOT))
    return svg(620, 290, "".join(out))


# ------------------------------------------------------------------ 08 UV

def fig_uv():
    out = [t(30, 26, "UV makes the bond the molecules were already close enough to make.", 14, INK)]
    out.append(t(30, 50, "254 nm, absorbed by the base itself", 13, MUTE))
    out.append(path("M 36 136 C 70 116, 110 156, 150 136 C 190 116, 230 156, 266 136", TOP, 2.6))
    out.append(t(36, 166, "single-stranded RNA", 12, TOP))
    out.append(prot(150, 100, 20, "RBP", PALE_VIO, VIO))
    for i in range(4):
        out.append(line(214 + i * 14, 74, 206 + i * 14, 88, HOT, 1.6))
    out.append(t(276, 78, "UV photons", 11.5, HOT))
    out.append(arrow(286, 124, 326, MUTE))
    out.append(path("M 340 136 C 374 116, 414 156, 454 136 C 494 116, 534 156, 570 136", TOP, 2.6))
    out.append(prot(454, 100, 20, "RBP", PALE_VIO, VIO))
    out.append(line(454, 120, 454, 128, HOT, 3.4))
    out.append(dot(454, 124, 3.5, HOT))
    out.append(t(340, 166, "one direct bond, no linker between them", 12, HOT))
    out.append(t(340, 186, "nothing one atom away is joined", 12, MUTE))
    out.append(t(30, 220, "Proteinase K then cuts the protein away, but not the bond:", 13, INK))
    out.append(path("M 36 260 C 70 240, 110 280, 150 260", TOP, 2.6))
    out.append(dot(94, 250, 4, HOT))
    out.append(box(104, 230, 86, 20, "peptide stub", PALE_HOT, HOT, 11, HOT))
    out.append(t(206, 256, "the stub stays on the crosslinked nucleotide, and the reverse "
                 "transcriptase meets it", 12.5, HOT))
    out.append(t(206, 276, "as a stop or a mis-insertion: the crosslink has become the readout",
                 12.5, HOT))
    return svg(720, 300, "".join(out))


# ------------------------------------------------------------------ 09 4sU

def fig_4su():
    out = [t(30, 26, "4-thiouridine moves the crosslink to a wavelength the cell tolerates.",
             14, INK)]
    rows = [("UV-C, 254 nm", "every pyrimidine absorbs", "also damages DNA and protein; "
             "irradiate on ice, briefly", HOT),
            ("UV-A, 365 nm", "only the thiol of 4sU absorbs", "cells feed on 4sU first, so the "
             "label marks new RNA as well", VIO)]
    for i, (a, b, c, col) in enumerate(rows):
        y = 60 + i * 76
        out.append(box(30, y, 148, 54, "", PALE_HOT if i == 0 else PALE_VIO, col))
        out.append(t(104, y + 22, a, 13, col, anchor="middle"))
        out.append(t(104, y + 40, "zero length either way", 11, MUTE, anchor="middle"))
        out.append(arrow(182, y + 27, 214, MUTE))
        out.append(t(222, y + 20, b, 13, INK))
        out.append(t(222, y + 40, c, 12, MUTE))
    out.append(t(30, 222, "Either way the bond cannot be undone, so the library is built around "
                 "it rather than after it:", 13, INK))
    out.append(t(30, 246, "a truncation at the stub, or a mismatch read through it. The CLIP "
                 "family differs mainly in which of the two it scores.", 13, HOT))
    return svg(720, 266, "".join(out))


# ------------------------------------------------------------------ 10 fixation

def fig_fix():
    out = [t(30, 26, "Fixation makes the cell a container that holds its contents and its state.",
             14, INK)]
    for i, (cx, lab, col, fill) in enumerate([(120, "live", TOP, PALE),
                                              (380, "fixed", HOT, PALE_HOT)]):
        out.append(circ(cx, 118, 58, fill, col, 1.8))
        out.append(circ(cx, 118, 26, "none", col, 1.4))
        out.append(t(cx, 122, "nucleus", 10.5, MUTE, anchor="middle"))
        out.append(t(cx, 196, lab, 13.5, col, anchor="middle"))
    for a in (20, 80, 150, 220, 300):
        ax, ay = 120 + 46 * math.cos(math.radians(a)), 118 + 46 * math.sin(math.radians(a))
        out.append(dot(round(ax, 1), round(ay, 1), 4, MUTE))
    out.append(arrow(140, 60, 196, MUTE))
    out.append(t(168, 50, "RNA leaks, profile drifts", 11.5, BAD, anchor="middle"))
    for a in (20, 80, 150, 220, 300):
        ax, ay = 380 + 46 * math.cos(math.radians(a)), 118 + 46 * math.sin(math.radians(a))
        out.append(dot(round(ax, 1), round(ay, 1), 4, HOT))
        out.append(line(round(ax, 1), round(ay, 1), round(380 + 58 * math.cos(math.radians(a)), 1),
                        round(118 + 58 * math.sin(math.radians(a)), 1), HOT, 1.6))
    out.append(t(470, 70, "What fixation buys", 13, OK))
    for i, s in enumerate(["the transcript profile stops changing at that moment",
                           "the cell survives handling, freezing and batching",
                           "the cell itself can be the compartment"]):
        out.append(t(470, 92 + i * 20, "– " + s, 12.5, MUTE))
    out.append(t(470, 170, "What it costs", 13, BAD))
    for i, s in enumerate(["crosslinked RNA is a poorer template for reverse transcription",
                           "sensitivity per cell falls, and the loss is not uniform"]):
        out.append(t(470, 192 + i * 20, "– " + s, 12.5, MUTE))
    out.append(cap(30, 248, "Methanol is the other common fixative: it precipitates protein "
                            "instead of crosslinking, so nothing has to be reversed, and nothing "
                            "is held in place either.", 14, HOT))
    return svg(760, 292, "".join(out))


# ------------------------------------------------------------------ 11 permeabilisation

def fig_perm():
    out = [t(30, 26, "Permeabilisation pulls against fixation: hold things in, let enzymes in.",
             14, INK)]
    panels = [("under-permeabilised", PALE, TOP, "enzyme stays outside", "few molecules captured"),
              ("the window", PALE_OK, OK, "enzyme in, contents in", "what the step is titrated for"),
              ("over-permeabilised", PALE_BAD, BAD, "contents diffuse out", "signal spreads or is lost")]
    for i, (lab, fill, col, a, b) in enumerate(panels):
        cx = 110 + i * 200
        out.append(circ(cx, 112, 52, fill, col, 1.8 if i != 1 else 2.6))
        if i == 0:
            out.append(box(cx + 62, 100, 26, 24, "E", PALE_HOT, HOT, 12, HOT))
            for a2 in (40, 140, 240, 320):
                out.append(dot(round(cx + 30 * math.cos(math.radians(a2)), 1),
                               round(112 + 30 * math.sin(math.radians(a2)), 1), 4, MUTE))
        elif i == 1:
            out.append(box(cx - 14, 100, 26, 24, "E", PALE_HOT, HOT, 12, HOT))
            for a2 in (40, 140, 240, 320):
                out.append(dot(round(cx + 32 * math.cos(math.radians(a2)), 1),
                               round(112 + 32 * math.sin(math.radians(a2)), 1), 4, MUTE))
        else:
            out.append(box(cx - 14, 100, 26, 24, "E", PALE_HOT, HOT, 12, HOT))
            for a2 in (30, 150, 270):
                out.append(dot(round(cx + 70 * math.cos(math.radians(a2)), 1),
                               round(112 + 70 * math.sin(math.radians(a2)), 1), 4, BAD))
        out.append(t(cx, 182, lab, 13, col, anchor="middle"))
        out.append(t(cx, 200, a, 11.5, MUTE, anchor="middle"))
        out.append(t(cx, 218, b, 11.5, MUTE, anchor="middle"))
    out.append(t(30, 250, "The dial is the detergent and the time: digitonin binds cholesterol and "
                 "largely spares the nuclear membrane,", 12.5, INK))
    out.append(t(30, 270, "NP-40 and IGEPAL are the same stronger non-ionic detergent under two "
                 "names, Tween-20 is milder.", 12.5, INK))
    out.append(cap(30, 298, "Crosslinks make the membrane harder to open and the enzyme's path "
                            "narrower, so the two steps have to be optimised together.", 14, HOT))
    return svg(680, 326, "".join(out))


# ------------------------------------------------------------------ 12 reversal

def fig_reversal():
    out = [t(30, 26, "Two different bonds, two different tools, in this order.", 14, INK)]
    out.append(box(30, 54, 180, 70, "", PALE_HOT, HOT))
    out.append(t(120, 76, "65 °C, overnight", 13, HOT, anchor="middle"))
    out.append(t(120, 96, "hydrolyses the methylene", 11.5, MUTE, anchor="middle"))
    out.append(t(120, 112, "bridge: protein lets go", 11.5, MUTE, anchor="middle"))
    out.append(arrow(216, 89, 252, MUTE))
    out.append(box(258, 54, 180, 70, "", PALE_OK, OK))
    out.append(t(348, 76, "proteinase K, 45–55 °C", 13, OK, anchor="middle"))
    out.append(t(348, 96, "cuts the peptide backbone:", 11.5, MUTE, anchor="middle"))
    out.append(t(348, 112, "removes the protein itself", 11.5, MUTE, anchor="middle"))
    out.append(arrow(444, 89, 480, MUTE))
    out.append(box(486, 54, 170, 70, "", PALE, TOP))
    out.append(t(571, 84, "clean nucleic acid,", 13, TOP, anchor="middle"))
    out.append(t(571, 104, "ready for a library", 13, TOP, anchor="middle"))
    out.append(t(30, 158, "What must survive the reversal", 13, INK))
    rows = [["DNA", "survives 65 °C overnight", "this is why ChIP works"],
            ["RNA", "hydrolyses and fragments", "RNA methods shorten or avoid the heat"],
            ["protein", "not meant to survive", "digested, so DSG needs no reversal"],
            ["UV bond", "survives both", "a peptide stub is left behind"]]
    out.append(table(30, 172, [92, 206, 262], 26, ["", "at 65 °C", "consequence"], rows))
    out.append(cap(30, 324, "Reverse before the protease and the protein comes off the nucleic "
                            "acid first; reverse after it and the stub stays, which is the "
                            "difference between ChIP and CLIP.", 14, HOT, maxc=86))
    return svg(700, 356, "".join(out))


# ------------------------------------------------------------------ 13 the ChIP walk

def fig_walk_chip():
    """Formaldehyde ChIP: the state of the material after every step."""
    out = [t(34, 26, "Formaldehyde ChIP: what is in the tube after each step. HeLa cells, "
             "one antibody.", 14, INK)]
    rows = [("1  fix: 1% formaldehyde, 10 min",
             [("intact cells, chromatin now a covalent network", 300, "hot")],
             "every contact within one carbon is joined"),
            ("2  quench: 125 mM glycine",
             [("the same cells, reaction stopped", 300, "hot")],
             "glycine competes for the aldehyde"),
            ("3  lyse, release nuclei",
             [("nuclei in detergent, crosslinks intact", 300, "cell")],
             "membranes gone, chromatin not"),
            ("4  sonicate",
             [("chr", 44, "ins"), ("chromatin pieces, ~700 bp average", 212, "ins"), ("chr", 44, "ins")],
             "each piece still carries its proteins"),
            ("5  bind antibody, then beads",
             [("beads: pieces whose protein shows the epitope", 300, "ok")],
             "the only selective step in the protocol"),
            ("6  wash in rising salt",
             [("beads: the same pieces, less of everything else", 300, "ok")],
             "non-covalent passengers come off"),
            ("7  elute, reverse at 65 °C overnight",
             [("protein released from DNA, still in the tube", 300, "cell")],
             "methylene bridges hydrolysed"),
            ("8  RNase A, proteinase K, purify",
             [("naked DNA fragments, a few hundred bp", 300, "ins")],
             "now an ordinary input for end repair")]
    for i, (lab, parts, note) in enumerate(rows):
        y = 50 + i * 32
        out.append(t(34, y + 15, lab, 12, INK))
        s, _ = chain(300, y, parts)
        out.append(s)
        out.append(t(620, y + 15, note, 11.5, MUTE))
    y = 50 + 8 * 32
    out.append(cap(34, y + 20, "The crosslink exists only between steps 1 and 7. Everything the "
                   "protocol selects on happens while it is there, and the library is built "
                   "from what is left once it is gone.", 13.5, HOT, maxc=104))
    return svg(1000, y + 58, "".join(out))


# ------------------------------------------------------------------ 14 the CLIP contrast

def fig_walk_clip():
    """UV CLIP: the same shape of walk, with no step 7."""
    out = [t(34, 26, "UV CLIP, the same walk with the reversal removed.", 14, INK)]
    rows = [("1  irradiate: UV-C, on ice",
             [("intact cells, RNA bonded to touching protein", 300, "vio")],
             "zero-length bond, no linker"),
            ("2  (no quench needed)",
             [("the same cells; the lamp is off", 300, "vio")],
             "the dose is the exposure"),
            ("3  lyse, partial RNase digestion",
             [("protein-RNA complexes, RNA trimmed to a footprint", 300, "cell")],
             "only bound RNA is protected"),
            ("4  immunoprecipitate, wash hard",
             [("beads: one protein and its RNA", 300, "ok")],
             "denaturing washes are survivable"),
            ("5  ligate the 3' adapter on the beads",
             [("ad", 40, "hot"), ("footprint RNA, protein still attached", 260, "vio")],
             "the complex is still a complex"),
            ("6  proteinase K",
             [("ad", 40, "hot"), ("footprint RNA with a peptide stub", 260, "bad")],
             "no heat step will undo the bond"),
            ("7  reverse transcribe",
             [("cDNA that stops at, or mis-reads, the stub", 300, "bad")],
             "the crosslink is now the measurement")]
    for i, (lab, parts, note) in enumerate(rows):
        y = 50 + i * 32
        out.append(t(34, y + 15, lab, 12, INK))
        s, _ = chain(300, y, parts)
        out.append(s)
        out.append(t(620, y + 15, note, 11.5, MUTE))
    y = 50 + 7 * 32
    out.append(cap(34, y + 20, "ChIP throws the crosslink away and keeps the DNA. CLIP cannot "
                   "throw it away, so it reads it instead. One bond that will not come off, "
                   "two opposite protocols.", 13.5, HOT, maxc=104))
    return svg(1000, y + 58, "".join(out))


# ------------------------------------------------------------------ 15 costs

def fig_costs():
    out = [t(30, 26, "The five costs, and what each one looks like in the data.", 14, INK)]
    header = ["cost", "what happens", "what you see"]
    rows = [["epitope masking", "the amine the antibody needs is bridged",
             "no enrichment with a validated antibody"],
            ["over-fixation", "chromatin will not shear or solubilise",
             "low yield, fragments far too long"],
            ["lost accessibility", "enzyme or oligo cannot reach the target",
             "weak signal that more cycles do not rescue"],
            ["chimeras", "two separate complexes are joined as one",
             "junctions between unrelated places"],
            ["nucleic-acid damage", "65 °C and UV both attack the backbone",
             "short inserts, low complexity"]]
    out.append(table(30, 50, [150, 300, 282], 28, header, rows))
    out.append(cap(30, 240, "Four of the five are made worse by the same thing, more crosslinking, "
                            "and the fifth by the step that undoes it. There is no setting at "
                            "which none of them applies.", 14, HOT))
    return svg(780, 282, "".join(out))


# ------------------------------------------------------------------ 16 avoiding it

def fig_avoid():
    out = [t(30, 26, "Three methods are shaped by the decision not to crosslink at all.", 14, INK)]
    cards = [("ATAC-seq", "nuclei, no fixation", "Tn5 needs open chromatin, and a crosslink "
              "closes it", PALE, TOP),
             ("CUT&amp;RUN", "permeabilised, not fixed", "the antibody binds a native epitope; "
              "cut fragments diffuse out", PALE_OK, OK),
             ("CUT&amp;Tag", "permeabilised, not fixed", "pA-Tn5 tagments in place, so no chromatin "
              "release is needed", PALE_OK, OK)]
    for i, (nm, sub, why, fill, col) in enumerate(cards):
        x = 30 + i * 240
        out.append(box(x, 56, 220, 118, "", fill, col))
        out.append(t(x + 110, 82, nm, 14, col, anchor="middle"))
        out.append(t(x + 110, 102, sub, 12, MUTE, anchor="middle"))
        out.append(cap(x + 12, 126, why, 11.5, INK, maxc=30))
    out.append(t(30, 200, "What they pay instead", 13, INK))
    for i, s in enumerate(["the target must survive native conditions, so weakly bound factors "
                           "are under-reported",
                           "the epitope must work without fixation, which is a different "
                           "antibody-validation problem",
                           "fixed or archival material cannot be used at all"]):
        out.append(t(30, 222 + i * 20, "– " + s, 12.5, MUTE))
    out.append(cap(30, 296, "Each of these is a protocol built around the costs on the previous "
                            "slide. Some targets and some samples leave no choice in either "
                            "direction.", 14, HOT))
    return svg(760, 332, "".join(out))


build(__file__, [
    ("why", fig_why),
    ("gauntlet", fig_gauntlet),
    ("formaldehyde", fig_formaldehyde),
    ("reach", fig_reach),
    ("dose", fig_dose),
    ("dsg", fig_dsg),
    ("family", fig_family),
    ("uv", fig_uv),
    ("foursu", fig_4su),
    ("fix", fig_fix),
    ("perm", fig_perm),
    ("reversal", fig_reversal),
    ("walk-chip", fig_walk_chip),
    ("walk-clip", fig_walk_clip),
    ("costs", fig_costs),
    ("avoid", fig_avoid),
])
