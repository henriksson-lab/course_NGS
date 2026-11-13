# How to build a unit

Contract for anyone (human or agent) adding a unit to this course. Follow it exactly: the
units are written independently and must come out looking like one course.

Read `CURRICULUM.md` for what the unit must cover, and `AUDIENCE.md` for who it is for.
`nucleic-acids/` and `sequencers/` are the worked examples — copy their shape.

## What a unit is

One folder at the repository root, named after the unit in kebab-case:

```
<unit>/lec.qmd          the slide deck (a second deck, if needed, is lec-<something>.qmd)
<unit>/readings.qmd     the reading list
<unit>/exercise.qmd     exercises
<unit>/make-figs.py     generates that unit's figures
<unit>/figNN-*.svg      the generated figures (committed)
```

Do **not** touch `_quarto.yml`, `index.qmd`, `CURRICULUM.md`, or any other unit's folder —
the sidebar order and the cross-links are added in a separate pass. Do not run `git`.

## The deck

YAML, verbatim apart from the title and subtitle:

```yaml
---
title: "<unit title>"
subtitle: "<Part> · NGS library preparation"
author: "Johan Henriksson"
format:
  revealjs:
    theme: [simple, ../theme.scss]
    slide-number: c/t
    width: 1280
    height: 720
    transition: none
    history: false
    highlight-style: github
    code-overflow: wrap
    code-line-numbers: false
    incremental: false
    chalkboard: false
    menu: true
    html-math-method: katex
---
```

Rules, all enforced by `python3 tools/check_course.py`:

- **At most 30 slides.** A slide is a `##` heading. Aim for 20–26.
- **At least half the slides carry a figure**, and every figure shares its slide with text —
  never a figure on a slide of its own.
- **Nothing is clipped.** The checker estimates the height of each figure slide against the
  720 px box and fails if the content would overflow. Shorten bullets or shrink the figure.
- Reference a figure as `![](figNN-name.svg){width=NN%}`. Pick the width so the rendered
  height is about 360 px: `width% ≈ 360 / natural_height × natural_width / 1280 × 100`.
- Cite the source paper for anything you name, inline, small:
  `[Author et al. 2014, doi:10.xxxx/yyyy]{.small}`

Write for late MSc and PhD students. Lead with the molecule and what physically happens to
it. Explain why a step exists by showing what fails without it. Prefer a worked example over
a list. No programming anywhere.

## Figures

`<unit>/make-figs.py` imports the shared library and calls `build`:

```python
#!/usr/bin/env python3
"""Figures for the <unit> unit.  Run: python3 <unit>/make-figs.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from figlib import *  # noqa: F401,F403


def fig_example():
    out = [t(40, 26, "A lead line in the figure", 14, INK)]
    b, w = duplex(60, 60, "ATGCTTAG", "TACGAATC", labels=False)
    out.append(b)
    out.append(t(40, 150, "What this shows.", 14, INK))
    return svg(600, 180, "".join(out))


build(__file__, [
    ("example", fig_example),
])
```

`build` numbers the files in slide order. Read `tools/figlib.py` for the primitives:
`svg t seq line duplex pairs arrow box dot vtick check_pairing` and the colours
`INK TOP BOT HOT OK BAD MUTE`. Notes:

- Figures are **conceptual diagrams that explain a mechanism**, not decoration and not
  photographs. Draw the molecule, the enzyme's action, the failure mode.
- `duplex()` asserts that the two strands actually base-pair — a wrong duplex raises.
- The canvas auto-widens to fit labels; labels that still escape raise an error.
- Keep a figure under ~300 px tall and about 2–4 times wider than tall.
- No external images, no network, standard library only.

## Readings

`readings.qmd`, with only a `title:` in the YAML (the project supplies the format).

- 4–8 entries, each with author, year, title, journal and a resolving DOI link.
- One or two sentences under each saying *why it is there* and what to look for.
- Mark one or two **start here**.
- **Every DOI must be verified** before you write it down:
  `curl -s -A "course-check/1.0" https://api.crossref.org/works/<doi> | head -c 300`
  If the title that comes back is not the paper you meant, the DOI is wrong: find the right
  one or drop the entry. Never write a DOI from memory.
- Close with a short "Reference material to keep open" section where it helps.

## Exercises

`exercise.qmd`, with only a `title:` in the YAML.

- 6–12 problems, grouped under `#` part headings.
- **No code.** These are design problems, reasoning problems and calculations done by hand.
- Each problem gets a collapsible solution, and a hint where it helps:

```
::: {.callout-tip collapse="true" appearance="minimal"}
## Hint
...
:::

::: {.callout-note collapse="true" appearance="minimal"}
## Solution
...
:::
```

- Favour these kinds: *design this step*; *why does this step exist*; *what went wrong, given
  this observation*; *pick the enzyme and say which property decides it* (students should use
  vendor selection charts, e.g. NEB's); *a trap where an unwanted activity ruins the result*.
- End with a short `# Self-check` list of questions and one collapsed `## Answers`.

## Scope and style

- **Human and mammalian biology throughout.** Where a method was first published in bacteria
  or viruses, teach the underlying step with a human application instead.
- Protocols named in the text should be ones in the collection at
  `~/github/chem` — `planning/protocol_links.tsv` maps every protocol to its page on
  <https://henriksson-lab.github.io/NGS_101/>, with a citation count you can use to pick the
  ones worth naming. Link to that page the first time a protocol appears.
- British spelling, plain words, no exclamation marks, no "simply" or "just".
- Say what is uncertain rather than inventing a number. If you cannot verify a claim about a
  protocol, check its notes in `~/github/chem/<protocol-dir>/*.md` or leave the claim out.

## Before you finish

```
python3 <unit>/make-figs.py     # must exit 0
python3 tools/check_course.py   # must print OK
```

Report: the unit folder, the slide count and figure ratio, which DOIs you verified, and
anything you were unsure about.
