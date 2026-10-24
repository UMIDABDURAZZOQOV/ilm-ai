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


## Batch06 — 2026-10-24

- Five new lessons: §19–22 plus practical4; chapterII review is integrated with
  exact source identity. **26/268 implemented,242 remaining**;171 cards/288
  assessments total (146 MCQ,67 short,54 numeric,7 formula,14 equation).
  Batch06 adds38 cards/52 questions, including6 equation tasks.
- Final complete Chemistry suite: **168 passed,1 skipped,1 existing warning,
  370.05s**. The skip is opt-in PostgreSQL, not a passing database run. Critical
  Ruff clean. Initial four failures were the new test treating the grader's
  string result as a dictionary; that test assertion was corrected before this
  final full run. No grader behavior changed to make the test pass.
- Full Flutter suite rerun: **482 passed,2m26s**. No Dart changes in batch06;
  the preceding clean analysis/source-widget results remain historical. No fresh
  native/browser/web-build/PostgreSQL/IME/TalkBack/teacher certification claimed.
- Real loopback HTTP appended five immutable manifests and answered52 new
  questions correctly. Prior21 completed lessons/420XP preserved; added100XP,
  total26/520XP. Repeated completion identical; pre-answer grading stays private.
  Only synthetic900003 in the existing private final sandbox was used.
- All817 original PDF pages decoded and five SHA identities verified again.
  Three chapter-review anchors integrated in total. One scientific hold and four
  scoped editorial issues are visible and gate whole-course readiness.
- New source guards reject the unapproved silane equation and starred oxygen
  attribution as answers. Source heading transcription corrected on62. All other
  source order/counts unchanged. Original §1 and imported prior snapshots remain
  unchanged. Full course readiness is false; no production or real-user action.


## Batch07 — 2026-10-24

- Five new lessons §23–27 plus both chapterIII review anchors: **31/268
  implemented,237 remaining**. Batch40 cards/55 questions; total211 cards/343
  assessments (163 MCQ,75 short,68 numeric,11 formula,26 equation).
- Full Chemistry **188 passed,1 skipped,1 existing warning,464.06s**. Skip is
  opt-in PostgreSQL, not a fresh database certification. After one plain-language
  water-prompt edit, final targeted20 tests passed again/28.91s. Scientific keys,
  options, grading and source identity did not change; SHA evidence renewed.
  Critical Ruff passed. Existing first§1 remains byte-identical.
- Final full Flutter **484 passed,104s** after the shared optional feedback-source
  slot and refreshed real API fixtures. Analysis **No issues found,118.7s**.
  Earlier484-test/144s run preceded the optional source slot and is superseded.
  Two final320px/200% water tests passed; source dialog resolves80→PDF41:left
  and feedback82→PDF42:left. Captured widget images were inspected visually.
- Chemistry feedback now supplies exact source links to the common scrollable
  panel; other callers retain the default absent slot. Hydrate is a recognition
  MCQ rather than unsupported formula input. Long prompt simplified in original
  Uzbek; source/key preserved. Both explanation and source scroll above the fixed
  continue action. No browser/native/IME/TalkBack/teacher certification claimed.
- Earlier continuity HTTP run preserved26 completions/520XP and added5/100XP.
  Final fresh immutable sandbox then completed **all31 lessons/343 questions/
  620 once-onlyXP** over real loopback HTTP, replay identical and private grading
  hidden. Old sandbox/attempt snapshots remain intact; synthetic900003 only.
- Original817 pages decoded and five hashes verified again; five review anchors
  integrated. One scientific blocker and nine scoped editorial issues remain
  visible, including a future-topic ocean-volume discrepancy. Course readiness
  is false; source mapping and JSON counts do not mean a whole course is ready.
- No fresh web build/PostgreSQL/full-backend or native suite in this batch. No
  PDF/OCR/fulltext/token upload, production DB/deploy, main merge, live AI or
  real-user/other-subject branch operation.


## Batch08 — 2026-10-24

- Five new lessons §28–32:**36/268 implemented,232 remaining**. Batch35 cards/
  42 questions (19 MCQ,11 short,12 numeric); total246 cards/385 assessments
  (182 MCQ,86 short,80 numeric,11 formula,26 equation). No artificial formula
  FRQ added to non-calculation conservation/water-source topics.
- Full Chemistry **208 passed,1 skipped,1 existing warning,263.72s**. Initial
  targeted batch20 passed/18.30s. Skip is opt-in PostgreSQL; no fresh PG claim.
  Critical Ruff clean. Original §1 bytes remain unchanged.
- Full Flutter **486 passed,74s**; analysis **No issues found,117.8s**. Two
  real-payload molarity tests at320px/200% passed; final recapture also2 passed/3s
  after ensuring the fixed-unit helper is fully visible. Initial assertion sought
  a standalone mol/l widget; the existing input helper includes it in a sentence,
  so the assertion was corrected. No production widget change in this batch.
- Actual screenshots inspected:0,4 input,visible mol/l helper and check button;
  feedback source91→PDF46:right; prior molar-mass source34→PDF18:left. Client
  submits the exact comma string; correctness and unit-fixed numeric rubric stay
  on server. No general unit conversion or native/browser/IME certification.
- Real loopback HTTP preserved31 completed lessons/620XP,appended five immutable
  lessons and answered all42 new questions. Added100 once-onlyXP,total36/720XP;
  completion replay identical and private grading hidden. Only synthetic900003
  in the private8900 sandbox used; existing rows/snapshots and real users intact.
- All817 original pages decoded and five hashes verified again. Open review still
  one scientific blocker and nine scoped editorial issues. Source86 enlarged
  image confirms375000000km²; provisional digit concern was not a book error.
  Disputed ocean-volume variants are rejected as keys. Course readiness false.
- No current drinking-water/clinical advice or home chlorination instructions.
  Source87 plot units are not silently interchanged with per100g solvent values.
  No fresh web build/PostgreSQL/full-backend/native suite,PDF/OCR/token upload,
  real-user operation,production/main/other-subject branch action or AI feature.


## Batch09 — 2026-10-24

- Practical5 plus§33–36 and both chapterIV review anchors:**41/268 implemented,
  227 remaining**. Batch37 cards/51 questions (19 MCQ,7 short,10 numeric,7 formula,
  8 equation); total283 cards/436 assessments (201 MCQ,93 short,90 numeric,
  18 formula,34 equation). Seven review anchors integrated,not extra lessons.
- Full Chemistry **228 passed,1 skipped,1 existing warning,515.21s**. Targeted
  batch20 passed/19.38s. Skip is opt-in PostgreSQL; no fresh PG certification.
  Critical Ruff clean. Original§1 unchanged by byte comparison.
- Full Flutter rerun **486 passed,86s**. No Dart/fixture change this batch; prior
  clean analysis117.8s and widget captures remain historical,not rerun claims.
  Existing UI/common learning contract preserved; no new teaching mechanism.
- Real HTTP preserved36 completions/720XP,appendedfive immutable manifests and
  passed all51 new questions. Added100XP once,total41/820XP; completion replay
  identical,private grading hidden. Synthetic900003 only in private8900 sandbox.
  Real user/Biology progress and old source-copy snapshots remain unchanged.
- Both practical components retained:solution calculations/label/report and
  supplied soil-filtrate/litmus observation. No physical reagent setup or invented
  universal-indicator result. Original-page evidence corrects source99's bad§9
  pointer to actual§7/26 without changing the classification fact.
- All817 original PDF pages decoded and five SHA identities verified again.
  One scientific hold and13 scoped editorial issues now visible. Held soil colour,
  hot-vapour state,Fr phase and imprecise Fe/O premise never become approved keys.
  All whole-course flags false; JSON coverage is not full scientific readiness.
- Material equations including parenthesized basic copper carbonate were checked
  for atom balance. Accepted typed variants include subscript digits,term order,
  arrow spelling and proportional integer coefficients; no general structural/
  ionic/reaction-prediction engine is claimed.
- No fresh web/native/browser/IME/TalkBack/teacher/full-backend/PostgreSQL suite,
  production/main/real-user/other-subject action,PDF/OCR/token upload or AI feature.


## Batch10 — 2026-10-24

- §37–41:**46/268 implemented,222 remaining**. Grade7:46/74. Batch29 cards/
  43 questions (16 MCQ,8 short,3 numeric,10 formula,6 equation). Total312 cards/
  479 assessments (217 MCQ,101 short,93 numeric,28 formula,40 equation).
- Full Chemistry **251 passed,1 skipped,1 existing warning,228.75s**. The skip
  is opt-in PostgreSQL;no fresh PG claim. Initial targeted run had one test-only
  metadata-path typo (20 others passed);fixed before the full passing run.
  An earlier slow full run was intentionally interrupted,not counted as passing.
  Critical Ruff and diff whitespace checks pass. Original§1 byte diff is empty.
- Full Flutter **486 passed,252s**. No Dart change/new visual certification.
  Previous clean analysis117.8s and widget captures remain historical evidence.
- Synthetic real loopback HTTP:preserved41 completions/820XP,passed43 new
  questions,added100XP once,total46/920XP. Completion replay identical;private
  grading hidden. Old rows/source snapshots and real Biology users preserved.
- Added a batch importer to validate the entire pinned index before any write,
  then import the verified in-memory snapshot. No caller document/skip-validation
  parameter or persistent cache. Every call revalidates evidence;all per-row
  immutable-content/assessment checks remain. Fixture,CLI and local QA server
  use it to avoid repeatedly validating the whole curriculum for each lesson.
  Tests prove one validation/call,revalidation on repeat,pre-write failure and
  rejection of a changed stored lesson. Single-document guard remains intact.
- All817 PDF pages decoded,five SHA identities verified. One scientific hold
  and15 editorial issues remain visible,including supplied-book gemstone-host
  conflict and grade9 unbalanced KOH equation. No disputed correction inserted.
- No new general notation engine,AI,production/main/real-user/other-subject work,
  PDF/fulltext/OCR/token upload,teacher/native/browser/IME/TalkBack/full-backend
  or PostgreSQL certification. Whole-course readiness stays false.


## Batch11 — 2026-10-24

- §42–44,practical6,§45:**51/268 implemented,217 remaining**. Grade7:51/74.
  New39 cards/53 questions:16 MCQ,11 short,8 numeric,10 formula,8 equation.
  Total351 cards/532 assessments:233 MCQ,112 short,101 numeric,38 formula,
  48 equation. Seven reviews integrated;earlier review reuse adds no entry.
- Full Chemistry **277 passed,1 skipped,1 existing warning,207.49s**;targeted
  **26 passed/17.06s**. PG skip remains opt-in. Critical Ruff/diff checks pass.
  Original§1 unchanged. Explicit review context must precede the lesson and
  already be integrated in an earlier indexed manifest. Tests reject future
  anchors,missing prior integration,legacy symbols and held basicity assertions.
- Full Flutter **488 passed/89s**;analysis **no issues/87.3s**. Two new real-widget
  tests/2s with sanitized real-HTTP practical6 fixtures. At320×568/200% text,
  earlier review context/feedback retains actual50→PDF26left and title/null
  paragraph,not false§6. Light theory/dark feedback captures visually inspected;
  source and continue are readable. Not native/browser/IME/TalkBack certification.
- Real loopback HTTP preserved46 completions/920XP,passed53 new questions,
  added100XP once,total51/1020XP. Completion replay identical;private grading
  hidden. Public fixture strips live attempt identity/expiry and contains no
  token/private pre-answer key. Only synthetic900003,real users unchanged.
- All817 original PDF pages decoded,five SHA identities verified again. Nineteen
  scoped editorial issues plus one scientific blocker remain open. No guessed
  iodine/basicity/product/density/condition repair or missing-keyword definition.
- Practical6 preserves both oxide branches as digital analysis. Copper equation
  and mass data are actual earlier50 evidence,not a fabricated quotation121.
  No physical lab/reagent setup,boiling/heating,unprovided observation,clinical,
  storage or harmful synthesis procedure. Existing learning/XP/grader unchanged.
- No production/main/real-user/other-subject/AI/PDF/fulltext/OCR/token upload or
  fresh independent teacher/PG/full-backend certification;all course-ready false.


## Batch12 — 2026-10-24

- §46–50/chapterV review:**56/268 implemented,212 remaining**. Grade7:56/74.
  New42 cards/59 questions:18 MCQ,10 short,12 numeric,11 formula,8 equation.
  Total393 cards/591 assessments:251 MCQ,122 short,113 numeric,49 formula,
  56 equation. Eight reviews integrated,not extra teaching entries.
- Final full Chemistry **306 passed,1 skipped,1 existing warning,221.15s**.
  Target **29 passed/23.31s**. Initial full run:305 passed/one test-only failure
  because batch11 counted future review anchors. Fixed its assertion to its own
  51-lesson slice (batch12 similarly56);final full rerun passes. Critical Ruff
  clean. Original§1 unchanged;only new manifests and explicit QA/docs changed.
- Full Flutter **488 passed/94s**. No Dart change in this batch;analysis clean
 87.3s and prior200% captures are batch11 evidence,not new native/visual claims.
- Real HTTP preserved51 completions/1020XP,passed59 new questions,added100XP
  once,total56/1120XP. Completion replay identical,private grading hidden.
  Synthetic900003 only;previous immutable source/attempt snapshots preserved.
- All817 PDF pages decoded,five source SHA identities verified. One scientific
  blocker and23 scoped editorial issues remain. Missing Cu,legacy iodine,
  sulfur/CO2 typo,unexplained rounding/state/clinical/current scopes are held.
- Compound/reaction conditions are explicit. Condensed/grouped formulas are
  finite reviewed spellings;hydrate-dot/complex/double-salt forms remain
  recognition. No new ionic/structural/prediction/AI mechanism. Equivalent g
  questions use the source's worked one-equivalent-mass models,not gas volumes
  or universal E claims;98/3 is exact,not a silently corrected decimal key.
- No production/main/real-user/other-subject/PDF/OCR/fulltext/token operation,
  fresh independent teacher/PG/native/browser/IME/TalkBack/full-backend
  certification. Whole-course flags remain false.


## Batch13 — 2026-10-24

- §51,practical7,labs1–3:**61/268 implemented,207 remaining**. Grade7:61/74.
  New24 cards/39 questions:15 MCQ,8 short,5 numeric,4 formula,7 equation.
  Total417 cards/630 assessments:266 MCQ,130 short,118 numeric,53 formula,
  63 equation. Nine chapter reviews integrated,not extra teaching entries.
- Full Chemistry **325 passed,1 skipped,1 existing warning,409.04s**. Targeted
  **19 passed/22.03s**. Critical Ruff/diff checks clean;original§1 unchanged.
  Distinct lab keys/prerequisites,digital policy,clinical hold,CO2-product scope,
  explicit rounding,typed grouping and preservation of56 prior completions tested.
- Full Flutter **490 passed/137s**;analysis **no issues/65.2s**. Two new real-widget
  tests/1s use sanitized actual-HTTP lab1 fixtures. At320×568/200% text,Lab1 source
  label and147→PDF74right are correct,not false§1. Light source/dark short-FRQ
  feedback captures visually inspected. No native/browser/IME/TalkBack claim.
- Real HTTP preserved56 completions/1120XP,passed39 new questions,added100XP
  once,total61/1220XP. Completion replay identical,grading private. Synthetic
 900003 only;public fixtures have fake attempt identity/future expiry,no tokens
  or private pre-answer keys. Real user data and previous snapshots unchanged.
- All817 pages decoded,five SHA identities verified. One scientific blocker and
 25 editorial reviews remain. Clinical recipe,powder purity and unspecified
  review CO2-product/loss assumptions are held. No gap/observation invented.
- Laboratories use the existing common MCQ/FRQ/XP flow with activity labels.
  Blank147 table is not filled with fabricated values;all three physical and
  chemical lab components remain digital classification. Original chain144
  solution cites earlier method/formulas;it is not a hidden correction of130.
- No new AI,notation/prediction engine,production/main/other-subject/real-user/
  PDF/OCR/fulltext/token operation or fresh teacher/PG/full-backend certification.
  All whole-course-ready flags remain false.


## Batch14 — 2026-10-24

- Labs4–11:**69/268 implemented,199 remaining**. Grade7:69/74,last5 labs remain.
  New28 cards/51 questions:20 MCQ,11 short,3 numeric,8 formula,9 equation.
  Total445 cards/681 assessments:286 MCQ,141 short,121 numeric,61 formula,
  72 equation. Nine integrated chapter reviews,not extra teaching entries.
- Full Chemistry **345 passed,1 skipped,1 existing warning,673.17s**. Final
  target **20 passed/45.69s**. Initial target19 passed/one test-only expected-code
  error:lowercase cu is invalid chemical syntax,not a well-formed wrong formula.
  Test corrected to existing invalid_answer behaviour;grader unchanged. Critical
  Ruff clean;original§1 and prior61 manifest bytes unchanged.
- Full Flutter **490 passed/218s**. No Dart/fixture change in this batch;latest
  analysis65.2s and200% lab captures belong to batch13,not a new visual claim.
- Real HTTP preserved61 completions/1220XP,passed51 new questions,added160XP
  once,total69/1380XP. Completion replay identical;private grading hidden.
  Synthetic900003 only,real users/previous immutable snapshots unchanged.
- All817 source pages decoded,five SHA identities verified. One scientific
  blocker and25 editorial reviews remain. No invented blank-table values,
  physical observations,efficiency figures or silent correction.
- Original Fe/CuCl2 and full-neutralisation balancing models explicitly give
  products and cite earlier rule/formula evidence. Printed Zn/HCl and CuO/H2
  equations remain exact source contexts. Shared MCQ/FRQ/XP/prerequisite/replay
  unchanged;no new teaching or notation/prediction/AI mechanism.
- No actual heat/flame/acid/gas/mercury handling,clinical/pest procedure,
  production/main/real-user/other-subject/PDF/OCR/fulltext/token operation or fresh
  teacher/native/browser/IME/TalkBack/PG/full-backend certification. Ready false.


## Batch15 — 2026-10-24

- Labs12–16:all74 grade7 teaching entries implemented;**74/268,194 remaining**.
  New17 cards/33 questions:10 MCQ,6 short,2 numeric,6 formula,9 equation.
  Total462 cards/714 assessments:296 MCQ,147 short,123 numeric,67 formula,
  81 equation. Nine integrated reviews do not inflate teaching-entry counts.
- Full Chemistry **363 passed,1 skipped,1 existing warning/365.38s**. Targeted
  **18 passed/35.53s**. Test-only module snapshot speeds pure positive grading
  examples,teardown fingerprint checks no mutation;negative/source/import/API
  cases remain fresh. Runtime validation/import semantics unchanged.
- Full Flutter **490 passed/85s**;no Dart/fixture change. Latest analysis65.2s
  and200% captures are batch13 evidence,not new visual/native certification.
  Initial execution was blocked by automatic-approval usage limit;after user
  continuation retry ran successfully. No security rejection bypassed.
- Real loopback HTTP preserved69 completions/1380XP,passed33 new questions,
  awarded100XP once,total74/1480XP. Completion replay identical;grading private.
  Synthetic900003 only;prior immutable snapshots and real user data untouched.
- All817 source pages decoded,five book SHA identities checked. One scientific
  blocker plus26 editorial issues remain. Lab15 Cu/H2SO4 scope machine guarded.
  No assumed pH7 endpoint,concentration,physical observation or crystal data.
- All grade7 coverage is local preview,not publication/teacher sign-off. No AI,
  production/main/other-subject/PDF/OCR/fulltext/token operation or fresh
  PG/full-backend/native/browser/IME/TalkBack certification. Ready flags false.


## Batch16 — 2026-10-24

- Grade8 §1–5:**79/268 implemented,189 remaining**;grade7:74/74,grade8:5/59.
  New44 cards/68 questions:22 MCQ,10 short,16 numeric,11 formula,9 equation.
  Total506 cards/782 assessments:318 MCQ,157 short,139 numeric,78 formula,
  90 equation. All nine grade7 reviews remain integrated,not extra entries.
- Full Chemistry **390 passed,1 skipped,1 existing warning/428.45s**. Final
  target **27 passed/16.84s**. Initial target26 passed/one test-only expected403
  vs409 mismatch for locked prerequisite,fixed to existing API403;runtime unchanged.
  Grade8 starts independently of grade7,ordered locks and once-only XP tested.
- Full Flutter **496 passed/114s**. Final analysis
  **no issues/38.3s**. Four grade8 real-widget cases/4s cover both themes,
  320×568/200% text,actual grade/source/full-page2019 identity,typed comma decimal,
  common feedback and draft restored after7↔8 switch. Actual final screenshots
  inspected;scrolling clips already-scrolled content intentionally,without overflow.
  Test MediaQuery now wraps navigator overlays;source modal itself is tested200%.
- Visual QA found missing Unicode subscript/arrow glyphs in Roboto test renders.
  Chemistry-only portable display spells H2SO4 and10^(-24),without changing any
  source/grading/input data. Optional source locatorSeparator keeps other-subject
  default intact. Unit test proves source data remains unchanged. No font download.
- Actual HTTP preserved74 completions/1480XP,passed68 new questions,awarded100XP
  once,total79/1580XP;grade7 catalog byte-equivalent,replay identical,grading private.
  Sanitized public grade8 fixtures have fake attempt ID/future expiry,no tokens
  or pre-answer keys. Real user data/older immutable manifests unchanged.
- All817 pages decoded,five SHA identities checked;one scientific blocker and31
  editorial reviews remain. Mol/rounding/phase/Na-oxygen/N-valence scopes held,
  not silently corrected. Historical/current source contexts explicitly distinct.
- No new learning/prediction/AI engine,production/main/other-subject/real-user/
  PDF/OCR/fulltext/token operation or fresh teacher/native/browser/IME/TalkBack/
  PG/full-backend certification. All whole-course-ready flags false.


## Batch17 — 2026-10-24

- Grade8 §6–10:**84/268 implemented,184 remaining**;grade7:74/74,grade8:10/59.
  New35 cards/52 questions:14 MCQ,11 short,27 numeric. Total541 cards/834
  assessments:332 MCQ,168 short,166 numeric,78 formula,90 equation.
- Full Chemistry **421 passed,1 skipped,1 existing warning/399.29s**. Target
  **31 passed/18.10s**. Source guard narrowing is deliberate:the helium8 hold
  applies to outer-electron premises,not the correct separate first-period H/He
  and second-period8 facts. All new held premises/removal bypasses tested.
  Critical Ruff/diff clean;prior79 manifest bytes unchanged.
- Full Flutter **496 passed/101s**. No Dart/fixture change in this batch. Latest
  analysis38.3s and200% source/grade/FRQ captures are batch16 evidence. Common
  feedback/result/draft/XP flow unchanged;no new grading or learning mechanism.
- Real HTTP preserved79 completions/1580XP,passed52 new questions,added100XP
  once,total84/1680XP. Grade7 catalog unchanged,completion replay identical,
  private grading hidden. Synthetic900003 only,real users/snapshots untouched.
- All817 pages decoded,five source SHA identities verified. One scientific
  blocker plus35 editorial reviews remain. Neutral atom,integer count versus
  average mass,conditional B model,maximum versus actual shell occupancy and
  short-table/source-era scopes explicit. No silent source repair or experiment.
- No AI,production/main/other-subject/PDF/OCR/fulltext/token/real-user operation
  or fresh teacher/native/browser/IME/TalkBack/PG/full-backend certification.
  Grade7 coverage and grade8 progress do not imply course-ready;all flags false.


## Batch18 — 2026-10-24

- Grade8 §11–15:**89/268 implemented,179 remaining**;grade7:74/74,grade8:15/59.
  New39 cards/61 questions:18 MCQ,13 short,26 numeric,4 formula. Total580 cards/
  895 assessments:350 MCQ,181 short,192 numeric,82 formula,90 equation.
- Full Chemistry **461 passed,1 skipped,1 existing warning/507.31s**. Target
  **40 passed/22.78s**. New prefix tests reject later pages,unscoped first-heading
  page,false paragraph,other chapter and chapter-as-review. Scoped original64
  pre-header fact reaches the public API with actual chapter identity. Critical
  Ruff/diff clean;prior84 manifest bytes unchanged.
- Full Flutter **498 passed/228s**;analysis **no issues/192.1s**. Two new real-
  widget tests/6s inspect actual63/64 chapter refs in both themes,320×568/200%
  text including navigator overlay. Localized pre-heading location is visible;
  original screenshots inspected,scrollable content/pinned actions intact.
  Flutter startup lock serialized analysis after test startup;both commands
  completed successfully. No native/browser/IME/TalkBack certification claimed.
- Actual HTTP preserved84 completions/1680XP,passed61 questions,added100XP once,
  total89/1780XP. Grade7 catalog unchanged,replay identical,grading private.
  Sanitized public fixtures have fake attempt ID/future expiry,no tokens/private
  pre-answer keys. No real account or prior immutable attempt/lesson change.
- All817 original pages decoded,five book SHA identities checked. One scientific
  blocker plus41 editorial reviews remain. La/Ce,valence/octet,average/fraction,
  scale and geometry scopes held;no external knowledge or silent correction.
- Common learning/input/XP/prerequisite/replay unchanged. New chapter prefix is
  evidence routing,not another course entry or new orbital/ionic/AI mechanism.
  No production/main/other-subject/PDF/OCR/fulltext/token/real-user operation or
  fresh teacher/PG/full-backend certification. All course-ready flags false.


## Batch19 — 2026-10-24

- Grade8 §16–20:**94/268 implemented,174 remaining**;grade7:74/74,grade8:20/59.
  New44 cards/66 questions:17 MCQ,9 short,23 numeric,4 formula,13 equation.
  Total624 cards/961 assessments:367 MCQ,190 short,215 numeric,86 formula,
  103 equation. Prior89 manifest bytes unchanged;critical Ruff/diff clean.
- Full Chemistry **505 passed,1 skipped,1 existing warning/846.50s**. Target
  **44 passed/33.67s**. Includes explicit exceptions,scope guards,every new key,
  source evidence,ordered attempts,prior progress and numeric-minus replay.
- Full Flutter **500 passed/214s**. Analysis: **No issues found! (ran in 225.7s)**.
  Two new actualHTTP widget tests **passed/9s**,320×568/200%,light oxidation and
  dark redox. Input and feedback captures inspected:long equation wraps within
  scrolling flow,source and pinned continue remain usable. No native/browser/
  keyboard/IME/TalkBack certification claimed.
- Actual HTTP preserved89 completions/1780XP,passed66 questions,added100XP once,
  total94/1880XP. U+2212 −2 and ASCII -2 replay responses identical. Grade7
  catalog unchanged,grading private. Sanitized public fixtures have fake IDs
  and future expiry;no private pre-answer rubrics or tokens.
- All817 original pages decoded,five SHA identities checked. One scientific
  blocker plus46 scoped editorial reviews remain. No external science,silent
  correction,physical experiment,production/main/other-subject/real-user change,
  raw PDF/OCR/fulltext upload or fresh teacher/PG/full-backend certification.


## Batch20 — 2026-10-24

- Grade8 §21–25:**99/268 implemented,169 remaining**;grade7:74/74,grade8:25/59.
  New54 cards/78 questions:19 MCQ,7 short,36 numeric,4 formula,12 equation.
  Total678 cards/1039 questions:386 MCQ,197 short,251 numeric,90 formula,
  115 equation. All94 earlier manifest hashes unchanged;Ruff/diff clean.
- Full Chemistry **544 passed,1 skipped,1 existing warning/901.86s**.
  Target **39 passed/25.51s**. Tests cover exact topic order,earlier context,
  visible source holds,hot/cold products,scientific Decimal notation,precision,
  units,private grading,94 old completions,once-onlyXP and unchanged Biology.
- Full Flutter **500 passed/157s**;fresh analysis **no issues/185.4s**.
  No new Flutter changes in this batch. Prior actualHTTP-widget small-screen
  oxidation/redox/source-sheet evidence remains;no fresh native/browser/IME/
  TalkBack or teacher certification claimed.
- Actual HTTP preserved94 completions/1880XP,passed78 answers,added100XP once,
  total99/1980XP. e/E numeric replay identical;grade7 catalog unchanged and
  private grading hidden. Synthetic900003 only,no real user modification.
- All817 PDF pages decoded,five source SHA identities checked. One scientific
  blocker plus51 scoped editorial issues remain;all ready flags false. Mixed
  gas-state/solubility/precision and unqualified generalizations held without
  external corrections. Original111–134 images additionally read for next batch.
- Shared theory/MCQ/FRQ/feedback/XP/progress/prerequisite/replay rules unchanged.
  No production/main/other-subject/AI/PDF/OCR/fulltext/token/real-user operation,
  physical experiment or fresh PG/whole-backend certification.
