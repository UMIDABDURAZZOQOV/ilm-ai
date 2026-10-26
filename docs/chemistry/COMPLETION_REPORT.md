# Chemistry 7–11: complete local interactive coverage

2026-10-26. **268/268 supplied-textbook teaching entries are implemented and
validated in isolated local QA.** This is not production release approval.

| Grade | Paragraphs | Digital laboratories | Digital practicals | Implemented |
| --- | ---: | ---: | ---: | ---: |
| 7 | 51 | 16 | 7 | 74/74 |
| 8 | 44 | 10 | 5 | 59/59 |
| 9 | 41 | 17 | 3 | 61/61 |
| 10 | 35 | 6 | 0 | 41/41 |
| 11 | 33 | 0 | 0 | 33/33 |
| Total | 204 | 49 | 15 | 268/268 |

The selected source map retains 29 chapters and 327 catalog records. Containers,
prefaces and review anchors are not extra teaching lessons. Grade 11 has no
separately labelled laboratory/practical entries in the supplied book; none were
invented. All 64 laboratory/practical entries are safe digital analysis activities.

## Authored learning and provenance

2,577 theory cards and 3,794 assessments: 1,057 MCQ, 537 short text, 1,135 fixed-unit
numeric, 359 formula, 706 equation. All 268 lessons have theory, MCQ and appropriate
FRQ. 191 have separate example blocks; the remaining 77 have no separate
example array. Applications may appear in theory and feedback: the
rechecked 8§26 cards work through mass ratios and 7§36 cards analyse equations;
7 laboratory 1 analyses a supplied property table without inventing measurements.
All 3,794 stored expected answers were regraded successfully
with the same server grader. Counts are not independent scientific certification.

Five supplied PDF SHA-256 values and 817 decoded PDF pages match the audited
sources. Every lesson/review digest was verified, along with 1,625 review-page
records against 781 exact original render files.
Grade 7 printed-page parity maps to the correct spread side; grades 8–11 retain
separate printed/PDF page fields. OCR remains a locator, not verified evidence.
Every scientific fact, question and explanation retains exact book/topic/page
references. Drafts never auto-publish. Original 7§1 and earlier batch hashes were
preserved at every continuation checkpoint.

A reviewed 9§40/186 erratum is supported by supplied-book corroboration
and the user's explicit correction; the immutable original hold/history remains.
220 scoped editorial review records retain uncertain/misprinted literals and
exclude them from accepted keys. Source checks remain enabled and tested.
For example, 8§26/114 explicitly uses the book's historical equivalent-mass
`g/mol` notation; the question labels it “kitobdagi g/mol”, and its existing scope
records that convention. Grade 11 equivalent-amount/unit models are explicit.
No unsupported scientific replacement was inferred from an OCR string.

## Executed QA

- Final Chemistry suite: 1,908 passed, 1 opt-in PostgreSQL skip, all 55 Chemistry
  test files once across 4 isolated SQLite databases; frozen source/runtime/test
  snapshot preserved. The opt-in PostgreSQL coverage was then run explicitly.
- Real PostgreSQL 16.14 on owned loopback staging: 3 passed / 4,310.58 s. Fresh random
  schemas tested additive legacy/OAuth migration, all 406 Biology mobile entries,
  idempotent Chemistry import of all 268 lessons, concurrent completion, once-only
  XP and preserved seeded legacy learner progress. No production database used.
  The owned PostgreSQL staging cluster was stopped after these checks.
- Final Flutter: 609 passed; analysis: 0 issues. Eight final 320×568 / 200% scenarios
  and 32 visually inspected captures cover long equations, word/numeric inputs,
  feedback and exact current/prior source locations. Earlier full-suite tests
  also cover landscape, keyboard insets, save/resume and other subjects.
- Actual loopback HTTP synthetic learner completed all 268 lessons across grades
  7–11, ending at 5,360 XP. Each batch preserved earlier progress and other grade
  catalogs; completion replay was identical and numeric equivalents agreed.
- Fresh Chemistry-only SQLite import: 268 created; repeat: 0 created / 268 skipped.
  All grade catalogs report their exact 74/59/61/41/33 completed entries.
- Critical Ruff/diff checks passed. Existing Starlette/httpx deprecation warnings
  are recorded; they were not hidden with a dependency upgrade.

## Readiness and boundaries

All five `course_ready` flags remain false because independent teacher review
and 220 editorial scopes remain open. Native Android / IME / TalkBack certification and
copy-spacing/editorial review are still pending. No claim of 10/10 UI/UX or
production approval is made. [2026 comparison](CURRICULUM_ALIGNMENT_2026.md)
documents official publication trails and structural differences; the selected
2017–2019 textbooks are not certified identical to every 2026 school programme.
The old 9§40 conflict mentioned in that dated comparison has since received the
controlled erratum; its historical record is retained.

No new AI, tutor, live generation or translation was added. Biology / Physics
branches, real user data, brand assets, main and production were not modified.
Only the Chemistry feature branches received commits. No source PDFs, full OCR,
raw full-text extracts, source renders, private logs, tokens or databases were pushed.

## Reproducible checkpoint

Final lesson batch backend: `45693b00901300abe058729da662a0294e6a2fe1`;
Flutter: `0312ff3108e96e1e3446bdc8c4dcb27fe7ecd37d`.
This documentation checkpoint follows those commits on
`feat/chemistry-curriculum`. See [measured batch 51](qa_batch51.json),
[final machine-readable QA](qa_final268.json), [progress](CURRICULUM_PROGRESS.md)
and [requirements](REQUIREMENTS.md). Future work should review retained source
issues and editorial/native accessibility gates; do not regenerate the 268 lessons,
disable validators or migrate/deploy production automatically.
