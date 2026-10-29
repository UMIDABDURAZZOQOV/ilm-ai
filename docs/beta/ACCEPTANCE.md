# Integrated beta validation evidence

Updated 2026-10-30. Source code is isolated on
`beta/android-integrated-five-subjects`, based on QA 0c7a80e / Flutter 4cd3a0a.

## Automated evidence

- `tests/test_integrated_beta.py`: **16 passed** on owned SQLite and PostgreSQL.
  All 1,381 units/source order/grade filters; account ownership, settings/profile,
  real grading in all five subjects, 50 answers and 80 XP, duplicate completion,
  resume, refresh, local gates, callback scheme safety and every teaching section.
- Flutter beta suites + Android configuration: **32 passed**. Four original FRQ
  editors, teaching/formulas/examples/reflections, source links, normal app shell,
  local login/session restore, completed-node review, 360px/200% text and pagination.
- Full normal Flutter suite: **1,304 passed / 1 static Android assertion failed**.
  That inherited assertion expected unrestricted debug cleartext. It was updated
  to require the existing stricter loopback-only network XML. Both Android tests
  then passed in the final 32-test run. No network restriction was relaxed.
- Backend normal regressions: **66 passed**, including all 406 Biology lessons
  and 47 checkpoints, OAuth/PKCE, ownership, reward replay and publication gates.
  A combined invocation also ran the old QA fixture after DB modules had already
  loaded, producing three staging-gate setup errors. The QA fixture requires its
  own fresh Python process; its separate rerun is recorded in the final report.

Logs remain local/ignored: `beta-integrated-final-tests.log`,
`beta-backend-regressions.log`, Flutter `beta-final-ui-tests.log`,
`beta-final-analyze.log`, `beta-full-flutter-tests.log`. Initial errors and reruns
are retained; do not relabel an interrupted or failed run as fully passing.

## Build and handset evidence

The debug build receipt lives beside the APK as `integrated-beta-build.json`.
It records exact Flutter/backend commits, bytes, SHA256, package and entrypoint.
Final handset/build acceptance is recorded in the delivered local report after
installation. ADB now sees Samsung SM-A125F, Android 12, 720×1600, serial
R58NC0JNBXJ. This observation alone is not an installation or smoke-test result.

## Preserved boundaries

Original source runtimes, source curricula/validators and OAuth router have no
diff from the QA checkpoint. Main and subject feature heads are unchanged.
Original Biology worktree contains pre-existing untracked files; they were left
alone. QA checkpoints remain locally available; GitHub API returned 422 for both
QA commits and no QA remote branch was advertised. No push/deployment performed.

No Google credentials/HTTPS host exist, as confirmed by the user. Real Google
login is not verified. This beta uses explicit local-only test authentication.
Biology FRQ is absent; no new scientific content or AI features were introduced.
See LOCAL_BETA.md for setup requirements and remaining staging work.
