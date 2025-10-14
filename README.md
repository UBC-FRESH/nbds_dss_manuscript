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
- `Makefile` – build targets for compiling the manuscript (`make pdf`)

## Build instructions

Requirements:

- TeX Live 2023 (or compatible LaTeX distribution)
- `latexmk`

Build the manuscript PDF:

```bash
latexmk -pdf manuscript.tex
```

This produces `manuscript.pdf` with the EarthArXiv cover page followed by the CES-formatted article. Clean auxiliary files with:

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
