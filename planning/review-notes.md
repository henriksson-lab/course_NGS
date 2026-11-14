# Review notes from the parallel unit build

Claims the unit authors flagged as unverified. Check these before the material is used.

## genomic-dna / targeted
- TruSeq PCR-free input "about 1–2 µg" written from memory; local notes only give
  100–500 ng (NEBNext FS PCR-free) and 1–500 ng (Illumina DNA Prep). Deck tells the
  reader to check the current guide.
- NEBNext PCR-free quantification method unconfirmed ("see guide" in the figure).
- Worked-example numbers labelled as assumptions: 20% library conversion efficiency,
  70% on-target capture, 90%/80% per-cycle PCR efficiency. GC-bias, damage-profile and
  error-floor plots labelled schematic.
- RRBS: "filled-in cytosine at the cut site cannot be scored" is from the author's own
  knowledge, not from the collection notes.
- Cas9 enrichment + UMIs listed as "not standard" — unverified.
- CAPP-Seq "later versions added molecule tags" carries no citation.

## handles / end-chemistry
- MspI fill-in geometry and the claim that the filled-in cytosine loses its methylation
  state are the author's own inference; slide note says to check the dNTP mix in Gu 2011.
- MNase / RNase A / alkali end states cited to no primary paper (standard enzymology).
- Cas9 end-masking rests on RGEN-seq notes; nothing confirmed for SITE-Seq.
- CEL-Seq handle order only partly stated, because the exact order was unverified.
- handles E5 (adapter dimer) and E7 (template-switching artefacts) give plausible rather
  than verified causes; end-chemistry E3 hedged on non-A tailing.
- Figures: the Tn5 mechanism and circularisation figures are the roughest; worth redrawing.
- Deliberate overlap with nucleic-acids/ on end states, nick/gap and A-tailing — check in
  the cross-reference pass that the depth difference is clear rather than repetitive.

## selection / barcodes-umis
- Colour-balance rule ("each cycle needs some red and some green in the pool") is a rule of
  thumb; deck points the reader at the instrument's index guide.
- The "distance fine, colour poor" barcode set is TruSeq-style and chosen deliberately; the
  balanced set was found by random search. Distances and collision rates are computed in
  make-figs.py, not quoted.
- Drop-seq 12 nt barcode + 8 nt UMI not checked against the collection notes; the
  28/10/10/90 read structure was copied from the sequencers deck, not a 10x manual.
- CAPP-Seq panel size "roughly a hundred kilobases" is hedged from memory.
- Nuclei hashing attributed to sci-Plex — wording worth checking.
- DSN and physical-selection figures are schematic.

## rna / long-reads
- RNA class shares (rRNA ~80%, tRNA ~10%, mRNA 1-5%) labelled approximate.
- Ribo-seq 2009 vs later linker chemistry (poly(A) tailing vs pre-adenylated linker) from
  the author's memory.
- "Tn5 prefers some sequences" caveat from memory.
- Unconfirmed vendor detail, flagged on the slides: how USER acts in NEBNext Directional,
  and how excess 3' adapter is removed in NEBNext small RNA.
- Nanopore cDNA-PCR PCS114 drawn per the ~/github/chem notes (adapter ligation to the
  poly(A) tail, then RT and strand switching) — differs from older VN-primer descriptions.
- Ultra-long cut densities and shearing break counts are schematic; adaptive-sampling
  exercise timings are invented and stated as such in the problem.
- Payne 2021 and Al'Khafaji 2024 cited by print year; Crossref "issued" is the earlier
  online year.
- NOTE: this worker rejected three of its own first-guess DOIs after Crossref returned
  different papers — evidence the verification step is doing real work.

## chemistry-to-sequence / compartments
- Semi-permeable capsules: no primary human-cell paper verified; slide cites only
  Clark 2023 and keeps claims general.
- Readings author lists written from memory (titles/journals/volumes from Crossref).
- Kang et al. cited as 2018 (print) vs Crossref online 2017.
- EM-seq is absent from planning/protocol_links.tsv, so that slide has no NGS 101 link.
- RRBS "2% of the genome" is an assumption for the arithmetic, not a measurement.
- Compartment "cells per run" ranges are orders of magnitude, flagged on the slide.
- Dropped a Jao & Salic EU click citation after Crossref returned a different paper.
- Poisson numbers (90.5% / 9.05% / 0.47% at lambda 0.1, 10.7% split-pool collisions)
  were hand-checked by the author; worth one independent check.

## chromatin / 3d-genome
- "About 10,000 loops" (Rao 2014) and "~20 bp tag" (Boyle 2008) are from the author's
  knowledge / collection notes, not the papers.
- DamID DpnI/DpnII logic is the author's own reasoning; footprint-bias caveat hedged.
- "Some protocols strip biotin from unligated ends" names no protocol — unverified.
- Crosslinker order (DSG before formaldehyde in ChIP, after in Micro-C) stated as
  "depending on the protocol".
- Calling cards: only the yeast Ty5 page exists in the collection; deck cites Wang 2012
  mammalian piggyBac and says so.
- Non-human examples retained with a note: GAM (mouse ES cells), DAP-seq (Arabidopsis).
- mtDNA / restriction-fragment / SPRITE-collision / GAM exercise arithmetic uses stated
  illustrative assumptions; SPRITE and Hi-C maths hand-checked.
- Four wrong DOIs caught and replaced by this worker (Zhao 4C, Schones, Fudenberg, DamID).

## fragmentation / amplification
- QUESTION FOR THE AUTHOR: "bottleneck dilution" in CURRICULUM.md was ambiguous. Taught as
  shear-point lengths acting as free molecule labels (Gillet 2011, Berry 2012), with
  dilution keeping molecule count below the number of possible lengths. Confirm intent.
- SPRI cut-offs in the curve figure (0.6x ~520 bp, 0.8x ~300 bp) are illustrative and
  labelled; the PEG arithmetic assumes a 20% PEG bead stock, stated as an assumption.
- Cycle-budget bars, HMW-handling bars and the Tn5 gel are schematic and labelled.
- No specific nicking enzymes named (could not verify).
- "Family B polymerases stall at template uracil" is uncited textbook knowledge; slide
  tells students to check the datasheet.
- From memory: small-RNA 145 bp product vs 120 bp dimer; MNase leaving 5'-OH/3'-P; MmeI
  and EcoP15I cut offsets.
- Non-human original methods cited but taught with human applications: Potter & Luo (fly),
  Ochman (fly), Quick (viral), Walker (bacterial).
- Two wrong DOIs from memory (Dean 2002, Dressman 2003) caught and replaced.

## spatial / screens
- Spot/bead sizes from memory of the papers, not the collection notes: Visium 55 um spot,
  Slide-seq 10 um bead, HDST 2 um bead, Stereo-seq 0.5 um pitch, DBiT-seq 10-50 um.
- Visium FFPE probe-pair chemistry from general knowledge, not the notes.
- lentiCRISPR v1/v2 diagram follows the notes (cPPT position) but full vector maps unchecked.
- Perturb-seq barcode-proxy / direct-capture diagram is schematic, from the notes.
- "Number of distinct shear positions gives a rough measure of clone size" is uncited.
- STARR-seq and splinkerette were first published in Drosophila; decks say so and teach only
  the transferable logic.
- Moffat protocol has no DOI; cited by name with its protocol page link.
- Dropped Wang 2007 (10.1101/gr.6286107) — Crossref returned not found.

## tricks / qc / design
- Author lists and page ranges written from memory (Crossref confirmed first author, title,
  journal, year only). Kircher cited as 2011 on slides and 2012 in readings — pick one.
- SPRI retention curves and cut-offs (0.6x above ~500 bp, 0.8x above ~250 bp) are schematic
  and labelled, with advice to calibrate against a ladder.
- Illustrative sequences from memory: TruSeq D701/D501 indexes (ATTACTCG, TATAGCCT) and the
  adapter sequences in the Annotate/Anneal/Sample-sheet demo mock-ups (labelled illustration,
  not screenshots).
- scifi-RNA-seq cited as the bioRxiv preprint from the protocol table.
- Three tricks figures exceed the 2-4x aspect guidance (fig05-splint 4.5, fig19 4.3,
  fig28 4.3); captions drive the width.
- Avoided eccDNA Circle-Seq (its DOI is a yeast paper) and made no claim about RNase H
  depletion kits.

## modifications / single-cell
- IMPORTANT DATA BUG: planning/protocol_links.tsv gives BD Rhapsody a DOI that is actually
  an organoid paper (Yoon 2018). Check the tsv for other mismatches; it was built by joining
  ours.tsv to citations.tsv without verification.
- EM-seq has no DOI in the tsv; Vaisvila 2021 (10.1101/gr.266551.120) verified directly.
- First HITS-CLIP DOI resolved to an unrelated paper; replaced with 10.1038/nature07488.
- Print vs online year used for Tsai 2015, Zubradt 2017, Rouskin 2014, GLORI (Liu 2023).
- Schematic figures: knee plot, barnyard scatter, Repair-seq outcome bars, replication-timing
  profile.
- Hedged claims from memory: miCLIP mutation one base 3' of the m6A; biotin-NTPs stopping
  the polymerase after one nucleotide in PRO-seq; RRBS fill-in removing the cut-site CpG;
  multiome barcodes linked but not identical; Drop-seq/10x bead loading behaviour.
- SPLiT-seq arithmetic corrected during the work: 48 x 96 x 96 = 442,368 (not 884,736).
- Mouse-first methods noted in the decks with human follow-ups: sci-RNA-seq3, SPLiT-seq,
  Microwell-seq.
- Part C subtitle used: "Use cases · NGS library preparation" — make consistent in the pass.
- This worker rendered its decks in Quarto: nothing clipped, but several slides sit close to
  the bottom edge, which the height estimate is too coarse to catch.

## Citation audit (course-wide, automated)

Every DOI appearing in any `.qmd` was fetched from Crossref and its author and year
compared against the surrounding text: **272 unique DOIs, 904 occurrences, none wrong.**
Script: `scratchpad/checkdoi.py` (not committed; re-runnable from the recipe below).

    grep -rhoE '10\.[0-9]{4,9}/[^ )]]"},;]+' --include=*.qmd .

Note for anyone repeating this: a naive DOI regex breaks on the two forms below, and both
produced false alarms the first time round.

- DOIs containing a bracket — `10.1016/S0021-9258(18)31688-0`, `10.1016/0378-1119(91)90480-Y`
  — get truncated at the `(` and then 404. All five such DOIs in the course are correct.
- Two-author citations, `[Rhee and Pugh 2011, ...]`, where a surname-before-year rule picks
  the second author and Crossref returns the first. Nine of these; all correct.

## Upstream data bug: BD Rhapsody's DOI

`planning/protocol_links.tsv` gives BD Rhapsody the DOI `10.1038/s41592-018-0255-0`, which
is "Reliability of human cortical organoid generation" (Nat Methods 2018). **The error is in
the `~/github/chem` catalogue, not in the join**: the protocol's directory name is
`bd-rhapsody__10.1038+s41592-018-0255-0`, so `ours.tsv` and the published NGS 101 URL both
carry it. Worth reporting to the collection.

For this course: the NGS 101 link works and stays; the DOI must not be cited. No unit cites
it — the citation audit above would have caught it.

Because the DOIs in that table were never verified upstream, **treat the whole `doi` column
as unverified**. Citation counts and NGS 101 URLs are fine; the DOIs are not a source.

## Scope: one non-human example

`screens/lec-readout.qmd:165` cites Potter and Luo 2010 for splinkerette PCR, a *Drosophila*
transposon-mapping paper. The chemistry is right and the method is used on human insertion
libraries, but the brief asks for a human application where one exists. Low priority.

## library-molecule: sequences checked, and what remains open

The worker wrote the Nextera sequences from memory and flagged them. All of them are
corroborated independently by the protocol collection, by `grep` over `~/github/chem`:

| sequence | what it is | entries in the collection |
|---|---|---|
| `AGATGTGTATAAGAGACAG` | Tn5 mosaic end | many |
| `TCGTCGGCAGCGTC` | Nextera Read 1 arm ("tail A" in the deck) | 173 |
| `GTCTCGTGGGCTCGG` | Nextera Read 2 arm ("tail B") | 161 |
| `AATGATACGGCGACCACCGAGATCTACAC` | P5 | 328 |
| `CAAGCAGAAGACGGCATACGAGAT` | P7 | 304 |
| `ACACTCTTTCCCTACACGACGCTCTTCCGATCT` | TruSeq Read 1 primer | 140 |

The reverse complements in the figures (`CTGTCTCTTATACACATCT`, `CCGAGCCCACGAGAC`) are correct,
and `make-figs.py` asserts the pairing anyway. The NGS 101 `annotate.html` and
`samplesheet.html` pages exist at the site root, so those links resolve.

Still open, both flagged by the worker and not resolved here:

- **"tail A" / "tail B" are the deck's own names**, not Illumina's. The deck says so. If
  anyone can confirm what S5 and S7 denote in the Illumina DNA Prep documentation, use the
  vendor's terms.
- **i7 orientation in the Read 1 read-through** is derived from strand logic, not checked
  against a vendor document. It is consistent with the sequences above but unverified.

## enzymes: no per-protocol NGS 101 links

The `enzymes/` worker looked for `~/github/chem/planning/protocol_links.tsv`; the table is at
`planning/protocol_links.tsv` inside *this* repository. It therefore linked only the NGS 101
root page, although Smart-seq2, RRBS, EM-seq and others are named in the text. Every other
unit links named protocols to their own page.

Fix after the cross-reference pass (that worker holds `enzymes/` now): add the per-protocol
links. The citation counts and URLs in the table are sound; only its `doi` column is not.

## enzymes: uncited claims

Flagged by the worker, none of them cited: MuA's 5 bp stagger, the ~17 bp T7 promoter, and
"RRBS sees a minority of CpGs". Also, the polymerase selection-chart figure gives error rates
as *ranks rather than numbers* because the worker could not read NEB's live chart, and the
cells it was unsure of are marked "check" in the figure itself. Compare those against the
live chart before teaching from it.

## Curriculum gap: crosslinking is used as a block but never taught as one

Found during the cross-reference pass. `chromatin/` lists crosslinking in its own "blocks we
reuse" table, and `3d-genome/` depends on it entirely — crosslink, digest, ligate — but **no
Part B unit teaches fixation chemistry**. The nearest material is UV crosslinking for CLIP in
`chemistry-to-sequence/`, and "fix and permeabilise, then react in place" in `compartments/`
and `tricks/lec-more.qmd`. Neither covers formaldehyde or DSG, reversal, or what
over-fixation costs. The worker left that table row unlinked rather than point somewhere
wrong, which was the right call.

It also bites `spatial/`, where fixation and permeabilisation are the limiting chemistry.

Options, for the course owner:

1. Add a short Part B unit on crosslinking and fixation (the honest fix; it is a block by the
   course's own definition, and three use cases depend on it).
2. Extend `compartments/`, which already owns fix-and-permeabilise.
3. Leave it to the use cases and accept that the spine has one hole.

A second, smaller instance: **cap trapping** lives only in `tricks/lec.qmd` and not in
`selection/`, although it is a selection method.

## Decision needed: SPRI is taught twice

`fragmentation/lec.qmd` and `qc/lec.qmd` both teach the SPRI mechanism, how the ratio sets
the cut-off, double-sided selection and a worked bead-volume calculation — about four
near-identical slides at the same depth. `CURRICULUM.md` does plan SPRI in both B4 and E1, so
overlap was intended, but this is duplication rather than a division of labour.

Proposed: keep the mechanism and the calculation in `qc/` (E1 marks it ★), and leave
`fragmentation/` the design decision — which size window, one-sided or two — with a link.
Not done yet; `qc/` was still being edited.

## Syllabus coverage audit

Every named method, reagent and enzyme in `CURRICULUM.md` Parts A–E (225 terms), plus a
phrase-level pass over the bullets, checked against all `.qmd` *and* the figure sources —
several syllabus items are taught inside a figure rather than in deck text (KAPA HiFi, LNA,
ddC, photocleavable linkers, 5'-PPP), so a `.qmd`-only search reports false gaps.

Everything in Parts B, D and E is covered. What is not:

| Item | Syllabus | Status |
|---|---|---|
| Ion Torrent | A2 platform list | closed — third panel in `sequencers/fig14`, Rothberg 2011 |
| Optical duplicates | A2 | **absent**, left open deliberately — see below |
| Acrydite | A1 oligo modifications | **absent** — matters for gel and bead-bound oligos |
| Lipid-anchored oligos | A1 oligo modifications | closed — now a mark on `nucleic-acids/fig11`, linked to hashing |
| FLAM-seq | C2 collection | **absent** — it belonged to the unbuilt C2c deck |

Deliberate and already recorded above: the C2c (full-length/isoform) and C7c (multimodal/VDJ)
decks were absorbed into `long-reads/`, `single-cell/` and `single-cell/lec-combinatorial.qmd`
rather than built separately.

Items the syllabus explicitly says to teach *through a human application* rather than by name
— Tn-seq, 16S, GBS, ARTIC, meta3C — are correctly absent as named protocols; insertion-site
mapping is taught in `screens/lec-readout.qmd`.

All five gaps are small: four are one line each, and FLAM-seq is one bullet in
`rna/lec-small-rna.qmd` or `long-reads/lec.qmd`. The structural gap worth more thought is
still crosslinking, recorded above.

Note that `## Still open` in `CURRICULUM.md` is now stale: it asks where to start building.

## Optical duplicates: still not covered, by decision

Two reads that came from **one** original molecule because the instrument read one cluster
twice, not because PCR copied it. On a patterned flow cell a single library molecule can seed
its own well and a neighbouring one (ExAmp pad hopping); on an unpatterned lane an overlarge
cluster can be called as two. The give-away is that the pair sit next to each other on the
flow cell, which is why dedup tools treat them separately and use a pixel-distance threshold.

Why it matters for library prep: it inflates duplicate rate without any PCR being at fault,
so it is one of the things that can make a good library look over-amplified. A UMI collapses
them like any other duplicate, since the molecule really is the same one.

Not added. It is an instrument artefact rather than a library-prep decision, and `qc/` already
teaches the duplicate-rate signature it would confuse. One line in `sequencers/lec.qmd` beside
cluster density would close it if wanted.

## Exercise overlap to decide

`modifications/exercise.qmd` and `chemistry-to-sequence/exercise.qmd` now pose three pairs of
similar problems: the lambda conversion-rate arithmetic (modifications E1 / chemistry E2), the
oxBS-minus-BS subtraction (E4 / E4) and RRBS cost (E5 / E8). In each pair the modifications
version is the harder one — it adds a correction and a standard error, an impossible negative,
and fragment-size arithmetic — so they are a progression rather than a duplicate, and both
were kept. Worth a deliberate decision by someone who owns both pages.

## Three course-wide inconsistencies the figure audit found

Each needs an author decision rather than a silent edit.

**Adapter-dimer size.** `library-molecule/fig15` says ~135 bp; `nucleic-acids/lec.qmd` says
~120 bp; `qc/exercise.qmd` uses 120 and 130. Both are defensible: 136 is the arithmetic for
the dual-indexed construct fig15 actually draws (70 + 66), 120 is the single-index number.
Pick one convention and say which construct it refers to.

**Guide-pool size in screens.** `fig18` works in 70,000 guides, `fig09` in 100,000, and
`lec.qmd` in 120,000 throughout. Changing fig18 ripples into its "~200 cells per guide".
Related and worth its own look: at 100 µg of gDNA (about 1.5e7 genomes) and 120,000 guides,
the readout samples roughly 125 cells per guide, far below the 500 cells per guide the deck
says the screen was *run* at. The decks never connect those two numbers, and a student who
does will think one of them is wrong.

**HOT and BAD are too close.** `#b4532a` and `#a33a28` cannot be told apart at 2 px stroke or
12 px type, and one figure depended on the distinction until the auditor added text tags.
Widening that hue gap in `tools/figlib.py` would help the whole course, at the cost of
regenerating every figure. Worth doing deliberately, not as a side effect of something else.

Also noted: cairosvg resolves figlib's `ui-monospace` to a proportional font, so tightly
packed `mono()` runs look overlapped in a local PNG render and are correct in a browser.
Render with `DejaVu Sans Mono` substituted before believing a mono overlap.

## A colour convention to decide: BAD for a rewritten base

Across nine figures in `chemistry-to-sequence/` (fig02, 03, 04, 10, 11, 12, 16, 22, 23) the
colour `BAD` marks *the base the chemistry rewrote*. Under the course's own convention `BAD`
means failure — and in every one of those figures the rewrite is the measurement succeeding.

The audit changed only the two figures where the colour contradicted the figure's own caption
(the TAPS row, where the caption says a T marks a modification, and the GLORI route). Changing
the other nine is a restyle rather than a fault fix, so it wants a decision: either adopt a
neutral "changed base" colour across the unit, or state in the deck that this unit reads BAD
as "rewritten" rather than "failed".

Related, lower risk: `modifications/fig15` and `fig32` use OK/HOT/TOP as card-identity
colours, which puts one named method in green beside others — close to a verdict the course
does not make.

## Split-pool collision figures use different cell counts

`tricks/fig31-splitpool` loads 10,000 cells (1.1% collisions) and
`barcodes-umis/fig08-splitpool` loads 50,000 (5.5%). Both are arithmetically right and the
repetition between the trick catalogue and the unit that owns a block is deliberate, but a
reader comparing the two sees two different answers to what looks like one question. Either
use the same load in both, or have the trick-catalogue figure say it is a different scenario.

## Colour as a verdict: the pattern the figure audit kept hitting

Across all seven audit groups the commonest fault was not a collision but a colour that
graded something the course refuses to grade. `OK` green and `BAD` red were used as plain
category colours in figures that compare methods, so a reader sees one protocol endorsed and
another marked as failed — in a course whose rule is to state what a chemistry does and leave
the choice alone.

Fixed where the colour contradicted the figure's own caption or slide. Left, because
recolouring an overview is a design decision rather than a fault fix:

- `genomic-dna/fig02-input-scale` and `fig21-decision` — green PCR-free, red single-cell WGA,
  though WGA is the right route for one cell
- `selection/fig01-map` — BAD for "depletion", OK for "enzymatic"
- `compartments/fig20-knee` — the keep-these-barcodes line drawn in BAD
- `modifications/fig15`, `fig32` — OK/HOT/TOP as card identity, which puts one named method
  in green beside its alternatives
- `chemistry-to-sequence` — nine figures where BAD means "the base the chemistry rewrote"

Two root causes worth fixing once rather than per figure: `HOT` and `BAD` are too close to
distinguish at slide size, and figlib has no neutral categorical palette, so an author
reaching for a third colour reaches for a semantic one.
