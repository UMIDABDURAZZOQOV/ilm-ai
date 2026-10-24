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
completed Chemistry7–11 course is claimed. That earlier checkpoint was1/268; see latest batch below.

No production data access, source PDF upload, main merge or deployment.
The scientific review queue is open; see SOURCE_REVIEW.md.


## Batch02 ? 2026-10-24

- Six reviewed lessons total (five newly authored): §2, practical1, practical2,
  §3, §4; source order and §1 bytes preserved. New batch:30 cards,32 MCQ,
  12 short-text FRQ,8 numerical FRQ, one formula and one worked example.
- Chemistry backend suite: **93 passed,1 existing Starlette/httpx warning,
  63.83s**. After the final source-wording edit, batch suite **24 passed,21.90s**.
  Earlier failing numeric expanded-decimal case fixed and rerun; both comma/dot,
  scientific notation, explicit units, bounds, invalid expressions, exact long
  replay fingerprints, ordered unlock, source gaps, once-only XP and preserved
  synthetic Biology137 XP/3 streak/2 stars are covered.
- **475 Flutter tests passed,2m02s** (full suite; two new numeric tests).
  New test uses public payloads captured from the real isolated backend and
  submits numeric FRQ at320x568 with200% text through the common flow.
- Static Flutter analysis **No issues found,101.3s**; critical Ruff passed.
- All five original PDF hashes/page counts rechecked; **817 pages decoded**.
  Catalogue still327 records/268 teaching entries,6 implemented,262 remaining,
  one unresolved grade9 source hold; all course-ready flags remain false.
- Fresh explicit local SQLite `chemistry_staging_batch02_final.db` imported
  all six reviewed documents. Legacy DB import emits existing missing-users
  migration diagnostics before fresh-table creation; schema creation and imports
  succeed. This is disposable staging only, not a production migration result.
- No fresh PostgreSQL/full-backend/web/native-device run in this batch. Earlier
  runs above are historical evidence, not rerun claims. Browser/IME/TalkBack and
  independent science-teacher sign-off remain unclaimed.


## Batch03 ? 2026-10-24

- Five additional reviewed lessons through grade7 §8, including practical3:
  **11/268 implemented,257 remaining**.28 new cards,32 MCQ,17 short-text FRQ,
  3 numerical FRQ. Prior committed lesson files are unchanged.
- Complete Chemistry suite now **95 passed,1 existing warning,93.38s**.
  The initial new test fixture wrongly supplied Biology's stars field to the
  separate ChemistryProgress model; corrected to best_score_pct and full suite
  rerun successfully. No runtime/schema change was required.
- New batch API tests complete and replay all52 new questions, verify sequential
  unlock and zero replay XP, and preserve the historical synthetic user.
- Fresh final local SQLite staging imported all11 unchanged reviewed lessons;
  five source hashes and817-page decode passed again. Critical Ruff passed.
- Flutter code/contract unchanged in this batch; prior475-test/clean-analysis
  result is historical evidence, not a new run. No new PG/native/browser claim.


## Batch04 — 2026-10-24

- Five additional source-reviewed lessons §9–13: **16/268 implemented,252
  remaining**. New batch30 cards,25 MCQ,11 short-text FRQ,14 numeric FRQ,
  2 formula FRQ and4 equation FRQ. Total16 lessons:96 cards and172 assessments
  (98 MCQ,43 short text,25 numeric,2 formula,4 equation).
- Final complete local Chemistry suite: **142 passed,1 existing Starlette/httpx
  warning,172.17s**, after editorial and UTF-8 guards. Earlier139/140-test runs
  and final45-test targeted guard run also passed; the142-test run is the final
  combined state. Critical Ruff passed.
- Full Flutter: **479 passed,2m12s**. Formula/equation public fixtures are captured
  from the actual isolated API. New tests submit typed Unicode notation at
  320x568/200% text and reject an attempt returned for a different lesson key.
- Final Flutter analyze: **No issues found,20.7s**. An intermediate missing import
  was caught, fixed and rerun; it is not counted as a passing run.
- Debug web build passed167.7s; rebuilt against the final corrected synthetic
  sandbox **183.9s**, `--debug --no-wasm-dry-run`. No release/WASM/native claim.
- Fresh final local QA imported all16 reviewed manifests. **Real HTTP** then
  completed all172 questions with the five supported response kinds:320 totalXP,
  identical repeated completion and no private keys in pre-answer content.
  Only synthetic900003 in the new private sandbox was used. Earlier QA snapshots
  and all real user data remain unchanged.
- Original source audit again verified five SHA identities and decoded817 pages.
  One blocking grade9 scientific hold and one scoped grade7 editorial issue are
  visible; ambiguous percentages are forbidden answer keys.
- Eight damaged apostrophes in four prior development manifests were restored,
  re-reviewed and SHA-pinned. Scientific keys are unchanged; first§1 bytes remain
  identical. Corrupted-copy regressions now reject embedded replacement marks.
- The build regenerated seven platform registrant files; these task-generated
  changes are restored to Chemistry HEAD and excluded from the feature commit.
  Dependency versions/lockfile and other subject worktrees are unchanged.
- No fresh PostgreSQL/full-backend/browser/native-device suite in this batch;
  older results remain historical. Native IME/TalkBack and teacher review are
  not certified. No source PDFs/OCR, credentials, production data or main merge.


## Batch05 — 2026-10-24

- Five new reviewed lessons §14–18, including both chapterI review anchors:
  **21/268 implemented,247 remaining**. Batch37 cards/64 assessments; total133
  cards/236 assessments (124 MCQ,54 short,45 numeric,5 formula,8 equation).
- Final complete Chemistry suite: **157 passed,1 skipped,1 existing warning,
  204.59s**. The opt-in PostgreSQL test was skipped; no fresh PostgreSQL claim.
  Final focused batch05 also passed15 tests/15.63s. Critical Ruff clean.
  An initial Windows wildcard invocation found no files; explicit file-list
  invocation produced the complete result above.
- Full Flutter suite with current Dart changes: **482 passed,1m44s**; analysis
  **No issues found,130.9s**. After final backend copy/coverage and sanitized
  fixture export, seven source tests passed again,4s, with320x568/200% captures.
  Actual widget images were visually inspected; source groups wrap separately.
- Prior-paragraph, chapter-review and practical source links retain actual book,
  topic, page and activity identity. Optional shared source labels preserve the
  existing default Biology behavior. No independent native/browser/IME/TalkBack
  or teacher certification is claimed. No fresh debug web build in this batch.
- Fresh final local staging sandbox imported all21 immutable manifests; real
  loopback HTTP completed **236 questions/420 once-onlyXP**, identical repeated
  completion and hidden private grading before submission. Synthetic900003 only.
  A separate earlier continuity run preserved16 completions/320XP then added5
  lessons/100XP; its60-question new-batch copy predates the final64 questions.
  These are distinguished rather than misreported as the same run.
- Original five PDF hashes verified and817 pages decoded again. Source holds:
  one scientific blocker and two scoped editorial issues. Readiness also checks
  these issues, so file counts alone cannot enable a complete course.
- Existing development imports/snapshots and real users are unchanged. Original
  §1 bytes remain unchanged. Only separate Chemistry feature branches are used.
  No PDF/OCR/fulltext/token upload, production DB/deploy or main merge.
