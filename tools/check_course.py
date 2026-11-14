#!/usr/bin/env python3
"""Check course material against the rules in CURRICULUM.md.

  - a deck is at most 30 slides (a soft ceiling: over it warns, it does not fail)
  - at least half of its content slides carry a picture
  - a picture never sits on a slide of its own: it must have text beside it
  - every referenced image file exists
  - exercise pages use collapsible Hint / Solution callouts

Run from anywhere:  python3 tools/check_course.py
Exits 1 if any rule is broken, so it can gate a commit.
"""
import math
import os
import struct
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"tools", "planning", "oldpres", "docs", "img", ".git", ".quarto", ".github"}
SOFT_MAX_SLIDES = 30   # a guideline, reported but not enforced
MIN_IMAGE_FRACTION = 0.50

# revealjs slide box and type scale, read from the generated quarto theme:
#   theme.scss: $presentation-font-size-root 24px, $presentation-h2-font-size 1.7em,
#   deck YAML: width 1280, height 720
SLIDE_W, SLIDE_H = 1280.0, 720.0
BODY_PX, HEAD_EM, SMALLER = 24.0, 1.7, 0.8
CHAR_W = 0.50          # average glyph width as a fraction of font size
LINE_H = 1.25

IMG = re.compile(r"!\[[^\]]*\]\(([^)]+?)(?:\s+\"[^\"]*\")?\)|<img[^>]+src=\"([^\"]+)\"")


def slides(text):
    """Split a revealjs document body into slides at '## ' headings."""
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    out, cur = [], []
    for ln in body.split("\n"):
        if ln.startswith("## "):
            if cur:
                out.append("\n".join(cur))
            cur = [ln]
        elif cur:
            cur.append(ln)
    if cur:
        out.append("\n".join(cur))
    return out


def images_in(s):
    return [m.group(1) or m.group(2) for m in IMG.finditer(s)]


def svg_size(path):
    """Natural size of a figure or photo, so the height estimate covers both."""
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        return raster_size(path)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(path).read())
    return (float(m.group(1)), float(m.group(2))) if m else None


def raster_size(path):
    """PNG and JPEG dimensions from the header, without an image library."""
    with open(path, "rb") as fh:
        head = fh.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return (float(w), float(h))
        if head[:2] == b"\xff\xd8":
            fh.seek(2)
            while True:
                b = fh.read(1)
                while b and b != b"\xff":
                    b = fh.read(1)
                while b == b"\xff":
                    b = fh.read(1)
                if not b:
                    return None
                marker = b[0]
                size = struct.unpack(">H", fh.read(2))[0]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">HH", fh.read(5)[1:])
                    return (float(w), float(h))
                fh.seek(size - 2, 1)
    return None


def estimate_height(slide, qmd_dir):
    """Rough height of a slide's content in slide coordinates.

    revealjs does not shrink overflowing content, it clips it, and this course cannot
    rely on a browser being available to check. The estimate is deliberately crude:
    it exists to catch gross overflow, not to be exact.
    """
    smaller = ".smaller" in slide.split("\n")[0]
    scale = SMALLER if smaller else 1.0
    body = BODY_PX * scale
    head = BODY_PX * HEAD_EM * scale
    total = 0.0

    heading = re.sub(r"\{[^}]*\}", "", slide.split("\n")[0][3:]).strip()
    total += max(1, math.ceil(len(heading) / (SLIDE_W / (head * CHAR_W)))) * head * LINE_H + 20

    for src in images_in(slide):
        if src.startswith(("http", "data:")):
            continue
        pct = 100.0
        m = re.search(re.escape(src) + r"\)\{width=(\d+)%", slide)
        if m:
            pct = float(m.group(1))
        size = svg_size(os.path.join(qmd_dir, src))
        if size:
            w = SLIDE_W * pct / 100.0
            total += w / size[0] * size[1] + 24

    for ln in slide.split("\n")[1:]:
        t = ln.strip()
        if not t or t.startswith(("![", ":::", "<img")):
            continue
        font = body * 0.58 if t.startswith("[") and "{.small}" in t else body
        t = re.sub(r"\{[^}]*\}|[*`\[\]]|^[-|] ", "", t)
        if not t.strip():
            continue
        total += max(1, math.ceil(len(t) / (SLIDE_W / (font * CHAR_W)))) * font * LINE_H
    return total


def text_of(slide):
    """Slide text with the heading, image markup and attributes removed."""
    s = IMG.sub("", slide)
    s = re.sub(r"^## .*$", "", s, flags=re.M)
    s = re.sub(r"\{[^}]*\}", "", s)
    s = re.sub(r":::.*$", "", s, flags=re.M)
    return s.strip()


def check_deck(path, problems, notes):
    text = open(path).read()
    rel = os.path.relpath(path, ROOT)
    sl = slides(text)
    n = len(sl) + 1  # + title slide
    withimg = [s for s in sl if images_in(s)]
    frac = len(withimg) / len(sl) if sl else 0

    if n > SOFT_MAX_SLIDES:
        notes.append(f"{rel}: {n} slides, over the {SOFT_MAX_SLIDES}-slide guideline "
                     f"— fine if the deck earns it, but look for something to cut")
    if frac < MIN_IMAGE_FRACTION:
        problems.append(f"{rel}: {frac:.0%} of slides have a picture, "
                        f"minimum is {MIN_IMAGE_FRACTION:.0%}")
    for s in withimg:
        if len(text_of(s)) < 40:
            head = s.split("\n")[0][:60]
            problems.append(f"{rel}: picture-only slide '{head}' — "
                            f"a picture must share its slide with text")
    for s in sl:
        if images_in(s):
            h = estimate_height(s, os.path.dirname(path))
            if h > SLIDE_H:
                head = re.sub(r"\{[^}]*\}", "", s.split("\n")[0][3:]).strip()[:48]
                problems.append(f"{rel}: slide '{head}' is about {h:.0f}px of content "
                                f"in a {SLIDE_H:.0f}px slide — it will be clipped")
        for src in images_in(s):
            if src.startswith(("http://", "https://", "data:")):
                continue
            if not os.path.exists(os.path.join(os.path.dirname(path), src)):
                problems.append(f"{rel}: missing image file {src}")
    return f"{rel}: {n} slides, {len(withimg)}/{len(sl)} with a picture ({frac:.0%})"


def check_exercises(path, problems):
    text = open(path).read()
    rel = os.path.relpath(path, ROOT)
    hints = text.count("## Hint")
    sols = text.count("## Solution") + text.count("## Answers")
    if sols == 0:
        problems.append(f"{rel}: no Solution callouts")
    if 'collapse="true"' not in text:
        problems.append(f"{rel}: callouts are not collapsible")
    for word in ("```{r", "```{python", "```{bash"):
        if word in text:
            problems.append(f"{rel}: contains executable code ({word}) — "
                            f"this course has no programming exercises")
    return f"{rel}: {hints} hints, {sols} solutions"


def main():
    """One folder per unit at the repository root: lec*.qmd, readings.qmd,
    exercise.qmd, and the unit's figNN-*.svg files."""
    problems, notes, lines = [], [], []
    for unit in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, unit)
        if not os.path.isdir(d) or unit in SKIP or unit.startswith("."):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".qmd"):
                continue
            path = os.path.join(d, name)
            text = open(path).read()
            if name.startswith("lec"):
                if "revealjs" not in text:
                    problems.append(f"{unit}/{name}: a lec*.qmd must be a revealjs deck")
                    continue
                lines.append(check_deck(path, problems, notes))
            elif name.startswith("exercise"):
                lines.append(check_exercises(path, problems))
            else:
                lines.append(f"{unit}/{name}: page")

    for ln in lines:
        print("  " + ln)
    if notes:
        print("\nNOTE")
        for n in notes:
            print("  - " + n)
    if problems:
        print("\nFAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("\nOK — %d files" % len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
