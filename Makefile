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
DECLARATIONS_MD := declarations-tool.md
DECLARATIONS_DOCX := declarations-tool.docx
PACKAGE_DIR := sf_submission_package
PACKAGE_ZIP := sf_submission_package.zip
PACKAGE_FILES := $(TEX) $(BIB) manuscript.bbl $(PDF) elsarticle.cls elsarticle-num-names.bst \
	Graphical_Abstract.pdf highlights.txt \
	Figure_1.pdf Figure_2.jpg Figure_3.pdf Figure_4.pdf Figure_7.pdf Figure_8.pdf \
	Figure_9.pdf Figure_10.pdf Figure_A1.pdf Figure_A2.pdf Figure_A5.pdf Figure_A6.pdf \
	Figure_A7.pdf Figure_A8.pdf Figure_B1.pdf Figure_B2.pdf Figure_B5.pdf Figure_B6.pdf \
	Figure_B7.pdf Figure_B8.pdf $(DECLARATIONS_DOCX)

# Tools
LATEXMK        := latexmk
VENV_DIR       := .venv
PYTHON         := $(VENV_DIR)/bin/python
PIP            := $(PYTHON) -m pip
BIBTEX_UTILS   := $(VENV_DIR)/bin/bibtex-utils

.PHONY: all abbreviate pdf cover-letter title-page clean distclean watch setup validate-references package clean-package declarations-docx
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

# Build declarations tool docx for portal upload
declarations-docx: $(DECLARATIONS_DOCX)

$(DECLARATIONS_DOCX): $(DECLARATIONS_MD)
	pandoc $(DECLARATIONS_MD) -o $(DECLARATIONS_DOCX)

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

# Build submission package and zip
package: pdf declarations-docx
	mkdir -p $(PACKAGE_DIR)
	cp -t $(PACKAGE_DIR) $(PACKAGE_FILES)
	python -c "from pathlib import Path; pkg=Path('$(PACKAGE_DIR)'); items=sorted(p.name for p in pkg.iterdir()); (pkg/'manifest.txt').write_text('\\n'.join(items)+'\\n')"
	zip -r $(PACKAGE_ZIP) $(PACKAGE_DIR)

# Remove submission package artifacts
clean-package:
	rm -rf $(PACKAGE_DIR) $(PACKAGE_ZIP)
