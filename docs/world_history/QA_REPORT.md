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

## Batch17 — grade7§36–40, 2026-10-27

Five additional lessons:36 cards,82 fact records,36 MCQ and20 objective FRQ.
Total **86/219 local-preview units**,644 cards,1304 fact records,533 MCQ,335 objective
FRQ and86 ungraded activities. Grade6 remains46/46; grade7 is40/44,4 remaining.
There are133 units left across grades7–11. Counts include reused final-review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |267 passed,767.94s wall | All19 modules/four independent shards;62/47/101/57 passes,738.19/555.76/652.53/763.54s; none omitted |
| Actual PostgreSQL |1 passed in139.92s | Dedicated fresh staging schema; parallel completion and all86 units/1720XP once, previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,868 answers,1720XP | Fresh learner900176; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |188 passed in03:58 | All86 API fixtures,200% theory/MCQ,typed FRQ and prior safeguards |
| Full Flutter |797 passed in05:13 | Entire worktree suite, sequential no-pub after targeted tests |
| Full analysis |0 issues in224.0s | Entire Flutter worktree, no-pub |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus162 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

Every opening/closing shared page is bounded; chronology, titles, office names,
full-name targets and distinct Korean polities remain source-specific. Tangun is
explicit legend-comprehension, not factual founder biography or personal faith.
The uncertain claims in SOURCE_REVIEW are absent from automatic answer keys.

Actual renders inspected: grade7§37 theory200%,§39 feedback200%,§40 resumed FRQ
with§40/139. Native Android/IME/TalkBack/independent teacher checks remain
unperformed. Earlier2569-pass full backend is baseline evidence, not full rerun.
No PDF/full source text/OCR/page images, keys or real-user data in Git; only two
history feature branches. Next:§41–44; original140–146 read, private§41–42 drafted,
then original147–154 plus155–156chronology. After grade7, continue grade8.

## Batch18 — grade7§41–44 and chronology reference, 2026-10-27

Four remaining grade7 lessons:31 cards,70 fact records,36 MCQ and16 objective FRQ.
Total **90/219 local-preview units**,675 cards,1374 fact records,569 MCQ,351 objective
FRQ and90 ungraded activities. Grade6 remains46/46; grade7 is44/44,0 remaining.
Grades8–11 have129 units left. Counts include reused final-review facts.

| Check | Measured result | Scope |
| --- | --- | --- |
| All history backend |278 passed,435.95s wall | All20 modules/four independent shards;62/58/101/57 passes,428.60/432.07/385.06/419.83s; none omitted |
| Actual PostgreSQL |1 passed in117.37s | Dedicated fresh staging schema; parallel completion and all90 units/1800XP once, previous synthetic user retained |
| Actual loopback HTTP |6 catalogues,920 answers,1800XP | Fresh learner900186; prerequisites/replay, no old learner reset |
| Targeted Flutter/captures |197 passed in02:31 | All90 API fixtures,200% theory/MCQ,typed FRQ,completed7→8 and bibliography; successful rerun |
| Full Flutter |806 passed in05:40 | Entire worktree suite, sequential no-pub after targeted tests |
| Full analysis |0 issues in74.8s | Entire Flutter worktree, after final test-helper changes |
| Preservation |687 baseline SHA pins matched | Existing subjects/runtime plus172 previous history lesson/review files byte-identical |
| Critical Ruff / whitespace |Passed | History Python only and Git diff checks |

Nine earlier backend tests now derive grade7 content availability from the current
catalogue while preserving their frozen learner prefix, once-onlyXP and unfinished
learner-progress assertions. Content presence44/44 is separate from global course
acceptance and learner completion. Both grade6 and7 presence complete; grade8
pending/source records retain their own bibliography and independent progress.

The first targeted Flutter run had194passes/3failures in test helpers: title-only
selection confused the two Hindiston lessons, and a bibliography assertion ran
before its expansion. Helpers now resolve lesson_key→sequence→chapter and check
the actual start request, then expand bibliography. The full197-test rerun passed.
No runtime/auth/subject manifest change or failed-run-as-pass claim.

All48 original155–156chronology entries reviewed with exact image pins and scoped
dispositions in GRADE7_REFERENCE_REVIEW.md. Lesson44 reference is ungraded; a list
repeating an error cannot promote it. Original source errors/caption mismatches
remain in SOURCE_REVIEW. Grade7 presence complete is not independent acceptance.

Actual renders inspected: grade7§41 theory200%,§44 resumed FRQ with§44/151 and
completed7→8 with its own2019bibliography. Native Android/IME/TalkBack/independent
teacher checks remain unperformed. Earlier2569-pass full backend is baseline
evidence, not full rerun. No rawbook/OCR/images, keys or real-user data in Git.
Only two history feature branches. Next:grade8§1–5; original3–13 read, first private
draft23facts/11cards/14questions, then original14–34 for§2–5.

## Batch19 — grade8§1–5, 2026-10-27

Five lessons add45 cards,85 fact records,46 MCQ and20 objective FRQ. Total
**95/219 local-preview lessons**,720 cards,1459 fact records,615 MCQ,371 FRQ,
95 self/teacher activities. Grade6/7 complete content presence46/44; grade8 has5/33.
**124 remain:** grade8=28,grade9=41,grade10=26,grade11=29. All acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |290 passed,905.50s wall | All21 modules,four isolated shards62/58/101/69;614.82/593.40/551.48/897.51s |
| Dedicated PostgreSQL |1 passed in96.82s | Fresh schema,parallel completion/all95 units1900XP/replay,old synthetic retained |
| Actual loopback HTTP |6 catalogues,986 answers,1900XP | Fresh synthetic900196,prerequisites/replay,not real users |
| Targeted Flutter |209 passed in04:05 | Own grade8 API snapshots,all95 lessons,320×568/200% theory/MCQ,typed FRQ,source and draftremount |
| Full Flutter |818 passed in05:54 | Sequential no-pub after targeted suite,allworktree tests |
| Final full analysis |0 issues in160.7s | Final test helper version |
| Preservation |687 baseline pins,180 previous history files unchanged | No refresh of baseline or rewrite of published lesson/review pairs |
| Ruff/diff/staged audit |Passed | History Python criticalerrors,whitespace and history-only text artifacts |

Grade8 starts independently: its first lesson can finish while grades6/7 remain
unstarted. Source identity remains2019Farmonov/Jo‘rayev/Ergashev, including linked
intro3–6. Bothgrades6/7 remaincomplete in the95-unit learnerflow; XP once perlesson.
The old grade7 implemented-grades assertion now derives available grades from
current lesson presence while retaining its grade7-only learner/XP assertions.

Private authoring initially omitted PYTHONPATH before any draft mutation; corrected.
Strict pre-import validation rejected two incomplete shared-boundary region tags;
private drafts were corrected to below_topic_heading/above_next_heading, then all
five validated before immutable import. Validator/runtime were not loosened.
Actual Flutter renders inspected: grade8§1 theory200%,§3 sharedfeedback200%,§5 FRQ
with its own31–33 source. Native Android/IME/TalkBack and independent teacher review
remain unperformed.2569 fullbackend passes are the earlier baseline, not this
targeted rerun. No PDFs/rawOCR/images/keys/realuser data in Git. Only twohistory
featurebranches; no mainmerge,deploy,other-subject runtime or production database.

Next batch20:grade8§6–10. Original3–37 read;§6 private draft not indexed. Read38
onward for§7–10. All ambiguous source details stay in SOURCE_REVIEW, not keys.

## Batch20 — grade8§6–10, 2026-10-27

Five lessons add36 cards,61 fact records,42 MCQ and20 objective FRQ. Total
**100/219 local-preview lessons**,756 cards,1520 fact records,657 MCQ,391 FRQ,
100 self/teacher activities. Grade6/7 complete content presence46/44;grade8 is10/33.
**119 remain:** grade8=23,grade9=41,grade10=26,grade11=29. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |303 passed,1347.83s wall | All22 modules/four isolated shards75/58/101/69;1262.78/855.01/784.73/1343.65s |
| Actual PostgreSQL |1 passed in200.62s | Fresh dedicatedschema/parallel completion/all100units2000XP/replay |
| Actual HTTP |6 catalogues,1048 answers,2000XP | Freshsynthetic900206/prerequisites/replay/noexistinguserreset |
| Targeted Flutter |219 passed in06:37 | All100publicAPI snapshots/200% theoryMCQ/typedFRQ/grade8draftsource |
| Full Flutter |828 passed in09:32 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0 issues in219.1s | EntireFlutterworktree |
| Preservation |687 baseline pins and190 previoushistoryfiles unchanged | Frozen other-subject/runtime and earlierlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | HistoryPython criticalerrors/history-only textfiles/noJWTprivateDB |

Scoped source limits in SOURCE_REVIEW; calendarlabels/imperialmapcolour areas/
politicalcausation never replace reviewedfactevidence. Tests reject expanded shared
regions,incorrect maprenderdigest,unassessed chronology keys,regnalordinal aliases
and mixing Konsul with Konsullik. All previous95 lesson/review pairs immutable.
Actual captures inspected:§6darktheory200%,§8darksharedfeedback200%,§10typedFRQ
withitsown49/53source. Independentteacher/nativeAndroid/IME/TalkBack remain
unperformed. Earlier2569-pass fullbackend is baseline evidence,notthisrerun.
No mainmerge/deploy/productionDB/AIfeature/rawPDFimagesOCR/realuserdata in Git.
Only thetwohistoryfeaturebranches. Nextbatch21 grade8§11–15; original3–65read,
private§11written butnotindexed; author12 next, then66onward. Do notcountprivatedrafts asready.

## Batch21 — grade8§11–15, 2026-10-27

Five lessons add37 cards,63 fact records,39 MCQ and19 objective FRQ. Total
**105/219 local-preview lessons**,793 cards,1583 fact records,696 MCQ,410 FRQ,
105 self/teacher activities. Grade6/7 complete content presence46/44;grade8 is15/33.
**114 remain:** grade8=18,grade9=41,grade10=26,grade11=29. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |317 passed,383.08s wall | All23 modules/four isolated shards75/72/101/69;379.17/380.31/279.43/381.44s |
| Actual PostgreSQL |1 passed in85.06s | Fresh dedicatedschema/parallel completion/all105units2100XP/replay |
| Actual HTTP |6 catalogues,1106 answers,2100XP | Freshsynthetic900216/prerequisites/replay/noexistinguserreset |
| Targeted Flutter |229 passed in01:30 | All105publicAPI snapshots/200% theoryMCQ/typedFRQ/grade8source |
| Full Flutter |838 passed in03:12 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0 issues in144.0s | EntireFlutterworktree |
| Preservation |687 baseline pins and200 previoushistoryfiles unchanged | Frozen other-subject/runtime and earlierlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | HistoryPython criticalerrors/history-only textfiles/noJWTprivateDB |

Source limits in SOURCE_REVIEW: constitutional vocabulary, mapregion identifiers,
patron versus dedicatee, finite full names and attributed cultural models remain
distinct. All prior100 lesson/review pairs immutable. Actual widget captures:
§11 lighttheory200%,§13 lightsharedfeedback200%,§15 typedFRQsource/resume.
Independentteacher/nativeAndroid/IME/TalkBack remain unperformed. Earlier2569-pass
fullbackend is baseline evidence,notthisrerun. No production/userdata/AIfeature.
The first attempt to launch full Flutter was not executed: automatic approval
review could not initialize because the disk was full. Removed only completed
first-baseline pytest scratch directories after resolving their absolute paths;
preserved reports/logs/source images and all user/progress databases. Then reran
the same authorized analysis/test commands successfully through approval review.
Nextbatch22 grade8§16–20; original3–84read,private§16written butnotindexed.

## Batch22 — grade8§16–20, 2026-10-27

Five lessons add39 cards,65 fact records,39 MCQ and20 objective FRQ. Total
**110/219 local-preview lessons**,832 cards,1648 fact records,735 MCQ,430 FRQ,
110 self/teacher activities. Grade6/7 complete content presence46/44;grade8 is20/33.
**109 remain:** grade8=13,grade9=41,grade10=26,grade11=29. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |331 passed,933.89s wall | All24 modules/four isolated shards75/72/101/83;750.26/739.71/436.63/931.17s |
| Actual PostgreSQL |1 passed in80.70s | Fresh dedicatedschema/parallel completion/all110units2200XP/replay |
| Actual HTTP |6 catalogues,1165 answers,2200XP | Freshsynthetic900226/prerequisites/replay/noexistinguserreset |
| Targeted Flutter |239 passed in02:59 | All110publicAPI snapshots/200% theoryMCQ/typedFRQ/grade8source |
| Full Flutter |848 passed in06:16 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0 issues in66.8s | EntireFlutterworktree |
| Preservation |687 baseline pins and210 previoushistoryfiles unchanged | Other-subject/runtime and priorlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | HistoryPython criticalerrors/history-only textfiles/noJWTprivateDB |

Source review holds in SOURCE_REVIEW. Tests reject broad office aliases, partial
names, switching regnal name with literary name, dominion with independence,
grading racist ideology as truth, modified source-render digest and broadened
shared opening/closing regions. Validator caught97 chapter-opening page scope
before publication; private source scope narrowed to below_topic_heading.
All105 prior lesson/review pairs immutable. Actual widget captures inspected:
§16 darktheory200%,§17 lightsharedfeedback200%,§20 typedFRQsource/resume.
Independentteacher/nativeAndroid/IME/TalkBack remain unperformed. Earlier2569-pass
fullbackend is baseline evidence,notthisrerun. No production DB/userdata/deploy/AI.
No textbookPDF/images/OCR in Git. Only two history feature branches.
Nextbatch23 grade8§21–25; original3–101read, next102 onward. No private work counted ready.

## Batch23 — grade8§21–25, 2026-10-28

Five lessons add40 cards,67 fact records,40 MCQ and24 objective FRQ. Total
**115/219 local-preview lessons**,872 cards,1715 fact records,775 MCQ,454 FRQ,
115 self/teacher activities. Grade6/7 complete content presence46/44;grade8 is25/33.
**104 remain:** grade8=8,grade9=41,grade10=26,grade11=29. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |345 passed,1810.48s wall | All25 modules/four isolated shards75/72/115/83;1508.92/1478.99/1340.48/1807.5s |
| Actual PostgreSQL |1 passed in206.92s | Fresh dedicatedschema/parallel completion/all115units2300XP/replay |
| Actual HTTP |6 catalogues,1229 answers,2300XP | Freshsynthetic900236/prerequisites/replay/noexistinguserreset |
| Targeted Flutter |249 passed in05:45 | All115publicAPI snapshots/200% theoryMCQ/typedFRQ/grade8source |
| Full Flutter |858 passed in05:38 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0 issues in187.5s | EntireFlutterworktree |
| Preservation |687 baseline pins and220 previoushistoryfiles unchanged | Other-subject/runtime and priorlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | HistoryPython criticalerrors/history-only textfiles/noJWTprivateDB |

Source limits in SOURCE_REVIEW. Tests reject incorrect regnalordinal, partial
names, switching literary and opera authors, historicalunion with presentstate,
grading colonial social categories as biological facts, altered original render
digest and broadened shared page regions. Full names and Morelos continuation
relation are explicitly taught before FRQ, not merely present in answer keys.
All110 prior lesson/review pairs immutable. Actual captures inspected:§21 light
theory200%,§23 lightsharedfeedback200%,§25 typedFRQsource/resume.
Independentteacher/nativeAndroid/IME/TalkBack remain unperformed. Earlier2569-pass
fullbackend is baseline evidence,notthisrerun. No production DB/deploy/AI/userdata.
No textbookPDF/images/OCR in Git. Only two history feature branches.
Nextbatch24 grade8§26–30; original3–138read/private§26–27 strictvalidated notindexed.

Precommit audit found initial grade8 catalogue exported during an unfinished
import still listed20 lessons, while completed API flow correctly covered25.
After importer completion, fresh synthetic900237 re-exported allsix initial
catalogues; verified grade8=25 before rerunning targeted and full Flutter suites
sequentially. Original synthetic900236 progress/results retained. Private HTTP
export helper now asserts each grade count against validated lesson index before
writing fixtures. Import command must finish before dependent HTTP QA starts.

## Batch24 — grade8§26–30, 2026-10-28

Five lessons add35 cards,49 fact records,28 MCQ and20 objective FRQ. Total
**120/219 local-preview lessons**,907 cards,1764 fact records,803 MCQ,474 FRQ,
120 self/teacher activities. Grade6/7 complete content presence46/44;grade8 is30/33.
**99 remain:** grade8=3,grade9=41,grade10=26,grade11=29. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |359 passed,1411.56s wall | All26 modules/four isolated shards89/72/115/83;1368.41/1028.23/975.15/1407.0s |
| Actual PostgreSQL |1 passed in159.20s | Fresh dedicatedschema/parallel completion/all120units2400XP/replay |
| Actual HTTP |6 catalogues,1277 answers,2400XP | Freshsynthetic900246/prerequisites/replay/noexistinguserreset |
| Targeted Flutter |259 passed in05:12 | All120publicAPI snapshots/200% theoryMCQ/typedFRQ/initialcatalogueguard |
| Full Flutter |868 passed in06:41 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0 issues in251.5s | EntireFlutterworktree |
| Preservation |687 baseline pins and230 previoushistoryfiles unchanged | Other-subject/runtime and priorlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | HistoryPython criticalerrors/history-only textfiles/noJWTprivateDB |

Tests reject partial names, king/regent/title substitutions, broad sameperson
aliases when a prompt requests another name, imperialdivinity/superiority as an
automatictruth, alteredmaprender and broadenedregions. Sipohiy is explicitly
scoped to the current chapter. FirstOpiumWar interval is marked bookperiodization.
Importer completion was awaited before dependent HTTP export. Private exporter
asserted allsix grade counts; Flutter now compares initial and latest completed
grade8 implemented counts and row counts. Both snapshots contain30 lessons.
All115 prior lesson/review pairs immutable. Actual captures inspected:§26 dark
theory200%,§27 lightsharedfeedback200%,§30 typedFRQsource/resume.
Independentteacher/nativeAndroid/IME/TalkBack remain unperformed. Earlier2569-pass
fullbackend is baseline evidence,notthisrerun. No production DB/deploy/AI/userdata.
No textbookPDF/images/OCR in Git. Only two history feature branches.
Nextbatch25 grade8§31–33 then grade9§1–2; grade8 original3–156 read and private
lastthree strictvalidated, notindexed. Scannedgrade9originalfactreview next.

## Batch25 — grade8§31–33 then grade9§1–2, 2026-10-28

Five units add40 cards,63 fact records,32 MCQ and23 objective FRQ. Three records
reuse exact prior grade8 knowledge; record totals are not unique knowledge counts.
Total **125/219 local-preview units**,947 cards,1827 fact records,835 MCQ,497 FRQ,
125 self/teacher activities. Grade6/7/8 content presence complete46/44/33;
grade9=2/41. **94 remain:**39/26/29 in grades9/10/11. Acceptance flags false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |373 distinct tests pass across27 modules | Four initial shards372pass/1obsolete expectation; corrected entire17testbatch09 rerun passes60.33s |
| Actual PostgreSQL |1 passed189.46s | Fresh dedicatedschema/parallel completion/all125units2500XP/replay |
| Actual HTTP |6catalogues,1332answers,2500XP | Freshsynthetic900256/prerequisites/grade9independentfirst/replay |
| Target Flutter |271 passed05:18 | All125API snapshots/200% theoryMCQ/typedFRQ/8→9transition/scannedbibliography |
| Full Flutter |880 passed04:24 | Sequential no-pub aftertargeted; entireworktree |
| Full analysis |0issues206.6s | EntireFlutterworktree |
| Preservation |687 baseline pins,240 previoushistoryfiles unchanged | Other-subject/runtime and120priorlesson/review bytes |
| Ruff/whitespace/stagedaudit |Passed | CriticalPythonerrors/history-only text/noJWTprivateDB/rawsources |

Initial shard counts88/72/115/97 at1779.58/1630.02/1566.83/1865.94seconds. The
initial batch09 finalizer test still expected grade8 conclusion to be pending.
Its assertion now compares fact_review and interactive_status for EVERY ancillary
record against the input catalogue: preserve reviewed and pending records alike.
No validator weakening/runtime change. Focused test passed2.52s, then all17 tests
in that module passed60.33s. Distinct passing coverage is373, not a claimed clean
four-shard rerun. Unchanged372 other tests passed their original executions.

New checks reject modified scan digests, tampered predecessor/context bindings,
invented recapfacts, partial person/document names, migration/urbanization alias
substitution, imperialist/colonial/workerjudgments as automatictruth and crossgrade
prerequisite confusion. Grade9first starts without finishinggrade8, second requires
its ownfirst. All125 completion replay unchanged, other synthetic accountXP137 kept.
Importer completion awaited, HTTP allsix counts guarded. Initialgrade8=33 and
grade9=2; completed snapshots match. Both8→9 and grade9intro own bibliography tested.
Actual captures inspected:grade8§31theory200%,grade9§1feedback200%,scannedintro
source200%. Grade8 conclusion exact earlierfact origins preserved, no raw map reuse.
Fullbackend2569pass/4skip remains earlier baseline,not this run. Independentteacher,
nativeAndroid/IME/TalkBack/full2026–27equivalence not performed/certified. No production
DB/deploy/AI or reallearnerdata. All changes only two history featurebranches.
Next batch26 grade9§3–7; original1–30 read, private drafts strictvalidated, unindexed.

## Batch26 — grade9§3–7, 2026-10-28

Five lessons add34 cards,56 fact records,30 MCQ and22 objective FRQ. Total
**130/219 local-preview units**,981 cards,1883 fact records,865 MCQ,519 FRQ,
130 self/teacher activities. Grade9=7/41;grades6/7/8 content presence46/44/33.
**89 remain:**34/26/29 in grades9/10/11. All acceptance flags remain false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |387 passed,1517.52s wall | All28modules,four clean shards103/72/115/97;1425.39/981.61/914.72/1514.31s |
| Actual PostgreSQL |1 passed171.41s | Dedicatedschema/parallel completion/all130units2600XP/replay after existingservice resume |
| Actual HTTP |6catalogues,1384answers,2600XP | Freshsynthetic900267/uniqueemail/gradedprerequisites/replay |
| Target Flutter |282 passed06:00 | All130snapshots/200% theoryMCQ/typedFRQ/grade9prefixguard |
| Full Flutter |891 passed06:27 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0issues227.2s | EntireFlutterworktree |
| Preservation |687pins and250priorhistoryfiles unchanged |125priorlesson/review pairs and other-subject/runtime baseline |
| Ruff/whitespace/stagedaudit |Passed | History-only text/noJWTprivateDB/rawscanOCR |

Tests reject changed scan/region digests, partialperson/institutionnames, ordinal
substitution, broadaliases, racial superiority and politicalcauses as automatic
truth. Dates are tied to specific events, not neighboring declarations; doubtful
war day/constitutional/treaty details have no answer keys. Frozen priorfixtures
retained, newgrade9initialcatalogue and latestcompletion both7lessons guarded.
Actual captures inspected:§3theory200%,§6darkfeedback200%,§7typedFRQresume/source.

LocalQA service incident: HTTP connection refused and PostgreSQL connection
failed before acceptance tests could run. Existing dedicated servers were resumed;
no initdb/drop/reset. PostgreSQL recovered its earlier unclean shutdown and became
ready after startup helper's60s timeout; readiness log was checked before rerun.
First HTTP attempt had created UID900266 but no lesson progress. NewUID900267
initially collided with its batch email; transaction rolled back. Exporter now uses
UID-specific syntheticemail; successful full run above preserves earlier accounts.
These initial infrastructure failures are not reported as passes. Existing
learnerdata and realusers were not reset/accessed. No other-subjectserver touched.

Earlier2569pass fullbackend remains baseline evidence,not this run. Independent
teacher/nativeAndroid/IME/TalkBack/full2026–27equivalence not performed/certified.
No productionDB/deploy/mainmerge/AI/sourceupload. Nextbatch27 grade9§8–12 private
strictvalidated, not indexed; originals1–46 read, continue§13and47onward next.

## Batch27 — grade9§8–12, 2026-10-28

Five lessons add31 cards,50 fact records,30 MCQ and20 objective FRQ. Total
**135/219 local-preview units**,1012 cards,1933 fact records,895 MCQ,539 FRQ,
135 self/teacher activities. Grade9=12/41;grades6/7/8 content presence46/44/33.
**84 remain:**29/26/29 in grades9/10/11. All acceptance flags remain false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |402 passed,827.17s wall | All29modules,four clean shards103/87/115/97;777.42/634.76/506.26/825.92s |
| Actual PostgreSQL |1 passed96.97s | Dedicatedschema/parallel completion/all135units2700XP/replay |
| Actual HTTP |6catalogues,1434answers,2700XP | Freshsynthetic900276/UID-specificemail/prerequisites/replay |
| Target Flutter |292 passed03:36 | All135snapshots/200% theoryMCQ/typedFRQ/grade9prefixguard |
| Full Flutter |901 passed03:13 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0issues135.8s | EntireFlutterworktree |
| Preservation |687pins and260priorhistoryfiles unchanged |130priorlesson/review pairs and other-subject/runtime baseline |
| Ruff/whitespace/stagedaudit |Passed | History-only text/noJWTprivateDB/rawscanOCR |

Tests reject altered scan/regions, ordinal/name/nickname and institution swaps,
broadaliases, political onlycorrectpath as automatictruth, external legal/date/
scientific guesses and misrepresentedcompletedrailway. Names and historical
policy labels are question-specific; colonial/religious/identity judgments remain
self/teacher only. Original priorfixtures frozen; initial and completion grade9
catalogues both12rows. Actual captures inspected:§8darktheory200%,§10darkfeedback
200%,§12typedFRQresume/source. No QA service interruption in this run.
Fullbackend2569pass/4skip remains earlier baseline,not this run. Independentteacher,
nativeAndroid/IME/TalkBack/full2026–27equivalence not performed/certified. No
productionDB/deploy/mainmerge/AI/rawsourceupload/reallearnerreset. Nextbatch28
grade9§13–17 private strictvalidated, not indexed; originals1–63andappendix154read.
155–156 notdeepreviewed,64onward next. Appendix154 only exact linkedtopic17facts.

## Batch28 — grade9§13–17, 2026-10-28

Five lessons add36 cards,60 fact records,32 MCQ and22 objective FRQ. Total
**140/219 local-preview units**,1048 cards,1993 fact records,927 MCQ,561 FRQ,
140 self/teacher activities. Grade9=17/41;**79 remain:**24/26/29 in grades9/10/11.
Grade6/7/8 content presence46/44/33; all acceptance flags remain false.

| Check | Actual result | Scope |
| --- | --- | --- |
| All history backend |416 passed,1549.00s wall | All30modules,four clean shards103/87/129/97;1475.69/1268.17/1180.96/1546.99s |
| Actual PostgreSQL |1 passed63.21s | Dedicatedschema/parallel/all140units2800XP/replay |
| Actual HTTP |6catalogues,1488answers,2800XP | Freshsynthetic900286/UID-specificemail/prerequisites/replay |
| Target Flutter |302 passed05:06 | All140snapshots/200% theoryMCQ/typedFRQ/grade9prefixguard |
| Full Flutter |911 passed08:34 | Entireworktree sequential no-pub aftertargeted |
| Full analysis |0issues67.5s | EntireFlutterworktree |
| Preservation |687pins and270priorhistoryfiles unchanged |135priorlesson/reviewpairs plus other-subject/runtime baseline |
| Ruff/whitespace/stagedaudit |Passed | History-only text/noJWTprivateDB/rawscanOCR |

New tests reject broadened shared-page regions, swapped people/policy names,
unapproved initials and automatic political/identity judgments. Appendix154 is
only exact linked§17 context with original image SHA;155–156 are not approved by
that lesson, and whole appendix fact_review remains not_reviewed. Prior fixtures
remain frozen; initial and completed grade9 catalogues both17rows. Actual widget
captures inspected:§14darktheory200%,§16darkfeedback200%,§17typedFRQ/source/resume.
No QA service interruption. Source details and all holds remain in SOURCE_REVIEW.
Private§18–22 passed strict validation; original1–80and154–155 read,156 pending.
These next drafts are not indexed/imported. Independentteacher/nativeAndroid/
IME/TalkBack/full2026–27equivalence remain unperformed. Fullbackend2569/4skip is
the earlier baseline, not this run. No productionDB/deploy/mainmerge/AI/rawsource
upload/reallearnerreset. Continue batch29 without routine permission.
