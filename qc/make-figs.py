#!/usr/bin/env python3
"""Figures for the cleanup, quantification and QC unit.  Run: python3 qc/make-figs.py"""
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


def logx(bp, x0, w, lo=35, hi=10380):
    return x0 + w * (math.log10(bp) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))


def trace(x0, y0, w, h, peaks, title=None, ticks=(100, 300, 1000, 3000)):
    """Electropherogram: peaks = [(bp, height 0-1, width in log10 units)]. Markers at both ends."""
    out = []
    pts = []
    n = 240
    allp = [(35, 0.55, 0.012), (10380, 0.55, 0.012)] + list(peaks)
    for i in range(n + 1):
        lg = math.log10(35) + (math.log10(10380) - math.log10(35)) * i / n
        v = 0.0
        for bp, ht, sd in allp:
            v += ht * math.exp(-((lg - math.log10(bp)) / sd) ** 2 / 2)
        pts.append(f"{x0 + w * i / n:.1f},{y0 + h - v * h:.1f}")
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" stroke-width="1.8"/>')
    for tk in ticks:
        xx = logx(tk, x0, w)
        out.append(line(xx, y0 + h, xx, y0 + h + 4, MUTE, 1.2))
        out.append(t(xx, y0 + h + 17, str(tk), 11, MUTE, anchor="middle"))
    # on the axis-title row, not the tick row: in a narrow panel the 100 tick sits
    # under the left marker
    out.append(t(x0 + 4, y0 + h + 32, "marker", 10.5, MUTE))
    out.append(t(x0 + w, y0 + h + 32, "marker", 10.5, MUTE, anchor="end"))
    out.append(t(x0 + w / 2, y0 + h + 32, "size (bp, log scale)", 11, MUTE, anchor="middle"))
    if title:
        out.append(t(x0, y0 - 6, title, 12.5, INK))
    return "".join(out)


# ---------------------------------------------------------------- cleanup

def fig_cleanup():
    out = [t(40, 26, "Four ways to clean a reaction. They differ in what they remove and what "
                     "they lose.", 14, INK)]
    x0, w = 240, 380
    def lx(bp):
        return x0 + w * (math.log10(bp) - math.log10(20)) / (math.log10(5000) - math.log10(20))
    for tk in (50, 100, 300, 1000, 3000):
        out.append(line(lx(tk), 52, lx(tk), 190, "#e4e6e8", 1))
        out.append(t(lx(tk), 206, str(tk), 11, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, 222, "fragment size (bp), log scale", 11, MUTE, anchor="middle"))
    rows = [("SPRI beads", 100, 5000, "ratio sets the lower limit", OK),
            ("silica column", 60, 5000, "fixed lower limit, about 50-100 bp", TOP),
            ("alcohol precipitation", 150, 5000, "short pieces stay in solution", HOT),
            ("gel extraction", 250, 700, "any window, exact, lossy", VIO)]
    for i, (lab, lo, hi, note, c) in enumerate(rows):
        y = 62 + i * 34
        out.append(t(40, y + 14, lab, 13, INK))
        out.append(f'<rect x="{lx(lo)}" y="{y}" width="{lx(hi) - lx(lo)}" height="20" rx="3" '
                   f'fill="{c}" opacity="0.28"/>')
        out.append(t(lx(hi) + 10 if hi < 3000 else x0 + w + 12, y + 14, note, 11.5, MUTE))
    out.append(t(40, 250, "Bars show what is retained, schematically. Exact limits depend on "
                          "the product and lot.", 13, MUTE))
    return svg(720, 268, "".join(out))


def fig_spri():
    out = [t(40, 26, "SPRI: DNA sticks to carboxyl-coated magnetic beads when PEG and salt "
                     "crowd it out of solution.", 14, INK)]
    out.append(t(40, 58, "high PEG / NaCl", 13, OK))
    out.append(dot(150, 110, 24, "#8a6f4a"))
    for i, a in enumerate(range(0, 360, 45)):
        r = math.radians(a)
        out.append(path(f"M {150+24*math.cos(r):.1f} {110+24*math.sin(r):.1f} "
                        f"q {14*math.cos(r+0.6):.1f} {14*math.sin(r+0.6):.1f} "
                        f"{22*math.cos(r):.1f} {22*math.sin(r):.1f}", TOP, 2))
    out.append(t(150, 172, "DNA collapses onto the bead", 12, MUTE, anchor="middle"))
    out.append(t(330, 58, "wash with 80% ethanol, elute in water or low-salt buffer", 13, OK))
    out.append(dot(380, 110, 24, "#8a6f4a"))
    out.append(arrow(420, 110, 480, MUTE))
    out.append(path("M 495 100 q 20 -20 40 0 t 40 0", TOP, 2.4))
    out.append(t(535, 132, "DNA released", 12, MUTE, anchor="middle"))
    out.append(t(40, 196, "Longer DNA binds at lower PEG, so the ratio of bead mix to sample "
                          "decides the shortest fragment kept.", 14, INK))
    out.append(t(40, 218, "Reference: DeAngelis et al. 1995, Rohland and Reich 2012.", 13, MUTE))
    return svg(700, 238, "".join(out))


def fig_ratio():
    out = [t(40, 26, "The ratio of beads to sample sets where the retention curve sits "
                     "(schematic).", 14, INK)]
    x0, y0, w, h = 80, 50, 520, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    for tk in (50, 100, 200, 400, 800, 1600):
        xx = x0 + w * (math.log10(tk) - math.log10(50)) / (math.log10(2000) - math.log10(50))
        out.append(line(xx, y0 + h, xx, y0 + h + 4, MUTE, 1.2))
        out.append(t(xx, y0 + h + 18, str(tk), 11, MUTE, anchor="middle"))
    out.append(t(x0 + w / 2, y0 + h + 34, "fragment size (bp)", 11, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 8, "bound", 11, MUTE, anchor="end"))
    out.append(t(x0 - 8, y0 + h, "free", 11, MUTE, anchor="end"))
    for ratio, s50, c in ((0.6, 520, HOT), (0.8, 300, TOP), (1.0, 170, OK), (1.8, 70, VIO)):
        pts = []
        for i in range(101):
            lg = math.log10(50) + (math.log10(2000) - math.log10(50)) * i / 100
            f = 1 / (1 + math.exp(-(lg - math.log10(s50)) * 7))
            pts.append(f"{x0 + w * i / 100:.1f},{y0 + h - f * h:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="2.4"/>')
        xl = x0 + w * (math.log10(s50) - math.log10(50)) / (math.log10(2000) - math.log10(50))
        # on the curve's own half-height point: lower down, the next curve to the
        # right has already risen through where the label would sit.
        out.append(t(xl + 14, y0 + h / 2, f"{ratio}x", 12.5, c))
    out.append(t(40, 252, "Higher ratio, more PEG, shorter fragments kept. Calibrate with a "
                          "ladder: the curve moves with bead lot and buffer.", 13.5, INK))
    return svg(720, 272, "".join(out))


def fig_double():
    out = [t(40, 26, "Double-sided selection: two bead additions keep a window.", 14, INK)]
    cols = [("1  add 0.6x beads", "long fragments (above ~500) bind", "keep the supernatant,\nbin the beads"),
            ("2  add beads to 0.8x total", "medium fragments (above ~300)\nbind from the supernatant", "keep the beads,\nbin the supernatant"),
            ("3  wash, elute", "what stuck in step 2:\n~300 to ~520 bp", "")]
    for i, (h, b, c) in enumerate(cols):
        x = 40 + i * 215
        out.append(box(x, 48, 195, 108, "", "#fbfbf9", MUTE))
        out.append(t(x + 98, 70, h, 13, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 98, 94 + j * 15, ln, 12, INK, anchor="middle"))
        for j, ln in enumerate(c.split("\n")):
            if ln:
                out.append(t(x + 98, 128 + j * 15, ln, 12, MUTE, anchor="middle"))
        if i < 2:
            out.append(arrow(x + 199, 102, x + 213, MUTE, head=4))
    out.append(t(40, 188, "Removes both the long fragments and the short ones (adapter dimers) "
                          "in one clean-up.", 14, INK))
    out.append(t(40, 210, "Cost: recovery is lower than for a single clean-up, so keep it for "
                          "samples that have enough DNA.", 13.5, MUTE))
    return svg(700, 230, "".join(out))


# ---------------------------------------------------------------- quantification

def fig_measures():
    out = [t(40, 26, "Three instruments, three different questions about the same tube.", 14, INK)]
    cols = [("Qubit", "how much double-stranded DNA", "a dye lights up in the helix:\nmass of everything,\nof any length", TOP),
            ("qPCR", "how many amplifiable molecules", "primers to P5 and P7:\nonly molecules with\nboth adapters count", OK),
            ("fragment analyser", "what sizes are present", "electrophoresis:\nsize shape, rough mass,\nnot a precise molarity", HOT)]
    for i, (h, q, b, c) in enumerate(cols):
        x = 40 + i * 225
        out.append(box(x, 48, 205, 128, "", "#fbfbf9", c))
        out.append(t(x + 102, 72, h, 15, c, anchor="middle", weight="bold"))
        out.append(t(x + 102, 92, q, 12, INK, anchor="middle"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 102, 118 + j * 15, ln, 12, MUTE, anchor="middle"))
    out.append(t(40, 208, "What the sequencer needs is the number of molecules with both adapters. "
                          "Only qPCR measures that.", 14, INK))
    out.append(t(40, 230, "So use qPCR for the concentration, the analyser for the size, and "
                          "Qubit for mass where size is clean.", 13.5, MUTE))
    return svg(700, 250, "".join(out))


def fig_qpcr():
    out = [t(40, 26, "qPCR quantification: a ten-fold dilution is about 3.3 cycles, if the PCR "
                     "doubles each cycle.", 14, INK)]
    x0, y0, w, h = 70, 48, 260, 130
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    cols = [HOT, TOP, OK, VIO]
    for k in range(4):
        pts = []
        for i in range(0, 41):
            cyc = i
            f = 1 / (1 + math.exp(-(cyc - (12 + 3.32 * k)) * 0.6))
            pts.append(f"{x0 + w * i / 40:.1f},{y0 + h - f * h:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{cols[k]}" stroke-width="2.2"/>')
    out.append(line(x0, y0 + 0.62 * h, x0 + w, y0 + 0.62 * h, MUTE, 1, dash="4 3"))
    out.append(t(x0 + w + 8, y0 + 0.62 * h + 4, "threshold", 11, MUTE))
    out.append(t(x0 + w / 2, y0 + h + 22, "cycle", 11, MUTE, anchor="middle"))
    out.append(t(x0 - 8, y0 + 8, "signal", 11, MUTE, anchor="end"))
    # standard curve
    xs, ys, ws, hs = 440, 48, 200, 130
    out.append(line(xs, ys + hs, xs + ws, ys + hs, MUTE, 1.2))
    out.append(line(xs, ys, xs, ys + hs, MUTE, 1.2))
    x1, y1, x2, y2 = xs + 10, ys + 10, xs + ws - 10, ys + hs - 10
    out.append(line(x1, y1, x2, y2, TOP, 2.2))
    for k in range(4):
        # the standards lie on the fitted line: the most concentrated (k = 0, the
        # earliest Cq on the left panel) sits bottom right, at the lowest Cq.
        xx = xs + 24 + (3 - k) * 50
        out.append(dot(xx, y1 + (xx - x1) / (x2 - x1) * (y2 - y1), 4.5, cols[k]))
    out.append(t(xs + ws / 2, ys + hs + 22, "log10 concentration", 11, MUTE, anchor="middle"))
    out.append(t(xs - 8, ys + 8, "Cq", 11, MUTE, anchor="end"))
    out.append(t(40, 224, "Fit the line through the standards, read the unknown off it, then "
                          "correct for dilution. The slope gives the efficiency.", 13.5, INK))
    out.append(t(40, 246, "A slope of -3.32 cycles per decade is 100% efficiency.", 13.5, MUTE))
    return svg(700, 264, "".join(out))


def fig_qubit_vs_qpcr():
    out = [t(40, 26, "Why the numbers disagree: each measurement counts a different subset of "
                     "what is in the tube.", 14, INK)]
    heads = ["Qubit", "qPCR", "analyser"]
    for j, h in enumerate(heads):
        out.append(t(300 + j * 100, 54, h, 13, MUTE, anchor="middle"))
    rows = [("library, both adapters", (1, 1, 1)),
            ("adapter dimer", (1, 1, 1)),
            ("one adapter only", (1, 0, 1)),
            ("no adapter (leftover fragments)", (1, 0, 1)),
            ("single-stranded DNA", (0, 1, 0)),
            ("RNA, free nucleotides", (0, 0, 0))]
    for i, (lab, v) in enumerate(rows):
        y = 70 + i * 28
        out.append(t(40, y + 4, lab, 13, INK))
        for j, ok in enumerate(v):
            out.append(tick(300 + j * 100, y - 2, OK) if ok else cross(300 + j * 100, y, MUTE, 5))
    out.append(t(40, 252, "Qubit high, qPCR low: much of the DNA lacks adapters, or is one-sided. "
                          "Trace says which.", 14, INK))
    out.append(t(40, 274, "Single-stranded DNA is invisible to dsDNA dyes, but amplifies if "
                          "adapters are there.", 13.5, MUTE))
    return svg(720, 292, "".join(out))


def fig_pool():
    out = [t(40, 26, "Equal mass is not equal molecules. Short fragments carry more molecules "
                     "per nanogram.", 14, INK)]
    libs = [("A  450 bp", 450, TOP), ("B  600 bp", 600, OK), ("C  300 bp", 300, HOT)]
    out.append(t(60, 54, "pooled by mass (20 ng each)", 13, MUTE))
    for i, (lab, bp, c) in enumerate(libs):
        fmol = 20e-9 / (660 * bp) * 1e15
        y = 66 + i * 30
        out.append(t(40, y + 15, lab, 12.5, INK))
        out.append(f'<rect x="130" y="{y}" width="{fmol*2.2:.0f}" height="20" fill="{c}" opacity="0.4"/>')
        out.append(t(130 + fmol * 2.2 + 8, y + 15, f"{fmol:.0f} fmol", 12, MUTE))
    out.append(t(60, 180, "pooled by moles (20 fmol each)", 13, MUTE))
    for i, (lab, bp, c) in enumerate(libs):
        y = 190 + i * 30
        out.append(t(40, y + 15, lab, 12.5, INK))
        out.append(f'<rect x="130" y="{y}" width="{20*2.2:.0f}" height="20" fill="{c}" opacity="0.4"/>')
        out.append(t(130 + 44 + 8, y + 15, "20 fmol", 12, MUTE))
    out.append(t(420, 110, "C would get twice the", 13, BAD))
    out.append(t(420, 128, "reads of B by mass", 13, BAD))
    return svg(700, 292, "".join(out))


def fig_denature():
    out = [t(40, 26, "Denature, neutralise, dilute, load: the library must be single-stranded "
                     "and at the right concentration.", 14, INK)]
    steps = [(["pool", "(nM)"], PB, TOP), (["+ NaOH,", "5 min"], PO, HOT),
             (["+ Tris", "neutralise"], PG, OK), (["dilute in", "chilled buffer"], PB, TOP),
             (["load,", "+ PhiX"], PP, VIO)]
    for i, (lines, f, c) in enumerate(steps):
        x = 40 + i * 132
        out.append(mbox(x, 54, 108, 54, lines, f, c, 12.5, c))
        if i < 4:
            out.append(arrow(x + 111, 81, x + 129, MUTE, head=4))
    out.append(t(40, 146, "NaOH separates the strands, so they can hybridise to the flow cell "
                          "instead of to each other.", 13.5, INK))
    out.append(t(40, 168, "Re-annealing starts as soon as the base is neutralised: load promptly.",
                 13.5, BAD))
    out.append(t(40, 190, "Final loading concentration depends on the instrument and kit: take "
                          "it from the instrument guide.", 13.5, MUTE))
    return svg(720, 210, "".join(out))


# ---------------------------------------------------------------- traces

def fig_trace_ideal():
    out = [trace(60, 50, 560, 130, [(420, 0.75, 0.07)], "a clean library")]
    out.append(t(logx(420, 60, 560) + 22, 74, "main peak: insert plus adapters", 12, OK))
    out.append(t(60, 24, "Ideal trace: one peak at the size you designed, markers either side, "
                         "nothing below.", 14, INK))
    out.append(t(60, 236, "Check: peak position, width, and nothing at 120-140 bp.", 13.5, MUTE))
    return svg(700, 252, "".join(out))


def fig_trace_dimer():
    out = [t(60, 24, "Adapter dimers: a sharp peak at about 120-140 bp, far from the library.",
             14, INK)]
    out.append(trace(60, 50, 560, 130, [(420, 0.5, 0.07), (130, 0.65, 0.025)], "dimers present"))
    out.append(t(logx(130, 60, 560) + 14, 74, "adapter dimer", 12, BAD))
    out.append(t(60, 236, "They carry both adapters, so qPCR and the sequencer count them. "
                          "Clean up again, or size-select.", 13.5, INK))
    return svg(700, 252, "".join(out))


def fig_trace_overamp():
    out = [t(60, 24, "Over-amplification: the main peak is intact, but a high-size shoulder "
                     "appears.", 14, INK)]
    out.append(trace(60, 50, 560, 130, [(420, 0.7, 0.07), (900, 0.3, 0.12), (2200, 0.16, 0.2)],
                     "primers exhausted"))
    out.append(t(logx(900, 60, 560) + 24, 74, "slower-moving products", 12, BAD))
    out.append(t(60, 236, "Library strands anneal through the shared adapters instead of to "
                          "primers, and run larger. Fewer cycles next time.", 13.5, INK))
    return svg(700, 252, "".join(out))


def fig_trace_gallery():
    out = [t(40, 22, "Three more traces and what they say.", 14, INK)]
    panels = [("too short", [(220, 0.7, 0.06)], "insert shorter than the read:\nadapter read-through"),
              ("too long or wide", [(800, 0.45, 0.2)], "clusters badly; short\nfragments dominate the run"),
              ("no clear peak", [(250, 0.25, 0.4)], "failed fragmentation or\ndegraded input")]
    for i, (h, pk, msg) in enumerate(panels):
        x = 40 + i * 235
        out.append(trace(x, 56, 205, 80, pk, h, ticks=(100, 1000)))
        for j, ln in enumerate(msg.split("\n")):
            out.append(t(x, 188 + j * 15, ln, 12, MUTE))
    return svg(720, 230, "".join(out))


# ---------------------------------------------------------------- tricks

def fig_diag_qpcr():
    out = [t(40, 26, "Diagnostic qPCR: run a small aliquot, stop the real PCR at about one "
                     "third of maximum.", 14, INK)]
    x0, y0, w, h = 80, 48, 420, 140
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    pts = []
    for i in range(0, 41):
        f = 1 / (1 + math.exp(-(i - 19) * 0.4))
        pts.append(f"{x0 + w * i / 40:.1f},{y0 + h - f * h:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" stroke-width="2.4"/>')
    out.append(line(x0, y0 + h - h / 3, x0 + w, y0 + h - h / 3, HOT, 1.4, dash="4 3"))
    out.append(t(x0 + w + 8, y0 + h - h / 3 + 4, "1/3 max", 12, HOT))
    xc = x0 + w * 14.5 / 40
    out.append(line(xc, y0 + h - h / 3, xc, y0 + h, HOT, 1.4, dash="4 3"))
    out.append(t(xc, y0 + h + 18, "extra cycles", 12, HOT, anchor="middle"))
    # beside the plateau, not on it: inside the axes the curve runs through this line
    out.append(t(x0 + w + 8, y0 + 14, "plateau:", 12, BAD))
    out.append(t(x0 + w + 8, y0 + 30, "over-amplified", 12, BAD))
    out.append(t(x0 + w / 2, y0 + h + 36, "cycle", 11, MUTE, anchor="middle"))
    out.append(t(40, 244, "ATAC-seq does five cycles, runs 5 uL in a qPCR, and adds the "
                          "cycles needed to reach one third of maximum.", 13.5, INK))
    out.append(t(40, 266, "The aliquot is spent so that the library is not over-amplified.",
                 13.5, MUTE))
    return svg(700, 284, "".join(out))


def fig_aliquot():
    out = [t(40, 26, "Spend a small aliquot, not the sample: test first, then commit.", 14, INK)]
    out.append(mbox(40, 70, 130, 56, ["reaction", "(whole sample)"], PB, TOP, 12.5, TOP))
    out.append(arrow(176, 98, 250, MUTE))
    out.append(mbox(256, 70, 130, 56, ["next step", "(committed)"], PB, TOP, 12.5, TOP))
    out.append(line(105, 126, 105, 160, MUTE, 1.6))
    out.append(arrow(105, 160, 150, MUTE))
    out.append(mbox(156, 148, 96, 34, ["1 uL aliquot"], PO, HOT, 12, HOT))
    out.append(arrow(256, 165, 306, MUTE))
    out.append(mbox(312, 148, 120, 34, ["trace / qPCR / gel"], "none", MUTE, 12))
    out.append(t(470, 98, "result decides whether", 13, INK))
    out.append(t(470, 116, "the sample goes on", 13, INK))
    out.append(t(40, 218, "1 uL of 25 uL is 4% of the sample. Cheap insurance against a step "
                          "that you cannot undo.", 14, INK))
    out.append(t(40, 240, "Examples: 1 uL on a trace after fragmentation; a test digest; "
                          "10% of the pre-amplified cDNA to qPCR.", 13.5, MUTE))
    return svg(700, 260, "".join(out))


def fig_checkpoints():
    out = [t(40, 26, "Where to look along a protocol, and what each look is for.", 14, INK)]
    steps = [("fragment", "trace: size?"), ("ligate", "aliquot: worked?"),
             ("clean up", "Qubit: yield?"), ("PCR", "qPCR cycles; trace"),
             ("pool", "qPCR: molarity"), ("load", "PhiX; demux")]
    for i, (s, q) in enumerate(steps):
        x = 40 + i * 112
        out.append(mbox(x, 54, 98, 34, [s], PB, TOP, 12.5, TOP))
        out.append(line(x + 49, 88, x + 49, 112, MUTE, 1.2, dash="3 3"))
        out.append(mbox(x, 114, 98, 34, [q], "none", HOT, 11, HOT))
        if i < 5:
            out.append(arrow(x + 100, 71, x + 112, MUTE, head=4))
    out.append(t(40, 184, "A trace after fragmentation costs 1 uL; discovering the same fault at "
                          "the sequencer costs the run.", 14, INK))
    return svg(720, 204, "".join(out))


build(__file__, [
    ("cleanup", fig_cleanup),
    ("spri", fig_spri),
    ("ratio", fig_ratio),
    ("double", fig_double),
    ("measures", fig_measures),
    ("qpcr", fig_qpcr),
    ("qubit-vs-qpcr", fig_qubit_vs_qpcr),
    ("pool", fig_pool),
    ("denature", fig_denature),
    ("trace-ideal", fig_trace_ideal),
    ("trace-dimer", fig_trace_dimer),
    ("trace-overamp", fig_trace_overamp),
    ("trace-gallery", fig_trace_gallery),
    ("diag-qpcr", fig_diag_qpcr),
    ("aliquot", fig_aliquot),
    ("checkpoints", fig_checkpoints),
])
