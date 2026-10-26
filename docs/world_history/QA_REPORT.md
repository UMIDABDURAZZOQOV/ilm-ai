# Jahon tarixi QA — initial source foundation

2026-10-26. These are initial inventory/algorithm tests, not final course QA.

- Six supplied books: SHA-256 verified, 961 pages actually decoded and privately
  rendered. Grade9's 160 pages have OCR locator files; no useful text layer.
- Bibliography and contents verified from original page images for all six.
  All numbered body headings cross-checked; factual body review remains pending.
- First test run: **26 passed in 1.04 s** for source identity/order/combined units,
  prerequisite protection, unreviewed catalogue gating, BCE/CE/century arithmetic.
- Critical Ruff (`F821,F822,E9`) passed for new source/chronology modules/scripts.
- Final initial-stage run: **30 passed in 4.56 s**, including all 961 render
  inventory entries, all 687 protected lesson/runtime hashes, rejected forged
  readiness flags and malformed-era input. No history content was imported.
- No history runtime/API/PostgreSQL/native Android tests yet: those components
  do not exist. No production DB or real user data accessed.
- Flutter dependencies resolved from the existing offline cache; no dependency
  upgrade was requested. Analysis in the new worktree: **0 issues, 252.3 s**.
  No Flutter implementation changed, so no new history widget pass is claimed.

Existing Chemistry's final 1,908 backend / 609 Flutter / 3 PostgreSQL results are
historical baseline evidence, **not new Jahon tarixi test results**.

## Completed catalogue checkpoint, 2026-10-26

- All961 original page images inspected for feature presence/layout. Every page
  has a digest-bound manual observation record and candidate parent binding.
- Complete219-unit teaching map: 46/44/33/41/26/29 by grade. Supporting records
  explicitly retained. No historical fact approved merely by catalogue status.
- **46 source/chronology/preservation tests passed in4.00s**. Mutations include
  forged render hash, duplicate/bool page, unknown/duplicate feature, missing
  heading/reference/unit/binding, wrong prerequisite/location/parent link.
- All687 protected files matched their baseline SHA-256 values.
- Critical Ruff (`F821,F822,E9`) and `git diff --check` passed.
- No history executable lesson, runtime, UI or DB import at this checkpoint.

## Batch01 — grade6§1–6, 2026-10-26

**Local preview only; the219-unit course remains incomplete.** Six lessons,
55 original theory cards,92 fact records,39 MCQ,19 objective FRQ and6 ungraded
self/teacher-review activities.213 units remain.

| Check | Measured result | Scope |
| --- | --- | --- |
| Full backend regression |2569 passed,4 skipped;71 files;2462.19s wall | First-lesson implementation snapshot, four isolated UTF-8 subprocess shards; frozen inputs preserved |
| Current history/source/preservation tests |88 passed in100.73s | All6 current manifests, exact source regions/digests, question-specific targets/aliases, activities, immutable API/progress/XP |
| Actual PostgreSQL |1 passed | Dedicated new history staging cluster; immutable import, snapshots, parallel first completion, all6 sequential lessons/120XP, old synthetic account preserved |
| Actual loopback HTTP |6 grade catalogues,58 answers,120XP | Prerequisites, auth, private-key exclusion, replay, once-only completion; synthetic users only |
| Full Flutter regression |632 passed,07:44 | Current six-lesson implementation and all existing UI/subject tests |
| Targeted history widgets |23 passed,00:17 | Real API fixtures for§1–6, MCQ/FRQ, source sheet, resume/account switch, lost request, 320×568/200%, light/dark, UZ/RU/EN |
| Full Flutter analysis |0 issues,183.2s | Entire history Flutter worktree |
| Preservation |687 SHA-256 pins matched |406 Biology +268 Chemistry lesson files and13 existing backend runtime/model/router files |
| Critical Ruff / Git whitespace |Passed | New history code and diffs |

The broad backend run's4 opt-in PostgreSQL skips are **not passes**. History's
real PostgreSQL scenario ran separately and passed. Initial broad-run Windows
subprocess decoding failures were environmental: both Biology tests passed with
`PYTHONUTF8=1`; the full UTF-8 rerun then passed without editing Biology.

Real PostgreSQL caught an overlong session kind; it was shortened to
`history_assessment_v2`, leaving the existing VARCHAR(24) schema intact.
The private HTTP sandbox is intentionally SQLite; its legacy DB bootstrap message
does not describe the separate real PostgreSQL test.

Inspected widget renders include path/bibliography, first theory, correct/wrong
feedback, scrollable explanation at200%, FRQ flow and self-review. Source PDF/map
images were not bundled. Screenshots/logs/DBs/tokens stay private. No actual Android,
IME/TalkBack, independent history-teacher sign-off or complete2026–2027 outcome
equivalence is claimed. No production/main/deploy/real-user operation occurred.
