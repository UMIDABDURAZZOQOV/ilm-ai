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

## Batch09 — grade6§42–44, conclusion and final review, 2026-10-27

Five additional units:32 cards,70 fact records,30 MCQ and18 objective FRQ.
Total **46/219 local-preview units**,361 cards,672 fact records,271 MCQ,175 objective
FRQ and46 ungraded activities. Grade6 is46/46 (44 numbered paragraphs + conclusion
and final review);173 units remain across grades7–11. Twelve final-review records
reuse exact earlier facts; record totals are not unique historical-fact counts.

| Check | Measured result | Scope |
| --- | --- | --- |
| Focused grade completion/context |17 passed in83.25s | Exact earlier-book context pins, aliases, scope, regions, index membership, finalizer preservation and grade transition |
| All history backend/source/preservation |169 passed in691.12s | Eleven modules;46 manifests, earlier regression cases, ordered completion/replay and920XP once |
| Actual PostgreSQL |1 passed in50.03s | Dedicated staging fresh schema; parallel completion/all46 units, older synthetic account preserved |
| Actual loopback HTTP |6 catalogues,446 answers,920XP | Fresh learner900096, prerequisites/replay, no previous-account reset |
| Targeted Flutter |106 passed in01:19 | Actual API fixtures all46 units, 320×568/200% theory/feedback/FRQ; real titles/source sheets for ancillary units and switch to grade7 pending catalogue |
| Full Flutter regression |715 passed in04:05 | Entire current Flutter suite, including shared and other subject tests |
| Full Flutter analysis |0 issues in90.6s | Entire history Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subject/runtime files plus82 prior history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python-only history paths and staged diff checks |

Review units may reuse earlier same-book numbered facts only through exact prior
lesson and fact digests. Tests reject absent indexed predecessors, unknown/future/
cross-book context, changed claims/aliases/assessment scope, remapped origins and
arbitrary reuse by regular numbered lessons. The ordered loader uses its validated
prefix; standalone validation resolves the explicit import index. No source gate
was bypassed. The finalizer preserves explicitly recorded ancillary readiness
and fact review; grade8's unimplemented conclusion stays unapproved.

`grade_content_complete` now reports local content presence for all46 grade6 units,
independently of learner completion. Earlier test expectations were updated for
this truthful catalogue state; previous XP/progress/prerequisite cases remain.
`course_complete` and all source-book acceptance flags remain false. Grade7 has no
imported teaching yet; switching there shows its44 source units as pending, not
an invented lesson. Existing learner progress is retained.

Original164–180/184 read. Caesar title/29BCE precision, outsider stereotypes,
world-first concrete, all-school/bath claims, religious miracles and political
values withheld/scoped.184 is a locator; copied exact earlier facts retain their
actual source pages, not184. Full-list review remains guided self/teacher work.
Inspected widget renders:§43 feedback200%,unit45/46 source sheets200%,§46 resumed
FRQ with original§39/152,153,155 citation. Source sheets/content scroll; no native
Android/IME/TalkBack or independent teacher acceptance claimed. Earlier2569-pass
full backend snapshot remains historical baseline evidence, not a rerun here.

Only history feature branches are committed/pushed. No production/main, real-user,
raw PDF/full-text/OCR/page-image publication or AI operation occurred. Next batch
is grade7§1–5; its opening source3–12 read and§1 draft validated privately.

## Batch10 — grade7§1–5, 2026-10-27

Five additional lessons:39 cards,83 fact records,32 MCQ and20 objective FRQ.
Total **51/219 local-preview units**,400 cards,755 fact records,303 MCQ,195 objective
FRQ and51 ungraded activities. Grade6 remains46/46; grade7 is5/44,39 remaining.
There are168 units left across grades7–11. Record totals include exact repeated
final-review facts and are not a unique historical-fact count.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend/source/preservation |178 passed in792.00s | Twelve history modules, all51 manifests, exact page/region/alias/source review, earlier regressions and6→7 transition |
| Actual PostgreSQL |1 passed in51.22s | Dedicated staging fresh schema; parallel first completion, all51 units/1020XP once, previous synthetic account retained |
| Actual loopback HTTP |6 catalogues,498 answers,1020XP | Fresh learner900106; grade6 then7, prerequisites/replay and no previous learner reset |
| Targeted Flutter |118 passed in01:32 | API fixtures for51 units, grade7 theory/MCQ200%, typed FRQ/source identity and local draft remount, prior safeguards |
| Full Flutter regression |727 passed in04:21 | Entire current worktree suite, shared and other subjects included |
| Full Flutter analysis |0 issues in85.4s | Entire current Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime and92 prior grade6 lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | Python-only history files and staged diff checks |

Grade7 first lesson has no cross-grade prerequisite. A new learner can start it
without marking any grade6 lesson completed; grade7 second lesson remains locked
until its own prerequisite. Tests complete all51 units once, retain grade6 history
and check shared1020XP. Earlier grade6 tests now count their own grade rather than
mistaking all imported grades for grade6. The runtime/schema and release routes
are unchanged. Grade7's first5 lessons are complete for the synthetic learner but
`grade_content_complete=false` because39 source units remain; course completion
and source-book acceptance flags stay false.

Original3–29 reviewed: author/introduction contexts belong to§1; shared12/17/21/26/
29 regions explicit. Allod16/17 language conflict, dynasty-founder/epic certainty,
Ambrosiy/Artur identity, Alfred reign/peace precision and Gerbert/Silvestr ordinal
are withheld rather than silently corrected externally. Source details appear in
SOURCE_REVIEW.md. No absent map route, present border or unprovided comparison
fact was invented. Objective names/terms and chronology are source-checked.

Actual widget renders inspected: grade7§2 feedback200%,§5 resumed FRQ and opening
source sheet200% with Salimov/Sultonov's own book. Sources/content are scrollable.
No actual Android/IME/TalkBack or independent teacher sign-off claimed. Earlier
2569-pass full backend snapshot remains baseline evidence, not a full rerun here.
No original PDF/full text/OCR/page images, private keys or real-user data in Git.
Only the two history feature branches are committed/pushed. Next: grade7§6–10;
§6 original29–33 read and its private draft validated, next original34 for§7.

## Batch11 — grade7§6–10, 2026-10-27

Five additional lessons:37 cards,84 fact records,32 MCQ and20 objective FRQ.
Total **56/219 local-preview units**,437 cards,839 fact records,335 MCQ,215 objective
FRQ and56 ungraded activities. Grade6 remains46/46; grade7 is10/44,34 remaining.
There are163 units left across grades7–11. Repeated final-review facts remain
included in record counts; these are not unique-fact totals.

| Check | Measured result | Scope |
| --- | --- | --- |
| Focused new backend |12 passed in87.70s | Five source manifests, seven shared-region mutations, finite targets/holds and all56-unit completion |
| All history backend/source/preservation |190 passed in1225.33s | Thirteen history modules, all56 manifests, earlier source/runtime regressions |
| Actual PostgreSQL |1 passed in80.38s | Dedicated staging fresh schema; parallel completion, all56 units/1120XP once and old synthetic user retained |
| Actual loopback HTTP |6 catalogues,550 answers,1120XP | Fresh learner900116; prerequisites/replay; no previous learner reset |
| Targeted Flutter |128 passed in01:36 | All56 API fixtures, grade7 chapter2, theory/MCQ200%, typed FRQ and earlier safeguards |
| Actual capture subset |20 passed in02:03 | Grade7§1–10 theory/feedback200% and FRQ renders written privately |
| Full Flutter regression |737 passed in08:24 | Entire current worktree suite, other subjects/shared functions included |
| Full Flutter analysis |0 issues in238.1s | Entire current Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus102 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python files only and diff checks |

Initial Flutter run found23 failures in test expectations/helpers: public start
snapshots do not contain sequence, and chapter1 no longer contains pending rows
once§1–9 are ready. The helper now resolves source-unit title and opens its actual
chapter; pending assertion opens chapter2. No production snapshot/schema change.
Rerun128/128 and full737/737 passed; the failed run is not claimed as acceptance.

Original29–50 read with exact boundary regions;37,47 and51 wholly belonging to
next topics are excluded where applicable. Source law40 death-penalty assertion,
Platon epithet42, alphabet creation46 and kvadrium45 spelling remain unassessed.
No external correction, Greek-fire recipe, religious loyalty/truth score or
unprovided map fact was introduced. Question-specific aliases reject Yasrib when
the prompt explicitly asks for its other nameMadina. More in SOURCE_REVIEW.md.

Actual renders inspected: grade7§6 theory200%,§9 feedback200%,§10 resumed FRQ
with its own§10/50 source. Text is scrollable. No native Android/IME/TalkBack or
independent teacher sign-off claimed. Earlier2569-pass full backend snapshot
remains baseline evidence, not a full backend rerun here. No source PDF/full
text/OCR/page images, real-user data or keys in Git. Only history feature branches.
Next batch12: grade7§11–15 original51–70 read; five private drafts validate,
92 fact records/39 cards/52 questions, not yet indexed/imported.

## Batch12 — grade7§11–15, 2026-10-27

Five additional lessons:39 cards,92 fact records,32 MCQ and20 objective FRQ.
Total **61/219 local-preview units**,476 cards,931 fact records,367 MCQ,235 objective
FRQ and61 ungraded activities. Grade6 remains46/46; grade7 is15/44,29 remaining.
There are158 units left across grades7–11. Counts include exact reused review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |203 passed,596.73s wall | All14 history modules in four isolated subprocess shards;36/27/75/65 passes,420.92/374.75/392.89/593.00s each; no omitted module |
| Actual PostgreSQL |1 passed in183.47s | Dedicated staging fresh schema, parallel completion and all61 units/1220XP once; previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,602 answers,1220XP | Fresh learner900126, prerequisites/replay and no previous learner reset |
| Targeted Flutter/captures |138 passed in03:42 | API fixtures for61 units, grade7 chapter3, theory/MCQ200% and typed FRQ; actual renders written privately |
| Full Flutter |747 passed in05:17 | Entire worktree suite, shared functions/other subjects included |
| Full analysis |0 issues in173.3s | Entire current Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus112 earlier history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

Four backend subprocesses use independent test databases/temp directories and
fresh fixture auth; the dedicated PG and HTTP flows remain separate. This changes
test orchestration only. Runtime, source strictness, auth and lesson bytes are not
relaxed. Earlier cumulative completion tests retain their exact historical prefix;
new61-unit flow checks1220XP and distinct grade progress. Grade7 is still incomplete.

Original51–70 image-reviewed: all topic boundaries, institution/land/money/art
terms and66 three-field diagram checked. Source errors and uncertain priorities
stay in SOURCE_REVIEW, with no external historical correction, explosives recipe,
medical procedure, compulsory religion or human-worth hierarchy.

Actual renders inspected: grade7§11 feedback200%,§14 theory200%,§15 resumed FRQ
with§15/65–66 source. Native Android/IME/TalkBack/independent teacher checks remain
unperformed. Earlier2569-pass full backend snapshot is baseline evidence, not a
full rerun. No PDF/full source text/OCR/page images, real-user data or keys in Git.
Only history feature branches. Next:§16–20; original70–83 read, private§16–18
drafted; author§19 then inspect84 onward for§20.

## Batch13 — grade7§16–20, 2026-10-27

Five additional lessons:34 cards,77 fact records,32 MCQ and20 objective FRQ.
Total **66/219 local-preview units**,510 cards,1008 fact records,399 MCQ,255 objective
FRQ and66 ungraded activities. Grade6 remains46/46; grade7 is20/44,24 remaining.
There are153 units left across grades7–11. Counts include exact reused review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |217 passed,612.42s wall | All15 modules/four isolated subprocess shards;50/27/75/65 passes,425.40/225.57/268.36/607.04s; none omitted |
| Actual PostgreSQL |1 passed in102.40s | Dedicated fresh staging schema, parallel completion and all66 units/1320XP once; previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,654 answers,1320XP | Fresh learner900136; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |148 passed in03:43 | All66 API fixtures, theory/MCQ200%, typed FRQ and prior safeguard coverage |
| Full Flutter |757 passed in04:54 | Entire suite, shared/other-subject functions included; successful no-pub rerun |
| Full analysis |0 issues in183.1s | Entire Flutter worktree |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus122 prior history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python files only and Git diff checks |

Initial full Flutter invocation stopped before running tests because simultaneous
dependency preparation could not delete ios/Flutter/ephemeral/Packages/.packages.
Analysis completed successfully. With unchanged resolved dependencies, a sequential
`flutter test --no-pub` rerun passed all757. No manual recursive deletion, package
upgrade, production runtime change or failed-run-as-pass claim.

Original70–86 reviewed with exact topic boundaries. Source market/bank priorities,
Kioto chronology, ecclesiastical terminology and universal social claims remain
scoped/withheld. Urban promises and complex motives are ungraded. No absent map,
theological repair, religious hierarchy or practical combat content introduced.
Question-specific aliases distinguish Ioanniy-other-name from Hospital identity.
See SOURCE_REVIEW.md for exact original page decisions.

Actual renders inspected: grade7§17 theory200%,§19 feedback200%,§20 typed FRQ
with its own§20/83 source. Native Android/IME/TalkBack and independent teacher
checks remain unperformed. Earlier2569-pass full backend is baseline evidence,
not a full backend rerun. No PDF/full source text/OCR/page images, real-user data
or keys in Git; only two history feature branches. Next:§21–25; original86–97
read and five private drafts validate,68 fact records/31 cards/52 questions.

## Batch14 — grade7§21–25, 2026-10-27

Five additional lessons:31 cards,68 fact records,32 MCQ and20 objective FRQ.
Total **71/219 local-preview units**,541 cards,1076 fact records,431 MCQ,275 objective
FRQ and71 ungraded activities. Grade6 remains46/46; grade7 is25/44,19 remaining.
There are148 units left across grades7–11. Counts include reused final-review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |229 passed,603.81s wall | All16 modules/four independent shards;50/47/75/57 passes,449.03/430.33/247.40/599.44s; none omitted |
| Actual PostgreSQL |1 passed in118.08s | Dedicated fresh staging schema; parallel completion and all71 units/1420XP once, previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,706 answers,1420XP | Fresh learner900146; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |158 passed in02:48 | All71 API fixtures, chapter4,200% theory/MCQ,typed FRQ and earlier safeguards |
| Full Flutter |767 passed in04:46 | Entire worktree suite, no-pub with unchanged dependencies |
| Full analysis |0 issues in164.4s | Entire Flutter worktree, no-pub |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus132 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

The completed-grade6 transition test now resolves the next pending source unit's
actual chapter from the catalogue. This retains a pending-row assertion after
chapter3 becomes fully reviewed and chapter4 contains the next pending unit.
Source-unit chapter/title navigation is checked for new§22–25. No runtime, auth,
release route, subject manifest or real-user progress changed.

Original86–97 reviewed. Difficult chronology/king ordinals and source claims stay
scoped: Latin empire, French centralization, estates, HundredYearsWar and Joan.
The erroneous/uncertain formulations in SOURCE_REVIEW are not correct-answer
keys; no outside historical replacement is invented. 89 and98 are excluded from
the previous whole-page topics. All original questions/activities remain linked.

Actual renders inspected: grade7§22 theory200%,§24 feedback200%,§25 resumed FRQ
with§25/96–97. Native Android/IME/TalkBack/independent teacher checks remain
unperformed. Earlier2569-pass full backend is baseline evidence, not full rerun.
No PDF/full source text/OCR/page images, keys or real-user data in Git; only two
history feature branches. Next:§26–30; original98–108 read, private§26–28 written,
next original109 for§29 and110 for§30.

## Batch15 — grade7§26–30, 2026-10-27

Five additional lessons:33 cards,72 fact records,32 MCQ and20 objective FRQ.
Total **76/219 local-preview units**,574 cards,1148 fact records,463 MCQ,295 objective
FRQ and76 ungraded activities. Grade6 remains46/46; grade7 is30/44,14 remaining.
There are143 units left across grades7–11. Counts include reused final-review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |241 passed,830.56s wall | All17 modules/four independent shards;50/47/87/57 passes,724.09/697.26/616.47/825.06s; none omitted |
| Actual PostgreSQL |1 passed in108.59s | Dedicated fresh staging schema; parallel completion and all76 units/1520XP once, previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,758 answers,1520XP | Fresh learner900156; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |168 passed in07:18 | All76 API fixtures,200% theory/MCQ,typed FRQ and prior safeguards |
| Full Flutter |777 passed in08:35 | Entire worktree suite, no-pub with unchanged dependencies |
| Full analysis |0 issues in109.5s | Entire Flutter worktree, no-pub |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus142 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

Exact shared-page regions preserve adjacent topics;102 and108 are excluded from
the preceding lessons. Roles, king ordinals, names and question-specific aliases
are tested. In particular, Nevskiy is the other-name target, whereas Aleksandr
Yaroslavich is the full-name target. Historical interpretations remain ungraded.

The first HTTP-helper command lacked PYTHONPATH and stopped before loading the
database or creating its learner. With PYTHONPATH set, the actual fresh-user flow
passed all758 answers. No progress reset or failed-run-as-pass claim.

Actual renders inspected: grade7§26 theory200%,§28 feedback200%,§30 resumed FRQ
with its own§30/110 source. Native Android/IME/TalkBack/independent teacher checks
remain unperformed. The earlier2569-pass full backend is baseline evidence,
not a full backend rerun. No PDF/full source text/OCR/page images, keys or real-user
data in Git. Only two history feature branches. Next:§31–35; original112–118
read, private§31–32 drafted, next119 for§33 then121–125 for§34–35.

## Batch16 — grade7§31–35, 2026-10-27

Five additional lessons:34 cards,74 fact records,34 MCQ and20 objective FRQ.
Total **81/219 local-preview units**,608 cards,1222 fact records,497 MCQ,315 objective
FRQ and81 ungraded activities. Grade6 remains46/46; grade7 is35/44,9 remaining.
There are138 units left across grades7–11. Counts include reused final-review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |253 passed,351.41s wall | All18 modules/four independent shards;62/47/87/57 passes,348.72/290.74/260.83/348.15s; none omitted |
| Actual PostgreSQL |1 passed in71.66s | Dedicated fresh staging schema; parallel completion and all81 units/1620XP once, previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,812 answers,1620XP | Fresh learner900166; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |178 passed in00:59 | All81 API fixtures,chapter5,200% theory/MCQ,typed FRQ and prior safeguards |
| Full Flutter |787 passed in07:30 | Entire worktree suite, successful sequential no-pub rerun |
| Full analysis |0 issues in196.4s | Entire Flutter worktree, no-pub |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus152 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

Initial simultaneous targeted/full Flutter startup hit a NativeAssetsManifest.json
copy collision in build/unit_test_assets before the full suite ran. The targeted
run passed178. After it finished, a sequential full no-pub rerun passed787. No
dependency upgrade, manual recursive delete or failed-run-as-pass claim. Future
Flutter targeted and full test commands must run sequentially; no-pub alone does
not isolate their generated build output.

Shared page bounds retain chapter4→5 and exclude117/121 from the prior lessons.
Per-question targets distinguish Donskoy, electedrektor/appointedkansler, artterms,
RomanIV/MehmetII/Yildirim; source-year order1402before1453 is taught explicitly.
Uncertain source claims remain in SOURCE_REVIEW, without outside replacements.

Actual renders inspected: grade7§32 theory200%,§34 feedback200%,§35 resumed FRQ
with§35/123–124. Native Android/IME/TalkBack/independent teacher checks remain
unperformed. Earlier2569-pass full backend is baseline evidence, not full rerun.
No PDF/full source text/OCR/page images, keys or real-user data in Git; only two
history feature branches. Next:§36–40; original125–136 read, private§36–37 drafted,
next author§38 using132–136 then read137–140 for§39–40.
