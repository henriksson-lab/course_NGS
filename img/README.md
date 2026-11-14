# Photographs

Equipment photographs used in the decks. Mechanism is always a drawn figure; a photograph is
only ever here to show what a piece of equipment physically is.

**Everything in this folder is CC0.** That is a deliberate restriction, not an accident of
what was available: CC0 carries no attribution condition, so the course cannot quietly fall
out of compliance as slides are edited. The author is credited anyway, on the slide and in
`CREDITS.tsv`, because it is the decent thing and it costs a line.

`CREDITS.tsv` is written by `tools/fetch_photo.py`, which is the only way a photograph should
enter this folder. It refuses any licence not on its allowlist, refuses a file with no
recorded author, and records the title, author, licence, licence URL and source page.

    python3 tools/fetch_photo.py "File:Some Photo.jpg" slug 900

## What was rejected, and why

Worth recording so the same candidates are not re-examined:

- **NovaSeq X** (CC0) — a trade-show photograph dominated by an identifiable person wearing a
  name badge. CC0 releases the photographer's rights, not the subject's likeness, and the
  frame reads as vendor marketing rather than equipment.
- **DNA nanoball flow cell** (CC0) — a synthetic rendering of spots, not a micrograph. Using
  it beside real photographs would imply it shows data.

## Still missing

Commons has no usable CC0 photograph of a PacBio instrument, a Covaris sonicator, a magnetic
bead rack, or a 10x Chromium controller. The decks that would use them have drawn figures
instead, which is not a loss — but if a freely licensed photograph turns up, those are the
gaps.
