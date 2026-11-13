# NGS library preparation — course materials

Quarto site for a course on next-generation sequencing (NGS) library preparation.
Scaffold copied from the 5MO115 *Bioinformatics and genome analysis* course.

## Layout

- `index.qmd` — landing page, links to every module
- `moduleN/lectures/` — lecture / reading pages (and revealjs slide decks)
- `moduleN/exercises/` — exercise pages with collapsible Hint / Solution callouts
- `AUDIENCE.md` — who the course is for; read before writing material

## Build

```
make          # render every .qmd to .html next to it
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
