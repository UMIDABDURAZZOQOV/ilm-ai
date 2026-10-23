# Chemistry QA: actual results

2026-10-24. Source mapping stage.

- Original files: SHA-256 and pypdf count recorded for all five.
- Every 817 PDF pages decoded; 320 scanned pages rendered and locally OCRed.
- Contents, bibliography, uncertain/scanned body heading images reviewed.
- Embedded-text heading checks, spread left/right mapping and eight grade8
  contents/body page discrepancies recorded in the canonical map.
- `load_catalog()` passes: 327 records, 268 source teaching entries.
- `python -m pytest -q tests/test_chemistry_sources.py`: **22 passed, 0.84s**.
- Reproducible original-file audit: **817 pages decoded**, source hashes/counts
  match the canonical map; source audit and all five grade maps regenerated.
- Interactive backend/Flutter/real PostgreSQL/native QA: not yet run in this stage.

No production data access, source PDF upload, main merge or deployment.
The scientific review queue is open; see SOURCE_REVIEW.md.
