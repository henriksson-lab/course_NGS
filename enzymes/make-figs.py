#!/usr/bin/env python3
"""Figures for the enzymes unit (all four decks).  Run: python3 enzymes/make-figs.py"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403

# ---------------------------------------------------------------- helpers

CM = {"A": "T", "T": "A", "G": "C", "C": "G", "U": "A"}
SOFT = "#e6e9ec"
WARM = "#f3dcd0"


def cp(s):
    """Complement written in the same left-to-right order (spaces kept)."""
    return "".join(CM.get(c, c) for c in s)


def dc(x, y, top, bot, tr=None, br=None, labels=False, ticks=True):
    """Duplex with per-run colours. tr/br = [(start, end, colour)]. Returns (svg, width)."""
    check_pairing(top, bot)

    def col(runs, i, default):
        for a, b, c in runs or []:
            if a <= i < b:
                return c
        return default

    out = []
    for i, ch in enumerate(top):
        if ch != " ":
            out.append(t(x + i * DX, y, ch, 13, col(tr, i, TOP), family=MONO))
    for i, ch in enumerate(bot):
        if ch != " ":
            out.append(t(x + i * DX, y + 30, ch, 13, col(br, i, BOT), family=MONO))
    if ticks:
        out.append(pairs(x, y, y + 30, top, bot))
    w = max(len(top), len(bot)) * DX
    if labels:
        out.append(t(x - 8, y, "5'", 11.5, MUTE, anchor="end"))
        out.append(t(x - 8, y + 30, "3'", 11.5, MUTE, anchor="end"))
    return "".join(out), w


def mark(x, y, i, strand=0, col=BAD):
    """A small tick on the backbone between base i-1 and i (a nick or cut)."""
    yy = y + 30 * strand
    return line(x + i * DX - 1.5, yy - 12, x + i * DX - 1.5, yy + 4, col, 2.2)


def tbl(x, y, heads, rows, size=12.5, rh=27, hotcols=()):
    """Auto-sized table. Returns (svg, right edge, bottom edge)."""
    widths = []
    for j, h in enumerate(heads):
        m = max([len(h)] + [len(r[j]) for r in rows])
        widths.append(m * size * 0.5 + 22)
    cx = [x]
    for w in widths:
        cx.append(cx[-1] + w)
    out = []
    for j, h in enumerate(heads):
        out.append(t(cx[j], y, h, size, INK, weight="bold"))
    out.append(line(x - 4, y + 8, cx[-1] - 10, y + 8, INK, 1))
    for i, r in enumerate(rows):
        yy = y + 8 + (i + 1) * rh - 8
        if i % 2 == 1:
            out.append(f'<rect x="{x-6}" y="{yy-rh+10}" width="{cx[-1]-x-6}" height="{rh}" '
                       f'fill="{SOFT}" opacity="0.55"/>')
        for j, c in enumerate(r):
            if j == 0:
                colr, wt = INK, "bold"
            else:
                l = c.lower()
                colr, wt = INK, None
                if l.startswith(("no", "none", "–", "-")):
                    colr = MUTE
                elif l.startswith(("yes", "strong", "very strong")):
                    colr = TOP
                elif l.startswith(("check", "stalls", "trap")):
                    colr = HOT
                if j in hotcols:
                    colr = HOT
            out.append(t(cx[j], yy, c, size, colr, weight=wt))
    return "".join(out), cx[-1], y + 8 + len(rows) * rh + 4


def lead(s, y=26):
    return t(30, y, s, 14.5, INK)


def foot(y, s, col=INK):
    return t(30, y, s, 14, col)


def strand_line(x1, x2, y, col=TOP, w=3):
    return line(x1, y, x2, y, col, w)


# ================================================================ DECK 1: polymerases

def fig_pol_core():
    x, y = 90, 92
    d, w = dc(x, y, "ATGCTT" + " " * 7, "TACGAAGCCTAGG", tr=[(0, 6, TOP)],
              br=[(0, 6, BOT), (6, 13, MUTE)], labels=True)
    out = [lead("What every DNA polymerase does: extend a 3'-OH, one base at a time, as the template dictates."), d]
    out.append(t(x + 6 * DX + 6, y - 40, "dCTP", 14, HOT, weight="bold"))
    out.append(line(x + 6 * DX + 16, y - 32, x + 6 * DX + 16, y - 15, HOT, 1.6))
    out.append(t(x + 6 * DX + 8, y + 5, "3'-OH", 11.5, HOT))
    out.append(t(x + 13 * DX + 8, y + 30, "5'", 11.5, MUTE))
    out.append(t(x - 8, y - 22, "primer", 13, TOP, anchor="end"))
    out.append(t(x - 8, y + 58, "template", 13, BOT, anchor="end"))
    out.append(t(x + 15 * DX, y - 8, "the 3'-OH attacks the α-phosphate;", 13.5, INK))
    out.append(t(x + 15 * DX, y + 10, "pyrophosphate leaves; the primer", 13.5, INK))
    out.append(t(x + 15 * DX, y + 28, "is now one base longer", 13.5, INK))
    out.append(foot(178, "Needs: a primer (or a nick) with a free 3'-OH, a template, dNTPs, Mg2+."))
    return svg(700, 196, "".join(out))


def fig_chart_chem():
    heads = ["Enzyme", "Error rate", "3'→5' exo", "5'→3' exo / flap", "Strand displacement", "RT activity"]
    rows = [
        ["Taq", "moderate", "no", "yes (flap endo)", "weak", "trace (Mn2+)"],
        ["Q5 / Phusion / KAPA HiFi", "very high fidelity", "yes", "no", "low", "no"],
        ["Klenow (exo+)", "high fidelity", "yes", "no", "moderate", "no"],
        ["Klenow exo−", "moderate", "no", "no", "moderate", "no"],
        ["T4 DNA polymerase", "high fidelity", "yes (strong)", "no", "none", "no"],
        ["Bst large fragment", "moderate", "no", "no", "strong", "weak"],
        ["phi29", "very high fidelity", "yes", "no", "very strong", "no"],
        ["uracil-tolerant HiFi", "very high fidelity", "yes", "no", "low", "no"],
    ]
    out = [lead("The chart, part 1: what the enzyme does to the DNA it meets")]
    b, r, bt = tbl(30, 62, heads, rows)
    out.append(b)
    out.append(foot(bt + 22, "Ranks, not numbers: error rates depend on the assay. Compare rows within one vendor's chart.", MUTE))
    out.append(foot(bt + 42, "Mn2+ in place of Mg2+ loosens Taq's base selection: that is what lets it copy RNA, and what costs it fidelity.", MUTE))
    return svg(int(r) + 20, int(bt) + 56, "".join(out))


def fig_chart_use():
    heads = ["Enzyme", "3' end made", "RNA primer", "Nick extension", "dU tolerance", "Temperature", "Longest product"]
    rows = [
        ["Taq", "mostly +A", "poor", "no (cuts flap)", "yes", "68–72 °C", "~5 kb"],
        ["Q5 / Phusion / KAPA HiFi", "blunt", "poor", "no", "stalls", "72 °C", "10–20 kb"],
        ["Klenow (exo+)", "blunt", "yes", "yes (displaces)", "yes", "37 °C", "short fill-in"],
        ["Klenow exo−", "+A", "yes", "yes (displaces)", "yes", "37 °C", "short fill-in"],
        ["T4 DNA polymerase", "blunt", "check", "no", "yes", "12–37 °C", "short fill-in"],
        ["Bst large fragment", "+A, partly", "check", "yes (displaces)", "yes", "60–65 °C", "isothermal, long"],
        ["phi29", "n/a (circular)", "check", "yes (displaces)", "yes", "30 °C", "10 kb or more"],
        ["uracil-tolerant HiFi", "blunt", "poor", "no", "yes", "72 °C", "10–20 kb"],
    ]
    out = [lead("The chart, part 2: what you get, and the conditions it needs")]
    b, r, bt = tbl(30, 62, heads, rows)
    out.append(b)
    out.append(foot(bt + 22, "'check' = depends on the product or the lot: read the datasheet before relying on it.", MUTE))
    return svg(int(r) + 20, int(bt) + 36, "".join(out))


def fig_error_bars():
    out = [lead("Mean errors per 300 bp molecule after 10 doublings ≈ length × rate × doublings")]
    rows = [("Taq-class", 1e-4), ("in between", 1e-5), ("high-fidelity", 1e-6),
            ("proofreading, best case", 1e-7)]
    y = 66
    for name, e in rows:
        v = 300 * e * 10
        wbar = 70 * (math.log10(v) + 4.6)
        out.append(t(30, y + 5, name, 13.5, INK))
        out.append(t(190, y + 5, "%.0e / base" % e, 13, MUTE, family=MONO))
        out.append(f'<rect x="300" y="{y-10}" width="{wbar:.0f}" height="20" fill="{TOP}"/>')
        out.append(t(300 + wbar + 8, y + 5, "%.4g errors" % v, 13.5, INK))
        y += 38
    wbar = 70 * (math.log10(0.3) + 4.6)
    out.append(t(30, y + 5, "sequencing itself", 13.5, HOT))
    out.append(t(190, y + 5, "~1e-3 / base", 13, MUTE, family=MONO))
    out.append(f'<rect x="300" y="{y-10}" width="{wbar:.0f}" height="20" fill="{HOT}"/>')
    out.append(t(300 + wbar + 8, y + 5, "0.3 per read", 13.5, HOT))
    out.append(foot(y + 40, "Illustrative orders of magnitude, log scale. Library PCR rarely needs more than ~10 doublings."))
    return svg(720, y + 56, "".join(out))


def fig_proofreading():
    out = [lead("Proofreading: the 3' end is moved from the polymerase site to the exonuclease site and trimmed")]
    x0, y = 40, 84
    panels = [
        ("1. mismatch at the 3' end", "ATGCTTG", "TACGAAA", True),
        ("2. exo site removes it", "ATGCTT ", "TACGAAA", False),
        ("3. polymerase site continues", "ATGCTTA", "TACGAAT", False),
    ]
    for i, (lab, top, bot, mm) in enumerate(panels):
        x = x0 + i * 250
        out.append(t(x, y - 28, lab, 13.5, INK))
        s1, _ = seq(x, y, top, TOP)
        s2, _ = seq(x, y + 30, bot, BOT)
        out += [s1, s2]
        for j in range(len(top)):
            if top[j] != " ":
                if mm and j == 6:
                    out.append(t(x + j * DX + 3, y + 19, "×", 15, BAD, anchor="start", weight="bold"))
                else:
                    out.append(line(x + j * DX + 4, y + 4, x + j * DX + 4, y + 19, MUTE, 1))
        if i == 1:
            out.append(t(x + 6 * DX + 4, y + 1, "G", 13, BAD, family=MONO))
            out.append(line(x + 6 * DX - 1, y - 11, x + 6 * DX + 12, y + 2, BAD, 1.4))
    out.append(foot(y + 92, "Cost: speed. Benefit: errors fall by one to two orders of magnitude. The same exonuclease cannot tell an error from an unpaired A you wanted."))
    return svg(820, y + 112, "".join(out))


def fig_t4_repair():
    out = [lead("T4 DNA polymerase turns ragged ends blunt: fill in 5' overhangs, chew back 3' overhangs")]
    y = 70
    rows = [
        ("5' overhang: polymerase fills in", "ATGCTTAG", "    " + cp("TTAG"), "ATGCTTAG", cp("ATGCTTAG")),
        ("3' overhang: exonuclease trims", "    TTAG", cp("ATGCTTAG"), "    TTAG", "    " + cp("TTAG")),
    ]
    for i, (lab, t1, b1, t2, b2) in enumerate(rows):
        yy = y + i * 98
        out.append(t(40, yy - 24, lab, 13.5, INK))
        d1, w = dc(60, yy, t1, b1, tr=[(0, 8, TOP)], br=[(0, 8, BOT)], labels=True)
        d2, _ = dc(60 + 330, yy, t2, b2, tr=[(0, 8, TOP)], br=[(0, 8, BOT)], labels=True)
        out += [d1, d2, arrow(60 + w + 40, yy + 15, 60 + 300, HOT)]
    out.append(t(60 + 140 + 40, y + 6, "+ dNTPs", 12.5, HOT))
    out.append(t(60 + 140 + 40, y + 104, "3'→5' exo", 12.5, HOT))
    out.append(foot(y + 190, "With dNTPs present, polymerase and exonuclease balance at the blunt end and stay there. It cannot displace a strand."))
    return svg(640, y + 208, "".join(out))


def fig_nick_translation():
    out = [lead("5'→3' exonuclease: the polymerase walks the nick along the template, replacing the downstream strand")]
    full = "ATGCTTAGCCATGA"
    for k, (lab, cut) in enumerate([("nick before", 8), ("after nick translation", 11)]):
        y = 76 + k * 96
        out.append(t(30, y - 26, lab, 13.5, INK))
        d, w = dc(80, y, full, cp(full), tr=[(0, cut, TOP), (cut, 14, HOT)], labels=True)
        out.append(d)
        out.append(mark(80, y, cut))
    out.append(t(80 + 8 * DX - 6, 50, "↓ nick", 12, BAD))
    out.append(t(80 + 11 * DX - 6, 146, "↓ nick has moved", 12, BAD))
    out.append(t(350, 108, "3 nt removed from the 5' side,", 13.5, INK))
    out.append(t(350, 126, "3 nt added to the 3' side", 13.5, INK))
    out.append(foot(234, "Pol I and Taq do this. Klenow, T4 DNA polymerase and the HiFi enzymes do not: they leave the nick, or displace past it."))
    return svg(700, 252, "".join(out))


def fig_displacement_modes():
    out = [lead("Meeting a downstream strand: three behaviours, three uses")]
    y = 70
    heads = [("stops (T4 DNA pol)", "nick or gap is left intact", MUTE),
             ("displaces (Klenow, Bst, phi29)", "downstream strand is peeled off as a flap", TOP),
             ("degrades (Taq, Pol I)", "downstream strand is cut away", HOT)]
    for i, (a, b, col) in enumerate(heads):
        yy = y + i * 68
        out.append(t(30, yy - 20, a, 13.5, col, weight="bold"))
        out.append(line(60, yy + 20, 480, yy + 20, BOT, 3))
        if i == 0:
            out.append(line(60, yy + 10, 260, yy + 10, TOP, 3))
            out.append(line(268, yy + 10, 480, yy + 10, HOT, 3))
            out.append(arrow(210, yy - 4, 258, TOP))
        elif i == 1:
            out.append(line(60, yy + 10, 330, yy + 10, TOP, 3))
            out.append(line(330, yy + 10, 400, yy - 12, HOT, 3))
            out.append(arrow(280, yy - 4, 328, TOP))
        else:
            out.append(line(60, yy + 10, 330, yy + 10, TOP, 3))
            # the downstream strand is cut off ahead of the new one and released
            # as short pieces; drawn, not written, so it survives any font
            for k in range(5):
                out.append(line(340 + k * 16, yy + 10, 350 + k * 16, yy + 10, HOT, 3))
            out.append(line(430, yy + 10, 480, yy + 10, HOT, 3))
            out.append(arrow(280, yy - 4, 328, TOP))
        out.append(t(510, yy + 15, b, 13.5, INK))
    out.append(foot(y + 3 * 68 - 4, "Blue: new strand. Orange: the downstream strand that is in the way."))
    return svg(820, y + 3 * 68 + 14, "".join(out))


def fig_rca_mda():
    out = [lead("Strand displacement lets one template be copied again and again")]
    # RCA
    out.append(t(40, 56, "rolling circle (phi29): a circle becomes a long tandem strand", 13.5, INK))
    out.append(f'<circle cx="90" cy="130" r="34" fill="none" stroke="{BOT}" stroke-width="3"/>')
    out.append(line(124, 130, 520, 130, TOP, 3))
    for i in range(5):
        out.append(line(160 + i * 80, 120, 160 + i * 80, 140, HOT, 1.6))
    out.append(t(124, 164, "copy 1", 12, MUTE))
    out.append(t(204, 164, "copy 2", 12, MUTE))
    out.append(t(284, 164, "copy 3", 12, MUTE))
    out.append(t(364, 164, "copy 4 ...", 12, MUTE))
    out.append(arrow(480, 108, 540, HOT))
    # MDA
    out.append(t(600, 56, "MDA: random primers make it branch", 13.5, INK))
    out.append(line(600, 130, 900, 130, BOT, 3))
    for x1, dy in [(630, -1), (700, 1), (770, -1), (830, 1)]:
        out.append(line(x1, 130, x1 + 60, 130 + dy * 34, TOP, 2.6))
        out.append(line(x1 + 60, 130 + dy * 34, x1 + 100, 130 + dy * 34, TOP, 2.6))
    out.append(foot(200, "Each new strand displaces the one ahead of it, which is itself copied. 30 °C, thousands-fold amplification, long fragments."))
    out.append(foot(222, "[Dean 2002, doi:10.1073/pnas.082089499]", MUTE))
    return svg(960, 240, "".join(out))


def fig_a_tail():
    out = [lead("The 3' end the enzyme leaves decides whether the next ligation can happen")]
    # insert + adapter (T overhang) panel
    ins_t, ins_b = "ATGCTTAGCA", "TACGAATCG "
    ad_t, ad_b = " CGTAGC", "TGCATCG"
    y = 74
    out.append(t(30, y - 28, "+A end (Taq, Klenow exo−, kit A-tailing) meets a T overhang: pairs, ligates", 13.5, OK))
    d, w = dc(60, y, ins_t, ins_b, tr=[(9, 10, HOT)], labels=True)
    out.append(d)
    d2, _ = dc(60 + w + 24, y, ad_t, ad_b, tr=[(0, 7, MUTE)], br=[(0, 1, HOT), (1, 7, MUTE)], labels=False)
    out.append(d2)
    y2 = 192
    out.append(t(30, y2 - 28, "proofreading enzyme: the A is removed as 'unpaired', the end is blunt, the T overhang cannot pair", 13.5, BAD))
    d, w = dc(60, y2, "ATGCTTAGC", cp("ATGCTTAGC"), labels=True)
    out.append(d)
    d2, _ = dc(60 + w + 24, y2, ad_t, ad_b, tr=[(0, 7, MUTE)], br=[(0, 1, HOT), (1, 7, MUTE)])
    out.append(d2)
    out.append(t(60 + w + 24 + 200, y2 + 16, "← no ligation, and no error message", 13.5, BAD))
    out.append(foot(258, "[Clark 1988, doi:10.1093/nar/16.20.9677]", MUTE))
    return svg(720, 272, "".join(out))


def fig_rt_switch():
    out = [lead("Template switching: at the end of the RNA, RT adds C's and hops onto an oligo that ends in G's")]
    rna = "GCUAACGGAUCG"
    tso = "CTAGATGGG"
    top1 = tso + rna
    bot1 = " " * 6 + "CCC" + cp(rna)
    y = 76
    out.append(t(30, y - 28, "1. RT reaches the 5' end of the RNA and adds non-templated C's; the oligo (orange) anneals by its G's", 13.5, INK))
    d, w = dc(80, y, top1, bot1, tr=[(0, 9, HOT), (9, 21, TOP)], br=[(0, 21, BOT)], labels=False)
    out.append(d)
    # the cDNA starts six bases in, so its 3' label goes there, not at the margin
    out.append(t(72, y, "5'", 11.5, MUTE, anchor="end"))
    out.append(t(80 + 6 * DX - 8, y + 30, "3'", 11.5, MUTE, anchor="end"))
    y2 = 188
    out.append(t(30, y2 - 28, "2. RT carries on copying the oligo: the cDNA now carries a known sequence at its 3' end", 13.5, INK))
    bot2 = cp(top1)
    d, w = dc(80, y2, top1, bot2, tr=[(0, 9, HOT), (9, 21, TOP)], br=[(0, 9, HOT), (9, 21, BOT)], labels=True)
    out.append(d)
    out.append(foot(256, "No ligation, no second primer. [Zhu 2001, doi:10.2144/01304pf02]  [Picelli 2013, doi:10.1038/nmeth.2639]", INK))
    return svg(720, 272, "".join(out))


def fig_second_strand():
    out = [lead("Second-strand synthesis from an RNA:DNA hybrid: RNase H makes the primers, Pol I extends them")]
    rows = [("1. first-strand cDNA (blue) with its RNA (orange)", 0),
            ("2. RNase H nicks the RNA: its fragments are now primers with 3'-OH", 1),
            ("3. Pol I extends each fragment and its 5'→3' exo eats the next: all RNA replaced by DNA", 2)]
    for k, (lab, mode) in enumerate(rows):
        y = 62 + k * 76
        out.append(t(30, y - 8, lab, 13.5, INK))
        out.append(line(60, y + 32, 620, y + 32, BOT, 3.2))
        segs = [(60, 190), (200, 330), (340, 470), (480, 620)]
        for a, b in segs:
            if mode == 0:
                out.append(line(60, y + 20, 620, y + 20, HOT, 3.2))
                break
            if mode == 1:
                out.append(line(a, y + 20, b - 24, y + 20, HOT, 3.2))
            else:
                out.append(line(a, y + 20, b, y + 20, TOP, 3.2))
    out.append(foot(62 + 3 * 76 - 10, "Short RNA pieces left on the strand act as the primers. A kit that skips RNase H and Pol I would leave single-stranded cDNA."))
    out.append(foot(62 + 3 * 76 + 12, "[Gubler and Hoffman 1983, doi:10.1016/0378-1119(83)90230-5]", MUTE))
    return svg(820, 62 + 3 * 76 + 28, "".join(out))


def fig_dutp_strand():
    out = [lead("dUTP marks the second strand: a polymerase that reads through U keeps both, one that cannot loses it")]
    def duplex_line(y, ulabel):
        out.append(line(60, y, 460, y, TOP, 3))
        out.append(line(60, y + 22, 460, y + 22, BOT, 3))
        for i in range(8):
            out.append(dot(80 + i * 48, y + 22, 4, HOT))
        out.append(t(470, y + 4, "first strand: dTTP", 13, TOP))
        out.append(t(470, y + 27, "second strand: dUTP (orange dots)", 13, HOT))
    duplex_line(70, "")
    out.append(t(30, 54, "library with a dU-marked second strand", 13.5, INK))
    # branches
    out.append(t(30, 150, "U-intolerant HiFi polymerase (or USER): the dU strand is not copied or is cut", 13.5, OK))
    out.append(line(60, 170, 460, 170, TOP, 3))
    out.append(t(470, 174, "only the first strand is amplified: strand of origin is preserved", 13.5, OK))
    out.append(t(30, 218, "U-tolerant polymerase: both strands are amplified", 13.5, BAD))
    out.append(line(60, 238, 460, 238, TOP, 3))
    out.append(line(60, 256, 460, 256, BOT, 3))
    out.append(t(470, 248, "strand information is lost, and nothing tells you", 13.5, BAD))
    out.append(foot(292, "[Parkhomchuk 2009, doi:10.1093/nar/gkp596]  [Levin 2010, doi:10.1038/nmeth.1491]  [Greagg 1999, doi:10.1073/pnas.96.16.9045]", MUTE))
    return svg(820, 308, "".join(out))


def fig_temps():
    out = [lead("Extension temperature: what it buys you, and what limits it")]
    items = [("phi29", 30, 30, TOP), ("T4 DNA polymerase", 12, 37, TOP), ("Klenow / exo−", 37, 37, TOP),
             ("Bst large fragment", 60, 65, HOT), ("Taq", 68, 72, BOT), ("Q5 / Phusion / KAPA HiFi", 72, 72, BOT)]
    x0, x1 = 230, 700
    sc = (x1 - x0) / 80.0
    y = 66
    for name, a, b, col in items:
        out.append(t(30, y + 5, name, 13.5, INK))
        out.append(line(x0, y, x1, y, SOFT, 14, cap="butt"))
        if a == b:
            out.append(dot(x0 + a * sc, y, 7, col))
        else:
            out.append(line(x0 + a * sc, y, x0 + b * sc, y, col, 14, cap="butt"))
        y += 34
    for tk in range(0, 81, 20):
        out.append(t(x0 + tk * sc, y + 2, "%d °C" % tk, 12, MUTE, anchor="middle"))
    out.append(foot(y + 32, "Hot extension melts hairpins and GC-rich structure and blocks mispriming. Cool extension keeps a polymerase that denatures at 95 °C out of the picture."))
    out.append(foot(y + 54, "A high temperature is why Bst and Taq families can copy structured DNA or RNA without help; low temperature is why phi29 never needs cycling."))
    return svg(820, y + 70, "".join(out))


def fig_traps_pol():
    out = [lead("Four silent failures: an activity nobody asked for")]
    heads = ["Step", "Wrong choice", "Unwanted activity", "What you see"]
    rows = [
        ["A-tail for TA ligation", "HiFi polymerase", "3'→5' exo removes the A", "blunt ends, adapters do not ligate"],
        ["Keep a nick as a strand mark", "Taq or Pol I", "5'→3' exo moves the nick", "the mark is gone, strand lost"],
        ["3'-blocked oligo as a blocker", "proofreading polymerase", "3'→5' exo eats the block", "the oligo now primes"],
        ["dU-marked strand to drop", "U-tolerant polymerase", "reads through uracil", "unstranded library, no warning"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "None of these produces an error. Each is visible only in a later step or in the data."))
    return svg(int(r) + 20, int(bt) + 40, "".join(out))


# ================================================================ DECK 2: ligases, kinases, phosphatases

def fig_lig_mech():
    out = [lead("Ligation is three transfers, and the 3 steps explain every requirement")]
    boxes = [("1. enzyme + ATP", "enzyme–AMP + PPi", "(NAD+ in bacteria: gives NMN)"),
             ("2. AMP moves to the 5'-phosphate", "5' end becomes 5'–App", "(an activated pyrophosphate)"),
             ("3. the 3'-OH attacks it", "phosphodiester forms, AMP leaves", "(a nick is sealed)")]
    for i, (a, b, c) in enumerate(boxes):
        x = 30 + i * 300
        out.append(box(x, 50, 270, 92, "", fill=SOFT, stroke=MUTE))
        out.append(t(x + 12, 74, a, 14, INK, weight="bold"))
        out.append(t(x + 12, 100, b, 13.5, TOP))
        out.append(t(x + 12, 124, c, 12.5, MUTE))
        if i < 2:
            out.append(arrow(x + 272, 96, x + 298, MUTE))
    out.append(foot(172, "Needs: 5'-phosphate on one side, 3'-OH on the other, both held in a duplex (a nick). No 5'-P, no step 2."))
    out.append(foot(194, "[Lehman 1974, doi:10.1126/science.186.4166.790]", MUTE))
    return svg(920, 212, "".join(out))


def fig_lig_chart():
    out = [lead("A ligase chart reads by donor chemistry and by substrate")]
    heads = ["Ligase", "Donor", "Joins", "Does not do"]
    rows = [
        ["T4 DNA ligase", "ATP", "blunt, TA, cohesive, DNA nicks", "ssDNA; RNA splints (poorly)"],
        ["E. coli DNA ligase", "NAD+", "cohesive ends, nicks", "blunt ends (barely)"],
        ["Taq DNA ligase", "NAD+, hot", "nicks only; checks the base at the junction", "any end that is not a nick"],
        ["T4 RNA ligase 1", "ATP", "ssRNA and ssDNA ends, intra- or intermolecular", "duplex ends"],
        ["T4 RNA ligase 2, truncated", "5'-App (pre-adenylated)", "adapter 3' to an RNA 3'-OH, no ATP", "phosphorylated donors"],
        ["Chlorella virus ligase (SplintR)", "ATP", "nicks in an RNA:DNA hybrid", "single strands"],
        ["CircLigase-type", "ATP, hot", "closes one ssDNA into a circle", "duplex ends"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=12.5, rh=27)
    out.append(b)
    out.append(foot(bt + 22, "Names differ between vendors; the properties do not. Read the 'substrate' and 'cofactor' lines of the datasheet.", MUTE))
    return svg(int(r) + 20, int(bt) + 36, "".join(out))


def fig_lig_ends():
    out = [lead("Three kinds of double-stranded end for T4 DNA ligase, from slowest to fastest")]
    y = 70
    out.append(t(30, y - 24, "blunt: nothing holds the two ends together long enough", 13.5, INK))
    d, w = dc(60, y, "ATGC", cp("ATGC"), labels=True)
    d2, _ = dc(60 + w + 40, y, "GCTA", cp("GCTA"), labels=True)
    out += [d, d2, t(420, y + 16, "slowest: needs more enzyme and more ends per volume", 13.5, MUTE)]
    y = 160
    out.append(t(30, y - 24, "TA: a single A:T pair (the A-tail and the adapter's T overhang)", 13.5, INK))
    d, w = dc(60, y, "ATGCA", cp("ATGC") + " ", tr=[(4, 5, HOT)], labels=True)
    d2, _ = dc(60 + w + 40, y, " GCTA", "TCGAT", br=[(0, 1, HOT)])
    out += [d, d2, t(420, y + 16, "intermediate: one pair; also stops inserts joining each other", 13.5, MUTE)]
    y = 250
    out.append(t(30, y - 24, "cohesive: a 4-nt overhang finds its partner", 13.5, INK))
    d, w = dc(60, y, "ATGC    ", "TACGTTAA", br=[(4, 8, HOT)], labels=True)
    d2, _ = dc(60 + w + 40, y, "AATTGCTA", "    CGAT", tr=[(0, 4, HOT)])
    out += [d, d2, t(440, y + 16, "fastest, and only with its matching overhang", 13.5, MUTE)]
    out.append(foot(318, "Crowding agents (5–15 % PEG) raise the effective concentration of ends. They speed blunt and TA joins most."))
    return svg(760, 336, "".join(out))


def fig_adapter_nick():
    out = [lead("Adapter ligation: a phosphate on the insert decides whether one or both strands are joined")]
    ins_t, ins_b = "ATGCTTAGCA", "TACGAATCG"
    ad_t, ad_b = "CGTAGC", "TGCATCG"
    top, bot = ins_t + ad_t, ins_b + ad_b
    for k, (lab, both, col) in enumerate([("insert 5'-P present: both strands sealed", True, OK),
                                          ("insert dephosphorylated (5'-OH): the adapter's 3' strand cannot join", False, BAD)]):
        y = 76 + k * 100
        out.append(t(30, y - 26, lab, 13.5, col))
        d, w = dc(60, y, top, bot, tr=[(0, 10, TOP), (10, 16, HOT)], br=[(0, 9, BOT), (9, 16, HOT)], labels=True)
        out.append(d)
        if not both:
            out.append(mark(60, y, 9, strand=1))
            out.append(t(60 + 9 * DX - 18, y + 58, "nick", 12.5, BAD))
    out.append(foot(76 + 100 + 84, "A nick is harmless for PCR (it is melted open and copied) and is a deliberate choice in several designs."))
    return svg(640, 76 + 100 + 100, "".join(out))


def fig_rna_ligation():
    out = [lead("Small RNA adapters in two ligations: no ATP in the first, so nothing but the adapter can join")]
    y = 70
    out.append(t(30, y - 28, "1. pre-adenylated 3' adapter + truncated T4 RNA ligase 2, no ATP", 13.5, INK))
    out.append(box(60, y - 14, 160, 28, "RNA 5'-P ... 3'-OH", fill=SOFT))
    out.append(box(230, y - 14, 220, 28, "5'-App  3' adapter  3'-block", fill=WARM))
    out.append(arrow(460, y, 520, HOT))
    out.append(box(530, y - 14, 160, 28, "RNA", fill=SOFT))
    out.append(box(690, y - 14, 220, 28, "3' adapter  3'-block", fill=WARM))
    out.append(t(60, y + 38, "no ATP: the RNA cannot circularise or join its neighbours; the blocked 3' end stops the adapter joining itself", 12.5, MUTE))
    y = 170
    out.append(t(30, y - 28, "2. 5' adapter + T4 RNA ligase 1, with ATP (the RNA's own 5'-P is the donor)", 13.5, INK))
    out.append(box(60, y - 14, 160, 28, "5' adapter  3'-OH", fill=WARM))
    out.append(box(230, y - 14, 160, 28, "RNA", fill=SOFT))
    out.append(box(390, y - 14, 220, 28, "3' adapter  3'-block", fill=WARM))
    out.append(t(630, y + 5, "← remove spare 3' adapter first, or the", 12.5, MUTE))
    out.append(t(630, y + 22, "5' adapter joins it: adapter dimer", 12.5, BAD))
    out.append(foot(240, "[Viollet 2011, doi:10.1186/1472-6750-11-72]", MUTE))
    return svg(960, 256, "".join(out))


def fig_splint():
    out = [lead("Splinted ligation: a bridging oligo holds two ends in a duplex, so the ligase sees a nick")]
    a, d = "GCTAGGAT", "TTCAGC"
    for k, (lab, aa, dd) in enumerate([("DNA ends on a DNA splint (T4 DNA ligase)", a, d),
                                       ("RNA ends on a DNA splint (a ligase for RNA:DNA hybrids, e.g. SplintR)", "GCUAGGAU", "UUCAGC")]):
        # headroom: the nick mark runs from y-12 to y+4, so the label above it
        # needs to sit clear of both the mark and the panel title
        y = 82 + k * 96
        out.append(t(30, y - 34, lab, 13.5, INK))
        top = aa + dd
        d1, w = dc(100, y, top, cp(top), tr=[(0, 8, TOP), (8, 14, HOT)], br=[(0, 14, BOT)], labels=False)
        out.append(d1)
        out.append(mark(100, y, 8, strand=0))
        out.append(t(100 + 8 * DX - 20, y - 16, "5'-P + 3'-OH meet here", 12, BAD, anchor="start"))
        out.append(t(92, y + 30, "3'", 11.5, MUTE, anchor="end"))
        out.append(t(100 + w + 6, y + 30, "5' splint", 11.5, MUTE))
    out.append(foot(76 + 96 + 62, "Used to join an RNA to an adapter by sequence, to close padlock probes, and to read single bases (mismatch at the junction blocks ligation)."))
    out.append(foot(76 + 96 + 84, "[Lohman 2013, doi:10.1093/nar/gkt1032]", MUTE))
    return svg(800, 76 + 96 + 100, "".join(out))


def fig_circle():
    out = [lead("Circularisation: one molecule, two ends, one ligation")]
    out.append(line(60, 90, 300, 90, TOP, 3))
    # both ends are the ends the ligation needs: neither is a failure
    out.append(dot(60, 90, 6, OK))
    out.append(dot(300, 90, 6, OK))
    out.append(t(60, 120, "5'-P", 13, OK, anchor="middle"))
    out.append(t(300, 120, "3'-OH", 13, OK, anchor="middle"))
    out.append(arrow(330, 90, 400, HOT))
    out.append(f'<circle cx="480" cy="90" r="40" fill="none" stroke="{TOP}" stroke-width="3"/>')
    out.append(t(540, 94, "dilute: ends find each other, not another molecule", 13.5, INK))
    out.append(t(540, 114, "concentrated: concatemers and chimeras", 13.5, BAD))
    out.append(foot(168, "Single-strand ligases close ssDNA or cDNA into circles. Used in ribosome profiling libraries and in single-stranded libraries of damaged DNA."))
    out.append(foot(190, "[Ingolia 2009, doi:10.1126/science.1168978]", MUTE))
    return svg(900, 208, "".join(out))


def fig_pnk():
    out = [lead("T4 PNK does two jobs, and which one you get depends on the buffer")]
    rows = [("5'-OH  →  5'-P", "kinase: needs ATP", "makes an end ligatable as a donor", OK),
            ("3'-P  →  3'-OH", "phosphatase: no ATP needed", "makes an end extendable and ligatable as an acceptor", OK),
            ("5'-P with ATP and ADP", "exchange: slow, reversible", "can also take a phosphate off (kinase reverse)", MUTE)]
    y = 62
    for a, b, c, col in rows:
        # not MONO: the mono stack has no arrow glyph, so it renders as a box
        out.append(t(40, y, a, 14.5, col, weight="bold"))
        out.append(t(290, y, b, 13.5, INK))
        out.append(t(520, y, c, 13.5, MUTE))
        y += 34
    out.append(foot(y + 12, "Same enzyme, same tube: end repair uses both at once. Use a buffer with ATP when you want the kinase to run."))
    return svg(960, y + 30, "".join(out))


def fig_end_control():
    out = [lead("Control which ends can ligate: read the table by end state")]
    heads = ["End state", "donor", "acceptor", "after rSAP", "after PNK + ATP"]
    rows = [
        ["5'-P, 3'-OH", "yes", "yes", "5'-OH, 3'-OH", "unchanged"],
        ["5'-OH, 3'-OH", "no", "yes", "unchanged", "5'-P, 3'-OH"],
        ["5'-OH, 3'-P (MNase cut)", "no", "no", "5'-OH, 3'-OH", "5'-P, 3'-OH"],
        ["5'-P, 3'-blocked (adapter)", "yes", "no", "5'-OH, blocked", "unchanged"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "Dephosphorylate to stop unwanted joins, re-phosphorylate only what you want to join. Between them, destroy the phosphatase."))
    return svg(int(r) + 20, int(bt) + 40, "".join(out))


def fig_trap_rsap():
    out = [lead("The phosphatase that was still active: a silent ligation failure")]
    steps = [("rSAP on the fragments", "5'-P removed", OK), ("inactivate (65 °C, 5 min)", "skipped or too cool", BAD),
             ("add 5'-P adapter + ligase", "adapter 5'-P removed too", BAD), ("result", "no product, no error", BAD)]
    for i, (a, b, col) in enumerate(steps):
        x = 30 + i * 230
        out.append(box(x, 54, 205, 70, "", fill=SOFT if col == OK else WARM, stroke=col))
        out.append(t(x + 10, 80, a, 13.5, INK, weight="bold"))
        out.append(t(x + 10, 104, b, 13, col))
        if i < 3:
            out.append(arrow(x + 207, 89, x + 228, MUTE))
    out.append(foot(160, "rSAP is heat-labile for exactly this reason. A phosphatase that survives dephosphorylates the very adapters you add next."))
    return svg(950, 176, "".join(out))


# ================================================================ DECK 3: nucleases

def fig_nuclease_map():
    out = [lead("Nucleases sorted by what they need and what they leave")]
    heads = ["Group", "Cuts", "Substrate", "Typical product"]
    rows = [
        ["Type II (EcoRI, MspI)", "inside a palindrome", "dsDNA, a site", "5'-P, 3'-OH; overhang or blunt"],
        ["Type IIS / IIG (BsaI, MmeI)", "a fixed distance away", "dsDNA, a site", "designable overhang"],
        ["Nicking enzymes", "one strand only", "dsDNA, a site", "nick with 3'-OH"],
        ["Exonucleases (Exo I, III, λ)", "from an end", "ss or ds, by end type", "shortened molecules"],
        ["RNase H", "RNA in a hybrid", "RNA:DNA", "RNA fragments"],
        ["RNase I, S1, mung bean", "single strands", "ssRNA / ssDNA", "short pieces"],
        ["DNase I, MNase", "anywhere, by accessibility", "dsDNA (MNase also ss)", "mixed ends"],
        ["USER (UDG + EndoVIII)", "at a uracil", "dU in DNA", "a gap"],
        ["Cas9, Cas12a RNPs", "where the guide pairs", "dsDNA + a PAM", "blunt or staggered"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=12.5, rh=27)
    out.append(b)
    out.append(foot(bt + 22, "Three questions for any nuclease: what does it need, where does it cut, what end does it leave?", MUTE))
    out.append(foot(bt + 42, "An RNP is the nuclease loaded with its guide RNA before use; a PAM is the short motif it must find beside the match.", MUTE))
    return svg(int(r) + 20, int(bt) + 56, "".join(out))


def fig_type_iis():
    out = [lead("Type II cuts inside its site; Type IIS reads a site and cuts beside it")]
    out.append(t(30, 54, "EcoRI (Type II): G^AATTC", 13.5, INK))
    d, w = dc(60, 90, "GAATTC", cp("GAATTC"), tr=[(0, 6, HOT)], br=[(0, 6, HOT)], labels=True)
    out.append(d)
    out.append(mark(60, 90, 1, 0))
    out.append(mark(60, 90, 5, 1))
    out.append(t(260, 100, "cut sits in the site: the overhang is whatever the site says", 13.5, MUTE))
    top = "GGTCTCAATGCCTTA"
    out.append(t(30, 158, "BsaI (Type IIS): GGTCTC(N1/N5)", 13.5, INK))
    d, w = dc(60, 194, top, cp(top), tr=[(0, 6, HOT)], br=[(0, 6, HOT)], labels=True)
    out.append(d)
    out.append(mark(60, 194, 7, 0))
    out.append(mark(60, 194, 11, 1))
    out.append(t(400, 204, "cut lies outside the site: the 4-nt overhang is free to design", 13.5, MUTE))
    out.append(foot(262, "Golden Gate cloning and several library designs rely on this: the site is cut off and lost, only the chosen overhang remains."))
    out.append(foot(284, "[Szybalski 1991, doi:10.1016/0378-1119(91)90605-b]", MUTE))
    return svg(820, 300, "".join(out))


def fig_methyl_pair():
    out = [lead("Same site, different sensitivity: methylation-sensitive pairs read the epigenome")]
    heads = ["Enzyme", "site", "unmethylated", "methylated (CpG C, or Dam A)"]
    rows = [["MspI", "C^CGG", "cuts", "cuts"],
            ["HpaII", "C^CGG", "cuts", "no cut"],
            ["DpnI", "GA^TC", "no cut", "cuts (methylated A required)"],
            ["DpnII / MboI", "^GATC", "cuts", "no cut (Dam-methylated)"]]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "MspI cuts every CCGG, so MspI digestion enriches CpG-rich DNA for RRBS: HpaII, not MspI, is blocked by the methyl group."))
    out.append(foot(bt + 46, "[Meissner 2008, doi:10.1038/nature07107]", MUTE))
    return svg(int(r) + 40, int(bt) + 62, "".join(out))


def fig_nicking():
    out = [lead("A nicking enzyme plus a displacing polymerase copies a site forever")]
    out.append(line(60, 102, 510, 102, BOT, 3))          # template strand
    out.append(box(110, 62, 70, 14, "", fill=WARM, stroke=HOT))
    out.append(t(145, 56, "site", 12, HOT, anchor="middle"))
    out.append(line(60, 80, 262, 80, TOP, 3))            # top strand up to the nick
    out.append(line(262, 68, 262, 92, BAD, 2.4))         # the nick itself
    out.append(t(272, 62, "nick (top strand only)", 12.5, BAD))
    out.append(arrow(262, 80, 430, TOP, 3, 7))           # new strand from the 3'-OH
    out.append(line(430, 80, 520, 46, HOT, 3))           # old strand peeled off ahead of it
    out.append(t(532, 46, "old top strand is displaced as a single strand", 13.5, INK))
    out.append(t(532, 92, "the new copy carries the site again: it is nicked", 13.5, INK))
    out.append(t(532, 110, "and copied once more, at one temperature", 13.5, INK))
    out.append(foot(156, "Nicks leave a 3'-OH, which is all a displacing polymerase (Bst, Klenow exo−) needs. Amplification at constant temperature, without cycling."))
    return svg(900, 172, "".join(out))


def fig_exo_table():
    out = [lead("Exonucleases: the end the enzyme needs is the whole story")]
    heads = ["Enzyme", "direction", "substrate", "blocked by"]
    rows = [
        ["Exo I", "3'→5'", "single strand", "phosphorothioate, a duplex"],
        ["Exo III", "3'→5'", "duplex: blunt, 5' overhang, recessed 3'", "3' overhang of 4 nt or more"],
        ["λ exonuclease", "5'→3'", "duplex with 5'-P (strongly)", "5'-OH or a bound protein"],
        ["T7 exonuclease", "5'→3'", "duplex, also nicks", "phosphorothioate"],
        ["RecBCD (Exo V)", "both, ATP", "linear DNA, not circles", "circular DNA survives"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "Typical uses: clear leftover primers (Exo I), clear linear DNA from a circle prep (RecBCD), make single strands (λ exo)."))
    return svg(int(r) + 40, int(bt) + 40, "".join(out))


def fig_rnaseh():
    out = [lead("rRNA depletion with RNase H: DNA oligos mark the rRNA, RNase H destroys what they bind")]
    out.append(t(30, 54, "1. DNA oligos (blue) tile across rRNA (orange); mRNA (green) is left alone", 13.5, INK))
    out.append(line(60, 84, 460, 84, HOT, 3.2))
    for a in range(60, 460, 80):
        out.append(line(a + 4, 98, a + 76, 98, TOP, 3))
    out.append(line(520, 84, 800, 84, OK, 3.2))
    out.append(t(30, 150, "2. RNase H cuts only the RNA in each hybrid; DNase I then removes the oligos", 13.5, INK))
    for a in range(60, 460, 80):
        out.append(line(a + 4, 176, a + 40, 176, HOT, 3.2))
    out.append(line(520, 176, 800, 176, OK, 3.2))
    out.append(foot(226, "Same enzyme, opposite use from second-strand synthesis, where RNase H makes primers. The exercise asks you to compare the two."))
    return svg(900, 244, "".join(out))


def fig_chromatin_digest():
    out = [lead("Cutting chromatin: MNase trims the linkers, DNase I enters open DNA")]
    out.append(line(40, 110, 740, 110, BOT, 2.4))
    for cx in (110, 230, 350, 620):
        out.append(f'<circle cx="{cx}" cy="110" r="26" fill="{SOFT}" stroke="{MUTE}" stroke-width="2"/>')
    # cut marks drawn, not written: the scissors glyph is missing from the
    # figure fonts and left the two labels pointing at nothing
    for x in (170, 290, 440, 565, 690):
        out.append(line(x, 96, x, 124, HOT, 2.4))
    out.append(t(170, 80, "MNase", 12.5, HOT, anchor="middle"))
    out.append(t(500, 80, "open region: DNase I", 12.5, HOT, anchor="middle"))
    out.append(t(110, 160, "~147 bp", 12.5, MUTE, anchor="middle"))
    out.append(t(230, 160, "protected", 12.5, MUTE, anchor="middle"))
    out.append(foot(204, "MNase leaves 5'-OH and 3'-phosphate: repair before ligation. DNase I leaves 5'-P and 3'-OH. Ca2+ activates MNase, Mg2+ DNase I."))
    out.append(foot(226, "[Boyle 2008, doi:10.1016/j.cell.2007.12.014]", MUTE))
    return svg(820, 244, "".join(out))


def fig_user():
    out = [lead("USER opens a dU hairpin: remove the base, then break the backbone")]
    for k, (lab, opened) in enumerate([("hairpin adapter with U in the loop", False), ("after USER: an open, forked adapter", True)]):
        x = 60 + k * 420
        out.append(t(x, 50, lab, 13.5, INK))
        out.append(line(x, 110, x + 120, 110, TOP, 3))
        out.append(line(x, 134, x + 120, 134, BOT, 3))
        if not opened:
            out.append(f'<path d="M {x+120} 110 C {x+170} 106, {x+170} 138, {x+120} 134" fill="none" stroke="{TOP}" stroke-width="3"/>')
            out.append(dot(x + 160, 122, 5, HOT))
            out.append(t(x + 176, 126, "U", 13, HOT, weight="bold"))
        else:
            out.append(line(x + 120, 110, x + 160, 96, TOP, 3))
            out.append(line(x + 120, 134, x + 160, 148, BOT, 3))
    out.append(arrow(420, 122, 470, HOT))
    out.append(t(396, 100, "UDG + EndoVIII", 12, HOT))
    out.append(foot(196, "NEBNext-type kits ligate a closed hairpin so the ends cannot join each other, then open it. The same USER digests dU-marked strands."))
    return svg(900, 214, "".join(out))


def fig_cas():
    out = [lead("Cas9 and Cas12a: where the guide pairs, the PAM sits, and what the cut leaves")]
    for k, (lab, pam_left) in enumerate([("Cas9: PAM (NGG) 3' of the target; blunt cut 3 bp from the PAM", False),
                                         ("Cas12a: PAM (TTTV) 5' of the target; staggered cut far from the PAM", True)]):
        y = 80 + k * 100
        out.append(t(30, y - 36, lab, 13.5, INK))
        out.append(line(60, y, 600, y, BOT, 3))
        out.append(line(60, y + 18, 600, y + 18, BOT, 3))
        px = 100 if pam_left else 500
        out.append(box(px, y - 10, 60 if pam_left else 60, 14, "", fill=WARM, stroke=HOT))
        out.append(t(px + 30, y - 16, "PAM", 12, HOT, anchor="middle"))
        # the guide: at y-30 it read as an underline of the caption above it,
        # and it carried no label at all
        out.append(line(160, y - 20, 500, y - 20, TOP, 2))
        if pam_left:
            out.append(t(506, y - 16, "guide", 11.5, TOP))
        else:
            out.append(t(154, y - 16, "guide", 11.5, TOP, anchor="end"))
        if pam_left:
            out.append(line(430, y - 10, 430, y + 12, BAD, 2.4))
            out.append(line(460, y + 8, 460, y + 30, BAD, 2.4))
        else:
            out.append(line(470, y - 10, 470, y + 30, BAD, 2.4))
    out.append(foot(y + 56, "A blunt cut ligates to anything; a staggered cut leaves a short 5' overhang. Cas12a also shreds nearby single strands once activated."))
    out.append(foot(y + 78, "[Jinek 2012, doi:10.1126/science.1225829]  [Zetsche 2015, doi:10.1016/j.cell.2015.09.038]", MUTE))
    return svg(820, y + 94, "".join(out))


# ================================================================ DECK 4: transposases and modifying enzymes

ME = "AGATGTGTATAAGAGACAG"


def fig_tn5_mech():
    out = [lead("Tn5 cuts the target 9 nt apart on the two strands and joins one strand of each end")]
    tgt = "ATGCCTAGGCCTAGCTA"
    y = 66
    out.append(t(30, y - 24, "1. target DNA: the two cuts are staggered", 13.5, INK))
    d, w = dc(60, y, tgt, cp(tgt), labels=True)
    out.append(d)
    out.append(mark(60, y, 0, 0))
    out.append(mark(60, y, 9, 1))
    # span the two cuts, so "9 nt" names the distance and not the base beside it
    out.append(line(58.5, y + 44, 60 + 9 * DX - 1.5, y + 44, BAD, 1))
    out.append(t(60 + 4.5 * DX, y + 58, "9 nt", 12.5, BAD, anchor="middle"))
    y = 164
    out.append(t(30, y - 24, "2. after cutting: the adapter (transferred strand) sits on the 5' end only", 13.5, INK))
    top = ME + tgt[:9] + tgt[9:]
    bot = cp(ME) + " " * 9 + cp(tgt[9:])
    d, w = dc(60, y, top, bot, tr=[(0, 19, HOT)], br=[(0, 19, HOT)], labels=True)
    out.append(d)
    out.append(t(60 + 19 * DX, y + 60, "gap: 9 nt", 12.5, BAD))
    y = 262
    out.append(t(30, y - 24, "3. at 72 °C a polymerase fills the gap from the free 3'-OH, leftwards", 13.5, INK))
    bot = cp(ME) + cp(tgt[:9]) + cp(tgt[9:])
    d, w = dc(60, y, top, bot, tr=[(0, 19, HOT)], br=[(0, 19, HOT), (19, 28, OK)], labels=True)
    out.append(d)
    out.append(foot(332, "The ME end (orange) is shown with the standard 19 nt. A gap, not a nick: it needs a polymerase, not a ligase."))
    out.append(foot(354, "[Goryshin 1998, doi:10.1074/jbc.273.13.7367]  [Adey 2010, doi:10.1186/gb-2010-11-12-r119]", MUTE))
    return svg(760, 372, "".join(out))


def fig_tn5_adapters():
    out = [lead("Two loaded adapters, four outcomes: only A at one end and B at the other amplifies")]
    combos = [("A ... A", 25, MUTE, "no: the same adapter at both ends folds back"),
              ("B ... B", 25, MUTE, "no: the same"),
              ("A ... B", 25, OK, "yes"), ("B ... A", 25, OK, "yes")]
    y = 64
    cols = {"A": TOP, "B": HOT}
    for name, p, col, note in combos:
        a, b = name[0], name[-1]
        out.append(line(120, y, 360, y, BOT, 3))
        out.append(box(98, y - 9, 22, 18, a, fill=SOFT, stroke=cols[a]))
        out.append(box(360, y - 9, 22, 18, b, fill=SOFT, stroke=cols[b]))
        out.append(t(400, y + 5, "25 %  " + note, 13.5, col))
        y += 40
    out.append(foot(y + 10, "Half the fragments are productive. A single loaded sequence (identical at both ends) cannot make that distinction, so the second adapter is added by PCR instead."))
    out.append(foot(y + 32, "[Picelli 2014, doi:10.1101/gr.177881.114]", MUTE))
    return svg(820, y + 48, "".join(out))


def fig_tn5_variants():
    out = [lead("Where Tn5 lands is set by what it is attached to")]
    out.append(t(30, 54, "free transposome: anywhere", 13.5, INK))
    out.append(line(40, 110, 260, 110, BOT, 2.6))
    out.append(box(110, 80, 30, 26, "Tn5", fill=WARM, stroke=HOT, size=11))
    out.append(t(310, 54, "ATAC-seq: only nucleosome-free DNA", 13.5, INK))
    out.append(line(320, 110, 600, 110, BOT, 2.6))
    for cx in (360, 450, 540):
        out.append(f'<circle cx="{cx}" cy="110" r="20" fill="{SOFT}" stroke="{MUTE}" stroke-width="2"/>')
    out.append(box(396, 80, 30, 26, "Tn5", fill=WARM, stroke=HOT, size=11))
    out.append(box(486, 80, 30, 26, "Tn5", fill=WARM, stroke=HOT, size=11))
    out.append(t(650, 54, "CUT&amp;Tag: protein A–Tn5 on an antibody", 13.5, INK))
    # dropped 16 px so the pA-Tn5 box clears the title running across it
    out.append(line(660, 166, 940, 166, BOT, 2.6))
    out.append(f'<circle cx="800" cy="166" r="20" fill="{SOFT}" stroke="{MUTE}" stroke-width="2"/>')
    out.append(line(800, 146, 800, 112, TOP, 2.4))
    out.append(line(800, 112, 788, 96, TOP, 2.4))
    out.append(line(800, 112, 812, 96, TOP, 2.4))
    out.append(box(776, 70, 48, 22, "pA–Tn5", fill=WARM, stroke=HOT, size=11))
    out.append(foot(216, "Loaded: sold with its adapters bound. Fused: Tn5 joined to a targeting protein. Same chemistry, different address."))
    out.append(foot(238, "[Buenrostro 2013, doi:10.1038/nmeth.2688]  [Kaya-Okur 2019, doi:10.1038/s41467-019-09982-5]", MUTE))
    return svg(980, 254, "".join(out))


def fig_atac_shift():
    out = [lead("ATAC-seq reads start at the cut: the two cuts of one Tn5 are 9 nt apart, so the centre is in between")]
    top = "ATGCCTAGGCCTAGCTA"
    y = 80
    d, w = dc(80, y, top, cp(top), labels=True)
    out.append(d)
    out.append(mark(80, y, 0, 0))
    out.append(mark(80, y, 9, 1))
    out.append(t(80 - 2, y - 22, "+ strand read starts here", 12.5, HOT))
    out.append(t(80 + 9 * DX - 30, y + 70, "− strand read starts here", 12.5, HOT))
    out.append(line(80 + 4.5 * DX + 4, y - 10, 80 + 4.5 * DX + 4, y + 40, OK, 1.6, dash="4 3"))
    out.append(t(80 + 4.5 * DX + 10, y + 56, "centre", 12.5, OK))
    out.append(foot(188, "Shift + strand reads by +4 and − strand reads by −5 to centre them on the insertion. Matters for footprints, not for peaks."))
    return svg(720, 206, "".join(out))


def fig_emseq():
    out = [lead("EM-seq: no bisulfite. Enzymes protect modified C, then deaminate the rest")]
    heads = ["Base", "TET2 + T4-BGT", "APOBEC3A", "Read after PCR"]
    rows = [["C", "unchanged", "→ U", "T"],
            ["5mC", "oxidised to 5caC", "not deaminated", "C"],
            ["5hmC", "glucosylated to 5gmC", "not deaminated", "C"]]
    b, r, bt = tbl(30, 62, heads, rows, size=13.5, rh=32)
    out.append(b)
    out.append(foot(bt + 24, "Intact long DNA is the benefit: bisulfite fragments DNA, this does not."))
    out.append(foot(bt + 46, "[Vaisvila 2021, doi:10.1101/gr.266551.120]", MUTE))
    return svg(int(r) + 40, int(bt) + 62, "".join(out))


def fig_capping():
    out = [lead("Telling capped mRNA from everything else by what is on the 5' end")]
    heads = ["Step", "capped mRNA", "rRNA, processed RNA", "result"]
    rows = [["1. start", "m7G cap", "5'-monophosphate", ""],
            ["2. 5'-P-dependent exonuclease", "survives", "destroyed", "enriched for cap"],
            ["3. decapping enzyme", "cap removed: 5'-P", "gone", "cap becomes ligatable"],
            ["4. ligate a 5' adapter", "adapter joins", "–", "tags capped RNA only"]]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "Each step needs its end state to be exactly as described: a cap, a phosphate, or a free 5'-P."))
    return svg(int(r) + 30, int(bt) + 40, "".join(out))


def fig_t7_ivt():
    out = [lead("T7 RNA polymerase as a linear amplifier: a promoter on the primer, then many RNAs per DNA")]
    steps = [("oligo-dT primer carries a T7 promoter", TOP), ("first and second strand make dsDNA with the promoter", TOP),
             ("T7 polymerase transcribes: hundreds of RNAs", HOT), ("RNA is reverse-transcribed into a library", OK)]
    for i, (a, col) in enumerate(steps):
        x = 30 + i * 240
        out.append(box(x, 56, 215, 72, "", fill=SOFT, stroke=col))
        words = a.split(" ")
        line1, line2 = " ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])
        out.append(t(x + 10, 86, line1, 13, INK))
        out.append(t(x + 10, 108, line2, 13, INK))
        if i < 3:
            out.append(arrow(x + 217, 92, x + 238, MUTE))
    out.append(foot(168, "Linear, not exponential: errors do not compound. Used where little RNA must be amplified fairly (CEL-Seq)."))
    out.append(foot(190, "[Hashimshony 2012, doi:10.1016/j.celrep.2012.08.003]", MUTE))
    return svg(980, 206, "".join(out))


def fig_tailing():
    out = [lead("Tailing enzymes add bases without a template")]
    out.append(t(30, 52, "TdT: DNA 3'-OH + dNTP, any DNA end (best on a 3' overhang)", 13.5, INK))
    d, w = dc(60, 90, "ATGCTT", cp("ATGCTT"), labels=True)
    out.append(d)
    s, _ = seq(60 + w, 90, "GGGGGG", HOT)
    out.append(s)
    out.append(t(60 + w + 6 * DX + 12, 94, "← homopolymer tail", 13, HOT))
    out.append(t(30, 164, "Poly(A) polymerase: RNA 3'-OH + ATP", 13.5, INK))
    s, _ = seq(60, 200, "GCUAACGG", TOP)
    s2, _ = seq(60 + 8 * DX, 200, "AAAAAAAA", HOT)
    out += [s, s2]
    out.append(foot(250, "A ddNTP ends the tail after one base, which is also a way to block a 3' end. The tail is a handle for an oligo-d(A, T) or an RT primer."))
    return svg(820, 266, "".join(out))


def fig_chooser():
    out = [lead("Choosing an enzyme: name the step, find the deciding property")]
    heads = ["Step", "Deciding property", "Enzyme family"]
    rows = [
        ["End repair, make blunt", "3'→5' exo and a 5'→3' pol, no displacement", "T4 DNA pol (+ Klenow)"],
        # not "non-templated ...": tbl() greys any cell that starts with "no"
        ["Add one A", "3' addition without a template, no 3'→5' exo", "Klenow exo−, Taq"],
        ["Library PCR", "fidelity, longest product, uracil tolerance", "HiFi polymerase"],
        ["Whole-genome amplification", "strand displacement, processivity", "phi29, Bst"],
        ["First-strand cDNA", "RT activity, RNase H, temperature", "MMLV-type RT"],
        ["Second strand", "RNA primer extension, nick extension", "Pol I + RNase H"],
        ["Join DNA ends", "donor chemistry, end type", "T4 DNA ligase"],
        ["Join a small RNA", "pre-adenylated donor, no ATP", "truncated RNA ligase 2"],
        ["Cut and tag at once", "9 nt stagger, loaded ends", "Tn5"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=12.5, rh=27)
    out.append(b)
    out.append(foot(bt + 22, "Then check the chart for the one column that would make the step fail silently.", MUTE))
    return svg(int(r) + 20, int(bt) + 36, "".join(out))


def fig_walkthrough():
    out = [lead("TruSeq DNA PCR-free: one row per step, and the row only the PCR kits use")]
    heads = ["Step", "Enzyme", "End state in", "End state out"]
    rows = [
        ["shear", "none: acoustic shearing", "intact genomic DNA", "~350 bp, ragged, 5'-OH or P"],
        ["end repair", "T4 DNA pol + T4 PNK", "ragged, 5'-OH or P", "blunt, 5'-P, 3'-OH"],
        ["A-tail", "Klenow exo− + dATP", "blunt", "3'-A overhang"],
        ["ligate", "T4 DNA ligase", "3'-A + T-overhang adapter", "full-length adapter on each end"],
        ["amplify", "not in PCR-free; HiFi pol with a stub adapter", "adapter-flanked insert", "many copies, blunt"],
    ]
    b, r, bt = tbl(30, 62, heads, rows, size=13, rh=30)
    out.append(b)
    out.append(foot(bt + 24, "Every row's end state out is the next row's end state in. Wrong enzyme at any row and the next row's 'in' does not match."))
    out.append(foot(bt + 44, "Tn5 does rows 1 to 4 in one reaction. PCR-free stops after row 4, which is why it needs micrograms of input.", MUTE))
    return svg(int(r) + 30, int(bt) + 58, "".join(out))


build(__file__, [
    # polymerases
    ("pol-core", fig_pol_core),
    ("chart-chem", fig_chart_chem),
    ("chart-use", fig_chart_use),
    ("error-bars", fig_error_bars),
    ("proofreading", fig_proofreading),
    ("t4-repair", fig_t4_repair),
    ("nick-translation", fig_nick_translation),
    ("displacement-modes", fig_displacement_modes),
    ("rca-mda", fig_rca_mda),
    ("a-tail", fig_a_tail),
    ("rt-switch", fig_rt_switch),
    ("second-strand", fig_second_strand),
    ("dutp-strand", fig_dutp_strand),
    ("temps", fig_temps),
    ("traps-pol", fig_traps_pol),
    # ligases, kinases, phosphatases
    ("lig-mech", fig_lig_mech),
    ("lig-chart", fig_lig_chart),
    ("lig-ends", fig_lig_ends),
    ("adapter-nick", fig_adapter_nick),
    ("rna-ligation", fig_rna_ligation),
    ("splint", fig_splint),
    ("circle", fig_circle),
    ("pnk", fig_pnk),
    ("end-control", fig_end_control),
    ("trap-rsap", fig_trap_rsap),
    # nucleases
    ("nuclease-map", fig_nuclease_map),
    ("type-iis", fig_type_iis),
    ("methyl-pair", fig_methyl_pair),
    ("nicking", fig_nicking),
    ("exo-table", fig_exo_table),
    ("rnaseh", fig_rnaseh),
    ("chromatin-digest", fig_chromatin_digest),
    ("user", fig_user),
    ("cas", fig_cas),
    # transposases and modifying enzymes
    ("tn5-mech", fig_tn5_mech),
    ("tn5-adapters", fig_tn5_adapters),
    ("tn5-variants", fig_tn5_variants),
    ("atac-shift", fig_atac_shift),
    ("emseq", fig_emseq),
    ("capping", fig_capping),
    ("t7-ivt", fig_t7_ivt),
    ("tailing", fig_tailing),
    ("chooser", fig_chooser),
    ("walkthrough", fig_walkthrough),
])
