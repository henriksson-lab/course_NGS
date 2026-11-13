QMD := $(shell find . -name '*.qmd' -not -path '*/old/*' -not -path './.quarto/*')
HTML := $(QMD:.qmd=.html)

.PHONY: all site preview add clean figures check

all: $(HTML)

site:
	quarto render

preview:
	quarto preview

# Stage everything needed for a deploy commit.
# Avoids `git add .` so big/unwanted files at the repo root (e.g. the .deb
# installer) don't slip in.
add:
	-git rm -f --ignore-unmatch index.md
	git add Makefile _quarto.yml .nojekyll .gitignore custom.scss README.md AUDIENCE.md
	git add index.qmd index.html
	git add -A img foundations blocks usecases tricks qc design

%.html: %.qmd _quarto.yml
	quarto render $<

clean:
	rm -rf .quarto _site
	rm -f $(HTML)

# Regenerate the conceptual SVG figures (they are checked in; run after editing the generator)
figures:
	python3 tools/make_figures.py

# Enforce the deck rules: <=30 slides, >=50% of slides with a picture, no code in exercises
check:
	python3 tools/check_course.py
