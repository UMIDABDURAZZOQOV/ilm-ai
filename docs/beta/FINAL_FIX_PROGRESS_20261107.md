# Final production fixes — active checkpoint, 2026-11-07

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
