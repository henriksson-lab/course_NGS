#!/usr/bin/env python3
"""Check course material against the rules in CURRICULUM.md.

  - a deck has at most 30 slides
  - at least half of its content slides carry a picture
  - a picture never sits on a slide of its own: it must have text beside it
  - every referenced image file exists
  - exercise pages use collapsible Hint / Solution callouts

Run from anywhere:  python3 tools/check_course.py
Exits 1 if any rule is broken, so it can gate a commit.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = ["foundations", "blocks", "usecases", "tricks", "qc", "design"]
MAX_SLIDES = 30
MIN_IMAGE_FRACTION = 0.50

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


def text_of(slide):
    """Slide text with the heading, image markup and attributes removed."""
    s = IMG.sub("", slide)
    s = re.sub(r"^## .*$", "", s, flags=re.M)
    s = re.sub(r"\{[^}]*\}", "", s)
    s = re.sub(r":::.*$", "", s, flags=re.M)
    return s.strip()


def check_deck(path, problems):
    text = open(path).read()
    rel = os.path.relpath(path, ROOT)
    sl = slides(text)
    n = len(sl) + 1  # + title slide
    withimg = [s for s in sl if images_in(s)]
    frac = len(withimg) / len(sl) if sl else 0

    if n > MAX_SLIDES:
        problems.append(f"{rel}: {n} slides, limit is {MAX_SLIDES}")
    if frac < MIN_IMAGE_FRACTION:
        problems.append(f"{rel}: {frac:.0%} of slides have a picture, "
                        f"minimum is {MIN_IMAGE_FRACTION:.0%}")
    for s in withimg:
        if len(text_of(s)) < 40:
            head = s.split("\n")[0][:60]
            problems.append(f"{rel}: picture-only slide '{head}' — "
                            f"a picture must share its slide with text")
    for s in sl:
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
    problems, lines = [], []
    for part in PARTS:
        for sub, fn in (("lectures", check_deck), ("exercises", check_exercises)):
            d = os.path.join(ROOT, part, sub)
            if not os.path.isdir(d):
                continue
            for name in sorted(os.listdir(d)):
                if not name.endswith(".qmd"):
                    continue
                path = os.path.join(d, name)
                if sub == "lectures" and "revealjs" not in open(path).read():
                    lines.append(f"{os.path.relpath(path, ROOT)}: page (not a deck)")
                    continue
                lines.append(fn(path, problems))

    for ln in lines:
        print("  " + ln)
    if problems:
        print("\nFAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("\nOK — %d files" % len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
