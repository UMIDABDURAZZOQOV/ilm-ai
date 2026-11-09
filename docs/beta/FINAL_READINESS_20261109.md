# ILM AI1.0.3 final readiness — active checkpoint

Production remains **NO-GO**. This document records actual evidence, not permission
to change production, its database, or Play Console. Existing package com.ilmai.app,
1.0.2/code3 to candidate1.0.3/code4, upload certificate unchanged.

## Backend coverage

- Runtime597b5ac CI42500888563 succeeded:5362 passed,75 skipped,21 warnings,
  6189.45s; import and Docker build passed. This is actual current runtime evidence.
- Expanded PostgreSQL18/PDF CI6899715/42504048745 ran5437 cases, with21 failures
  and11 Windows-only skips. Failures were one expired synthetic token after
  quadratic Chemistry setup,19 fixtures selecting an uninstalled default driver,
  and one World History fixture database-name mismatch. These are failures, not
  additional passes. PDF optional fixtures actually ran.
- Fixes preserve production TTL and strict source/preview guards: existing reviewed
  batch importer validates every pinned source per invocation; test authentication
  starts after setup; explicit installed psycopg2 driver; isolated database name
  meets the history prefix; owned random schemas removed in fixture teardown.
- Corrected83-case Windows/PostgreSQL/PDF gap run is in progress. It uses a new
  disposable loopback database, never the production clone or public staging.
  Earlier interrupted diagnostic runs are retained, not counted as passes.
- New exact-source full CI and final Docker result are still pending.

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

Google optional entry and bounded catalogue retry are active Flutter changes.
Single primary auth CTA retained; secure password login/signup/session contracts
reused, duplicate guard and cancellation retained.49 focused auth tests passed;
initial expected golden changes visually reviewed in light/dark. Full new-source
suite/analyze, new artifacts, phone startup acceptance and signed upgrade pending.

## Privacy / Play / release gates

Owner reports previous Play audience review approved. Supplied wizard text does
not show checkbox states, Data safety or App access values. No Console settings
were changed. Google policy requires mixed-audience apps to provide full access
without mandatory Google sign-in; optional password addresses that gate, not
parental-consent compliance. Neutral age handling and applicable consent still
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
