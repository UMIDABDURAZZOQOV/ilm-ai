# Jahon tarixi continuation checkpoint — batch10

2026-10-27. **Task incomplete. Continue autonomously through grade11.**

## Exact progress

- 219 teaching units; **51 reviewed local-preview lessons;168 remain**.
- Last ready: grade7§5 “Muqaddas Rim imperiyasi”,26–29 above§6.
- Keys: `world-history-6-p01-r1` through `world-history-6-p46-r1`, plus grade7
  `world-history-7-p01-r1` through `world-history-7-p05-r1`.
- 400 cards,755 reviewed fact records,303 MCQ,195 objective FRQ,51 self/teacher activities.
- Grade6 has46/46 units ready:44 numbered paragraphs plus conclusion/final review.
  Twelve fact records in the final review reuse exact previously reviewed knowledge;
  total records are not a count of unique historical facts.
- Grade7 has5/44 units ready;39 remain in this grade. Grades8–11 remain unimplemented.
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
- Current fifty-one-unit targeted suite: **178 passed in792.00s**.
- Real isolated PostgreSQL: **1 passed in51.22s**, parallel completion and51
  sequential units/1020XP once only. Broad-suite opt-in skips are not passes.
- Actual loopback HTTP:6 catalogues,498 answers, prerequisites/replay and once-only
  1020XP; fresh synthetic account only. No existing learner reset.
- Current Flutter: **118 history widgets passed in01:32**, **727 full tests passed in04:21**, full analysis **0 issues in85.4s**. Exact scope: QA_REPORT.md.
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
- §7 Tutmos II campaign priority remains uncorroborated and not an automatic key.
- §8–11 divine actions/afterlife/Gilgamesh/Tofon are attributed beliefs or stories.
  Question keys test names and narrative comprehension, not supernatural truth.
- §10 fixed alphabet count/first-calendar priority, §11 first-standing-army
  priority and universal mino weight are withheld from automatic grading.
- Original44 map labels and influence hatching reviewed; no invented trade route.
- §12 first-law/prior-laws tension, universal legal equality and Misr annexation
  attribution withheld from keys. Severe punishments described non-graphically.
- §13 Xattusa/Xatusa are explicit same-book spellings; Teyshebani cause withheld.
- §14 shoh-yo‘li exact endpoints are withheld;522 keys accession only. Maps53/57
  retain their exact legend era, not current borders.
- §15 caste vocabulary is the book's simplified schema, with no human-worth
  ranking or learner caste-assignment. Divine caste origin is belief, not science.
- §16 calendar/innovation priority, literal Gautama legend and universal “godless
  religion” definitions are withheld from automatic keys. Xuanxe68 belongs to§17.
- §17 original69 Chjou3-ming line conflicts with71 summary2-ming; no invented
  corrected date or contradictory chronology key. Rice-origin/tea-health held.
- §18 seismograph prediction wording is separate, unassessed and absent from
  automatic feedback.246 unification/title timing and exact wall metrics held.
- §19 Central Asian material retained here; no new ozbekiston_tarixi course,
  exclusive modern descent/territory or exact relative-age arithmetic.
- §20 Avesto/Zand/ossuary names assessed; astrology, revelation, compilation
  priority and moral/religious agreement not automatic facts or scored opinions.
- §21 exact mountain fraction/collapse model held; Olimp and Olimpiya distinct.
- §22 citizenship/education and Sparta universals scoped; original90 Periek/
  periyek finite spellings accepted, not Ilotlar aliases.
- §23 original92 main VIII–VI versus summary VIII–VII mismatch and VIII-century/
 24-letter precision withheld; outsider label attributed, no invented date fix.
- §24 instant equal democracy/office access and strateg-as-council-head held;
  institution diagram not a validated hierarchy. Gender/metek exclusions explicit.
- §25 runner/death/42km, total300, exact ship/speed and definitive449 endpoint not
  automatic facts; map route-colour legend not invented.
- §26 tactics/portrait/voice anecdote held; broad dependency not uniform annexation,
  treaty terms not universal compliance. No ethnic superiority or reenactment.
- §27 Olimp/Olimpiya and394/torch continuity precision held;776BCE to1896CE
  ordering verified without year0. §28 horse-episode/Iliad link not approved.
- §29 separate Aristotel/Arastu, Platon/Aflotun and Sokrat/Suqrot pairs; burning
  mirrors/philosophical cosmology not literal modern science.
- §30 every deity-table row checked; narrative/table comprehension only, no
  automatic judgment on supernatural truth or personal belief.
- §31 Gerodot, Behistun and Poliyen accounts distinct; Poliyen era and third-year/
 519 timing unresolved, no invented date correction or definitive campaign result.
- §32 campaigns and casualty/period precision scoped; §33 successor-state and
  succession schema not immediate exhaustive chronology.
- §34 calendar original134 bodyCEI/recallBCEI mismatch explicit and ungraded.
  Qang‘yuy state not a catch-all capital alias; no never-conquered Ershi key.
- §35 script genealogy/first-named coin/chess attribution held; §36 network
  distance approximate, naming association not global-first priority.
- §37 founding narrative attributed; §38 constitutional/office universals held.
- §39 ritual/deity vocabulary is belief comprehension, not supernatural proof.
- §40 army eras and campaign precision scoped; no invented route map.
- §41 slave/tenant status not human worth, thumb gestures and74 start not keys.
- §42 Caesar title/Avgust29BCE precision held; no external correction or absent
  battle name. §43 outsider labels attributed;476 is Western/course periodization.
- §44 concrete priority, school/bath universals and supernatural narratives not
  automatic facts;313 permission distinct from sole state religion.
- Conclusion values self/teacher-only. Final-review184 is a locator, not meanings;
  nine exact earlier units/twelve facts supply independently pinned definitions.
- Grade7§1 broad Europe/Asia land/climate models attributed; no invented map.
- Grade7§2 Allod16 Greek versus17 Latin question unresolved; no etymology key
  or invented warrior-execution story. §3 dynasty-founder/epic details held.
- Grade7§4 Ambrosiy/Artur not interchangeable identity; Alfred reign/peace date
  precision and whole-island partition not keys.
- Grade7§5 Gerbert/SilvestrIII(999–1003) ordinal/date unresolved and not taught
  as a verified identity; no outside correction. OttonI distinct fromOttonIII.
- Grade11 UN body109/111 remains unresolved; no accepted key. “Today” claims keep
 2018 publication scope. Preserve all open review records.

## Next exact work

1. Finish/persist batch10 QA/Git checkpoint if not already in latest branch log.
   Commit/push only the two history feature branches.
2. Continue batch11 **grade7§6–10**, starting§6 on original29 below its heading.
   Original3–33 read;§1–5 authored/published, private§6 draft validated
   (15 facts/6 cards/10 questions). Next image34 for§7.
   No§6+ indexed/imported. Keep grade selection and progress independent;
   author in book order through grade11.
3. Reuse common-v2 and mandatory source/fact/per-question-target validators.
   Inspect each original image/map legend, not merely OCR/embedded text.
4. Shared pages require `below_topic_heading` or `above_next_heading`; no adjacent
   paragraph facts. Objective aliases are question-specific. Complex writing is
   self/teacher review, without automatic correctness/score/XP.
5. Update exact counts/review, backend/Flutter and local HTTP/PG QA, commit/push,
   continue without routine permission. Never announce all219 done prematurely.

Private authoring helpers: `.local/`. **Do not rerun** one-time
`author_history_first.py`, `integrate_history_batch01.py`, `integrate_history_batch02.py`,
`integrate_history_batch03.py`, `integrate_history_batch04.py`, `integrate_history_batch05.py`, `integrate_history_batch06.py`, `integrate_history_batch07.py`, `integrate_history_batch08.py`, `integrate_history_batch09.py`, `integrate_history_batch10.py`,
`finalize_unpublished_history14.py`, or old initial catalogue
builders: they could reset the current allowlist. Update future helper review
output to include `approved_answer_targets` and checked activity targets.
Public `finalize_world_history_catalog.py` preserves explicitly recorded numbered
and ancillary readiness/review; never approves a fact by page inventory.

Private QA: `../ilm-ai-world-history-local-qa/` (SQLite server8916),
`.local/history-pg-cluster/` (dedicated loopback PostgreSQL55446). Synthetic data
only; no DB/log/defines/token in Git. Do not touch other subjects' servers/clusters.
