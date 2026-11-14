#!/usr/bin/env python3
"""Find text that collides with other text, or runs off the canvas, in the figures.

figlib's lint() catches text leaving the canvas but not two labels landing on top of each
other, so that fault stayed invisible to the quality gates until a reader hit it.

ADVISORY, not a gate. Glyph widths are estimated from the font size, so the boxes are
approximate and a short string sitting above a long one ("A" over a caption) is reported
when nothing is wrong. Render the figure and look before changing it.

  python3 tools/check_overlap.py

Known false positives, each checked by rendering and looking (2026-11-14):

  chemistry-to-sequence/fig20-antibody.svg   antibody glyphs sit clear below the label
  rna/fig17-riboconstruct.svg                heading ends well short of the cDNA circle
  sequencers/fig05-linearise.svg             two separate lines; only the descenders are close
  handles/fig17-topo-recomb.svg              no longer referenced by any slide

A new name in the output is worth looking at. These four are not.
"""
import re, glob, sys, html
TXT = re.compile(r'<text([^>]*)>(.*?)</text>', re.S)
def attr(a, n, d=None):
    m = re.search(r'\b%s="([^"]*)"' % n, a)
    return m.group(1) if m else d
def boxes(path):
    s = open(path).read()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    W, H = (float(vb.group(1)), float(vb.group(2))) if vb else (0, 0)
    out = []
    for a, body in TXT.findall(s):
        t = html.unescape(re.sub(r'<[^>]+>', '', body)).strip()
        if not t: continue
        x = float(attr(a, "x", 0)); y = float(attr(a, "y", 0))
        fs = float(attr(a, "font-size", "13").replace("px", ""))
        anc = attr(a, "text-anchor", "start")
        mono = "mono" in (attr(a, "font-family", "") or "").lower()
        w = len(t) * fs * (0.60 if mono else 0.50)
        x0 = x if anc == "start" else (x - w / 2 if anc == "middle" else x - w)
        out.append((x0, y - fs * 0.78, x0 + w, y + fs * 0.26, t))
    return W, H, out
def ov(a, b):
    ix = min(a[2], b[2]) - max(a[0], b[0]); iy = min(a[3], b[3]) - max(a[1], b[1])
    if ix <= 0 or iy <= 0: return 0.0
    return ix * iy / min((a[2]-a[0])*(a[3]-a[1]), (b[2]-b[0])*(b[3]-b[1]))
bad = []
for f in sorted(glob.glob("*/fig*.svg")):
    W, H, bs = boxes(f)
    for i in range(len(bs)):
        for j in range(i+1, len(bs)):
            r = ov(bs[i], bs[j])
            if r > 0.18:
                bad.append((f, round(r,2), bs[i][4][:34], bs[j][4][:34]))
        if W and (bs[i][0] < -1 or bs[i][2] > W + 1):
            bad.append((f, "offcanvas", bs[i][4][:46], ""))
seen=set(); uniq=[]
for b in bad:
    if b[0] not in seen or b[1]=="offcanvas": uniq.append(b)
    seen.add(b[0])
print(len({b[0] for b in bad}), "figures with a problem,", len(bad), "instances\n")
for b in bad: print(" ", b[0], "|", b[1], "|", b[2], "||", b[3])
