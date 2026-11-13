# Audience

**Target:** late MSc students, PhD students and postdocs who will either run established
library preparations or design new ones. Self-selecting and self-paced: they take the modules
they need, in the order they need them. There is no fixed cohort, no course code and no exam.

Two readers to keep in mind while writing:

- **The runner.** Has a kit and a protocol, and wants to understand what each step does so
  they can tell a real failure from a cosmetic one, and so they can change a parameter without
  guessing.
- **The designer.** Has a biological question no existing kit answers, and needs to assemble a
  protocol out of blocks that are known to work together.

Material should serve both. The runner needs the failure modes and the bench reality; the
designer needs the building blocks and the tricks. Neither needs a kit manual recited back.

## What we can expect them to know

- **Molecular biology at working level:** DNA and RNA structure, transcription, translation,
  the central dogma. They know what a plasmid, a primer and PCR are.
- **Basic enzymology:** that enzymes have substrates, cofactors and optima, even if they have
  not thought hard about exonuclease activities.
- **Lab experience:** pipetting, PCR, gels, spectrophotometry. Most have done a wet-lab
  project. They can read a protocol and follow it.
- **They have seen sequencing data**, usually as a FASTQ file or a count table someone else
  produced, and often without knowing where the adapters went.

## What we should NOT assume they know

- **How a sequencer actually works.** Flow cell chemistry, why P5 and P7 exist, what an index
  read is, why a read has a maximum length. Treated from scratch in Foundations.
- **Why protocol steps exist.** End repair, A-tailing, bead ratios and cycle numbers are
  usually performed as ritual. Breaking that habit is the point of the course.
- **Enzyme properties in any detail.** That a proofreading polymerase removes an A-tail, or
  that some polymerases stall at uracil, is new to most.
- **Oligo design.** Modifications, degenerate bases, Tm as a property of a duplex in a buffer,
  what you are choosing when you order.
- **Anything computational.** There is no programming in this course, and none is assumed.
- **Platform diversity.** Many have only met Illumina. PacBio and Nanopore chemistry are new.
- **Single-cell, spatial and screen chemistries**, beyond having heard the names.

## Pedagogical implications

- **Lead with the molecule.** Every step is a transformation of an end state. Draw it.
- **Explain why a step exists by showing what fails without it.** The failure modes are the
  most useful thing we can teach, because they are what the student will actually meet.
- **Teach the properties, not the product names.** An enzyme is a row of activities; the
  vendor chart is the tool for reading it. Products change, properties do not.
- **Bench literacy without a wet lab.** They should finish knowing what is in the tube, the
  volumes and molarities, the incubations and clean-ups, and how to read a datasheet — even
  though they will not run anything as part of the course.
- **Cite the original paper** for every method. This audience reads papers, and often needs
  to justify a method choice to a supervisor or a reviewer.
- **Human biology throughout.** The chemistry is the same for any organism; using human
  examples keeps the material consistent and avoids irrelevant framing.
- **Self-paced means self-contained.** A module cannot assume the student attended anything
  else except Foundations. State the prerequisites, and link rather than assume.
- **Respect their time.** They are not undergraduates filling a timetable. Every slide should
  earn its place.
