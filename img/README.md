# Photographs

Equipment photographs used in the decks. Mechanism is always a drawn figure; a photograph is
only ever here to show what a piece of equipment physically is.

CC0, CC-BY and CC-BY-SA are all fine here. The photographs are used **unmodified**, so
share-alike never bites: a slide carrying a photograph is a collection, not an adaptation.

**Every image has a `.md` beside it** with its author, licence and source, so the attribution
travels with the file and cannot be lost when a slide is edited. The credit is also on the
slide itself, which is what a reader sees.

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

Widening to CC-BY-SA filled the PacBio gap (a SMRT cell) and added both flow cells. Commons
still has nothing usable for a **Covaris sonicator**, a **magnetic bead rack**, or a **10x
Chromium controller**. The decks that would use them have drawn figures instead.
