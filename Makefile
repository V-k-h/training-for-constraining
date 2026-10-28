PYTHON ?= python3
LLZK_OPT ?= llzk-opt

.PHONY: demo test lean llzk-check all slides speaker-notes

demo:
	$(PYTHON) -m demos.circuits

test:
	$(PYTHON) -m unittest discover -s tests -v

lean:
	cd lean && lake exe cache get && lake build

llzk-check:
	@command -v $(LLZK_OPT) >/dev/null || (echo 'llzk-opt not installed; see llzk/README.md' >&2; exit 1)
	$(LLZK_OPT) llzk/and_vulnerable.llzk -o /dev/null
	$(LLZK_OPT) llzk/and_fixed.llzk -o /dev/null

all: demo test

slides:
	cd slides && tectonic --keep-intermediates workshop.tex

speaker-notes: slides
	cd slides && tectonic speaker-notes.tex
