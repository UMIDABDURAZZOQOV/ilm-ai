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
