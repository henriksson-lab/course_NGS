#!/usr/bin/env python3
"""Generate the conceptual SVG figures for the Foundations / nucleic acids deck.

Course-internal build tool (students never run or read code). Standard library only.
Run:  python3 tools/make_figures.py
Writes: foundations/img/*.svg
"""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

MONO = 'ui-monospace, "DejaVu Sans Mono", "Courier New", monospace'
SERIF = '"Palatino Linotype", "Book Antiqua", Palatino, FreeSerif, serif'

INK = "#23282d"       # main text
TOP = "#1f3b57"       # top strand
BOT = "#4a6b8a"       # bottom strand
HOT = "#b4532a"       # the thing being pointed at
OK = "#2e6b3f"
BAD = "#a33a28"
MUTE = "#8a8f94"

DX = 13.5             # per-base advance, matches 13px monospace


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family=\'{SERIF}\' fill="{INK}">\n'
        f'<rect width="{w}" height="{h}" fill="none"/>\n{body}\n</svg>\n'
    )


def t(x, y, s, size=15, fill=None, anchor="start", family=None, weight=None, style=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    f = f' fill="{fill}"' if fill else ""
    fam = f" font-family='{family}'" if family else ""
    w = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" font-size="{size}"{a}{f}{fam}{w}{st}>{s}</text>'


def seq(x, y, s, fill=INK, size=13):
    """A run of bases in monospace, returns (svg, width)."""
    out = []
    for i, ch in enumerate(s):
        if ch != " ":
            out.append(t(x + i * DX, y, ch, size=size, fill=fill, family=MONO))
    return "".join(out), len(s) * DX


def line(x1, y1, x2, y2, stroke=INK, w=1.4, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linecap="{cap}"{d}/>')


COMP = {"AT", "TA", "GC", "CG", "AU", "UA", "GU", "UG"}


def check_pairing(top, bot):
    """Guard: aligned bases must actually pair. A wrong duplex in teaching material
    is worse than no figure, so this raises instead of drawing it."""
    for i, (a, b) in enumerate(zip(top, bot)):
        if a != " " and b != " " and a + b not in COMP:
            raise AssertionError(f"position {i}: {a} cannot pair with {b}\n  {top}\n  {bot}")


def pairs(x, ytop, ybot, top, bot):
    """Vertical pairing ticks where both strands have a base."""
    out = []
    for i, (a, b) in enumerate(zip(top, bot)):
        if a != " " and b != " ":
            cx = x + i * DX + 4
            out.append(line(cx, ytop + 4, cx, ybot - 11, stroke=MUTE, w=1))
    return "".join(out)


def duplex(x, y, top, bot, ltop="5'", rtop="3'", lbot="3'", rbot="5'",
           topfill=TOP, botfill=BOT, show_pairs=True, labels=True):
    """Draw a duplex. top/bot are strings, spaces = no base there."""
    check_pairing(top, bot)
    ytop, ybot = y, y + 30
    s1, w = seq(x, ytop, top, topfill)
    s2, _ = seq(x, ybot, bot, botfill)
    out = [s1, s2]
    if show_pairs:
        out.append(pairs(x, ytop, ybot, top, bot))
    if labels:
        out.append(t(x - 10, ytop, ltop, 13, MUTE, anchor="end"))
        out.append(t(x + w + 8, ytop, rtop, 13, MUTE))
        out.append(t(x - 10, ybot, lbot, 13, MUTE, anchor="end"))
        out.append(t(x + w + 8, ybot, rbot, 13, MUTE))
    return "".join(out), w


def arrow(x1, y, x2, color=HOT, w=1.6, head=5):
    d = 1 if x2 > x1 else -1
    return (line(x1, y, x2 - d * head, y, color, w) +
            f'<path d="M {x2} {y} L {x2 - d*head} {y - head*0.7} L {x2 - d*head} '
            f'{y + head*0.7} Z" fill="{color}"/>')


def brace_label(x, y, text, color=HOT, size=13, anchor="middle"):
    return t(x, y, text, size, color, anchor=anchor)


PROBLEMS = []


def lint(name, content):
    """Catch text that runs off the canvas.

    Figures are checked in and reviewed in a browser, but a browser is not always
    available, so estimate each label's extent and complain if it leaves the box.
    """
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
    W, H = float(m.group(1)), float(m.group(2))
    bad = []
    for mt in re.finditer(r'<text x="([-\d.]+)" y="([-\d.]+)" font-size="([\d.]+)"'
                          r'([^>]*)>([^<]*)</text>', content):
        x, y, size, attrs, txt = (float(mt.group(1)), float(mt.group(2)),
                                  float(mt.group(3)), mt.group(4), mt.group(5))
        w = len(txt) * size * 0.50
        if 'text-anchor="middle"' in attrs:
            x0, x1 = x - w / 2, x + w / 2
        elif 'text-anchor="end"' in attrs:
            x0, x1 = x - w, x
        else:
            x0, x1 = x, x + w
        if x0 < -2 or x1 > W + 2 or y > H or y < 8:
            bad.append(f'    "{txt[:46]}" at x={x:.0f} y={y:.0f} '
                       f'(extends to {x1:.0f}, canvas {W:.0f}x{H:.0f})')
    if bad:
        PROBLEMS.append("  %s\n%s" % (name, "\n".join(bad)))


def fit(content):
    """Widen the canvas so no label is clipped.

    Captions are written as single lines; rather than hand-tuning every canvas,
    measure the labels and grow the box to fit them.
    """
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', content)
    W, H = float(m.group(1)), float(m.group(2))
    need = W
    for mt in re.finditer(r'<text x="([-\d.]+)" y="[-\d.]+" font-size="([\d.]+)"'
                          r'([^>]*)>([^<]*)</text>', content):
        x, size, attrs, txt = (float(mt.group(1)), float(mt.group(2)),
                               mt.group(3), mt.group(4))
        w = len(txt) * size * 0.50
        if 'text-anchor="middle"' in attrs:
            x1 = x + w / 2
        elif 'text-anchor="end"' in attrs:
            x1 = x
        else:
            x1 = x + w
        need = max(need, x1 + 14)
    if need > W:
        content = content.replace(f'viewBox="0 0 {m.group(1)} {m.group(2)}" '
                                  f'width="{m.group(1)}"',
                                  f'viewBox="0 0 {need:.0f} {m.group(2)}" width="{need:.0f}"')
    return content


def write(unit, name, content):
    content = fit(content)
    lint(name, content)
    d = os.path.join(ROOT, unit)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    with open(p, "w") as fh:
        fh.write(content)
    print("wrote", os.path.relpath(p, ROOT))


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




# ---------------------------------------------------------------- A2 helpers

def box(x, y, w, h, label="", fill="none", stroke=MUTE, size=13, tcol=INK, r=4):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
         f'stroke="{stroke}" stroke-width="1.2"/>')
    if label:
        s += t(x + w / 2, y + h / 2 + size * 0.35, label, size, tcol, anchor="middle")
    return s


def dot(x, y, r=5, fill=HOT):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def vtick(x, y0, y1, color=TOP, w=2.2):
    return line(x, y0, x, y1, color, w)


# ---------------------------------------------------------------- A2a figures

def fig_sanger():
    out = []
    out.append(t(40, 30, "one template, one primer", 13.5, MUTE))
    out.append(line(60, 56, 300, 56, TOP, 2.4))
    out.append(t(50, 60, "3'", 11.5, MUTE, anchor="end"))
    out.append(line(60, 44, 110, 44, HOT, 2.4))
    out.append(t(85, 34, "primer", 11.5, HOT, anchor="middle"))
    # terminated products of increasing length
    for i, c in enumerate([OK, HOT, BOT, TOP, OK, HOT]):
        y = 84 + i * 15
        out.append(line(60, y, 118 + i * 28, y, MUTE, 2))
        out.append(dot(118 + i * 28, y, 4.5, c))
    out.append(t(40, 190, "every chain stops at one ddNTP", 13.5, MUTE))
    # chromatogram
    bx = 360
    out.append(t(bx, 30, "separate by length, read the colours", 13.5, MUTE))
    import math
    pts = []
    cols = [OK, HOT, BOT, TOP, OK, HOT]
    for i, c in enumerate(cols):
        cx = bx + 20 + i * 36
        p = " ".join(f"{cx-16+j*2.0:.0f},{120-26*math.exp(-((j-16)/5.0)**2):.0f}" for j in range(33))
        out.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="2"/>')
        out.append(t(cx, 140, "ACGT"[i % 4], 13, c, anchor="middle", family=MONO))
    out.append(line(bx, 120, bx + 230, 120, MUTE, 1))
    out.append(t(bx, 190, "700-1000 bases, one molecule species", 13.5, MUTE))
    out.append(t(40, 224, "A mixture would give overlapping peaks: Sanger needs every molecule "
                          "in the tube to be the same.", 14, INK))
    return svg(660, 244, "".join(out))


def fig_universal_ends():
    out = [t(40, 28, "Unknown inserts, identical ends — so one primer reads them all.", 14, INK)]
    for i, w in enumerate([150, 95, 210]):
        y = 62 + i * 46
        x = 60
        out.append(box(x, y, 52, 20, "P5", "#e8eef5", TOP, 12, TOP))
        out.append(box(x + 52, y, w, 20, "insert " + "ABC"[i], "none", MUTE, 12, MUTE))
        out.append(box(x + 52 + w, y, 52, 20, "P7", "#f5eae6", BAD, 12, BAD))
        out.append(arrow(x + 16, y + 32, x + 62, HOT))
        out.append(t(x + 52 + w + 64, y + 15, "same primer, same site", 12, MUTE))
    out.append(t(40, 212, "This is the whole reason a library exists: the sequencer only knows "
                          "how to read the ends you gave it.", 14, HOT))
    return svg(680, 232, "".join(out))


def fig_flowcell():
    out = [t(40, 28, "The flow cell is a lawn of two oligos.", 14, INK)]
    y = 150
    out.append(f'<rect x="40" y="{y}" width="600" height="14" fill="#dfe3e6"/>')
    for i in range(24):
        x = 52 + i * 25
        c = TOP if i % 2 == 0 else BAD
        out.append(vtick(x, y, y - 26, c, 2.6))
    out.append(t(52, y + 32, "P5", 12.5, TOP))
    out.append(t(77, y + 32, "P7", 12.5, BAD))
    out.append(t(120, y + 32, "grafted by their 5' ends, so the 3' ends are free to be extended",
                 12.5, MUTE))
    # library molecule
    out.append(line(220, 62, 420, 62, MUTE, 3))
    out.append(box(176, 52, 46, 20, "P5'", "#e8eef5", TOP, 12, TOP))
    out.append(box(418, 52, 46, 20, "P7'", "#f5eae6", BAD, 12, BAD))
    out.append(t(320, 44, "insert", 12.5, MUTE, anchor="middle"))
    out.append(arrow(200, 96, 200, TOP))
    out.append(f'<path d="M 199 80 L 199 112" stroke="{TOP}" stroke-width="1.4" '
               f'stroke-dasharray="4 3"/>')
    out.append(t(214, 104, "anneals to a P5 lawn oligo", 12.5, TOP))
    out.append(t(40, 214, "A molecule with the same end at both ends, or with only one, "
                          "cannot bridge — and never forms a cluster.", 14, HOT))
    return svg(680, 234, "".join(out))


def fig_bridge():
    out = []
    titles = ["1. copy, keep the copy", "2. bend over and bridge", "3. repeat → a cluster"]
    for p in range(3):
        x0 = 36 + p * 215
        out.append(t(x0 + 95, 28, titles[p], 13, INK, anchor="middle"))
        out.append(f'<rect x="{x0}" y="150" width="190" height="10" fill="#dfe3e6"/>')
        if p == 0:
            out.append(vtick(x0 + 40, 150, 70, TOP, 2.6))
            out.append(t(x0 + 46, 64, "copied strand, now attached", 11.5, MUTE))
        elif p == 1:
            out.append(f'<path d="M {x0+40} 150 C {x0+40} 80, {x0+140} 80, {x0+140} 150" '
                       f'fill="none" stroke="{TOP}" stroke-width="2.6"/>')
            out.append(vtick(x0 + 140, 150, 142, BAD, 2.6))
            out.append(t(x0 + 90, 92, "free end finds a", 11.5, MUTE, anchor="middle"))
            out.append(t(x0 + 90, 106, "P7 oligo nearby", 11.5, MUTE, anchor="middle"))
        else:
            for i in range(9):
                xx = x0 + 18 + i * 19
                out.append(vtick(xx, 150, 150 - (34 + (i % 3) * 8),
                                 TOP if i % 2 else BAD, 2.4))
            out.append(t(x0 + 95, 70, "~1000 copies, all identical", 11.5, MUTE, anchor="middle"))
    out.append(t(36, 196, "Amplification is local: the copies stay where they were made, which "
                          "is why one cluster gives one read.", 14, INK))
    return svg(690, 216, "".join(out))


def fig_linearise():
    out = [t(40, 28, "Before reading, make every strand in the cluster point the same way.",
             14, INK)]
    y = 120
    for panel, lab in enumerate(["mixed orientations", "cut and wash away one kind",
                                 "anneal the Read 1 primer"]):
        x0 = 40 + panel * 215
        out.append(f'<rect x="{x0}" y="{y}" width="190" height="10" fill="#dfe3e6"/>')
        out.append(t(x0 + 95, 54, lab, 12.5, INK, anchor="middle"))
        for i in range(8):
            xx = x0 + 16 + i * 22
            fwd = i % 2 == 0
            if panel == 0 or fwd:
                out.append(vtick(xx, y, y - 40, TOP if fwd else BAD, 2.4))
            if panel == 1 and not fwd:
                out.append(t(xx, y - 14, "×", 13, BAD, anchor="middle"))
        if panel == 2:
            out.append(arrow(x0 + 150, y - 48, x0 + 178, HOT))
            out.append(t(x0 + 95, y - 56, "R1 primer", 12, HOT, anchor="middle"))
    out.append(t(40, 196, "Only one strand is read at a time. Everything else is removed or "
                          "blocked at its 3' end.", 14, MUTE))
    return svg(690, 216, "".join(out))


def fig_sbs():
    out = [t(40, 28, "One cycle = one base, on every cluster at once.", 14, INK)]
    steps = [("add", "all four bases,\neach dye-labelled and\n3'-blocked"),
             ("image", "one colour per cluster\ntells you the base"),
             ("cleave", "remove the dye and\nthe 3' block"),
             ("repeat", "next cycle adds\nexactly one more base")]
    for i, (h, b) in enumerate(steps):
        x = 42 + i * 160
        out.append(box(x, 56, 132, 96, "", "#fbfbf9", MUTE))
        out.append(t(x + 66, 80, h, 14.5, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 66, 102 + j * 16, ln, 11.5, MUTE, anchor="middle"))
        if i < 3:
            out.append(arrow(x + 136, 104, x + 156, MUTE))
    out.append(t(40, 182, "The 3' block is what makes it stepwise: without it a polymerase "
                          "would run to the end and you would see nothing.", 14, INK))
    out.append(t(40, 206, "Read length is limited by how well the block and dye are removed — "
                          "errors accumulate, so quality falls with cycle number.", 13.5, MUTE))
    return svg(700, 226, "".join(out))


def fig_read_order():
    out = [t(36, 26, "Four reads, four primers, one molecule — in this order.", 14, INK)]
    y = 92
    segs = [("P5", 48, "#e8eef5", TOP), ("i5", 40, "#efe9f3", "#6b5b8a"),
            ("R1 site", 70, "#f1f1ee", MUTE), ("insert", 150, "none", MUTE),
            ("R2 site", 70, "#f1f1ee", MUTE), ("i7", 40, "#efe9f3", "#6b5b8a"),
            ("P7", 48, "#f5eae6", BAD)]
    x = 60
    pos = {}
    for name, w, fill, col in segs:
        out.append(box(x, y, w, 24, name, fill, col, 11.5, col))
        pos[name] = (x, w)
        x += w
    end = x
    # read arrows
    rx, rw = pos["R1 site"]
    out.append(arrow(rx + rw, y + 44, rx + rw + 120, HOT))
    out.append(t(rx + rw + 4, y + 62, "1  Read 1 → into the insert", 12, HOT))
    ix, iw = pos["i7"]
    out.append(arrow(ix + iw, y - 16, ix, "#6b5b8a"))
    out.append(t(ix + iw + 6, y - 12, "2  Index 1 (i7)", 12, "#6b5b8a"))
    jx, jw = pos["i5"]
    out.append(arrow(jx, y - 16, jx + jw, "#6b5b8a"))
    out.append(t(60, y - 28, "3  Index 2 (i5)", 12, "#6b5b8a"))
    sx, sw = pos["R2 site"]
    out.append(arrow(sx, y + 44, sx - 120, HOT))
    out.append(t(sx - 124, y + 62, "4  Read 2 ← from the other end", 12, HOT))
    out.append(t(36, 188, "The indexes are read because they are sequence like any other — "
                          "that is why a sample index must sit next to a primer site.", 14, INK))
    return svg(end + 60, 208, "".join(out))


def fig_pe_turnaround():
    out = [t(40, 26, "How the sequencer gets to the other end of the insert.", 14, INK)]
    steps = ["Read 1 and both\nindex reads are done",
             "strip the new strand;\nthe template bridges again",
             "copy it, then remove\nthe strand just read",
             "Read 2 primer anneals\nand reads the other end"]
    for i, s in enumerate(steps):
        x = 40 + i * 162
        out.append(box(x, 52, 142, 86, "", "#fbfbf9", MUTE))
        for j, ln in enumerate(s.split("\n")):
            out.append(t(x + 71, 86 + j * 17, ln, 11.5, INK, anchor="middle"))
        out.append(t(x + 71, 66, str(i + 1), 13, HOT, anchor="middle", weight="bold"))
        if i < 3:
            out.append(arrow(x + 146, 95, x + 164, MUTE))
    out.append(t(40, 168, "Read 2 is a fresh copy of the opposite strand — it is not the same "
                          "molecule read backwards.", 14, INK))
    out.append(t(40, 192, "This costs time and chemistry, which is why paired-end runs cost "
                          "more than single-end.", 13.5, MUTE))
    return svg(720, 212, "".join(out))


def fig_i5_orientation():
    out = [t(40, 26, "The i5 index is read in one of two directions, depending on the "
                     "instrument.", 14, INK)]
    rows = [("forward-strand workflow", "AGGATAGG", "AGGATAGG",
             "MiSeq, HiSeq 2000/2500, NovaSeq 6000 v1.0"),
            ("reverse-complement workflow", "AGGATAGG", "CCTATCCT",
             "iSeq, MiniSeq, NextSeq, HiSeq 3000/4000/X, NovaSeq 6000 v1.5, NovaSeq X")]
    for i, (name, written, read, instr) in enumerate(rows):
        y = 64 + i * 78
        out.append(t(50, y, name, 13.5, HOT, weight="bold"))
        out.append(t(50, y + 22, "ordered:", 12, MUTE))
        out.append(t(130, y + 22, written, 13.5, INK, family=MONO))
        out.append(t(250, y + 22, "sample sheet needs:", 12, MUTE))
        out.append(t(400, y + 22, read, 13.5, OK if written == read else BAD, family=MONO))
        out.append(t(50, y + 42, instr, 11.5, MUTE))
    out.append(t(40, 224, "Get this wrong and the run looks empty: every read lands in "
                          "Undetermined, with the indexes themselves intact.", 14, HOT))
    out.append(t(40, 248, "Always check the current instrument documentation — the lists "
                          "change with reagent versions.", 13, MUTE))
    return svg(700, 268, "".join(out))


def fig_readthrough():
    out = [t(40, 26, "If the insert is shorter than the read, the read runs into the adapter.",
             14, INK)]
    for i, (ins, lab) in enumerate([(230, "insert longer than the read — fine"),
                                    (90, "insert shorter — read-through")]):
        y = 70 + i * 86
        out.append(box(60, y, 60, 22, "adapter", "#f1f1ee", MUTE, 11, MUTE))
        out.append(box(120, y, ins, 22, "insert", "none", MUTE, 11.5, MUTE))
        out.append(box(120 + ins, y, 60, 22, "adapter", "#f1f1ee", MUTE, 11, MUTE))
        out.append(arrow(120, y + 38, 120 + 170, HOT))
        out.append(t(124, y + 56, "read, 150 bases", 11.5, HOT))
        if ins < 170:
            out.append(f'<rect x="{120+ins}" y="{y+30}" width="{170-ins}" height="16" '
                       f'fill="{BAD}" opacity="0.18"/>')
            out.append(t(120 + ins + 66, y + 56, "adapter bases — must be trimmed off",
                         11.5, BAD))
        out.append(t(330 if i == 0 else 350, y + 15, lab, 12.5, OK if i == 0 else BAD))
    out.append(t(40, 246, "Adapter content in a QC report is this, and it tells you your "
                          "fragment size, not your sequencing quality.", 14, INK))
    return svg(700, 266, "".join(out))


def fig_index_hopping():
    out = [t(40, 26, "Free adapter in the pool can give a read the wrong sample index.", 14, INK)]
    out.append(box(50, 54, 150, 56, "", "#fbfbf9", MUTE))
    out.append(t(125, 76, "pooled libraries", 12.5, INK, anchor="middle"))
    out.append(t(125, 96, "sample A  +  sample B", 12, MUTE, anchor="middle"))
    out.append(t(125, 128, "+ leftover free adapter", 12, BAD, anchor="middle"))
    out.append(arrow(210, 86, 250, MUTE))
    out.append(box(260, 54, 180, 56, "", "#fbfbf9", MUTE))
    out.append(t(350, 78, "on the flow cell the free", 12, INK, anchor="middle"))
    out.append(t(350, 96, "index primes a molecule", 12, INK, anchor="middle"))
    out.append(arrow(450, 86, 490, MUTE))
    out.append(box(500, 54, 150, 56, "", "#fdf3f0", BAD))
    out.append(t(575, 78, "sample A read filed", 12, BAD, anchor="middle"))
    out.append(t(575, 96, "under sample B", 12, BAD, anchor="middle"))
    out.append(t(40, 162, "Worse on patterned flow cells with ExAmp chemistry. "
                          "Typically 0.1–2% of reads.", 13.5, MUTE))
    out.append(t(40, 192, "Fix: unique dual indexes — a hopped read then carries a pair that "
                          "belongs to no sample, so it can be discarded.", 14, OK))
    out.append(t(40, 216, "And clean up thoroughly: free adapter is the fuel.", 13.5, MUTE))
    return svg(700, 236, "".join(out))


def fig_diversity():
    out = [t(40, 26, "The instrument needs all four colours in the first cycles.", 14, INK)]
    import random
    random.seed(7)
    cols = {"A": OK, "C": TOP, "G": HOT, "T": BOT}
    for panel, (lab, kind) in enumerate([("a varied library", "mixed"),
                                         ("an amplicon library", "same")]):
        x0 = 60 + panel * 320
        out.append(t(x0 + 110, 56, lab, 13, INK, anchor="middle"))
        for c in range(10):
            x = x0 + c * 22
            y = 150
            if kind == "mixed":
                fr = [0.25] * 4
            else:
                fr = [1.0, 0, 0, 0] if c < 6 else [0.25] * 4
            for b, f in zip("ACGT", fr):
                h = f * 72
                if h > 0:
                    out.append(f'<rect x="{x}" y="{y-h:.0f}" width="16" height="{h:.0f}" '
                               f'fill="{cols[b]}" opacity="0.85"/>')
                y -= h
            out.append(t(x + 8, 166, str(c + 1), 10, MUTE, anchor="middle"))
        out.append(t(x0 + 110, 186, "cycle", 11.5, MUTE, anchor="middle"))
    out.append(t(40, 216, "All-identical early bases blind the instrument: it cannot tell "
                          "clusters apart or set its colour thresholds.", 14, INK))
    out.append(t(40, 240, "Fixes: spike in PhiX, order primers with 0–3 extra bases so "
                          "libraries are out of phase, or use a varied index set.", 13.5, OK))
    return svg(700, 260, "".join(out))


# ---------------------------------------------------------------- A2b figures

def fig_dnbseq():
    out = [t(40, 26, "MGI: make a circle, copy it hundreds of times into one ball.", 14, INK)]
    steps = [("adapters +\nsplint", "ligate the ends\ntogether"),
             ("ssDNA circle", "exonuclease removes\nanything still linear"),
             ("rolling circle", "phi29 copies round\nand round"),
             ("DNA nanoball", "one long concatemer,\nfolded up")]
    for i, (h, b) in enumerate(steps):
        x = 42 + i * 162
        out.append(box(x, 52, 140, 100, "", "#fbfbf9", MUTE))
        out.append(t(x + 70, 76, h.split("\n")[0], 13, HOT, anchor="middle", weight="bold"))
        if "\n" in h:
            out.append(t(x + 70, 92, h.split("\n")[1], 13, HOT, anchor="middle", weight="bold"))
        for j, ln in enumerate(b.split("\n")):
            out.append(t(x + 70, 114 + j * 16, ln, 11.5, MUTE, anchor="middle"))
        if i < 3:
            out.append(arrow(x + 144, 102, x + 160, MUTE))
    out.append(t(40, 182, "No PCR on the flow cell, so no PCR duplicates from clustering and "
                          "no index hopping of the Illumina kind.", 14, OK))
    out.append(t(40, 206, "The balls sit on a patterned array and are read by probe-anchor "
                          "ligation, not by a processive polymerase.", 13.5, MUTE))
    return svg(710, 226, "".join(out))


def fig_other_shortread():
    out = [t(40, 26, "Two other ways to read a cluster.", 14, INK)]
    out.append(box(46, 50, 300, 118, "", "#fbfbf9", MUTE))
    out.append(t(196, 74, "Element AVITI — sequencing by avidity", 13, HOT, anchor="middle",
                 weight="bold"))
    out.append(t(196, 98, "a multivalent probe carries many copies of", 11.5, MUTE,
                 anchor="middle"))
    out.append(t(196, 114, "one base, so it binds a polony very tightly", 11.5, MUTE,
                 anchor="middle"))
    out.append(t(196, 138, "bright signal from little reagent;", 11.5, INK, anchor="middle"))
    out.append(t(196, 154, "binding is separated from incorporation", 11.5, INK,
                 anchor="middle"))
    out.append(box(362, 50, 300, 118, "", "#fbfbf9", MUTE))
    out.append(t(512, 74, "Ultima — flow-based, no terminator", 13, HOT, anchor="middle",
                 weight="bold"))
    out.append(t(512, 98, "beads on an open wafer; one base flows at a", 11.5, MUTE,
                 anchor="middle"))
    out.append(t(512, 114, "time and is incorporated until it runs out", 11.5, MUTE,
                 anchor="middle"))
    out.append(t(512, 138, "signal height counts homopolymer length,", 11.5, INK,
                 anchor="middle"))
    out.append(t(512, 154, "so homopolymers are the weak spot", 11.5, INK, anchor="middle"))
    out.append(t(40, 198, "Both read short, accurate reads and both want the same thing from "
                          "you: a library with the platform's own ends.", 14, INK))
    out.append(t(40, 222, "The chemistry differs; the library design problem does not.",
                 13.5, MUTE))
    return svg(700, 242, "".join(out))


def fig_smrtbell():
    out = [t(40, 26, "PacBio: close the duplex into a loop so it can be read forever.", 14, INK)]
    b, w = duplex(120, 70, "ATGCTTAGCCA", "TACGAATCGGT", labels=False)
    out.append(b)
    for xx, d in ((120, -1), (120 + w, 1)):
        out.append(f'<path d="M {xx} 70 C {xx + d*44} 70, {xx + d*44} 100, {xx} 100" '
                   f'fill="none" stroke="{HOT}" stroke-width="2.6"/>')
    out.append(t(76, 126, "hairpin", 12, HOT, anchor="middle"))
    out.append(t(120 + w + 44, 126, "hairpin", 12, HOT, anchor="middle"))
    out.append(t(120 + w / 2, 142, "insert", 12, MUTE, anchor="middle"))
    out.append(t(40, 176, "Both strands and both adapters are now one covalently closed "
                          "single-stranded circle.", 14, INK))
    out.append(t(40, 200, "The polymerase can go round it as many times as the insert is "
                          "short enough to allow.", 13.5, MUTE))
    out.append(t(40, 230, "A nick anywhere in the insert ends the read: input DNA quality "
                          "matters more here than for short reads.", 13.5, HOT))
    return svg(660, 250, "".join(out))


def fig_zmw():
    out = [t(40, 26, "One polymerase, watched in real time.", 14, INK)]
    out.append(f'<rect x="60" y="56" width="150" height="96" fill="#eceff1" stroke="{MUTE}"/>')
    out.append(f'<rect x="96" y="56" width="78" height="96" fill="#ffffff" stroke="{MUTE}"/>')
    out.append(t(135, 48, "zero-mode waveguide", 11.5, MUTE, anchor="middle"))
    out.append(dot(135, 140, 9, TOP))
    out.append(t(135, 168, "polymerase fixed at the bottom", 11.5, MUTE, anchor="middle"))
    out.append(t(135, 184, "only this tiny volume is lit", 11.5, MUTE, anchor="middle"))
    # trace
    x0 = 260
    out.append(line(x0, 140, x0 + 360, 140, MUTE, 1))
    import math
    for i, (c, w) in enumerate([(OK, 16), (HOT, 15), (TOP, 16), (BOT, 15), (OK, 44), (HOT, 16)]):
        cx = x0 + 34 + i * 58 + (0 if i < 4 else 14)
        p = " ".join(f"{cx-w/2+j*(w/16.0):.0f},{140-42*math.exp(-((j-8)/3.2)**2):.0f}"
                     for j in range(17))
        out.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="2.2"/>')
    out.append(t(x0, 60, "each base gives a flash of its own colour", 12, INK))
    out.append(t(x0 + 250, 96, "a long gap", 11.5, HOT))
    out.append(t(x0 + 250, 112, "before this one", 11.5, HOT))
    out.append(t(40, 196, "The timing between flashes is data too: a modified base on the "
                          "template slows the polymerase down.", 14, INK))
    out.append(t(40, 220, "That is how PacBio calls 5mC and 6mA without any conversion "
                          "chemistry at all.", 13.5, OK))
    return svg(700, 240, "".join(out))


def fig_ccs():
    out = [t(40, 26, "Accuracy comes from reading the same molecule many times.", 14, INK)]
    cx, cy, r = 110, 108, 44
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TOP}" '
               f'stroke-width="2.6"/>')
    out.append(t(cx, cy + 5, "one insert", 11.5, MUTE, anchor="middle"))
    out.append(arrow(cx + r + 10, cy, cx + r + 46, HOT))
    for i in range(4):
        y = 70 + i * 24
        out.append(line(230, y, 420, y, MUTE, 2))
        for j in range(2):
            out.append(dot(258 + ((i * 37 + j * 91) % 150), y, 3.2, BAD))
    out.append(t(230, 56, "passes, each with random errors", 12, MUTE))
    out.append(arrow(436, 106, 470, MUTE))
    out.append(line(486, 106, 676, 106, OK, 3))
    out.append(t(486, 88, "consensus: the errors do not agree, the sequence does", 12, OK))
    out.append(t(40, 186, "A short insert gets many passes and very high accuracy; a long "
                          "insert gets few passes and less.", 14, INK))
    out.append(t(40, 210, "So on PacBio, insert length and accuracy are the same decision — "
                          "and size selection is how you make it.", 13.5, HOT))
    return svg(700, 230, "".join(out))


def fig_nanopore():
    out = [t(40, 26, "No polymerase, no copying: the molecule itself is the signal.", 14, INK)]
    out.append(f'<rect x="60" y="96" width="330" height="12" fill="#dfe3e6"/>')
    out.append(t(60, 88, "membrane", 11.5, MUTE))
    out.append(f'<path d="M 216 96 L 204 78 L 248 78 L 236 96 L 236 108 L 248 126 L 204 126 '
               f'L 216 108 Z" fill="#eef1f3" stroke="{TOP}" stroke-width="1.6"/>')
    out.append(t(226, 146, "pore", 11.5, TOP, anchor="middle"))
    out.append(f'<path d="M 120 52 C 170 52, 180 70, 226 78" fill="none" stroke="{MUTE}" '
               f'stroke-width="2.4"/>')
    out.append(dot(150, 56, 8, HOT))
    out.append(t(150, 40, "motor protein ratchets the strand through", 11.5, HOT))
    out.append(line(226, 126, 226, 160, MUTE, 2.4))
    # squiggle
    import math
    pts = []
    for i in range(170):
        x = 420 + i * 1.5
        y = 96 + 20 * math.sin(i / 3.0) + 10 * math.sin(i / 7.0 + 1)
        pts.append(f"{x:.0f},{y:.0f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{TOP}" '
               f'stroke-width="1.8"/>')
    out.append(t(420, 58, "current through the pore", 12, INK))
    out.append(t(420, 142, "a neural network turns the squiggle into bases", 11.5, MUTE))
    out.append(t(40, 190, "Read length is simply how long the molecule was — so how you "
                          "pipette becomes how long your reads are.", 14, INK))
    out.append(t(40, 214, "Modified bases change the current too, so they can be called "
                          "from the same signal, with no conversion step.", 13.5, OK))
    return svg(700, 234, "".join(out))


def fig_ont_kits():
    out = [t(40, 26, "Three ways to attach the motor adapter.", 14, INK)]
    rows = [("ligation", "end-repair, dA-tail, ligate the adapter",
             "best yield and read length; most handling", OK),
            ("rapid", "a transposase inserts the adapter sequence",
             "ten minutes, but tagmentation cuts the DNA", HOT),
            ("ultra-long", "very gentle, very high molecular weight input",
             "reads in the hundreds of kilobases", TOP)]
    for i, (name, how, trade, col) in enumerate(rows):
        y = 62 + i * 46
        out.append(t(60, y, name, 13.5, col, weight="bold"))
        out.append(t(170, y, how, 12.5, INK))
        out.append(t(170, y + 17, trade, 11.5, MUTE))
    out.append(t(40, 212, "Whatever the route, the molecule ends up with a motor protein on "
                          "one end — that end goes into the pore first.", 14, INK))
    out.append(t(40, 236, "Barcodes are ligated before the motor adapter, so a barcode is "
                          "read at the start of every read.", 13.5, MUTE))
    return svg(700, 256, "".join(out))


def fig_platform_compare():
    out = [t(40, 26, "What each platform is actually good at.", 14, INK)]
    x0, y0, w, h = 90, 56, 420, 150
    out.append(line(x0, y0 + h, x0 + w, y0 + h, MUTE, 1.2))
    out.append(line(x0, y0, x0, y0 + h, MUTE, 1.2))
    out.append(t(x0 + w / 2, y0 + h + 36, "read length  →", 12.5, MUTE, anchor="middle"))
    out.append(t(x0 - 12, y0 + 8, "accuracy", 12.5, MUTE, anchor="end"))
    out.append(t(x0 - 12, y0 + 24, "↑", 12.5, MUTE, anchor="end"))
    pts = [("Illumina", 0.10, 0.80, TOP), ("MGI", 0.16, 0.82, TOP),
           ("AVITI", 0.13, 0.90, TOP), ("Ultima", 0.09, 0.66, MUTE),
           ("PacBio HiFi", 0.62, 0.93, OK), ("Nanopore", 0.92, 0.58, HOT)]
    for name, fx, fy, c in pts:
        px, py = x0 + fx * w, y0 + h - fy * h
        out.append(dot(px, py, 6, c))
        out.append(t(px, py - 14, name, 11.5, c, anchor="middle"))
    out.append(t(x0 + 10, y0 + h + 18, "150 bp", 11, MUTE))
    out.append(t(x0 + w - 10, y0 + h + 18, "100 kb +", 11, MUTE, anchor="end"))
    out.append(t(40, 248, "There is no best platform. There is a question, a sample, and a "
                          "budget — and those pick the platform.", 14, INK))
    out.append(t(40, 272, "Positions here are schematic, and they move every year.", 12.5, MUTE))
    return svg(700, 292, "".join(out))


def fig_error_profiles():
    out = [t(40, 26, "Each platform fails in its own way.", 14, INK)]
    rows = [("Illumina / MGI / AVITI", "substitutions, rising with cycle number", 0.9, TOP),
            ("Ultima", "homopolymer length: AAAAA read as AAAA", 0.5, MUTE),
            ("PacBio HiFi", "few, random, mostly indels — and consensus removes them", 0.95, OK),
            ("Nanopore", "indels, worst in homopolymers; improving each chemistry", 0.6, HOT)]
    for i, (name, how, acc, col) in enumerate(rows):
        y = 62 + i * 44
        out.append(t(56, y, name, 13, col, weight="bold"))
        out.append(t(56, y + 18, how, 11.5, MUTE))
        bx = 330
        out.append(f'<rect x="{bx}" y="{y-11}" width="200" height="12" fill="#eceff1"/>')
        out.append(f'<rect x="{bx}" y="{y-11}" width="{200*acc:.0f}" height="12" '
                   f'fill="{col}" opacity="0.8"/>')
    out.append(t(330, 44, "accuracy of a single raw read", 11.5, MUTE))
    out.append(t(40, 246, "This decides whether you need UMIs or consensus reads, and "
                          "whether a variant call can be trusted.", 14, INK))
    out.append(t(40, 270, "A library cannot fix a platform's error mode — but it can give "
                          "you a second copy of the molecule to check against.", 13.5, MUTE))
    return svg(700, 290, "".join(out))


FIGURES = {
    "nucleic-acids": [
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
    ],
    "sequencers": [
        ("sanger", fig_sanger),
        ("universal-ends", fig_universal_ends),
        ("flowcell", fig_flowcell),
        ("bridge", fig_bridge),
        ("linearise", fig_linearise),
        ("sbs", fig_sbs),
        ("read-order", fig_read_order),
        ("pe-turnaround", fig_pe_turnaround),
        ("i5-orientation", fig_i5_orientation),
        ("readthrough", fig_readthrough),
        ("index-hopping", fig_index_hopping),
        ("diversity", fig_diversity),
        ("dnbseq", fig_dnbseq),
        ("other-shortread", fig_other_shortread),
        ("smrtbell", fig_smrtbell),
        ("zmw", fig_zmw),
        ("ccs", fig_ccs),
        ("nanopore", fig_nanopore),
        ("ont-kits", fig_ont_kits),
        ("error-profiles", fig_error_profiles),
        ("platform-compare", fig_platform_compare),
    ],
}

if __name__ == "__main__":
    for unit, figs in FIGURES.items():
        for i, (name, fn) in enumerate(figs, start=1):
            write(unit, "fig%02d-%s.svg" % (i, name), fn())
    if PROBLEMS:
        print("\ntext leaves the canvas:")
        print("\n".join(PROBLEMS))
        raise SystemExit(1)
