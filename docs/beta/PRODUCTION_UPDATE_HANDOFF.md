# Existing Play update: backend audit — 2026-11-06

## 2026-11-06 - Final-readiness follow-up: NO-GO remains

The user's full195-line final-readiness brief was read with credential redaction.
They confirmed Google AI Studio credentials. No disclosed key was used, saved,
committed or sent to any service. Revoke/replace them through the provider
console. Gemini Developer API's current under-18 client restriction conflicts
with this school app and the user's audience-compatibility requirement; it was
not connected. No replacement provider was activated.

### Changes completed in the isolated backend branch

- Optional existing OpenAI evidence selector: explicit reviewed private config
  outside all Git checkouts, symlink/reparse restrictions,1–8 unique configured
  keys, fixed provider origin, bounded authorized standby for eligible errors.
  Quota/rate errors do not sweep accounts. Retry-After pauses the whole pool;
  credit/spend exhaustion stops inference until operator reconfiguration.
- Reviewed evidence fallback retained. Free-form learner messages, selected
  answers, account/attempt IDs, source metadata and grader feedback/solutions
  are excluded from the optional external payload. Only reviewed teaching
  snippets may be selected; generated prose never becomes scientific content.
- Two-call/6s-per-attempt limits, capped input/completion, two in-flight calls,
 20/min and1000/UTC-day per-process attempt budget. Distributed durable billing
  caps and a real audience/privacy review are still production requirements.
- Read-only public API preflight: health200; mobile auth/catalogue and all five
  grade endpoints404 (seven failed required contracts). No production writes.
- Additive0014 PKCE migration creates/validates state/grant tables, ownership
  and schemas without changing existing user IDs, XP or progress. No live
  migration was run. Backup/restore/rollback and old-client transition plan
  recorded in backend docs/beta/PRODUCTION_DEPLOYMENT_PLAN.md.

### Fresh tests and handset measurements

- Combined reviewed SQLite integration/provider/preflight/migration: **86 passed,
 12 deselected,1 deprecation,51.28s**. Explicit owned bootstrap and copied fixture.
- Separate backend identity/auth/security/migration: **57 passed,1 warning,
 301.01s**. Provider/preflight/migration unit run:65 passed. Suites overlap;
  do not sum these counts or add them to historical Flutter totals.
- New-file Ruff checks and Git whitespace checks passed. The legacy study_help
  file still has pre-existing ambiguous-variable lint findings; they were not
  suppressed and are not claimed fixed. No Dart/native source changed here.
- Fresh Flutter analyze: **No issues found,247.9s**. The earlier1334 Flutter/95
  Beta/other suites refer to the unchanged app source384f6d6, not new test runs.
- Profile builds succeeded (310.1s isolated Perf,454.4s existing Beta identity);
  package/certificate checks passed. Temporary same-certificate profile install
  used install-r and preserved existing authentication/draft. No answer, logout,
  onboarding reset, uninstall or data clear was performed.
- Actual existing-account profile startup, five force-stop launches: **Android
  TotalTime2443–2528ms, median2450ms**; Dart first-frame callback470–492ms,
  median477ms. All five reached Learn. UI-polled Learn visibility5902–7186ms
  includes ADB/uiautomator overhead and is not exact time-to-interactive.
- First launch after profile install was8330ms; debug restore launch again
  timed out at10532ms and later loaded. The original11s debug issue is NOT
  proven fixed or diagnosed as ANR. No “0 lag” or controlled speedup claim.
- Two five-tab navigation rounds:21/219(9.59%) and29/105(27.62%) frames exceeded
  the60Hz build/raster budget. Post-GC heap18,190,112→19,816,160 bytes and
  PSS156,134→174,123KiB. This short, instrumented workload cannot prove no leak;
  Android16/16KB, sustained workloads and crash/ANR acceptance remain open.
- Restored the unchanged stable debug APK with install-r Success. All nine
  measured user/progress table hashes remained unchanged throughout profiling.
  Installed-artifact hash and final UI verification are recorded in local receipts.

### Artifacts and outstanding work

The **existing** signed AAB remains:
`../ilm-ai-beta-artifacts/ILM-AI-1.0.3-code4-release-candidate.aab`
(76,951,648 bytes/73.39MiB, SHA256
`a3aa66463f996a772fc1f0d7b3f2fbc653c55f75160c3c34d02a65e4043f003c`,
source384f6d6). It is still Biology-only, not a newly integrated five-subject
release. Stable debug Beta remains209,804,239 bytes/200.08MiB, SHA256
`1a54a015468ad5087407ddb18ad88d5a47cb5c4136b759e99922bbdf239d8754`.
No release AAB was rebuilt while critical gates remain, and nothing was uploaded.

**Unfinished engineering:** production publication/integration of five subjects
without disabling preview/source gates; owner-verified in-app and public web
account deletion lifecycle; old-client compatibility; startup/jank diagnosis and
optimization. **Unavailable external acceptance:** approved HTTPS/OAuth staging,
new/returning/different real Google accounts and cross-device progress, actual
deployed schemas/config, Play-signed internal-track upgrade and owner-reviewed
Data safety/privacy declarations. Keys do not close any of these gates.

Port8930 remains the original running loopback Beta process with reviewed
fallback and no external AI; new source changes are not claimed deployed there.
Production DB/main/subject branches and existing signing material are preserved.
Full details: backend AI_PROVIDER_READINESS.md and PRODUCTION_DEPLOYMENT_PLAN.md.
Local receipts: final-readiness-production-contract.json, final-readiness-backend-
combined.log, final-readiness-backend-auth-confirm.log, final-readiness-flutter-
analyze.log, performance-final-readiness-existing-account-20261106-startup.json,
final-readiness-profile-nav.json and final-readiness-progress-restored.json.


The user corrected the earlier first-release answer: `com.ilmai.app` is already
on Play. Preserve its permanent identity and existing verified upload key.
The upload certificate provided by the user matches the local key and older AAB.
Do not reset signing or assume Beta's missing private files mean no key exists.

Detailed audit: sibling Flutter `docs/PRODUCTION_UPDATE_AUDIT.md`.
Both Beta worktrees use `qa/play-release-audit-20261106`.
Production/main/subject branches and databases were not changed.

Read-only public probes of the existing configured HTTPS server returned health
200 but `/auth/mobile/config` and `/mobile/skills/subjects` **404**. `/skills/subjects`
is a legacy list, not a reviewed mobile replacement. Existing Google OAuth may
still work for the old app; this audit did not claim it is unconfigured in
production or log in to production. New PKCE mobile clients deliberately fail
closed on the old protocol. Do not revert to JWTs in custom URI callbacks.

Separate HTTPS test/OAuth configuration is unavailable, per the user's answer.
The server on localhost8930 remains local Beta, with test identity available,
Google unconfigured and `production_ready=false`. Keep it running for phone QA.

## Verified tests

- `tests/test_beta_unified_identity.py`, `test_release_hardening.py`,
  `test_mobile_oauth_redirect.py`: **53 passed**, one Starlette/httpx warning.
  Disposable SQLite fixtures; identity, ownership, PKCE, rotation, replay,
  logout and reward/prerequisite assertions exercised.
- `test_integrated_beta.py`, `test_study_help.py -k 'not postgres'`:
  **14 passed, 12 deselected**, one deprecation. A consistent reviewed SQLite
  fixture was made through a read-only connection; tests copy it into their own
  disposable database. No writes to the live phone database. PostgreSQL not run.
- Across real local handset logout/login, all nine measured user/progress table
  counts and SHA256 digests were identical. Refresh-token rows may legitimately
  change; never print their contents.

Auto-review rejected the first integration-test invocation referencing a live DB
path. It was replaced with the explicit disposable-copy setup above; no override,
policy bypass or test weakening. Logs are local ignored artifacts.

## Release work still required

1. An approved HTTPS test environment and Google provider config, then real
   account chooser, returning/new/different accounts and cross-device progress.
2. A backward-compatible production mobile namespace/auth deployment with
   database migration/dry-run/backup/rollback verification. Local Beta's reviewed
   source and preview authorization restrictions must remain in place.
3. Explicit reviewed five-subject publication and help/FRQ integration. Ordinary
   mobile release is Biology only; no preview gate may simply be removed.
4. Implement/test owner-scoped account deletion/request lifecycle across auth,
   progress, sessions, uploads and other retained personal data, with public web
   request path. Never delete shared curriculum/source data or other users' rows.
   Current auth routes have no account-deletion flow; a privacy URL is not deletion.
5. Reconcile the public Play “No data collected” statement with actual account,
   age, progress and SDK processing. Verify public AI retention/sharing claims
   against the real provider configuration before editing declarations.

No backend service code or deployed configuration was changed by this audit.
Tests do not confer production approval or verify current PostgreSQL migrations.
