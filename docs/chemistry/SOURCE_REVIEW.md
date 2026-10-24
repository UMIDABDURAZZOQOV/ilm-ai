# Chemistry source review

2026-10-24. All five files were found in the user's original
`Desktop/Kimyo Uzb-Rus` folder and copied unchanged to the requested private
`Projects/ilm-ai-chemistry-sources` directory. That directory was absent when work
began; its local `.gitignore` ignores everything. No PDF was added to this repo.

## Bibliography checked against page images

| Grade | Verified edition | Authors | Publisher | ISBN | PDF pages / bibliographic pages |
| --- | --- | --- | --- | --- | --- |
| 7 | Kimyo, revised fifth edition, 2017 | I.R. Asqarov, N.X. To‘xtaboyev, K.G‘. G‘opirov | Sharq | 978-9943-26-621-6 | 81 / 160 |
| 8 | Kimyo 8, revised fourth edition, 2019 | I.R. Asqarov, K. G‘opirov, N.X. To‘xtaboyev | Yangiyul Poligraph Service | 978-9943-361-08-9 | 208 / 208 |
| 9 | Kimyo 9, revised fourth edition, 2019 | I.R. Asqarov, K.G‘. G‘opirov, N.X. To‘xtaboyev | O‘zbekiston NMIU | 978-9943-07-261-9 | 208 / 208 |
| 10 | Organik kimyo, first edition, 2017 | A. Mutalibov, E. Murodov, S. Masharipov, H. Islomova | G‘afur G‘ulom nomidagi nashriyot-matbaa ijodiy uyi | 978-9943-5009-4-5 | 160 / 160 |
| 11 | Umumiy kimyo, first edition, 2018 | S. Masharipov, A. Mutalibov, E. Murodov, H. Islomova | Same publisher as grade 10 | 978-9943-5291-6-8 | 160 / 160 |

Title/verso pages PDF1–2, contents and relevant colophon credits were checked.
The 8/9 colophons also credit MITTI YULDUZ for layout/preparation; this is recorded
beside the title-page publisher rather than silently choosing a different edition.
The title pages state ministry approval (grade 8: recommendation). These statements
establish the supplied editions' school scope. **Alignment with a separate current
2026 syllabus is not verified: no such syllabus was provided.** No outside
subject knowledge or alternative textbook was used to fill gaps.

Exact SHA-256s are pinned in `chemistry_sources.json`, the validator and every
record. The five grade maps also display them in full.

## Layout, extraction and completeness of this audit

- Every **817 PDF pages** decoded successfully with PDFium, and counts were checked
  with pypdf. Successful decoding is not proof every scientific statement is true.
- Grade 7 has embedded text on 80 PDF pages; PDF81 contains a rental form image.
  PDF1 is a centred single title page. PDF2–80 contain printed2–159 as spreads:
  printed even -> left, odd -> right; PDF = floor(printed/2)+1. PDF81 is the
  unnumbered single rental form corresponding to the bibliographic final page.
  No visible printed numeral is invented for title/rental pages. Teaching citations
  retain PDF page and left/right region. Splitting the title into two pages is wrong.
- Grades 8/9 have embedded text on all 208 pages. Fonts sometimes extract `Òemir`
  or `elåmånt`; title images establish the correct glyphs. Chemistry notation and
  answer keys are never repaired by a blind text replacement.
- Grades 10/11 have **zero text-layer pages**. All **320 scan pages** were rendered
  at 1700px and processed locally with Windows OCR en-US. OCR is a locator only.
  All 68 paragraph headings, their chapter headings, prefaces and grade-10 lab
  headings were checked against original body images. Clipped/incorrect fuzzy
  crops (grade10 chapterII; grade11 §7/chapterII) were replaced by full-page review.
- Contents images: grade7 PDF79–80; grades8/9 PDF205–206; grades10/11 PDF157–158.
  Embedded body heading matching supplements the image-reviewed contents for
  grades7–9. The 105 uncertain/scanned heading crops were reviewed locally.
- Laboratories/practicals were found in the **body**, not merely the aggregated
  contents pointer. Counts are 16/7, 10/5, 17/3, 6/0, 0/0 respectively. Grade11 has
  no separately labelled laboratory/practical section in this supplied book;
  numerical exercise paragraphs remain paragraphs, not invented laboratories.
- Shared boundary pages are explicitly marked. A paragraph may begin partway down
  a page; a whole-page citation does not approve all facts for both neighbours.
  Every authored fact needs its own paragraph and reviewed page/region evidence.

## Confirmed catalogue discrepancies

| Grade / record | Contents pointer | Actual body start | Resolution |
| --- | --- | --- | --- |
| 8 §6 | 30 | 31 | Both retained |
| 8 §7 | 32 | 34 | Both retained |
| 8 §8 | 36 | 37 | Both retained |
| 8 §9 | 39 | 41 | Both retained |
| 8 §10 | 42 | 44 | Both retained |
| 8 §11 | 46 | 48 | Both retained |
| 8 §12 | 49 | 51 | Both retained |
| 8 §13 | 51 | 53 | Both retained |
| 7 §25 | Adds “Ishlatilishi” | Heading at72 omits that word | Contents/body wording stored separately |

Grade7 practical5 contains a second named soil activity (printed94); it is a
child anchor, not an eighth practical. Grade10 lab5 also contains a starch/iodine
activity on156, retained as a child rather than a seventh laboratory.

## Scientific review queue

This is not a complete expert review of every formula/fact in all five books.
Only individually reviewed claims may be authored. At least this internal
contradiction was found while checking headings:

- **Grade9 §40, PDF/printed186:** the worked example's given outer configurations
  include `3s²3p⁵`, while the following prose says all examples are groupII and later
  shortens the chlorine configuration to `3s²`; the displayed full configuration
  retains `3p⁵`. Do not import that worked answer as a verified rule. Preserve the
  source and require scientific review before that lesson is authored.

This issue is also an open, machine-readable source hold on `ch9-paragraph40`.
The validator rejects a lesson for that topic and refuses deletion of the known
hold. Explicit source-backed resolution and validation changes are required;
an image-reviewed page alone cannot silently approve contradictory content.

No missing page or uncertain OCR is replaced by a model-generated fact. No expert
teacher sign-off, current-syllabus approval or complete scientific inventory is claimed.

## First authored source review

Grade7 §1 was read from all original images for printed3–8: PDF2:right,
PDF3:left/right, PDF4:left/right and PDF5:left. PDF3–5 were re-rendered at2200px
for readable review. Each page/region and render SHA is recorded in
`grade7_paragraph01_review.json`; the explicit lesson index pins the UTF-8/LF
manifest digest. The earlier heading render hash for `ch7-scientists` was updated
to the reviewed higher-resolution image, without changing the source PDF hash.
The reviewed adaptation is original prose, not textbook OCR pasted as lessons.
Biographical claims are scoped to the supplied2017 edition; no current-status,
clinical, unverified historical-priority or physical-experiment claim was added.


## Batch02 image review (2026-10-24)

Grade7 printed9-20 was inspected from original PDF5:right through PDF11:left.
The five new evidence files pin every cited region and rendered image SHA.
Paragraph boundaries are respected: practical1 begins mid printed10; practical2
begins mid12; paragraph3 begins mid15; paragraph4 begins on19; paragraph5 begins
mid20 and is excluded from this batch's §4 claims.

- Practical1, printed11-12: the book contains mercury spill and sodium disposal
  procedures, acid dilution/transfer and explosive-mixture cautions. These are
  retained as review flags in evidence; no learner cleanup, disposal, dilution,
  ignition or hazardous physical execution is prescribed. Safety scenarios use
  recognition, recorded observations and notebook structure only.
- Practical2, printed13-14: asbestos mesh is a historical equipment label in this
  edition, explicitly flagged for qualified laboratory-safety review. The digital
  lesson does not recommend obtaining or using it. Fuel filling, wick preparation,
  lighting and heating sequences are not interactive execution tasks.
- §3 printed16's introductory molecule generalisation is scoped to molecular
  examples. The same book's printed21-22 distinguishes nonmolecular substances;
  the lesson does not claim all substances contain molecules. Historical atomos
  wording is separated from the taught electron/proton/neutron structure.
- §4 printed19: Å/nm exponents, kg exponents, carbon-12 fraction, rounded mass
  unit and oxygen ratio visually verified. The original 3.32/1.66 worked exercise
  follows the printed rule and is labelled a hypothetical arithmetic example,
  not an unverified element measurement. Numeric comparisons use exact Decimal
  values; no formula evaluation, fuzzy grading or silent unit conversion.

These safety adaptations do not resolve the open grade9 §40 scientific hold.
Independent subject-teacher and real laboratory certification remain unclaimed.


## Batch03 image review (2026-10-24)

Printed20-29, PDF11:left through PDF15:right, individually inspected. Each new
lesson has its own page/region image hashes and fact/answer citations. §8 stops
on29; §9 begins on30. Practical3 stops before §7 starts midway on26.
Molecular/nonmolecular distinctions are explicit, and a homogeneous mixture is
not classified as pure simply because it is clear. Practical3 uses only the
printed flow diagram, recorded quantities/results and report structure.
The2017 edition's element-distribution/count anecdotes are scoped as that book's
description. The table's gas density values are not taught as universal20°C data.
§8 retains101.3kPa water phase conditions and avoids exact0/100°C boundary cases.
Sublimation/combustion and phosphorus examples are descriptions, never handling
or execution assignments. MCQ distractors use already taught nearby concepts.


## Batch04 image review (2026-10-24)

Grade7 printed30–41, PDF16:left through PDF21:right, individually reviewed.
§9 stops before §10 on33; §10's two final exercises precede §11 on35; §12's
final exercises precede §13 on40; §13 stops before §14 on42. All formula
subscripts, coefficient counts, powers, units and given mass values were read
from original page images. Original examples use these rules/data, not external
constants. The old carbon12-based mol definition and rounded6.02e23 value are
identified as the edition's convention. Mr numerical equality with molar mass
is scoped to g/mol, consistent with the printed34 table's kg/mol alternatives.

### Scoped editorial review: grade7 §13, printed41/PDF21:right

Prose CO percentages42.88/57.12 differ from table42.86/57.14; prose CO₂
27.29/72.71 differs from table27.27/72.73. This is now a pinned
`editorial_review_issues` record, separate from the blocking grade9 hold. The
validator refuses deletion of the issue and refuses those disputed percentages
as verified answers. No value was silently corrected from memory. The lesson
uses the unambiguous water/peroxide values on40 and integer-ratio conclusion
on41; it does not grade the disputed percentage values.

### Development text integrity

A Windows default ASCII pipe replaced eight apostrophes in four prior development
files (practical2, §6, practical3, §8). The original spelling was restored with a
UTF-8 file, evidence manifests re-reviewed and hashes updated. No fact, correct
answer or learning policy changed; §1 bytes remain unchanged. The validator now
rejects replacement characters and question marks embedded in words. Old local
QA imports remain immutable, and corrected content is loaded into a fresh
synthetic sandbox. No real user data or old attempt snapshots were rewritten.
