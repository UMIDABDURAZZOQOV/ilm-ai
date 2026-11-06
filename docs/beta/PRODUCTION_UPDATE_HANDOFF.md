# Existing Play update: backend audit — 2026-11-06

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
