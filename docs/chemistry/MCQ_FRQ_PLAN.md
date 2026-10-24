# Common learning contract and Chemistry integration

2026-10-24. Stable backend base `c0f84d0`; Flutter UI base `444743b`.
Physics `07f748b` and Flutter `cf01011` were inspected read-only.
No unmerged Physics branch was used as the Chemistry base.

## One learning structure

Source -> short original theory -> original MCQ/topic-appropriate FRQ -> authored
feedback -> existing result/XP/progress. Every claim and assessment links to a
taught fact and an image-reviewed page. Activities use guided digital analysis.
No independent hazardous experiment, live translation or AI feedback.

Biology v1 keeps its MCQ constraint and existing 406 manifests. Physics v2 is a
local/test-only preview with private rubrics, immutable StudySession snapshots,
authenticated ownership, 24-hour expiry, ordered answers, replay fingerprints,
StudyEvent ledger and once-only completion XP. It is not production-ready FRQ.

Chemistry uses this same versioned contract through an isolated local preview
adapter and separate opt-in tables/namespace. No change to Physics files,
Biology validators, startup import, mobile publication allowlist or main routes.
Before eventual shared-engine consolidation, compare pinned contract tests and
coordinate the merge explicitly. An isolated adapter is not a new pedagogy.

## First paragraph

Grade7 §1 is conceptual/history content. Start with MCQ plus bounded, authored
short-text concept answers (normalised case/Uzbek apostrophe variants; no fuzzy
semantic grading). Do not invent formula/equation/numeric questions before the
book teaches them. Reviewed aliases remain server-private.

## Reviewed topic-specific extensions

Batch02 introduced exact numeric input in the unit fixed by the prompt. Batch04
adds case-sensitive formula notation and finite balanced-equation checking after
reviewing §9–13. See ASSESSMENT_CONTRACT.md for actual supported syntax and bounds.
Formula counts do not predict products; only reviewed textbook species and
answer keys are authoritative. Numeric prose, fuzzy grading and eval are absent.

Charge/isotope/structural input, oxidation-state syntax, numerical tolerance and
general unit conversion remain future topic-specific extensions. Add them only
with source review, explicit rules and negative tests; do not claim the current
introductory parser already provides them. Ambiguous data go to review.

All cards, worked example steps, question prompts, answers and solution steps
must carry source refs, not just one blanket lesson citation. Client payloads
contain no expected answers/rubrics before submission. Format errors can be
corrected without disclosing the solution. Identity, input limits, forged score,
unknown IDs, replay conflicts, expiry and duplicate completion must be tested.

Flutter reuses Ilmo, light/dark brand, existing source/feedback/result components
and learning conventions. Chemistry preview is explicit local QA; the released
Biology flow remains intact. Test small/landscape screens, 200% text, keyboard
and focus. Report native TalkBack/phone QA separately from widget tests.
