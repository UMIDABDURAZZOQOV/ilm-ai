# ILM AI1.0.3 final readiness — active checkpoint

Production remains **NO-GO**. This document records actual evidence, not permission
to change production, its database, or Play Console. Existing package com.ilmai.app,
1.0.2/code3 to candidate1.0.3/code4, upload certificate unchanged.

## Backend coverage

- Runtime597b5ac CI42500888563 succeeded:5362 passed,75 skipped,21 warnings,
  6189.45s; import and Docker build passed. This is the deployed staging runtime,
  not the later21d1623 recovery runtime's full-CI acceptance.
- Expanded PostgreSQL18/PDF CI6899715/42504048745 ran5437 cases, with21 failures
  and11 Windows-only skips. Failures were one expired synthetic token after
  quadratic Chemistry setup,19 fixtures selecting an uninstalled default driver,
  and one World History fixture database-name mismatch. These are failures, not
  additional passes. PDF optional fixtures actually ran.
- Fixes preserve production TTL and strict source/preview guards: existing reviewed
  batch importer validates every pinned source per invocation; test authentication
  starts after setup; explicit installed psycopg2 driver; isolated database name
  meets the history prefix; owned random schemas removed in fixture teardown.
- Corrected83-case gap set actually passed:57 PostgreSQL,15 source-PDF and11
  WindowsACL cases. One extra SQLite production-guard control passed:84 unique
  node IDs, not a sum of reruns. Disposable loopback databases dropped in finally;
  no production clone or public staging used. Earlier failures remain in receipts.
- New exact-source full CI and final Docker result are still pending.

### Later corrections from real Windows/PostgreSQL execution

48 selected cases passed before a30s full-course Physics CLI test budget expired.
That offline316-lesson source-validation/import rehearsal now has a bounded180s
budget, preserving all source checks and assertions; it actually passed afterward.
This changes a test timeout, not production request/identity TTLs.

The next real PostgreSQL test revealed a runtime defect: replay of the same attempt
serialized the same expiry instant as UTC on creation and+05:00 after DB retrieval.
Canonical UTC wire serialization now covers the four v2 assessment engines without
changing expiry instants, grading, rewards or stored rows.26 targeted helper/engine/
driver/CI contracts passed; real PostgreSQL Physics replay then passed. Subject
branches are untouched; integration corrections exist only on the recovery branch.
The83 selected gap cases are now complete. Additional fixture corrections bind
token ownership/revocation lookups to the same owned history schema, refresh the
test JWT between the406-lesson walkthrough and separate concurrency phase, and
assert SQLite-only production rejection only for SQLite. PostgreSQL must remain
accepted. Biology catalogue preparation is shared per import transaction while
each lesson's source is still validated. These do not change runtime auth/TTL.
The separate60-case identity/wire/OAuth regression run also passed; counts overlap
other suites and are not added to a claimed full backend total. Full CI pending.

### Historical baseline and locking, private clone only

Fresh0012 metadata comparison found no missing historical tables/columns or type/
nullability differences, but13 missing server defaults. Private rehearsal set only
those explicit defaults and all original row digests remained unchanged. Review-only
SQL is outside Git; it was not applied to production. Key/index/constraint differences
were reviewed offline against the encrypted saved schema. Actualix_users_email
is a full unique btree on non-nullusers.email, with no predicate/expression; its
logical uniqueness matches the historical column rule. It is structurally an
index rather than a named unique constraint. No SQL was executed for this review;
operator baseline/default reconciliation approval still remains required.
No Google-provider rows required the historical email-verification backfill.

### Email-only identity linking correction

Historical password signup could set email_verified without delivered verification.
Google callback therefore must not trust that boolean to automatically merge an
existing account by matching email. Any email-only collision now requires the
existing account's own login/recovery; exact Google provider-subject lookup remains
first and preserves existing accounts, including changed email/display names.
No account/progress row is rewritten by this guard. Existing encrypted production
snapshot aggregate inspection found no missing subjects in Google rows.60 actual
identity/OAuth/migration/wire regressions passed, including both legacy verification
flag states and missing Google-subject records. Real hosted current-source acceptance
is still pending; do not imply deployment or live signoff from these tests.

A held reader blocked exclusive DDL as expected:55P03 under250ms lock_timeout,
approximately352ms observed including overhead. Uncontended hypothetical baseline+
0018 upgrade took5496ms on the private local clone. This is not a production downtime
estimate. Use a maintenance/quiescence window and bounded lock/statement deadlines;
abort/rollback on contention. Private databases were dropped; PG18 clone server
stopped after rehearsals, encrypted owner-bound backup retained. Production unchanged.

## Actual backup / restore / migration evidence

Production is PostgreSQL18.6 with46 public tables and no Alembic revision table.
TLS read-only consistent snapshot backup was encrypted with CurrentUser DPAPI and
owner/SYSTEM-only ACL outside Git. No production DDL/DML/migration was performed.
Encrypted backup SHA256:
`b88e818847b72942de497ceef654350b5e117d0ec6db6a575e150a1e9a880afa`.

Actual private PostgreSQL18 restore matched46 tables/21,346 rows. A **hypothetical**
0012 baseline followed by0018 additive migration retained original row digests.
Source-validated1381-lesson import/reimport retained every original row; repeated
import inserted0 Biology lessons/0 reviewed rows and modified0 progress rows.
Temporary restored databases were dropped. Receipts are outside Git:
production-private-backup-rehearsal-20261108.json and
production-saved-backup-rehearsal-20261108.json.

This does not authorize blindly stamping the unversioned production database.
Historical defaults/backfills/index equivalence, lock/downtime review, independent
off-machine recovery and final operator approval remain gates. DPAPI recovery is
tested under this Windows owner; it is not portable disaster recovery.

## Phone / Flutter

Third recreated account onboarding completed by owner. A30XP/2lessons and
B20XP/1lesson preserved. Opt-in profile source320c7a7 installed with install-r.
Samsung baseline navigation:308 frames,22.4% over16.67ms; repeated warmed sample
288 frames,12.85% over budget. Same source: **not an optimization improvement claim**.
Cold Android activity2.579/2.688s, warm sample145ms; first frame469/490ms.
Catalogue readiness failed during polling; the poll duration includes ADB overhead
and is not exact TTI. No current performance GO. Current public staging health and
catalogue both200, approximately6.9s each; no raw phone logs exported.

Latest owner instruction supersedes optional-password UI: Google-only entry is
restored with one primary CTA. Password choice/form and unused email/signup/reset
screens are removed. Existing Google subject/PKCE/session/progress are preserved.
Old profile4c2ab1c and debug22ea794 contain superseded UI. New Google-only68d0697
APK installed-r Success.54 targeted Flutter tests/analyze passed; actual third
Google login returned without onboarding, and force-stop/reopen restored session.
New signed AAB verified with existing upload identity; no upload. Current full
Flutter suite and phone performance/signed upgrade acceptance remain pending.

## Privacy / Play / release gates

Owner reports previous Play audience review approved. Supplied wizard text does
not show checkbox states, Data safety or App access values. No Console settings
were changed. Google policy requires mixed-audience apps to provide full access
without mandatory Google sign-in; the owner's Google-only decision leaves that
release policy review unresolved. Neutral age handling and applicable consent still
need a reviewed product/legal basis. No audience was silently changed to18+.

Public privacy snapshot still names OpenAI data-sharing/model improvement. Current
reviewed staging has no external AI configured and serves verified explanations.
Prepare version-accurate disclosure/retention/support decisions before publication;
do not assert the old production client has the new data flow. In-app and external
deletion are implemented and actual staging Google deletion/relogin passed; public
production deletion and new mobile endpoints remain gated by approved deployment.

Required final evidence: current full CI; production baseline/lock/backup/rollback
review; approved production deployment and safe endpoint checks; current policy and
Console declarations; credentials rotated; full phone performance; Play-signed
1.0.2→1.0.3 internal-track update; new final APK/AAB hashes and source commits.
Old7a2e37e NO-GO AAB is historical and cannot substitute for a new final build.

## Official policy references checked2026-11-08/09

- [Google API user data policy](https://developers.google.com/terms/api-services-user-data-policy)
- [Google Play Families](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en)
- [Google Play User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en)
- [Data safety](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en)
- [Target API](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en)
