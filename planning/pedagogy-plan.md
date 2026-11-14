# Plan: whole examples, concept load, bead ladders

Agreed with the course owner after the seven-deck pedagogy audit (findings in
`review-notes.md`). The problem the audit confirmed: of 32 decks, only four trace a named
protocol from sample to finished library. The rest are correct mechanisms with nothing for a
student to pin them to, and the early units are the worst affected.

## Backbone protocols

The course adopts a small set of named protocols that recur as spines, so a student meets the
same molecule repeatedly instead of a new example every slide. Chosen because each is already
named in several decks, so they cost no new vocabulary:

| Spine | Carries | Already named in |
|---|---|---|
| **Amplicon + index PCR** (CRISPR screen readout) | the simplest library of all: PCR with tailed primers | screens/lec-readout, handles, barcodes-umis, library-molecule |
| **Tagmentation of naked DNA** | the shortest complete library there is: cut-and-tag, then PCR | library-molecule, enzymes/lec-transposases, genomic-dna, fragmentation |
| **ATAC-seq** | the same two steps, in nuclei: the enzyme chooses where | enzymes/lec-transposases, chromatin, compartments |
| **TruSeq DNA PCR-free** | the DNA ligation library: ends, adapters, PCR-free | handles, end-chemistry, genomic-dna, amplification, tricks, design |
| **SMART-seq2** | the RNA/cDNA spine: RT, template switching, full length | handles, enzymes, rna, single-cell |
| **EM-seq** | conversion chemistry: protect, deaminate, read as T | enzymes/lec-transposases, chemistry-to-sequence, modifications |
| **10x 3′ and 5′** | compartments, cell barcodes, **UMIs**, read structure | library-molecule, barcodes-umis, single-cell, compartments |

**Start with an amplicon, because it is the one case where the sequence is already known.**
Targeted PCR with tailed primers — the readout of a CRISPR screen is the cleanest example —
is the simplest complete library in the course: no fragmentation, no ligation, no enzyme that
cuts anything. Two primers sit on sequence you already know, their tails carry P5, the index
and the read-1 site, and after one or two PCRs the molecule is finished. It is the earliest
possible place to teach **PCR, tailed primers, index PCR and read structure**, all on a
molecule a student can draw from memory.

It also sets up the course's central idea rather than competing with it. `handles/` says the
problem is putting a known sequence onto an *unknown* molecule; the amplicon is the degenerate
case where that problem does not exist yet. Everything after it is a different answer to
"what do I do when I do not know the ends?"

**Then introduce Tn5, on naked DNA.** Tagmentation of purified
DNA is the shortest complete library in the course: one enzyme cuts and attaches the handle in
a single step, one PCR finishes the adapters, and the molecule is ready. Nothing else has to
be taught first — no end repair, no A-tailing, no ligase, no size selection. That makes it the
first whole example for *unknown* sequence, and it is a real protocol (Nextera-style
whole-genome sequencing), not a teaching toy.

So the sequence of worked examples runs from knowing both ends to knowing neither:
**amplicon** (both ends known) → **tagmentation of naked DNA** (neither end known, one enzyme)
→ **ATAC-seq** (same chemistry, the enzyme chooses where) → **TruSeq ligation** (neither end
known, five steps, and why you would still pay for them).

**Then ATAC-seq is the same two steps with nuclei instead of purified DNA.** The chemistry does
not change at all; what changes is that the enzyme can only reach open chromatin, so where it
inserts becomes the measurement. Teaching it in that order means ATAC costs the student almost
no new library chemistry — it is the cleanest possible demonstration of the course's own thesis
that a protocol is an assembly of blocks, and that swapping one input changes the question.

TruSeq DNA PCR-free then arrives as the contrast: what you must do when there is no transposase
in the route — the five steps Tn5 collapsed into one, and why you would still choose them
(even coverage, no insertion-sequence bias, no PCR at all). Be honest about the trade: Tn5 has
a sequence and chromatin-state insertion preference and its insert size depends on the
enzyme-to-DNA ratio, which is exactly why PCR-free ligation survives for whole genomes.

**The contrast runs at two levels, and both are worth drawing explicitly.**

1. *As chemistry:* tagmentation against end repair, dA-tailing and ligation. One step against
   five. Each A-tailing slide can then say which Tn5 step it is replacing, which is what turns
   the end-chemistry material from a catalogue into a set of answers to a question the student
   already has.
2. *As adapter systems:* TruSeq against Nextera — a forked Y adapter carrying the full P5…P7
   sequence, versus a mosaic end plus short S5/S7 arms completed by tailed index PCR. This is
   the better of the two contrasts for teaching read structure, because the two systems put
   the same information in different places and the student can derive each read's content
   from the construct.

`library-molecule/lec.qmd` already teaches level 2 well — it follows Nextera for six slides and
TruSeq for four, with the same seven-part drawing on both, and the audit named it the best deck
in Part A. So the spine does not have to build that contrast, only point at it and reuse its
drawing. Level 1 is the part no deck currently makes, and it is where the work goes.

**10x carries UMIs.** It is the reference point for both 3′ and 5′ single-cell RNA-seq, and
the natural place to introduce UMIs for the first time, because there the UMI is visible in
the read structure and has an obvious job: one bead barcode, many UMIs, one molecule each.
Teach UMIs on 10x and let the other UMI uses — duplex tags in `targeted`, MIP counting in
`screens`, consensus in `tricks` — refer back to it rather than re-deriving the idea. The
3′/5′ pair also earns its keep later: the 5′ configuration is where V(D)J enrichment comes
from, so `single-cell/lec-combinatorial.qmd` stops needing a cold open for it.

A spine is not a new topic. Each deck keeps teaching its own subject; the spine is the thread
the slides hang on, and each slide says which step of it the slide decides.

## The work, in cost order

**A. Terminology sweep.** About 25 terms are used but defined nowhere in the course, several
load-bearing: `processivity` (5 uses), `PAM` (bolded as if defined), `sequencing-by-ligation`
(four spatial slides depend on it), `N50`, `cPPT`, `VAF`, `TSO` (never expanded), `polony`,
`concatemer`, `probe-anchor ligation`, `ExAmp`, `RACE`, `Adaptase`, `fold-80`, `diol`,
`k-mer`, `jackpotting`, `genotype mixing`, `DSG`, `FFPE`, `MBC`, `sublibrary index`.
Two collisions to disambiguate: **HiFi** (polymerase class vs PacBio read) and **template
switching** (TSO reaction vs RT strand-switching between co-packaged genomes in screens).
Done: `Cq`, `chaotropic`.

**B. Ordering fixes.** Slide moves, no new content. `chromatin:44` (nine unexplained protocol
names on slide 3) becomes a late recap; CLIP before miCLIP; the display block moves out of the
middle of the 15-slide screens trace; 3C/4C after the Hi-C trace; CROP-seq signposted because
the lentiviral vector it depends on is taught two decks later.

**C. Spines for the five worst.** `nucleic-acids` (TruSeq front end), `enzymes/lec` (promote
`fig44-walkthrough.svg`, which already exists, unused, in the wrong deck), `chemistry-to-sequence`
(EM-seq), `chromatin` (ChIP-seq, across four already-consecutive slides), and the `design`
capstone, which asks students to do five things the course never demonstrates.

**D. Cut the Part C duplication of Part B** — 21 slides across the modifications and
single-cell decks, 8 in genomic-dna, sometimes with identical numbers and citations. This is
the slide budget that pays for C.

**The visual idiom already exists:** `design/fig02-walk-dna.svg` and `fig03-walk-rna.svg` are
the five-panel sample-to-P5…P7 trace Part C lacks. Port it back rather than inventing one.
Copy the figure-to-figure handoff of `rna/fig12`/`fig13`, which label a panel "after step 1".

## E. Bead-ratio ladders

Students must see what a size ladder actually looks like after a clean-up at a series of
ratios, and choose a ratio from it — the thing a vendor's AMPure XP application note shows.

The course currently has retention **curves** (`fragmentation/fig12-spri-curve.svg`,
`qc/fig03-ratio.svg`) and twice tells the student to "run your own ladder", but shows no
ladder and never asks them to read one.

- **All images are synthetic**, generated by `make-figs.py` from the course's own retention
  model. No vendor figure is copied or traced. Lane intensities are computed, and the figure
  says on its face that the midpoints are illustrative and must be calibrated per bead lot.
- Belongs in `fragmentation/`, which owns *which window do you ask for*; `qc/` keeps the
  mechanism and the bead-volume arithmetic.
- Add an exercise: given a target insert window and a ladder panel, choose the one-sided or
  two-sided ratios, then say what changes if the sample already contains PEG.
- Optional follow-up, if wanted: an interactive demo (a slider over the ratio, bands appearing
  and disappearing) on the HTML page rather than in the deck. The no-code rule is about what
  students write, not about what a demo may do.

## F. Keep Illumina as the focal point; postpone long reads

Decided by the course owner. Long-read material should not arrive until the key short-read
protocols are covered, so that Illumina can serve as the single reference instrument while a
student is still learning what a library *is*. Branching to other chemistries is a later
reward, not an early tax.

The problem is `sequencers/lec-platforms.qmd`, which sits in **Foundations** (unit A2) and
spends **nine of its fifteen slides on PacBio and Nanopore** — ZMWs, SMRTbells, motor
proteins, squiggles, basecalling, adaptive sampling — before the student has seen a single
protocol end to end.

**The split:**

- `sequencers/lec-platforms.qmd` stays in Foundations and becomes short-read only: why look
  past Illumina, MGI/DNBSEQ, and the AVITI / Ultima / Ion Torrent slide. About seven slides.
  These earn their place early because they are the same *kind* of library with a different
  readout — the point being that the library design problem does not change.
- A new deck, `long-reads/lec-instruments.qmd`, becomes the **first deck of the long-reads
  unit** in Part C: PacBio (SMRTbell, ZMW, HiFi) and Nanopore (pore and motor, the three
  attachment routes, direct RNA, basecalling and error, adaptive sampling), plus the two
  cross-platform comparison tables, which only make sense once every platform is known.
  `long-reads/lec.qmd` already opens by pointing at the platform deck for exactly this, so
  the unit becomes self-contained: how the instrument reads, then how to prepare for it.

**Cross-references to retarget — 12 inbound links, 8 of them long-read:**
`modifications/lec-rna.qmd:202` and `modifications/lec.qmd:143` (nanopore direct RNA and
modification calling), `chemistry-to-sequence/lec.qmd:215` and `:217` (polymerase kinetics,
HiFi), `tricks/lec-more.qmd:80` (HiFi as rolling-circle consensus), `end-chemistry:193`
(SMRTbell hairpin), `long-reads/lec.qmd:31` and `:224`, plus `qc:258` and `design:276` which
should point at both decks. `spatial:122` (DNBSEQ nanoballs) stays as it is — that one is
genuinely short-read.

**One consequence to handle honestly:** `chemistry-to-sequence/` is Part B and teaches native
readout of modifications, which depends on PacBio kinetics and nanopore signal. After the
move those become forward references. They should be signposted as such rather than
explained twice — the native-readout slides are a preview of a Part C unit, and saying so is
better than quietly relying on a deck the student has not reached.

## Sequencing by ligation: how to treat it

Course owner's call: interesting mainly as inspiration for advanced students, in case the
approach returns. It should not be taught as a current platform chemistry.

Accurate framing, because the two halves differ:

- **Dead in bulk sequencing.** SOLiD and Complete Genomics' cPAL are both discontinued, and
  no current short-read instrument reads by ligation. It belongs in no comparison table of
  instruments a student might buy time on.
- **Alive in situ.** Ligation-based readout survived where the molecules cannot be moved:
  STARmap's SEDAL is sequencing by ligation, and FISSEQ used a SOLiD-style ligation readout.
  This is why four slides in `spatial/` depend on it, and why it cannot simply be cut.

So: one short definition at the point `spatial/` first needs it, with a clause noting it was
replaced by sequencing by synthesis in bulk instruments but persists in in-situ methods, plus
at most one sentence for the advanced reader on why the idea is worth knowing. No new slide,
and nothing in Foundations — that would spend the student's attention early on a chemistry
they will never meet on an instrument, which is the opposite of keeping Illumina as the focal
point (see F above).
