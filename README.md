# NBDS DSS Manuscript

This repository contains the LaTeX source, figures, and supporting material for the manuscript:

> **Ghasemi, E., Coupland, K., Ghotb, S., & Paradis, G.** Developing a prototype decision support framework to assess forest management scenarios as a nature-based decarbonization solution for the mining sector: A case study in British Columbia, Canada.

The manuscript has been prepared for submission to *Cleaner Environmental Systems* and formatted for EarthArXiv preprint compliance.

## Repository layout

- `manuscript.tex` – main LaTeX source (EarthArXiv cover page + journal submission formatting)
- `references.bib` – bibliography file
- `nbds_dss_manuscript_graphical-abstract.pdf` – graphical abstract used for EarthArXiv and CES
- `Fig.*`, `Fig.A.*`, `Fig.B.*` – figure assets referenced in the manuscript
- `cover_letter-cesys.tex` – submission cover letter for *Cleaner Environmental Systems*
- `Makefile` – build targets for abbreviating references and compiling the manuscript

## Build instructions

Requirements:

- TeX Live 2023 (or compatible LaTeX distribution)
- `latexmk`
- Python 3.10+ (virtual environment support)
- GNU Make
- Git (for the `bibtex-utils` submodule)

Regenerate the abbreviated bibliography and compile the manuscript:

```bash
make all
```

This target will:

1. Update the `bibtex-utils` submodule.
2. Create `.venv` (if absent) and install the CLI in editable mode.
3. Run `bibtex-utils abbreviate-with-ltwa --in-place` on `references.bib`.
4. Compile `manuscript.pdf` with `latexmk`.

You can run individual steps as needed:

- `make abbreviate` – refresh `references.bib` using the Typer CLI.
- `make pdf` – build only the LaTeX document (assumes references are already updated).
- `make distclean` – remove generated PDF and abbreviation report.

Direct `latexmk` commands remain useful for quick iterations, e.g.:

```bash
latexmk -pdf manuscript.tex
```

Clean auxiliary files with:

```bash
latexmk -C
```

## Reproducibility & code

All code and data for the decision support framework are hosted separately:

- GitHub: <https://github.com/UBC-FRESH/nbds_dss>
- Archived snapshot (Zenodo DOI) referenced in the manuscript (`nbds_dss_2025`)

Refer to those resources and the manuscript for full reproduction instructions.

## License

Unless otherwise noted, the manuscript text and figures in this repository will be released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license when the preprint is posted on EarthArXiv.
