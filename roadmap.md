# Sustainable Futures Transfer Submission Roadmap

- [ ] Phase 1 — Requirements alignment
  - [x] Task 1.1 — Confirm article type and scope fit
    - [x] Subtask 1.1.1 — Confirm full-length article target (6,000–10,000 words)
    - [x] Subtask 1.1.2 — Record current word count in readiness checklist
  - [d] Task 1.2 — Reconfirm SF guide requirements (file formats, highlights, data policy)
    - [x] Subtask 1.2.1 — Confirm highlights must be a separate file in EM
    - [ ] Subtask 1.2.2 — Confirm Option C data policy requirements
    - [ ] Subtask 1.2.3 — Confirm AI policy for text vs. figures/graphical abstract
  - [d] Task 1.3 — Capture any portal-specific items (declarations docx, APC, ORCID, phone)
    - [d] Subtask 1.3.1 — List required upload items (manuscript source, PDF, figures, highlights, GA)
    - [ ] Subtask 1.3.2 — Capture portal metadata needs (ORCID, phone, APC selection, funding)
    - [x] Subtask 1.3.3 — Update readiness checklist with portal items

- [ ] Phase 2 — Manuscript compliance updates
  - [ ] Task 2.1 — Update journal target
    - [x] Subtask 2.1.1 — Change `\journal{Cleaner Environmental Systems}` → `Sustainable Futures`
  - [ ] Task 2.2 — Declarations & policy sections
    - [x] Subtask 2.2.1 — Rename AI disclosure section to SF-required title and align wording
    - [x] Subtask 2.2.2 — Add sponsor role statement to Funding section
    - [x] Subtask 2.2.3 — Move Acknowledgements to directly precede references
  - [ ] Task 2.3 — Keywords and highlights alignment
    - [x] Subtask 2.3.1 — Tighten keywords to 1–7, prefer single-word terms
    - [x] Subtask 2.3.2 — Remove LaTeX highlights block; rely on `highlights.txt` only
  - [ ] Task 2.4 — Data policy compliance (Option C)
    - [x] Subtask 2.4.1 — Confirm dataset deposit and add explicit dataset citation/link
    - [ ] Subtask 2.4.2 — If data cannot be shared, add a clear reason statement
  - [ ] Task 2.5 — Appendix numbering and references
    - [x] Subtask 2.5.1 — Verify lettered numbering for appendix figures/tables/equations
    - [x] Subtask 2.5.2 — Confirm numeric reference style in compiled PDF
  - [x] Task 2.6 — Label hygiene (descriptive, stable labels)
    - [x] Subtask 2.6.1 — Replace numeric equation labels (e.g., eq:7) with descriptive names
    - [x] Subtask 2.6.2 — Replace numeric figure/table/section labels with descriptive names
    - [x] Subtask 2.6.3 — Update all cross-references after relabeling

- [ ] Phase 3 — Figures, tables, and assets
  - [ ] Task 3.1 — Figure file hygiene
    - [x] Subtask 3.1.1 — Rename figures to SF naming convention (e.g., `Figure_1.pdf`)
    - [x] Subtask 3.1.2 — Update all `\includegraphics` paths
    - [d] Subtask 3.1.3 — Confirm resolution/legibility and non-AI provenance
  - [ ] Task 3.2 — Graphical abstract
    - [d] Subtask 3.2.1 — Verify size/readability at 5×13 cm
  - [ ] Task 3.3 — Tables
    - [ ] Subtask 3.3.1 — Ensure tables are cited, numbered, and editable

- [ ] Phase 4 — Build and package
  - [ ] Task 4.1 — Rebuild manuscript PDF
  - [ ] Task 4.2 — Assemble submission package (LaTeX source, figures, highlights, GA)
  - [ ] Task 4.3 — Final QA pass (spelling/grammar, references, checklist items)

- [ ] Phase 5 — Portal submission prep
  - [ ] Task 5.1 — Declarations tool docx (competing interests) ready to upload
  - [ ] Task 5.2 — Corresponding author details (email, postal address, phone)
  - [ ] Task 5.3 — APC funding/waiver decision documented
  - [ ] Task 5.4 — Record submission ID/date after upload

## Notes — Narrative Anchor (Draft)
We are arguing that many forest restoration/reforestation projects are “ghost projects”: locally they appear slightly negative NPV, so they never gain a champion and never reach the candidate‑project stage. A global actor with strong biodiversity/carbon (and possibly social) commitments may value these benefits more highly than local actors, effectively shifting the marginal value of outcomes and turning some “almost viable” ghost projects into investable real options. The DSS framework is positioned as a scalable way to scan the solution space, identify these near‑threshold opportunities, and surface candidates that become viable once broader global benefits are priced in.

## Notes — Label Hygiene
Current equation/figure/table/section labels include numeric patterns (e.g., `eq:7`) that are already out of sync with the rendered numbering. This defeats the purpose of stable, descriptive LaTeX labels and should be corrected.
