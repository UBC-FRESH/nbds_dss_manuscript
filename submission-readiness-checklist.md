## NBDS DSS Submission Readiness Checklist (Sustainable Futures)

| **Category** | **Status** | **Details & Notes** |
|--------------|------------|---------------------|
| Article type & length | ✅ Ready | Full-length article; texcount reports ~8,641 words (target 6,000–10,000). |
| Journal target | ✅ Ready | `\journal{Sustainable Futures}` set in `manuscript.tex`. |
| Title page & affiliations | 🔍 Verify | Frontmatter includes authors, emails, and full postal address; confirm corresponding author phone in portal. |
| Abstract | ✅ Ready | ~199 words; no citations in `manuscript.tex:61-67`. |
| Keywords | ✅ Ready | Tightened to 6 single-word/hyphenated keywords in `manuscript.tex`. |
| Highlights | ✅ Ready | Separate `highlights.txt` confirmed for EM; LaTeX highlights removed to avoid divergence. |
| Graphical abstract | 🔍 Verify | `Graphical_Abstract.pdf` size 2000×800 pt (ratio matches 531×1328 px); non-AI confirmed by author; visual readability check still pending. |
| Figures (files + naming) | 🔍 Verify | Renamed to `Figure_*.{pdf,jpg}` and paths updated; sample sizes ok and `Figure_2.jpg` is 2550×3300 at 300 DPI; visual legibility check still pending. |
| Tables | 🔍 Verify | LaTeX tables appear compliant (editable, captions). Ensure all tables cited and numbered in order. |
| References style | ✅ Ready | Compiled PDF shows numeric square-bracket citations (e.g., [1], [2], [3]). |
| Acknowledgements placement | ✅ Ready | Acknowledgements now immediately precede references. |
| CRediT roles | ✅ Ready | CRediT statement present `manuscript.tex:691-693`. |
| Competing interests | ⚠️ Needs update | Statement present in manuscript, but SF requires declarations tool docx upload during submission. |
| Funding statement | 🔍 Verify | Sponsor role statement added; confirm accuracy with authors. |
| Generative AI disclosure | 🔍 Verify | SF template wording added and placed before references; confirm policy for figures/graphical abstract. |
| Research data (Option C) | ✅ Ready | Zenodo DOI (10.5281/zenodo.17316315) includes all data and code required to reproduce results; GitHub linked for latest. |
| Ethics / consent | 🔍 Verify | Likely N/A; confirm and add statement if required. |
| Inclusive language / sex & gender analysis | 🔍 Verify | Do a quick scan to ensure compliance; add N/A note if appropriate. |
| Appendices numbering | ✅ Ready | Appendix A/B/C numbering verified in compiled PDF (tables and figures). |
| Build status | ✅ Ready | `latexmk` build succeeded; `Figure_1.pdf` converted to PDF 1.5 to clear the pdfTeX inclusion warning. |
| Submission package | ⚠️ Needs update | Provisional EM package: LaTeX source (.tex/.bib/.bbl + nonstandard .sty), compiled PDF, separate figures, graphical abstract, cover letter PDF, `highlights.txt`. Finalize later. |
| Portal metadata | 🔍 Verify | Corresponding author details, ORCIDs, funding, and APC selection ready for entry. |

### Immediate Action Items
1. Visual-check figure and graphical abstract readability at submission scale.
2. Decide whether to down-convert `Figure_1.pdf` to PDF 1.5 to clear the pdfTeX warning.
3. Verify numeric reference style and appendix numbering in the compiled PDF.
4. Prepare declarations tool docx for competing interests.
5. Finalize EM submission package contents (LaTeX sources, figures, GA, highlights, cover letter).

### Submission Package Checklist
- [ ] Manuscript source: `manuscript.tex`, `references.bib`, class/style files
- [ ] Compiled PDF
- [ ] Separate figure files (renamed per SF guidance)
- [ ] `highlights.txt` (3–5 bullets, ≤85 chars)
- [ ] Graphical abstract file
- [ ] Declarations tool docx (competing interests)
