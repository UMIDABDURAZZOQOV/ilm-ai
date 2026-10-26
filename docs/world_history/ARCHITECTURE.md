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

No history runtime/schema/UI adapter exists at this checkpoint. Before adding
one, preserve authenticated identity, immutable server snapshots, private keys,
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
chapter/topic order and separate bibliography once the reviewed UI adapter exists.

## Mandatory continuation and acceptance

Finish the complete source/activity catalogue, then author grade 6 §1 onward in
source order through the end of grade 11. In each 5–10 lesson batch, inspect the
actual source pages, validate taught facts and answer keys, run backend/Flutter
and needed local HTTP/PostgreSQL QA, update exact readiness, commit and push the
history feature branches. Do not ask routine continuation permission.

Keep total/implemented/remaining counts, last grade/topic, unresolved issues,
tests, commit/push and the next exact page. A final audit is requested only after
all catalogue entries are accounted for. No AI Tutor/Explain/translation,
production operation, main merge or deployment is authorized. Independent history
teacher and actual Android/TalkBack checks must never be claimed without a run.
