# Android integrated beta — active work

User request: attachment 8f7ea76e-a400-4dbc-aef8-bde631a69d0d, read in full.
Goal: normal main.dart/onboarding/SubjectHomeScreen/five-tab app, all 1,381
reviewed units in the same grade-filtered catalogue and learning path. No QA hub
or separate subject preview screens in the learner flow. No production release.

## Git evidence (2026-10-29)

QA checkpoints exist locally: Flutter 4cd3a0a8fc07fc1215d961d9271c40e24d831249;
backend 0c7a80e9c5ced3bfc09622997ad9f287d19b3f6a. Both GitHub commit API lookups
returned HTTP422 “No commit found”; ls-remote also advertised no QA branch.
Do not claim they were pushed. All five source feature heads match the previous
verified inputs on GitHub. UI improvements are already ancestors of Flutter QA.

New independent worktrees: ilm-ai-beta and ilm-ai-flutter-beta; branch in both:
beta/android-integrated-five-subjects. QA worktrees, original feature branches,
main, production backend and real user databases are unchanged.

## Implementation

1. Add an isolated /beta API adapter over existing source-validated Biology v1
   and Physics/Chemistry/two History v2 runtimes. Preserve source/grading/XP/
   prerequisite gates and tables; no fabricated curriculum or publication flag.
2. Same normal subject/grade/path UI for all subjects. Math and native language
   remain disabled with “coming soon”. Chapter names/order from source catalogues.
3. One shared v2 lesson engine using existing validated repositories and subject
   answer editors. Page through theory/formulas/worked examples; preserve all
   content and source references. Reuse branded lesson chrome/feedback. Biology
   keeps its v1 engine; no invented Biology FRQ.
4. Aggregate all five progress models into the existing profile and activity UI.
   Shared account XP/streak and existing preferences/auth remain authoritative.
5. main.dart compiled with explicit beta flag, unique package/name/callback.
   No QA homepage or pairing-code login. Google configuration remains server-side;
   local-only beta test login is separately gated and never enabled for HTTPS
   staging. No secrets are compiled into APK.
6. User confirmed no HTTPS staging or Google credentials exist and requested a
   local beta plus setup requirements. See LOCAL_BETA.md. No deployment performed.
7. Analyze, Flutter tests, API/source/isolation tests, real local PostgreSQL,
   debug APK, device smoke tests where attached. Record actual evidence and open
   acceptance items; do not call beta production-ready.

## Open external dependencies

- Dedicated HTTPS staging and Google OAuth are not configured, as confirmed by
  the user. Local beta authentication is explicitly permitted instead.
- Need check ADB device availability again for real handset acceptance.
- PostgreSQL integration passed on a new owned cluster, port 55461, database
  world_history_staging_integrated_beta, disposable test schemas. Credentials are
  outside Git in ilm-ai-beta-pg-local; original subject clusters were not changed.

Update this file with implementation checkpoints and precise commands after edits.

## Implemented checkpoint

- Normal catalogue/path adapters enumerate all 1,381 reviewed units in source
  order. Grade filters and unready subjects are tested. No scientific data edited.
- Existing graders/editors and source/preview gates retained; server-only grading.
- One branded v2 teaching/exercise controller; Biology remains the original v1.
- Runtime-generated local identity, existing access/refresh tokens and normal
  onboarding/preferences/profile. No code/token embedded in the APK.
- 16 real SQLite/PostgreSQL API tests passed, including all five graders, 50
  submitted answers, 80 shared XP, duplicate completion, resume and ownership.
- 27 Flutter beta lesson/onboarding tests, 3 normal app-shell/login/path tests
  and 2 Android configuration tests passed, including 360px width and 200% text
  for the v2 lesson screens. Completed-node review opens a fresh attempt while
  unfinished review drafts remain resumable.
- Full regressions/analyzer/APK verification recorded in ACCEPTANCE.md when done.
