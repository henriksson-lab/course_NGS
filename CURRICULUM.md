# Curriculum plan

## Aim and format

After working through the relevant parts, a student can open any protocol in the NGS_101
collection (`~/github/chem`, <https://henriksson-lab.github.io/NGS_101/>, ~840 protocols),
explain what each step does to the molecule, and design a new library prep.

- **Audience:** late MSc and PhD students. Self-paced; students pick the modules they need.
  No cap on total length.
- **Organising principle:** design backwards from the sequencer, then build from
  **building blocks**. Part A (sequencers, the final library molecule) is the prerequisite.
  Part B is the core: a detailed, technical catalogue of building blocks, each with its
  enzymes, oligo designs, failure modes and tricks. Part C is use cases: each one is a map
  showing which building blocks a protocol family combines and why. Part D is a cross-cut
  catalogue of tricks. Part E is QC and designing your own protocol.
- **Unit of material:** a *deck* (revealjs, ≤ 30 slides) + a reading list of original papers +
  an exercise page with Hint/Solution callouts. A module can have several decks.
- **No programming.** Unlike the course this scaffold came from, there are no coding
  exercises and no R or shell for the student to write. Bioinformatics is another course.
  What we use instead:
  - **Demos** — show a tool, a calculation or an animation running; the student watches and
    interprets, and does not write it.
  - **Quizzes** — short factual checks after a deck.
  - **Design questions** — the main exercise type. "You need to attach a handle to the 5' end
    of a capped RNA without losing the cap: which block, which enzyme, which oligo?"
    "This trace shows a 130 bp peak: what went wrong and which step do you change?"
  - **Enzyme and reagent selection** — a skill in its own right. Students should be able to
    pick an enzyme from vendor selection charts and datasheets, e.g. NEB's DNA polymerase
    selection chart (<https://www.neb.com/en/tools-and-resources/selection-charts>), reading
    off fidelity, strand displacement, 3'→5' exonuclease, thermostability, end type produced,
    uracil tolerance and hot start, and justifying the choice for a given step. (neb.com
    refuses automated fetches, so link to the charts rather than copying them.)
- **Slides:** ≥ 50 % of slides carry a picture, always together with text on the same slide.
  Image sources, in order of preference: our own SVG diagrams; construct diagrams and
  animations from the NGS_101 site (our own work); figures from open-access papers with
  attribution.
- **Citations:** every method named on a slide cites its original paper. DOIs for collection
  protocols come from `~/github/chem/catalogue/ours.tsv`.
- **Scope:** all examples are framed in human (mammalian) biology. The chemistry is identical
  whatever the source organism, so where a method was first published in bacteria or viruses
  (Tn-seq, 16S, GBS, ARTIC, meta3C), we teach the underlying block with a human application
  instead — transposon mapping as insertion-site mapping in human cells, tiled amplicons as a
  human targeted panel, reduced representation as human methylation RRBS.

Sources for this plan: `planning/concepts/` (concept lists from parallel agents over the
collection, triaged by citation count; `sequencers.md` items tagged `[KB]` need checking
against vendor docs) and the two old lectures in `oldpres/`.

Legend: **★** core concept used by most protocols · *(rare)* specialised, examples only.

---

## Part A — What the sequencer needs

### A1. Nucleic acids as a building material
Deck A1 (~25 slides)
- ★ Strand polarity; 5'-phosphate and 3'-OH; why every enzyme cares about end states
- ★ ss vs ds, RNA:DNA hybrids, nicks, gaps, 5'/3' overhangs, blunt ends
- ★ Hybridisation and Tm, secondary structure, hairpins, primer/adapter dimers
- ★ Sequence notation: top/bottom strand, reverse complement, IUPAC codes (N, V, B …)
- ★ Oligo modifications: 5'-P, biotin, 3' blocks (C3 spacer, ddC, inverted dT), phosphorothioate,
  dU, RNA/LNA bases, acrydite, photocleavable linkers, lipid anchors
- RNA end states: cap, 5'-PPP, 5'-OH, 2',3'-cyclic phosphate, poly(A)
- Oligo pools from array synthesis (from the 2025 screening lecture)

### A2. How sequencers read DNA
Deck A2a: Sanger and Illumina (~30 slides) · Deck A2b: other short-read platforms and long reads (~30 slides)
- ★ Sanger as the baseline: one primer, one clonal template. Why NGS needs universal ends.
- ★ Illumina: P5/P7 lawn, only P5…P7 molecules cluster, bridge amplification vs ExAmp on
  patterned flow cells, SBS with reversible terminators, 4-, 2- and 1-colour chemistry
- ★ Read order Read 1 → Index 1 (i7) → Index 2 (i5) → Read 2; paired-end turnaround;
  i5 forward vs reverse-complement workflows
- ★ Insert size vs read length, adapter read-through
- Custom sequencing primers, dark cycles, base diversity / PhiX / staggered primers, phasing,
  cluster density, index hopping, optical duplicates
- DNBSEQ (circularisation, DNA nanoballs), Element AVITI, Ultima, Ion Torrent; SOLiD as history
- PacBio: ZMW, SMRTbell, CCS/HiFi, kinetics for modifications
- Oxford Nanopore: motor-protein adapter, ligation vs rapid kits, direct RNA, basecalling,
  modification calling, adaptive sampling
- ★ FASTQ, Phred, demultiplexing, read-structure notation (e.g. 28/8/0/91), error profiles per platform
- Papers: Sanger 1977; Bentley et al. 2008 (Illumina SBS); Eid et al. 2009 (PacBio);
  Drmanac et al. 2010 (DNA nanoballs); Clarke et al. 2009 / Jain et al. 2016 (nanopore)

### A3. Anatomy of a library molecule
Deck A3 (~25 slides)
- ★ P5 – i5 – Read 1 primer site – insert – Read 2 primer site – i7 – P7
- ★ TruSeq Y-adapter vs Nextera (Tn5 mosaic end, S5/S7) architecture
- ★ Full adapters vs truncated adapters completed by tailed index PCR
- ★ Placing information: what goes into R1, R2, I1 and I2 (sample index, cell barcode, UMI, insert)
- ★ Strand and orientation: when is strand information kept?
- What does not cluster or read: adapter dimers, same-end molecules, inserts that are too long
- Exercise: from a construct derive the read structure, and vice versa. Use the NGS_101
  *Annotate* and *Sample-sheet* tools.
- Collection examples: TruSeq DNA PCR-free, Nextera XT, Illumina DNA Prep, 10x 3' v3

---

## Part B — Building blocks

This is the heart of the course, and the most technical part. Each block is a step you can
put into a protocol. Every deck covers: what the block does to the molecule (drawn base by
base), the enzymes and oligos it needs, what it requires of the ends, what it costs, how it
fails, the *tricks* practitioners use, and which use cases (Part C) and collection protocols
rely on it.

### B1. The enzyme toolbox
Decks: B1a polymerases and reverse transcriptases · B1b ligases, kinases and phosphatases ·
B1c nucleases · B1d transposases and modifying enzymes
- ★ Polymerases: fidelity and proofreading, 3'→5' exonuclease, strand displacement,
  thermostability and extension rate, hot start, the end type produced (blunt vs A-tailed),
  uracil tolerance; Klenow and Klenow exo−, T4 DNA polymerase, phi29, Bst, Taq, Q5/KAPA
- ★ Reverse transcriptases: MMLV-derived, template switching, TGIRT; processivity through
  structure and modifications; RT stop vs misincorporation
- ★ Ligases: T4 DNA ligase (blunt, TA, cohesive; PEG crowding), T4 RNA ligase 1 and 2 truncated,
  pre-adenylated adapters, splinted ligation, circularisation ligases
- ★ Kinases and phosphatases: T4 PNK, rSAP — controlling which ends can ligate
- Nucleases: Type II, Type IIS/IIG (cut outside the recognition site), methylation-sensitive
  pairs, nicking enzymes, exonucleases (Exo I, λ, Exo III), RNase H, RNase I, MNase, DNase I,
  S1, USER/UDG, Cas9 and Cas12a RNPs
- ★ Transposases: Tn5 (tagmentation, the 9 bp gap, loaded and fused variants), MuA
- Modifying enzymes: methyltransferases, TET, β-glucosyltransferase, APOBEC3A, glycosylases,
  capping and decapping enzymes, T7 RNA polymerase, TdT, poly(A) polymerase
- ★ **Skill: choosing an enzyme.** Reading vendor selection charts and datasheets (NEB's
  polymerase, ligase and RNA-polymerase charts; buffer compatibility; unit definitions) and
  justifying a choice for a step. Recurring exercise type throughout Part B.
- Tricks: exploiting an activity the enzyme was not sold for (Taq's A-addition, Tn5 on
  RNA:DNA hybrids, RT template switching, phi29's strand displacement for RCA)

### B2. Attaching a handle — the five ways
Deck B2 (~30 slides). The central idea of the course: there are only a few ways to put a known
sequence onto an unknown molecule.
- ★ DNA ligation (blunt, TA, cohesive, splinted)
- ★ RNA ligation (3' pre-adenylated adapter, 5' adapter, circularisation)
- ★ Primer tails: PCR and RT primers carrying the handle
- ★ Transposition: Tn5 cuts and tags in one step
- ★ Template switching: RT adds the handle at the 5' end
- Also: homopolymer tailing (TdT, poly(A) polymerase), topoisomerase, recombination
- Tricks: partial/truncated adapters finished by index PCR; two-step PCR to cut noise;
  nested handles; asymmetric adapters; bead-bound handles

### B3. End chemistry
Deck B3 (~30 slides)
- ★ End states: 5'-P vs 5'-OH, 3'-OH vs 3'-P vs 3'-blocked, overhangs, nicks, gaps
- ★ End repair and blunting; dA-tailing; fill-in; gap repair after tagmentation
- ★ Dephosphorylation to suppress unwanted ligation; selective re-phosphorylation
- Tricks: blocked 3' ends to force one-sided ligation; dU in adapters cleaved later by USER;
  methylated adapters surviving bisulfite; hairpin adapters; inverted-dT; adaptase and
  single-strand ligation for degraded input; dilute ligation to favour intramolecular events

### B4. Fragmentation and size control
Deck B4 (~25 slides)
- ★ Acoustic shearing, enzymatic fragmentation, tagmentation, restriction digest, MNase, DNase I,
  chemical and alkaline hydrolysis
- ★ Size targets set by the sequencer; size selection by SPRI ratio, double-sided selection,
  gel and PAGE
- Tricks: fragment before or after the key chemistry, and why the order changes the answer;
  partial digestion; bottleneck dilution to define endpoints; cutting away from the recognition
  site with Type IIS/IIG enzymes to produce fixed-length tags; avoiding fragmentation altogether
  for long reads

### B5. Amplification
Deck B5 (~30 slides)
- ★ PCR: fidelity, cycle number, GC and length bias, duplicates, over-amplification, PCR-free
- ★ Linear amplification: IVT (T7), single-primer extension
- Isothermal: RCA, MDA, PTA, MALBAC, LAMP, nicking-enzyme SDA
- Inverse PCR, nested and anchored PCR, multiplex and tiled amplicons, emulsion PCR
- Tricks: pre-amplify then split for several libraries; uracil-tolerant polymerases;
  suppressing adapter-dimer amplification; splinkerettes to kill one-sided background;
  rolling-circle consensus for error correction

### B6. Selection — keeping what you want
Deck B6 (~30 slides)
- ★ Affinity: streptavidin–biotin, antibodies, oligo-dT, hybridisation capture with baits
- ★ Depletion: RNase H with DNA oligos, Cas9 cutting, blocking oligos, duplex-specific nuclease
- Enzymatic selection: exonucleases removing linear or unligated species, methylation-sensitive
  digestion, selective circularisation
- Physical selection: size, FACS, subcellular fractionation, gradients
- Tricks: suppression PCR; select by end structure rather than by sequence; carrier nucleic acid
  for low input; spike-in standards

### B7. Barcodes, UMIs and where information lives
Deck B7 (~30 slides)
- ★ Sample indexes, unique dual indexes, barcode design (edit distance, colour balance)
- ★ Cell barcodes: bead-bound, split-pool, plate-based
- ★ UMIs: where they can be added (ligation, RT, TSO) and why never in PCR; collapsing
- ★ Read-structure budgeting: what fits in R1, R2, I1, I2
- Tricks: hashing with antibodies or lipids; combinatorial barcodes from a small oligo set;
  staggered/phased primers for base diversity; UMI plus duplex tags for consensus

### B8. Converting chemistry into sequence
Deck B8 (~30 slides). The trick that makes anything measurable: turn a non-sequence property
into a base change, an end, or a ligation event.
- ★ Base conversion: bisulfite, enzymatic conversion, TAPS, APOBEC; conversion seen as a change
  the polymerase copies
- ★ Position as information: RT stops, polymerase stalls, cut sites, ligation junctions, read ends
- Antibodies and affinity for modified bases; metabolic labels and click chemistry;
  crosslinking signatures (truncations, mutations)
- Native readout: PacBio kinetics, nanopore signal
- Tricks: reduced representation to cut cost; controls that must be run alongside a conversion;
  protect-then-convert strategies

### B9. Compartments
Deck E1 (~25 slides)
- ★ Why compartments: keeping molecules from one cell, one fragment or one complex together
- Wells and plates, droplets, nuclei as compartments, semi-permeable capsules, hydrogels,
  split-and-pool as a virtual compartment
- Poisson loading, doublets, collisions, barcode-to-compartment mapping
- Tricks: fix and permeabilise instead of isolating; two-stage encapsulation; in-situ reactions
  inside nuclei

---

## Part C — Use cases: blocks assembled into protocols

Each module takes a biological question, derives the protocol from the blocks in Part B, then
reads real protocols from the collection and asks why they differ. The recurring exercise:
*given this question and this sample, design the library; then compare with what the field does.*

### C1. Genomic DNA
Deck C1 (~25 slides). Blocks: B4 fragmentation + B3 end chemistry + B2 handle (ligation or
Tn5) + B5 amplification + E1 QC.
- Whole-genome shotgun, PCR-free, degraded and ancient DNA, low input, single-cell WGA
- Why PCR-free when input allows; duplicate rates; coverage uniformity and GC bias
- Collection: TruSeq DNA PCR-free, NEBNext Ultra II, Illumina DNA Prep, Nextera XT, MALBAC, PTA

### C2. RNA
Deck C2a: mRNA and total RNA · Deck C2b: small RNA, 3'/5' tag and low input · Deck C2c: full-length and isoforms
- Choosing by RNA class: length, poly(A), cap, abundance
- rRNA depletion strategies; RT priming; second-strand synthesis; dUTP strandedness;
  template switching; tag vs full-length
- Collection: TruSeq Stranded mRNA, NEBNext Directional, SMART-seq2, CEL-Seq2, STRT-seq,
  NEBNext small RNA, Ribo-seq, FLAM-seq
- Reuses the 2026 RNA-seq lecture

### C3. Targeted sequencing
Deck C3 (~25 slides)
- Amplicons and tiled panels, hybrid capture, MIPs and padlocks, Cas9-guided enrichment,
  reduced representation (RRBS for human methylation; RAD/ddRAD/GBS as the same idea in genotyping)
- Rare-variant detection and why it forces UMIs or duplex tags
- Collection: CAPP-Seq, SureSelect, smMIPs, Safe-SeqS, RRBS, tiled amplicon panels

### C4. Chromatin and protein–DNA
Deck C4 (~30 slides)
- Accessibility (DNase-seq, ATAC-seq, MNase-seq, methyltransferase footprinting)
- Binding (ChIP-seq, CUT&RUN, CUT&Tag, DamID, calling cards, DAP-seq)
- Crosslinking and reversal; the tethered-enzyme idea (pA-MNase, pA-Tn5) as a block
- Collection: ATAC-seq, Omni-ATAC, ChIP-seq, CUT&RUN, CUT&Tag, DNase-seq

### C5. Three-dimensional genome and contacts
Deck C5 (~25 slides)
- Proximity ligation as a block: crosslink, digest, ligate, pull down the junction
- 3C → 4C → Hi-C → in situ Hi-C → Micro-C; viewpoint methods; HiChIP; bridge linkers;
  ligation-free approaches (SPRITE, GAM); RNA–chromatin contacts
- Collection: Hi-C, in situ Hi-C, HiChIP, 4C-seq, ChAR-seq, SPRITE (all human/mammalian)

### C6. Modifications, damage and dynamics
Deck C6a: DNA methylation and damage · Deck C6b: RNA modifications and nascent RNA
- Bisulfite and its successors; break mapping; replication timing; repair outcomes
- m6A and other RNA marks; CLIP family; metabolic labelling; GRO-seq and PRO-seq;
  TSS mapping; structure probing
- Collection: RRBS, EM-seq, TAB-seq, GUIDE-seq, END-seq, Repli-seq, m6A-seq, eCLIP, PAR-CLIP, GRO-seq

### C7. Single cells
Deck C7a: plates, droplets, microwells · Deck C7b: combinatorial indexing · Deck C7c: multimodal and VDJ
- The same blocks, but every molecule must carry a compartment barcode
- Collection: 10x 3' v3, Drop-seq, inDrop, MARS-seq, sci-RNA-seq3, SPLiT-seq, SHARE-seq,
  CITE-seq, 10x Multiome, 10x VDJ

### C8. Spatial
Deck C8 (~25 slides)
- Array capture (Visium, Slide-seq, Stereo-seq, HDST), microfluidic barcoding (DBiT-seq),
  region selection (GeoMx), in situ sequencing (FISSEQ, STARmap)
- Fixation and permeabilisation as the limiting chemistry

### C9. Pooled screens and synthetic libraries
Deck C9a: building pooled libraries · Deck C9b: reading screens out
- Oligo pools, pooled cloning, lentiviral delivery and integration into the human genome
- Readout as a library-prep problem: inverse PCR, splinkerettes, two-step index PCR,
  MIPs with UMIs for absolute counting
- MPRA and STARR-seq, deep mutational scanning, lineage recording, display libraries
- Collection: lentiCRISPR v2, Joung one-PCR readout, Moffat two-step readout, STARR-seq,
  CROP-seq, Perturb-seq, GUIDE-seq
- Insertion-site mapping (the old Tn-seq material) taught as mapping lentiviral or transposon
  integration sites in human cells
- Reuses the 2025 screening lecture

### C10. Long reads
Deck C10 (~30 slides)
- HMW DNA handling and what shears it; PacBio SMRTbell, Iso-Seq, Kinnex; ONT ligation, rapid,
  ultra-long, native barcoding, cDNA and direct RNA; Cas9 enrichment and adaptive sampling
- Collection: SMRTbell prep 3.0, PacBio Iso-Seq, ONT LSK114, RAD114, ULK114, direct RNA RNA004

## Part D — The trick catalogue

A cross-cutting reference, indexed by the problem rather than by the block. Each entry: the
problem, the trick, the molecular reason it works, and protocols that use it. Decks here are
short and can be read in any order; this is also the part a practising student returns to.

### D1. Making the right thing ligate
- Blocked and inverted ends, dephosphorylation, A/T overhangs, splints, one-sided ligation,
  dilute ligation for intramolecular events, PEG crowding

### D2. Killing what you do not want
- Adapter-dimer suppression, suppression PCR, exonuclease clean-up of unligated species,
  blocking oligos, RNase H depletion, Cas9 depletion, methylation-sensitive digestion

### D3. Getting a handle onto an impossible end
- Template switching, tailing with TdT or poly(A) polymerase, adaptase and single-strand
  ligation, cap trapping, circularisation to turn an end into an internal position

### D4. Squeezing information into the read
- Truncated adapters completed by index PCR, custom sequencing primers, dark cycles,
  barcodes in the index read vs inline, staggered primers for base diversity

### D5. Counting honestly
- UMIs and where they may be added, duplex tags, RCA consensus, spike-ins, PCR-free when
  input allows, limiting cycle number by diagnostic qPCR

### D6. Working with very little, or very degraded, material
- Carrier nucleic acid, single-strand library prep, pre-amplification then splitting,
  bead-bound handles to avoid transfer losses, low-volume reactions

### D7. Keeping molecules together
- Nuclei as compartments, droplets, split-and-pool, fix-and-permeabilise instead of isolating,
  in-situ reactions, two-stage encapsulation

### D8. Turning a property into a base
- Base conversion chemistries, protect-then-convert, position-as-information (stops, cuts,
  junctions), affinity for a modification, native signal readout

---

## Part E — Quality control and designing your own

### E1. Cleanup, quantification and QC
Deck E1 (~25 slides)
- ★ SPRI beads: how the ratio sets the cut-off; columns, precipitation, gels
- ★ Quantification: Qubit vs qPCR vs fragment analyser, and what each actually measures
- ★ Pooling to equal molarity; denature and load; PhiX
- Reading a Bioanalyzer trace: adapter dimers, over-amplification, the right insert size
- Tricks: double-sided selection; diagnostic qPCR to pick a cycle number; small analytical
  aliquots before committing the sample

### E2. Design patterns and failure modes
Deck E2 (~30 slides)
- Reading a protocol as a sequence of blocks; drawing the construct after every step
- Failure modes and their signatures: adapter dimers, one-sided products, chimeras, index
  hopping, low complexity, bias from over-amplification, off-target ligation
- The controls that distinguish them
- Demos: the NGS_101 *Annotate*, *Anneal* and *Sample-sheet* tools run on real constructs

### E3. Capstone
- Design a library prep for a question of your choosing: state the blocks, draw the construct
  at each step, specify the oligos and the enzymes (with a justification from the selection
  charts), predict the read structure, name the controls and the expected failure modes.
  Compare against the closest protocol in the collection.

---

## Open questions for the course author

- Which parts are examined, if any, and how?
- Is there a wet lab component, or is this all paper and reading?
- How much read-level reasoning is needed? There is no programming, but "position as
  information" (B8) and QC (E1) need students to interpret reads and traces.
- Can the NGS_101 site's construct diagrams be embedded directly in slides, or should the
  course re-draw them?
