SHELL := /bin/bash

# Main document and outputs
TEX      := manuscript.tex
PDF      := $(TEX:.tex=.pdf)
BIB      := references.bib
REPORT   := abbrev_report.txt

# Tools
LATEXMK  := latexmk
PYTHON   := python
ABBRV    := scripts/abbreviate_journals.py

.PHONY: all abbreviate pdf clean distclean watch
.DEFAULT_GOAL := all

# Build everything: abbreviate journals, then compile PDF
all: abbreviate pdf

# Abbreviate journal names in-place using LTWA + JSON mapping (drop stopwords)
abbreviate: $(BIB) $(ABBRV)
	$(PYTHON) $(ABBRV) \
		--bib $(BIB) \
		--in-place \
		--report $(REPORT) \
		--drop-stopwords

# Compile the document
pdf: $(PDF)

$(PDF): $(TEX) $(BIB)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(TEX)

# Continuous preview (optional)
watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode $(TEX)

# Clean auxiliary files
clean:
	$(LATEXMK) -c

# Clean all generated files (including PDF and report)
distclean: clean
	rm -f $(PDF) $(REPORT)

