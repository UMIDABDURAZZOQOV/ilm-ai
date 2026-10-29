# World history: integration boundaries

## Starting checkpoints

- Backend: Chemistry `9b37213cfeeebb358f2179d76c8c5d97417f1861`, including
  Biology 406 and Chemistry 268 reviewed lesson manifests.
- Flutter: Chemistry `0312ff3108e96e1e3446bdc8c4dcb27fe7ecd37d`.
- Separate branch in each repository: `feat/world-history-curriculum`.
- Existing Biology, Chemistry, Physics and UI worktrees/branches are not edited.
- `protected_baseline.json` pins all 674 existing lesson files and 13 existing
  backend runtime/model/router/validation files. Their bytes must remain intact.

## Common learning contract

Reuse the existing v2 contract and common ILM sequence: source-backed theory,
server-graded MCQ/topic-appropriate FRQ, authored feedback, result, threshold,
atomic once-only XP, progress, prerequisites, save/resume and replay. The Physics
prototype is not treated as a finished production grader. History work must
remain opt-in and independently regression-tested until reviewed integration.

Objective names, terms and dates may use explicit accepted alternatives.
Chronological selection/order exercises use only verified taught event/date
relations. Complex interpretations/opinions are self-review or teacher-review;
never fuzzy automatic true/false marking. BCE/CE arithmetic must reject display
year zero and distinguish ordering from elapsed-year calculations.

The isolated history runtime/schema/UI adapter now exists for local QA. It
preserves authenticated identity, immutable server snapshots, private keys,
expiry, sequential submission, cross-account isolation and replay protections.
Never expose grading specs/aliases/expected answers in start or local drafts.
Use additive isolated tables and explicit reviewed manifest imports. No startup
seed, production connection, production DDL or modification of existing progress.

## Source contract

Each fact, theory card, question, answer, explanation, date/person/region and
cause-effect relation must retain the supplied book identity/SHA, grade,
chapter/topic, printed/PDF pages, fact ID, verification and review note.
Image review is an evidence record, not independent teacher certification.
Uncertain OCR, outdated universal interpretations and unresolved discrepancies
must not become auto-graded facts. Preserve review history and correction bases.

Keep Uzbek authored content. UZ/RU/EN interface labels must remain functional;
unreviewed translation is not published historical content. Reuse Ilmo and
existing source/feedback/completion components. Provide grades 6–11, original
chapter/topic order and separate bibliography in the reviewed UI adapter.

## Implemented local adapter

- `services/world_history_lessons.py`: exact page/region render digests, reviewed
  facts/cards, per-question answer targets/aliases and source-activity coverage.
  Two terms in one fact are not interchangeable aliases for every question.
- Separate history model/curriculum/runtime modules: four isolated tables, explicit
  immutable import, authenticated accounts, snapshots,24h expiry, ordered answers,
 60% completion and20XP first pass only. Shared account/session/event contract.
- Session kind `history_assessment_v2` fits the existing24-character column.
  The initial longer value failed real PostgreSQL; no common schema was changed.
- `/preview/world_history/v2`: opt-in development/test local staging only.
  Ordinary main/startup/other subject routers remain unchanged.
- Explicit import CLI is DB/ORM-free by default; apply/schema steps require local QA.
  Separate loopback server uses synthetic users and private defines outside Git.
- Flutter `lib/world_history_preview_main.dart`: separate debug/loopback entry,
  Ilmo/theme/source sheets/shared feedback/completion, six grades, original chapter
  expansion, bibliography, theory/MCQ/typed FRQ, self-review and account/origin resume.
- Source and schema checks remain mandatory. No production certification is
  inherited from the unfinished Physics prototype.

The batch42 checkpoint has219 explicitly allowed units (all grade6/7/8/9 plus grade10§1–26 and grade11§1–29). Content additions do not
change the common runtime/schema or ordinary release routes. Future reviewed revisions must
retain prior manifest bytes and validate exact page regions and finite per-question
answer targets before immutable local import. See CHECKPOINT.md and QA_REPORT.md.

## Exact review-unit predecessor context

Ancillary conclusion/review units may cite earlier numbered units of the same
book. The ordered loader supplies only its validated prefix; standalone review
resolves the explicit digest-pinned import index. No inferred filename, future
unit, cross-book context or arbitrary numbered-lesson context is allowed.
`approved_context_sha256` pins each prior lesson; per-fact bindings pin the exact
prior fact. Reused facts retain original pages, regions, render hashes, aliases
and assessability; only local fact IDs differ. A glossary locator is not a meaning
approval. Neither a held fact nor a broader alias can be promoted by review.

All six grades now have `grade_content_complete=true`: their46/44/33/41/26/29
local-preview units exist. This does not mean a learner completed them or that
independent acceptance is complete. `course_complete` and all source-book `course_ready` flags remain false.
Grade selection/progress are independent: grade7 first lesson has no cross-grade
prerequisite. Completing grade7 does not mark grade6 complete; account XP remains
shared, awarded once per immutable lesson. The catalogue finalizer preserves explicit ancillary readiness and review fields;
its original-page presence inventory cannot approve new facts or content.

## Completed implementation and future review

All219 catalogue entries are now represented by source-reviewed interactive
lessons. The measured final audit and exact source limits are in
WORLD_HISTORY_FINAL_AUDIT.md, FINAL_COVERAGE_REPORT.json and SOURCE_REVIEW.md.
Initial authoring and per-batch backend/Flutter/HTTP/PostgreSQL checkpoints are
complete; do not restart the source inventory or overwrite immutable lessons.
Future substantive edits need a new reviewed revision and the same strict
validation and regression checks. No AI Tutor/Explain/translation, production
operation, main merge or deployment is authorized. Independent history-teacher
and actual Android/IME/TalkBack checks remain unperformed and must not be claimed.
