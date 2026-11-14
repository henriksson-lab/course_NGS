# Audit: whole examples, and how fast concepts arrive

This course was written one unit at a time, by different authors, against a brief that said
what each unit must *contain*. Nothing checked what it is like to **read it in order**, as a
student meeting most of this for the first time.

The concern, in the course owner's words: a deck can become "a lot of randomly connected
material". A student needs **whole examples to pin the steps to**. A mechanism taught on its
own, correct and well drawn, is still hard to hold on to if the reader never sees it doing a
job inside a complete, named protocol from sample to sequence.

This is an **audit, not a rewrite**. Do not edit any `.qmd`, `.py` or `.svg` file. Do not run
git. Produce findings.

## What to judge

Read your decks the way a late-MSc student would: in the course order, once, without
stopping to look things up. `index.qmd` gives the order and the whole map.

**1. Is there a whole example?** For each deck, find the longest *continuous* worked example:
one named, real protocol or one molecule followed from start to finish through consecutive
steps. Say what it is and how many slides it spans, or say there is none. A list of six
methods each illustrated by one slide is **not** a whole example. A worked numerical
calculation is not one either, unless the molecule is followed through the steps.

**2. How many new concepts arrive, and how fast?** Count the terms a deck introduces that a
student would not already have from the earlier units (use the course order in `index.qmd`;
assume a solid molecular-biology background but no library-prep experience). Report:

- the count for the deck, and the three densest slides with their counts
- any slide introducing **more than about four** new terms at once
- terms **used before they are explained** — either earlier in the same deck, or taught in a
  later unit with no signposting. These are the worst offenders, so list every one with its
  file and line.

**3. Is there a spine?** Does the deck return to one running example, or does each slide
start somewhere new? Note where a deck changes subject without a transition.

**4. Where would one example fix several problems at once?** This is the most useful thing
you can report. Name the protocol you would run through the deck as its backbone, say which
existing slides it would tie together, and what it would replace.

## Weighting

Be hardest on the early material. A student meets most of the vocabulary in the first few
units, and a concept dropped unexplained there costs them for the rest of the course. Later
use-case decks can assume more, and should — flag it if they *re-explain* something instead.

## Report

Per deck: slide count; the whole example (or none); new-concept count and the three densest
slides; every use-before-explained term with file and line; and your single best
recommendation. End with the three changes across your whole set that you judge most
valuable, ranked, with a sentence each on the cost of making them.

Be concrete and quote slide headings. "Could be clearer" is not a finding. If a deck is in
good shape, say so plainly and briefly — do not invent problems to fill a report.
