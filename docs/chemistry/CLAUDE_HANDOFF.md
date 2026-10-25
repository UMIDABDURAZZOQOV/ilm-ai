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

124 reviewed lessons:all74 grade7 entries and grade8 §1–44,practical1–5 and lab1;144 remain. All
whole-course flags remain false. §2 is substance properties, practical1 is safety.
The previous safety label for §2 was a handoff error.

MCQ, bounded short text, exact fixed-unit numeric input, formula notation and
finite equation balance share ILM AI v2 ordered attempts, private server rubrics,
immutable snapshots, replay, expiry, source feedback and once-only XP. Read
ASSESSMENT_CONTRACT.md for actual syntax/limits; charge/structural/general-unit
engines are not silently supported. Flutter uses common Ilmo/source/feedback/
result/exit components and a separate explicit local preview entrypoint.

Exact implementation commits/tests/next page: CHECKPOINT.md and QA_REPORT.md.
Next nine:grade8 labs2–10,sequence51–59,original200–204.
Grade7 all74 entries;grade8 has50/59.
Nine grade7 reviews integrated;chapter prefatory context is not an extra entry.
One scientific blocker/77 editorial reviews still gate readiness. Same shared
MCQ/FRQ/feedback/XP/draft rules;no new orbital/ionic/structure prediction engine.

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


## Batch09 digital practical and oxide boundaries

Practical5 includes both solution-label/report arithmetic and soil-filtrate/
litmus observation. No physical procedure or agricultural treatment is assigned.
ChapterIV review identities ch7-6/ch7-7 attach only to that preceding lesson.
CaCl2 M111g/mol comes from explicit worked96. Source99's bad §9 pointer is
resolved to actual §7/26,not copied into false source metadata. Oxide graphics
are the prior§9 valence-line representation,not a claim of molecules/covalent
bonds for every oxide. Source-specific formula/equation spelling bounds remain.

New held contexts:universal soil-indicator colour94,hot water-vapour state98,
Fr state100,Fe/O percentage precision104. Together with previous holds there
are13 scoped editorial issues plus the grade9 scientific blocker. None is
silently repaired or promoted into verified teaching/keys. Read SOURCE_REVIEW.md.


## Batch10 oxide applications and bases

§37–41 adds29 cards/43 questions. Source37 gas constancy/absolute occurrence and
gemstone-host assignments are held. Grade9§27/130–131 was visually compared with
grade7/108;the incompatible host lists and unbalanced Al(OH)3/KOH equation are
explicit review issues,not corrected from memory. Total15 editorial issues plus
one scientific blocker. No source-complete or teacher-certified claim.

Base formulas preserve parentheses;NH4OH is the supplied notation convention.
Partial neutralisation retains Mg(OH)Cl/CaHPO4 and Cu(OH)Cl products. The current
equation editor accepts plain material equations,not ↑↓ annotations. Indicator
and precipitate observations are recognition tasks. No reagent/heating/exposure
or home experiment. Ca(OH)2 ratio uses the printed1.56g/1l water at20°C;
the original half-water question expects0.78g without inventing a solution density.


`import_reviewed_lessons(db)` validates the full explicit index once per call,
before storing anything. CLI,synthetic preview and test fixture use this safe
batch path. It accepts no caller documents and caches nothing. Per-row published
immutability remains unchanged. `import_lesson` still rejects changed documents.


## Batch11 acids and practical6

§42–44,practical6,§45 adds39 cards/53 questions. Acid naming groups preserve
reviewed formulas;no legacy HJ/J substitution or blanket total-written-H rule.
H3PO3/H3BO3 names/formulas are distinct from their held basicity/residue claims.
Partial neutralisation keeps Mg(OH)Cl/KH2PO4;Cu/concentratedHNO3 keeps NO2.
Do not grade the196gCu(OH)2/73gHCl exercise as unqualified full neutralisation.
Unexplained keyword-only bromat/atsetat/oksalat116 remain a visible source gap.
Total19 editorial issues plus one scientific blocker;no course-ready claim.

Practical6 retains copper and iron oxide branches in digital source/report
analysis. Actual copper equation/molar data come from earlier worked50,not an
invented practical121 quotation. Original4g virtual variant:4.9g acid,8g salt,
0.9g water. No heating,reagent setup,physical observation invention or invented
iron-sulfate formula. Applications and passivation remain scoped recognition.

Existing source_context_ids can now cite a same-book earlier review only if its
end precedes the new topic and its last preceding teaching sequence is earlier.
The explicit lesson index must already integrate that review in a previous
manifest. Future,unintegrated,cross-book and same-chapter activity mislabelling
remain rejected. Exact source title/null paragraph/page and image hashes remain.
No new learning mechanism or XP rule. Flutter uses the same source-button path.


## Batch12 salts and equivalent law

§46–50 adds42 cards/59 questions;chapterV review135–136 belongs to§49 before§50.
Earlier ch7-6/96 supplies M(NaOH)=40 with its actual null-paragraph review title;
the original full-neutralisation4g model requires0.05mol H2SO4. Condensed
CH3COONa and grouped phosphate/basic salt formulas are finite reviewed spellings.
Hydrate-dot,complex brackets and double salts remain MCQ recognition,not a new
input grammar or general equivalence/structure engine.

New holds:KJ125;Cu missing from product130 and legacy NaJ/AgJ132;clinical/body
percentage/saline-density/current-industry scope133–134;sulfur oxide printedCO2,
fumigation doses,98/3 decimal precision and gas-state/unit/generalisation scope
137–140. Total23 editorial reviews plus one scientific blocker. Never silently
repair any of these as a verified key. Equivalent examples are explicitly
compound/reaction-specific;one-equivalent mass questions use the source's
worked g models. H3PO4 calculation remains exact98/3,not32.66/32.67 grading.


## Batch13 genetic links,practical7 and laboratories1–3

§51,practical7,labs1–3 adds24 cards/39 questions. Labs have distinct labNN keys
and source activity labels,ordinary MCQ/FRQ/XP and exact prerequisites. No new
learning mechanism or real-lab certification. Blank table147 is not filled with
fabricated measurements. Lab2 retains all3 components but odour is recognition
only;lab3 retains burning,copper and carbonate inquiry without invented results.

Practical7 retains all5 inquiry components. Unknown black powder has no asserted
purity;indicator observations are explicit virtual rows from111/118. The balanced
CuCl2/NaOH solution is an original solution for chain144 using earlier review135
and formulas112;it is not a silent certification of malformed130. That hold stays.
Mass models144 explicitly use totals/declared rounding;ideal copper conservation
146 explicitly assumes no loss. Clinical recipe and unspecified CO2-product
volume are held. Total25 editorial issues plus one scientific blocker.


## Batch14 laboratories4–11

Eight separate ordered lab entries add28 cards/51 questions. All retain the
existing MCQ/FRQ/feedback/XP/prerequisite system. Lab4 uses verified simple/
compound and metal/nonmetal examples. Lab5 keeps all3 reaction modes,including
an explicitly original Fe/CuCl2 model with given FeCl2/Cu products and earlier
substitution/formula evidence. No invented measured copper deposit/colour.

Lab6 oxide and lab7 fuel tables are blank;formula/group data come only from
earlier reviewed102/103/63,not fabricated specimen values or efficiency numbers.
Labs8/9 use exact earlier Zn/HCl70 and CuO/H2 73 equations plus explicitly virtual
1:1 molar models. Lab10 retains all3 oxide/water components and exact earlier
indicator tables,not a universal oxide/water rule. Lab11 original full-neutral-
isation models explicitly give products using actual earlier50/111/119 evidence;
no claim that the completed equations or colours/crystals are printed on153.


## Batch15 laboratories12–16

Final5 labs add17 cards/33 questions. Original154–155 plus precise earlier
formula/equation/indicator contexts were visually read. Lab15 unspecified
Cu/H2SO4 concentration/heating is held in ch7-lab15-acid-condition-scope and
machine guarded;no universal outcome key. All original products-given balancing
models are distinguished from printed completed equations. No invented starting
CuOH2 colour,pH7 endpoint,crystal/hydrate value or physical procedure.

Pure positive grading tests06–15 now share a module-scoped fully validated
document snapshot,with a teardown fingerprint proving no mutation. Source
mutation/loader/import/API tests still read and validate fresh. No runtime or
importer cache introduced;all363 Chemistry tests pass (one opt-in PG skipped).


## Batch16 grade8 §1–5

Original5–31 fully visually read. Exact pages are full,printed=PDF. New source
holds are pinned:ch8-p01-mol-definition-scope,ch8-p02-rounding-scope,
ch8-p03-classification-scope,ch8-p04-oxygen-and-phase-scope,
ch8-p05-nitrogen-valence-review. Unambiguous definitions,worked masses/amounts,
five salt classes,amphoteric models,families and historical/modern periodic-law
definitions remain distinct. No repaired Na/oxygen or N2O5 valence answer.

Private author_grade8_helpers.py is a grade8 serialization helper,not a source
of science. Never rerun indexed author_batch16.py or its catalog initializer.
New earlier-grade facts must remain immutable. All input/XP/feedback contracts
unchanged;no orbital/ionic/hydrate/general structure prediction engine added.

Chemistry-only display converts Unicode indices to ordinary digits and raised
runs to explicit ^(...) spelling,avoiding absent Roboto glyphs. It does not
mutate manifests,answers,labels used for grading or API data. Shared source
button gains optional locatorSeparator (default unchanged for other subjects).
Chemistry uses ASCII ->. Modal source QA now scales the navigator overlay too;
previous home-only MediaQuery captures did not certify the modal at200%.


## Batch17 grade8 §6–10

All original31–48 images visually read before authorship. Five lessons add35
cards/52 questions:14 MCQ,11 short,27 numeric. Atomic/subshell terms and supplied
integer/weighted models use existing bounded text/numeric grading. No isotope,
charge,orbital,structural or unrestricted configuration parser added.

Pinned reviews:ch8-p06-group-rule-scope,ch8-p07-mass-model-scope,
ch8-p08-isotope-average-scope,ch8-p09-classical-electron-model-scope. First-period
H/He exception and short eight-group representation are explicit. Original A in
§7 is declared total nucleus-particle count,not a silently repaired average Ar.
§8 B10/B11 model is conditional source40 algebra,not a new natural measurement.
§9 maximum2n² is distinct from actual Na M1 and other shell populations43.
§10 orbital shape/count/capacity and2019 block counts retain exact table context.

Current private sandbox84 completions/1680XP on8900,own PID28132 (verify before
stop). Never rerun indexed author_batch17.py or source-review initializer. Original
48–71 already visually read for next batch;chapter03 intro63 is a container
anchor,not an invented extra lesson. Assess precise source-context support before
using chapter preface facts;do not label chapter3 as paragraph3 or cite future
chapter pages. Upcoming Ce/La52 and isotope-fraction/table scopes need review.


## Batch18 grade8 §11–15 and exact chapter prefix

Original48–71 fully visually read. Five lessons add39 cards/61 questions,
including donor-acceptor69–71. H–Ar,K/Ca/Sc/Zn/Ga/Kr/Cs,Sr/As/V and historical
predictions are precise source examples;La/Ce detail52 held,not corrected.
Natural isotope mass/particle fraction ambiguity and Cl38/59 conflict remain.
Bond polarity is not an unreviewed whole-molecule geometry statement. Donor
pair origin is distinguished from a shared resulting bond. No new typed ionic,
orbital,formal-charge or Lewis-structure syntax.

Chapter context is now accepted only for the same chapter's prefix,whose start
precedes its first teaching paragraph. Full earlier intro pages allowed;the
first teaching page needs matching before_first_teaching_heading scope in ref
AND original-image evidence. No later chapter page allowed. Chapter refs have
paragraph:null,actual chapter title and exact book/page/image SHA. This fixes
63 and top64 preface without falsely calling it§3 or§14. Existing84 manifests
remain byte-identical. No catalog container is counted as another teaching entry.

Flutter preserves separate scoped source groups and displays the actual heading
boundary in localized source sheet. Sanitized actualHTTP chapter-intro fixtures
use fake attempt ID/future expiry,no private keys/tokens. Own sandboxPID15680,
89 synthetic900003 completions/1780XP on8900;verify command before stopping.


## Batch19: oxidation and redox

Original71–89 fully reviewed. Five lessons add44 cards/66 questions,including
ionic K+/Cl-/Ar comparison,lattice neighbours,peroxide/hydride exceptions,
electron balances and original balancing of the textbook's given products.
N2O oxidation+1 is a worked average,not an individual-site assertion. Exact
nitric-acid products remain tied to their stated equation/conditions. No
physical heating,gas collection,mercury handling or charged-half-equation engine.
Five scoped reviews bring46 editorial issues plus one scientific blocker.

Numeric input accepts the mathematical minus U+2212 as a spelling of ASCII
minus. Raw80-character limit and Decimal grammar still apply;units,expressions,
charges,superscript minus and en dash remain rejected. Canonicalization treats
−2/-2 identically for replay. Source facts and numeric keys are unchanged.
Actual HTTP preserved89 completions/1780XP and added66 answers/100XP once:
94 completions/1880XP. Own loopback8900 sandbox PID16136;verify command before
stopping. Earlier94 imported lesson revisions are immutable. Sanitized public
oxidation/redox fixtures contain fake attempt IDs,not tokens or private rubrics.


## Batch20: nonmetals through gas models

Original89–111 read;five lessons add54 cards/78 questions. Short-table labels,
He2/XeF4 exceptions,ionicNaCl vsCl2,hot/coldKOH products,gas vsaqueousHCl and
matching gas temperature/pressure retained. Liquid water4°C is separate from
n.sh.22.4L/mol gas calculations. Scientific notation reuses existing Decimal
grading;no gas-law,charge,hydrate or general-unit engine added.

Source-held keys:universal noble-gasRO4;unverified1866 history;table95 density
conditions;unconditional iodine phase path;chlorine0.63% mixed-state result;
HCl500 volume without conditions;water-vapour112L without gas-state support.
Five new reviews bring51 editorial issues plus one scientific blocker. Numeric
rounding is explicit;unrounded intermediate liquid-water particle calculation
produces3.344e25 to4 significant figures. Clear40/60 volume-fraction mixture is
separate from ambiguous107 percentages. NO2/air is a given M46/M29 model only.

HTTP preserved94 completions/1880XP,passed78 questions,added100XP once:
99 completions/1980XP. e/E scientific-notation replay identical. Same owned
loopback8900 sandbox now PID14352;verify full command before stopping.
Earlier99 imported revisions immutable. Flutter production code unchanged.
Next§26/27/28/practical1/29;original112–134 also visually read during QA wait.


## Batch21: equivalent law,halogen practical,oxygen family

Original111–134 fully read;five source-order lessons add59 cards/72 questions.
Practical1 lies between§28 and§29. All six categories use digital evidence and
given-product atom balancing,no invented tube result/flame test/physical lab.
The fourthZnCl2 equation is an explicitly original application of earlier
Zn-metal75/Cl2-metal97/knownZnCl2 product116,not falsely a printed equation124.
EarlierZn(OH)2/HCl is explicitly printed20. Composite claims cite all these
sources and question/solution/source-group refs retain them. Ag-halide evidence
does not independently proveNa cation. BalancedCa(OH)2 equation is separately
verified125;conflicting124 copy remains held.128 first division method retained,
second multiplication copy held. No clinicalCaCl2/F/Br/iodine advice or doses.

Equivalent law retains supplied valence/reaction and textbookE/unit conventions;
Al/O target mismatch114–115 is not silently repaired. HgCl2 insolubility/atomicO/
lime ambiguity held. Oxygen exceptions,ordinary0,S/Se/Te source models,allotropes,
natural compounds and exact redox models retained without universal d-promotion,
Se79 representative-isotope or all-sulfideS−2 keys. Five new issues bring56+1.

Mutation tests found new checks initially placed in the question loop using the
last fact. Moved them into per-fact validation;all45 target tests now pass. No
held claim entered imported lessons. HTTP preserved99 completions/1980XP,passed
72 questions,added100XP once:104/2080XP. Own loopback8900PID21696;verify command
before stopping. Earlier104 imported revisions immutable. Public practical
fixtures have fake attempt IDs/future expiry,no private rubrics/tokens.

Flutter production code unchanged;two actualHTTP widget cases cover original
equation and2.408e23 input,multi-source feedback and actual practical label.
Full30-lesson catalog/attempt payloads triggerDio background JSON isolation;
bounded real-async waits in harness drain decoding before UI assertions. This
fixes test timing assumptions,not scientific grading or production behavior.
Original135–147 additionally read for next batch during QA.


## Batch22: sulfur compounds,rates and equilibrium

Original134–147 fully read;five lessons add56 cards/74 questions. All clear
H2S/SO2/SO3/H2SO4 material models and source conditions retained. Earlier1/7
H1/S32/O16,2/12Al27,25 gas model and26Fe56 evidence supports original density/
mass/stoichiometry calculations;all constituent refs retained. H2SO3 is a
supplied aqueous model,not isolated-species proof. Air-volume question136 lacks
earlier verified air fraction,so only its oxygen portion is keyed;no future§33.

Exposure/solubility conditions,Ag nonreaction,gypsum water conflict,symbolic
carbonization,universal rate-order/temperature rules and lowerT=faster claim held.
Rates use exact average0.06 and given gamma2 models;equilibrium uses dynamic
rate equality and conditional direction comparisons. No unrestricted rate-law/
equilibrium/charge/structure engine. Five new reviews bring61 plus one blocker.

HTTP preserved104 completions/2080XP,passed74 questions,added100XP once:
109/2180XP. Comma/dot0.06 replay identical. Own loopback8900PID19612;verify
full command before stopping. Earlier109 imported revisions immutable.
Sanitized public kinetics/equilibrium fixtures contain fake IDs/future expiry.

Visual QA found actual missing⇌ glyph in the bundled Roboto font. The existing
Chemistry display adapter now renders it as <=>;source payloads,typed input,
rubrics and server grading stay unchanged. Unit check confirms source JSON is
not mutated. New theory/source widgets cover gamma/equilibrium at320×568/200%,
both themes;updated captures show the repaired sign. No native/IME certificate.
Original148–165 also visually read for the next batch.


## Batch23: sulfur practical and nitrogen

Original147–top165 reviewed;five lessons add60 cards/86 questions. Clear source
industrial sulfur models and all four digital practical categories retained.
Prior33/142 and current155 now support a new later80gS/air calculation266.67L;
old immutable§30 remains oxygen-only. Ozone heat153 and100g/200g solution154
conflicts remain held;clear11.65gBaSO4→4.9g pureH2SO4 step is retained.

Chapter06 prefix156/top157 keeps actual title,null paragraph and matching
before_first_teaching_heading scope on157 refs AND image evidence. Bi5p10 row
held;P complete configuration independently verified in earlier table11/50.
N2/nonpolar/triple-pair,source air fractions,nitrides and conditional gas models
retained. NH3/ammonium donor pair distinguishes N valence4 from oxidation−3;
acid-salt/normal-salt ratios and Pt/uncatalyzed products remain explicit.
NH4OH is aqueous school notation,not isolated-molecule proof. Six N-oxide
identities and conditionalCu/HNO3 models retained;N2O5 valence and unqualified
realNO2 density remain held. Density questions explicitly use school models.

Initial manifest validation rejected three missing exact Uzbek answer labels;
page-verified synonyms were added before first import. No validator weakening.
53 new backend tests and actualHTTP86 answers pass. Synthetic109/2180XP
preserved,then114/2280XP;Unicode/ASCII−3 replay identical. No new parser.
Own loopback8900PID27844;verify full command before stopping. All114 imported
revisions immutable. Public nitrogen/ammonia fixtures have fake IDs/expiry.
Four small-screen/200% widgets in both themes cover chapter157 heading scope
and signed numeric feedback161;source sheets/pinned continuation inspected.

Original166–185 additionally read for continuation. Private detailed next-source
notes:.local/batch24_source_notes.md. Before authoring next batch,catalog the
newly found nitrate/generalization,cyanamide formula,phosphine/directreaction,
phosphate solubility/structure and unbalanced water184 issues. Do not silently
repair. All course-ready flags remain false;no independent teacher certificate.


## Batch24: nitrates,phosphorus/phosphates and digital practicals

Original165–top184 reviewed;five lessons add68 cards/86 questions. Specific
nitrate/Cu/Pb/Fe models,industrial source diagrams,allotropes,acid/salt/ion
models,clear biology/history and original worked arithmetic retained. No new
parser,AI or production capability. WrongNH3+NH3 prose,Ca(CN)2/name mismatch,
directP/H2 formation,unconditionalredP safety,phosphate solubility/structure/
clinical claims and unbalanced water184 remain visible review scopes.

Initial misplacedHCl24/98 citation rejected and replaced by visually checked
27/116. Final dissociation card clarified that residual acidH count decreases,
not H+ itself. Pre-clarification full run was stopped,not counted as passed.
Older119-lesson disposable DB was preserved;fresh batch24-final-qa copied only
114 exact synthetic baseline progress rows/2280XP after checking lesson SHAs.
New119 lesson QA then passed86 answers and once-only100XP→2380XP. Comma/dot
0.833 replay identical;grade7 unchanged. Loopback8901PID19924,private defines
in the fresh sandbox. Older8900 sandbox remains historical,not current.

Full739 backend and510 Flutter tests pass;two new320×568/200% widgets cover
decimal practical feedback172173 and clarified ion theory/source178. Five
captures inspected;no native/IME/TalkBack certificate. All114 prior hashes
and original§1 unchanged. 72 editorial scopes plus one scientific blocker.

All remaining grade8 teaching pages through204 read;205–208 contents/colophon/
rental seen. Upright table199 exposes contradictory NH4Cl nitrate-gas positive
andKNO3 negative rows:hold,no silent swap. Private detailed remaining-source
notes:.local/grade8_remaining_source_notes.md. Before next authoring,catalog
commercial nutrient-equivalent/hydrate scopes,16.4/4.117/473.3 arithmetic,
medical/essentiality/clinical claims in§44,table199 and lab1 condition reviews.
Source knowledge remains textbook-only;never fill gaps with memory.


## Batch25 — 2026-10-25: grade8 sequence46–50

124/268 implemented;144 remain. Grade7 all74;grade8 all44 paragraphs,all5
practicals and lab1 (50/59). Next nine labs2–10,sequence51–59,original200–204.
New5 lessons add59 cards/68 questions (19 MCQ,8 short,18 numeric,11 formula,
12 equation). Total980 cards/1425 questions:483/235/374/128/205 respectively.

§42 distinguishes primaryNPK from total element counts;commercial percentages,
hydrates and mixtures are not pure compound identities. §43 teaches P2O5/K2O
reporting equivalents and exact given arithmetic:16.47%,4.120t,473.2kg,with
printed16.4/4.117/473.3 separately flagged. §44 retains neutral source
classification/relative amounts/symbols/environment;clinical,treatment,
universal essentiality,current statistics and waste application claims held.
Practical5 covers digital known models and original exact calculations;upright
table199 contradictory nitrate rows held. No unknown sample IDs or actual
observations invented. Lab1 retains exact school zincate model and limited Cu
comparison. Exact prior Na/water4/21,AlCl3 20/83 and KHSO4 2/15 checked.

77 editorial scopes plus one scientific blocker remain;all ready flags false.
No source gap filled by memory,AI feature,new solver,physical experiment or
teacher certificate. Five PDF identities/all817 decoded pages audited.

Target50 passed/20.53s;full Chemistry789 passed,1 opt-in PG skip,1 existing
Starlette warning/906.77s. Full Flutter512 passed/137s. Analyzer initially
reported missing braces in one new test;fixed,final no issues/35.0s. Two new
320×568/200% light/dark widgets passed/15s;four captures visually inspected
for fertilizer decimal feedback/source191 and zincate feedback/source200.
Scroll/pinned continuation preserved. No runtime UI/parser change this batch.

Actual loopbackHTTP68 answers preserved119 completions/2380XP,added100XP
once,now124 completions/2480XP. Comma/dot4,120/4.120 replay identical,grade7
unchanged,private rubrics hidden,six public fixtures sanitized. Current sandbox
ilm-ai-chemistry-batch24-final-qa,port8901,ownPID24132 (verify command before
stopping);private defines remain there. Imported r1 lessons are immutable.
All prior119 hashes and original§1 unchanged;critical Ruff/diff checks passed.
Biology/Physics branches and real user data preserved. No production/main,
PDF/OCR/fulltext/token push or native/IME/TalkBack/whole-backend certificate.
