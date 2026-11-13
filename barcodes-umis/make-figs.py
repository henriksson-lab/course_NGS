#!/usr/bin/env python3
"""Figures for the barcodes-umis unit.  Run: python3 barcodes-umis/make-figs.py

Every distance, count and probability drawn here is computed, not typed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

PALE = "#fbfbf9"
BLUEF = "#e8eef5"
REDF = "#f5eae6"
GREENF = "#eaf2ec"
GREYF = "#dfe3e6"
BASEC = {"A": OK, "C": TOP, "G": HOT, "T": BOT}
# two-colour chemistry: C red, T green, A both, G neither
CHAN = {"A": "#d9a21b", "C": "#c8503f", "T": "#4f9a58", "G": "#4a4f55"}


def hamming(a, b):
    assert len(a) == len(b)
    return sum(x != y for x, y in zip(a, b))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def min_dist(s):
    return min(hamming(a, b) for i, a in enumerate(s) for b in s[i + 1:])


def cross(x, y, c=BAD, s=6):
    return line(x - s, y - s, x + s, y + s, c, 2) + line(x - s, y + s, x + s, y - s, c, 2)


def bead(x, y, r=20, label=""):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GREYF}" stroke="{MUTE}" stroke-width="1.2"/>'
    if label:
        s += t(x, y + 4, label, 11, MUTE, anchor="middle")
    return s


SET4 = ["AATCCG", "TCATTG", "TCAAGA", "GACATC"]
OLD4 = ["ATCACG", "CGATGT", "TTAGGC", "TGACCA"]
BAD4 = ["GATCAC", "GCTAGT", "GTCAGA", "GACTGG"]
assert min_dist(SET4) == 3, min_dist(SET4)
assert min_dist(OLD4) == 4 and min_dist(BAD4) == 3


def channels(bs, pos):
    red = any(b[pos] in "AC" for b in bs)
    green = any(b[pos] in "AT" for b in bs)
    return red, green


# ------------------------------------------------------------------ 1 information budget

def fig_info():
    out = [t(40, 26, "A read carries four kinds of information. Each has its own address in the molecule.", 14, INK)]
    parts = [("P5", 40, BLUEF, TOP), ("i5", 50, "#eaf2ec", OK), ("cell BC", 78, "#f7ede6", HOT),
             ("UMI", 60, "#f5eae6", BAD), ("insert", 230, PALE, MUTE), ("i7", 50, "#eaf2ec", OK), ("P7", 40, REDF, BAD)]
    x = 40
    pos = {}
    for lab, w, f, c in parts:
        out.append(box(x, 70, w, 34, lab, f, c, 12, c if c != MUTE else INK))
        pos[lab] = x + w / 2
        x += w
    rows = [("which sample", ["i5", "i7"], OK, "sample index"),
            ("which cell", ["cell BC"], HOT, "cell barcode"),
            ("which molecule", ["UMI"], BAD, "UMI"),
            ("which sequence", ["insert"], INK, "the insert itself")]
    for i, (q, ps, c, nm) in enumerate(rows):
        y = 140 + i * 24
        out.append(t(40, y, q, 13, c))
        out.append(t(180, y, "= " + nm, 13, MUTE))
        for p in ps:
            out.append(line(pos[p], 106, pos[p], 124 + i * 0, c, 1.2, dash="2 3"))
    out.append(t(40, 252, "Protocols differ in which of these they need, and in which read each one is "
                          "placed; that choice is the read structure.", 14, INK))
    return svg(720, 272, "".join(out))


# ------------------------------------------------------------------ 2 demultiplexing table

def fig_demux():
    out = [t(40, 26, "Demultiplexing is a distance calculation, one read at a time.", 14, INK)]
    obs = "AATGCG"
    out.append(t(40, 62, "observed index read", 12.5, MUTE))
    s, _ = seq(240, 62, obs, INK, 15)
    out.append(s)
    out.append(t(240 + 6 * DX * 1.15 + 20, 62, "(one base differs from sample 1)", 12, MUTE))
    out.append(t(40, 96, "sample barcodes", 12.5, MUTE))
    out.append(t(330, 96, "mismatches vs read", 12.5, MUTE))
    best = min(range(4), key=lambda i: hamming(SET4[i], obs))
    for i, b in enumerate(SET4):
        y = 124 + i * 28
        out.append(t(40, y, f"sample {i+1}", 13, INK))
        for j, ch in enumerate(b):
            c = BAD if ch != obs[j] else TOP
            out.append(t(240 + j * DX * 1.15, y, ch, 15, c, family=MONO))
        d = hamming(b, obs)
        out.append(t(350, y, str(d), 14, OK if i == best else MUTE, anchor="start"))
        if i == best:
            out.append(t(380, y, "closest: assign here", 12.5, OK))
    d2 = sorted(hamming(b, obs) for b in SET4)
    out.append(t(40, 252, f"The next-closest barcode is {d2[1]} away, so the call is safe. "
                          f"This set has minimum distance {min_dist(SET4)}.", 14, INK))
    return svg(640, 272, "".join(out))


# ------------------------------------------------------------------ 3 distance ladder

def fig_ladder():
    out = [t(40, 26, "Minimum distance between barcodes decides what an error does.", 14, INK)]
    cases = [(1, "distance 1", "one error turns A into B,\nsilently: wrong sample", BAD),
             (2, "distance 2", "one error is noticed but sits\nhalfway: detect, cannot correct", HOT),
             (3, "distance 3", "one error is still closer to A:\ncorrect it", OK)]
    for k, (d, ttl, desc, c) in enumerate(cases):
        y = 66 + k * 64
        out.append(t(40, y + 4, ttl, 13, c))
        x0 = 150
        step = 70
        nodes = d + 1
        for i in range(nodes):
            x = x0 + i * step
            if i > 0:
                out.append(line(x - step + 8, y, x - 8, y, MUTE, 1.4))
            if i in (0, nodes - 1):
                out.append(dot(x, y, 8, TOP if i == 0 else BAD))
                out.append(t(x, y - 14, "A" if i == 0 else "B", 12, TOP if i == 0 else BAD, anchor="middle"))
            else:
                out.append(f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="{MUTE}" stroke-width="1.4"/>')
        # observed read marker: one error away from A
        if d >= 2:
            xo = x0 + step
            out.append(f'<circle cx="{xo}" cy="{y}" r="11" fill="none" stroke="{c}" stroke-width="1.8"/>')
            out.append(t(xo, y + 28, "read with 1 error", 10.5, c, anchor="middle"))
        for j, ln in enumerate(desc.split("\n")):
            out.append(t(420, y - 4 + j * 15, ln, 12, INK))
    out.append(t(40, 266, "Each hop is one base difference. With errors rare, distance 3 corrects one; "
                          "distance 5 corrects two.", 14, INK))
    return svg(720, 286, "".join(out))


# ------------------------------------------------------------------ 4 indels

def fig_indel():
    bc = "ATCACG"
    rd = "ACACGT"       # T lost at position 2, next base T slides in
    out = [t(40, 26, "Hamming distance counts substitutions; a lost base shifts everything after it.", 14, INK)]
    out.append(t(40, 66, "true barcode", 12.5, MUTE))
    s, _ = seq(200, 66, bc, TOP, 15)
    out.append(s)
    out.append(t(40, 100, "read, one T deleted", 12.5, MUTE))
    for j, ch in enumerate(rd):
        c = BAD if ch != bc[j] else TOP
        out.append(t(200 + j * DX, 100, ch, 15, c, family=MONO))
    h, lv = hamming(bc, rd), lev(bc, rd)
    out.append(t(40, 150, f"Hamming distance: {h} of 6 positions differ", 14, BAD))
    out.append(t(40, 174, f"Levenshtein (edit) distance: {lv}, one deletion plus the base that slid in", 14, OK))
    out.append(t(40, 214, "Substitutions dominate on Illumina, so Hamming is the right design metric there.", 13.5, INK))
    out.append(t(40, 236, "Platforms with indel errors (nanopore, long reads) need edit-distance-aware "
                          "barcode sets.", 13.5, INK))
    return svg(640, 256, "".join(out))


# ------------------------------------------------------------------ 5 colour balance

def _grid(x0, y0, bs, title):
    out = [t(x0, y0 - 14, title, 13, INK)]
    for i, b in enumerate(bs):
        for j, ch in enumerate(b):
            x = x0 + j * 36
            y = y0 + i * 26
            out.append(f'<rect x="{x}" y="{y}" width="32" height="22" rx="3" fill="{CHAN[ch]}" opacity="0.9"/>')
            out.append(t(x + 16, y + 16, ch, 13, "#ffffff", anchor="middle", family=MONO))
    yv = y0 + len(bs) * 26 + 14
    for j in range(len(bs[0])):
        r, g = channels(bs, j)
        ok = r and g
        out.append(t(x0 + j * 36 + 16, yv, "ok" if ok else ("dark" if not (r or g) else ("no red" if not r else "no green")), 10.5,
                     OK if ok else BAD, anchor="middle"))
    return "".join(out)


def fig_colour():
    out = [t(40, 26, "Two-colour chemistry: C is red, T is green, A is both, G is dark.", 14, INK)]
    out.append(_grid(40, 70, OLD4, "distance 4, but colour-poor"))
    out.append(_grid(320, 70, SET4, "distance 3, balanced"))
    for k, (ch, lab) in enumerate([("C", "red"), ("T", "green"), ("A", "both"), ("G", "dark")]):
        out.append(f'<rect x="{590}" y="{70 + k*24}" width="18" height="16" rx="3" fill="{CHAN[ch]}"/>')
        out.append(t(614, 83 + k * 24, f"{ch}: {lab}", 12, MUTE))
    out.append(t(40, 232, "At every position the pool needs some signal in each colour. "
                          "A column of G is dark: the instrument sees nothing and cannot lock on.", 13.5, INK))
    return svg(740, 252, "".join(out))


# ------------------------------------------------------------------ 6 UDI

def fig_udi():
    out = [t(40, 26, "A hopped read is only recognisable if the pair it carries belongs to no sample.", 14, INK)]
    for p, (ttl, unique) in enumerate([("combinatorial: every i7 with every i5", False),
                                       ("unique dual: each pair used once", True)]):
        x0 = 60 + p * 330
        out.append(t(x0 - 20, 54, ttl, 12.5, INK))
        for r in range(4):
            out.append(t(x0 - 8, 98 + r * 28, f"i7-{r+1}", 10.5, MUTE, anchor="end"))
            for c in range(4):
                x, y = x0 + c * 40, 80 + r * 28
                used = (not unique) or (r == c)
                out.append(f'<rect x="{x}" y="{y}" width="34" height="22" rx="3" '
                           f'fill="{BLUEF if used else "none"}" stroke="{TOP if used else MUTE}" stroke-width="1.2"'
                           f'{"" if used else " stroke-dasharray=\"3 3\""}/>')
        for c in range(4):
            out.append(t(x0 + c * 40 + 17, 74, f"i5-{c+1}", 10.5, MUTE, anchor="middle"))
        # the hopped read: i7-1 with i5-2
        x, y = x0 + 1 * 40, 80
        out.append(f'<circle cx="{x+17}" cy="{y+11}" r="14" fill="none" stroke="{BAD if not unique else OK}" stroke-width="2.2"/>')
        out.append(t(x0, 214, "hopped read: i7-1 with i5-2" , 12, MUTE))
        out.append(t(x0, 234, "lands in a real sample: undetectable" if not unique else
                     "lands in an empty cell: discard it", 12.5, BAD if not unique else OK))
    out.append(t(40, 264, "Cost: unique dual sets need 2 × n index oligos for n samples; "
                          "combinatorial sets need about 2 × sqrt(n).", 13.5, INK))
    return svg(720, 284, "".join(out))


# ------------------------------------------------------------------ 7 bead oligo

def fig_beadoligo():
    out = [t(40, 26, "Bead-bound barcodes: one barcode per bead, a different UMI on every oligo.", 14, INK)]
    out.append(bead(90, 150, 52, "bead"))
    cols = [(HOT, "cell barcode"), ]
    ys = [88, 128, 168]
    umis = ["GTCAGTAA", "CCATGAAT", "TAGGCTCA"]
    for i, y in enumerate(ys):
        x = 190
        out.append(line(130, 150, x, y, MUTE, 1.2))
        out.append(box(x, y - 13, 80, 26, "PCR handle", BLUEF, TOP, 11, TOP))
        out.append(box(x + 80, y - 13, 100, 26, "ACGTTGCAGTCA", "#f7ede6", HOT, 11.5, HOT))
        out.append(box(x + 180, y - 13, 76, 26, umis[i], "#f5eae6", BAD, 11.5, BAD))
        out.append(box(x + 256, y - 13, 90, 26, "TTTTTTTT...", GREENF, OK, 11.5, OK))
    out.append(t(230, 62, "handle", 11.5, TOP, anchor="middle"))
    out.append(t(320, 62, "cell barcode", 11.5, HOT, anchor="middle"))
    out.append(t(320, 76, "(same on the bead)", 10.5, HOT, anchor="middle"))
    out.append(t(448, 62, "UMI", 11.5, BAD, anchor="middle"))
    out.append(t(448, 76, "(differs per oligo)", 10.5, BAD, anchor="middle"))
    out.append(t(530, 218, "oligo-dT captures poly(A) mRNA", 11.5, OK, anchor="middle"))
    out.append(t(40, 252, "Only the cell barcode is shared. The UMIs make every captured molecule distinct. "
                          "Drop-seq uses 12 nt of barcode and 8 nt of UMI.", 13.5, INK))
    return svg(740, 272, "".join(out))


# ------------------------------------------------------------------ 8 split-pool

def fig_splitpool():
    out = [t(40, 26, "Split-pool: each round appends one barcode, and the path through the wells is the cell's identity.", 14, INK)]
    rounds = 3
    wells = 3
    xs = [110 + r * 190 for r in range(rounds)]
    paths = {"cell 1": (HOT, [1, 0, 2]), "cell 2": (TOP, [1, 2, 0]), "cell 3": (OK, [0, 0, 2])}
    for r in range(rounds):
        out.append(t(xs[r] + 22, 52, f"round {r+1}", 12.5, INK, anchor="middle"))
        for w in range(wells):
            y = 70 + w * 44
            out.append(box(xs[r], y, 44, 30, "ABC"[w] + str(r + 1), PALE, MUTE, 12, MUTE))
    for name, (c, pth) in paths.items():
        for r in range(rounds - 1):
            y1 = 70 + pth[r] * 44 + 15
            y2 = 70 + pth[r + 1] * 44 + 15
            off = {"cell 1": -4, "cell 2": 0, "cell 3": 4}[name]
            out.append(line(xs[r] + 44, y1 + off, xs[r + 1], y2 + off, c, 2))
        out.append(t(xs[-1] + 56, 70 + pth[-1] * 44 + 20 + {"cell 1": -10, "cell 2": 0, "cell 3": 10}[name],
                     name + ": " + "-".join("ABC"[p] + str(i + 1) for i, p in enumerate(pth)), 11.5, c))
    out.append(t(40, 232, "Between rounds, all wells are pooled and re-split at random.", 12.5, MUTE))
    n = 96 ** 3
    cells = 50000
    p_collide = 1 - math.exp(-cells / n)
    out.append(t(40, 254, f"3 rounds of 96 wells give 96³ = {n:,} paths. Load {cells:,} cells and about "
                          f"{p_collide*100:.1f}% of them share a path with another cell.", 13.5, INK))
    return svg(740, 274, "".join(out))


# ------------------------------------------------------------------ 9 plate

def fig_plate():
    rows, cols = 16, 24
    out = [t(40, 26, "Plate-based: the well is the address, and two short index sets give the pair.", 14, INK)]
    x0, y0, s = 90, 54, 17
    for r in range(rows):
        for c in range(cols):
            hl = (r, c) == (5, 8)
            out.append(f'<rect x="{x0 + c*s}" y="{y0 + r*s}" width="{s-3}" height="{s-3}" rx="3" '
                       f'fill="{HOT if hl else BLUEF}" stroke="{TOP}" stroke-width="0.8"/>')
    out.append(t(x0 - 8, y0 + 5 * s + 10, "i5-6", 11, HOT, anchor="end"))
    out.append(t(x0 + 8 * s + 6, y0 - 4, "i7-9", 11, HOT, anchor="middle"))
    out.append(t(x0 - 8, y0 + 9, "rows: 16 i5", 11, MUTE, anchor="end"))
    out.append(t(x0 + 12 * s, y0 + rows * s + 14, "columns: 24 i7", 11, MUTE, anchor="middle"))
    out.append(t(x0 + cols * s + 20, y0 + 40, f"{rows} + {cols} = {rows+cols} indexes", 13, INK))
    out.append(t(x0 + cols * s + 20, y0 + 60, f"label {rows*cols} wells", 13, INK))
    out.append(t(x0 + cols * s + 20, y0 + 96, "the highlighted well carries", 11.5, MUTE))
    out.append(t(x0 + cols * s + 20, y0 + 112, "i5-6 on its row and i7-9", 11.5, MUTE))
    out.append(t(x0 + cols * s + 20, y0 + 128, "on its column", 11.5, MUTE))
    out.append(t(40, 372, "One short set on each primer labels every well, so 384 wells "
                          "need 40 oligos, not 384.", 13.5, INK))
    return svg(740, 392, "".join(out))


# ------------------------------------------------------------------ 10 combinatorial scaling

def fig_combscale():
    N = 10_000
    out = [t(40, 26, f"Oligos to buy for {N:,} distinct barcodes (log scale).", 14, INK)]
    rows = []
    for r in range(1, 5):
        k = math.ceil(N ** (1 / r) - 1e-9)
        while k ** r < N:
            k += 1
        rows.append((r, k, r * k))
    for i, (r, k, tot) in enumerate(rows):
        y = 54 + i * 44
        lab = "one set, one position" if r == 1 else f"{r} positions of {k}"
        out.append(t(40, y + 15, lab, 12.5, INK))
        w = 100 * math.log10(tot + 1) / 1.0
        out.append(f'<rect x="230" y="{y}" width="{w:.0f}" height="22" fill="{HOT if i else MUTE}" opacity="0.85"/>')
        out.append(t(230 + w + 10, y + 16, f"{tot:,} oligos  ({k}^{r} = {k**r:,})", 12.5, INK))
    out.append(t(40, 244, "Each added position multiplies the barcodes while adding oligos linearly. "
                          "Split-pool and plate designs both use this.", 13.5, INK))
    return svg(740, 264, "".join(out))


# ------------------------------------------------------------------ 11 UMI idea

def fig_umiidea():
    out = [t(40, 26, "Three molecules, amplified unequally: reads count the amplification, UMIs count the molecules.", 14, INK)]
    mols = [("AAGTC", TOP, 6), ("CGTAC", HOT, 2), ("GCATA", OK, 1)]
    out.append(t(40, 56, "before PCR: 3 molecules, each tagged once", 12.5, MUTE))
    for i, (u, c, n) in enumerate(mols):
        y = 78 + i * 22
        out.append(box(60, y - 8, 52, 16, u, BLUEF, c, 10.5, c))
        out.append(line(112, y, 200, y, c, 3))
    out.append(arrow(240, 100, 290, MUTE))
    out.append(t(265, 90, "PCR", 11.5, MUTE, anchor="middle"))
    out.append(t(310, 56, "after PCR and sequencing: 9 reads", 12.5, MUTE))
    y = 78
    for u, c, n in mols:
        for k in range(n):
            xx = 320 + (k % 6) * 48
            yy = y + (k // 6) * 0
            out.append(box(xx, yy - 8, 44, 14, u, BLUEF, c, 9.5, c))
        y += 22
    out.append(t(40, 176, "Reads at this position: 9", 14, BAD))
    out.append(t(40, 200, "Distinct UMIs at this position: 3", 14, OK))
    out.append(t(40, 232, "Without UMIs a 6-fold read count cannot be told from 6 independent molecules.", 13.5, INK))
    return svg(640, 252, "".join(out))


# ------------------------------------------------------------------ 12 UMI placement

def fig_umiwhere():
    out = [t(40, 26, "A UMI can enter at any single-copy step: ligation, reverse transcription or template switching.", 14, INK)]
    rows = [("ligation", "adapter carries the UMI", [("adapter + UMI", 120, REDF, BAD), ("DNA fragment", 220, PALE, MUTE)]),
            ("reverse transcription", "primer carries the UMI", [("handle", 54, BLUEF, TOP), ("UMI", 46, REDF, BAD), ("dT...", 50, GREENF, OK), ("cDNA", 190, PALE, MUTE)]),
            ("template switching", "TSO carries the UMI", [("cDNA", 190, PALE, MUTE), ("UMI", 46, REDF, BAD), ("TSO", 54, BLUEF, TOP)])]
    for i, (step, note, parts) in enumerate(rows):
        y = 56 + i * 58
        out.append(t(40, y + 20, step, 13, INK, weight="bold"))
        x = 220
        for lab, w, f, c in parts:
            out.append(box(x, y, w, 28, lab, f, c, 11.5, c if c != MUTE else INK))
            x += w
        out.append(t(x + 16, y + 19, note, 12, MUTE))
    out.append(t(40, 244, "In each case the tag is attached once per molecule, before the first copy is made. "
                          "Everything downstream inherits it.", 13.5, INK))
    return svg(820, 264, "".join(out))


# ------------------------------------------------------------------ 13 UMI in PCR

def fig_umipcr():
    out = [t(40, 26, "A random tag in a PCR primer is not a molecular label: the template is tagged again every cycle.", 14, INK)]
    out.append(t(40, 58, "one template molecule, primers carrying random UMIs", 12.5, MUTE))
    out.append(line(60, 92, 200, 92, MUTE, 3.4))
    out.append(t(54, 96, "template", 11.5, MUTE, anchor="end"))
    for i, (u, c) in enumerate([("CCGAT", TOP), ("TAGCA", HOT), ("GGTAC", OK)]):
        y = 128 + i * 30
        out.append(t(40, y + 4, f"cycle {i+1}", 11.5, MUTE))
        out.append(line(110, y - 2, 200, y - 2, MUTE, 2, dash="3 3"))
        out.append(box(210, y - 11, 56, 18, u, BLUEF, c, 11, c))
        out.append(line(266, y - 2, 340, y - 2, c, 3))
    out.append(t(380, 130, "one molecule", 13, INK))
    out.append(t(380, 150, "now has three UMIs", 13, BAD))
    out.append(t(380, 190, "counted as three molecules", 13, BAD))
    out.append(t(40, 232, "Reverse transcription, ligation and template switching each run once per molecule, "
                          "so the tag is applied once. PCR is a cycle that repeats.", 13.5, INK))
    return svg(700, 252, "".join(out))


# ------------------------------------------------------------------ 14 collapse

def fig_collapse():
    umis = [("ACGTAC", 120), ("ACGTAG", 4), ("TTGCAA", 35), ("TTGCAT", 2), ("GGATCC", 9)]
    out = [t(40, 26, "Sequencing errors create near-copies of real UMIs. Merge a small UMI into a large neighbour.", 14, INK)]
    pos = [(110, 90), (110, 160), (320, 90), (320, 160), (480, 125)]
    # edges: hamming 1 and count ratio rule: big >= 2*small - 1
    keep = set(range(len(umis)))
    for i, (a, na) in enumerate(umis):
        for j, (b, nb) in enumerate(umis):
            if i != j and hamming(a, b) == 1 and na >= 2 * nb - 1:
                out.append(arrow(pos[j][0], pos[j][1] - 16 if pos[j][1] > pos[i][1] else pos[j][1] + 16,
                                 pos[i][0], MUTE) if False else "")
                out.append(line(pos[j][0], pos[j][1], pos[i][0], pos[i][1], MUTE, 1.5, dash="4 3"))
                keep.discard(j)
    for i, ((u, n), (x, y)) in enumerate(zip(umis, pos)):
        r = 10 + math.sqrt(n) * 1.8
        c = TOP if i in keep else MUTE
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.0f}" fill="{BLUEF if i in keep else "none"}" stroke="{c}" stroke-width="1.6"/>')
        out.append(t(x, y + 4, str(n), 11, c, anchor="middle"))
        out.append(t(x + r + 6, y + 4, u, 12, c, family=MONO))
    out.append(t(40, 212, f"{len(umis)} distinct UMI strings, {len(keep)} real molecules.", 14, OK))
    out.append(t(40, 236, "UMIs within one mismatch of a much more abundant UMI are read as its errors "
                          "(a directional network rule).", 13.5, INK))
    return svg(640, 256, "".join(out))


# ------------------------------------------------------------------ 15 UMI length

def fig_umilen():
    out = [t(40, 26, "A short UMI runs out: two molecules draw the same tag. Fraction of molecules lost to collisions.", 14, INK)]
    x0, y0, W, H = 90, 50, 480, 150
    out.append(line(x0, y0 + H, x0 + W, y0 + H, MUTE, 1))
    out.append(line(x0, y0, x0, y0 + H, MUTE, 1))
    cols = {6: BAD, 8: HOT, 10: TOP, 12: OK}
    for L, c in cols.items():
        N = 4 ** L
        pts = []
        for k in range(0, 61):
            lm = 1 + k * 5 / 60          # log10 molecules from 10^1 to 10^6
            m = 10 ** lm
            distinct = N * (1 - math.exp(-m / N))
            loss = 1 - distinct / m
            x = x0 + W * k / 60
            y = y0 + H - H * min(loss, 1.0)
            pts.append(f"{x:.1f},{y:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="2.2"/>')
        out.append(t(x0 + W + 10, y0 + H - H * min(1 - N * (1 - math.exp(-1e6 / N)) / 1e6, 1) + 4 + (L == 6) * -6 + (L == 8) * 10,
                     f"{L} nt", 12, c))
    for v in (0, 0.5, 1.0):
        out.append(t(x0 - 8, y0 + H - H * v + 4, f"{int(v*100)}%", 11, MUTE, anchor="end"))
    for e in range(1, 7):
        out.append(t(x0 + W * (e - 1) / 5, y0 + H + 16, f"10^{e}", 11, MUTE, anchor="middle"))
    out.append(t(x0 + W / 2, y0 + H + 34, "molecules of one gene in one cell or sample", 11.5, MUTE, anchor="middle"))
    N8, m = 4 ** 8, 1000
    loss8 = 1 - N8 * (1 - math.exp(-m / N8)) / m
    out.append(t(40, 266, f"An 8 nt UMI ({N8:,} tags) loses about {loss8*100:.1f}% at 1,000 molecules, "
                          "and far more at 100,000.", 13.5, INK))
    return svg(700, 286, "".join(out))


# ------------------------------------------------------------------ 16 duplex tags

def fig_duplex():
    out = [t(40, 26, "UMI plus duplex tag: a real variant must appear on both strands of the original molecule.", 14, INK)]
    for p, (ttl, both, c) in enumerate([("true variant", True, OK), ("damage on one strand", False, BAD)]):
        x0 = 40 + p * 340
        out.append(t(x0, 56, ttl, 13, c))
        out.append(line(x0, 84, x0 + 230, 84, TOP, 3))
        out.append(line(x0, 98, x0 + 230, 98, BOT, 3))
        out.append(t(x0 + 110, 76, "tag α·β", 11, TOP, anchor="middle"))
        out.append(t(x0 + 110, 116, "tag β·α", 11, BOT, anchor="middle"))
        for k in range(3):
            y = 134 + k * 14
            out.append(line(x0, y, x0 + 230, y, TOP, 1.6))
            out.append(dot(x0 + 150, y, 3.6, c))
        for k in range(3):
            y = 182 + k * 14
            out.append(line(x0, y, x0 + 230, y, BOT, 1.6))
            if both:
                out.append(dot(x0 + 150, y, 3.6, c))
        out.append(t(x0 + 240, 150, "top strand family", 11, TOP))
        out.append(t(x0 + 240, 198, "bottom strand family", 11, BOT))
        out.append(t(x0, 238, "both families agree: keep" if both else "one family only: reject", 12.5, c))
    out.append(t(40, 262, "Single-strand damage (deamination, oxidation) and early PCR errors appear on "
                          "one strand only.", 13.5, INK))
    return svg(720, 282, "".join(out))


# ------------------------------------------------------------------ 17 read structure

def fig_readstruct():
    out = [t(40, 26, "One construct, four reads: cycles drawn to scale (28 / 10 / 10 / 90).", 14, INK)]
    S = 5.2
    reads = [("Read 1", [("cell barcode 16", 16, "#f7ede6", HOT), ("UMI 12", 12, "#f5eae6", BAD)]),
             ("Index 1 (i7)", [("sample 10", 10, GREENF, OK)]),
             ("Index 2 (i5)", [("sample 10", 10, GREENF, OK)]),
             ("Read 2", [("cDNA insert  90 cycles", 90, PALE, MUTE)])]
    tot = 0
    for i, (nm, parts) in enumerate(reads):
        y = 56 + i * 44
        out.append(t(40, y + 17, nm, 12.5, INK))
        x = 160
        for lab, n, f, c in parts:
            w = n * S
            out.append(box(x, y, w, 26, lab if w > 60 else "", f, c, 11, c if c != MUTE else INK))
            if w <= 60:
                out.append(t(x + w + 6, y + 18, lab, 11, c))
            x += w
        tot += sum(n for _, n, _, _ in parts)
    out.append(t(40, 244, f"Total: {tot} cycles. Only Read 2 reads the transcript; "
                          f"the other {tot - 90} cycles say whose it is.", 13.5, INK))
    return svg(720, 264, "".join(out))


# ------------------------------------------------------------------ 18 budget placement

def fig_budget():
    out = [t(40, 26, "Where a 12 nt UMI goes changes which read pays for it.", 14, INK)]
    S = 4.2
    designs = [("in Read 1", [("BC 16", 16, "#f7ede6", HOT), ("UMI 12", 12, REDF, BAD)], 0, 92),
               ("in index read 2", [("BC 16", 16, "#f7ede6", HOT)], 12, 92),
               ("at start of Read 2", [("BC 16", 16, "#f7ede6", HOT)], 0, 80)]
    for i, (nm, r1, i2, r2) in enumerate(designs):
        y = 54 + i * 62
        out.append(t(40, y + 17, nm, 12.5, INK, weight="bold"))
        x = 200
        r1n = sum(n for _, n, _, _ in r1)
        for lab, n, f, c in r1:
            out.append(box(x, y, n * S, 24, lab, f, c, 10.5, c))
            x += n * S
        if i2:
            out.append(box(x + 6, y, i2 * S, 24, "UMI 12", REDF, BAD, 10.5, BAD))
            x += 6 + i2 * S
        else:
            x += 6
        x2 = x + 6
        if i == 2:
            out.append(box(x2, y, 12 * S, 24, "UMI", REDF, BAD, 10.5, BAD))
            out.append(box(x2 + 12 * S, y, 80 * S, 24, "insert 80", PALE, MUTE, 10.5, INK))
        else:
            out.append(box(x2, y, 92 * S, 24, "insert 92", PALE, MUTE, 10.5, INK))
        out.append(t(40, y + 40, f"R1 {r1n}, index {i2 or 0}, R2 {12 + 80 if i == 2 else r2}", 11, MUTE))
    out.append(t(40, 250, "Index reads cost cycles but do not shorten the insert; the same UMI in Read 2 "
                          "takes 12 of the 92 insert bases.", 13.5, INK))
    return svg(820, 270, "".join(out))


# ------------------------------------------------------------------ 19 stagger

def fig_stagger():
    amp = "CCTACGGG"
    out = [t(40, 26, "Staggered primers: shift the start so that the first cycles show all four bases.", 14, INK)]
    out.append(t(40, 56, "four primers with 0, 1, 2, 3 random bases before the conserved site", 12.5, MUTE))
    for i in range(4):
        y = 84 + i * 22
        out.append(t(40, y, f"offset {i}", 11.5, MUTE))
        for k in range(i):
            out.append(t(120 + k * 15, y, "N", 14, MUTE, family=MONO))
        for k, ch in enumerate(amp):
            out.append(t(120 + (i + k) * 15, y, ch, 14, BASEC[ch], family=MONO))
    # composition per cycle
    for panel, (ttl, stag) in enumerate([("unstaggered: cycles 1-8", False), ("staggered: cycles 1-8", True)]):
        x0 = 380 + panel * 0
        yb = 130 + panel * 0
    for panel, (ttl, stag) in enumerate([("all four primers at offset 0", False), ("pool of four staggered primers", True)]):
        x0 = 60 + panel * 340
        y0 = 150
        out.append(t(x0, y0 + 96, ttl, 12, INK))
        for c in range(8):
            comp = {b: 0.0 for b in "ACGT"}
            for i in range(4):
                off = i if stag else 0
                if c < off:
                    for b in comp:
                        comp[b] += 0.25 / 4
                else:
                    comp[amp[c - off]] += 1 / 4
            y = y0 + 80
            for b in "ACGT":
                h = comp[b] * 70
                if h > 0:
                    out.append(f'<rect x="{x0 + c*26}" y="{y - h:.1f}" width="20" height="{h:.1f}" fill="{BASEC[b]}" opacity="0.85"/>')
                y -= h
    for k, b in enumerate("ACGT"):
        out.append(f'<rect x="{680}" y="{150 + k*18}" width="14" height="12" fill="{BASEC[b]}" opacity="0.85"/>')
        out.append(t(700, 160 + k * 18, b, 11.5, MUTE))
    out.append(t(40, 276, "Cost: the reads begin 0 to 3 bases later and must be trimmed. Used for amplicons "
                          "and 16S, and for any library whose reads start identically.", 13.5, INK))
    return svg(760, 296, "".join(out))


# ------------------------------------------------------------------ 20 hashing

def fig_hashing():
    out = [t(40, 26, "Hashing: label each sample's cells with its own oligo, then pool before the encapsulation step.", 14, INK)]
    tags = [("A", TOP), ("B", HOT), ("C", OK)]
    out.append(t(40, 56, "three samples, three tags", 12.5, MUTE))
    for i, (tg, c) in enumerate(tags):
        x = 70 + i * 70
        out.append(f'<circle cx="{x}" cy="100" r="22" fill="none" stroke="{c}" stroke-width="2"/>')
        out.append(t(x, 104, tg, 14, c, anchor="middle", weight="bold"))
        out.append(arrow(x, 134, x + (1 - i) * 18, MUTE) if False else "")
    out.append(arrow(140, 142, 140, MUTE))
    out.append(t(140, 168, "pool, run once", 12, MUTE, anchor="middle"))
    # table
    x0 = 330
    out.append(t(x0, 56, "hashtag reads per cell barcode", 12.5, MUTE))
    heads = ["", "tag A", "tag B", "tag C", "call"]
    for j, h in enumerate(heads):
        out.append(t(x0 + j * 70, 82, h, 12, MUTE, anchor="start"))
    cells = [("cell 1", (98, 2, 0)), ("cell 2", (1, 120, 3)), ("cell 3", (60, 55, 1)), ("cell 4", (3, 2, 1))]
    for i, (nm, (a, b, c)) in enumerate(cells):
        y = 108 + i * 26
        vals = [a, b, c]
        strong = [k for k, v in enumerate(vals) if v >= 20]
        call = "doublet" if len(strong) > 1 else ("tag " + "ABC"[strong[0]] if strong else "empty")
        out.append(t(x0, y, nm, 12.5, INK))
        for j, v in enumerate(vals):
            out.append(t(x0 + (j + 1) * 70, y, str(v), 12.5, tags[j][1] if v >= 20 else MUTE))
        out.append(t(x0 + 4 * 70, y, call, 12.5, BAD if call in ("doublet", "empty") else OK))
    out.append(t(40, 244, "One cell with two strong tags must contain cells from two samples: a "
                          "doublet you can see and discard.", 13.5, INK))
    return svg(740, 264, "".join(out))


build(__file__, [
    ("info", fig_info),
    ("demux", fig_demux),
    ("ladder", fig_ladder),
    ("indel", fig_indel),
    ("colour", fig_colour),
    ("udi", fig_udi),
    ("beadoligo", fig_beadoligo),
    ("splitpool", fig_splitpool),
    ("plate", fig_plate),
    ("combscale", fig_combscale),
    ("umiidea", fig_umiidea),
    ("umiwhere", fig_umiwhere),
    ("umipcr", fig_umipcr),
    ("collapse", fig_collapse),
    ("umilen", fig_umilen),
    ("duplex", fig_duplex),
    ("readstruct", fig_readstruct),
    ("budget", fig_budget),
    ("stagger", fig_stagger),
    ("hashing", fig_hashing),
])
