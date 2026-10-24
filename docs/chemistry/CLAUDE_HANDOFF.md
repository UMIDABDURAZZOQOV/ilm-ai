# Central CLAUDE.md handoff: Chemistry

The central CLAUDE.md in the Chemistry branch records this permanent requirement
and links this handoff. The shared Biology worktree's CLAUDE.md was not changed.

User's permanent rule: **all subject knowledge must come only from user-provided,
verified textbooks**. No unverified memory, OCR guesses, replacement facts or live
AI generation. Original explanations/questions are allowed only within taught,
page-reviewed textbook knowledge. All formulas/answers/feedback require precise
paragraph/page evidence. Scientific contradictions enter a review queue.
Full requirements: docs/chemistry/REQUIREMENTS.md.

Chemistry branches: backend/Flutter `feat/chemistry-curriculum` in separate
worktrees, from stable Biology `c0f84d0` and polished UI `444743b` respectively.
Reviewed Flutter implementation was pushed at `14b3407` (first preview `4642e38`).
Physics code `07f748b`/`cf01011` read-only. Its unfinished v2 FRQ remains local
preview, not an already available production mechanism. Use the same learning,
server grading, XP/progress/prerequisite/replay rules across subjects; do not
invent incompatible educational engines.

Five supplied Uzbek sources are pinned by SHA/edition: grades7/8/9/10/11 actual
PDF counts81/208/208/160/160. Grade7 spread regions and singleton front/back;
grades10/11 scans require original-image review. Catalogue:29 chapters,
204 paragraphs,49 laboratories,15 practicals,327 records/268 teaching entries.
All source maps exist; this does not mean all interactive content is ready.
Current interactive counts and exact next source: CURRICULUM_PROGRESS.md.

First local lesson: `chemistry-7-p01-r1`, eight cards, nine MCQ, three short-text
FRQ; printed3–8 with spread regions. Strict deterministic input and source gates,
immutable server snapshots, ordered/replayed answers and once-only XP are tested.
The known grade9 §40/page186 contradiction has a machine-enforced review hold.
All other267 source teaching entries remain unauthored. Next is7-sinf §2,
printed9/PDF5:right. Formula/equation/numeric grading is not yet implemented.

PDFs/OCR/page renders stay private. Drafts never auto-import. Test-only explicit
allowlist, source validation and isolated DB required; production data/user
progress, Biology's406 lessons and Physics work remain unchanged. No AI feature,
main merge or production publication is authorized.


## 2026-10-24 continuation ? authoritative latest state

User explicitly authorizes automatic sequential batches of 5?10 lessons through
all five grades, with source review, validation, staging, tests and a pushed
checkpoint after each batch. Do not request routine continuation approval.
Preserve ?1 bytes and commits. Source order is ?2 substance properties, practical1
safety, practical2 apparatus, ?3 particles/elements, ?4 mass, then ?5 substances.
The earlier ?2 safety label is a handoff error, not source evidence.
See CURRICULUM_PROGRESS.md and CHECKPOINT.md for current counts and next source.
The only new response kind is bounded exact numeric_value with the unit fixed
in the public prompt; it is not a formula/equation engine. Short-text grading
remains unchanged. Chemical symbols are case-sensitive MCQ labels.
