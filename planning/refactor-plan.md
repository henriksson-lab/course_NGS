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
| 1 | **Amplicon + index PCR** (CRISPR screen readout) | PCR, tailed primers, index PCR, read structure — both ends already known | screens/lec-readout, referenced from handles, barcodes-umis |
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

### Phase 3 — Part C stops re-teaching Part B

21 slides across `modifications` (both), `single-cell` (both) duplicate `chemistry-to-sequence`,
`compartments`, `barcodes-umis` and `amplification`, sometimes with identical numbers and
citations. Replace each with a one-line callback. This is the slide budget for phase 2.

### Phase 4 — remaining content gaps

- **Crosslinking has no Part B block** although `chromatin`, `3d-genome` and `spatial` all
  depend on it. Either a short unit or an extension of `compartments`.
- `acrydite`, FLAM-seq: one line each.
- `design` capstone's five missing demonstrations (construct per step, oligo sequences with Tm,
  enzyme table with the deciding property, the Omni-ATAC comparison, QC closure).

## One open question for the owner

`single-cell/lec-combinatorial.qmd` depends on the lentiviral vector taught in `screens`, two
decks later. Phase 1.6 patches it with a signpost. The alternative is to **move `screens`
before `single-cell`** in Part C, which fixes it properly and also puts the amplicon backbone
(#1) early, where it belongs. The cost is re-checking every Part C cross-reference. Worth
deciding before phase 2 starts, because the spines assume an order.

## Verification

After each phase: `python3 tools/check_course.py`, regenerate all figures, `quarto render`,
and confirm no cross-unit link broke (405 at last count). The slide-height estimator is coarse
— slides near 700px should be spot-rendered.
