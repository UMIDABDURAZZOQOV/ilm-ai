# Final production fixes — active checkpoint, 2026-11-07

## Latest blockers result — local fixes complete, external acceptance open

**NO-GO for production.** This section supersedes the historical checkpoint below.
Functional commits on `qa/final-production-fixes-20261106`:

- Backend `b4e138a31d605cee0e1d2ae4a45068b5ce0da88c`.
- Flutter `ac168c3acbd045f80a275d3297832057590cdae4`.

### Implemented and checked

- Verified account deletion in Settings and a public web page: email OTP,
  explicit consent, persistent rate/attempt limits, transactional owned-data
  removal and token/grant revocation, immutable scrubbed UID tombstones, stale
  write barriers and retryable file cleanup. Paid/financial accounts honestly
  enter operator retention review, not false success. No real account was deleted.
- Flutter cleanup is scoped to the exact deleted UID and secure-session
  generation. Other accounts, ordinary logout, global theme/language and existing
  progress are preserved. Fixed a reproduced Uzbek dialog overflow at 200% text
  with the keyboard visible; buttons now remain in scrollable content.
- Pinned migration0016 and runtime foundation0017 (55 table definitions), with a
  fresh-install-only0011 guard for its missing SAT table. Actual Alembic full-chain
  execution was rehearsed in a fresh loopback PostgreSQL schema, not create_all.
- Explicit five-subject reviewed publication import validates all sources before
  writes, refuses private-grader/content drift and never rewrites user progress.
  Batch catalogue reuse is restricted to one transaction. Fresh import, idempotent
  reimport and synthetic137 XP preservation passed on PostgreSQL.
- Production/staging browser session cookies now require HTTPS. Existing auth,
  preview/source guards and provider quota/fallback rules remain enforced.

See [deletion contract and deployment gate](ACCOUNT_DELETION.md),
[operator sequence](PRODUCTION_DEPLOYMENT_PLAN.md) and
[isolated HTTPS/OAuth setup](HTTPS_STAGING.md).

### Final local command evidence

Counts overlap across commands; do not sum them as unique tests. Logs live in the
sibling `ilm-ai-beta-artifacts` directory.

| Check | Actual result / receipt |
| --- | --- |
| Full Flutter suite before the last responsive dialog fix |1359 passed,20m35s; `blockers-flutter-full-tests-20261107.log`|
| Final deletion widget/repository/auth/storage suite, including the dialog fix |20 passed; `blockers-flutter-deletion-final-20261107.log`|
| Final Flutter analyze |No issues found,234s; `blockers-flutter-analyze-20261107.log`|
| Reviewed-staging Flutter UI/API, mocked HTTPS transport |44 passed; `blockers-reviewed-staging-flutter-20261107.log`|
| Local-Beta Flutter UI/API |44 passed; `blockers-local-beta-flutter-20261107.log`|
| Deletion lifecycle, disposable SQLite and real PostgreSQL schemas |32 passed,262.72s; `blockers-deletion-tests-20261107.log`|
| Additional cached-file-auth runtime rejection, SQLite/PostgreSQL |2 passed,32 deselected; command output|
| Actual Alembic chain +1381 lessons +reimport +XP preservation |1 passed,151.47s; `blockers-postgres-publication-20261107.log`|
| Publication/five-subject/provider regression |5 passed,5 PostgreSQL variants skipped; `blockers-publication-provider-tests-20261107.log`; separate PG evidence above|
| Final config/startup/secure-cookie/email checks |42 passed; command output|
| New/changed lifecycle/import/migration/config Ruff and git diff checks |passed|
| Pure source validation with an intentionally invalid DB URL |406 Biology +975 reviewed lessons,9418 reviewed assessments; no DB access/write; `blockers-publication-dry-validation-20261107.log`|
| Android Beta debug build |success,166.3s; `blockers-beta-apk-build-20261107.log`|

Earlier broad backend regression yielded207 passed/5 skipped/5 fixture errors:
the five Beta fixtures used a disallowed sandbox filename. The guarded test URL
was corrected and all five affected tests passed in the final publication command;
preview restrictions were not weakened. This was not a clean full-backend run.
Initial two Uzbek large-text widget overflow failures were fixed and all20 final
targeted cases passed. The full1359 run preceded that final UI fix; it is not a
claim that a full1367-test command was executed. Real Google/email/provider and
phone benchmarks are not covered by these mocks/synthetic tests.

### New APK and operating state

- `ilm-ai-beta-artifacts/ILM-AI-Beta-1.0.3-code4-ac168c3.apk`:
  **209821062 bytes /200.10MiB**, Flutter source `ac168c3`.
- SHA256 `4854ff1c23282c0f159d55f563b6eb467d4184b481c882854440a12c17ccf2c5`.
- Verified `com.ilmai.app.beta`, `ILM AI Beta`,1.0.3/code4,min24/target36,
  debug flag and APK v2 signature. Launch activity is
  `com.ilmai.ilm_ai_flutter.MainActivity`. ZIP scan found no checked private files
  or NVIDIA/AQ/JWT literal patterns; this is not a guarantee for every secret format.
  Receipt: `blockers-beta-debug-build-20261107.json`. Existing future KGP warnings
  remain; current build succeeded. This is not the final production AAB.
- Local server resumed from backend `b4e138a`, PID3892, loopback8930. Health200,
  17 public API checks passed, all five subjects remain visible for grades5–11.
  Grade5 opens only Biology; actual grade6 availability includes Physics/history.
  No opening grade was guessed. Google is unconfigured; reviewed help fallback
  needs no provider key. Account deletion is deliberately disabled until deployment
  prerequisites are satisfied. Receipt: `blockers-beta-health-final-20261107.json`.
- All46 account/progress table counts and hashes match both before resume and the
  earlier checkpoint. Receipt: `blockers-beta-preservation-final-20261107.json`.
  No authenticated request/answer/reward/account was created by public probes.
  Local SQLite Beta is left running. The separate owned PostgreSQL test cluster
  was gracefully stopped after its tests; it is not the8930 database.
- Fresh ADB list is empty. No new install, phone smoke/upgrade, Android15 layout
  acceptance or profile/release startup/frame benchmark was performed. Never
  uninstall or clear data to work around connectivity.

### External release blockers and next concrete actions

1. Latest read-only production probe at2026-11-07T10:07:32Z: health200, mobile
   auth config/catalogue/all five grade routes404. The187-path OpenAPI inventory
   lacks the mobile contracts but has legacy routes. Exact deployed revision,
   branch/root/start command and schema must be inspected in the hosting dashboard;
   no admin configuration/access was found. Receipt:
   `blockers-production-preflight-handoff-20261107.json`. No production fix was deployed.
2. Provision an approved separate HTTPS origin/PostgreSQL role+database, Google
   Web OAuth client/callback/test users and actual mailbox. Staging config/guards
   are prepared; no hosted service, certificate or live Google acceptance exists.
3. Approve retention/support/backups/third-party lifecycle, persistent storage and
   cleanup worker; accept actual OTP delivery and app/web deletion on synthetic
   staging accounts. Publish matching privacy/Data safety and deletion URL.
   Local implementation/tests do not complete that operator/policy acceptance.
4. Connect an authorized phone for install, session/progress/MCQ/FRQ checks and
   profile/release benchmarks. Verify actual Play-signed1.0.2→1.0.3 upgrade,
   Android15 behavior and compatibility of existing clients without data loss.
5. Only after critical configuration/acceptance, build and inspect the signed
   five-subject production1.0.3/code4 AAB. The older Biology-only AAB is not this
   code. No new final production AAB, provider activation, paid resource, remote
   push, production deployment/migration or Play upload was performed.

Full13-point owner report and safe PowerShell commands:
`ilm-ai-beta-artifacts/BLOCKERS_FIX_HANDOFF_20261107.md`.

## Historical checkpoint before the latest blockers implementation

The following older test counts, APK, process and pending engineering tasks are
retained as history and are superseded by the latest section above.

**NO-GO. This is not a completed production release.** Work is isolated on
`qa/final-production-fixes-20261106` in backend and Flutter Beta worktrees.
Main/subject branches, production users/database/deployment and Play Console
were not modified. Owner confirmed existing package `com.ilmai.app`, highest
Play code3 and permission to prepare1.0.3/code4; no permission to upload/deploy.

## Implemented locally

- Shared five-subject mobile router factory: old `/beta` contracts retain their
  guards; opt-in `/mobile` publication reuses the same source-bound graders.
  No test-login route is mounted by the release router. Private session marker,
  exact pinned source/assessment coverage and loaded-object validation reject
  missing/extra/drifted content, including changed private rubrics. Production
  requires PostgreSQL and an explicit operator publication reference. A reference
  is not independent pedagogical/scientific approval.
- Grade-filtered catalogue keeps every subject; `available` reflects actual
  imported grade content. All grades5–11 are regression checked.
- Production startup no longer runs legacy automatic schema repairs/create_all,
  seed/retag jobs. Existing production reminders now start/stop through application
  lifecycle; staging sends no scheduled notifications. Additive migration0015 pins12
  Chemistry/history tables, checks conflicts before DDL, refuses destructive
  downgrade;0014 PKCE migration remains. No deployed DB migration was executed.
- Isolated staging template, offline validator, guarded launcher and exact OAuth
  callback scheme (`ilmai-staging`) are prepared. Normal callback stays`ilmai`.
  No hosting/DB/domain/TLS/Google resource was provisioned. See[setup](HTTPS_STAGING.md).
- Latest final-production brief supersedes earlier quota hopping: NVIDIA402/403
  stop the pool;429 pauses globally; bounded authorized standby only for401,
  connection failure or5xx without Retry-After. Trial remains internal Beta only.
  No actual key was persisted/transmitted/activated; reviewed evidence fallback
  remains available without a provider.
- Removed verification-code/recipient/raw-provider-error console and monitoring
  leakage in email delivery. A delivery failure returnsFalse instead of logging
  the OTP or claiming successful delivery. No real email was sent in tests.
- Flutter reviewed-learning flag reuses the Beta learning UI/API while preserving
  separate Google authentication. Staging Gradle identity is
  `com.ilmai.app.staging`/`ILM AI Staging`/`ilmai-staging`; production identity is
  unchanged. Beta/QA/preview combinations are rejected. Normal release remains
  opt-in pending hosted acceptance; no unsafe test-auth promotion.
- One registration action and persisted one-time textbook notice in reviewed
  welcome flow. Correct/incorrect MCQ/FRQ explanation UI, source hiding, grade
  locks and draft/retry behavior share the tested learning implementation.
- Known cached sessions route immediately; bounded profile/preferences validation
  proceeds in background, with session-generation/epoch checks across logout,
  another account and a new login to the same account. Legacy unknown profile
  state still waits or shows retry. Server auth/refresh401 remains authoritative.
  This is not a measured real-device startup improvement yet.

## Completed local evidence

Counts below are per command and overlap; do not add them as unique tests.

| Check | Actual result |
| --- | --- |
| Shared-router baseline: integrated Beta + study help |21 passed,12 deselected,48.92s|
| Initial release publication API/source/ownership |4 passed,4 PostgreSQL deselected,76.58s|
| Focused staging/OAuth/NVIDIA/preflight |94 passed,1 existing warning,22.30s|
| Publication + Beta + provider regression, grades5–11 |182 passed,19 PostgreSQL deselected,1 existing warning,96.17s|
| Pinned schema/PKCE/config |37 passed,1.60s|
| Startup policy/email redaction/schema/config final |43 passed,3.92s|
| Auth/session/OAuth/migration/config regression |94 passed,1 warning,173.40s|
| Final scheme/config regression, including legacy Beta callback |34 passed,1 warning,11.86s|
| Flutter session/performance/release hardening |38 passed|
| Flutter five-subject reviewed staging UI/API |44 passed,18s test phase|
| Flutter local Beta UI/API final regression |44 passed,21s test phase|
| Login light/dark goldens after inspected button text change |2 passed,2s|
| Full Flutter final rerun |1347 passed,6m40s; first run's3 old-label/golden failures corrected|
| Final flutter analyze |No issues found,90s; preceding braces lint corrected|
| Android Beta debug APK |Built205.9s; package.beta/code4/target36; v2 signature verifies|
| Ruff new/modified policy/publication/tests |passed|

`scripts/check_staging_config.py --env-file deploy/staging.env.example`
intentionally fails six missing-real-configuration checks, without exposing
values, connecting to a server or claiming readiness.

Fresh live read-only preflight (receipt in sibling artifacts directory): health200,
mobile auth config404, subjects404, all five grade routes404. Earlier sandboxed
network probe returned no HTTP status; only the approved network-enabled probe
establishes these live statuses. It does not prove the deployed commit/root cause.

ADB device list is empty on2026-11-07. No new phone install, physical QA, signed
upgrade, device performance acceptance or progress mutation was performed.

New local Beta artifact (not production AAB):
`ilm-ai-beta-artifacts/ILM-AI-Beta-1.0.3-code4-d00ce86.apk`,209809731bytes/200.09MiB,
Flutter source`d00ce86ffd359a640b0553bb49dd6508f99386fd`, SHA256
`4dc61f94bf81410c1f96ab5da27bbacc598a7a58aa53200b710d37ceeed57a6e`.
Package/label/debug/code4/version1.0.3/target36 and v2 debug signature verified.
Static scan found no PDF/DB/private config/keystore or checked credential/JWT
literals; this is not a guarantee against every possible secret format.
Existing future-KGP plugin migration warnings remain; build succeeded.

## Required next work / release blockers

1. Finish and test explicit publication import into a fresh isolated PostgreSQL
   staging database, plus whole migration chain/rollback rehearsal. Do not
   substitute copying live user data or weakening original preview guards.
2. Implement/test verified in-app **and public web account deletion**, session
   revocation and complete data lifecycle. Audit all owner/FK/files/legacy stores;
   prevent stale JWTs and reused account IDs from exposing another account.
3. Provision operator-approved HTTPS staging and dedicated Google OAuth test
   client, verify real new/returning/switch/logout/expiry/offline flows and five
   subject progress/XP. No such resources/access exist in this session.
4. Finish full Flutter/analyze/native build checks and real Android profile/release
   performance/upgrade acceptance. Do not confuse mock timing tests with actual
   frame/startup measurements. Restore phone connectivity without clearing data.
5. Correct public privacy/Data safety/deletion declarations and verify Play App
   Signing upgrade compatibility. Upload certificate match alone is insufficient.
6. Produce the final signed five-subject1.0.3/code4 AAB after critical fixes and
   record commit/hash/size and all remaining unperformed tests. Old Biology-only
   candidate AAB is not a completed five-subject release. Never upload without
   explicit owner permission.

The earlier local8930 process was no longer running when checked. It was restored
with `--resume` from source`ac668bf` (PID22368), listening only on127.0.0.1:8930.
Health200/ok/integrated_beta; all five catalogue entries and grade5 lock states
verified; unauthenticated help401 and old tutor404. **46 account/progress table
counts and hashes are unchanged** before/after resume and public probes. Receipts:
`local-beta-health-20261107.json`, `beta-resume-before-20261107.json`,
`beta-resume-after-20261107.json` in the sibling artifacts directory.
Google remains unconfigured; no test account/attempt/reward was created by probes.
Keep test data/credentials
out of Git/APKs and preserve ongoing learner progress.
