## NBDS DSS Submission Readiness Checklist (Sustainable Futures)

| **Category** | **Status** | **Details & Notes** |
|--------------|------------|---------------------|
| Article type & length | ✅ Ready | Full-length article; texcount reports ~8,641 words (target 6,000–10,000). |
| Journal target | ✅ Ready | `\journal{Sustainable Futures}` set in `manuscript.tex`. |
| Title page & affiliations | 🔍 Verify | Frontmatter includes authors, emails, and full postal address; confirm corresponding author phone in portal. |
| Abstract | ✅ Ready | ~199 words; no citations in `manuscript.tex:61-67`. |
| Keywords | ✅ Ready | Tightened to 6 single-word/hyphenated keywords in `manuscript.tex`. |
| Highlights | ✅ Ready | Separate `highlights.txt` confirmed for EM; LaTeX highlights removed to avoid divergence. |
| Graphical abstract | 🔍 Verify | `nbds_dss_manuscript_graphical-abstract.pdf` present; confirm size/readability at 5×13 cm and non-AI origin. |
| Figures (files + naming) | ⚠️ Needs update | SF expects separate figure files with logical names (e.g., Figure_1.*). Current names include spaces and mixed formats (e.g., `fig 1.1.pdf`, `Fig.2.jpg`). Rename and update `\includegraphics` paths. |
| Tables | 🔍 Verify | LaTeX tables appear compliant (editable, captions). Ensure all tables cited and numbered in order. |
| References style | 🔍 Verify | `elsarticle-num-names` should render numeric [#]. Confirm compiled PDF uses square-bracket numbering and web refs include access dates. |
| Acknowledgements placement | ✅ Ready | Acknowledgements now immediately precede references. |
| CRediT roles | ✅ Ready | CRediT statement present `manuscript.tex:691-693`. |
| Competing interests | ⚠️ Needs update | Statement present in manuscript, but SF requires declarations tool docx upload during submission. |
| Funding statement | 🔍 Verify | Sponsor role statement added; confirm accuracy with authors. |
| Generative AI disclosure | 🔍 Verify | SF template wording added and placed before references; confirm policy for figures/graphical abstract. |
| Research data (Option C) | ✅ Ready | Zenodo DOI (10.5281/zenodo.17316315) includes all data and code required to reproduce results; GitHub linked for latest. |
| Ethics / consent | 🔍 Verify | Likely N/A; confirm and add statement if required. |
| Inclusive language / sex & gender analysis | 🔍 Verify | Do a quick scan to ensure compliance; add N/A note if appropriate. |
| Appendices numbering | 🔍 Verify | `\appendix` present; ensure lettered numbering for equations/figures/tables across all appendices. |
| Submission package | ⚠️ Needs update | Provisional EM package: LaTeX source (.tex/.bib/.bbl + nonstandard .sty), compiled PDF, separate figures, graphical abstract, cover letter PDF, `highlights.txt`. Finalize later. |
| Portal metadata | 🔍 Verify | Corresponding author details, ORCIDs, funding, and APC selection ready for entry. |

### Immediate Action Items
1. Update `\journal{Sustainable Futures}` and fix acknowledgements placement.
2. Align highlights (file + LaTeX block) and rename figure files to SF naming convention.
3. Update AI disclosure section title/wording and add sponsor role statement.
4. Confirm Option C data compliance (dataset deposit + citation or a clear non-share statement).
5. Rebuild manuscript PDF and verify references and appendix numbering.

### Submission Package Checklist
- [ ] Manuscript source: `manuscript.tex`, `references.bib`, class/style files
- [ ] Compiled PDF
- [ ] Separate figure files (renamed per SF guidance)
- [ ] `highlights.txt` (3–5 bullets, ≤85 chars)
- [ ] Graphical abstract file
- [ ] Declarations tool docx (competing interests)
