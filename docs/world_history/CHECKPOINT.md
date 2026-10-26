# Jahon tarixi continuation checkpoint — batch01

2026-10-26. **Task incomplete. Continue autonomously through grade11.**

## Exact progress

- 219 teaching units; **6 reviewed local-preview lessons;213 remain**.
- Last ready: grade6§6 “Nil vodiysi va uning aholisi”, original printed/PDF28–31.
- Keys: `world-history-6-p01-r1` through `world-history-6-p06-r1`.
- 55 cards,92 reviewed facts,39 MCQ,19 objective FRQ,6 self/teacher activities.
- 961 pages decoded/rendered; every original image inspected for feature presence.
  Bibliography/contents and216 body headings cross-checked. No blanket fact approval.
- 219 units =216 numbered blocks plus grade6 conclusion/final review and grade8
  conclusion; by grade46/44/33/41/26/29. Original26 chapters and ancillary links kept.
- `world_history_lessons.json` is the sole import allowlist. No glob-based import.
  Whole-book course-ready flags remain false. No production/course-complete claim.

## Sources and isolation

- User originals: `C:/Users/Page/Desktop/Jaxon-Tarixi/`.
- Exact copies: `../ilm-ai-world-history-sources/`; six pinned SHA identities.
- Private images/text/OCR: `.local/source-review/`; no raw textbook data in Git.
- Grade9 is scanned; OCR is locator only, never fact approval.
- Worktrees: `ilm-ai-world-history`, `ilm-ai-flutter-world-history`, each on
  `feat/world-history-curriculum`. Other subject/UI worktrees unchanged.
- Baselines: backend9b37213, Flutter0312ff3. Initial history82b115d / Flutter8c3f1d1;
  completed catalogue backend720c279 was pushed. Latest batch commit: branch log.
- 674 existing lesson files plus13 runtime files remain byte-for-byte pinned.
- No real-user/production DB, main merge, deploy, AI Tutor/Explain/translation.

## Implementation and measured QA

- Isolated common-v2 API `/preview/world_history/v2`, immutable explicit importer,
  separate tables, shared authenticated account/session/event contract.
- Session kind `history_assessment_v2` fits existing VARCHAR(24); no schema change.
- Ownership/snapshot/expiry/order/replay,60% completion, once-only20XP tested.
- Separate Flutter debug entry, six grades, original chapter expansion/bibliography,
  source sheets, Ilmo, theory, MCQ, typed FRQ, shared feedback/results and resume.
- Full backend first-lesson baseline: **2569 passed,4 skipped**, all71 files,
  four isolated UTF-8 subprocess shards; frozen inputs preserved.
- Current six-lesson targeted suite: **88 passed**.
- Real isolated PostgreSQL: passed parallel completion and six sequential lessons,
 120XP once only. Broad-suite opt-in skips are not called passes.
- Actual loopback HTTP:6 catalogues,58 answers, prerequisites/replay and once-only
 120XP; synthetic account only. Public fixtures contain no token/private key.
- Flutter current full suite632 passed; six-lesson targeted23 passed; full
  analysis0 issues. Exact measured results: QA_REPORT.md.
- Windows subprocess Unicode failures were fixed with `PYTHONUTF8=1`, without
  Biology edits. Use that setting in later backend QA.
- Screenshots are real Flutter widget renders, not native Android. Independent
  teacher/native IME/TalkBack/full2026–2027 equivalence remain unperformed.

## Source decisions

- Social/gender stages, religion-origin and burial/ritual meanings are attributed
  textbook interpretations; not automatically graded universal historical truths.
- Original21 reads40–12, matching12/18. Earlier40–19 suspicion was a false alarm,
  explicitly retracted in SOURCE_REVIEW.md; no textbook erratum.
- Copper-zinc=bronze, exact1500°C, world-first/oldest priorities, exact modern Nile
  length and unqualified Menes/3000 first-pharaoh keys are withheld.
- Original29 map legend read; historical scope preserved, no PDF map republished.
- Grade11 UN body109/111 remains unresolved; no accepted key. “Today” claims keep
 2018 publication scope. Preserve all open review records.

## Next exact work

1. Finish/persist batch01 QA/Git checkpoint if not already in latest branch log.
   Commit/push only the two history feature branches.
2. Continue **grade6§7 “Qadimgi Misr”**, starting original page32. Confirm final
   boundary from catalogue and original images. Page32 read; no§7 lesson authored.
   Continue§8 onward in5–10 lesson batches through the end of grade11.
3. Reuse common-v2 and mandatory source/fact/per-question-target validators.
   Inspect each original image/map legend, not merely OCR/embedded text.
4. Shared pages require `below_topic_heading` or `above_next_heading`; no adjacent
   paragraph facts. Objective aliases are question-specific. Complex writing is
   self/teacher review, without automatic correctness/score/XP.
5. Update exact counts/review, backend/Flutter and local HTTP/PG QA, commit/push,
   continue without routine permission. Never announce all219 done prematurely.

Private authoring helpers: `.local/`. **Do not rerun** one-time
`author_history_first.py`, `integrate_history_batch01.py`, or old initial catalogue
builders: they could reset the current allowlist. Update future helper review
output to include `approved_answer_targets` and checked activity targets.
Public `finalize_world_history_catalog.py` preserves numbered-unit readiness.

Private QA: `../ilm-ai-world-history-local-qa/` (SQLite server8916),
`.local/history-pg-cluster/` (dedicated loopback PostgreSQL55446). Synthetic data
only; no DB/log/defines/token in Git. Do not touch other subjects' servers/clusters.
