#!/usr/bin/env python3
"""Figures for the long-reads unit.  Run: python3 long-reads/make-figs.py"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

RNA = "#7a3b5e"
NEW = HOT
TB, TR, TG, TY = "#e8eef5", "#f5eae6", "#e9f1ea", "#f6f0e0"


def lab(x, y, s, size=12, col=MUTE, anchor="start"):
    return t(x, y, s, size, col, anchor=anchor)


def strand(x1, x2, y, col=TOP, w=3.2):
    return line(x1, y, x2, y, col, w, cap="butt")


def scissors(x, y, col=BAD):
    return line(x - 5, y - 6, x + 5, y + 6, col, 1.8) + line(x - 5, y + 6, x + 5, y - 6, col, 1.8)


def motor(x, y, r=7, fill=TY):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{HOT}" stroke-width="1.3"/>'


def hairpin(x, y, side, col=BOT):
    """A hairpin loop closing a duplex end at (x, y..y+14). side=+1 on the right."""
    return (f'<path d="M {x} {y} C {x + side*22} {y - 2}, {x + side*22} {y + 16}, {x} {y + 14}" '
            f'fill="none" stroke="{col}" stroke-width="3"/>')


# ---------------------------------------------------------------- figures

def fig_shear():
    out = [t(40, 26, "Every step that moves the DNA can break it, and a break is a shorter read for good.",
             14, INK)]
    cols = [("fast pipetting, narrow tips", "wide-bore tips, slow", 5),
            ("vortexing, hard bead mixing", "invert or flick gently", 7),
            ("freeze-thaw, old stock", "store cold, aliquot", 4),
            ("nucleases, heat, metal ions", "EDTA, keep cold", 3),
            ("dried beads, hard elution", "wait, elute warm", 2)]
    for i, (bad, good, cuts) in enumerate(cols):
        x0 = 30 + i * 172
        out.append(box(x0, 44, 160, 160, "", "#fbfbf9", MUTE))
        out.append(t(x0 + 80, 66, bad, 11.5, BAD, anchor="middle"))
        random.seed(i + 3)
        pos = sorted(random.sample(range(1, 19), cuts))
        prev = 0
        for p in pos + [20]:
            a, b = x0 + 12 + prev * 7, x0 + 12 + p * 7
            out.append(strand(a + 2, b - 3, 118, TOP, 4))
            prev = p
        out.append(lab(x0 + 80, 160, "gentle alternative:", 11, MUTE, "middle"))
        out.append(t(x0 + 80, 180, good, 11.5, OK, anchor="middle"))
    out.append(t(40, 232, "Schematic: the harsher the handling, the more breaks per molecule.", 13.5, HOT))
    return svg(920, 250, "".join(out))


def fig_molarity():
    out = [t(40, 26, "1 microgram of DNA is a very different number of molecules at different lengths.", 14, INK)]
    rows = [("1 kb", 1540, MUTE), ("10 kb", 154, TOP), ("100 kb", 15.4, HOT)]
    out.append(line(160, 190, 640, 190, MUTE, 1))
    for v in (10, 100, 1000):
        x = 160 + (math.log10(v) - 1) * 160
        out.append(line(x, 190, x, 196, MUTE, 1))
        out.append(lab(x, 212, str(v), 11.5, MUTE, "middle"))
    out.append(lab(400, 230, "femtomoles of molecules in 1 µg (log scale)", 11.5, MUTE, "middle"))
    for i, (n, v, c) in enumerate(rows):
        y = 62 + i * 40
        out.append(t(40, y + 16, n, 13.5, INK))
        w = (math.log10(v) - 1) * 160
        out.append(f'<rect x="160" y="{y}" width="{w:.0f}" height="24" fill="{c}" opacity="0.8"/>')
        out.append(t(160 + w + 8, y + 17, f"{v:g} fmol", 12.5, INK))
    out.append(t(40, 262, "A ligation kit that asks for 100 to 200 fmol is asking for about 1 µg at 10 kb, "
                          "but 10 µg at 100 kb.", 13.5, HOT))
    return svg(760, 282, "".join(out))


def fig_smrt():
    out = [t(40, 26, "SMRTbell prep 3.0: six steps from sheared DNA to a loaded polymerase.", 14, INK)]
    steps = [("shear", "to 15 to 20 kb for\nhuman WGS", TB), ("repair + A-tail", "37 °C 30 min,\nthen 65 °C 5 min", TG),
             ("ligate adapter", "hairpins, 20 °C\n30 min, then cleanup", TY),
             ("nuclease", "37 °C 15 min:\nremoves free ends", TR), ("size select", "35% AMPure PB\ndrops short DNA", TB),
             ("primer + polymerase", "anneal, bind,\nclean up", TG)]
    for i, (h, b, f) in enumerate(steps):
        x = 30 + i * 146
        out.append(box(x, 48, 128, 100, "", f, MUTE))
        out.append(t(x + 64, 70, h, 12.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 64, 96 + j * 16, ln, 11.5, INK, anchor="middle"))
        if i < 5:
            out.append(arrow(x + 130, 98, x + 144, MUTE, 1.4, 4))
    out.append(lab(30, 182, "Each ligation and nuclease step is followed by a bead cleanup; the last of them also "
                            "removes the nuclease.", 12.5, INK))
    out.append(t(30, 222, "The shear size decides the insert size, and therefore the read length and the accuracy.",
                 13.5, HOT))
    return svg(920, 240, "".join(out))


def fig_dumbbell():
    out = [t(40, 26, "The nuclease keeps only molecules with no free end: the closed SMRTbell.", 14, INK)]
    rows = [("closed SMRTbell", True, True, "survives: no end to attack", OK),
            ("unligated insert", False, False, "digested from both ends", BAD),
            ("adapter on one end only", True, False, "digested from the free end", BAD)]
    for i, (n, left, right, note, c) in enumerate(rows):
        y = 60 + i * 56
        x1, x2 = 200, 520
        out.append(t(40, y + 12, n, 13, INK))
        out.append(strand(x1, x2, y, TOP, 3.2))
        out.append(strand(x1, x2, y + 14, BOT, 3.2))
        if left:
            out.append(hairpin(x1, y, -1))
        if right and i == 0:
            out.append(hairpin(x2, y, 1))
        if i == 1:
            out.append(scissors(x1 - 8, y + 7))
            out.append(scissors(x2 + 8, y + 7))
        if i == 2:
            out.append(scissors(x2 + 8, y + 7))
        out.append(lab(560, y + 12, note, 12, c))
    out.append(lab(40, 238, "Closed topology also means the polymerase can go round: forward strand, hairpin, "
                            "reverse strand, hairpin, again.", 12.5, INK))
    out.append(t(40, 266, "The nuclease is what turns a messy ligation into a clean library.", 13.5, HOT))
    return svg(780, 284, "".join(out))


def fig_isoseq():
    out = [t(40, 26, "Iso-Seq: a cDNA with a primer at each end, so that full length is something you can test for.",
             14, INK)]
    x = 60
    parts = [("bc primer", 80, TG, OK), ("5' end, TSO", 60, TB, TOP), ("cDNA, whole transcript", 300, "none", RNA),
             ("poly(A)", 56, TY, HOT), ("3' primer", 80, TB, TOP)]
    for n, w, f, c in parts:
        out.append(box(x, 56, w, 30, n, f, c, 11, c))
        x += w
    out.append(lab(60, 104, "RT from an oligo-dT primer, template switch with the TSO, ~12 cycles of PCR with "
                            "barcoded primers", 12, MUTE))
    out.append(lab(60, 138, "Read classes after HiFi:", 13, INK))
    rows = [("both primers + poly(A)", "full length: keep", OK, [(80, TG), (300, "#cfd6dc"), (80, TB)]),
            ("3' primer only", "RT stopped early or RNA cut: not full length", BAD, [(200, "#cfd6dc"), (80, TB)]),
            ("3' primer inside the read", "chimera of two cDNAs: discard", BAD,
             [(80, TG), (140, "#cfd6dc"), (80, TB), (80, TG), (120, "#cfd6dc"), (80, TB)])]
    for i, (n, v, c, segs) in enumerate(rows):
        y = 156 + i * 32
        out.append(t(60, y + 14, n, 12, INK))
        xx = 280
        for w, f in segs:
            out.append(f'<rect x="{xx}" y="{y}" width="{w}" height="18" fill="{f}" stroke="{MUTE}" stroke-width="0.8"/>')
            xx += w
        out.append(lab(xx + 12, y + 14, v, 12, c))
    out.append(t(60, 270, "Where the isoform is read in one molecule, a splice junction is no longer inferred "
                          "from short pieces.", 13.5, HOT))
    return svg(960, 288, "".join(out))


def fig_kinnex():
    out = [t(40, 26, "Kinnex: join cDNAs end to end, so that one long read holds many transcripts.", 14, INK)]
    out.append(lab(40, 56, "1. split the cDNA into 8 PCRs, each with its own pair of tails", 12.5, INK))
    for i, n in enumerate("ABCDEFGH"):
        x = 60 + i * 52
        out.append(box(x, 66, 42, 26, "HQ" if n == "H" else n, TB if i % 2 == 0 else TG, MUTE, 12, INK))
    out.append(lab(40, 118, "2. pool, then ligate: matching tails force the order 1, 2, ... 8", 12.5, INK))
    for i in range(8):
        x = 60 + i * 62
        out.append(f'<rect x="{x}" y="128" width="54" height="16" fill="{[TB, TG, TY, TR][i % 4]}" stroke="{MUTE}"/>')
        out.append(t(x + 27, 140, str(i + 1), 10.5, INK, anchor="middle"))
    out.append(lab(40, 172, "3. a SMRTbell around the whole array; the polymerase goes round it", 12.5, INK))
    out.append(strand(60, 556, 192, BOT, 4))
    out.append(hairpin(60, 185, -1))
    out.append(hairpin(556, 185, 1))
    out.append(lab(40, 224, "4. software cuts each HiFi read back into its 8 transcripts", 12.5, INK))
    out.append(lab(560, 140, "8 transcripts per array", 12, HOT))
    for i in range(8):
        out.append(f'<rect x="{60 + i * 62}" y="234" width="54" height="14" fill="{[TB, TG, TY, TR][i % 4]}" stroke="{MUTE}"/>')
    out.append(t(40, 282, "A cDNA is a kilobase or two but a HiFi read can be far longer: joining cDNAs fills "
                          "the read with transcripts.", 13.5, HOT))
    return svg(860, 300, "".join(out))


def fig_lsk():
    out = [t(40, 26, "Ligation sequencing: repair and A-tail, ligate the adapter, clean up, load.", 14, INK)]
    out.append(lab(40, 56, "1. repair damage; every end gets a 5' phosphate and a single 3' A", 12.5, INK))
    out.append(strand(120, 520, 80, TOP))
    out.append(strand(120, 520, 94, BOT))
    out.append(t(526, 98, "A", 11, HOT, family=MONO))
    out.append(t(108, 84, "A", 11, HOT, family=MONO))
    out.append(lab(40, 130, "2. the adapter has a T overhang, and a motor protein already on it", 12.5, INK))
    out.append(strand(160, 480, 154, TOP))
    out.append(strand(160, 480, 168, BOT))
    out.append(strand(126, 160, 154, NEW, 3.2))
    out.append(motor(122, 148, 7))
    out.append(strand(480, 514, 154, NEW, 3.2))
    out.append(motor(518, 148, 7))
    out.append(lab(40, 204, "3. bead cleanup with long-fragment buffer (~3 kb and up) or short-fragment buffer (all sizes)",
                   12.5, INK))
    out.append(t(40, 236, "No ethanol after ligation: it denatures the motor protein, so the buffers are "
                          "part of the chemistry.", 13.5, HOT))
    return svg(820, 254, "".join(out))


def fig_rapid():
    out = [t(40, 26, "Rapid kit: a transposase cuts and tags in one step, and the adapter clips on.", 14, INK)]
    out.append(lab(40, 56, "1. transposase complexes bind HMW DNA and cut", 12.5, INK))
    out.append(strand(60, 560, 82, TOP))
    out.append(strand(60, 560, 96, BOT))
    for xx in (190, 330, 450):
        out.append(f'<ellipse cx="{xx}" cy="89" rx="14" ry="16" fill="{TY}" stroke="{HOT}"/>')
    out.append(lab(40, 134, "2. fragments with a tag on each cut end", 12.5, INK))
    for a, b in ((60, 180), (200, 320), (340, 440), (460, 560)):
        out.append(strand(a, b, 160, TOP))
        out.append(strand(a, b, 174, BOT))
        out.append(box(a - 4, 154, 6, 26, "", TR, BAD))
        out.append(box(b - 2, 154, 6, 26, "", TR, BAD))
    out.append(lab(40, 210, "3. adapter with motor attaches to the tag; no enzyme, no cleanup", 12.5, INK))
    for a, b in ((60, 180), (200, 320), (340, 440), (460, 560)):
        out.append(strand(a, b, 232, TOP))
        out.append(strand(a, b, 246, BOT))
        out.append(motor(a - 8, 232, 6))
    out.append(t(40, 284, "Five minutes of hands-on time is bought with shorter reads and lower yield: the "
                          "transposase and loose tags stay in the tube.", 13, HOT))
    return svg(780, 302, "".join(out))


def fig_uhmw():
    out = [t(40, 26, "The same 1 Mb molecule, cut at different densities.", 14, INK)]
    rows = [("shear, then ligation", 42), ("rapid kit", 14), ("ultra-long kit", 4)]
    cols = [TOP, HOT, OK, BOT]
    for i, (n, k) in enumerate(rows):
        y = 70 + i * 54
        out.append(t(40, y + 4, n, 13, INK))
        random.seed(10 + i)
        cuts = sorted(random.sample(range(5, 295), k))
        prev = 0
        for j, c in enumerate(cuts + [300]):
            a, b = 230 + prev * 2.2, 230 + c * 2.2
            out.append(strand(a + 1, b - 1, y, cols[j % 4], 7))
            prev = c
        out.append(lab(230 + 300 * 2.2 + 14, y + 4, f"{k} cuts", 12, MUTE))
    out.append(lab(40, 224, "Dilute the transposase so that most molecules are cut a few times: the pieces "
                            "are then tens to hundreds of kb.", 12.5, INK))
    out.append(lab(40, 244, "The ultra-long kit, SQK-ULK114, targets a read N50 above 50 kb from ultra-HMW DNA.",
                   12.5, INK))
    out.append(t(40, 278, "Schematic. Fewer cuts means longer reads and fewer reads from the same mass of DNA.",
                 13.5, HOT))
    return svg(820, 296, "".join(out))


def fig_native():
    out = [t(40, 26, "Native barcoding: barcode each sample, pool, then one adapter ligation for all.", 14, INK)]
    out.append(lab(40, 52, "1. each sample is end-prepped and gets its own barcode", 12.5, INK))
    for i, c in enumerate([TOP, HOT, OK]):
        y = 80 + i * 36
        out.append(t(40, y + 4, f"sample {i + 1}", 12, INK))
        out.append(strand(140, 330, y, MUTE, 3.2))
        out.append(box(124, y - 7, 16, 14, "", c, c))
        out.append(box(330, y - 7, 16, 14, "", c, c))
    out.append(arrow(360, 116, 420, MUTE))
    out.append(lab(390, 100, "EDTA, pool", 11.5, MUTE, "middle"))
    out.append(lab(430, 52, "2. one pool, one ligation", 12.5, INK))
    for i, c in enumerate([TOP, HOT, OK]):
        y = 80 + i * 36
        out.append(strand(470, 640, y, MUTE, 3.2))
        out.append(box(454, y - 7, 16, 14, "", c, c))
        out.append(box(640, y - 7, 16, 14, "", c, c))
        out.append(motor(444, y, 7))
        out.append(motor(666, y, 7))
    out.append(lab(40, 204, "Samples are mixed in equimolar amounts before barcoding, because after pooling "
                            "the barcode is what tells them apart.", 12.5, INK))
    out.append(lab(40, 224, "No PCR, so base modifications survive; a barcode only tells you which sample, "
                            "not which molecule.", 12.5, INK))
    out.append(t(40, 258, "Barcodes come before the adapter, because the adapter is added to the pool. "
                          "Reverse the order and nothing can be pooled.", 13.5, HOT))
    return svg(860, 276, "".join(out))


def fig_cdna():
    out = [t(40, 26, "Two nanopore routes from RNA to cDNA: amplify it, or do not.", 14, INK)]
    lanes = [("cDNA-PCR (SQK-PCS114)", [("ligate RT adapter\\nto the poly(A)", TB), ("RT and\\nstrand switch", TG),
                                       ("PCR with\\ntagged primers", TY), ("rapid adapter\\nattaches", TR)]),
             ("direct cDNA, no PCR", [("RT +\\nstrand switch", TB), ("second\\nstrand", TG),
                                      ("end-prep,\\ndA-tail", TY), ("ligate\\nadapter", TR)])]
    for r, (n, steps) in enumerate(lanes):
        y = 48 + r * 100
        out.append(t(40, y + 12, n, 13.5, INK, weight="bold"))
        for i, (s_, f) in enumerate(steps):
            x = 60 + i * 190
            out.append(box(x, y + 24, 160, 46, "", f, MUTE))
            for j, ln in enumerate(s_.split("\\n")):
                out.append(t(x + 80, y + 44 + j * 15, ln, 12, INK, anchor="middle"))
            if i < 3:
                out.append(arrow(x + 163, y + 47, x + 187, MUTE, 1.4, 4))
    out.append(lab(40, 262, "cDNA-PCR needs little RNA but PCR favours short transcripts; direct cDNA needs "
                            "far more RNA and avoids amplification bias.", 12, INK))
    out.append(t(40, 290, "RNA to cDNA is the same chemistry as in the RNA unit; what changes is the handle, "
                          "and whether you amplify.", 13.5, HOT))
    return svg(860, 308, "".join(out))


def fig_drna():
    out = [t(40, 26, "Direct RNA: the molecule that is sequenced is the RNA itself, read from its 3' end.", 14, INK)]
    out.append(lab(40, 56, "1. adapter on the 3' poly(A) end", 12.5, INK))
    out.append(strand(80, 440, 80, RNA, 3.5))
    out.append(dot(76, 80, 4.5, HOT))
    out.append(t(444, 84, "AAAA", 11, RNA, family=MONO))
    out.append(box(480, 70, 60, 20, "RTA", TB, TOP, 11, TOP))
    out.append(lab(40, 122, "2. RT makes a cDNA strand: it steadies the RNA and is not sequenced", 12.5, INK))
    out.append(strand(80, 440, 146, RNA, 3.5))
    out.append(strand(120, 440, 160, BOT, 3))
    out.append(box(480, 136, 60, 20, "RTA", TB, TOP, 11, TOP))
    out.append(lab(40, 198, "3. the motor adapter ligates to the 3' end, and the RNA strand goes through the pore",
                   12.5, INK))
    out.append(strand(80, 440, 222, RNA, 3.5))
    out.append(strand(120, 440, 236, BOT, 3))
    out.append(box(480, 212, 60, 20, "RLA", TY, HOT, 11, HOT))
    out.append(motor(560, 222, 8))
    out.append(arrow(430, 262, 90, HOT, 1.6, 5))
    out.append(lab(260, 282, "read direction: 3' to 5'", 12, HOT, "middle"))
    out.append(t(40, 312, "No RT bias, no PCR, and modifications are in the signal. The price is that the whole "
                          "RNA must be intact and plentiful.", 13.5, HOT))
    return svg(860, 330, "".join(out))


def fig_cas9():
    out = [t(40, 26, "Cas9 enrichment: only the cut ends can take an adapter.", 14, INK)]
    out.append(lab(40, 52, "1. dephosphorylate every existing end", 12.5, INK))
    out.append(strand(80, 700, 76, TOP))
    out.append(lab(70, 80, "OH", 10.5, BAD, "end"))
    out.append(lab(708, 80, "OH", 10.5, BAD))
    out.append(lab(40, 112, "2. Cas9 cuts either side of the target: fresh 5' phosphate ends", 12.5, INK))
    out.append(strand(80, 700, 138, MUTE))
    out.append(strand(260, 520, 138, HOT, 6))
    for xx in (260, 520):
        out.append(scissors(xx, 124))
        out.append(lab(xx, 160, "P", 11, OK, "middle"))
    out.append(lab(390, 124, "target", 12, HOT, "middle"))
    out.append(lab(40, 188, "3. A-tail, then ligate: adapters join only where there is a phosphate", 12.5, INK))
    out.append(strand(80, 250, 212, MUTE))
    out.append(strand(270, 510, 212, HOT, 6))
    out.append(strand(530, 700, 212, MUTE))
    for xx in (252, 524):
        out.append(motor(xx - 4 if xx < 300 else xx + 6, 212, 7))
    out.append(lab(390, 240, "adapters on the target ends", 11.5, OK, "middle"))
    out.append(lab(40, 266, "Background DNA has no phosphate, so it is not sequenced, and no PCR is "
                            "needed, so modifications survive.", 12.5, INK))
    out.append(t(40, 298, "Enrichment is chemical: the cut is what makes the molecule sequenceable.", 13.5, HOT))
    return svg(860, 316, "".join(out))


def fig_adaptive():
    out = [t(40, 26, "Adaptive sampling: decide at the pore, from the first bases of the molecule.", 14, INK)]
    steps = [("a pore captures\na molecule", TB), ("the first few\nhundred bases\nare read", TG),
             ("basecall and\nmatch to the\ntarget list", TY)]
    for i, (n, f) in enumerate(steps):
        x = 40 + i * 190
        out.append(box(x, 56, 160, 76, "", f, MUTE))
        for j, ln in enumerate(n.split("\n")):
            out.append(t(x + 80, 82 + j * 16, ln, 12, INK, anchor="middle"))
        out.append(arrow(x + 163, 94, x + 187, MUTE, 1.4, 4))
    out.append(box(610, 40, 190, 46, "", TG, OK))
    out.append(t(705, 68, "on target: keep reading", 12, OK, anchor="middle"))
    out.append(box(610, 102, 190, 46, "", TR, BAD))
    out.append(t(705, 130, "off target: reverse voltage, eject", 12, BAD, anchor="middle"))
    out.append(lab(40, 178, "No wet-lab step: the target list is a file, so changing the target means changing "
                            "the file.", 12.5, INK))
    out.append(lab(40, 198, "The cost: ejected molecules still occupy the pore for a moment, and a blocked "
                            "pore ends the saving.", 12.5, INK))
    out.append(t(40, 232, "Enrichment is a ratio, and it is spent on pore time, so a short run on a rich "
                          "library beats a long one on a poor library.", 13.5, HOT))
    return svg(860, 250, "".join(out))


build(__file__, [
    ("shear", fig_shear),
    ("molarity", fig_molarity),
    ("smrt", fig_smrt),
    ("dumbbell", fig_dumbbell),
    ("isoseq", fig_isoseq),
    ("kinnex", fig_kinnex),
    ("lsk", fig_lsk),
    ("rapid", fig_rapid),
    ("uhmw", fig_uhmw),
    ("native", fig_native),
    ("cdna", fig_cdna),
    ("drna", fig_drna),
    ("cas9", fig_cas9),
    ("adaptive", fig_adaptive),
])
