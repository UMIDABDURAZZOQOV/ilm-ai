# Chemistry: isolated local QA

This is a separate debug preview, not published Chemistry in the normal app.
Backend base: stable Biology c0f84d0; Flutter base: polished UI444743b.
Physics v2 contract references: 07f748b/cf01011. Chemistry adapters have their own
namespace/tables. No Physics files or Biology validation/grading code changed.

## Validate without a database

```powershell
python scripts/catalog_chemistry_sources.py
python scripts/import_chemistry_curriculum.py
```

The importer defaults to pure validation. It does not import ORM/database modules,
even when a production DATABASE_URL is in the environment. Only explicit,
unchanged reviewed index entries can be applied. The first conceptual lesson
supports MCQ and bounded short text. Batch02 adds exact numeric_value FRQ in
the stated unit. Formula/equation input parsers remain pending.

## Disposable sandbox

Run from the backend Chemistry worktree. Use a **new directory outside every
Git repository**. The helper creates one synthetic learner900003 and a separate
`chemistry_staging.db`. It never opens production, normal OAuth or real accounts.

```powershell
python scripts/serve_chemistry_preview.py --directory C:/Users/Page/Desktop/Projects/ilm-ai-chemistry-local-qa --port 8897
```

Use `--resume` only when reopening that helper's existing sandbox. It refreshes a
private one-hour test token in `flutter-defines.json`. Do not commit, upload or
paste that file. `--create-only` prepares the sandbox without starting the server.
The server binds only127.0.0.1; the QA CORS origins use port7358.

From the Flutter Chemistry worktree:

```powershell
flutter run -d chrome --web-hostname=127.0.0.1 --web-port=7358 --target=lib/chemistry_preview_main.dart --dart-define-from-file=C:/Users/Page/Desktop/Projects/ilm-ai-chemistry-local-qa/flutter-defines.json
```

Use the SDK's Dart/flutter_tools.snapshot invocation if flutter.bat is unsuitable
in the local shell. Normal main.dart, Google sign-in, navigation and publication
flags stay intact. The separate entrypoint requires debug mode, an explicit
CHEMISTRY_PREVIEW flag and a loopback API; release/public/LAN hosts fail closed.

## Regression commands

Windows backend tests need `PYTHONUTF8=1` because existing Biology tests read
UTF-8 manifests with the platform default. Reviewed manifest paths use LF through
`.gitattributes` so SHA pins survive Windows checkout. An initial CRLF checkout
was restored to the exact Git blobs; zero Biology content changes were staged.

Set test-only ENVIRONMENT, DATABASE_URL pointing to disposable chemistry_staging
SQLite, AUTH_STORAGE=database and a synthetic JWT_SECRET. Use an explicit local
`--basetemp` and `-p no:cacheprovider` when the OS temp/cache ACL is unavailable.
Long Windows integration runs may require test-only
`ACCESS_TOKEN_EXPIRE_MINUTES=120`; production defaults are unchanged.

```powershell
python -m pytest -q tests/test_chemistry_sources.py tests/test_chemistry_lesson.py tests/test_chemistry_batch02.py --basetemp=.local/pytest-chemistry -p no:cacheprovider
```

Real PostgreSQL tests use the existing opt-in loopback staging guard and a private
ILM_TEST_POSTGRES_URL_FILE. Each fixture creates a fresh random schema. No public
host, production URL, shared user data or SQLite fallback is accepted.

Flutter public fixtures are captured from the real test API, not hand-generated
grading payloads. Optional explicit fixture export:
`CHEMISTRY_WRITE_MOBILE_FIXTURES=<Flutter worktree>/test/fixtures` for
`test_mobile_fixtures_come_from_the_real_authoritative_api` only. No JWT/private
specification is exported. Widget screenshots can be captured under ignored
`build/chemistry-review` using `--dart-define=CHEMISTRY_CAPTURE=true`.

Actual pass/fail results and native-device limits: [QA_REPORT.md](QA_REPORT.md).


## Batch04 sandbox and notation

Current corrected local QA uses the separate directory
`C:/Users/Page/Desktop/Projects/ilm-ai-chemistry-batch04-final-qa`, port8898.
It contains only synthetic learner900003. Its private defines file is for the
separate debug entrypoint only. Do not commit tokens or reuse it for production.
Older development sandboxes preserve older immutable snapshots; source-copy
review fixes require a fresh sandbox, not importer overwrite. Formula/equation
input is now supported within ASSESSMENT_CONTRACT.md's explicit finite bounds.


## Batch05 final immutable sandbox

Current final21-lesson QA uses a fresh synthetic900003 sandbox at
`C:/Users/Page/Desktop/Projects/ilm-ai-chemistry-batch05-final-qa`, loopback8899.
Old sandboxes and their immutable rows/snapshots remain intact. Defines/tokens
stay private; no production application/router publication is implied.


## Batch07 final sandbox

Final31-lesson source-copy QA uses the new private directory
`C:/Users/Page/Desktop/Projects/ilm-ai-chemistry-batch07-final-qa`, loopback8900,
synthetic900003 only. Older sandbox26→31 continuity and immutable snapshots remain
intact. Never publish defines/tokens or treat the isolated preview as production.


## Current grade8 continuation (batch16)

The append-compatible batch07 sandbox onloopback8900 now has79 immutable
reviewed lessons:74 grade7 and5 grade8. Synthetic900003 has79 completions/1580XP;
no real accounts. Grade picker lists7/8 only and is hidden during an attempt.
Actual public grade8 fixtures contain source metadata and post-answer feedback;
fake attempt ID/future expiry replace private identities,without tokens/rubrics.
Fresh sandbox is required if an already imported revision is changed.


## Current continuation after batch17

The same private loopback8900 sandbox now contains84 immutable reviewed lessons
and84 synthetic900003 completions/1680XP. Grade8 has10 lessons;grade7 still74.
Older79 manifests/attempts and grade7 catalog were preserved during append QA.


## Current continuation after batch18

The same private loopback8900 sandbox now contains89 immutable reviewed lessons
and89 synthetic900003 completions/1780XP. Grade8 has15 lessons;grade7 still74.
Sanitized actualHTTP chapter-intro fixtures cover63 and scoped top64;source sheet
names the chapter and heading boundary,without a false paragraph3.


## Current continuation after batch19

Private loopback8900 now has94 immutable reviewed lessons and94 synthetic900003
completions/1880XP. Grade7 remains74;grade8 has20. Actual HTTP verifies U+2212
numeric answer and ASCII-minus replay equivalence. Public fixtures cover§18
negative oxidation input and§20 long redox equation in the common Flutter flow.


## Current continuation after batch20

Private loopback8900 has99 immutable lessons and99 synthetic900003 completions/
1980XP. Grade7 still74;grade8 now25. All78 new answers passed actualHTTP with
once-only100XP and identical completion replay. Scientific-notation e/E spellings
replay identically. No new Flutter production code,fixtures or response kinds.


## Current continuation after batch21

Private loopback8900 has104 immutable lessons and104 synthetic900003 completions/
2080XP. Grade7 still74;grade8 now30 withpractical1 in correct sequence29.
All72 new answers passed actualHTTP;100XP once,replay identical. Public practical
fixtures are sanitized;the fourth original balance keeps all earlier source refs.
No production Flutter change. Full catalog JSON decoding is awaited in widget QA.


## Current continuation after batch22

Private loopback8900 contains109 immutable lessons and109 synthetic900003
completions/2180XP. Grade7 remains74;grade8 now35. ActualHTTP passed74 answers
and once-only100XP;comma/dot replay identical. Public kinetics/equilibrium
fixtures are sanitized. Display-only <=> fixes missing⇌,without changing raw
source or grading. No new response type or production publication.


## Current continuation after batch23

Private loopback8900 contains114 immutable lessons and114 synthetic900003
completions/2280XP. Grade7 remains74;grade8 now40. ActualHTTP passed86 answers
and once-only100XP;Unicode/ASCII−3 replay identical. Public nitrogen/ammonia
fixtures sanitized. Four source/feedback widgets at320×568/200% in both themes
pass. No new parser,production publication or real-user operation.


## Current continuation after batch24

Current fresh sandbox:ilm-ai-chemistry-batch24-final-qa,loopback8901PID19924.
It holds119 immutable lessons and119 synthetic900003 completions/2380XP.
Only114 exact old synthetic progress rows/2280XP were seeded read-only from
the previous sandbox;the revised five lessons then passed86 actualHTTP answers
and once-only100XP. Older8900 is historical. Use the fresh private defines file.
Comma/dot0.833 replay identical. Public nitrate/phosphate fixtures sanitized.


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


## Batch26 — 2026-10-25: final grade8 laboratories2–10

**133/268 implemented,135 remain. Grade7 all74;grade8 all59 mapped entries.**
Nine final labs add55 cards/93 questions:27 MCQ,9 short,20 numeric,23 formula,
14 equation. Total1035 cards/1518 questions:510/244/394/151/219 respectively.
Mapped coverage is not independent scientific approval;all ready flags false.

Original200–204 reviewed with exact prior source pages. KClcoord6 separated
from1:1formula;S8model versus other sulfur phases;iodine limitedtwoatom/solid
facts. AgClwhite/AgBrsarg‘ish/AgIyellow exact122;lab3 starch/food colors absent
and held. Soil task does not supply actual chloride result. Halogen3x3 table
uses exact earlierKmodels/rank for originalNa givenproductbalances. Iodine
water/organic qualitative comparison;layercolor/position/measurement held.
MineralsFeS2/ZnS/CaSO4·2H2O andS8 masses use exact priorconstants;formula
unit versus atom/molecule distinguished. Known four sulfate solution models
retainBaSO4white evidence;no universalwhitesolid identification. NH3 equation,
aqueousschoolmodel andindicator context retained;recipe1.5:1 is not exact
stoichiometricmass key. Fiveexplicit fertilizer examples,not invented samples.
NH3/HCl exact page161 checked instead of initial162 reference. Br2 FRQ uses
existing chemical_formula contract rather than prose;no new scientific parser.
86 editorial scopes plus one grade9 scientific blocker remain. No source gap
filled from memory,physical experiment,AI feature or teacher certificate.

Target final62 passed/6.88s;initial61pass/1fail was wrong test expectation
incorrect_species for formula mismatch (actual documentedcode incorrect),
fixed assertion only. FullChemistry851 passed,1 opt-in PG skip,1 existing
Starlette warning/389.15s. Critical Ruff anddiff checks passed;all prior124
hashes and original§1 unchanged. FivePDF identities/all817 pages audited.
FullFlutter514 passed/79s;analysis no issues/87.0s. Two new320×568/200%
light/dark laboratory widgets passed/6s;capture rerun2passed/7s. Four source/
feedback captures visually inspected203/204:scroll/pinnedcontinuation works.
No runtimeUI/parser change or native/IME/TalkBack/whole-backend certificate.

ActualHTTP93 answers preserve124 baseline completions/2480XP,award180XP
once→133completions/2660XP. Comma/dot74,5/74.5 replay identical;grade7
catalog unchanged,private rubrics hidden,six sanitized public fixtures.
Current sandboxilm-ai-chemistry-batch24-final-qa,port8901,ownPID9864,
verify full command before stopping;private defines stay there. All133 r1
imported revisions immutable. Real users,Biology andPhysics untouched.
No production/main/PDF/OCR/fulltext/token push or new externalknowledge.

Nextbatch27:grade9 §1–5,sequence1–5,original5–28. Original4–29 already
visually read;private notes .local/grade9_start_source_notes.md andrenders4–42.
Review before authoring:Ar/nucleoncount,legacygroup/period universal claims,
Mg radius .269 andstrictmonotonictrends,Cs strongestabsolute,orbitalpaths;
bond/valence/oxidation universals;water/CO2 conductivity,H3PO3 acidH task,
universal chloride safety;NH4OH schoolmodel/acidstages;58%H2SO4 ambiguous
basis,allorganicweak/allconcentrationstrong andunlimitedKconcentrationlaw.
Keep exact clear models,hold errors visibly,no silent memory repair.


## Batch27 — 2026-10-25: grade9 paragraphs1–5

**138/268 implemented,130 remain. Grade9 5/61;7/8 all74/59 mapped entries.**
New5 add64 cards/97 questions:28 MCQ,14 short,36 numeric,19 formula.
Total1099 cards/1615 questions:538/258/430/170/219 respectively.

Original5–28 fully reviewed:periodiclaw/history/nuclearcharge/atomcounts,
scopedlegacygroups/trends,capacities/configurations,bondtypes/energy/redox/
formaloxidation,electrolyte/ionmobility/hydration/H3O+,acid/base/saltstages,
degree/percent/weak equilibrium andconditionalK arithmetic. No new parser:
charged equations shown/selected inMCQ;FRQ existingneutralformula/name/
numericcounts. H3PO4 stages introduced only in§5 with actual27P(OH)3,
earlier§4task linked. Exactreferences9/11,23/24/25 and27/28 tightened.

91 editorial scopes plus one scientific blocker. Held source issues include
Ar/nucleoncount,Mg.269/strictIEtrend/Csabsolute,allperiodalkali/outer8 and
literalorbitalpath universals,bond/valence/oxidation universals,water/CO2
conductivity,H3PO3threeacidH/chlorideuniversalsafety,NH4OHschoolnotation,
58%H2SO4 ambiguousstage,allorganicweak/allconcentrationstrong andunlimited
Klaw. No silentmemoryrepair;all ready flags false. Originalgivenmodels and
arithmetic are labeled,not fabricated experiments or clinical guidance.

FinalfullChemistry916 passed,1 opt-in PG skip,1existingwarning/378.31s.
Targetfinal154/23.19s coversbatch16/26/27. Initialnew65/7.18s and127/13.99s
were before finalcopy. Fullv1/v2 stopped,not counted aspass:historicalbatch26
exacttotal133 andbatch16exactavailable[7,8] wronglyforbade newgrade9.
Assertions now preservebaseline andrequiredgrades while allowing continuation;
runtime/learningrules unchanged. All133 prior hashes/original§1 same;Ruff/diffpass.

FinalfullFlutter516 passed/79s;analysis noissues/5.7s. Two320×568/200%
light/dark grade9 widgets passed/3s;four finalfeedback/source11/28 captures
seen. Initialdraftwidgets2/2s,full516/80s,analysis26.2s precededcopyspacing.
Visualreviewcaught number/formula wordsjoined;onlynew5 learnercopy spaced.
Old138draft sandbox preserved. Fresh batch27final sandbox compared133content
SHAs andcopied only exactsyntheticbaseline progress/2660XP read-only,then
passed97actualHTTP answers and once-only100XP→138/2760XP. Comma/dot1,66/
1.66 andscientific1e-5/0.00001 replay identical;grade7/8catalogs unchanged,
private rubrics hidden,six sanitized fixtures. Grade9 selection uses existingUI.

Current sandboxilm-ai-chemistry-batch27-final-qa,loopback8902,ownPID24044.
Verifycommand before stopping;private defines staythere. Current138r1 immutable.
Older8901draft stopped(20776),preservedhistorical. No real-user/prod/main,
other-subject/PDF/OCR/fulltext/tokenpush,AI,newsolver orphysicalexperiment.
No independentteacher/native/IME/TalkBack/whole-backend certificate.

Next5:grade9 §6–10,original29–top53. All29–53 read;43–61rendered privately.
Notes .local/grade9_next_source_notes.md: H2Sinsolubleclaim,wateralpha,
weak/weakallfullyhydrolyze,FeIIIcarbonateunbalanced38,CO2conductancezero,
carbon2p6legend/fullerenecount/classicalphase constants,coalcurrentstatistics/
medicaladsorption andunlimitedheat/combustion claims need visible review.
Exactprovided textbookconstants fromearliergrade mayneed narrowly validated
explicitcrossgrade sourcecontexts;currentlyownbookonly. Do not fill bymemory.


## Batch28 — 2026-10-25: grade9 paragraphs6–10

**143/268 implemented,125 remain. Grade9 10/61;7/8 all74/59 mapped entries.**
New5 add72 cards/124 questions:23 MCQ,10 short,26 numeric,21 formula,44
equation. Total1171 cards/1739 questions:561/268/456/191/263 respectively.

Original29–top53 fullyreviewed:ion exchange/full/net models/qualitativetable,
hydrolysis/conditionalstages/limitingreactants,carbonfamily/allotropes/cycle,
adsorption/givenproductreactionfamilies,CO/CO2/salt-ratio/heat/density models.
Printed38water/FeOH2 errors held;originalgivenFeOH3/CO2 balance has3water.
ClearBaSO4 example5.825g andcarbonate1.12Ln.sh retained. SiH4 exercise uses
actual earlier8/25/110He4,8/5/27Si28/SiH4,8/1/7H1;CuO20g model uses
actualCu64 from8/practical1/127,O16 from8/1/7,C12 from8/5/29→3gC/16gCu.
Bookheat412/572 used onlyasexplicitgivenmathmodels,notexperimentalenthalpy.
No COCl2productionconditions,physicalgas/CS2/cyanogen/fluorination/acid/heat/
electricityprotocol or clinical/field/fire certificate. Neutralformula/equation,
numeric andMCQ/short commonassessment contract unchanged;no newsolver/AI.

Strict earlier-grade citation support added to Chemistry validator. Context must
be teaching record in earliergrade andalreadyvalidated importer manifestprefix.
Standalonevalidation checks referencedindexedlesson digest/review andvalidates
it. Eachref retains citedbookSHA/file/title/authors/year/topic/page/region;
grade7left/right mappings preserved. Futuregrade/unreviewed/blocked/container
contexts rejected. Samebookordering/chapterprefix/review/heldfact guards intact.
22 new structural/forgery/spread/index tests pass. REQUIREMENTS andASSESSMENT
contract updated. Existing138 lesson bytes/learning/XP/progress untouched.

96 editorial scopes plus one scientific blocker remain;allreadyfalse. Newholds:
H2Sinsolubility/universalselectivity,wateralpha/allweak-weakfullyhydrolyze,
FeIIIcarbonatebalance/Sbproductidentity/conductancezero,C2p6diagram/fullerenecount,
charcoalpurity/allphase/currentcoal/medicaladsorption/unlimitedheat/fireclaims.
No silentmemoryrepair;five textbook identities/all817 pages audited.

FinalfullChemistry991 passed,1 opt-in PG skip,1existingwarning/436.59s.
Finaltarget75/10.61s includes22 earlier-source plus53batchtests. Initialtarget
74pass/1fail was wrong testexpectation invalid_answer forSIH4 (a validS/I/H
formula withwrong composition);assertioncorrected toincorrect,graderunchanged.
First correctedtarget75/9.71s,initialfull991/521.05s precededfinalcopyspacing.
CriticalRuff/diffpass;all138 baseline hashes/original§1 unchanged.

FinalFlutter518/87s,analysisnoissues/6.2s;two320×568/200%widgets4s.
Sixfinalcaptures inspected:darkSiH4/light71,5feedback,currentgrade9source47/
51,53 andearliergrade8source110/105. Actualgrade8filename/bibliography and
locators shown separately;scroll/pinnedcontinuation preserved. Initialwidgets
2/5s,full518/86s,analysis64s precededfinalremainingword/unitspacing polish.
No runtimeUIchange/native/IME/TalkBack/whole-backend certificate.

Historical143draftQA preserved. Freshbatch28final sandbox compared138content
SHAs,copied only138exactbaseline syntheticprogressrows/2760XP read-only,
then124actualHTTP answers/once-only100XP→143completions/2860XP. Comma/dot
71,5/71.5 andscientific1.71666667e5/171666.667 replayidentical;grade7/8
catalogs unchanged,rubricsprivate,six fixtures sanitized. Current143r1 immutable.
Current sandboxilm-ai-chemistry-batch28-final-qa,loopback8903,ownPID27960;
verifyfullcommand beforestop,private definesstaythere. Older8902draft stopped
ownPID24440 andpreservedhistorical. No actualusers/production/main/otherbranch,
PDF/OCR/fulltext/tokenpush or independentteacher signoff.

Next5:grade9 §11–15,original53–top74. All53–74 read;62–77 renderedprivately.
Notes .local/grade9_batch29_source_notes.md. Reviewbeforeauthoring:HCO3wrong
charge54,hydrate11.44/4.28ambiguous56,2.74versus2.47and20.4Vmtypos59/60,
cave/clinicalsafety,Si phase/density/acid-subject/polysilaneuniversals,cement
450C,crystalsodaearlyround146/limestone.953,densitythreshold500/metalloid/
currentresourcerank universals. Exactclearbookmodels only,no externalrepair.
