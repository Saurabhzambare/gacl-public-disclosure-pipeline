# Source register and attribution

Sources were retrieved and visually inspected on 19 November 2026. The machine-readable register is config/sources.json.

## Dahej Plot 3 environmental compliance report

- Official PDF: https://gacl.com/wp-content/uploads/2026/04/EC_Compliance_Plot-3_April-to-Sept-25.pdf
- Reporting period: April–September 2025.
- Table: PDF page 5, printed page 4, condition 17.
- Measurement: monthly average freshwater consumption, KL/day.
- SHA-256: 4882f4e453a78fe956850944d9df2b636c74d225eab2331e7d8873fe4050c9c1.
- Six rows: April 12540.8; May 12621.3; June 12452.7; July 11818.3; August 11865.5; September 11738.1.
- Source scope is retained as dahej_plot3_report; no finer equipment attribution is assumed.
- The 2026 upload directory is not the measurement year.

## Business Responsibility and Sustainability Report FY 2025–26

- Official PDF: https://gacl.com/wp-content/uploads/2026/08/53RD-AR-BRSR.pdf
- Reporting periods extracted: FY 2025–26 and FY 2024–25.
- Boundary: standalone, confirmed on PDF page 1 / printed page 43 / item 13.
- Energy totals: PDF page 36 / printed page 78.
- Water withdrawal and consumption: PDF page 37 / printed page 79.
- Water discharge: PDF page 38 / printed page 80.
- SHA-256: 9fa0d33a69af711744590ad564145b93b2891e77f2e86004084bb89ba3390230.
- Six selected totals for each of two financial years = twelve rows.

Some labels in the BRSR do not survive text extraction. The implementation deliberately selects only visible, unambiguous total rows. The document-specific parser checks year-column order and exact row-match count. It does not pretend to support arbitrary reports or perform OCR.

## Retrieval metadata

Normal online runs write a retrieval sidecar with the actual retrieval time and checksum. Cached/offline runs do not invent a fresh retrieval time. The original setup used a direct verified download before this sidecar existed; run --refresh to generate sidecars for those original cached files.

## Source changes

A changed checksum stops execution before the cached report is overwritten. Review the changed document, page positions, definitions and comparative values, then update the manifest/parser in a reviewed commit. Retain the prior hash and history; never silently substitute new bytes.

## Rights

The original reports and GACL branding belong to their respective owners. The code license does not relicense the source documents. Link to official reports and download them locally instead of committing the PDFs.

## Phase 2 — same approved corpus, broader text retrieval

No new source is authorized or added by the AI extension. The local reference
index reads usable embedded text across these same two pinned PDFs: 71 physical
pages, 70 indexed text pages and 136 chunks. The monthly cover is image-only and
is recorded as skipped; OCR is not implemented. Indexing more text does not
mean every table, label or topic was extracted or evaluated correctly.

Physical and printed page numbers remain distinct. `config/retrieval.json`
contains additional version-pinned reviewed metadata for annual PDF pages 1 and
37, including the known printed mapping for page 1. Reviewed notes are exposed
separately from extracted text and must not be presented as automatic OCR or
freshly inferred source claims. Unknown mappings stay null.

The annual water-consumption note attributes an increase to production; that
annual statement does not establish a cause for the monthly site's decline.
The assistant may attribute explicit source explanations but must not infer
unreported operational causes. The existing 18 validated observations remain
the numerical route for answers. Adding another report, source version or
training dataset requires its own rights/provenance/boundary review.

The original source retrieval/inspection date above is historical. A new local
index build does not claim a fresh PDF download or source re-verification run
on the learner's laptop. Follow [build order](PHASE_2_BUILD_ORDER.md),
[contracts](AI_CONTRACTS.md) and [security](../SECURITY.md).


Comparative-basis note: printed BRSR pages 79–80 state that FY 2024–25 disclosures were recalculated for reporting-boundary and methodology alignment. Water consumption for that year was revised using withdrawal minus discharge. The project retains the latest report's disclosed figures and does not overwrite earlier-source history.
