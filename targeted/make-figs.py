#!/usr/bin/env python3
"""Figures for the targeted unit.  Run: python3 targeted/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE = "#eef2f6"
PALE_OK = "#e3efe6"
PALE_BAD = "#f4e0dc"
ADA = "#c98a2b"


def path(d, stroke=INK, w=1.6, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def rect(x, y, w, h, fill, stroke="none", r=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def poly(pts, col, w=2.4):
    return path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), col, w)


# ------------------------------------------------------------------ figures

def fig_strategies():
    out = [t(20, 24, "Three ways to look at 1% of the genome: amplify it, catch it, or copy it out.", 14)]
    panels = [("Amplicon PCR", "primer pairs flank each target"),
              ("Hybrid capture", "biotinylated baits pull fragments"),
              ("Probe circularisation", "probe closes only on its target")]
    for i, (h, sub) in enumerate(panels):
        x = 20 + i * 270
        out.append(t(x, 56, h, 13.5, INK, weight="bold"))
        out.append(t(x, 72, sub, 12, MUTE))
        out.append(line(x, 120, x + 240, 120, TOP, 3))
        out.append(rect(x + 80, 112, 80, 16, PALE_OK, OK))
        out.append(t(x + 120, 106, "target", 11.5, OK, anchor="middle"))
        if i == 0:
            out.append(arrow(x + 60, 100, x + 100, HOT))
            out.append(arrow(x + 190, 142, x + 150, HOT))
            out.append(t(x, 170, "product: only the region between", 12, MUTE))
            out.append(t(x, 185, "the two primers, exponentially", 12, MUTE))
        elif i == 1:
            out.append(line(x + 85, 112, x + 85, 90, HOT, 2))
            out.append(line(x + 155, 112, x + 155, 90, HOT, 2))
            out.append(dot(x + 85, 86, 5, HOT))
            out.append(dot(x + 155, 86, 5, HOT))
            out.append(t(x, 170, "everything else is washed away,", 12, MUTE))
            out.append(t(x, 185, "then PCR amplifies what stayed", 12, MUTE))
        else:
            out.append(path(f"M {x+82} 112 C {x+60} 80 {x+180} 80 {x+158} 112", HOT, 2.2))
            out.append(t(x, 170, "ligase seals a circle; nucleases", 12, MUTE))
            out.append(t(x, 185, "remove all linear DNA", 12, MUTE))
    return svg(820, 204, "".join(out))


def fig_tiling():
    out = [t(20, 24, "Tiled amplicons: overlapping products, alternate ones in separate pools.", 14)]
    out.append(line(30, 60, 780, 60, TOP, 4))
    out.append(t(30, 48, "region to cover (for example a gene, or a viral genome)", 12, MUTE))
    cols = [OK, HOT]
    for i in range(7):
        x = 30 + i * 100
        y = 90 if i % 2 == 0 else 120
        out.append(rect(x, y, 150, 12, cols[i % 2]))
        out.append(t(x + 75, y + 10, f"{i+1}", 10.5, "#ffffff", anchor="middle"))
    out.append(t(30, 168, "pool 1: amplicons 1, 3, 5, 7", 12.5, OK))
    out.append(t(30, 184, "pool 2: amplicons 2, 4, 6", 12.5, HOT))
    out.append(t(300, 168, "Neighbours overlap, so a failed amplicon leaves a gap only if both", 12.5, MUTE))
    out.append(t(300, 184, "sides fail; separate pools stop overlapping primers from priming each other.", 12.5, MUTE))
    return svg(820, 204, "".join(out))


def fig_amplicon_failures():
    out = [t(20, 24, "How multiplex PCR fails, and what you would see.", 14)]
    rows = [("primer dimer", "two primers anneal to each other", "short peak, wasted reads", BAD),
            ("allele dropout", "a variant under a primer prevents annealing", "one allele missing: false homozygote", BAD),
            ("uneven efficiency", "some primer pairs work better", "10-fold spread in depth", HOT),
            ("cross-products", "primers from different pairs join", "chimeric, off-target reads", HOT)]
    for i, (a, b, c, col) in enumerate(rows):
        y = 56 + i * 34
        out.append(t(20, y, a, 13.5, col, weight="bold"))
        out.append(t(160, y, b, 12.5, INK))
        out.append(t(470, y, c, 12.5, MUTE))
    # allele dropout mini drawing
    out.append(line(120, 200, 340, 200, TOP, 3))
    out.append(arrow(150, 190, 240, OK))
    out.append(dot(260, 200, 6, BAD))
    out.append(t(260, 224, "SNP in primer site", 12, BAD, anchor="middle"))
    out.append(t(380, 200, "The primer is 20 nt; one mismatch near its 3' end can stop it priming.", 12.5, INK))
    return svg(800, 240, "".join(out))


def fig_hybrid():
    out = [t(20, 24, "Hybrid capture: library first, then pull down what a bait matches.", 14)]
    steps = [("1 Library", "fragments with\nadapters on both ends"),
             ("2 Hybridise", "biotinylated baits anneal\nto target-derived fragments"),
             ("3 Streptavidin beads", "bind biotin; wash away\nthe rest of the genome"),
             ("4 PCR", "amplify the captured\nlibrary; sequence")]
    for i, (h, body) in enumerate(steps):
        x = 24 + i * 200
        out.append(t(x, 52, h, 13.5, INK, weight="bold"))
        if i == 0:
            for k, yy in enumerate([84, 102, 120]):
                out.append(rect(x, yy - 4, 8, 8, ADA))
                out.append(line(x + 8, yy, x + 100, yy, TOP, 3))
                out.append(rect(x + 100, yy - 4, 8, 8, ADA))
        elif i == 1:
            out.append(rect(x, 84 - 4, 8, 8, ADA))
            out.append(line(x + 8, 84, x + 100, 84, TOP, 3))
            out.append(rect(x + 100, 80, 8, 8, ADA))
            out.append(line(x + 20, 92, x + 88, 92, HOT, 3))
            out.append(dot(x + 90, 92, 5, HOT))
            out.append(line(x + 8, 114, x + 100, 114, MUTE, 3))
            out.append(t(x + 110, 90, "match", 11.5, OK))
            out.append(t(x + 110, 118, "no match", 11.5, MUTE))
        elif i == 2:
            out.append(dot(x + 40, 98, 18, "#d6dce2"))
            out.append(line(x + 40, 98, x + 80, 84, HOT, 2))
            out.append(line(x + 8, 124, x + 100, 124, MUTE, 2, dash="3 4"))
            out.append(t(x + 112, 128, "washed out", 11.5, MUTE))
        else:
            out.append(line(x, 90, x + 100, 90, TOP, 3))
            out.append(line(x, 100, x + 100, 100, BOT, 3))
            out.append(t(x + 112, 98, "x 8 to 12", 12, MUTE))
        for k, ln in enumerate(body.split("\n")):
            out.append(t(x, 166 + k * 15, ln, 12, MUTE))
        if i < 3:
            out.append(arrow(x + 150, 100, x + 184, MUTE))
    out.append(t(24, 218, "Blocking oligos against the adapters prevent library fragments pulling each other down.", 13, INK))
    return svg(820, 236, "".join(out))


def fig_mip():
    out = [t(20, 24, "Molecular inversion probe: capture, gap fill, close into a circle.", 14)]
    out.append(line(60, 120, 560, 120, TOP, 4))
    out.append(rect(240, 112, 120, 16, PALE_OK, OK))
    out.append(t(300, 150, "gap to be copied", 12, OK, anchor="middle"))
    # probe arms
    out.append(line(200, 110, 240, 110, HOT, 3.5))
    out.append(line(360, 110, 400, 110, HOT, 3.5))
    out.append(path("M 200 110 C 170 40 430 40 400 110", ADA, 3))
    out.append(t(300, 54, "backbone + random tag", 12.5, ADA, anchor="middle"))
    out.append(t(180, 100, "arm 1", 11.5, HOT, anchor="end"))
    out.append(t(420, 100, "arm 2", 11.5, HOT))
    out.append(arrow(246, 104, 350, BOT))
    out.append(t(300, 96, "polymerase", 11.5, BOT, anchor="middle"))
    out.append(t(20, 190, "A ligase can close the circle only when both arms sit on the target and the gap is filled.", 13.5, INK))
    out.append(t(20, 210, "Exonuclease then destroys all linear DNA, including the genome and unused probes.", 13.5, INK))
    return svg(640, 226, "".join(out))


def fig_cas9():
    out = [t(20, 24, "Cas9-guided enrichment: cut where you want to read, and ligate adapters only there.", 14)]
    out.append(line(30, 80, 640, 80, TOP, 3))
    out.append(line(30, 90, 640, 90, BOT, 3))
    for x in (60, 140, 220, 440, 520, 600):
        out.append(dot(x, 85, 4, MUTE))
    out.append(t(30, 66, "1 Dephosphorylate all ends: background cannot ligate", 12.5, MUTE))
    out.append(line(300, 60, 300, 112, HOT, 2.5, dash="4 3"))
    out.append(line(380, 60, 380, 112, HOT, 2.5, dash="4 3"))
    out.append(t(340, 130, "2 Cas9 cuts both sides of the target,", 12.5, HOT, anchor="middle"))
    out.append(t(340, 146, "leaving 5'-phosphate ends", 12.5, HOT, anchor="middle"))
    out.append(rect(296, 160, 10, 10, ADA))
    out.append(line(306, 165, 374, 165, TOP, 3))
    out.append(rect(374, 160, 10, 10, ADA))
    out.append(t(396, 169, "3 Ligate sequencing adapters: only cut ends take them", 12.5, ADA))
    out.append(t(20, 208, "Read by nanopore, so long reads and modifications are preserved. See nCATS (Gilpatrick et al.).", 13, INK))
    return svg(720, 224, "".join(out))


def fig_digest():
    out = [t(20, 24, "Reduced representation: a restriction enzyme chooses the same fragments in every sample.", 14)]
    out.append(line(30, 70, 780, 70, TOP, 3))
    sites = [70, 120, 135, 220, 330, 345, 470, 560, 575, 700]
    for s in sites:
        out.append(line(30 + s, 58, 30 + s, 82, HOT, 2))
    # CpG island cluster
    out.append(rect(30 + 100, 94, 60, 10, PALE_OK, OK))
    out.append(t(30 + 130, 118, "CpG island", 12, OK, anchor="middle"))
    out.append(rect(30 + 310, 94, 60, 10, PALE_OK, OK))
    out.append(rect(30 + 540, 94, 60, 10, PALE_OK, OK))
    out.append(t(30, 56, "MspI cuts at C^CGG: it finds CpG-rich DNA", 12.5, HOT))
    # selected fragments
    for a, b in [(120, 135), (330, 345), (560, 575)]:
        out.append(rect(30 + a, 140, b - a, 12, OK))
    out.append(t(30, 150, "kept", 12, OK))
    out.append(t(30, 182, "Short fragments between close-by sites are retained; the rest of the genome is never sequenced.", 13, INK))
    out.append(t(30, 200, "The same idea with one or two enzymes gives RAD, ddRAD and GBS for genotyping.", 13, INK))
    return svg(820, 216, "".join(out))


def fig_bisulfite():
    out = [t(20, 24, "Bisulfite conversion: unmethylated C becomes T, methylated C stays C.", 14)]
    s = "ATCGGTCACGTTCGAC"
    meth = {2, 8, 12}   # methylated CpG positions (the C of CG)
    for i, ch in enumerate(s):
        pass
    x0 = 150
    out.append(t(x0 - 14, 66, "genome", 13, MUTE, anchor="end"))
    out.append(t(x0 - 14, 126, "after bisulfite", 13, MUTE, anchor="end"))
    out.append(t(x0 - 14, 96, "methylation", 12, MUTE, anchor="end"))
    for i, ch in enumerate(s):
        x = x0 + i * 16
        out.append(t(x, 66, ch, 14, INK, family=MONO))
        if ch == "C":
            m = i in meth
            if m:
                out.append(dot(x + 4, 90, 4, HOT))
            conv = "C" if m else "T"
            out.append(t(x, 126, conv, 14, HOT if m else BAD, family=MONO, weight="bold"))
            out.append(line(x + 4, 72, x + 4, 112, MUTE, 1, dash="2 3"))
        else:
            out.append(t(x, 126, ch, 14, INK, family=MONO))
    out.append(t(x0, 166, "Read C = it was methylated. Read T = it was not. Positions 3, 9 and 13", 13, INK))
    out.append(t(x0, 184, "are methylated CpGs (dots); every other C reads as T.", 13, INK))
    return svg(640, 200, "".join(out))


def fig_error_floor():
    out = [t(20, 24, "A real variant at 0.1% and a sequencing error look the same.", 14)]
    x0, base = 70, 190
    bars = [("A (true)", 1000, TOP), ("G: error", 2, BAD), ("C: error", 1, BAD), ("T: variant", 1, HOT)]
    out.append(line(x0 - 10, base, x0 + 420, base, MUTE, 1.2))
    for i, (lab, n, col) in enumerate(bars):
        x = x0 + i * 100
        h = max(4, math.log10(n + 1) * 36)
        out.append(rect(x, base - h, 50, h, col))
        out.append(t(x + 25, base + 18, lab, 12, MUTE, anchor="middle"))
    out.append(t(x0, 52, "reads at one position, 1000 reads (counts illustrative; log height)", 12.5, MUTE))
    out.append(t(500, 100, "The one true variant read cannot", 13, INK))
    out.append(t(500, 118, "be told apart from the errors that", 13, INK))
    out.append(t(500, 136, "have the same count.", 13, INK))
    out.append(t(500, 164, "Error rate is of the order of 0.1%", 12.5, MUTE))
    out.append(t(500, 180, "per base for Illumina data.", 12.5, MUTE))
    return svg(800, 224, "".join(out))


def fig_umi():
    out = [t(20, 24, "A UMI lets reads vote: errors differ between reads, the variant does not.", 14)]
    fams = [("molecule 1", "tag AGTC", "ACGTTCGA", [None, None, None]),
            ("molecule 2", "tag CCAT", "ACGTTCGA", [None, 5, None]),
            ("molecule 3", "tag TTGA", "ACGATCGA", [None, None, None])]
    for i, (name, tag, s, err) in enumerate(fams):
        y = 56 + i * 76
        out.append(t(20, y + 4, name, 12.5, INK, weight="bold"))
        out.append(t(20, y + 20, tag, 11.5, ADA, family=MONO))
        for k in range(3):
            yy = y + k * 15
            for j, ch in enumerate(s):
                col = INK
                c = ch
                if i == 1 and k == 1 and j == 5:
                    c, col = "A", BAD
                if i == 2 and j == 3:
                    col = HOT
                out.append(t(130 + j * 13.5, yy + 4, c, 13, col, family=MONO))
        out.append(arrow(260, y + 18, 300, MUTE))
        cons = s
        for j, ch in enumerate(cons):
            col = HOT if (i == 2 and j == 3) else INK
            out.append(t(320 + j * 13.5, y + 22, ch, 13, col, family=MONO))
        verdict = "variant kept: all reads agree" if i == 2 else ("error voted out" if i == 1 else "no change")
        out.append(t(450, y + 22, verdict, 12.5, HOT if i == 2 else (OK if i == 1 else MUTE)))
    out.append(t(20, 280, "Reads sharing a tag are one molecule: collapse them to one consensus.", 13.5, INK))
    return svg(720, 296, "".join(out))


def fig_duplex():
    out = [t(20, 24, "Duplex sequencing: both strands of one molecule must agree.", 14)]
    top, bot = "ACGTTCGAAC", "TGCAAGCTTG"
    b, w = duplex(60, 70, top, bot)
    out.append(b)
    out.append(t(60, 56, "original duplex, tagged at each end", 12.5, MUTE))
    out.append(t(60 + w + 60, 78, "top strand reads", 12.5, TOP))
    out.append(t(60 + w + 60, 108, "bottom strand reads", 12.5, BOT))
    rows = [("strand A consensus", "ACGTTCGAAC", INK, ""),
            ("strand B consensus", "TGCAAGCTTG", INK, ""),
            ("duplex consensus", "ACGTTCGAAC", OK, "agree: accepted")]
    out.append(t(60, 150, "A damage or PCR error on one strand shows only on that strand:", 13, INK))
    out.append(t(60, 172, "strand A read:  ACGTTCGAAC", 13, INK, family=MONO))
    out.append(t(60, 190, "strand B read:  TGCAAGCTTG, complement matches: no mutation", 13, OK, family=MONO))
    out.append(t(60, 214, "strand A read:  ACGTTCTAAC", 13, BAD, family=MONO))
    out.append(t(60, 232, "strand B read:  TGCAAGCTTG, does not match A: rejected", 13, BAD, family=MONO))
    out.append(t(60, 256, "A true mutation is present on both strands, in complementary form.", 13, INK))
    return svg(680, 272, "".join(out))


def fig_umi_placement():
    out = [t(20, 24, "Where the tag goes decides what it protects against.", 14)]
    rows = [("Safe-SeqS", "gene-specific primer with a random tag, first PCR cycles", "amplification errors"),
            ("smMIP", "random tag is inside the probe, before any PCR", "amplification and capture"),
            ("SureSelect XT HS2 (MBC)", "adapter carries the tag, before capture and PCR", "amplification and capture"),
            ("Duplex sequencing", "tag on both strands, strand-linked", "also damage on one strand")]
    for j, c in enumerate(["protocol", "where the tag enters", "what it can correct"]):
        out.append(t([20, 230, 600][j], 52, c, 13, INK, weight="bold"))
    out.append(line(20, 60, 800, 60, MUTE, 1))
    for i, (a, b, c) in enumerate(rows):
        y = 84 + i * 30
        out.append(t(20, y, a, 12.5, HOT, weight="bold"))
        out.append(t(230, y, b, 12.5, INK))
        out.append(t(600, y, c, 12.5, MUTE))
    out.append(t(20, 224, "A tag added after PCR cannot tell PCR copies from distinct molecules.", 13.5, INK))
    return svg(840, 240, "".join(out))


def fig_poisson():
    lam = 3.0
    out = [t(20, 24, "10 ng of cell-free DNA holds about 3 mutant molecules at 0.1% (Poisson).", 14)]
    x0, base = 60, 190
    out.append(line(x0 - 10, base, x0 + 400, base, MUTE, 1.2))
    for k in range(0, 9):
        p = math.exp(-lam) * lam ** k / math.factorial(k)
        h = p * 480
        col = BAD if k < 2 else OK
        out.append(rect(x0 + k * 44, base - h, 30, h, col))
        out.append(t(x0 + k * 44 + 15, base + 18, str(k), 12.5, MUTE, anchor="middle"))
        out.append(t(x0 + k * 44 + 15, base - h - 5, f"{p*100:.0f}%", 11, INK, anchor="middle"))
    out.append(t(x0 + 190, base + 40, "mutant molecules present in the sample", 12.5, MUTE, anchor="middle"))
    out.append(t(500, 80, "5% of the time no mutant", 13, BAD))
    out.append(t(500, 98, "molecule is there at all", 13, BAD))
    out.append(t(500, 128, "80% of the time two or more:", 13, OK))
    out.append(t(500, 146, "enough to require two molecules", 13, OK))
    out.append(t(500, 176, "More reads cannot add molecules.", 13, INK))
    return svg(780, 236, "".join(out))


def fig_family_hist():
    out = [t(20, 24, "Reads per UMI family: the shape tells you whether the library is deep enough.", 14)]
    lam = 4.0
    x0, base = 60, 190
    out.append(line(x0 - 10, base, x0 + 400, base, MUTE, 1.2))
    z = 1 - math.exp(-lam)
    for k in range(1, 12):
        p = math.exp(-lam) * lam ** k / math.factorial(k) / z
        h = p * 520
        col = BAD if k == 1 else TOP
        out.append(rect(x0 + (k - 1) * 34, base - h, 24, h, col))
        out.append(t(x0 + (k - 1) * 34 + 12, base + 18, str(k), 11.5, MUTE, anchor="middle"))
    out.append(t(x0 + 190, base + 40, "reads in the family", 12.5, MUTE, anchor="middle"))
    out.append(t(500, 80, "Families of one read cannot be", 13, BAD))
    out.append(t(500, 98, "corrected: they carry the error.", 13, BAD))
    out.append(t(500, 128, "Counts are zero-truncated Poisson,", 12.5, MUTE))
    out.append(t(500, 144, "mean 4 reads per molecule.", 12.5, MUTE))
    out.append(t(500, 174, "Large families = deep, but you", 12.5, INK))
    out.append(t(500, 190, "need many molecules as well.", 12.5, INK))
    return svg(780, 236, "".join(out))


def fig_sureselect():
    out = [t(20, 24, "SureSelect XT HS2: the molecular barcode is on the adapter, so it survives capture.", 14)]
    labels = ["fragment", "end repair\nA-tail", "ligate adapter\n(with MBC)", "index PCR", "pool,\nhybridise baits", "post-capture\nPCR"]
    for i, lab in enumerate(labels):
        x = 20 + i * 130
        l1 = lab.split("\n")
        h = 46
        out.append(box(x, 50, 112, h, "", fill=PALE if i != 2 else "#f7e7dd", stroke=MUTE if i != 2 else HOT))
        for k, ln in enumerate(l1):
            out.append(t(x + 56, 70 + k * 15 - (7 if len(l1) == 2 else -2), ln, 12, INK, anchor="middle"))
        if i < 5:
            out.append(arrow(x + 114, 73, x + 128, MUTE))
    out.append(t(20, 134, "Order of the steps: tag first, amplify, capture, amplify again. All PCR duplicates of one", 13, INK))
    out.append(t(20, 152, "molecule keep its tag, so reads can be grouped back to the original molecule.", 13, INK))
    out.append(t(20, 178, "Pooling indexed libraries before capture lets one capture reaction serve many samples.", 13, MUTE))
    return svg(800, 196, "".join(out))


def fig_compare():
    out = [t(20, 24, "Targeting methods side by side (qualitative).", 14)]
    cols = ["", "Tiled amplicon", "Hybrid capture", "smMIP / padlock", "Cas9 + nanopore"]
    cw = [110, 170, 170, 170, 170]
    xs = [20]
    for w in cw[:-1]:
        xs.append(xs[-1] + w)
    rows = [("target size", "small to medium", "kb to tens of Mb", "kb to Mb", "a few loci"),
            ("input", "ng or less", "10 to 200 ng typical", "tens of ng", "µg"),
            ("uniformity", "primer dependent", "good, bait dependent", "probe dependent", "n/a"),
            ("sequence-specific", "primers per target", "bait tiling", "probe per target", "guide per target"),
            ("UMI possible", "yes, in primer", "yes, in adapter", "yes, in probe", "not standard"),
            ("strength", "cheap, fast", "flexible, big panels", "tiny input, accurate", "long, modified DNA")]
    for j, c in enumerate(cols):
        out.append(t(xs[j] + 4, 50, c, 12.5, INK, weight="bold"))
    out.append(line(20, 58, 840, 58, MUTE, 1))
    for i, r in enumerate(rows):
        y = 80 + i * 26
        for j, c in enumerate(r):
            out.append(t(xs[j] + 4, y, c, 12.5, MUTE if j == 0 else INK))
    return svg(870, 246, "".join(out))


def fig_decision():
    out = [t(20, 24, "From question to targeting method: a decision sketch.", 14)]
    rows = [("a few loci, many samples", "multiplex PCR, tiled amplicons", OK),
            ("tens to thousands of genes", "hybrid capture, with UMIs if rare variants", ADA),
            ("tiny panel, very low input", "smMIPs or padlock probes", HOT),
            ("methylation at CpG-rich regions", "RRBS: restriction enzyme + bisulfite", BAD),
            ("a locus in native long DNA", "Cas9-guided enrichment, nanopore", MUTE)]
    for i, (a, b, col) in enumerate(rows):
        y = 44 + i * 48
        out.append(box(20, y, 250, 34, a, fill=PALE, size=12.5))
        out.append(arrow(276, y + 17, 316, col))
        out.append(box(322, y, 400, 34, b, fill=PALE, stroke=col, size=12.5))
    return svg(740, 288, "".join(out))


build(__file__, [
    ("strategies", fig_strategies),
    ("tiling", fig_tiling),
    ("amplicon-failures", fig_amplicon_failures),
    ("hybrid-capture", fig_hybrid),
    ("mip", fig_mip),
    ("cas9", fig_cas9),
    ("digest", fig_digest),
    ("bisulfite", fig_bisulfite),
    ("error-floor", fig_error_floor),
    ("umi", fig_umi),
    ("duplex", fig_duplex),
    ("umi-placement", fig_umi_placement),
    ("poisson", fig_poisson),
    ("family-hist", fig_family_hist),
    ("sureselect", fig_sureselect),
    ("compare", fig_compare),
    ("decision", fig_decision),
])
