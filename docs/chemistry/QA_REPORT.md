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


## Batch21 — 2026-10-25

- **104/268 implemented,164 remaining**;grade7:74/74,grade8:30/59.
  New§26/27/28/practical1/§29:59 cards/72 questions (18 MCQ,8 short,26 numeric,
  4 formula,16 equation). Total737 cards/1111 questions:404/205/277/94/131.
  All99 earlier manifest hashes unchanged;original§1 unchanged;Ruff/diff clean.
- Full Chemistry **589 passed,1 skipped,1 existing warning/742.26s**.
  Final target **45 passed/24.80s**. Initial target40pass/5fail exposed misplaced
  new guards;fixed per-fact scope,not answer expectations. Tests cover all new
  source issues,composite evidence,fourth originalZn balance,practical ordering,
  every key,99 old completions/XP,replay and preserved Biology test account.
- Full Flutter **502 passed/184s**;analysis **no issues/104.2s**.
  Two actualHTTP practical widget cases **passed/9s**,320×568/200%,both themes.
  Six input/feedback/source captures inspected:fields,scrolling feedback/source
  sheet and pinned actions usable. Initial harness0pass/2fail then1pass/1fail
  were background JSON decoding races;bounded real-async drain fixes harness.
  Production UI/grading unchanged. No native/browser/IME/TalkBack certification.
- Actual HTTP preserved99 completions/1980XP,passed72 answers,added100XP once,
  total104/2080XP;scientific e/E replay identical. Grade7 catalog unchanged,
  grading private,synthetic900003 only. New public fixtures contain fake attempt
  IDs/future expiry,no tokens/private pre-answer keys.
- Five source SHA identities/all817 pages audited. One scientific blocker plus
 56 editorial issues remain;no silently repaired conflicts/external science or
  claimed teacher sign-off. Original135–147 read for continuation,not counted as
  new authored material. Catalog327/268 unchanged;all ready flags false.
- No production/main/other-subject/AI/PDF/OCR/fulltext/token/real-user operation,
  physical experiment,new chemistry engine or fresh PG/whole-backend certificate.


## Batch22 — 2026-10-25

- **109/268 implemented,159 remaining**;grade7:74/74,grade8:35/59.
  New§30–34:56 cards/74 questions (20 MCQ,12 short,22 numeric,3 formula,
  17 equation). Total793 cards/1185 questions:424/217/299/97/148 respectively.
  All104 prior hashes/original§1 unchanged;Ruff/diff clean.
- Full Chemistry **633 passed,1 skipped,1 existing warning/722.46s**.
  Target **44 passed/27.64s**. Initial43pass/1fail was expected-error regex
  mismatch (validator correctly rejected future context);test now asserts the
  actualsource_context_must_precede_lesson code. No runtime weakening.
- Full Flutter **504 passed/153s**;analysis **no issues/91.8s**.
  Two new actualHTTP theory/source widgets **passed/7s**,320×568/200%,both
  themes. Initial visual capture found missing⇌ glyph;display-only <=> repair
  visually rechecked. Four final captures inspected;source pages143/145 visible,
  scroll and pinned actions preserved. Source JSON mutation assertion passes.
  No native/browser/IME/TalkBack certification.
- ActualHTTP preserved104 completions/2080XP,passed74 answers,added100XP once,
  total109/2180XP. Comma/dot0.06 replay identical,grade7 catalog unchanged,
  grading private,synthetic900003 only. Six new public fixtures sanitized.
- Five source SHA identities/all817 pages audited. One scientific blocker and
 61 editorial scopes remain;no silent correction or teacher certification.
  Original148–165 additionally read for continuation,not counted as authored.
  Catalog327/268 unchanged;all ready flags false.
- No production/main/other-subject/AI/PDF/OCR/fulltext/token/real-user operation,
  physical experiment,new chemical solver or fresh PG/whole-backend certificate.


## Batch23 — 2026-10-25

- **114/268 implemented,154 remaining**;grade7:74/74,grade8:40/59.
  §35/practical2/§36–38 add60 cards/86 questions (21 MCQ,6 short,31 numeric,
  8 formula,20 equation). Total853 cards/1271 questions:445/223/330/105/168.
  All109 prior hashes/original§1 unchanged;critical Ruff/diff checks pass.
- Full Chemistry **686 passed,1 skipped,1 existing warning/764.37s**.
  Target **53 passed/32.11s**. Source mutation tests retain all six reviews and
  reject erroneousBi configuration,ozone heat,solution fraction,yield/rate and
  valence premises. Prefix157 evidence scope must match. Initial manifest
  rejected three missing exact Uzbek answer labels;source-backed labels were
  completed before first import,without changing the validator contract.
- Full Flutter **508 passed/117s**;analysis **no issues/181.2s**.
  Four new actualHTTP-fixture widgets **passed/11s**,320×568/200%,both themes.
  Table/source prefix157 and signed numeric feedback/source161 inspected;
  eight captures generated,four representative captures visually reviewed.
  Scrollable source sheets and pinned continuation remain usable. No native,
  browser,IME or TalkBack certificate;no new runtime parser/display change.
- ActualHTTP preserved109 completions/2180XP,passed86 answers,added100XP once,
  total114/2280XP. Unicode/ASCII−3 replay identical;grade7 catalog unchanged;
  rubrics private. Synthetic900003 only. Six new public fixtures sanitized.
- Five textbook SHA identities/all817 pages re-audited. Catalog327/268 unchanged;
  one scientific blocker and67 editorial scopes remain. Ready flags false.
  Original166–185 additionally read for continuation,not yet authored lessons.
- No production/main/other-subject/AI/PDF/OCR/fulltext/token/real-user operation,
  physical experiment,new scientific solver or fresh PG/whole-backend claim.


## Batch24 — 2026-10-25

- **119/268 implemented,149 remaining**;grade7:74/74,grade8:45/59.
  §39/practical3/§40/41/practical4 add68 cards/86 questions (19 MCQ,4 short,
  26 numeric,12 formula,25 equation). Total921 cards/1357 questions:
  464/227/356/117/193. All114 prior hashes/original§1 unchanged;critical Ruff
  anddiff checks pass. Catalog327/268 unchanged;all ready flags false.
- Final full Chemistry **739 passed,1 skipped,1 existing warning/795.29s**.
  Final target **53 passed/19.23s**. Earlier target53/21.23s preceded one card
  wording clarification. Fullv1 was explicitly stopped before editing,not
  counted as a pass. Finalv2 is the clarified immutable snapshot.
- Full Flutter **510 passed/140s**;analysis **no issues/72.8s**.
  Two new actualHTTP-fixture widgets **passed/13s**,320×568/200%,light/dark.
  Five captures inspected:practical feedback top/source172173 and clarified
  phosphate dissociation/source178. Scroll and pinned continuation preserved.
  No runtime parser change,native/browser/IME/TalkBack certificate.
- Initial misplacedHCl24/98 citation was rejected;actual27/116 image confirmed
  and all refs/evidence relinked before final import. Dissociation body clarified
  residual acidH count. Older draft sandbox left immutable;fresh local sandbox
  seeded114 exact baseline synthetic progress rows and2280XP read-only after
  SHA checks,then passed86 actualHTTP answers/once-only100XP→119/2380XP.
  Comma/dot replay identical,grade7 unchanged,rubrics private,six fixtures sanitized.
- Five textbook SHA identities/all817 pages audited. One scientific blocker and
  72 editorial scopes remain. Remaining185–208 material and upright table199
  read for continuation,not counted as authored/teacher-approved knowledge.
- No production/main/other-subject/AI/PDF/OCR/fulltext/token/real-user operation,
  physical experiment,new scientific solver or fresh PG/whole-backend claim.


## Batch25 — 2026-10-25: grade8 sequence46–50

124/268 implemented;144 remain. Grade7 all74;grade8 all44 paragraphs,all5
practicals and lab1 (50/59). Next nine labs2–10,sequence51–59,original200–204.
New5 lessons add59 cards/68 questions (19 MCQ,8 short,18 numeric,11 formula,
12 equation). Total980 cards/1425 questions:483/235/374/128/205 respectively.

§42 distinguishes primaryNPK from total element counts;commercial percentages,
hydrates and mixtures are not pure compound identities. §43 teaches P2O5/K2O
reporting equivalents and exact given arithmetic:16.47%,4.120t,473.2kg,with
printed16.4/4.117/473.3 separately flagged. §44 retains neutral source
classification/relative amounts/symbols/environment;clinical,treatment,
universal essentiality,current statistics and waste application claims held.
Practical5 covers digital known models and original exact calculations;upright
table199 contradictory nitrate rows held. No unknown sample IDs or actual
observations invented. Lab1 retains exact school zincate model and limited Cu
comparison. Exact prior Na/water4/21,AlCl3 20/83 and KHSO4 2/15 checked.

77 editorial scopes plus one scientific blocker remain;all ready flags false.
No source gap filled by memory,AI feature,new solver,physical experiment or
teacher certificate. Five PDF identities/all817 decoded pages audited.

Target50 passed/20.53s;full Chemistry789 passed,1 opt-in PG skip,1 existing
Starlette warning/906.77s. Full Flutter512 passed/137s. Analyzer initially
reported missing braces in one new test;fixed,final no issues/35.0s. Two new
320×568/200% light/dark widgets passed/15s;four captures visually inspected
for fertilizer decimal feedback/source191 and zincate feedback/source200.
Scroll/pinned continuation preserved. No runtime UI/parser change this batch.

Actual loopbackHTTP68 answers preserved119 completions/2380XP,added100XP
once,now124 completions/2480XP. Comma/dot4,120/4.120 replay identical,grade7
unchanged,private rubrics hidden,six public fixtures sanitized. Current sandbox
ilm-ai-chemistry-batch24-final-qa,port8901,ownPID24132 (verify command before
stopping);private defines remain there. Imported r1 lessons are immutable.
All prior119 hashes and original§1 unchanged;critical Ruff/diff checks passed.
Biology/Physics branches and real user data preserved. No production/main,
PDF/OCR/fulltext/token push or native/IME/TalkBack/whole-backend certificate.


## Batch26 — 2026-10-25: final grade8 laboratories2–10

**133/268 implemented,135 remain. Grade7 all74;grade8 all59 mapped entries.**
Nine final labs add55 cards/93 questions:27 MCQ,9 short,20 numeric,23 formula,
14 equation. Total1035 cards/1518 questions:510/244/394/151/219 respectively.
Mapped coverage is not independent scientific approval;all ready flags false.

Original200–204 reviewed with exact prior source pages. KClcoord6 separated
from1:1formula;S8model versus other sulfur phases;iodine limitedtwoatom/solid
facts. AgClwhite/AgBrsarg‘ish/AgIyellow exact122;lab3 starch/food colors absent
and held. Soil task does not supply actual chloride result. Halogen3x3 table
uses exact earlierKmodels/rank for originalNa givenproductbalances. Iodine
water/organic qualitative comparison;layercolor/position/measurement held.
MineralsFeS2/ZnS/CaSO4·2H2O andS8 masses use exact priorconstants;formula
unit versus atom/molecule distinguished. Known four sulfate solution models
retainBaSO4white evidence;no universalwhitesolid identification. NH3 equation,
aqueousschoolmodel andindicator context retained;recipe1.5:1 is not exact
stoichiometricmass key. Fiveexplicit fertilizer examples,not invented samples.
NH3/HCl exact page161 checked instead of initial162 reference. Br2 FRQ uses
existing chemical_formula contract rather than prose;no new scientific parser.
86 editorial scopes plus one grade9 scientific blocker remain. No source gap
filled from memory,physical experiment,AI feature or teacher certificate.

Target final62 passed/6.88s;initial61pass/1fail was wrong test expectation
incorrect_species for formula mismatch (actual documentedcode incorrect),
fixed assertion only. FullChemistry851 passed,1 opt-in PG skip,1 existing
Starlette warning/389.15s. Critical Ruff anddiff checks passed;all prior124
hashes and original§1 unchanged. FivePDF identities/all817 pages audited.
FullFlutter514 passed/79s;analysis no issues/87.0s. Two new320×568/200%
light/dark laboratory widgets passed/6s;capture rerun2passed/7s. Four source/
feedback captures visually inspected203/204:scroll/pinnedcontinuation works.
No runtimeUI/parser change or native/IME/TalkBack/whole-backend certificate.

ActualHTTP93 answers preserve124 baseline completions/2480XP,award180XP
once→133completions/2660XP. Comma/dot74,5/74.5 replay identical;grade7
catalog unchanged,private rubrics hidden,six sanitized public fixtures.
Current sandboxilm-ai-chemistry-batch24-final-qa,port8901,ownPID9864,
verify full command before stopping;private defines stay there. All133 r1
imported revisions immutable. Real users,Biology andPhysics untouched.
No production/main/PDF/OCR/fulltext/token push or new externalknowledge.

Nextbatch27:grade9 §1–5,sequence1–5,original5–28. Original4–29 already
visually read;private notes .local/grade9_start_source_notes.md andrenders4–42.
Review before authoring:Ar/nucleoncount,legacygroup/period universal claims,
Mg radius .269 andstrictmonotonictrends,Cs strongestabsolute,orbitalpaths;
bond/valence/oxidation universals;water/CO2 conductivity,H3PO3 acidH task,
universal chloride safety;NH4OH schoolmodel/acidstages;58%H2SO4 ambiguous
basis,allorganicweak/allconcentrationstrong andunlimitedKconcentrationlaw.
Keep exact clear models,hold errors visibly,no silent memory repair.


## Batch27 — 2026-10-25: grade9 paragraphs1–5

**138/268 implemented,130 remain. Grade9 5/61;7/8 all74/59 mapped entries.**
New5 add64 cards/97 questions:28 MCQ,14 short,36 numeric,19 formula.
Total1099 cards/1615 questions:538/258/430/170/219 respectively.

Original5–28 fully reviewed:periodiclaw/history/nuclearcharge/atomcounts,
scopedlegacygroups/trends,capacities/configurations,bondtypes/energy/redox/
formaloxidation,electrolyte/ionmobility/hydration/H3O+,acid/base/saltstages,
degree/percent/weak equilibrium andconditionalK arithmetic. No new parser:
charged equations shown/selected inMCQ;FRQ existingneutralformula/name/
numericcounts. H3PO4 stages introduced only in§5 with actual27P(OH)3,
earlier§4task linked. Exactreferences9/11,23/24/25 and27/28 tightened.

91 editorial scopes plus one scientific blocker. Held source issues include
Ar/nucleoncount,Mg.269/strictIEtrend/Csabsolute,allperiodalkali/outer8 and
literalorbitalpath universals,bond/valence/oxidation universals,water/CO2
conductivity,H3PO3threeacidH/chlorideuniversalsafety,NH4OHschoolnotation,
58%H2SO4 ambiguousstage,allorganicweak/allconcentrationstrong andunlimited
Klaw. No silentmemoryrepair;all ready flags false. Originalgivenmodels and
arithmetic are labeled,not fabricated experiments or clinical guidance.

FinalfullChemistry916 passed,1 opt-in PG skip,1existingwarning/378.31s.
Targetfinal154/23.19s coversbatch16/26/27. Initialnew65/7.18s and127/13.99s
were before finalcopy. Fullv1/v2 stopped,not counted aspass:historicalbatch26
exacttotal133 andbatch16exactavailable[7,8] wronglyforbade newgrade9.
Assertions now preservebaseline andrequiredgrades while allowing continuation;
runtime/learningrules unchanged. All133 prior hashes/original§1 same;Ruff/diffpass.

FinalfullFlutter516 passed/79s;analysis noissues/5.7s. Two320×568/200%
light/dark grade9 widgets passed/3s;four finalfeedback/source11/28 captures
seen. Initialdraftwidgets2/2s,full516/80s,analysis26.2s precededcopyspacing.
Visualreviewcaught number/formula wordsjoined;onlynew5 learnercopy spaced.
Old138draft sandbox preserved. Fresh batch27final sandbox compared133content
SHAs andcopied only exactsyntheticbaseline progress/2660XP read-only,then
passed97actualHTTP answers and once-only100XP→138/2760XP. Comma/dot1,66/
1.66 andscientific1e-5/0.00001 replay identical;grade7/8catalogs unchanged,
private rubrics hidden,six sanitized fixtures. Grade9 selection uses existingUI.

Current sandboxilm-ai-chemistry-batch27-final-qa,loopback8902,ownPID24044.
Verifycommand before stopping;private defines staythere. Current138r1 immutable.
Older8901draft stopped(20776),preservedhistorical. No real-user/prod/main,
other-subject/PDF/OCR/fulltext/tokenpush,AI,newsolver orphysicalexperiment.
No independentteacher/native/IME/TalkBack/whole-backend certificate.

Next5:grade9 §6–10,original29–top53. All29–53 read;43–61rendered privately.
Notes .local/grade9_next_source_notes.md: H2Sinsolubleclaim,wateralpha,
weak/weakallfullyhydrolyze,FeIIIcarbonateunbalanced38,CO2conductancezero,
carbon2p6legend/fullerenecount/classicalphase constants,coalcurrentstatistics/
medicaladsorption andunlimitedheat/combustion claims need visible review.
Exactprovided textbookconstants fromearliergrade mayneed narrowly validated
explicitcrossgrade sourcecontexts;currentlyownbookonly. Do not fill bymemory.


## Batch28 — 2026-10-25: grade9 paragraphs6–10

**143/268 implemented,125 remain. Grade9 10/61;7/8 all74/59 mapped entries.**
New5 add72 cards/124 questions:23 MCQ,10 short,26 numeric,21 formula,44
equation. Total1171 cards/1739 questions:561/268/456/191/263 respectively.

Original29–top53 fullyreviewed:ion exchange/full/net models/qualitativetable,
hydrolysis/conditionalstages/limitingreactants,carbonfamily/allotropes/cycle,
adsorption/givenproductreactionfamilies,CO/CO2/salt-ratio/heat/density models.
Printed38water/FeOH2 errors held;originalgivenFeOH3/CO2 balance has3water.
ClearBaSO4 example5.825g andcarbonate1.12Ln.sh retained. SiH4 exercise uses
actual earlier8/25/110He4,8/5/27Si28/SiH4,8/1/7H1;CuO20g model uses
actualCu64 from8/practical1/127,O16 from8/1/7,C12 from8/5/29→3gC/16gCu.
Bookheat412/572 used onlyasexplicitgivenmathmodels,notexperimentalenthalpy.
No COCl2productionconditions,physicalgas/CS2/cyanogen/fluorination/acid/heat/
electricityprotocol or clinical/field/fire certificate. Neutralformula/equation,
numeric andMCQ/short commonassessment contract unchanged;no newsolver/AI.

Strict earlier-grade citation support added to Chemistry validator. Context must
be teaching record in earliergrade andalreadyvalidated importer manifestprefix.
Standalonevalidation checks referencedindexedlesson digest/review andvalidates
it. Eachref retains citedbookSHA/file/title/authors/year/topic/page/region;
grade7left/right mappings preserved. Futuregrade/unreviewed/blocked/container
contexts rejected. Samebookordering/chapterprefix/review/heldfact guards intact.
22 new structural/forgery/spread/index tests pass. REQUIREMENTS andASSESSMENT
contract updated. Existing138 lesson bytes/learning/XP/progress untouched.

96 editorial scopes plus one scientific blocker remain;allreadyfalse. Newholds:
H2Sinsolubility/universalselectivity,wateralpha/allweak-weakfullyhydrolyze,
FeIIIcarbonatebalance/Sbproductidentity/conductancezero,C2p6diagram/fullerenecount,
charcoalpurity/allphase/currentcoal/medicaladsorption/unlimitedheat/fireclaims.
No silentmemoryrepair;five textbook identities/all817 pages audited.

FinalfullChemistry991 passed,1 opt-in PG skip,1existingwarning/436.59s.
Finaltarget75/10.61s includes22 earlier-source plus53batchtests. Initialtarget
74pass/1fail was wrong testexpectation invalid_answer forSIH4 (a validS/I/H
formula withwrong composition);assertioncorrected toincorrect,graderunchanged.
First correctedtarget75/9.71s,initialfull991/521.05s precededfinalcopyspacing.
CriticalRuff/diffpass;all138 baseline hashes/original§1 unchanged.

FinalFlutter518/87s,analysisnoissues/6.2s;two320×568/200%widgets4s.
Sixfinalcaptures inspected:darkSiH4/light71,5feedback,currentgrade9source47/
51,53 andearliergrade8source110/105. Actualgrade8filename/bibliography and
locators shown separately;scroll/pinnedcontinuation preserved. Initialwidgets
2/5s,full518/86s,analysis64s precededfinalremainingword/unitspacing polish.
No runtimeUIchange/native/IME/TalkBack/whole-backend certificate.

Historical143draftQA preserved. Freshbatch28final sandbox compared138content
SHAs,copied only138exactbaseline syntheticprogressrows/2760XP read-only,
then124actualHTTP answers/once-only100XP→143completions/2860XP. Comma/dot
71,5/71.5 andscientific1.71666667e5/171666.667 replayidentical;grade7/8
catalogs unchanged,rubricsprivate,six fixtures sanitized. Current143r1 immutable.
Current sandboxilm-ai-chemistry-batch28-final-qa,loopback8903,ownPID27960;
verifyfullcommand beforestop,private definesstaythere. Older8902draft stopped
ownPID24440 andpreservedhistorical. No actualusers/production/main/otherbranch,
PDF/OCR/fulltext/tokenpush or independentteacher signoff.

Next5:grade9 §11–15,original53–top74. All53–74 read;62–77 renderedprivately.
Notes .local/grade9_batch29_source_notes.md. Reviewbeforeauthoring:HCO3wrong
charge54,hydrate11.44/4.28ambiguous56,2.74versus2.47and20.4Vmtypos59/60,
cave/clinicalsafety,Si phase/density/acid-subject/polysilaneuniversals,cement
450C,crystalsodaearlyround146/limestone.953,densitythreshold500/metalloid/
currentresourcerank universals. Exactclearbookmodels only,no externalrepair.


## Batch29 — 2026-10-25: grade9 paragraphs11–15

**148/268 implemented;120 remain. Grade9 15/61, with all74 grade7 and59 grade8 entries.**
Five new lessons add80 cards and125 questions:23 MCQ,9 short,35 numeric,
18 formula and40 equation. Total1251 cards/1864 questions:584/277/491/209/303.

Original53–top74 was visually reviewed. Coverage includes carbonate equilibria,
salts and worked mass balances; silicon structure, minerals and given reduction
models; silica/metasilicate transformations; glass/cement/ceramic categories;
and metal occurrence, extraction families and electron counts. Worked arithmetic
uses exact declared textbook models and final rounding. Earlier-grade constants
retain their own book identity, including8/practical1/125–126 mass316 for
2KMnO4 and8/20/84–85 decomposition. No remembered Mn atomic mass was added.

New source review scopes remain visible: bicarbonate charge54, ambiguous hydrate
sample56,2.74 versus2.47 and20.4 versus22.4 copies59/60; silicon phase density;
unqualified silane/acid/species claims; cement450C; early-rounding water146g and
limestone.953; metal density500kg/m3 and current resource statistics. Clear
given models yield2.467%,146.140g and.952 at declared precision. These original
calculations are identified as such. No silent external450→1450 or500→5000
correction. All five ready flags remain false:101 editorial scopes and one
scientific blocker, with no independent teacher approval claimed.

The validator now rejects both superscript minus forms of the wrong HCO3 charge
and both disputed silicon phase density values. New tests cover these holds,
source order,125 grading answers and once-only XP. Equation prompts present
unbalanced supplied species; private expected ratios remain source checked.
The shared MCQ/FRQ, immutable attempt, expiry, replay and20XP rules are unchanged.
Learner copy and unit spacing were proofread before the first immutable import;
carbonate hydrate content uses “suvsiz tuz”, not “anhidrid”.

Full Chemistry:1058 passed,1 opt-in PostgreSQL skip,1 existing Starlette warning,
523.49s. Target89 passed/11.23s includes22 earlier-source tests. Initial target
had88 pass/1 fail because AU was incorrectly expected to return invalid_answer;
existing grammar returns incorrect for a wrong formula. Only that test assertion
changed. Critical Ruff/diff checks passed. All143 predecessor lesson hashes and
manifest pins, plus original grade7§1, are unchanged.

Flutter520 tests passed/111s; analysis0 issues/153.1s. Four200% source widgets
passed/6s, including two new320×568 dark/light scenarios. Six new captures were
visually inspected: silicon mass feedback/current9/62/earlier8/27, and silicate
industry feedback/current9/70/earlier8/84–85. Source dialogs scroll separately,
and feedback keeps its continuation button reachable. No runtime UI change or
native Android/IME/TalkBack certification is claimed.

Actual loopback HTTP answered125 questions and preserved143 synthetic progress
rows/2860XP. It added100XP once, reaching148 completions/2960XP. Complete replay
is identical;146,140/146.140 and3.568e2/356.8 replays agree. Grade7/8 catalogs
remain unchanged and private rubrics are hidden. Six sanitized public fixtures
were exported. Current sandbox remainsilm-ai-chemistry-batch28-final-qa on8903,
now ownPID22976; verify its full command before stopping. Private defines stay
outside Git. All148 imported r1 revisions are immutable.

Five PDF hashes/all817 pages audited; source map remains327 anchors/268 entries.
No raw PDF/OCR/full text/render/token push, main merge, production DB operation,
AI feature or other-subject branch mutation. Digital models do not provide
physical lead/silane/HF/thermite/refining/electrolysis/clinical instructions.

Next five: grade9§16–20, original74–top100. All74–100 visually read; detailed
notes are private at.local/grade9_batch30_source_notes.md. Review alloy universal
properties/incomplete compositions; metal displacement conditions; corrosion
charge/Fe(OH)3/inhibitor exponents; electrolysis wrong electrode labels, charged
products and tableH2S; and alkali Fr/medical/biological universals. The clear
source examples remain usable under their declared conditions.


## Batch30 — 2026-10-25: grade9 paragraphs16–20

**153/268 implemented;115 remain. Grade9 20/61;grade7 all74 andgrade8 all59.**
Five new lessons add75 cards/111 questions:22 MCQ,11 short,46 numeric,
17 formula and15 equation. Total1326 cards/1975 questions:606/288/537/226/318.

Original74–top100 visually reviewed. Coverage includes alloy composition and
structure, metallic bonding and scoped displacement, corrosion/protection roles,
electrolysis of specified melts/solutions, Faraday unit pairing and all seven
worked examples, and alkali configurations/compound categories. Current and
earlier source pages remain explicit. Ag107.9 from8/13/59 is openly rounded108
for the school mass model. CuO is a declaredCu(II) product with prior7/9/31
(PDF16:right) and8/2/10 evidence, not an unbounded reaction prediction.

New source scopes remain visible: alloy universal properties/incomplete recipes,
undefined gold assay and acid products; unqualified metal displacement; corrosion
charge/pure rust/inhibitor exponent; electrolysis wrong electrode labels, charged
hydrogen/oxygen copies and tableH2S; and Fr/medical/biological alkali claims.
106 editorial issues plus one scientific blocker remain. Course-ready flags are
false. Conditional original balances and exact arithmetic are taught without
silently copying disputed assertions or repairing them from external knowledge.
No new ionic/equilibrium solver, pedagogy, AI or physical experiment was added.

Full Chemistry1118 passed,1 opt-in PostgreSQL skip,1 existing Starlette warning,
507.17s. Target82 passed/11.10s includes22 earlier-source tests. All111 new
answers also passed actual HTTP. An initial standalone validation caught a
missing Natriy entry in the already taught names fact; the evidence list was
completed before tests/import. Critical Ruff/diff checks passed. All148 prior
lesson bytes/manifest pins and original grade7§1 remain unchanged.

Flutter522 tests passed/93s; analysis0 issues/26.3s. Six200% source widgets
passed/7s, including two new320×568 dark/light scenarios. Six new captures were
inspected: corrosion feedback/source9/85/source7/31→PDF16:right, and electrolysis
feedback/source9/90,93,94,96/source8/59. Source ownership, spread locators,
scrolling and pinned continuation remain usable. No runtime UI change or native
Android/IME/TalkBack certificate is claimed.

Actual HTTP preserved148 synthetic completions/2960XP and added100XP once,
reaching153 completions/3060XP. Complete replay is identical;2,24/2.24 and
3.01e23/301000000000000000000000 replays agree. Grade7/8 catalogs are unchanged;
private rubrics remain hidden. Six sanitized public fixtures were exported.
Current sandboxilm-ai-chemistry-batch28-final-qa on8903 now runs ownPID26704;
verify full command before stopping. All153 imported r1 revisions are immutable;
private defines remain outside Git.

Five PDF hashes/all817 pages audited; catalogue327 anchors/268 teaching entries
unchanged. No PDF/OCR/full text/render/token push, production operation, main merge
or other-subject branch mutation. Source teacher review remains outstanding.

Next five:grade9§21–25,original100–top124,all visually read. Private detailed
notes:.local/grade9_batch31_source_notes.md. Review K potential/KO2 category/NaON,
conditional hydride identification, mineral formula conflicts, clinical claims,
lime-name ambiguity, hardness/biological arithmetic copies, and Al electrode
signs/carbon balance/nepheline ratios. Do not fill missing keys from memory.


## Batch31 — 2026-10-25: grade9 paragraphs21–25

**158/268 implemented;110 remain. Grade9 25/61;grade7 all74 andgrade8 all59.**
Five new lessons add80 cards/133 questions:20 MCQ,10 short,34 numeric,
20 formula and49 equation. Total1406 cards/2108 questions:626/298/571/246/367.

Original100–top124 visually reviewed. Coverage includes Na/K source models,
historical soda cycles and gross versus recycled inputs, Mg/Ca/lime/gypsum
categories, water hardness and ion exchange, and aluminium structure/electrolysis.
Every key uses the shared bounded response types and exact supplied page evidence.
The unspecified lime question is adapted to an openly defined90%CaO input/
20%Ca(OH)2 output model, not silently repaired. The milk/bone contexts are
abstract declared arithmetic, with clinical and actual body-composition claims
held. Crystal-soda acid example uses full intermediate5139.860139g pure acid,
5354.020979g96%solution and2909.794010mL→2.910L under declared assumptions.

New source scopes remain visible: K potential/KO2 category/NaON label; hydride
identity and cycle boundaries; mineral/medical/lime-name ambiguities; hardness
phase simplifications/milk165/bone denominator; Al electrode signs/carbon
balance/nepheline ratios/required intake.111 editorial issues and one scientific
blocker keep all readiness flags false. No external memory repair, physical
experiment, clinical recommendation, new complex/ionic solver or AI feature.

Final full Chemistry1178 passed,1 opt-in PostgreSQL skip,1 existing Starlette
warning/1370.84s. Final target82 passed/43.75s includes22 earlier-source
tests. Earlier target81 pass/1 fail was a test pointing Mg/CO2 answer at q17
instead of q16; only its index changed, grader unchanged. Corrected pre-final
target82/38.40s also passed. Pre-import copy validation caught a formatter
splitting4Li into4 L i; exact lithium formulas were restored, then a regression
assertion added. Final prose polish excludes expected/verified formula keys
and source metadata. Critical Ruff/diff checks passed. All153 prior lesson
hashes/manifest pins and original grade7§1 remain unchanged.

Flutter524 tests passed/151s. Analysis0 code issues/135.0s; the command first
waited for Flutter's startup lock, then exited0. Eight200% source widgets
passed/28s, including two new320×568 dark/light scenarios. Six new captures
were inspected: Na/K mass feedback/source9/105/earlier8/29–30, and Al cathode
feedback/source9/123/prior9/85,91. Source ownership, page locators, scrolling
and pinned continuation are preserved. No runtime UI or native/IME/TalkBack
certificate is claimed.

Actual HTTP133 answers preserved153 synthetic completions/3060XP, then added
100XP once→158completions/3160XP. Complete replay is identical;22,4/22.4 and
6.15385e2/615.385 replays agree. Grade7/8 catalogs are unchanged; private
rubrics hidden; six sanitized public fixtures exported. Current sandbox remains
ilm-ai-chemistry-batch28-final-qa on8903,now ownPID7544. Verify full command
before stopping; private defines remain outside Git. All158 imported r1 immutable.

Five PDF hashes/all817 pages audited;327 anchors/268 teaching entries unchanged.
No PDF/OCR/full text/render/token push, main merge, production operation or
other-subject branch mutation. Independent teacher review remains outstanding.

Next five:grade9§26–30,original124–top145,all visually read. Private detailed
notes:.local/grade9_batch32_source_notes.md. Private author_batch32a.py,
author_batch32b.py and author_batch32c.py are prepared but unexecuted;
no batch32 catalogue scope run.
Review Al nitrate/water/H2 copies, missing legitimate priorCr mass constant,
KOH coefficient/amethyst identity, Cu conditional chemistry, Ag medical/Au
leaf-thickness/cyanide-complex scope, and Zn/Hg acid/product/balance copies.
Never invent missing constants or enable unsupported complex notation grading.


## Batch32 — 2026-10-25: grade9 paragraphs26–30

**163/268 implemented;105 remain. Grade9 30/61;grade7 all74 andgrade8 all59.**
Five lessons add78 cards/151 questions:20 MCQ,10 short,40 numeric,19 formula,
62 equation. Total1484 cards/2259 questions:646/308/611/265/429.
Original124–top145 visually reviewed. Al properties and amphoteric compounds,
Cu,Ag/Au,Zn/Cd/Hg use the existing common learning/input/grading contracts.

Source holds remain explicit: Al nitrate/water/H2 copies, missing legitimate
earlier Cr mass constant for paragraph26, hydrate rounding; legacy paragraph27
gem-host contradiction with grade7/108 and KOH coefficient; Cu conditional
phases/products; Ag clinical assertions/Au leaf-thickness unit/exclusive acid
claim; Zn/Hg concentration labels and water coefficient. Existing paragraph27
issue ID and cross-book evidence retained; disputed gemstone and KOH equation
keys are excluded, including a mathematically repaired KOH key. Complex species
remain display/MCQ/count only. No physical hazardous procedure or clinical advice.
115 editorial issues and one scientific blocker keep every ready flag false.

Full Chemistry1244 passed,1 opt-in PG skip,1 existing Starlette warning/
1964.72s. Target88/46.05s includes22 earlier-grade source tests. Critical
Ruff/diff checks passed. All158 predecessor hashes/manifest pins and original§1
remain unchanged. Five PDF hashes/all817 pages audited;327anchors/268entries.

Flutter527 tests/254s; analysis0 issues/117.5s. Three new320×568/200% dark/light
widgets passed/31s. Eight captures visually inspected: Al kaolin20,930 feedback,
source9/129 and prior8/27; Zn3,270 feedback,source9/144 and prior9/57; existing
bounded complex MCQ feedback and source9/129–130. Dialog source ownership,
locators, scrolling and pinned continuation remain intact. No runtime UI change
or native Android/IME/TalkBack certificate is claimed.

Actual HTTP151 answers preserve158 synthetic completions/3160XP and add100XP
once→163completions/3260XP. Complete replay identical;3,270/3.270 and
2.093e1/20.930 replays equivalent. Grade7/8 catalogs unchanged; rubrics private;
nine sanitized public fixtures. All163r1 imported snapshots immutable.
Current sandboxilm-ai-chemistry-batch28-final-qa,loopback8903,ownPID19764.
Verify full command before stopping; private tokens/defines remain outside Git.

No PDF/OCR/full text/render/token push, main merge, production DB/deploy,
other-subject branch mutation or AI feature. Teacher review remains outstanding.

Next5:grade9§31–35,original145–top165,all visually read. Detailed private notes
.local/grade9_batch33_source_notes.md. Five author_batch33a–e scripts prepared
but unsaved/unindexed. In-memory dry run:89cards/189questions; all expected
answers accepted by existing grader. Do not call that a finished course batch.
Review Cr acid/product conditions/CrO3 coefficient, Mn nonoxidation and +7/+6
copies, Fe diagram/potential/limonite/rust, complex phase and clinical claims.
No catalogue scope run yet. Freeze source data during full snapshot tests.
