# Reviewed textbook errata

User instruction: 2026-10-25. An affected claim may be corrected after comparing
the original page with other supplied textbook evidence. Other verified content
continues. A correction is neither an outside science source nor a waiver of
source validation. The original PDF is never changed or republished.

## Grade9 §40, printed/PDF186

Original issue `ch9-p40-page186-configuration-conflict` is retained in the source
catalogue. Its sample places Be, Cl and Ca together in groupII, and the following
Cl prose omits3p5. The displayed full Cl configuration on that same page includes
3p5. The user explicitly authorized this correction and a tested mechanism.

The original images were compared with:

| Supplied source | Evidence used |
| --- | --- |
| Grade9 §1, page9 | Main-subgroup outer-electron/group relationship, with its stated scope |
| Grade9 §1, page11 | Cl row: groupVII, Z17, full1s2 2s2 2p6 3s2 3p5 |
| Grade8 §23, page96 | Cl explicitly in seventh main subgroup; Z17 and configuration |
| Grade8 §11, page49 | Be: Z4, full1s2 2s2 |
| Grade8 §12, page52 | Ca: Z20, full1s2 2s2 2p6 3s2 3p6 4s2 |
| Grade9 §23, page109 | Ca explicitly in second main subgroup; [Ar]4s2 |

Corrected facts: Be and Ca are in main subgroupII (IIA); Cl is in main
subgroupVII (VIIA). Their outer configurations are2s2,4s2 and3s2 3p5 respectively.
The user also confirmed modern group17 for Cl. Assessed group labels in this
erratum use the supplied books' I–VIII main-subgroup notation; Z17 is kept
distinct from a group-label question.

## Controlled validation

`scripts/curriculum/chemistry/chemistry_reviewed_errata.json` contains one
explicit erratum. `services/chemistry_errata.py` pins its bytes by SHA-256 and
allows only its known issue, paragraph, page, correction IDs, finite verified
values and seven exact evidence locations. Each evidence record preserves its
own textbook identity, bibliography, PDF SHA and original-page image digest.
An arbitrary approval flag, unknown erratum, new file, future source or OCR-only
proof cannot resolve a source hold.

The catalogue keeps the original issue ID and location, records its original
open status, and links `resolved_by_reviewed_erratum` to this specific artifact.
Removing the history or linking an incomplete/unknown resolution still fails.

An authored fact citing affected page186 must declare `reviewed_erratum_ids`
and `reviewed_erratum_claim_ids`, retain the original page and the specific
corroborating pages, and match their pinned image evidence. Its verified values
must stay within the reviewed correction. Each MCQ/FRQ using such a fact also
declares exactly one `reviewed_erratum_claim_id`; its correct answer and aliases
are checked against that claim. This prevents borrowing an unrelated numeric
value from another corrected claim. These are private review metadata, not a
new response type, client-side grading rule or learning mechanism.

Unresolved source contradictions continue to fail catalogue/lesson/context
validation. Uncertain facts stay excluded from assessment. Course-ready flags,
independent teacher sign-off, explicit manifest import, immutable attempts,
prerequisites, progress, replay and XP rules remain in force.

The foundation correction itself did not add a lesson. Batch34 subsequently
authored and source/API/UI-validated grade9 §40 within174/268 implemented entries.
See qa_batch34.json for measured checks. Independent teacher sign-off remains
outstanding. No production operation or Biology/Physics mutation occurred.
