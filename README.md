# NGS library preparation — course materials

Quarto site for a course on next-generation sequencing (NGS) library preparation.
Scaffold copied from the 5MO115 *Bioinformatics and genome analysis* course.

## Layout

- `index.qmd` — landing page, links to every module
- `CURRICULUM.md` — the plan for the whole course, and the decisions behind it (repo-only)
- `foundations/`, `blocks/`, `usecases/`, `tricks/`, `qc/`, `design/` — the five parts, each
  with `lectures/` (revealjs decks and reading pages), `exercises/` and `img/`
- `planning/` — concept inventory from the protocol collection, and `protocol_links.tsv`
  mapping every protocol to its NGS 101 page (repo-only)
- `tools/make_figures.py` — generates the conceptual SVG figures
- `tools/check_course.py` — enforces the material rules

## Build

```
make          # render every .qmd to .html next to it
make check    # enforce the deck rules (slide count, picture ratio, no code)
make figures  # regenerate the conceptual SVG figures
make site     # full quarto render into _site/
make preview  # live preview
make add      # stage everything needed for a deploy commit
```

## Slides

Use revealjs with the shared theme:

```
---
title: "..."
format:
    revealjs:
        theme: [serif, ../../custom.scss]
---
```

Save to PDF from the browser: print, landscape, no margins, background graphics on.

## Rules for the material

- No programming. Exercises are design questions, quizzes and enzyme-selection tasks.
- A deck is at most 30 slides, and at least half of them carry a picture — always alongside
  text, never a picture on its own slide. `make check` enforces this.
- All examples are framed in human biology.
- Every method named cites its original paper; protocols link to their
  [NGS 101](https://henriksson-lab.github.io/NGS_101/) page.
- Figures are generated as SVG by `tools/make_figures.py`, which asserts that every drawn
  duplex actually base-pairs.
