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
