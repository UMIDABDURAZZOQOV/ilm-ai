# Chemistry QA: actual results

2026-10-24. Source mapping plus first-paragraph isolated integration.

- Original files: SHA-256 and pypdf count recorded for all five.
- Every 817 PDF pages decoded; 320 scanned pages rendered and locally OCRed.
- Contents, bibliography, uncertain/scanned body heading images reviewed.
- Embedded-text heading checks, spread left/right mapping and eight grade8
  contents/body page discrepancies recorded in the canonical map.
- `load_catalog()` passes: 327 records, 268 source teaching entries.
- `python -m pytest -q tests/test_chemistry_sources.py`: **22 passed, 0.84s**.
- Reproducible original-file audit: **817 pages decoded**, source hashes/counts
  match the canonical map; source audit and all five grade maps regenerated.

## First paragraph and backend

- Explicit reviewed index:one lesson,8 cards,9 MCQ,3 short-text FRQ,18 fact entries.
  Source pages3–8/PDF2:right throughPDF5:left were read as original images.
- Final Chemistry suite:**69 passed,1 existing Starlette/httpx deprecation warning,
  59.49s**. Source/region/OCR/bibliography tampering, taught-fact links, aliases,
  input limits, private-key hiding, authenticated ownership, immutable snapshots,
  order, expiry, changed replay, failed/new attempts, atomic once-only XP,
  immutable imports, prerequisite gaps and DB-free dry-run are covered. The known
  grade9 §40 contradiction is machine-blocked; deleting its hold also fails validation.
- Existing learner42 retained137 XP,3-day streak and2-star Biology progress in
  synthetic regression fixtures. No real learner database was used.
- Initial Windows checkout had CRLF in SHA-pinned Biology JSON. The original Git
  blobs were verified and restored in the Chemistry worktree; no Biology content
  diff was staged. Both preserved-baseline tests then passed (**2 passed,36.67s**).
  `.gitattributes` now preserves LF for reviewed manifests across Windows checkout.
- Critical Ruff E9/F63/F7/F82:**All checks passed**.
- Full backend run:**646 passed,3 opt-in PostgreSQL skips,14 existing warnings,
  2392.50s**; its two failures were the initial CRLF checkout SHA checks described
  above. Both were rerun after exact Git-byte restoration and passed. The later
  69-case Chemistry suite includes the final bibliography/import/source-hold safeguards.
  The full run and the targeted rechecks are reported separately.

## Actual HTTP and PostgreSQL

- A new outside-Git sandbox created only synthetic learner900003 and a separate
  chemistry_staging SQLite database. Real loopback HTTP start/12 answers/complete
  produced11/12,3 stars,20 XP; repeated complete returned the identical result.
  The pre-submission payload contained no private rubric/expected answer.
- Actual private PostgreSQL16.14 ran on127.0.0.1:15437 with its own cluster/database.
  Chemistry additive schema/install/reimport, private snapshots, parallel complete,
  once-only20 XP and preserved Biology rows passed. Existing OAuth/migration test
  also passed. The old406-lesson mobile test completed its bulk exercise but its
  original15-minute test JWT expired before the last tree query. It was rerun with
  a test-only120-minute token; production token settings were not changed.
- Final PostgreSQL bulk rerun:**1 passed,1 existing warning,1262.90s**. Together
  with the two earlier passing Chemistry/OAuth cases, all three opt-in PostgreSQL
  cases passed. The full406-lesson/47-checkpoint exercise, mobile replay/reimport,
  final parallel complete and preserved137-XP/2-star historical learner passed.

## Flutter and visual review

- Final full Flutter suite:**473 passed,1m41s**, including20 new Chemistry checks.
- Final static analysis:**No issues found,86.8s**.
- New checks cover explicit debug/loopback gates, public schema/version/source
  contracts, one-card theory, spread citations, server MCQ/FRQ, ambiguous-network
  payload replay, saved request ID/text, account separation, shared exit dialog,
  expiry, common result/answer review and small/landscape200% text. A completed
  lesson says "Review lesson" when reopened; it does not promise an old result on
  a device without that attempt's saved request ID.
- UZ/RU/EN,light/dark,320x568 and640x360 widget checks passed. Ten original app UI
  captures (theory,MCQ,FRQ,feedback,result in both themes) were visually inspected.
  They contain original authored app text, not textbook page images.
- Separate debug web build:**Built build/web,548.5s**, using only the separate
  Chemistry entrypoint and private synthetic-account defines. Existing
  flutter_secure_storage_web/flutter_tts WASM dry-run incompatibility warnings
  remain; the standard JavaScript debug build succeeded. No WASM build is claimed.
- Final rebuild after the completed-lesson label fix and sandbox-token refresh:
  **Built build/web,120.2s**, `--debug --no-wasm-dry-run`; local artifacts only.
- Loopback web server7358 returned HTTP200 for index.html and main.dart.js.
  Automated browser QA was attempted twice; the browser-use webview could not
  attach (timeouts). No actual browser-render/interaction pass is claimed.
- Native Android/phone, real IME and TalkBack QA have not been performed. Widget
  layout/keyboard behavior is not represented as native accessibility sign-off.

The isolated adapters use the pinned Physics common v2 contract and existing ILM
AI source/choice/feedback/result/exit components; no production FRQ capability or
completed Chemistry7–11 course is claimed. Exact progress remains1/268.

No production data access, source PDF upload, main merge or deployment.
The scientific review queue is open; see SOURCE_REVIEW.md.
