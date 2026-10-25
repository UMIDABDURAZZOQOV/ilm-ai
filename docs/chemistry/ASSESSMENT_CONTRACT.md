# Local Chemistry assessment contract

The existing ILM AI v2 flow remains theory → ordered assessments → source-linked
feedback → server result/XP/progress. This namespace is a local, opt-in preview;
normal Biology/Physics endpoints and production startup do not enable it.

| response_kind | Input | Authoritative check |
| --- | --- | --- |
| concept_selection | allowed choice_id | Private reviewed option ID |
| short_text | value, at most80 characters | Bounded Uzbek spelling normalisation and reviewed aliases; no fuzzy grading |
| numeric_value | value; unit fixed in prompt | Exact Decimal value, comma/dot/e notation; no expression evaluation or silent unit conversion |
| chemical_formula | value | Case-sensitive finite formula grammar and reviewed formula/aliases; subscripts accepted |
| chemical_equation | value | Reviewed species on each side, per-element atom balance and reviewed coefficient ratio |

Formula/equation grammar is a notation checker, not a chemical knowledge source.
It contains no periodic table, reaction generation or imported scientific facts.
Correct identities, products and explanations must come from individually
reviewed textbook facts. Structural-isomer, charge, isotope and ionic-equation
input contracts are not silently inferred from this introductory grammar.

## Bounds and alternatives

- At most80 input characters, three nested parenthesis levels, individual
  indices/coefficients1–999 and eight terms per equation side. Zero, fractional
  coefficients, invalid parentheses, scripts and expressions fail format checks.
- Only ordinary digits and explicitly translated **subscript** digits are used
  for atom counts. Superscript charges are not folded into indices. Case matters:
  a different capitalisation never becomes the expected element automatically.
- Formula aliases must be explicitly reviewed and have the same atom counts.
  Same composition alone does not make an unlisted structural isomer correct.
- Equation `=`, `->` and `→`, ordinary spaces, reordered terms and proportional
  integer coefficients represent the same answer for replay. Reversing the
  reaction or changing an index changes the submitted chemistry.
- Format errors return422 with authored input feedback and leave the answer
  unconsumed. Wrong species or unbalanced atoms return submitted-answer feedback
  and the reviewed solution; changing that answer later conflicts as before.
- Canonical replay fingerprints preserve exact numbers without context rounding.
  XP is awarded transactionally once; an equivalent replay never awards more.

## Evidence and frontend

Every card, formula, example, question and solution references taught fact IDs,
reviewed page/region images and the pinned source PDF identity. Expected keys
must be listed in those facts and pass their deterministic grader. A reviewed
equation that is itself unbalanced cannot be imported. Conflicting textbook
percentages are review material, not authoritative answer keys.

Flutter sends the exact typed string and performs no correctness/stoichiometry
calculation. It supports a full keyboard for case, parentheses, e and arrows,
uses the common feedback/result/exit components, and refuses an attempt returned
for a different requested lesson. Public fixtures are captured from the actual
isolated backend; private specs and tokens never enter frontend start payloads.


## Explicit source context (batch05)

Optional source_context_ids refer to earlier teaching records in the same book,
or explicitly reviewed,already-indexed teaching records in an earlier grade
(batch28). Each earlier-grade reference retains its own book identity,reviewed
page and original spread mapping. source_activity_ids only attach same-chapter review anchors to the final
preceding teaching lesson. Every source ref and image evidence retains its own
topic ID/title, paragraph or null review number, printed page and spread side.
Future/unknown/duplicate/undeclared/misidentified contexts fail validation.
Known source holds cannot be bypassed by citing them in another lesson.

Earlier-grade contexts must already be validated in the importer manifest prefix.
Standalone validation checks the referenced lesson digest and review and validates
that lesson. Grade strictly decreases across such book links;future grades,
unreviewed records and cross-book chapter/review containers are rejected.
Per-ref SHA,file,title,authors,year,topic,printed/PDF page and region are checked
against the cited book. Existing same-book ordering and chapter-prefix limits,
source holds,private rubrics and all learning/XP/progress rules remain in force.


## Grade selection and portable display (batch16)

The isolated catalog accepts grade7–11 and lists only grades with an imported
first lesson. Flutter sends the selected grade,validates the list and rejects a
mismatched catalog. The picker is absent during attempts;existing cancellation,
account/origin/lesson storage and once-only XP semantics remain unchanged.

Chemistry display maps Unicode subscript digits to ordinary digits and raised
runs to explicit ^(...) strings;arrows render as ->. This is presentation only,
not scientific interpretation or new accepted input. API/manifests/typed strings
and correctness comparisons remain original. Shared source-button separator is
optional;its default and Biology behaviour stay unchanged.


## Exact chapter-preface context (batch18)

source_context_ids may include the current chapter's actual intro anchor only
when that chapter starts before its first teaching paragraph. Citations are
limited to pages before that paragraph;on its first page both ref and image
review must declare before_first_teaching_heading. Later chapter pages,other
chapters,chapter-as-review and false paragraph numbers fail closed. Actual
chapter title/null paragraph is public. This is evidence reuse,not a new lesson,
new response kind or permission to cite arbitrary pages in the chapter range.


## Numeric minus spelling (batch19)

Only numeric_value accepts U+2212 mathematical minus as ASCII minus before the
existing Decimal grammar. The raw80 bound is checked first. Number value,unit,
precision and reference answers are unchanged. Both spellings have the same
canonical replay fingerprint. Units,arithmetic expressions,ionic notation,
superscript minus and en dash are not accepted by this normalization.


## Portable equilibrium display (batch22)

The Chemistry display-only adapter spells source⇌ as ASCII <=> when presenting
theory/prompts/feedback. Bundled-font captures showed a missing glyph. Raw API
source text and typed answers are unchanged;the finite equation grader has no
new reversible-arrow/equilibrium semantics. A material-balancing question still
requires the existing accepted= or-> syntax and does not compute equilibrium.
