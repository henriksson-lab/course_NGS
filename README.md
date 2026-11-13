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
make site     # render the whole site into _site/ (what CI runs)
make preview  # live preview, re-rendering as you edit
make check    # enforce the material rules (slide count, picture ratio, no code)
make figures  # regenerate the conceptual SVG figures
make clean    # remove _site/ and .quarto/
```

No HTML is committed. `.github/workflows/pages.yml` renders the site on every push
to `main` and publishes it to
[henriksson-lab.github.io/course_NGS](https://henriksson-lab.github.io/course_NGS/).
The workflow runs `make check` and verifies the checked-in figures still match
`tools/make_figures.py` before it publishes, so a broken deck never reaches the site.
Only `_site/` is published: `CURRICULUM.md`, `planning/` and `oldpres/` stay out of it.

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
