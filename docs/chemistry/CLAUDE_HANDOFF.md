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

36 reviewed lessons through grade7 §32, including practical1–4;232 remain. All
whole-course flags remain false. §2 is substance properties, practical1 is safety.
The previous safety label for §2 was a handoff error.

MCQ, bounded short text, exact fixed-unit numeric input, formula notation and
finite equation balance share ILM AI v2 ordered attempts, private server rubrics,
immutable snapshots, replay, expiry, source feedback and once-only XP. Read
ASSESSMENT_CONTRACT.md for actual syntax/limits; charge/structural/general-unit
engines are not silently supported. Flutter uses common Ilmo/source/feedback/
result/exit components and a separate explicit local preview entrypoint.

Exact implementation commits/tests/next page: CHECKPOINT.md and QA_REPORT.md.
Next teaching entry is grade7 practical5,printed93–95,then chapterIV reviews
95–99 and §33–36. Five earlier chapter-review anchors are integrated with actual
source identities; do not double-count or mislabel them.

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


## Batch07 conditions and UI source feedback

Kipp/acid/metal/halogen/oxygen examples are digital recognition and material
equations only. No physical gas generation, tasting, ignition or apparatus steps.
Unreconciled heat signs on72, universal clean-fuel scope on73, phase context in
review77 and absolute dry-gas claims on82 remain held. Future §28 ocean-volume
numbers on83 conflict and are already pinned for review. Source image details
are in SOURCE_REVIEW.md. No model-memory correction is authorized.

Chemistry feedback now supplies the existing exact source widget to an optional
slot in the common scrollable panel; other callers keep their prior behavior.
Water fixtures are actual sanitized API payloads. At320px/200% text both theory
and hydrate MCQ feedback expose the correct printed/PDF side. Hydrate input is
recognition, not a newly claimed parser feature. One water prompt was shortened
without changing science/key and uses a fresh synthetic final sandbox.


## Batch08 units and source review

Massa ulushi uses whole solution mass; eruvchanlik uses solvent mass. CM=n/V
requires litre solution volume; mass-based CM=m×1000/(M×V) requires V in ml,
m in g and M in g/mol. NaOH40g/mol is explicitly prior§10/34 context,not a
fabricated constant. Only digital calculations,not physical solution preparation.
Source85 municipal sequence is recognition,not home disinfection or a potable
water assurance. Dated WHO/2050 statements are not approved current statistics.
Source86 high-resolution review confirmed375000000km²; no false discrepancy
was added. Source87 graph g/l axis is not silently read as g/100g solvent.
Existing nine scoped issues remain open; ocean-volume keys are now guarded.
