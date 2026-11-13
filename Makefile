# Mirrors the quantbio-3MB00A course framework: a Quarto website rendered into
# docs/, one folder per unit, figures generated as SVG.

.PHONY: all render preview check figs clean

all: check render

render:
	quarto render
	@touch docs/.nojekyll

preview:
	quarto preview

# Enforce the material rules: deck length, picture ratio, slides that would be
# clipped, code in exercises. CI runs this before publishing.
check:
	python3 tools/check_course.py

# Re-generate the conceptual SVG figures (not run by quarto render).
figs:
	for f in */make-figs.py; do python3 "$$f"; done

clean:
	rm -rf .quarto docs
