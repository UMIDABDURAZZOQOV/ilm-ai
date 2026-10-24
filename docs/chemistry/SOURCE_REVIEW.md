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


## Batch05 original image review (2026-10-24)

Grade7 §14–18, printed42–58/PDF22–30, reviewed against original spreads,
including chapterI problem/test anchors47–54. §16 integrates both review anchors
under their actual identities. Prior §12/40 carbonate products, §10/34 CO2 molar
mass and §15/43 gas-volume rule remain explicitly linked to those earlier topics.
All five oxygen-preparation equations and atomic [O] notation were checked;
these are symbolic tasks, never physical preparation instructions. The density
table1.429 and later1.428 g/l text are not universal precision answer keys.

### Scoped ozone-context issue: §18, printed57–58

The 2–4.5mm layer statement lacks reduction/interpretation conditions; resin
oxidation formation wording lacks reaction context; the old 10^-5% exposure
figure is not approved current exposure guidance. These three claims are
withheld from teaching/graded answers, not replaced from model memory. A pinned
editorial issue and answer guards preserve the review. Unambiguous allotropy,
formula, preparation equations and protective atmosphere role remain separately
sourced. No claim that every ozone clause is resolved or teacher-certified.

Readiness now checks open source-review issues as well as missing lesson IDs.
There is one blocking scientific hold and two scoped editorial issues. All
whole-course ready flags remain false.


## Batch06 image review — 2026-10-24

Original spreads30–35/printed58–69 read. §19 uses only58–59; §20 starts on60.
§21 starts halfway down62 and ends before practical4 on64. Practical4 uses64–65
with chapterII review66 explicitly linked. §22 uses67–68; acids begin on69.
The printed Yonilg‘ilarning heading on62 corrected a misplaced apostrophe in the
catalogue transcription; topic identity, source order/count are unchanged.

- **ch7-p19-silane-equation-review**,59/PDF30:right: printed
  SiH4+2O2=SiO2+H2O has4 hydrogen atoms left and2 right. It is withheld, including
  an unapproved silent repaired answer. Other individually balanced reactions
  are taught. No oxygen-cylinder operation or physical burning instructions.
- **ch7-p20-photosynthesis-label-review**,60/PDF31:left: printed6H2O* and6O2*
  labels mark different oxygen counts, and nearby routing/half-biomass prose
  requires context. Isotope origin is withheld; only the balanced overall
  unlabeled equation and its reverse are used. No mechanistic correction from
  memory is supplied.
- Air table values are identified as this2017 edition's sea-level dry-air data;
  historical reserve/geographic statements are not certified current statistics.
- Practical4's limewater instruction asks for an observation without stating an
  outcome there. No result is fabricated. Digital work uses supplied gas identity,
  earlier verified equations, report structure and original stoichiometric tasks.
- §22 isotope table and edition-specific detailed masses are separate from
  roundedH=1/O=16 arithmetic. The H2O2 mass-fraction example cites prior §10/33
  and §13/40 as well as the current paragraph; no disputed §13/41 numbers used.

Open issues now total one blocking scientific hold and four scoped editorial
issues. File coverage alone cannot make a whole course ready. The lessons are
source-image reviewed, not independently teacher-certified.


## Batch07 image review — 2026-10-24

Printed69–83/PDF35–42 reviewed in original images; earlier source47,55 reread for
heat convention and oxygen mass. §23 ends before §24 on70; §24 before §25 on72;
§25 before §26 on73; §26 main content ends on74. ChapterIII problems75–78 and
tests78–79 retain ch7-4/ch7-5 identities. §27 uses80–82, before §28 on83.

- **ch7-p24-heat-sign-review**,72: printed206/40kJ terms have unreconciled
  heat-direction and condition conventions. Material equations alone are taught;
  no silent sign swap or approved heat key. Earlier §16/47 convention is retained.
- **ch7-p26-environmental-scope-review**,73: the broad no-pollution statement
  lacks lifecycle/all-condition scope. Teaching states the actual H2/O2 equation
  produces water; no general environmental absence is inferred.
- **ch7-review3-gas-phase-context**,77: room-temperature sulfur-vapour and actual
  normal-state HF density premises lack phase boundaries. Neither S8 nor0.89g/l
  from those examples is an answer. The75 density rules are separately taught
  with original O2/H2S/Zn/FeO/KClO3 calculations from explicit source data.
- **ch7-p27-water-condition-review**,82: dry-gas/catalysis statements omit needed
  reaction-condition context. Absolute no-reaction-without-water claims are
  withheld. Other water structure,states,density and balanced material equations
  are separately linked. Hydrate dot/association notation is recognition only.
- **ch7-p28-ocean-volume-discrepancy**,83, identified for the next topic: the
  page gives1.35·10^6km³ and approximately1.4billionkm³. Neither is silently
  approved as the correct ocean volume. No replacement exponent is invented.

No current prices,spoon mass or clinical breathing-rate data fill underspecified
review78 exercises. No acid tasting,gas collection setup,ignition,metal/water or
halogen experiment is assigned. Indicator colors follow the exact69 caption.
Water uses source80 angle104.3° and source81 constants as edition data. Source
page55, not54, explicitly supports the rounded O2 molecular mass32 used in the
new density example. One water MCQ prompt was shortened for small screens;
facts/options/keys unchanged and SHA evidence renewed before final fresh QA.

Open review: one blocking scientific hold plus nine scoped editorial issues.
Five chapter-review anchors integrated; source mapping is not independent
teacher certification or complete interactive-course readiness.


## Batch08 image review — 2026-10-24

Original printed83–92/PDF42–47 read. §28 ends before §29 on84; §29 before§30
on85; §30 before§31 on88; §31 before§32 on90; practical5 starts on93,which is
not cited as §32 content. Prior§10/34 table was visually reread:NaOH40g/mol is
the explicit molar-mass datum used by the new CM example. No invented NaCl mass.

- Held ocean volumes on83 remain withheld; canonical numeric variants cannot
  enter verified answers. Source distribution/physical-role facts are separate.
- Higher-resolution PDF44 image confirms the86 numeral **375000000km²**,not
  37500000. The provisional digit concern was resolved from the original; no
  erroneous source hold or replacement numeral was introduced. The earlier3/4
  statement is approximate,not an exact equality with the area pair.
- Source87 prose uses g/100g solvent; figure35 says g/l. Only prose/worked
  numeric givens are graded. No curve value was guessed from pixels or treated
  as a directly interchangeable unit. Boundary equality at10/0.01 is not inferred.
- Original solubility examples preserve denominator:250g solution−60g salt=
  190g solvent;60/190×100≈31.6g/100g water,one decimal. BaCl2 ratio uses the
  printed40°C/50g-per100g-water datum in a digital75g/150g variant only.
- Mass fraction denominator is whole solution; concentration volume is whole
  solution. CM=n/V(l)=m(g)×1000/[M(g/mol)×V(ml)]. Given density models are
  hypothetical arithmetic conditions,not fabricated measured solution densities.
- Municipal coagulation/filter/chlorination is recognition only. No doses,
  domestic procedure,potable-water certification,clinical dehydration threshold
  or medicinal/mineral-water cure instruction. Dated statistics/forecasts are
  edition attributions,not independently verified current facts or answer keys.

Open review remains one scientific blocker plus nine scoped editorial issues.
All source-only,immutable-import and no-production rules remain in force.


## Batch09 image review — 2026-10-24

Original93–106/PDF47–54 reviewed; practical5 uses93–94,review anchors95–98,
§33 uses99–101,§34 uses102–104 before§35,§35 uses104–105 before§36,§36 uses
105–106. §37 starts on107,not cited as§36 teaching. Prior§7/26 and§9/32 retain
their exact source identities. Each displayed material equation atom-checked.

- Practical5 retains both components:mass fraction,label/report and soil aqueous
  extract/filtrate/litmus interpretation. No reagent amounts/setup,physical
  execution,agricultural treatment or inferred unprovided observations.
- **ch7-practical5-universal-colour-review**,94:the universal-indicator yellow/
  pink alkaline-soil inference lacks formulation/chart context. No corrected
  colour is invented. The separately printed litmus violet→blue observation is
  used as supplied digital evidence.
- **ch7-review4-water-vapour-state**,98:hot vapour volume lacks definite pressure/
  temperature. Normal-state22.4l is not silently substituted. The independently
  specified4°C liquid-density part is taught with prior§27/81 instead.
- **ch7-p33-francium-state-review**,100:Fr exception in the normal-condition
  phase table is held pending corroborating source/condition context. No melting
  point or corrected state is invented; other named examples/general trends
  remain separately taught.
- **ch7-p34-iron-percentage-precision**,104:72.2/27.8 Fe/O exercise gives no
  tolerance/precision boundary. Earlier Fe56/42 and O16/55 would give Fe3O4
  approximately72.41/27.59. Printed values are withheld as an exact premise;
  neither numbers nor formula are silently repaired. Other explicit formulas
  are separately available. Validator rejects the held percentage premise.
- Source99's backward reference says26/§9,but original simple/compound topic
  is§7 on26;§9/formulas begins30. This pointer is resolved from original pages
  and cited accurately,without altering the scientific rule.
- ChapterIV arithmetic variants use exact source rules/data:CaCl2 M111g/mol on96;
 20g/(40g/mol×2.5l)=0.2mol/l;100g10%+150g20% gives16%. No invented atomic mass.
  Graphic oxide lines retain source§9's valence representation;formal structural
  input/automatic bond inference is not introduced.

Open review now one scientific blocker plus13 scoped editorial issues. Seven
chapter-review anchors integrated; source mapping is not full-course readiness
or independent teacher certification. Existing source-only rules remain in force.


## Batch10 image review — 2026-10-24

§37:107–108;§38:109;§39:110;§40:111–112;§41:113–114 before§42 heading.
PDF54–58 left/right images retain hashes. Earlier§20/60 is an explicit source
context for the overall photosynthesis statement;no isotope routing added.

- **ch7-p37-occurrence-mineral-review**:fixed/current0.03%CO2 conflicts with
  same-book§20/61 variable wording;the unqualified NO2 absence claim lacks scope.
  Neither becomes an answer. Grade7/108 quartz gemstone list conflicts with
  supplied grade9§27/130–131 corundum/Al2O3 list. Both disputed assignments held.
- **ch9-p27-gem-and-equation-review**:same cross-book host conflict;on130 the
  printed Al(OH)3+2KOH=KAlO2+2H2O has K2/H5 left and K1/H4 right. No coefficient
  repair is inserted as a verified key. Grade9 content is still unauthored.
- Original107 ocean-area numeral was rechecked in a supplemental high-resolution
  original rendering:375000000km². No guessed digit or new discrepancy was added.
- All displayed base reaction examples atom-checked. Partial products remain
  Mg(OH)Cl,CaHPO4 and Cu(OH)Cl. No unique-neutral-salt inference is imposed on
  the8gNaOH/19gH2SO4 exercise. Existing plain-equation grammar remains explicit.
- Ca(OH)2 sparse solubility on113 is distinct from insoluble-example list110.
  No universal not-NaOH/KOH→insoluble rule. NH4OH notation is the book convention,
  not an isolated-crystal claim;metal–O–H graphics are not universal bond claims.
- Indicator111 is a specific printed table,not resolution of the held universal
  soil-indicator issue94. No physical caustic handling,clinical recommendation,
  pesticide use or invented electrolysis equation in the interactive lessons.

One scientific blocker and15 scoped editorial issues remain open. The holds gate
readiness while separately verified material can continue in book order.


## Batch11 original acid pages — 2026-10-24

Grade7 originals114–124/PDF58–63 read,with exact boundaries:§42 uses114–116
before43;§43 uses116–117 before44;§44 uses117–120;practical6 uses121;§45 uses
122–124. Prior worked50 retains ch7-1 review identity. Grade8 original23 was
visually compared for notation only;its science is not silently inserted in7.

- **ch7-p42-acid-notation-valence-review**:HJ/-J115 differs from supplied
  grade8§4/23 HI/I2. No legacy-symbol FRQ or hidden replacement. H3PO3/=PO3
  has3 written H versus2 valence lines,so blanket114 equality is not approved
  for all rows. Formula/name is separately recognised. Keyword-only116 bromat,
  atsetat,oksalat have no formula/definition in115;no missing content invented.
- **ch7-p43-basicity-scope-review**:total-written-H rule is not promoted to
  universal ionisable-H equivalence. H3BO3 three-basic assignment117 lacks a
  reviewed operational explanation here;held without inventing an alternative.
  Other individually reviewed examples and oxygen classification are separate.
- **ch7-p44-product-scope-review**:196gCu(OH)2/73gHCl exercise120 is not an
  unqualified neutral-salt mass key.119 includes partial Mg(OH)Cl/KH2PO4;112
  includes Cu(OH)Cl. Zn/H2SO4→H2 versus Cu/concentratedHNO3→NO2 retains
  conditions rather than a universal metal/acid prediction. Material equations
  atom-checked;phase annotations remain recognition,not unsupported input.
- **ch7-p45-condition-scope-review**:unspecified density/gas-drying scope and
  broad metal-reactivity/storage wording122–124 are held as universal keys or
  procedures. Cold-concentrated passivation is explicitly scoped. No corrosive
  dilution,drying,metal-storage,medical or explosives synthesis task.
- Practical6 retains both named oxides,filtration/crystal goal and reporting.
  No unprovided colour,iron product formula or actual experiment. Its copper
  equation/data are explicitly printed in earlier ch7-1/50;virtual4g variant
  uses80:98:160:18 to obtain4.9/8/0.9g. Earlier review context is not relabelled
  as practical121 or reintegrated as a new chapter activity.

One scientific blocker and19 editorial reviews remain open. Source-image review
and passing software tests are not independent teacher/scientific certification.


## Batch12 original salt/equivalent pages — 2026-10-24

Original125–140/PDF63–71 read. §46 uses125–127 before47;§47 uses127–129 before48;
§48 uses129–132;§49 uses133–134 and chapterV review135–136 before50;§50 uses
136–140. Earlier chapterIV worked96 keeps its own review identity and evidence.

- **ch7-p46-legacy-iodide-review**:KJ125 is unresolved legacy iodine notation,
  not a hidden KI substitution. Other source formulas/names are separately used.
- **ch7-p48-copper-iodide-review**:130 prints CuCl2+2NaOH=(OH)2+2NaCl,missing Cu
  on the right. Neither this unbalanced line nor a silently repaired copper-
  hydroxide line becomes a key. Complete Mg full/partial equations131 are
  separately taught. KJ/J2 on130 and NaJ/AgJ132 remain held legacy species.
- **ch7-p49-medical-current-scope-review**:5.5% body-salt/self-treatment claims,
  1l0.9% mass without density and broad/current industrial statements are not
  clinical advice or exact keys. Mining examples are explicitly2017-attributed;
  no inferred2026 operating sites/processes or home saline preparation.
- **ch7-p50-gas-precision-context-review**:140 calls sulfur(IV) oxide CO2 in a
  sulfur-burning exercise;earlier58 gives S+O2=SO2. The faulty exercise/fumigation
  doses stay held,not repaired or parameterised. 98/3 is printed32.66 without a
  precision rule;no32.66 or silent32.67 expected key. Gas-equivalent volumes lack
  definite T/P here. Unit/reaction/binding context prevents universal E claims.
  Written-H/basicity is not generalised to the unresolved phosphite/boric cases.
- School equivalent calculations use explicit source models:Al27/3=9,CuO80/2=40,
  Cu(OH)2 98/2=49,CuCl2 135/2=67.5. g questions explicitly mean mass of one
  equivalent amount in that model;no new unit-conversion engine or gas-state
  assumption. Carbon CO/CO2 example137 is separate from the sulfur typo140.
- ChapterV review is integrated only into last preceding§49,not§50. Virtual4g
  NaOH full-neutralisation model uses prior40g/mol and1:2 ratio,not ambiguous
  partial-neutralisation products. All complete typed material equations checked
  for atom balance;phase glyphs are not promised as supported input.
- Hydrate/complex/double-salt forms are source recognition only. Salt graphics
  are valence representations;no universal covalent-molecule claim. No reagent,
  mercury/chlorine exposure,heating,pest-control,clinical or physical task.

One scientific blocker and23 editorial reviews remain open;all course-ready
flags false. This is source-image review,not independent teacher certification.


## Batch13 original genetic/practical/lab pages — 2026-10-24

Original141–155/PDF71–78 now visually read. Current batch uses§51 141–143 before
practical7;practical7 143–144 plus chapterVI review145–146;lab1 147–148 before2;
lab2 148–149 before3;lab3 149 before lab4 on150. No facts are taken from a later
heading merely because the printed/PDF page is shared.

- **ch7-practical7-clinical-source-scope**:the clinical Regidron recipe144 is
  not a treatment/preparation/dose task. Unknown black-powder inquiry143 has no
  supplied purity result;appearance alone is insufficient evidence. Digital
  mass-fraction variants are separate explicitly virtual non-clinical models.
- **ch7-review6-product-loss-scope**:146 CO2-volume question does not specify
  carbonate/bicarbonate,while130 gives both ratios. No unqualified volume key.
  Copper-loop options overlap without loss conditions;original question is not
  copied as a uniquely keyed MCQ. Our virtual model explicitly says no loss.
- §51 diagram arrows are class relationships with conditions,not an unrestricted
  reaction engine. Every typed printed equation atom-checked;no physical HgO
  heating,gas preparation or chemical handling assigned.
- Practical7 retains all5 inquiry components. Virtual indicator rows cite actual
 111/118;CuCl2→Cu(OH)2 solution is original atom-balanced reasoning for the144
  target chain using earlier135 salt/alkali method and112 formulas. It is not
  quoted as a printed130 equation or a resolution of the missing-Cu typo.
- Virtual arithmetic144:80g10%→8g;20gsolute+80gwater→80%solvent;500g20%+300gwater
  →12.5%;400g5%+50gsolute→70/450×100≈15.6% to one decimal. Ideal no-loss Cu loop
  retains12.8g. None is an actual observation,clinical or agricultural procedure.
- Lab1 table147 is blank. Only property columns/classification are taught;no
  invented densities,colours or measured sample values. Lab2 phase/dissolution/
  odour components remain recognition,no melting/flames/inhalation. Lab3 keeps
  burning,copper and carbonate inquiry;prior35 supplies chemical-change rule
  and143 names the CuO candidate. No fabricated purity/gas/colour result.

One scientific blocker and25 editorial reviews remain open. Digital lab entries
do not certify physical execution or independent subject-teacher approval.


## Batch14 source review — laboratories4–11

Exact shared-page segments:lab4 on150 before5;lab5 on150–151 before6;lab6/7
on151 between their own headings;lab8 on151–152 before9;lab9 on152 before10;
lab10 on152–153 before11;lab11 on153 before12. Original images were visually
read;earlier source contexts retain actual title/paragraph/page/region/hash.

- Lab4 uses prior§7/26 and§33/100 classification examples. No arbitrary specimen
  physical properties. Lab5 retains lime/water,green malachite and Fe/CuCl2;
  complete prior111/106 equations and original atom-balanced FeCl2/Cu model
  derive from stated reactants plus earlier46/142 rule/formulas. No invented
  actual metal deposition,gas/flame or colour observation.
- Lab6 sample table151 and lab7 fuel-property values are blank. Earlier oxide
  formulas102–103 and named fuel groups63 are separately cited;no density,
  colour,odour,hardness,efficiency or heating-value measurement invented.
- Lab8:Zn+2HCl=ZnCl2+H2 uses exact earlier70. Lab9:CuO+H2=Cu+H2O uses exact73.
  Original virtual0.25/0.3mol questions use1:1 coefficients,not actual gas
  measurements,collection,ignition,heating or apparatus steps.
- Lab10 keeps CaO/P2O5/water/indicator and CuO/water inquiry separately. Exact
  prior111/117 equations and111/118 tables support positive examples;review135
  supplies salt/alkali CuOH2 route. No unqualified all-oxide/water prediction.
- Lab11 stated reactants153 support original full-neutralisation balancing
  models with products explicitly given:CuOH2/H2SO4→CuSO4/H2O and FeOH3/HCl→
  FeCl3/H2O. Actual earlier50/111/119 formulas/rule are cited. Completed
  equations are original solutions,not misquoted as printed equations153.
  No unprovided crystal/hydrate/initial-colour result or physical evaporation.

One scientific blocker and25 editorial reviews remain open. All new content is
guided digital analysis;software/source-image review is not physical-lab or
independent teacher certification.


## Batch15 source review — laboratories12–16

Original154–155 read:lab12 before13 on154;lab13 before14 on154;lab14 spans
154–155 before15;lab15 before16 on155;lab16 on155. Each cited earlier source
retains actual title/paragraph/printed/PDF page/region/book and image hashes.

- Lab12 exact decomposition112;no fabricated initial CuOH2 colour or experiment.
- Lab13 source-specific pink→colourless;no inference endpoint=pH7. Original
  numeric model explicitly assumes complete1:1 neutralisation,not measurement.
- Lab14 both acids and both indicators;exact118 table rows,not universal pH.
- Lab15 concentration/heating and ready-made observations unspecified. New
  ch7-lab15-acid-condition-scope holds universal Cu/H2SO4 keys. Zn models use
  exact70/119;Fe model explicitly gives FeCl2/H2 with earlier142/119 evidence.
- Lab16 both Fe(III)-oxide/MgO and HCl/H2SO4 retained. Products-given original
  full-neutralisation models use earlier102–103/111/115/119/127. Completed
  equations are original derived solutions,not claimed printed equations155.
  No crystal colour/shape/hydrate,heating/evaporation or actual lab result.

All74 grade7 teaching entries covered;one scientific blocker and26 scoped
editorial issues across the supplied catalog remain. Coverage is not independent
teacher certification or whole-course publication approval;ready flags false.


## Batch16 source review — grade8 §1–5

Original5–31 images fully read,not inferred from extraction. §1 begins5 and
continues through the exercises before§2 on10;§2 ends16 before§3 on17;§3
includes the exercise at top21 before§4;§4 ends24 before§5 on25;§5 ends in31
before§6. Exact full-page identities and hashes accompany all facts/keys.

- §1:the first mol bullet7 describes grams,unlike following definition and9
  N=m/M models. Ambiguous identity held;explicit amount/mass/molar mass units
  preserved. FeSO4·7H2O10 is recognition,not new typed hydrate syntax.
- §2:rounded Mn empirical ratios10–11 and inconsistent percentage precision12
  held. Exact molar-mass sums and printed balanced material equations retained.
  Five salt types,ammonium exception and1:1 NaOH/H2SO4→NaHSO4 model are source
  specific. No invented products for the open reaction grid/chains or heat work.
- §3:unqualified all-metal phase/hydride statements19 held. Typical-property
  wording and iodine counterexample are separate. Exact Zn hydroxide equations20
  and CrO/Cr2O3/CrO3 classifications remain precise source contexts.
- §4:2Na+O2=Na2O2 on21 is atom-unbalanced;no silent correction. K/oxygen outcome
  and blanket hydrogen-halide gas phase need conditions. Water/chlorine models,
  family lists,table identities and aqueous acids remain. Inert-gas oxygen/
  fluorine exception retained;no universal no-compound assertion.
- §5:N2O5 row29 labels valenceIV,conflicting with given oxygenII rule/formula;
  IV/V cell answers held. Li superlative and repetition stay within shown
  examples. Historical1869 mass definition25 and modern nuclear-charge
  definition30 are distinct;Ar/K ordering and historical Be prediction retain
  actual source rounded values. No external current chemistry/history added.

Five additional editorial reviews bring31 open issues plus one scientific
blocker. Coverage/software tests are not independent teacher review or publication.


## Batch17 source review — grade8 §6–10

Original31–48 fully read. §6 ends33 before§7 on34;§7 ends in37 before§8;§8
includes exercises on41 before§9;§9 ends in44 before§10;§10 ends47,with§11
starting48. Printed=PDF,full-page identity/image SHA recorded for every ref.

- §6:book short eight-group/main/side representation scoped. H/He first period
  is explicit32;universal alkali-start and outer-electron/group equality withheld
  (He row43 reviewed). O/F valence exceptions kept;no Fr superlative key.
- §7:p/e equality is neutral-atom only. Rounded particle masses1/1/0 and Ar=N+Z
  cannot become exact physical masses or a fractional isotope-average identity.
  Original A is explicitly the given total nucleus-particle count. No ion/radiation
  experiment or external nuclear model;historical scattering analysed only.
- §8:38 chart fractions and35.543 prose disagree with label35/37 weighted result;
  chart mass/particle meaning is unclear. Natural K proportions41 uncorroborated
  in reviewed supplied pages. Both withheld,not repaired. Exact definitions and
  given B10/B11/10.81 model40,Ar counts39–40 and isoton examples40 retained.
- §9:classical centrifugal stability41/mechanical own-axis spin43 and arbitrary
  multi-electron energy-distance inferences held. Cloud,2n² maximum and exact
  H–Ar shell populations retained. He2/Na M1 illustrate limits of broad rules.
- §10:s/p/d/f,shapes,allowed l values,2(2l+1) and actual tables45–46 source based.
  Short terms/numbers/MCQ only,not chemical-formula parsing of orbital notation.
  Historical2019 block counts are attributed,not independently current-certified.

Four new scoped editorial reviews bring35 plus one scientific blocker. None
silently removed;all whole-course-ready flags false.


## Batch18 source review — grade8 §11–15

Original48–71 fully read. §11 ends in51 before§12;§12 ends in53 before§13;
§13 ends62;63 and top64 introduce chapter03 before§14;§14 ends in66 before§15;
§15 includes donor-acceptor69–71 before§16. All refs keep full-page/book/image SHA.

- §11:H–Ar neutral ground-state table strings/populations only. Third-period
  3d0/outer8 is not all-state capacity;2n² remains separate. No gas-density
  key from an unprovided state/model context or new orbital parser.
- §12:La f-start/Ce4f2 and20/8 shell detail52 held for state/configuration
  review. No alternate from memory. Clearly printed K/Ca/Sc/Zn/Ga/Kr/Cs retained.
- §13:unqualified oxygen-valence1–8/outer2=metal held against previous O/F/He.
  Sr88/As75/Ba137 are explicit integer models,not average-mass rounding. Cl38/59
  and mass/particle fraction terminology held;no natural Cl/Ag/Ne fraction key.
  Historical ekasilicon/germanium comparison is source-attributed. Worked/review
  material53–62 belongs to actual§13 anchor,not another source teaching count.
- Chapter03:63 and top64 are actual preface. Formula examples do not imply
  isolated molecules for ionic solids or unlimited octet/stability. New strict
  prefix context/null paragraph preserves the actual chapter title;64 requires
  explicit pre-heading evidence. Arbitrary future chapter pages are rejected.
- §14:exact clearly legible table65 values used without Li rescaling,unseen
  values or invented ionic cutoff. Na/F electron examples64 are given models.
- §15:all common-pair/nonpolar/polar/donor-acceptor topics retained. HCl partial
  charges are not full transfer;H2/O2/N2 are the supplied Lewis models. NH4+/H3O+
  recognition and donor identity use existing MCQ/short/numeric/formula inputs,
  not an unrestricted ionic/geometry/structure grader.

Six new scoped issues bring41 plus one scientific blocker. No silent repair,
physical experiment or independent teacher/publication certification.


## Batch19 source review — grade8 §16–20

Read complete original71–89;§20 ends88 before chapter04/§21 on89.

- §16:K+/Cl-/Ar all18 electrons with different nuclei. Broad shared-pair
  wording73 does not replace the earlier ionic-transfer distinction.
- §17:solid molecular lattice examples and amorphous exception retained.
  NaCl6 neighbours and diamond4 neighbours are separate printed models;
  no fabricated measured melting point or universal all-solids=molecules claim.
- §18:neutral weighted sum0,ordinary substances0,peroxide O−1 and metal-hydride
  H−1 remain explicit. Oxidation number is bookkeeping,not every atom's literal
  ionic charge. H3PO4 and Al2S3 worked models use exact source pages.
- §19:unchanged oxidation states in CuO/H2SO4 differ from CuO/H2 redox.
  Free metal and metal ion are distinguished. Earlier§18/78 supplies explicit
  hydrogen context for H2/LiH/HgO examples. Electron loss/gain uses existing
  short/numeric types;no typed charge parser.
- §20:unbalanced intermediate lines83–84 are working steps. Final given-product
  equations and original balancing are distinguished. N2O+1 is an average
  model;nitric-acid products require their exact supplied context. No invented
  general reaction prediction. All complex equations pass atom/material balance.

Five new editorial scopes bring46 plus one scientific blocker. No silent repair
or independent teacher certification. All course-ready flags remain false.


## Batch20 source review — grade8 §21–25

All original89–111 read. Shared heading boundaries respected;chapter04 on89
has no scientific prefix before§21. No new chapter-prefix permission added.

- §21:exact short-table families/trends with89/90/92 citations,He2 andXeF4
  exceptions. General highest-oxide row is not a universal noble-gas formula.
  CO2 bond/molecule distinction is explicitly printed90. Water association
  illustration is not a definite n-index compound for formula grading.
- §22:neutral configurations,outer7,exact halide examples,source displacement
  equations and phases/colors.95 history1866/density conditions/unconditional
  iodine heat path held;no alternate date/constant from memory. Forward
  sublimation concept retained without an all-pressure phase assertion.
- §23:actualCl2 molecule vsion crystal uses earlier16/73,17/74 and23/96 context.
  Exact hot/coldKOH products retained. Solubility97 at20°C versus22.4L/mol
  arithmetic99–100 lacks state correspondence,so0.63% is not an answer key.
- §24:gas/aqueousHCl distinction,all given material equations and theoretical
  stated n.sh./100% examples retained. No universal dry-gas nonreaction or500
  condition-free solubility key. Final rounding is explicit.
- §25:103–111 gas limitations,Vm/density/relative density,particle counts,liquid
  water4°C and clear40/60 volume mixture covered. Water-vapour107/111 held;
  no invented gas state. Precision-dependentH2 table and ambiguous107 mixture
  basis not merged with integer models. Exact2.86*22.4=64.064 is explicitly
  rounded to64,not represented as an exact equality. NO2/air stays given model.

Five new editorial scopes bring51 plus one scientific blocker. Digital analysis
only,no physical gas generation/heating/collection or medical/teacher certificate.


## Batch21 source review — 2026-10-25,grade8 sequence26–30

Original111–134 read;source order§26/27/28/practical1/§29 preserved.

- §26:bookE/equivalent-mass units andvalence/full-replacement model are explicit.
  ClearCa20/oxide28,Fe28/18.67,CO6/CO2=3 and original mass-ratio exercises retained.
  Cu52.74→52.7 working precision and questionO/solutionAl9 mismatch held.
- §27:gas/aqueous distinction,indicators,clear metal/oxide/base/carbonate/AgCl/
  redox models,chloride/mineral/industrial categories andoxyacid names retained.
  Density conditions,HgCl2 insolubility,atomicO/lime notation/balance,medical/
  current-population claims and unqualified oxidant rankings held.
- §28:actual minerals,diatomic/dispersion trend,explicitXeF2/SiO2/F2/water/HI
  material balances,Ag/Pb halide colors andindustrial categories retained. HI
  heat sign and unqualified reaction predictors not keyed;clinical dosing and
  sedative/hemostatic claims held. No new charged/reversible-equilibrium grader.
- Practical1:all6 tasks mapped into evidence and original balances. ThreeZnCl2
  acid models explicitly116/20;fourth originalZn+Cl2=ZnCl2 combines actual earlier
  Zn-metal75,generalCl2-metal97,known product116 and task124. All exact refs kept.
  AgCl/AgI evidence alone does not identifyNa;no invented observation/flame test.
  Ca(OH)2 conflict124 uses separately verified125.128 firstdivision,not wrong
  secondmultiplication.129H2S observation lacks earlier taught support and is
  held,not borrowed from future§30. Clinical context held. Original ion counts
  use explicitα1,priorCa40/NA andsame-practicalCl35.5 with full composite refs.
- §29:outer6,OF2/H2O2/ordinary0,S/Se/Te models,natural sulfides/sulfates,allotropes,
  nonwetting/flotation and exact source redox models retained. NoSe79 natural
  abundance,universal d-promotion/oxygen/S−2 or physicalCS2/plastic-sulfur task.

56 editorial issues plus one scientific blocker;all course-ready flags false.
All817 original pages decoded,five SHA identities checked. No independent teacher
or medical certification. Original135–147 read next;not yet authored facts.


## Batch22 source review — 2026-10-25,grade8 §30–34

Original134–top147 read in full;shared headings delimit each topic.

- §30:gas/aqueousH2S,oxygen-dependent products,FeCl3/Cl2/H2SO3 and clear acid/
  sulfide tests retained. Exposure limits,solubility conditions and actual school
  air-testing withheld. Original density uses priorH1/S32/H2/air constants.
  Original oxygen-only80gS calculation is not claimed as air volume;future
  air-fraction context is forbidden. CuSO4 product-given balance is original
  application of the suppliedCuS model,not a fabricated observation.
- §31:all clearSO2/SO3 production/acidic/sulfite/redox models,oleum recognition,
  original50/50 composition and5.6LSO2/pyrite exercises retained. H2SO3 aqueous
  model and variableoleum composition remain scoped;no isolated-species proof
  or new complex syntax. Solubility/exposure/food-preservation keys withheld.
- §32:explicit dilute/concentrated models and source conditions,whiteBaSO4,
  named sulfate hydrates,applications and original5.4gAl/20% problem retained.
  Ag blanket nonreaction,elementalS gas,undefined organic equation and gypsum
  quarter-water conflict held;no silent alternative from memory or physical task.
- §33:average reactant decrease1→0.4 over10s gives0.06;given gamma2 gives16/32/
  128. These are models,not general orders/rates for all species/reactions.
  Missingk/display ambiguity and coefficient=universal-order claim withheld.
  Five factors,catalyst examples and inhibitor retained with net/example scope.
- §34:school irreversibility/reversible aqueous model,dynamic rate equality,
  catalyst nonshift and conditional heat/pressure/concentration comparisons.
  No lowerT=faster or absoluteSO3 volume key;equal rates not all concentrations.
  Finite material balancing is separate from equilibrium direction;no new solver.

61 editorial scopes plus one scientific blocker;ready false. All817 pages/five
SHA identities audited. Original148–165 read next,not yet authored facts.
