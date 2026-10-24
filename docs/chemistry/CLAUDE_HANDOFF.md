# Chemistry handoff — authoritative current state

## Permanent user instruction

All scientific knowledge comes exclusively from the five user-supplied,
page-reviewed textbooks. Original teaching, questions and worked arithmetic are
allowed; unverified memory, OCR guesses, missing-page replacements and live AI
are not. Exact paragraph, printed/PDF page, spread region and PDF identity apply
to facts, formulas, examples, questions, keys and feedback. Contradictions remain
visible in review. See REQUIREMENTS.md for the complete requirements.

Continue automatically in source order through grades7–11, in reviewed batches
of5–10 lessons. Validate, test, import to isolated local staging, record a precise
checkpoint, commit/push the feature branch and proceed. Routine continuation does
not need approval. Preserve completed work and original §1; do not regenerate it.

## Branches and source map

Backend/Flutter use separate `feat/chemistry-curriculum` worktrees from stable
Biology `c0f84d0` and polished UI `444743b`. Physics `07f748b`/`cf01011` were read
only; its unfinished FRQ is not production functionality. Original other-subject
branches,406 Biology lessons and real user data remain intact.

The five books have81/208/208/160/160 PDF pages,817 total. The map has29 chapters,
204 paragraphs,49 laboratories,15 practicals:268 teaching entries and327 total
anchors. Grade7 spreads preserve left/right; grades10/11 scans require image
review. Mapping is not interactive readiness.

## Current implementation

26 reviewed lessons through grade7 §22, including practical1–4;242 remain. All
whole-course flags remain false. §2 is substance properties, practical1 is safety.
The previous safety label for §2 was a handoff error.

MCQ, bounded short text, exact fixed-unit numeric input, formula notation and
finite equation balance share ILM AI v2 ordered attempts, private server rubrics,
immutable snapshots, replay, expiry, source feedback and once-only XP. Read
ASSESSMENT_CONTRACT.md for actual syntax/limits; charge/structural/general-unit
engines are not silently supported. Flutter uses common Ilmo/source/feedback/
result/exit components and a separate explicit local preview entrypoint.

Exact implementation commits/tests/next page: CHECKPOINT.md and QA_REPORT.md.
Next paragraph is grade7 §23, printed69–70, then §24–26, chapterIII review
anchors and §27. ChapterI/II reviews are integrated with actual source identities;
do not double-count or mislabel them.

## Review and development notes

- Grade9 §40/186 has a machine-enforced scientific hold; no silent approval.
- Grade7 §13/41 has differing prose/table CO/CO₂ percentages. The catalogue pins
  a scoped editorial issue, and the validator forbids those numbers as answer
  keys. Unambiguous law, water/peroxide and integer-ratio material is separately
  cited. Do not replace the conflicting data from memory.
- Official2026-linked programmes differ by stream/structure; see
  CURRICULUM_ALIGNMENT_2026.md. Chapter correspondence is not full outcome or
  current-school-curriculum certification. No external programme knowledge is
  added to lessons.
- A PowerShell ASCII pipe damaged eight apostrophes in four development lesson
  files; UTF-8 repair and renewed review hashes restore typography only. Facts,
  correct answers and learning rules did not change. Existing imported rows are
  never overwritten. Use a fresh synthetic QA sandbox for corrected manifests;
  old QA snapshots/data remain separate. Original §1 bytes stay unchanged.
- Use UTF-8 files/apply_patch for Uzbek text; do not pipe Unicode through default
  Windows PowerShell OutputEncoding. The validator rejects corrupted lesson copy.

PDF/OCR/page images and tokens remain private. No production DB/deploy/main merge,
other-subject branch edit, AI Tutor/Explain or physical hazardous activity is
authorized. Native phone/IME/TalkBack and independent teacher sign-off are not
claimed by widget/source-image tests.


## Batch05 provenance and readiness

Prior-topic context is explicit, earlier in the same book and page validated.
Chapter-review anchors attach only to their preceding teaching section. Source
buttons retain their real paragraph/review/practical labels; default Biology
source behavior is unchanged. Source issues prevent complete-course readiness.
Grade7 §18 ozone thickness interpretation, resin-formation context and old
exposure figure remain withheld under ch7-p18-ozone-context-review. Do not
convert the 2–4.5mm statement into geometric stratospheric thickness or teach
the edition's 10^-5% figure as a current exposure guideline.


## Batch06 source boundaries

§19 silane equation on59 is atom-unbalanced and withheld; do not repair from
memory. §20 oxygen-routing prose/star labels on60 need contextual review; the
balanced overall unlabeled photosynthesis equation is taught separately. These
issues are pinned, not resolved. Dry-air percentages and reserve figures are
explicit edition data, not present-day observations. Practical4 is guided
digital analysis; absent limewater outcomes are not invented. §22 is Vodorod,
not a heat topic. Isotope table recognition uses MCQ/text, not unsupported syntax.
