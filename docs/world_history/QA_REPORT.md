# Jahon tarixi QA — initial source foundation

2026-10-26. These are initial inventory/algorithm tests, not final course QA.

- Six supplied books: SHA-256 verified, 961 pages actually decoded and privately
  rendered. Grade9's 160 pages have OCR locator files; no useful text layer.
- Bibliography and contents verified from original page images for all six.
  All numbered body headings cross-checked; factual body review remains pending.
- First test run: **26 passed in 1.04 s** for source identity/order/combined units,
  prerequisite protection, unreviewed catalogue gating, BCE/CE/century arithmetic.
- Critical Ruff (`F821,F822,E9`) passed for new source/chronology modules/scripts.
- Final initial-stage run: **30 passed in 4.56 s**, including all 961 render
  inventory entries, all 687 protected lesson/runtime hashes, rejected forged
  readiness flags and malformed-era input. No history content was imported.
- No history runtime/API/PostgreSQL/native Android tests yet: those components
  do not exist. No production DB or real user data accessed.
- Flutter dependencies resolved from the existing offline cache; no dependency
  upgrade was requested. Analysis in the new worktree: **0 issues, 252.3 s**.
  No Flutter implementation changed, so no new history widget pass is claimed.

Existing Chemistry's final 1,908 backend / 609 Flutter / 3 PostgreSQL results are
historical baseline evidence, **not new Jahon tarixi test results**.

## Completed catalogue checkpoint, 2026-10-26

- All961 original page images inspected for feature presence/layout. Every page
  has a digest-bound manual observation record and candidate parent binding.
- Complete219-unit teaching map: 46/44/33/41/26/29 by grade. Supporting records
  explicitly retained. No historical fact approved merely by catalogue status.
- **46 source/chronology/preservation tests passed in4.00s**. Mutations include
  forged render hash, duplicate/bool page, unknown/duplicate feature, missing
  heading/reference/unit/binding, wrong prerequisite/location/parent link.
- All687 protected files matched their baseline SHA-256 values.
- Critical Ruff (`F821,F822,E9`) and `git diff --check` passed.
- No history executable lesson, runtime, UI or DB import at this checkpoint.

## Batch01 — grade6§1–6, 2026-10-26

**Local preview only; the219-unit course remains incomplete.** Six lessons,
55 original theory cards,92 fact records,39 MCQ,19 objective FRQ and6 ungraded
self/teacher-review activities.213 units remain.

| Check | Measured result | Scope |
| --- | --- | --- |
| Full backend regression |2569 passed,4 skipped;71 files;2462.19s wall | First-lesson implementation snapshot, four isolated UTF-8 subprocess shards; frozen inputs preserved |
| Current history/source/preservation tests |88 passed in100.73s | All6 current manifests, exact source regions/digests, question-specific targets/aliases, activities, immutable API/progress/XP |
| Actual PostgreSQL |1 passed | Dedicated new history staging cluster; immutable import, snapshots, parallel first completion, all6 sequential lessons/120XP, old synthetic account preserved |
| Actual loopback HTTP |6 grade catalogues,58 answers,120XP | Prerequisites, auth, private-key exclusion, replay, once-only completion; synthetic users only |
| Full Flutter regression |632 passed,07:44 | Current six-lesson implementation and all existing UI/subject tests |
| Targeted history widgets |23 passed,00:17 | Real API fixtures for§1–6, MCQ/FRQ, source sheet, resume/account switch, lost request, 320×568/200%, light/dark, UZ/RU/EN |
| Full Flutter analysis |0 issues,183.2s | Entire history Flutter worktree |
| Preservation |687 SHA-256 pins matched |406 Biology +268 Chemistry lesson files and13 existing backend runtime/model/router files |
| Critical Ruff / Git whitespace |Passed | New history code and diffs |

The broad backend run's4 opt-in PostgreSQL skips are **not passes**. History's
real PostgreSQL scenario ran separately and passed. Initial broad-run Windows
subprocess decoding failures were environmental: both Biology tests passed with
`PYTHONUTF8=1`; the full UTF-8 rerun then passed without editing Biology.

Real PostgreSQL caught an overlong session kind; it was shortened to
`history_assessment_v2`, leaving the existing VARCHAR(24) schema intact.
The private HTTP sandbox is intentionally SQLite; its legacy DB bootstrap message
does not describe the separate real PostgreSQL test.

Inspected widget renders include path/bibliography, first theory, correct/wrong
feedback, scrollable explanation at200%, FRQ flow and self-review. Source PDF/map
images were not bundled. Screenshots/logs/DBs/tokens stay private. No actual Android,
IME/TalkBack, independent history-teacher sign-off or complete2026–2027 outcome
equivalence is claimed. No production/main/deploy/real-user operation occurred.

## Batch02 — grade6§7–11, 2026-10-26

Five additional reviewed lessons:44 cards,72 fact records,29 MCQ and17 objective
FRQ. Total **11/219 local-preview lessons**,99 cards,164 facts,68 MCQ,36 FRQ and11
self/teacher activities;208 units remain. Whole-book course-ready flags are false.

| Check | Measured result | Scope |
| --- | --- | --- |
| Current backend/source/preservation |96 passed in158.95s | All11 lessons, source regions/digests, private per-question keys, aliases, beliefs/interpretations, original44 map legend, immutable API and once-only220XP |
| Actual PostgreSQL |1 passed in26.22s | Dedicated history staging schema; parallel first completion, all11 sequential lessons,220XP, pre-existing synthetic account unchanged |
| Actual loopback HTTP |6 grade catalogues,104 answers,220XP | Fresh synthetic learner; prerequisites and idempotent completion; no old progress reset |
| Current targeted Flutter |33 passed in00:12 | Actual API fixtures§1–11; MCQ/FRQ, 320×568/200% theory/feedback, resume, UZ/RU/EN and prior safeguards |
| Full Flutter regression |642 passed in03:41 | Entire current suite; common UI and existing subject tests included |
| Full Flutter analysis |0 issues in112.4s | Entire current Flutter history worktree |
| Protected baseline |687 SHA pins matched | Existing406 Biology +268 Chemistry manifests and13 runtime files |
| Critical Ruff / whitespace |Passed | History code/tests and Git diffs |

The full2569-backend regression recorded above remains the first-lesson snapshot;
it was not rerun for this content-only batch. Current96 tests cover all new
content and the unchanged history runtime. The new batch adds no production route,
database migration or application networking change.

The initial§11 FRQ widget test failed because its66KB fixture crossed Dio's
background-isolate decoding threshold outside the widget fake-async zone. The
fixture adapter now uses synchronous decoding, preserving strict response checks.
All33 targeted tests and then all642 full tests passed. This was a test harness
timing issue; no shared runtime/UI/subject code was changed.

Inspected actual widget renders:§7 theory at200%,§10 feedback at200%,§11 resumed
FRQ and earlier shared-feedback scroll states. No PDF image was bundled.
No actual Android/IME/TalkBack, independent teacher approval, full2026–2027
equivalence, deployment, main merge or real-user access is claimed.

## Batch03 — grade6§12–16, 2026-10-26/27

Five additional lessons:46 original cards,78 fact records,29 MCQ and21 objective
FRQ. Total **16/219 local-preview lessons**,145 cards,242 facts,97 MCQ,57 objective
FRQ and16 self/teacher activities;203 units remain (30 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Current backend/source/preservation |104 passed in137.99s | All16 lessons, exact source regions/digests and answer targets, explicit Xattusa/Xatusa variants, rejection of unreviewed aliases, complete prerequisite/XP flow |
| Actual PostgreSQL |1 passed in22.81s | Dedicated history staging; parallel first completion, all16 sequential lessons/320XP, old synthetic account preserved |
| Actual loopback HTTP |6 grade catalogues,154 answers,320XP | Fresh synthetic learner; locked-next enforcement and idempotent completion; prior learner progress retained |
| Targeted Flutter |43 passed in00:38 | Real API fixtures§1–16, new MCQ/objective FRQ, 320×568/200%, shared feedback and prior auth/resume/language checks |
| Full Flutter regression |652 passed in03:41 | Entire current suite; common UI and existing subjects included |
| Full Flutter analysis |0 issues in120.6s | Entire Flutter history worktree |
| Preservation |687 SHA pins matched |406 Biology +268 Chemistry manifests and13 protected runtime files; prior11 history manifests unchanged |
| Critical Ruff / whitespace |Passed | History source/tests and staged diffs |

The original2569-pass full-backend snapshot is historical regression evidence,
not a rerun for batch03. Current104 tests and the separate real PostgreSQL test
were run after finalizing all new manifests and before publication. No history
runtime/schema or ordinary application route was modified in this content batch.

§14's unresolved shoh-yo‘li endpoints are absent from unqualified learner prose
and automatic keys; the original discrepancy stays visible in fact-review notes.
Other scoped issues: first-law/prior-law wording, legal-equality generalization,
Misr annexation attribution, state-collapse causes, caste/varna simplification,
literal divine/rebirth narratives, and exact calendar/innovation priorities.
None is silently promoted to a reviewed correction or definitive answer.

Inspected widget renders include§12 feedback at200%,§15 theory at200%,§16 resumed
FRQ, plus prior source/feedback scroll states. No actual native Android, IME,
TalkBack, independent teacher sign-off, full2026–2027 equivalence, production/main
operation, raw-source publication or real-user access is claimed.

## Batch04 — grade6§17–21, 2026-10-27

Five additional lessons:41 cards,71 fact records,26 MCQ,20 objective FRQ. Total
**21/219 local-preview lessons**,186 cards,313 facts,123 MCQ,77 objective FRQ and21
ungraded self/teacher activities;198 units remain (25 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Current backend/source/preservation |112 passed in196.85s | All21 lessons, source identity/regions/digests, exact answer targets, reviewed aliases, disputed facts excluded, complete prerequisites and once-only420XP |
| Actual PostgreSQL |1 passed in29.16s | Dedicated history staging; parallel first completion, all21 sequential lessons,420XP, old synthetic account preserved |
| Actual loopback HTTP |6 grade catalogues,200 answers,420XP | Fresh synthetic learner; ordered access/replay and no previous-progress reset |
| Targeted Flutter |53 passed in00:44 | Actual API fixtures§1–21, third-chapter opening, MCQ/FRQ, 320×568/200%, previous resume/account/language safeguards |
| Full Flutter regression |662 passed in03:58 | Entire current suite, including shared UI and existing subjects |
| Full Flutter analysis |0 issues in96.9s | Entire current Flutter history worktree |
| Preservation |687 SHA pins matched |406 Biology +268 Chemistry manifests and13 protected runtime files; prior16 history manifests unchanged |
| Critical Ruff / whitespace |Passed | History code/tests and staged diffs |

The full2569-pass backend snapshot remains earlier evidence, not a batch04 rerun.
Current112 tests and separate real PostgreSQL ran against the finalized21-lesson
manifests. History runtime/schema and production routes remain unchanged.

Unresolved Chjou69/71 chronology, Qin246 timing, rice-origin and tea-health
wording, seismograph prediction, exact wall metrics, ancient-city relative ages,
astrological etymology, literal revelation, geographic fractions and definite
collapse models are excluded from automatic keys as documented. The seismograph
prediction sentence has its own unassessed fact ID and cannot enter the reviewed
instrument-name feedback. No invented correction date or external fact was added.

Actual widget renders inspected:§18 feedback at200%,§19 resumed FRQ and§21 theory
at200%, plus prior shared-feedback scroll states. No source PDF images bundled.
Independent teacher review, native Android/IME/TalkBack and full2026–2027 outcome
certification remain pending; no production/main/real-user operation occurred.

## Batch05 — grade6§22–26, 2026-10-27

Five additional lessons:35 cards,68 fact records,28 MCQ and20 objective FRQ.
Total **26/219 local-preview lessons**,221 cards,381 facts,151 MCQ,97 objective FRQ
and26 ungraded activities;193 units remain (20 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Current backend/source/preservation |122 passed in451.74s | Seven history test modules; all26 lessons, identity/region/digest/target gates, exclusions, finite Periek variants, prerequisites/replay and520XP once |
| Actual PostgreSQL |1 passed in54.78s | Fresh schema in dedicated history staging; parallel completion and all26 sequential lessons, old synthetic account preserved |
| Actual loopback HTTP |6 catalogues,248 answers,520XP | Fresh synthetic learner900056, prerequisite/replay checks; prior learner accounts not reset |
| Targeted Flutter |63 passed in01:28 | Actual API fixtures§1–26, small-screen/200% theory/MCQ and resumed FRQ, prior language/account/snapshot guards |
| Full Flutter regression |672 passed in05:57 | Entire current suite, shared and other subject coverage included |
| Full Flutter analysis |0 issues in138.6s | Entire history Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing406 Biology/268 Chemistry manifests plus13 runtime files; all42 prior history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python history modules/scripts/tests only; git diff check |

The earlier2569-pass full backend snapshot is baseline evidence, not a rerun here.
The first overly broad Ruff glob accidentally included a PowerShell OCR script;
rerunning with Python-only paths passed. No source/runtime fix was needed.
Tool-generated Flutter plugin line-ending changes were restored separately.

Original86–104 exact paragraph regions reviewed;91/98/102 wholly next-topic pages
were excluded from preceding lessons,93/104 shared boundaries are explicit.92
period mismatch,96 council headship, schematic citizenship/education, Marathon
runner and ship precision remain withheld/scoped; no external correction invented.
Source-review record contains the full decisions. Actual renders inspected:
§24 feedback at200%,§26 resumed FRQ and§23 theory at200%; shared feedback scroll
tests passed. No PDF images bundled, native run or teacher approval claimed.

## Batch06 — grade6§27–31, 2026-10-27

Five additional lessons:39 cards,79 fact records,30 MCQ and20 objective FRQ.
Total **31/219 local-preview lessons**,260 cards,460 facts,181 MCQ,117 objective FRQ
and31 ungraded activities;188 units remain (15 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Current backend/source/preservation |132 passed in583.39s | Eight history modules, all31 manifests; exact boundaries, aliases, objective chronology, source decisions, prerequisites and620XP once |
| Actual PostgreSQL |1 passed in53.72s | Dedicated staging fresh schema; parallel first completion,31 sequential lessons and old synthetic account preservation |
| Actual loopback HTTP |6 catalogues,298 answers,620XP | Fresh synthetic learner900066, prerequisites/replay and no previous-progress reset |
| Targeted Flutter |73 passed in01:30 | Actual API fixtures§1–31, four original chapters, 320×568/200% theory/MCQ, resumed FRQ and previous account/language safeguards |
| Full Flutter regression |682 passed in06:25 | Entire current suite, including existing subject/shared UI tests |
| Full Flutter analysis |0 issues in128.6s | Entire current history Flutter worktree |
| Preservation |687 baseline SHA pins matched |406 Biology/268 Chemistry manifests plus13 runtime files; all52 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python-only history paths and git diff check |

Earlier full backend2569/4-skipped evidence remains a baseline, not a batch06 rerun.
No schema or shared/runtime/release route changed. Tool-generated Flutter plugin
line-ending files restored separately. New public fixtures contain no private keys.

Exact original104–122 topic regions reviewed. Whole next-topic pages115/118/123
excluded from preceding lessons;107/111 shared regions explicit. Reviewed decisions
cover Olympic dating/place conflation, Trojan-horse episode attribution, separate
philosopher name pairs, all deity-table rows and conflicting campaign narratives.
No external era/date correction or literal supernatural/scientific claim invented.

Inspected actual widget renders:§27 theory at200%,§29 resumed FRQ,§31 feedback
at200%. No native Android/IME/TalkBack, independent teacher sign-off or full2026–27
programme equivalence claimed. No production/main/real-user operation or raw PDF,
page-image/full-text/OCR publication occurred.

## Batch07 — grade6§32–36, 2026-10-27

Five additional lessons:37 cards,75 fact records,30 MCQ and20 objective FRQ.
Total **36/219 local-preview lessons**,297 cards,535 facts,211 MCQ,137 objective FRQ
and36 ungraded activities;183 units remain (10 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Final backend/source/preservation |142 passed in353.78s | Nine history modules;36 manifests, exact regions/aliases, chronology, source decisions, owner/snapshot/prerequisite/replay and720XP once |
| JWT fixture regression |2 passed in19.15s | Fresh signed default token per request; explicit expired JWT remains401, normal signed JWT200; production auth/TTL unchanged |
| Actual PostgreSQL |1 passed in69.87s | Dedicated staging; parallel completion and36 sequential lessons, old synthetic learner retained |
| Actual loopback HTTP |6 catalogues,348 answers,720XP | Fresh synthetic learner900076; prior learner accounts not reset |
| Targeted Flutter |83 passed in00:52 | Actual API fixtures§1–36, source/MCQ/resumed FRQ, 320×568/200% and earlier account/language guards |
| Full Flutter regression |692 passed in02:57 | Entire current Flutter worktree suite |
| Full Flutter analysis |0 issues in88.9s | Entire current Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime retained; all62 prior history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python-only history paths and staged diff check |

The initial backend run had140 passes and one401 failure after a long wall-clock
delay expired its default test JWT (10518.24s elapsed). The test fixture now signs
a fresh default token for each request and preserves explicitly provided owner or
expired tokens. It bypasses no signature/expiry/owner checks, extends no production
TTL and changes no runtime file. The two focused cases and the full142-test rerun
passed. The failed first run is not claimed as a pass. Earlier full2569 backend
results remain historical baseline evidence, not a rerun in this batch.

Original123–144 regions reviewed, shared137 explicit, whole next-topic129/133/142/
145 excluded where appropriate.134 calendar CEI/BCEI contradiction, successor and
military era compression, script genealogy, coin/chess priority and route precision
are withheld or attributed. No outside replacement facts or guessed map routes.
Actual widget renders inspected:§34 feedback at200%,§35 theory at200%,§36 resumed
FRQ. No native/independent-teacher or
production acceptance is claimed. Original PDF/page/OCR and private tokens stay out
of Git; only public API payloads are Flutter fixtures.

## Batch08 — grade6§37–41, 2026-10-27

Five additional lessons:32 cards,67 fact records,30 MCQ and20 objective FRQ.
Total **41/219 local-preview lessons**,329 cards,602 facts,241 MCQ,157 objective FRQ
and41 ungraded activities;178 units remain (5 in grade6).

| Check | Measured result | Scope |
| --- | --- | --- |
| Backend/source/preservation |152 passed in434.92s | Ten history modules;41 manifests, exact source/regions/keys/aliases, prerequisites, replay and820XP once |
| Actual PostgreSQL |1 passed in55.41s | Dedicated history staging fresh schema; parallel completion and41 sequential lessons, old synthetic learner retained |
| Actual loopback HTTP |6 catalogues,398 answers,820XP | Fresh synthetic learner900086; prior progress never reset |
| Targeted Flutter |93 passed in01:03 | Actual API fixtures§1–41, source/MCQ/resumed FRQ,320×568/200%, previous account/language guards |
| Full Flutter regression |702 passed in03:23 | Entire current Flutter suite |
| Full Flutter analysis |0 issues in101.8s | Entire current Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus all72 prior history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python-only history files and staged diff |

Earlier full2569 backend results remain historical baseline evidence. No shared
runtime/schema or production route changed. Actual widget renders inspected:
§38 feedback200%,§40 theory200%,§41 resumed FRQ. No native Android/IME/TalkBack,
independent teacher or production acceptance claimed.

Original145–164 exact topic regions reviewed; founding legend, constitutional
universals, religious/divination claims, army-era compression, battle precision,
slave-status stereotypes and thumb gestures scoped/withheld. No absent map route,
external replacement date, raw textbook image/OCR, private key or real-user data
published. Only history feature branches receive these changes.
