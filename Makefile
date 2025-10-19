SHELL := /bin/bash

# Main document and outputs
TEX      := manuscript.tex
PDF      := $(TEX:.tex=.pdf)
COVER_LETTER_TEX := cover_letter-cesys.tex
COVER_LETTER_PDF := $(COVER_LETTER_TEX:.tex=.pdf)
TITLE_PAGE_TEX := title_page-cesys.tex
TITLE_PAGE_PDF := $(TITLE_PAGE_TEX:.tex=.pdf)
BIB      := references.bib
REPORT   := abbrev_report.txt
VALIDATION_REPORT := reference-validation-report.txt

# Tools
LATEXMK        := latexmk
VENV_DIR       := .venv
PYTHON         := $(VENV_DIR)/bin/python
PIP            := $(PYTHON) -m pip
BIBTEX_UTILS   := $(VENV_DIR)/bin/bibtex-utils

.PHONY: all abbreviate pdf cover-letter title-page clean distclean watch setup validate-references
.DEFAULT_GOAL := all

# Build everything: abbreviate journals, then compile PDF
all: abbreviate pdf cover-letter title-page

# Ensure submodule and editable install are ready
setup:
	git submodule update --init --recursive bibtex-utils
	test -d $(VENV_DIR) || python -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install --editable ./bibtex-utils
	$(PIP) install bibtexparser requests

# Abbreviate journal names in-place using LTWA + JSON mapping (drop stopwords)
abbreviate: setup $(BIB)
	$(BIBTEX_UTILS) abbreviate-with-ltwa \
		--bib $(BIB) \
		--in-place \
		--report $(REPORT)

# Compile the document
pdf: $(PDF)

$(PDF): $(TEX) $(BIB)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(TEX)

# Validate references against Crossref
validate-references: setup $(BIB)
	$(PYTHON) scripts/validate_references.py --bib $(BIB) --output $(VALIDATION_REPORT)

# Compile the cover letter
cover-letter: $(COVER_LETTER_PDF)

$(COVER_LETTER_PDF): $(COVER_LETTER_TEX)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(COVER_LETTER_TEX)

# Compile the title page
title-page: $(TITLE_PAGE_PDF)

$(TITLE_PAGE_PDF): $(TITLE_PAGE_TEX)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(TITLE_PAGE_TEX)

# Continuous preview (optional)
watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode $(TEX)

# Clean auxiliary files
clean:
	$(LATEXMK) -c

# Clean all generated files (including PDF and report)
distclean: clean
	rm -f $(PDF) $(REPORT) $(VALIDATION_REPORT) $(COVER_LETTER_PDF) $(TITLE_PAGE_PDF)
