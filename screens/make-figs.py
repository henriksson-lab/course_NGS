#!/usr/bin/env python3
"""Figures for the pooled-screens unit (both decks).  Run: python3 screens/make-figs.py"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

BLUE, RED, GREEN, TAN, GREY = "#e8eef5", "#f5eae6", "#e6f0e8", "#f3ecd9", "#eceff1"
PAL = [TOP, HOT, OK, BOT, BAD, "#7a5c99", "#b08a1e", "#2c7d83"]
STY = {"b": (BLUE, TOP), "r": (RED, BAD), "g": (GREEN, OK), "t": (TAN, HOT), "k": (GREY, MUTE)}


def comp(s):
    return "".join({"A": "T", "T": "A", "G": "C", "C": "G"}[c] for c in s)


def cons(x, y, parts, h=28, size=12, gap=0):
    """A linear construct from (label, width, style) parts. Returns (svg, end_x)."""
    out = []
    for lab, w, st in parts:
        f, s_ = STY[st]
        out.append(box(x, y, w, h, lab, f, s_, size, s_))
        x += w + gap
    return "".join(out), x


def lines3(x, y, rows, size=12.5, fill=MUTE, step=17, anchor="start"):
    return "".join(t(x, y + i * step, r, size, fill, anchor=anchor) for i, r in enumerate(rows))


def row_of_boxes(x0, y, labels, w, h, gap, styles=None, size=12.5):
    out = []
    for i, l in enumerate(labels):
        f, s_ = STY[(styles or "b" * len(labels))[i]]
        x = x0 + i * (w + gap)
        out.append(box(x, y, w, h, l, f, s_, size, s_))
        if i < len(labels) - 1:
            out.append(arrow(x + w + 2, y + h / 2, x + w + gap - 2, MUTE, 1.4, 5))
    return "".join(out)


# ================================================================ lec.qmd (build)

def fig_pipeline():
    out = []
    labels = ["oligo pool", "plasmid library", "lentivirus", "cells", "selection", "genomic DNA", "PCR, sequence"]
    out.append(row_of_boxes(30, 40, labels, 104, 40, 14, "bbbbrrr", 12))
    x4 = 30 + 3 * 118 + 104
    out.append(line(30, 100, x4, 100, TOP, 2))
    out.append(t(30, 120, "building the library (this deck)", 13, TOP))
    out.append(line(x4 + 14, 100, 30 + 6 * 118 + 104, 100, BAD, 2))
    out.append(t(x4 + 14, 120, "reading it out (next deck)", 13, BAD))
    out.append(lines3(30, 160, ["Each box is a bottleneck: a guide lost in any of them is gone for good,",
                                "and the counts at the end only mean something if every box was kept wide."], 13, INK))
    return svg(790, 220, "".join(out))


def fig_oligo_arch():
    out = [t(30, 26, "One 74-nt member of a guide pool (the GeCKO v2 design)", 14, INK)]
    pre, post = "TGGAAAGGACGAAACACCG", "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGC"
    k = 7.4
    x = 40
    s1, x1 = cons(x, 50, [("hU6 + G", len(pre) * k, "b"), ("guide", 20 * k, "t"), ("scaffold", len(post) * k, "b")], h=30, size=12.5)
    out.append(s1)
    out.append(t(x, 112, pre, 9.5, TOP, family=MONO))
    out.append(t(x + len(pre) * k + 2, 112, "N" * 20, 9.5, HOT, family=MONO))
    out.append(t(x + (len(pre) + 20) * k + 4, 112, post, 9.5, TOP, family=MONO))
    out.append(line(x, 92, x + 19 * k, 92, MUTE, 1)); out.append(t(x, 90, "19 nt", 11, MUTE))
    out.append(t(x + 19 * k + 4, 90, "20 nt, one per oligo", 11, HOT))
    out.append(t(x + 39 * k + 10, 90, "35 nt", 11, MUTE))
    out.append(t(30, 152, "Constant ends, variable middle. The constant ends are what a pair of primers binds,", 13.5, INK))
    out.append(t(30, 172, "so one primer pair can amplify every member of the pool, and also what lets each", 13.5, INK))
    out.append(t(30, 192, "oligo be joined to a vector by homology.", 13.5, INK))
    return svg(760, 214, "".join(out))


def fig_array_synthesis():
    out = [t(30, 26, "Chip synthesis grows many sequences in parallel, one base per cycle", 14, INK)]
    out.append(f'<rect x="30" y="44" width="170" height="130" rx="6" fill="{GREY}" stroke="{MUTE}"/>')
    for i in range(10):
        for j in range(8):
            out.append(f'<rect x="{40 + i*16}" y="{54 + j*15}" width="10" height="10" fill="{PAL[(i*3+j*5)%8]}" opacity="0.8"/>')
    out.append(t(30, 196, "each spot makes one sequence", 12.5, MUTE))
    labs = ["deprotect", "couple a base", "cap failures", "oxidise"]
    for i, l in enumerate(labs):
        x = 250 + i * 118
        out.append(box(x, 70, 104, 34, l, BLUE if i != 1 else RED, TOP if i != 1 else HOT, 12.5))
        if i < 3:
            out.append(arrow(x + 106, 87, x + 116, MUTE, 1.4, 5))
    out.append(f'<path d="M 654 106 L 654 130 L 302 130 L 302 108" fill="none" stroke="{MUTE}" stroke-width="1.4"/>')
    out.append(f'<path d="M 302 106 l -4 8 l 8 0 z" fill="{MUTE}"/>')
    out.append(t(478, 150, "repeat for every position; each cycle fails a little", 12.5, MUTE, anchor="middle"))
    out.append(t(30, 232, "Finally everything is cleaved off and pooled: ~10^5 sequences in one tube, in tiny amounts.", 14, HOT))
    return svg(720, 250, "".join(out))


def fig_yield():
    out = [t(30, 26, "Fraction of oligos that are full length after n couplings", 14, INK)]
    X0, Y0, W, H = 70, 190, 520, 140
    out.append(line(X0, Y0, X0 + W, Y0, INK, 1.2)); out.append(line(X0, Y0, X0, Y0 - H, INK, 1.2))
    for n in (0, 50, 100, 150, 200):
        x = X0 + n / 200 * W
        out.append(line(x, Y0, x, Y0 + 4, INK, 1)); out.append(t(x, Y0 + 18, str(n), 11.5, MUTE, anchor="middle"))
    out.append(t(X0 + W / 2, Y0 + 36, "oligo length (nt)", 12.5, MUTE, anchor="middle"))
    for p in (0, 50, 100):
        y = Y0 - p / 100 * H
        out.append(line(X0 - 4, y, X0, y, INK, 1)); out.append(t(X0 - 8, y + 4, f"{p}%", 11.5, MUTE, anchor="end"))
    for cc, col in ((0.99, BAD), (0.995, OK)):
        pts = " ".join(f"{X0 + n/200*W:.0f},{Y0 - cc ** (n - 1) * H:.0f}" for n in range(1, 201, 4))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2"/>')
        for n in (74,):
            out.append(dot(X0 + n / 200 * W, Y0 - cc ** (n - 1) * H, 4.5, col))
            out.append(t(X0 + n / 200 * W + 8, Y0 - cc ** (n - 1) * H - 6, "%d%%" % round(cc ** (n - 1) * 100), 12, col))
    out.append(t(X0 + W + 8, Y0 - 0.99 ** 199 * H + 4, "99.0% per step", 12, BAD))
    out.append(t(X0 + W + 8, Y0 - 0.995 ** 199 * H + 4, "99.5% per step", 12, OK))
    out.append(t(30, 250, "At 99% coupling only about half of 74-mers are intact; at 200 nt only one in seven.", 14, HOT))
    return svg(780, 268, "".join(out))


def fig_pcr_skew():
    out = []
    rnd = random.Random(7)
    n = 28
    eff = [rnd.uniform(0.82, 0.97) for _ in range(n)]
    before = [10.0] * n
    after = [b * (1 + e) ** 20 for b, e in zip(before, eff)]
    tot = sum(after) / n
    after = [a / tot * 10 for a in after]
    for k, (title, hs, x0) in enumerate((("pool as synthesised", before, 40), ("after 20 cycles of PCR", after, 400))):
        out.append(t(x0, 28, title, 14, HOT, weight="bold"))
        for i, h in enumerate(hs):
            hh = min(h, 38) * 3.4
            out.append(f'<rect x="{x0 + i*11}" y="{170 - hh:.0f}" width="8" height="{hh:.0f}" fill="{BOT}" opacity="0.85"/>')
        out.append(line(x0, 170, x0 + n * 11, 170, INK, 1.2))
        out.append(t(x0 + n * 11 / 2, 188, "28 different guides", 11.5, MUTE, anchor="middle"))
    out.append(t(30, 226, "A 1% difference in efficiency per cycle becomes a ~20% difference after 20 cycles.", 14, INK))
    out.append(t(30, 246, "Amplify the pool as little as you can, and in many small reactions.", 14, HOT))
    return svg(760, 264, "".join(out))


def fig_gibson():
    out = [t(30, 26, "Gibson: a 5' exonuclease exposes homology; the joint is then filled and sealed", 14, INK)]
    ov = "TGGAAAGGACGAAACACC"
    vec = "ACTTGCATCA"
    ins = "GTTTTAGAGC"
    top = vec + ov + ins
    bot = comp(top)
    x = 100
    n = len(vec)
    for i, ch in enumerate(top):
        out.append(t(x + i * DX, 86, ch, 13, TOP if i < n + len(ov) else BOT, family=MONO))
        out.append(t(x + i * DX, 116, bot[i], 13, TOP if i < n else BOT, family=MONO))
    out.append(pairs(x, 86, 116, top, bot))
    out.append(t(x - 10, 86, "vector", 12.5, TOP, anchor="end")); out.append(t(x - 10, 116, "insert", 12.5, BOT, anchor="end"))
    for (c, y0, y1) in ((n + len(ov), 70, 92), (n, 100, 122)):
        out.append(line(x + c * DX - 1.5, y0, x + c * DX - 1.5, y1, BAD, 2.2))
    out.append(t(x + (n + len(ov)) * DX, 62, "nick", 12, BAD, anchor="middle")); out.append(t(x + n * DX, 138, "nick", 12, BAD, anchor="middle"))
    ox = x + n * DX
    out.append(f'<rect x="{ox-2}" y="70" width="{len(ov)*DX+4}" height="56" rx="4" fill="none" stroke="{HOT}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    out.append(t(ox + len(ov) * DX / 2, 156, "18 nt overlap anneals", 12.5, HOT, anchor="middle"))
    out.append(t(30, 196, "T5 exonuclease chews back the 5' ends, leaving 3' overhangs that find each other. Polymerase fills", 13.5, INK))
    out.append(t(30, 216, "any gap and ligase seals the two nicks. No restriction site is needed in the insert.", 13.5, INK))
    return svg(760, 236, "".join(out))


def fig_golden_gate():
    out = [t(30, 26, "Golden Gate (BsmBI): the enzyme cuts outside its own site, so the site leaves with the fragment", 14, INK)]
    top = "CGTCTCACACCGATCGTAGC"
    bot = comp(top)
    x = 60
    s1, w = seq(x, 70, top, TOP); s2, _ = seq(x, 100, bot, BOT)
    out.append(s1); out.append(s2); out.append(pairs(x, 70, 100, top, bot))
    out.append(f'<rect x="{x-3}" y="54" width="{6*DX+6}" height="62" rx="4" fill="none" stroke="{HOT}" stroke-width="1.4"/>')
    out.append(t(x + 3 * DX, 46, "site CGTCTC", 12.5, HOT, anchor="middle"))
    out.append(line(x + 7 * DX - 2, 52, x + 7 * DX - 2, 84, BAD, 2)); out.append(line(x + 11 * DX - 2, 88, x + 11 * DX - 2, 118, BAD, 2))
    out.append(t(x + 7 * DX - 2, 134, "top cut: N1", 12, BAD, anchor="middle")); out.append(t(x + 12 * DX, 134, "bottom cut: N5", 12, BAD))
    # after
    g = 34
    lt, lb = top[:7], bot[:11]
    rt, rb = " " * 7 + top[7:], " " * 11 + bot[11:]
    out.append(t(30, 186, "after cutting", 12.5, MUTE))
    b1, _ = duplex(x, 200, lt + " " * 13, lb + " " * 9, labels=False, topfill=HOT, botfill=HOT)
    out.append(b1)
    b2, _ = duplex(x + g, 200, rt, rb, labels=False)
    out.append(b2)
    out.append(t(x + 4 * DX, 258, "site goes away", 12, HOT, anchor="middle"))
    out.append(t(x + g + 14 * DX, 258, "4-nt overhang CACC, free to pair", 12, OK, anchor="middle"))
    out.append(t(30, 286, "Once the site is gone the product cannot be re-cut, so cut and ligate can run together in one tube.", 14, INK))
    return svg(720, 304, "".join(out))


def fig_guide_cloning():
    out = [t(30, 26, "lentiCRISPR v2: one guide in, the filler out. Overhangs make the order unambiguous.", 14, INK)]
    left, right = "AAGGACGAAA", "GTTTTAGAGC"
    guide = "TCATCGATTGACGTAGCTAC"
    oligo_top = "CACCG" + guide
    top = left + oligo_top + right
    bot = comp(top)
    x = 50
    col = lambda i: TOP if i < 10 or i >= 35 else HOT
    for i, ch in enumerate(top):
        out.append(t(x + i * DX, 80, ch, 13, col(i), family=MONO))
        out.append(t(x + i * DX, 112, bot[i], 13, BOT if (i < 14 or i >= 39) else BAD, family=MONO))
    out.append(pairs(x, 80, 112, top, bot))
    for c, y0, y1 in ((10, 66, 84), (35, 66, 84), (14, 106, 124), (39, 106, 124)):
        out.append(line(x + c * DX - 1.5, y0, x + c * DX - 1.5, y1, BAD, 2.2))
    out.append(t(x, 58, "hU6 end (vector)", 12.5, TOP)); out.append(t(x + 10 * DX, 58, "CACCG + guide (annealed oligo pair)", 12.5, HOT))
    out.append(t(x + 35 * DX, 58, "scaffold (vector)", 12.5, TOP))
    out.append(t(x + 10 * DX, 146, "CACC overhang pairs with the vector's GTGG;", 12.5, MUTE))
    out.append(t(x + 10 * DX, 163, "GTTT of the vector pairs with the oligo's CAAA", 12.5, MUTE))
    out.append(t(30, 204, "Red ticks are the four nicks that T4 DNA ligase seals. Make 120,000 of these separately and it is a", 13.5, INK))
    out.append(t(30, 224, "plate of guides; make them as a pool and Gibson assembly is the practical route.", 13.5, INK))
    return svg(780, 244, "".join(out))


def fig_coverage():
    out = [t(30, 26, "How many guides are missing, for an ideally even pool of 100,000 guides", 14, INK)]
    rows = [(1, math.exp(-1)), (3, math.exp(-3)), (5, math.exp(-5)), (10, math.exp(-10)), (20, math.exp(-20))]
    for i, (c, f) in enumerate(rows):
        y = 52 + i * 34
        out.append(t(30, y + 17, f"{c}x coverage", 13, INK))
        n = f * 100000
        wlen = max(4, (math.log10(max(n, 1)) + 0.3) / 5.3 * 330)
        out.append(f'<rect x="130" y="{y}" width="{wlen:.0f}" height="22" fill="{BAD if c < 5 else OK}" opacity="0.8"/>')
        lab = "%s guides lost" % (f"{n:,.0f}" if n >= 1 else "about 0")
        out.append(t(130 + wlen + 8, y + 16, lab, 12.5, MUTE))
    out.append(t(30, 236, "Length is log10 of the number lost. Real pools are uneven, so aim well above 100x at every step.", 13.5, HOT))
    return svg(720, 254, "".join(out))


def fig_vector_map():
    out = [t(30, 26, "lentiCRISPR v2 transfer vector: everything between the LTRs ends up in the cell's genome", 14, INK)]
    parts = [("5' LTR", 54, "r"), ("psi", 30, "k"), ("RRE", 36, "k"), ("cPPT", 40, "k"), ("U6", 36, "b"), ("guide", 54, "t"),
             ("scaffold", 56, "b"), ("EFS", 36, "b"), ("SpCas9", 80, "g"), ("P2A", 34, "k"), ("puro", 42, "g"), ("WPRE", 46, "k"), ("3' LTR", 54, "r")]
    s1, xe = cons(30, 60, parts, h=34, size=11)
    out.append(s1)
    x = 30 + 54 + 30 + 36 + 40
    out.append(line(x, 110, x + 36 + 54 + 56, 110, TOP, 2)); out.append(t(x, 128, "Pol III: makes the guide RNA", 12.5, TOP))
    x2 = x + 36 + 54 + 56
    out.append(line(x2, 150, x2 + 36 + 80 + 34 + 42, 150, OK, 2)); out.append(t(x2, 168, "Pol II: Cas9 and drug resistance, one message", 12.5, OK))
    out.append(t(30, 200, "Two promoters, one genome: the guide for the screen, the drug marker for selecting transduced cells.", 14, HOT))
    return svg(760, 220, "".join(out))


def fig_packaging():
    out = []
    for i, (l1, l2) in enumerate([("transfer vector", "(guide library)"), ("packaging", "(gag, pol, rev)"), ("envelope", "(VSV-G)")]):
        y = 40 + i * 60
        out.append(f'<circle cx="60" cy="{y+16}" r="22" fill="{BLUE}" stroke="{TOP}" stroke-width="1.4"/>')
        out.append(t(98, y + 12, l1, 12.5, INK)); out.append(t(98, y + 28, l2, 12, MUTE))
        out.append(line(215, y + 16, 270, 100, MUTE, 1.2))
    out.append(box(270, 70, 120, 60, "", TAN, MUTE)); out.append(t(330, 96, "producer cell", 13, INK, anchor="middle")); out.append(t(330, 114, "(HEK293T)", 12, MUTE, anchor="middle"))
    out.append(arrow(394, 100, 450, MUTE, 1.6))
    out.append(f'<circle cx="500" cy="100" r="40" fill="{GREY}" stroke="{MUTE}" stroke-width="1.4"/>')
    for k in range(10):
        a = k / 10 * 6.283
        out.append(dot(500 + 40 * math.cos(a), 100 + 40 * math.sin(a), 3, HOT))
    out.append(f'<path d="M 480 92 q 10 -14 20 0 t 20 0" fill="none" stroke="{TOP}" stroke-width="2"/>')
    out.append(f'<path d="M 480 108 q 10 -14 20 0 t 20 0" fill="none" stroke="{TOP}" stroke-width="2"/>')
    out.append(t(500, 160, "virion: two copies of the", 12.5, MUTE, anchor="middle")); out.append(t(500, 177, "vector RNA only", 12.5, MUTE, anchor="middle"))
    out.append(arrow(548, 100, 600, MUTE, 1.6))
    out.append(box(604, 70, 110, 60, "", TAN, MUTE)); out.append(t(659, 96, "target cell", 13, INK, anchor="middle")); out.append(t(659, 114, "(human)", 12, MUTE, anchor="middle"))
    out.append(t(30, 222, "Genes the virus needs live on other plasmids, so the particle can enter once and never spread.", 14, HOT))
    return svg(740, 240, "".join(out))


def fig_ltr_dup():
    out = [t(30, 26, "Reverse transcription copies the 3' LTR region into both ends", 14, INK)]
    out.append(t(30, 64, "RNA in the virion", 12.5, MUTE))
    r, xe = cons(150, 48, [("R", 32, "k"), ("U5", 40, "k"), ("everything in between", 220, "b"), ("U3 + cassette", 110, "t"), ("R", 32, "k")], h=28)
    out.append(r)
    out.append(arrow(300, 84, 108, MUTE, 0) if False else "")
    out.append(t(310, 102, "reverse transcription", 12.5, MUTE))
    out.append(t(30, 138, "DNA", 12.5, MUTE))
    r1, x1 = cons(150, 128, [("U3 + cassette", 110, "t"), ("R", 32, "k"), ("U5", 40, "k")], h=28)
    r2, x2 = cons(x1 + 190, 128, [("U3 + cassette", 110, "t"), ("R", 32, "k"), ("U5", 40, "k")], h=28)
    out.append(r1); out.append(r2)
    out.append(t(x1 + 8, 146, "...", 14, MUTE)); out.append(line(x1 + 6, 142, x1 + 184, 142, MUTE, 1.2, "3 3"))
    out.append(t(150, 192, "5' LTR", 12.5, MUTE)); out.append(t(x1 + 190, 192, "3' LTR", 12.5, MUTE))
    out.append(t(30, 222, "A cassette placed in the 3' U3 is copied into the 5' LTR as well: the provirus carries it twice.", 14, HOT))
    return svg(740, 240, "".join(o for o in out if o))


def fig_integration():
    out = [t(30, 26, "Integrase joins viral DNA ends to a staggered cut; repair duplicates 5 bp of host sequence", 14, INK)]
    host_top = "ACTGGCAGTTC"
    b, w = duplex(60, 70, host_top, comp(host_top), labels=False)
    out.append(b)
    out.append(f'<rect x="{60+4*DX-2}" y="52" width="{5*DX+4}" height="62" rx="3" fill="none" stroke="{HOT}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    out.append(t(60 + 6.5 * DX, 44, "target", 12, HOT, anchor="middle"))
    out.append(t(30, 158, "after integration", 12.5, MUTE))
    lt = "ACTG"; tsd = "GCAGT"; rt = "TC"
    x = 60
    b1, w1 = duplex(x, 170, lt + tsd, comp(lt + tsd), labels=False)
    out.append(b1)
    px = x + w1 + 4
    out.append(box(px, 160, 220, 46, "provirus  5'-TG ... CA-3'", TAN, HOT, 13, HOT))
    b2, w2 = duplex(px + 224, 170, tsd + rt, comp(tsd + rt), labels=False)
    out.append(b2)
    out.append(t(x + 4 * DX + 2.5 * DX, 232, "GCAGT", 12.5, HOT, anchor="middle")); out.append(t(px + 224 + 2.5 * DX, 232, "GCAGT", 12.5, HOT, anchor="middle"))
    out.append(t(30, 262, "Same 5 bp on both sides of the provirus. Where it lands is not random: HIV-derived vectors prefer genes.", 13.5, INK))
    return svg(760, 280, "".join(out))


def fig_moi():
    out = [t(30, 26, "Cells receiving 0, 1 or 2+ copies, at three multiplicities of infection", 14, INK)]
    for i, m in enumerate((0.1, 0.3, 1.0)):
        p0 = math.exp(-m); p1 = m * p0; p2 = 1 - p0 - p1
        y = 52 + i * 56
        out.append(t(30, y + 18, f"MOI {m:g}", 13, INK))
        x = 110
        for pv, col, lab in ((p0, "#d5d8db", ""), (p1, OK, ""), (p2, BAD, "")):
            wv = pv * 420
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{wv:.1f}" height="26" fill="{col}"/>')
            if pv > 0.07:
                out.append(t(x + wv / 2, y + 18, f"{pv*100:.0f}%", 12, INK if col == "#d5d8db" else "#ffffff", anchor="middle"))
            x += wv
        out.append(t(540, y + 18, "of infected cells, %d%% have 2+" % round(p2 / (1 - p0) * 100), 12.5, MUTE))
    out.append(f'<rect x="110" y="224" width="12" height="12" fill="#d5d8db"/>'); out.append(t(126, 235, "none", 12, MUTE))
    out.append(f'<rect x="170" y="224" width="12" height="12" fill="{OK}"/>'); out.append(t(186, 235, "one", 12, MUTE))
    out.append(f'<rect x="226" y="224" width="12" height="12" fill="{BAD}"/>'); out.append(t(242, 235, "two or more", 12, MUTE))
    out.append(t(30, 262, "Low MOI keeps one guide per cell; the price is that most cells are not transduced at all.", 14, HOT))
    return svg(760, 280, "".join(out))


def fig_payloads():
    out = [t(30, 26, "The same oligo-pool machinery carries different payloads", 14, INK)]
    rows = [("CRISPR guides", [("promoter", 74, "b"), ("guide", 70, "t"), ("scaffold", 70, "b")], "read: guide sequence"),
            ("reporter variants", [("candidate", 80, "t"), ("promoter", 74, "b"), ("reporter", 70, "g"), ("tag", 36, "r")], "read: tag, RNA / DNA"),
            ("protein variants", [("tile with codon changes", 190, "t")], "read: the variant"),
            ("lineage barcodes", [("barcode", 60, "t"), ("target sites", 110, "r")], "read: scars")]
    for i, (name, parts, rd) in enumerate(rows):
        y = 48 + i * 42
        out.append(t(30, y + 19, name, 13, INK))
        s_, _ = cons(190, y, parts, h=28)
        out.append(s_)
        out.append(t(520, y + 19, rd, 12.5, MUTE))
    out.append(t(30, 236, "Each payload changes the readout, not the way the pool is made and delivered.", 14, HOT))
    return svg(720, 256, "".join(out))


def fig_v1_v2():
    out = [t(30, 26, "Vector geometry decides the readout: cPPT moves between lentiCRISPR v1 and v2", 14, INK)]
    out.append(t(30, 72, "v1", 14, HOT, weight="bold"))
    s1, _ = cons(70, 54, [("LTR", 40, "r"), ("RRE", 36, "k"), ("U6", 36, "b"), ("guide", 50, "t"), ("scaffold", 56, "b"), ("cPPT", 46, "k"), ("EFS", 36, "b"), ("Cas9", 70, "g"), ("puro", 44, "g"), ("LTR", 40, "r")], h=30, size=11)
    out.append(s1)
    out.append(t(30, 132, "v2", 14, HOT, weight="bold"))
    s2, _ = cons(70, 114, [("LTR", 40, "r"), ("RRE", 36, "k"), ("cPPT", 46, "k"), ("U6", 36, "b"), ("guide", 50, "t"), ("scaffold", 56, "b"), ("EFS", 36, "b"), ("Cas9", 70, "g"), ("puro", 44, "g"), ("LTR", 40, "r")], h=30, size=11)
    out.append(s2)
    out.append(t(30, 186, "A primer pair that spans the cassette gives a short product in one version and a long one in the other.", 13.5, INK))
    out.append(t(30, 206, "Choose readout primers from the real map of the vector you used.", 13.5, HOT))
    return svg(760, 224, "".join(out))


def fig_one_end():
    out = [t(30, 26, "After integration the cassette is known, and everything next to it is not", 14, INK)]
    out.append(line(30, 90, 130, 90, MUTE, 3)); out.append(line(410, 90, 510, 90, MUTE, 3))
    out.append(box(130, 74, 280, 32, "provirus: LTR to LTR, sequence known", TAN, HOT, 13, HOT))
    out.append(t(80, 76, "host DNA", 12.5, MUTE, anchor="middle")); out.append(t(80, 120, "unknown", 12.5, BAD, anchor="middle"))
    out.append(t(460, 76, "host DNA", 12.5, MUTE, anchor="middle")); out.append(t(460, 120, "unknown", 12.5, BAD, anchor="middle"))
    out.append(arrow(150, 142, 80, HOT, 2)); out.append(t(158, 146, "primer in the LTR", 12.5, HOT))
    out.append(t(60, 150, "?", 22, BAD)); out.append(t(220, 176, "no second primer site", 12.5, BAD))
    out.append(t(30, 214, "PCR needs two primer sites. Here there is one, and the job is to get a second one.", 14, INK))
    return svg(640, 232, "".join(out))


# ================================================================ lec-readout.qmd

def fig_needle():
    out = [t(30, 26, "What is in the tube: ~15 million guide copies diluted in 100 micrograms of genome", 14, INK)]
    out.append(box(40, 50, 600, 30, "", GREY, MUTE))
    out.append(t(340, 70, "one diploid human genome: ~6.4 Gb, ~6.6 pg", 13, MUTE, anchor="middle"))
    out.append(f'<rect x="410" y="50" width="4" height="30" fill="{HOT}"/>')
    out.append(line(412, 80, 470, 120, HOT, 1.2)); out.append(t(476, 126, "one integrated guide cassette", 12.5, HOT))
    rows = ["100 ug of DNA = 100e-6 / 6.6e-12 = ~1.5 x 10^7 genomes",
            "a pool of 70,000 guides then has ~200 cells per guide",
            "the guide region is ~100 bp of 6.4 Gb, about 1 part in 10^7, so PCR must pick it out"]
    for i, r in enumerate(rows):
        out.append(t(40, 156 + i * 22, r, 13.5, INK))
    out.append(t(30, 236, "Readout is a purification problem as much as a counting problem.", 14, HOT))
    return svg(720, 254, "".join(out))


def fig_two_strategies():
    out = []
    out.append(t(30, 28, "Both flanks known: a guide cassette", 14, HOT, weight="bold"))
    out.append(line(40, 80, 600, 80, MUTE, 3))
    s1, _ = cons(160, 64, [("U6 side", 90, "b"), ("guide", 80, "t"), ("scaffold", 90, "b")], h=32)
    out.append(s1)
    out.append(arrow(165, 54, 235, TOP, 1.8))
    out.append(arrow(420, 112, 350, BAD, 1.8))
    out.append(t(440, 118, "two primers, one PCR", 12.5, MUTE))
    out.append(t(30, 154, "One flank known: an integration site", 14, HOT, weight="bold"))
    out.append(line(40, 200, 600, 200, MUTE, 3))
    out.append(box(240, 184, 140, 32, "known LTR", TAN, HOT, 12.5, HOT))
    out.append(t(80, 190, "?", 20, BAD)); out.append(t(520, 190, "?", 20, BAD))
    out.append(t(30, 250, "The first needs ordinary PCR design. The second needs a trick to give the unknown side a primer site.", 14, INK))
    return svg(740, 268, "".join(o for o in out if o))


def fig_joung():
    out = [t(30, 26, "Joung one-PCR readout: the integrated cassette becomes a sequencer-ready molecule in one reaction", 14, INK)]
    s1, xe = cons(40, 56, [("P5", 40, "b"), ("stagger", 70, "k"), ("U6 site", 90, "b"), ("guide", 80, "t"), ("scaffold site", 100, "b"), ("index", 60, "g"), ("P7", 40, "b")], h=32, size=12)
    out.append(s1)
    out.append(arrow(40 + 40 + 70, 108, 40 + 40 + 70 + 90 + 80 + 30, TOP, 2)); out.append(t(190, 128, "Read 1: 80 cycles, runs through the U6 site into the guide", 12.5, TOP))
    out.append(t(40, 156, "Forward primers: P5 + staggered spacer + U6 binding. Reverse primers: P7 + index + scaffold binding.", 13, INK))
    out.append(t(40, 176, "Both primers are long, so one PCR (about 12 cycles after a first denaturation) makes the finished library.", 13, INK))
    out.append(t(30, 214, "Binding sites sit on the vector's constant parts, so the same primers fit any guide.", 14, HOT))
    return svg(760, 232, "".join(out))


def fig_stagger():
    out = [t(30, 26, "Staggered forward primers: every read starts at a different place in the constant sequence", 14, INK)]
    const = "TTGTGGAAAGGACGAAACACCG"
    pads = ["", "A", "CT", "GAT", "TCAG"]
    x0 = 70
    for i, p in enumerate(pads):
        y = 66 + i * 24
        out.append(t(30, y, "P%d" % (i + 1), 11.5, MUTE))
        out.append(t(x0, y, p, 13, BAD, family=MONO))
        out.append(t(x0 + len(p) * DX, y, const, 13, TOP, family=MONO))
    for c in (0, 4):
        out.append(f'<rect x="{x0 + c*DX - 1.5}" y="48" width="{DX+1}" height="124" fill="none" stroke="{HOT}" stroke-width="1.3"/>')
    out.append(t(x0 + 0.5 * DX, 190, "cycle 1", 12, HOT, anchor="middle")); out.append(t(x0 + 4.5 * DX, 190, "cycle 5", 12, HOT, anchor="middle"))
    out.append(t(420, 82, "Without stagger, every cluster would show", 12.5, MUTE)); out.append(t(420, 99, "the same base in each early cycle,", 12.5, MUTE))
    out.append(t(420, 116, "and the instrument loses its calibration.", 12.5, MUTE))
    out.append(t(30, 226, "Pooling the five primers makes the first cycles look like random sequence.", 14, HOT))
    return svg(760, 244, "".join(out))


def fig_two_step():
    out = []
    out.append(t(30, 26, "Moffat two-step readout: enrich first, index second", 14, INK))
    out.append(t(30, 66, "PCR 1", 13.5, HOT, weight="bold"))
    out.append(line(110, 62, 600, 62, MUTE, 3))
    s1, _ = cons(240, 46, [("U6 side", 70, "b"), ("guide", 60, "t"), ("scaffold side", 100, "b")], h=30)
    out.append(s1)
    out.append(arrow(250, 38, 310, TOP, 1.8)); out.append(arrow(420, 90, 360, BAD, 1.8))
    out.append(lines3(110, 116, ["gDNA, 3.5 ug per 50 uL reaction, many reactions, 25 cycles.", "Locus-specific primers only. Product ~600 bp."], 12.5, MUTE))
    out.append(t(30, 176, "PCR 2", 13.5, HOT, weight="bold"))
    s2, _ = cons(110, 160, [("P5 + i5", 80, "g"), ("guide region", 130, "t"), ("i7 + P7", 80, "g")], h=30)
    out.append(s2)
    out.append(lines3(110, 212, ["A little PCR 1 product, 10 cycles, nested primers that carry the full indexed arms.", "Product ~200 bp, cut from a gel."], 12.5, MUTE))
    return svg(720, 250, "".join(out))


def fig_dark_cycles():
    out = [t(30, 26, "Dark cycles: skip the constant stretch without imaging it", 14, INK)]
    s1, _ = cons(40, 50, [("P5 + i5", 60, "g"), ("constant 21 nt", 126, "k"), ("guide region", 156, "t"), ("i7 + P7", 60, "g")], h=30)
    out.append(s1)
    out.append(line(100, 104, 226, 104, MUTE, 3, "4 3")); out.append(t(163, 124, "21 dark cycles", 12.5, MUTE, anchor="middle"))
    out.append(arrow(226, 104, 382, TOP, 2.2)); out.append(t(304, 124, "26 read cycles", 12.5, TOP, anchor="middle"))
    out.append(t(40, 156, "Run: 21 dark + 26 read, then 8 cycles each for the two indexes.", 13, INK))
    out.append(t(40, 176, "The constant stretch is the same in every cluster; reading it adds nothing but cost and noise.", 13, INK))
    out.append(t(30, 210, "The read starts exactly where the information starts.", 14, HOT))
    return svg(640, 228, "".join(out))


def fig_pcr_bias():
    out = []
    rnd = random.Random(3)
    gcs = [0.35, 0.42, 0.5, 0.58, 0.65, 0.72]
    eff = [1.0 - 0.9 * (g - 0.35) / 0.4 * 0.45 for g in gcs]
    for k, (title, mode) in enumerate((("cells in the screen", "eq"), ("reads after PCR", "pcr"), ("molecules counted (MIP/UMI)", "eq"))):
        x0 = 40 + k * 240
        out.append(t(x0, 28, title, 13.5, HOT, weight="bold"))
        for i, g in enumerate(gcs):
            h = [100, 88, 76, 64, 54, 45][i] if mode == "pcr" else 100
            out.append(f'<rect x="{x0 + i*30}" y="{170 - h * 0.9:.0f}" width="22" height="{h*0.9:.0f}" fill="{PAL[i % 8]}" opacity="0.85"/>')
        out.append(line(x0, 170, x0 + 180, 170, INK, 1.2))
        out.append(t(x0, 188, "GC content: low", 11.5, MUTE)); out.append(t(x0 + 180, 188, "high", 11.5, MUTE, anchor="end"))
    out.append(t(30, 226, "Six guides in equal numbers: high-GC amplicons amplify less, so counts reflect chemistry too.", 13.5, INK))
    out.append(t(30, 246, "Counting the molecules, not their PCR copies, removes that term.", 14, HOT))
    return svg(760, 264, "".join(out))


def fig_mip():
    out = []
    cols = [("1  Hybridise", ["both arms bind", "with a gap between"]),
            ("2  Fill and ligate", ["polymerase copies the gap,", "ligase closes a circle"]),
            ("3  Exonuclease", ["linear DNA is destroyed,", "circles survive"]),
            ("4  Universal PCR", ["primers on the backbone", "copy tag + target"])]
    for i, (h, ls) in enumerate(cols):
        x = 30 + i * 180
        out.append(t(x, 26, h, 13.5, HOT, weight="bold"))
        cy = 84
        if i == 0:
            out.append(line(x, cy + 16, x + 150, cy + 16, MUTE, 3))
            out.append(line(x + 10, cy + 4, x + 55, cy + 4, TOP, 3)); out.append(line(x + 95, cy + 4, x + 140, cy + 4, HOT, 3))
            out.append(f'<path d="M {x+10} {cy+4} C {x} {cy-40}, {x+150} {cy-40}, {x+140} {cy+4}" fill="none" stroke="{BOT}" stroke-width="2"/>')
        elif i == 1:
            out.append(f'<circle cx="{x+70}" cy="{cy}" r="32" fill="none" stroke="{TOP}" stroke-width="3"/>')
            out.append(f'<path d="M {x+38} {cy} A 32 32 0 0 1 {x+70} {cy-32}" fill="none" stroke="{OK}" stroke-width="3"/>')
            out.append(dot(x + 70, cy + 32, 4, HOT))
        elif i == 2:
            out.append(f'<circle cx="{x+40}" cy="{cy}" r="24" fill="none" stroke="{TOP}" stroke-width="3"/>')
            out.append(line(x + 90, cy - 20, x + 140, cy - 20, MUTE, 2, "3 3")); out.append(line(x + 90, cy + 20, x + 140, cy + 20, MUTE, 2, "3 3"))
            out.append(t(x + 115, cy + 5, "x", 18, BAD, anchor="middle"))
        else:
            out.append(f'<circle cx="{x+70}" cy="{cy}" r="32" fill="none" stroke="{TOP}" stroke-width="3"/>')
            out.append(arrow(x + 40, cy - 40, x + 100, OK, 1.8)); out.append(arrow(x + 100, cy + 40, x + 40, BAD, 1.8))
        out.append(lines3(x, 150, ls, 12.5, MUTE))
    out.append(t(30, 212, "Each probe carries a random 12-nt tag, so every captured molecule gets its own label before any amplification.", 13.5, INK))
    out.append(t(30, 232, "Counting tags counts molecules, whatever the PCR did afterwards.", 14, HOT))
    return svg(780, 250, "".join(out))


def fig_umi():
    out = [t(30, 26, "UMIs: count the original molecules, not the copies", 14, INK)]
    cols = [OK, HOT, BAD]
    for i, c in enumerate(cols):
        out.append(box(40, 50 + i * 36, 70, 26, "tag %d" % (i + 1), "none", c, 12, c))
    out.append(arrow(116, 100, 200, MUTE, 1.6)); out.append(t(158, 92, "PCR", 12.5, MUTE, anchor="middle"))
    copies = [4, 1, 5]
    k = 0
    for i, c in enumerate(cols):
        for j in range(copies[i]):
            out.append(f'<rect x="{210 + k*22}" y="64" width="16" height="44" fill="{c}" opacity="0.8"/>')
            k += 1
    out.append(t(210, 128, "10 reads", 12.5, MUTE))
    out.append(arrow(210 + 10 * 22 + 6, 86, 210 + 10 * 22 + 70, MUTE, 1.6)); out.append(t(210 + 10 * 22 + 38, 78, "collapse", 12.5, MUTE, anchor="middle"))
    for i, c in enumerate(cols):
        out.append(f'<rect x="{500 + i*22 + 60}" y="64" width="16" height="44" fill="{c}" opacity="0.8"/>')
    out.append(t(560, 128, "3 molecules", 12.5, MUTE))
    out.append(t(30, 178, "Read counts say 4 : 1 : 5. The truth is 1 : 1 : 1; the extra reads were copies.", 13.5, INK))
    out.append(t(30, 200, "Needs a tag that is random, long enough to be unique among the molecules, and read.", 13.5, INK))
    out.append(t(30, 232, "Kivioja et al. 2012: the tag makes counting absolute, within the limits of the tag space.", 13.5, HOT))
    return svg(720, 250, "".join(o for o in out if o))


def fig_cropseq():
    out = [t(30, 26, "CROP-seq: put the guide where a polyadenylated transcript will carry it", 14, INK)]
    s1, x1 = cons(40, 44, [("5' LTR", 54, "r"), ("...", 40, "k"), ("U6 + guide", 90, "t"), ("EFS", 40, "b"), ("puro", 50, "g"), ("3' LTR + U6 + guide", 130, "r")], h=30, size=11)
    out.append(s1)
    out.append(line(184, 92, 460, 92, OK, 2)); out.append(t(190, 108, "Pol II transcript: puro mRNA with the guide in its 3' UTR, then poly(A)", 12.5, OK))
    out.append(t(40, 150, "capture:", 12.5, MUTE))
    out.append(box(110, 134, 190, 24, "bead oligo-dT + cell barcode", BLUE, TOP, 11.5, TOP))
    out.append(t(310, 151, "reads the 3' end of the same message that carries the guide", 12.5, MUTE))
    out.append(t(30, 196, "One cell gives its whole transcriptome and the identity of its guide from an ordinary 3' library.", 14, HOT))
    out.append(t(30, 216, "A short enrichment PCR makes sure the guide, a rare part of the message, is seen.", 13.5, INK))
    return svg(720, 234, "".join(o for o in out if o))


def fig_perturbseq():
    out = []
    out.append(t(30, 26, "Barcode proxy (Perturb-seq 2016)", 14, HOT, weight="bold"))
    s1, _ = cons(40, 40, [("U6 guide", 70, "t"), ("...", 24, "k"), ("EF1a puro BFP", 120, "g"), ("barcode", 56, "r"), ("polyA", 46, "k")], h=28, size=11)
    out.append(s1)
    out.append(t(40, 96, "A separate table pairs each guide with its barcode (dictionary).", 12.5, MUTE))
    out.append(t(30, 136, "Direct capture (2020)", 14, HOT, weight="bold"))
    out.append(line(40, 170, 330, 170, BAD, 2.4)); out.append(t(335, 174, "guide RNA, no poly(A)", 12.5, MUTE))
    out.append(arrow(240, 156, 170, OK, 2)); out.append(t(175, 148, "primer in the constant part", 12.5, OK))
    out.append(t(40, 200, "Reverse transcriptase copies it, template switching adds the cell barcode and UMI.", 12.5, MUTE))
    out.append(t(30, 232, "The proxy is read from a poly(A) transcript, but depends on a table; direct capture reads the guide itself.", 13.5, INK))
    return svg(760, 250, "".join(out))


def fig_inverse_pcr():
    out = []
    cols = [("1  Cut", ["restriction enzyme cuts", "in the flank and inside"]),
            ("2  Self-ligate", ["dilute, so ends join", "within one fragment"]),
            ("3  Outward primers", ["read from the known part", "into the unknown flank"])]
    for i, (h, ls) in enumerate(cols):
        x = 30 + i * 250
        out.append(t(x, 26, h, 13.5, HOT, weight="bold"))
        if i == 0:
            out.append(line(x, 80, x + 200, 80, MUTE, 3))
            out.append(box(x + 70, 66, 70, 28, "known", TAN, HOT, 12, HOT))
            for c in (x + 30, x + 175):
                out.append(line(c, 56, c, 104, BAD, 2))
            out.append(t(x + 30, 50, "site", 11.5, BAD, anchor="middle")); out.append(t(x + 175, 50, "site", 11.5, BAD, anchor="middle"))
        elif i == 1:
            out.append(f'<circle cx="{x+100}" cy="82" r="38" fill="none" stroke="{MUTE}" stroke-width="3"/>')
            out.append(f'<path d="M {x+68} 64 A 38 38 0 0 1 {x+132} 64" fill="none" stroke="{HOT}" stroke-width="5"/>')
            out.append(t(x + 100, 80, "known", 11.5, HOT, anchor="middle"))
            out.append(t(x + 100, 100, "unknown flank", 11.5, MUTE, anchor="middle"))
        else:
            out.append(f'<circle cx="{x+100}" cy="82" r="38" fill="none" stroke="{MUTE}" stroke-width="3"/>')
            out.append(f'<path d="M {x+68} 64 A 38 38 0 0 1 {x+132} 64" fill="none" stroke="{HOT}" stroke-width="5"/>')
            out.append(arrow(x + 84, 44, x + 56, TOP, 1.8)); out.append(arrow(x + 116, 44, x + 144, BAD, 1.8))
            out.append(t(x + 100, 140, "product spans the junction", 11.5, MUTE, anchor="middle"))
        out.append(lines3(x, 176, ls, 12.5, MUTE))
    out.append(t(30, 232, "Circularising turns the unknown flank into the sequence between two known ends.", 14, HOT))
    return svg(780, 250, "".join(o for o in out if o))


def fig_splinkerette():
    out = [t(30, 26, "Splinkerette: an adapter with a hairpin, so only copied molecules can be amplified", 14, INK)]
    out.append(t(30, 60, "1  Ligate", 13, HOT, weight="bold"))
    out.append(line(40, 88, 200, 88, MUTE, 3)); out.append(box(150, 74, 50, 28, "known", TAN, HOT, 11.5, HOT))
    out.append(t(30, 118, "genomic cut end + adapter with a loop", 12, MUTE))
    out.append(t(280, 60, "2  Extend from the LTR primer", 13, HOT, weight="bold"))
    out.append(line(290, 88, 450, 88, MUTE, 3)); out.append(arrow(430, 74, 300, HOT, 1.8))
    out.append(t(290, 118, "copy runs through the flank and the adapter", 12, MUTE))
    out.append(t(530, 60, "3  PCR", 13, HOT, weight="bold"))
    out.append(arrow(540, 88, 640, TOP, 1.8)); out.append(arrow(660, 106, 560, BAD, 1.8))
    out.append(t(530, 126, "adapter primer can bind", 12, MUTE)); out.append(t(530, 143, "only the new copy", 12, MUTE))
    out.append(t(30, 186, "The original adapter strand is held in a hairpin, so primer cannot bind it: no copy of the LTR, no product.", 13.5, INK))
    out.append(t(30, 206, "Without that rule, genomic ends joined to adapters would amplify and swamp the one junction wanted.", 13.5, INK))
    return svg(740, 228, "".join(o for o in out if o))


def fig_guideseq():
    out = [t(30, 26, "GUIDE-seq: a double-stranded tag pins the breaks that Cas9 makes", 14, INK)]
    out.append(line(40, 70, 240, 70, MUTE, 3)); out.append(box(240, 56, 50, 28, "tag", TAN, HOT, 12.5, HOT)); out.append(line(290, 70, 520, 70, MUTE, 3))
    out.append(t(40, 52, "break in genome", 12, MUTE)); out.append(t(265, 100, "tag inserted at break", 12, HOT, anchor="middle"))
    out.append(t(30, 134, "Shear, ligate adapter with UMI, nested PCR from the tag and adapter", 13, INK))
    out.append(line(60, 174, 330, 174, MUTE, 3)); out.append(box(290, 160, 40, 28, "tag", TAN, HOT, 12, HOT))
    out.append(arrow(310, 152, 360, TOP, 1.8))
    out.append(t(60, 212, "known tag on one side; unknown genome next to it; adapter from the shear on the other", 12.5, MUTE))
    out.append(t(30, 242, "Every read that contains the tag next to genome names a break. A one-end-known problem again.", 14, HOT))
    return svg(760, 260, "".join(o for o in out if o))


def fig_mpra():
    out = [t(30, 26, "MPRA: link each candidate sequence to a tag the cell will transcribe", 14, INK)]
    s1, _ = cons(40, 46, [("candidate", 90, "t"), ("minimal promoter", 110, "b"), ("reporter ORF", 100, "g"), ("tag", 44, "r"), ("polyA", 50, "k")], h=30, size=11.5)
    out.append(s1)
    out.append(t(40, 106, "DNA from the pool: how many plasmids carry each tag", 12.5, MUTE))
    out.append(t(40, 124, "RNA from the cells: how many transcripts carry each tag", 12.5, MUTE))
    for i, (d, rr) in enumerate([(40, 66), (40, 28), (40, 34)]):
        x = 60 + i * 120
        out.append(f'<rect x="{x}" y="{200 - d}" width="26" height="{d}" fill="{BOT}" opacity="0.8"/>')
        out.append(f'<rect x="{x + 30}" y="{200 - rr:.0f}" width="26" height="{rr:.0f}" fill="{HOT}" opacity="0.8"/>')
    out.append(line(50, 200, 420, 200, INK, 1.2))
    out.append(t(70, 220, "tag A", 12, MUTE)); out.append(t(190, 220, "tag B", 12, MUTE)); out.append(t(310, 220, "tag C", 12, MUTE))
    out.append(t(440, 150, "blue: DNA copies", 12, BOT)); out.append(t(440, 168, "red: RNA copies", 12, HOT))
    out.append(t(440, 190, "activity = RNA / DNA", 12.5, INK))
    out.append(t(30, 250, "Many tags per candidate average out the effect of where in the vector and the plasmid each tag landed.", 13.5, HOT))
    return svg(780, 268, "".join(out))


def fig_starr():
    out = [t(30, 26, "STARR-seq: the candidate sits in the 3' UTR and writes itself into the RNA", 14, INK)]
    s1, _ = cons(40, 56, [("core promoter", 100, "b"), ("reporter ORF", 110, "g"), ("candidate fragment", 150, "t"), ("polyA", 56, "k")], h=30, size=11.5)
    out.append(s1)
    out.append(f'<path d="M 255 54 C 255 10, 100 10, 100 54" fill="none" stroke="{HOT}" stroke-width="1.8"/>')
    out.append(line(60, 120, 400, 120, OK, 2.2)); out.append(t(60, 140, "transcript: reporter ORF, then the candidate itself, then poly(A)", 12.5, OK))
    out.append(t(40, 176, "No tag is needed: sequencing the RNA reads the fragment, and its abundance is the activity.", 13, INK))
    out.append(t(30, 214, "The price: fragments must be cloned intact, and long ones amplify unevenly.", 13.5, HOT))
    return svg(760, 232, "".join(o for o in out if o))


def fig_dms():
    out = [t(30, 26, "Deep mutational scanning: every single-codon change in a stretch of one protein", 14, INK)]
    out.append(t(40, 56, "wild type", 12.5, MUTE)); out.append(t(120, 56, "GAT  AAA  CGG  TTC", 13, INK, family=MONO))
    for i, v in enumerate(["GAT  AAA  CGG  TTC", "NNK  AAA  CGG  TTC", "GAT  NNK  CGG  TTC", "GAT  AAA  NNK  TTC"][:1]):
        pass
    out.append(t(40, 80, "library", 12.5, MUTE))
    for i, (s_, c) in enumerate([("NNK AAA CGG TTC", HOT), ("GAT NNK CGG TTC", HOT), ("GAT AAA NNK TTC", HOT), ("GAT AAA CGG NNK", HOT)]):
        out.append(t(120, 80 + i * 18, s_, 13, c, family=MONO))
    out.append(t(330, 80, "NNK: any base, any base, G or T", 12, MUTE)); out.append(t(330, 98, "= 32 codons, all 20 amino acids,", 12, MUTE)); out.append(t(330, 116, "one stop, fewer unwanted stops", 12, MUTE))
    out.append(t(40, 170, "select, then sequence before and after:", 12.5, MUTE))
    for i, (b, a) in enumerate([(50, 50), (50, 15), (50, 80), (50, 48)]):
        x = 300 + i * 70
        out.append(f'<rect x="{x}" y="{200-b*0.7:.0f}" width="22" height="{b*0.7:.0f}" fill="{BOT}" opacity="0.8"/><rect x="{x+24}" y="{200-a*0.7:.0f}" width="22" height="{a*0.7:.0f}" fill="{HOT}" opacity="0.8"/>')
    out.append(line(290, 200, 580, 200, INK, 1.2))
    out.append(t(30, 226, "Tiles that fit inside one read are read directly. Longer ones", 13, INK)); out.append(t(30, 244, "need a barcode linked to the variant, read once by long reads.", 13, INK))
    return svg(760, 262, "".join(o for o in out if o))


def fig_lineage():
    out = [t(30, 26, "Lineage recording: a barcode array that accumulates edits as cells divide", 14, INK)]
    def arr(x, y, marks):
        s_ = []
        for i in range(4):
            col = BAD if i in marks else OK
            s_.append(f'<rect x="{x + i*18}" y="{y}" width="14" height="14" fill="{col}" opacity="0.85"/>')
        return "".join(s_)
    out.append(arr(40, 90, []))
    out.append(line(112, 98, 170, 60, MUTE, 1.4)); out.append(line(112, 98, 170, 138, MUTE, 1.4))
    out.append(arr(176, 52, [0])); out.append(arr(176, 130, [3]))
    for (yy, base, ms) in ((52, 52, [[0, 1], [0, 2]]), (130, 130, [[3, 1], [3, 2]])):
        out.append(line(252, yy + 8, 310, yy - 12, MUTE, 1.4)); out.append(line(252, yy + 8, 310, yy + 28, MUTE, 1.4))
        out.append(arr(316, yy - 22, ms[0])); out.append(arr(316, yy + 20, ms[1]))
    out.append(t(412, 78, "green: unedited target", 12, OK)); out.append(t(412, 96, "red: scar from an edit", 12, BAD))
    out.append(t(412, 120, "Cells with the same scars share an ancestor.", 12.5, INK))
    out.append(t(30, 218, "Readout: amplify the array and read the scars; the library has to survive recombination during PCR.", 13.5, HOT))
    return svg(760, 236, "".join(out))


build(__file__, [
    ("pipeline", fig_pipeline),
    ("oligo-arch", fig_oligo_arch),
    ("array-synthesis", fig_array_synthesis),
    ("yield", fig_yield),
    ("pcr-skew", fig_pcr_skew),
    ("gibson", fig_gibson),
    ("golden-gate", fig_golden_gate),
    ("guide-cloning", fig_guide_cloning),
    ("coverage", fig_coverage),
    ("vector-map", fig_vector_map),
    ("packaging", fig_packaging),
    ("ltr-duplication", fig_ltr_dup),
    ("integration", fig_integration),
    ("moi", fig_moi),
    ("payloads", fig_payloads),
    ("v1-v2", fig_v1_v2),
    ("one-end-known", fig_one_end),
    ("needle", fig_needle),
    ("two-strategies", fig_two_strategies),
    ("joung", fig_joung),
    ("stagger", fig_stagger),
    ("two-step", fig_two_step),
    ("dark-cycles", fig_dark_cycles),
    ("pcr-bias", fig_pcr_bias),
    ("mip", fig_mip),
    ("umi", fig_umi),
    ("cropseq", fig_cropseq),
    ("perturbseq", fig_perturbseq),
    ("inverse-pcr", fig_inverse_pcr),
    ("splinkerette", fig_splinkerette),
    ("guideseq", fig_guideseq),
    ("mpra", fig_mpra),
    ("starr", fig_starr),
    ("dms", fig_dms),
    ("lineage", fig_lineage),
])
