# Refactoring plan

Consolidates the seven-deck pedagogy audit and the course owner's decisions. Supersedes the
ordering notes in `pedagogy-plan.md`, which stays as the record of *why* each choice was made.

The problem in one line: 32 decks were written in parallel against a brief that said what each
must contain, and nothing checked what it is like to read them in order. Only four decks trace
a named protocol from sample to finished library. The rest are correct mechanisms with nothing
for a student to pin them to, and the early units are worst affected.

## Principles

1. **Every deck earns a whole example**, or explicitly defers to the one that carries it. A
   whole example is one named protocol or one molecule followed through consecutive steps —
   not six methods with a slide each, and not a calculation.
2. **Illumina is the focal point** until the short-read protocols are covered. Branching is a
   later reward, not an early tax.
3. **Concept budget.** No slide introduces more than about four new terms. Nothing is used
   before it is explained or signposted.
4. **No recommendations.** State what a chemistry does, costs and how it fails; leave the
   choice to the reader. Distinguish kits from published methods, because that is a fact, and
   let it speak for itself.
5. **Teach from the shortest complete library upward**, in order of how much the student must
   already know.

## The backbone ladder

Ordered by how much prior knowledge each needs. Each is already named in several decks, so
none costs new vocabulary.

| # | Backbone | What it carries | Home |
|---|---|---|---|
| 1 | **Amplicon + index PCR** | PCR, tailed primers, index PCR, read structure — both ends already known | **introduced in Part A/B**: library-molecule, handles, amplification. Applied, not re-taught, in screens/lec-readout |
| 2 | **Tagmentation of naked DNA** | the shortest library for unknown sequence: cut-and-tag, then PCR | library-molecule, enzymes/lec-transposases, genomic-dna |
| 3 | **ATAC-seq** | the same two steps in nuclei; the enzyme chooses where | enzymes/lec-transposases, chromatin |
| 4 | **TruSeq DNA PCR-free** | the five steps Tn5 collapsed into one, and why you would still pay for them | nucleic-acids, end-chemistry, handles, genomic-dna |
| 5 | **SMART-seq2** | RT, template switching, full-length cDNA | rna, enzymes, handles, single-cell |
| 6 | **10x 3′ and 5′** | compartments, cell barcodes, **UMIs taught here first**, read structure | barcodes-umis, compartments, single-cell |
| 7 | **SPLiT-seq** | combinatorial barcoding: the barcode is the path, collisions replace doublets | single-cell/lec-combinatorial, compartments |
| 8 | **EM-seq** | conversion: protect, deaminate, read as T | chemistry-to-sequence, modifications |
| 9 | **Padlock + PCR panel** (smMIP) | targeted capture by circularisation; in-situ is a later branch | targeted |

Rule for reuse: the deck that owns a backbone teaches it; every other deck *refers* to it in
one line rather than re-deriving it.

**The amplicon is introduced early, not in Part C.** An earlier draft of this plan put it in
`screens/lec-readout`, which is wrong: PCR, tailed primers, index PCR and read structure are
Part A and Part B material, and by Part C a student must already have them. The amplicon is
the worked example *for those blocks*, not an application that teaches them:

- `library-molecule` (A3) already has "A tailed primer, cycle by cycle" and "Truncated
  adapters, completed by PCR". That is the amplicon construct, and it is the right place for
  the first complete molecule a student sees built.
- `handles` (B2) teaches primer tails as one of the five ways; the amplicon is its simplest case.
- `amplification` (B5) teaches the PCR itself.

`screens/lec-readout` then *uses* it — the CRISPR readout is an application of a construction
the student has known since Part A — and a reminder slide is all it needs.

## Phases

Ordered so that each phase makes the next cheaper. Phases 1 and 2 are independent of each
other and can run in parallel; phase 3 depends on 2.

### Phase 0 — done

Terminology sweep (~38 glosses, ~23 signposts, two collisions); the SPRI seam and its orphan
figure; `Cq` and `chaotropic`; the padlock chain slide; the bead-ratio ladder and its
exercise; MERFISH/seqFISH; the FISSEQ framing; display libraries; Ion Torrent; lipid anchors.

### Phase 1 — structural moves (no new teaching content)

Cheapest real gains. Each is a relocation or a retarget.

1. **Split the platforms deck.** `sequencers/lec-platforms.qmd` keeps MGI, AVITI, Ultima, Ion
   Torrent (~7 slides). PacBio and Nanopore, plus the two cross-platform tables, become
   `long-reads/lec-instruments.qmd`, the first deck of that unit. Retarget 8 of its 12 inbound
   links; `spatial`'s DNBSEQ link stays. Signpost the two `chemistry-to-sequence` native-readout
   slides as previews rather than explaining instruments twice.
2. **`chromatin:44`** — the nine-unexplained-protocol-names table moves to just before "Why
   real protocols differ" as a recap.
3. **CLIP before miCLIP** in `modifications/lec-rna.qmd` (currently the mechanism arrives after
   the method that depends on it).
4. **Move the display block** out of the middle of the 15-slide `screens/lec.qmd` trace, to
   after "The problem handed to the next deck".
5. **3C/4C after the Hi-C trace** in `3d-genome`, so the best trace in the course starts earlier.
6. **CROP-seq/Perturb-seq** in `single-cell/lec-combinatorial.qmd`: reduce to one signposted
   slide, since the lentiviral vector they depend on is taught two decks later.

### Phase 2 — spines, worst first

Each entry: the deck, the backbone, and what is cut to pay for it.

| Deck | Backbone to run through it | Paid for by |
|---|---|---|
| `nucleic-acids` | TruSeq front end across slides 2–12, five questions answered per step | demoting the oligo-modification gallery and IUPAC table to reference slides |
| `enzymes/lec` | promote `fig44-walkthrough.svg` (exists, unused, in the wrong deck) to the front, named | demoting the three chart slides to a reference block after "Extension temperature" |
| `chemistry-to-sequence` | EM-seq through the first ten slides, construct drawn at each step | pulling `:276`/`:277` out of the footer into the body where they are load-bearing |
| `chromatin` | ChIP-seq across the four already-consecutive slides `:143`–`:173` | the relocated `:44` table |
| `handles` | lift the "three ideas" sentence out of `fig02` into slide 2, label each family; then SMART-seq3 | the topoisomerase/recombination slide, which the deck itself calls out of scope |
| `genomic-dna` | drawn TruSeq DNA PCR-free | cutting 8 slides that re-teach `amplification` |
| `rna` | draw `:139` TruSeq Stranded mRNA — three preceding slides already draw its steps | nothing; one figure |
| `targeted` | promote CAPP-Seq to a traced construct | the padlock slide already added shows the pattern |
| `design` | the five-slide capstone: ATAC from question to loaded flow cell | nothing; the deck is at 25 of 30 |

### Phase 3 — Part C stops re-teaching Part B, but may remind

21 slides across `modifications` (both) and `single-cell` (both) duplicate
`chemistry-to-sequence`, `compartments`, `barcodes-umis` and `amplification`, sometimes with
identical worked numbers and identical citations. `genomic-dna` has 8 more against
`amplification`.

**Do not simply delete them.** The course owner's rule: avoid re-teaching, but reminder slides
are welcome. A student arriving at a Part C deck months after Part B should not be stranded.

A **reminder** differs from a re-teach in all of these ways:

| Re-teach (cut it) | Reminder (keep it) |
|---|---|
| derives the mechanism again | states the conclusion the reader needs here |
| repeats the worked numbers | names the result, links to where it was worked |
| repeats the original citations | cites nothing; the owning deck holds the references |
| its own figure | no figure, or the owning deck's figure reused unchanged |
| a full slide of bullets | two or three lines, often folded into the next slide |

Rule of thumb: a reminder says *what you already know and why it matters here*, then gets on
with the deck's own subject. If a reminder is longer than about three lines, or if it would
make sense to someone who had not read the owning deck, it has turned back into a re-teach.

**Some things get no reminder at all. By Part C, assume the student knows PCR.** PCR, index
PCR, tailed primers and what a cycle costs are Part A and Part B material that the student has
by then used repeatedly; restating them is padding, not courtesy. This settles the open
question about `genomic-dna`: its eight slides against `amplification` — the PCR-cost trio,
duplicates and complexity, and the MDA/MALBAC/PTA set — are **cut, not converted to
reminders**. One line pointing at `amplification` is enough for all of them.

Reserve reminders for what is genuinely easy to lose across a long course: a specific end
state, a particular arithmetic result, or a constraint that a protocol turns on.

The slides freed this way are the budget for phase 2.

### Phase 4 — remaining content gaps

**Crosslinking is now a Part B unit, B10, after `compartments`.** ✅ built. Decision taken
rather than extending `compartments`, for three reasons:

- It is a block by the course's own definition — a step you put into a protocol, with its own
  reagents, its own end states, its own failure modes and its own tricks. The course's central
  claim is that protocols are assemblies of blocks; a block used by five units and taught in
  none undercuts that claim everywhere it is made.
- `compartments` is about *physical containers* that keep molecules from one cell together.
  Crosslinking is *chemical tethering* that holds an association in place while you take the
  sample apart. Filing one under the other would mis-teach both.
- Five units depend on it: `chromatin` (formaldehyde ChIP, and the tethered-enzyme methods
  that deliberately avoid it), `3d-genome` (formaldehyde plus DSG, where the crosslink is the
  measurement), `modifications/lec-rna` (UV CLIP), `spatial` and `single-cell` (fixation and
  permeabilisation as the limiting chemistry).

Scope, about 16–20 slides: formaldehyde (what it joins, protein–DNA and protein–protein, and
that it is reversible); DSG and the longer-arm protein–protein crosslinkers; UV as the
zero-length, irreversible, RNA–protein case; fixation and permeabilisation of whole cells and
nuclei; reversal by heat and proteinase K; and the costs — epitope masking, over-fixation,
lost accessibility, chimeras, and why some methods go to great lengths to avoid crosslinking
altogether. Worked example: formaldehyde ChIP from cells to reversed, sheared chromatin, with
UV CLIP as the contrast that cannot be reversed.

Its arrival lets `chromatin:44`'s block table finally be honest, and gives `3d-genome` a block
to point at for its first step.

- `acrydite`, FLAM-seq: one line each.
- `acrydite`, FLAM-seq: one line each.
- `design` capstone's five missing demonstrations (construct per step, oligo sequences with Tm,
  enzyme table with the deciding property, the Omni-ATAC comparison, QC closure).

## Part C order: decided

**`screens` now comes before `single-cell`.** Done in the sidebar and `index.qmd`. This fixes
the dependency properly rather than patching it: the lentiviral vector, the LTR, Pol II/Pol III
and the amplicon backbone are all in place before any single-cell deck needs them.

### Single-cell screens: the teaching order inside it

Course owner's sequence, now possible because `screens` precedes:

1. **Pooled screens** (bulk) — the vector, integration, the amplicon readout.
2. **Single cell** — compartments, cell barcodes, UMIs, on the 10x 3′ and 5′ backbones.
3. **Perturb-seq by 5′ direct guide capture** — the *introduction* to single-cell screens.
   It is the simplest form: a capture sequence in the guide scaffold, read by the 5′ kit the
   student already knows. No trick is required to see the guide.
4. **CROP-seq** — taught *after* as a variation, not before. It needs the guide to appear in a
   polyadenylated transcript via LTR duplication during reverse transcription, which is real
   machinery and only makes sense once the vector is known. The audit called the current
   CROP-seq slide the worst in its set precisely because it arrives before that material.
5. **Multiplexed and combinatorial knockouts** — last, once both single cell and pooled
   screening are established.

This replaces phase 1.6: CROP-seq and Perturb-seq do not get cut to a signposted stub, they
get reordered and taught properly, with 5′ capture leading.

## Verification

After each phase: `python3 tools/check_course.py`, regenerate all figures, `quarto render`,
and confirm no cross-unit link broke (405 at last count). The slide-height estimator is coarse
— slides near 700px should be spot-rendered.
