# ILM AI — Jahon tarixi 6–11

2026-10-26. Work in progress on separate backend and Flutter
`feat/world-history-curriculum` worktrees. The complete original user instruction
is preserved in [REQUIREMENTS_UZ.md](REQUIREMENTS_UZ.md); all five attached copies
had SHA-256 `1fc780611965fc472d3314c9f96a2e00ff516a56d06107cb49d9886567e30de3`.

## Measured source coverage

| Grade | Year | PDF pages | Numbered topic blocks | Printed number labels |
| --- | ---: | ---: | ---: | ---: |
| 6 | 2017 | 192 | 44 | 44 |
| 7 | 2017 | 161 | 44 | 44 |
| 8 | 2019 | 160 | 32 | 32 |
| 9 | 2019 | 160 | 41 | 41 |
| 10 | 2017 | 144 | 26 | 29 |
| 11 | 2018 | 144 | 29 | 29 |
| Total | | 961 | 216 | 219 |

These are numbered source blocks. The completed ancillary/activity inventory
defines **219 teaching units**: grades6–11 have 46/44/33/41/26/29 respectively.
The full ordered [course map](COURSE_MAP.md) records every unit and supporting
source record; [page feature audit](PAGE_FEATURE_AUDIT.md) summarizes all961
original images. This inventory does not approve historical claims or lessons.
There are 26 explicitly named source chapters; grade 10 has a flat contents list.
Do not invent chapter headings or split its combined 7–8, 15–16, 19–20 source
topics merely to increase the count.

All 961 pages decoded. Title/copyright and contents images were inspected for
every book. All 216 numbered body headings were cross-checked: embedded text for
grades 6/7/8/10/11 and original scanned image regions for grade 9. Grade 9 has no
usable text layer; OCR is an unverified locator, never an approval.

**Reviewed local-preview lessons:105/219; remaining:114.** Grade6 has44 numbered paragraphs plus conclusion and final review:361 cards,
271 MCQ,175 objective FRQ and46 self/teacher-review activities. Grade7§1–44
add314 cards,298 MCQ and176 objective FRQ; all44 units are present in local
preview. Its48-entry chronology reference is scoped in GRADE7_REFERENCE_REVIEW.md.
Grade8§1–15 add118 cards,127 MCQ and59 objective FRQ. Grade8 has18 units left;
grades9–11 have41/26/29 left, for114 remaining overall. The isolated API and
Flutter debug entrypoint exist; nothing has been released to production. All
book course-ready flags remain false. See [checkpoint](CHECKPOINT.md), [source review](SOURCE_REVIEW.md),
[architecture](ARCHITECTURE.md) and [QA](QA_REPORT.md).

## Files and isolation

Verified private originals: `../ilm-ai-world-history-sources/`. User's updated
input location: `C:/Users/Page/Desktop/Jaxon-Tarixi/`. Exact original hashes match
the first inventory from the earlier folder. Originals, extracted text, OCR,
source renders, logs, databases and credentials must stay outside Git.

Public machine-readable catalogues are under `scripts/curriculum/world_history/`.
No `ozbekiston_tarixi` course is being authored. Central Asian/O‘zbekiston topics
already inside the supplied grade-6 book remain within `jahon_tarixi`.
