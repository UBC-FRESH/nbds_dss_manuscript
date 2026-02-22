## NBDS DSS Submission Readiness Checklist (Sustainable Futures)

| **Category** | **Status** | **Details & Notes** |
|--------------|------------|---------------------|
| Article type & length | ✅ Ready | Full-length article; texcount reports ~8,641 words (target 6,000–10,000). |
| Journal target | ✅ Ready | `\journal{Sustainable Futures}` set in `manuscript.tex`. |
| Title page & affiliations | 🔍 Verify | Frontmatter includes authors, emails, and full postal address; confirm corresponding author phone in portal. |
| Abstract | ✅ Ready | ~199 words; no citations in `manuscript.tex:61-67`. |
| Keywords | ✅ Ready | Tightened to 6 single-word/hyphenated keywords in `manuscript.tex`. |
| Highlights | ✅ Ready | Separate `highlights.txt` confirmed for EM; LaTeX highlights removed to avoid divergence. |
| Graphical abstract | ✅ Ready | `Graphical_Abstract.pdf` size 2000×800 pt (ratio matches 531×1328 px); embedded raster layers show >1000 dpi; non-AI confirmed by author; readability verified. |
| Figures (files + naming) | ✅ Ready | Renamed to `Figure_*.{pdf,jpg}` and paths updated; embedded raster layers show ~470+ dpi (e.g., Figure 2); legibility verified. |
| Tables | ✅ Ready | LaTeX tables are editable; captions/numbering consistent and all tables cited. |
| References style | ✅ Ready | Compiled PDF shows numeric square-bracket citations (e.g., [1], [2], [3]). |
| Acknowledgements placement | ✅ Ready | Acknowledgements now immediately precede references. |
| CRediT roles | ✅ Ready | CRediT statement present `manuscript.tex:691-693`. |
| Competing interests | ✅ Ready | Declarations tool docx prepared (`declarations-tool.docx`) with the manuscript statement. |
| Funding statement | 🔍 Verify | Sponsor role statement added; confirm accuracy with authors. |
| Generative AI disclosure | 🔍 Verify | SF template wording added and placed before references; confirm policy for figures/graphical abstract. |
| Research data (Option C) | ✅ Ready | Zenodo DOI (10.5281/zenodo.17316315) includes all data and code required to reproduce results; GitHub linked for latest. |
| Ethics / consent | 🔍 Verify | Likely N/A; confirm and add statement if required. |
| Inclusive language / sex & gender analysis | 🔍 Verify | Do a quick scan to ensure compliance; add N/A note if appropriate. |
| Appendices numbering | ✅ Ready | Appendix A/B/C numbering verified in compiled PDF (tables and figures). |
| Build status | ✅ Ready | `latexmk` build succeeded; box warnings resolved; `Figure_1.pdf` converted to PDF 1.5 to clear the pdfTeX inclusion warning. |
| Submission package | ✅ Ready | Updated package assembled in `sf_submission_package/` and `sf_submission_package.zip` (LaTeX source, .bib/.bbl, class/bst, PDF, figures, GA, `highlights.txt`). |
| Portal metadata | ✅ Ready | Corresponding author: Gregory Paradis; email: gregory.paradis@ubc.ca; phone: +1 (604) 822-1890; affiliation: Faculty of Forestry \& Environmental Stewardship, University of British Columbia; postal address already in frontmatter. |

### Immediate Action Items
1. Visual-check figure and graphical abstract readability at submission scale.
2. Decide whether to down-convert `Figure_1.pdf` to PDF 1.5 to clear the pdfTeX warning.
3. Verify numeric reference style and appendix numbering in the compiled PDF.
4. Prepare declarations tool docx for competing interests.
5. Finalize EM submission package contents (LaTeX sources, figures, GA, highlights, cover letter).

### Submission Package Checklist
- [x] Manuscript source: `manuscript.tex`, `references.bib`, class/style files
- [x] Compiled PDF
- [x] Separate figure files (renamed per SF guidance)
- [x] `highlights.txt` (3–5 bullets, ≤85 chars)
- [x] Graphical abstract file
- [x] Declarations tool docx (competing interests)
