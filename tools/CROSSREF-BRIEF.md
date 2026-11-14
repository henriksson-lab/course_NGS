# How to cross-reference a unit

The units of this course were written independently and in parallel. They are correct on
their own, but they do not yet point at each other, so the course reads as 29 separate
documents rather than one argument. This pass fixes that.

Read `index.qmd` first: it is the map of the whole course, and the only place where every
unit is described in one screen. Read `CURRICULUM.md` for the intent behind the parts.

## The spine

The course has one organising idea: **a protocol is an assembly of blocks**.

- **Part A** (foundations) gives the vocabulary. Everything else may point back to it.
- **Part B** (building blocks) teaches each step on its own.
- **Part C** (use cases) assembles blocks into real protocols. *Every Part C unit must point
  back to the Part B blocks it uses* — that is what makes the spine visible.
- **Part D** (tricks) is indexed by problem. Tricks named in A–C should point into it, and
  its entries should point back at the units where the trick is used.
- **Part E** (QC and design) is where a student judges whether the thing worked.

## What to add

Two kinds of link, both in the deck (`lec*.qmd`):

**1. Inline, where a concept is used but taught elsewhere.** One link, in the flow of the
slide, when the reader would otherwise need knowledge this deck does not give:

```
Tn5 leaves a 9 nt gap that must be filled before amplification
([end chemistry](../end-chemistry/lec.qmd)).
```

Add these only where they earn their place — a reader who followed the link would genuinely
understand the slide better. Three to eight per deck is typical. Do not turn the prose into a
field of links, and never link the same target twice in one deck.

**2. A closing slide, `## Where this connects`.** The last slide of every deck. Group the
links and say *why* each matters in a few words — a bare list of unit names is of no use:

```
## Where this connects

**Blocks this protocol uses**

- [Fragmentation](../fragmentation/lec.qmd) — sets the insert size the sequencer needs
- [End chemistry](../end-chemistry/lec.qmd) — why A-tailing comes before ligation

**If this fails**

- [QC](../qc/lec.qmd) — the trace that tells you the ligation did not work
```

Pick headings that suit the unit: *Blocks this protocol uses*, *Where these blocks are used*,
*Before this*, *If this fails*, *Tricks that apply here*. Four to eight links.

## Rules

- Links are **relative paths between unit folders**: `../unit/lec.qmd`, and for a second deck
  `../unit/lec-name.qmd`. Check the target file exists. Quarto rewrites `.qmd` to `.html`.
- **Only link a target that genuinely covers the point.** If you are unsure what another unit
  says, read it. A wrong cross-reference is worse than none, because it sends a reader away
  for an answer that is not there.
- Do **not** rewrite the teaching content. This pass adds links and one slide. If you find a
  real error, leave the text alone and report it instead.
- Do **not** edit `index.qmd`, `_quarto.yml`, `CURRICULUM.md`, another worker's units, or any
  `readings.qmd` / `exercise.qmd`. Do not run `git`.
- A deck should stay near **30 slides** (soft: reported, not enforced) and at least **half**
  its slides must carry a figure (enforced). Your new slide is a text slide, so check the
  ratio still passes; if a deck is already at the guideline, prefer putting the connections on
  the existing final slide to pushing it over.
- `python3 tools/check_course.py` must print OK before you finish.

## Watch for

Units written in parallel sometimes overlap. Where two decks cover the same ground at
different depths, the cross-reference should make the division explicit ("the end states are
introduced in [nucleic acids]; here we use them"), not pretend the overlap is absent. If two
units genuinely duplicate each other, report it rather than fixing it yourself.

Report: which decks you touched, how many inline links and what the closing slides say, any
cross-reference you wanted to make but could not, and any overlap or error you found.
