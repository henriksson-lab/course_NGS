# The site is built and published by .github/workflows/pages.yml on every push
# to main. These targets are for working locally.

.PHONY: site preview check figures clean

# Render the whole site into _site/ (same command CI runs).
site:
	quarto render

# Live preview in a browser; re-renders as you edit.
preview:
	quarto preview

# Enforce the material rules: deck length, picture ratio, slides that would be
# clipped, code in exercises. CI runs this before publishing.
check:
	python3 tools/check_course.py

# Regenerate the conceptual SVG figures (they are checked in; CI verifies they
# match this generator).
figures:
	python3 tools/make_figures.py

clean:
	rm -rf .quarto _site
