# Refactor brief: reminders, cuts and relocations

Read `planning/refactor-plan.md` first for the whole picture, and `index.qmd` for the course
order. This brief is the part every worker must follow identically.

You are editing an existing course, not writing a new one. Most of your work is **removing**
and **moving**, not adding. If you find yourself writing new teaching content, stop and check
it against your assignment.

## The rules

**1. Part C assumes PCR.** By the time a student reaches a use case, PCR, index PCR, tailed
primers and what a cycle costs are long since taught and repeatedly used. Do not restate
them, not even as a reminder. The same goes for anything the student has used in several
earlier decks.

**2. Replace re-teaching with reminders, not deletions** — except where rule 1 applies, in
which case delete. A reminder is:

| Re-teach (cut) | Reminder (keep) |
|---|---|
| derives the mechanism again | states the conclusion needed *here* |
| repeats the worked numbers | names the result, links where it was worked |
| repeats the original citations | cites nothing; the owning deck holds them |
| has its own figure | no figure of its own |
| a full slide | two or three lines, usually folded into a neighbouring slide |

If a reminder runs past about three lines, or would make sense to someone who had not read
the owning deck, it has become a re-teach again.

**3. The course makes no recommendations.** State what a chemistry does, what it costs and
how it fails. Do not tell the reader what to use, what to avoid, or what to "read for the
idea rather than adopt". Kits and published methods differ in kind — say which is which where
it matters and let that stand on its own.

**4. Do not invent facts.** If a cut leaves a gap you cannot fill from material already in the
course, say so in your report rather than writing something plausible.

## Scope discipline

- Edit only the files named in your assignment. Other workers are editing other folders at
  the same time, and staging another worker's file corrupts the history.
- **Never run git.** Not status, not add, not commit.
- Do not touch `_quarto.yml`, `index.qmd`, `CURRICULUM.md` or `planning/`.
- Keep the voice: British spelling, plain words, no exclamation marks, no "simply" or "just".

## Quality gates

```
python3 <unit>/make-figs.py     # exits 0, for every unit whose figures you changed
python3 tools/check_course.py   # prints OK
```

- About 30 slides per deck — a soft ceiling, reported but not enforced — and at least half
  carrying a figure, which is enforced. **Cutting text slides raises the
  figure fraction, so cuts are safe; cutting a figure slide may not be.** Check.
- Nothing may exceed the 720px height estimate.
- If you remove a figure from a `make-figs.py` build list, every later figure is renumbered,
  which breaks every reference after it. Either leave the generator alone, or renumber the
  references and delete the stale SVG files. Leaving it alone is usually right: an unused
  figure costs nothing.

## Report

What you cut, what you turned into a reminder, what you moved, and the before/after slide
count per deck. Flag anything you were asked to cut that you judged load-bearing, and say
why — a wrong cut is harder to notice later than a wrong addition.
