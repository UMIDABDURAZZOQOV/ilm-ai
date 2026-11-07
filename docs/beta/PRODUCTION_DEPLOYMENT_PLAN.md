# Existing Play update: deployment and rollback plan

## Current blocker implementation (2026-11-07)

This section supersedes the historical open engineering items below. New local
code includes verified app/public-web deletion, migrations0016/0017 and a pinned
55-table runtime foundation, plus an explicit transactional publication importer.
See [deletion deployment requirements](ACCOUNT_DELETION.md). Full current command
results belong in FINAL_FIX_PROGRESS_20261107.md; unfinished runs are not passes.
Backend functional commit: `b4e138a`. Actual full-chain Alembic plus1381-lesson
import/reimport/XP-preservation acceptance passed on isolated real PostgreSQL.
This does not establish the current production schema revision or authorize a
production upgrade. A fresh-install rehearsal is not backup/restore acceptance
for an existing deployment. Final read-only production preflight at10:07:32Z
still reports the mobile404 blockers. No hosted migration/deploy was executed.

The production read-only OpenAPI inventory has187 paths and no `/mobile/*` or
`/auth/mobile/*` contract, while legacy `/auth/google-login` and `/skills/subjects`
exist. This confirms deployment/contract divergence, not an exact deployed Git
revision. Hosting admin access was not found; no deployment was attempted.

Operator sequence after separate authorization:

1. Record the actual Render service repository, branch, root, build/start command
   (`uvicorn main:app`), deployed commit and approved DB identity. Compare with
   this isolated feature branch; retain the existing secrets, package and users.
2. Provision/approve an isolated HTTPS origin and PostgreSQL role/database. Fill
   the private staging template, dedicated Google client/callback, test mailbox,
   storage and deletion policy. Run `scripts/check_staging_config.py` before
   launch. Nothing here provisions paid resources or approves a public deployment.
3. Inventory Alembic/schema state before upgrading. Fresh schemas now require
   `0017_runtime_foundation`;0011 has a fresh-install-only guard for its previously
   missing SAT table. Existing already-applied0011 is not rerun. Conflicts fail
   review; no production create_all, destructive downgrade or blanket stamp.
4. Validate manifests with `python scripts/import_reviewed_publication.py`.
   Local rehearsal apply accepts only a private URL file pointing to loopback
   PostgreSQL staging. It refuses production/hosted writes and does not migrate
   tables. Hosted publication requires a separately approved operator transaction
   using `services.reviewed_publication_import.import_reviewed_publication(db)`.
   Import preserves existing lesson IDs, users, sessions and progress; mismatched
   content/private rubrics require review rather than overwriting live lessons.
5. Activate reviewed `/mobile` publication only with exact imported coverage and
   an explicit review reference. Keep preview/test-login flags disabled. Activate
   deletion only after real OTP delivery, policy/storage/worker acceptance.
6. Test actual HTTPS/Google new/returning users, expired sessions, deletion,
   account isolation, five subjects and signed upgrade on owned staging accounts.
   Preserve legacy `/skills` and auth contracts. Do not infer old Play-client
   compatibility from only current-client mocks.
7. Re-run public preflight, health revision, catalogue and deletion capability
   through the real origin. Separate permission is still required for production
   migrations/deployments and Play upload. Keep application rollback additive;
   never restore an old DB over new learner progress.

No final five-subject production AAB or GO is authorized by this checklist.

## 2026-11-07 implementation checkpoint

Read [HTTPS staging preparation](HTTPS_STAGING.md) and the current
[fix progress](FINAL_FIX_PROGRESS_20261107.md) first. The startup writes described
in the historical audit below are now guarded out of `ENVIRONMENT=production`
in local source. No live deployment was changed. Additive migration0015 covers
the12 existing Chemistry/history engine tables; source publication has a separate
fail-closed dependency and Flutter opt-in. Hosted PostgreSQL/OAuth acceptance,
publication import, deletion, store declarations and signed upgrade remain open.

Status: **NO-GO**, 2026-11-06. This is a plan, not an executed deployment or
permission to upload to Play. Preserve `com.ilmai.app`, the existing signing
identity, users' IDs/provider identities and persistent database/secrets.

## Verified mismatch and reproducible public check

The local branch includes `routers/auth.py` PKCE-v2 preflight/exchange and mounts
`routers/mobile_skills.py` from `main.py`. The configured live server returns404
for `/auth/mobile/config`, `/mobile/skills/subjects` and all five public mobile
grade routes, while `/health` returns200. This demonstrates a deployed contract
mismatch. It does not identify the deployed commit, provider configuration or DB
schema. A blind route rename or `/skills` fallback is unsafe.

`render.yaml` still starts `uvicorn main:app`; the inspected `main.py` performs
table creation, legacy content seeding, retagging and scheduler startup during
import. Do not launch it against a production DB merely to inspect routes.
Those startup writes need a separate explicit deployment/seed policy review.
Do not make ephemeral SQLite the production database or regenerate JWT secrets.

Read-only preflight (no account/token needed):

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
python -X utf8 scripts/mobile_release_preflight.py `
  --origin https://ilm-ai-backend-256x.onrender.com `
  --output ..\ilm-ai-beta-artifacts\final-readiness-production-contract.json
```

Exit1 is expected while contracts fail. Even exit0 means **further acceptance
required**, not GO: this script does not log in, mutate accounts or verify store
declarations, deletion, source publication correctness or upgrade performance.

## Approved HTTPS staging needed before writes

Owner/operator provides a deployment isolated from production, a fresh persistent
PostgreSQL database and secret-manager configuration. No such environment or
admin access is currently available in this session. Record service/repository
branch/commit, API origin, database identity, current schema revision, region,
backup policy, CORS origins, existing JWT/refresh-token handling and Google client
configuration without printing secret values. Use distinct staging OAuth clients,
exact HTTPS redirect URI and correct release app-signing SHA certificate. Upload
certificate confirmation alone does not establish Play App Signing OAuth setup.

Never deploy the loopback test-login endpoint, `BETA_TEST_AUTH_ENABLED`, local
installation-secret identity, preview routes or a debug APK as production auth.

## Additive schema and backup rehearsal

Inventory the live schema/revision through an approved read-only connection.
Do not assume `create_all()` migrated existing column types, indexes or ownership
constraints. The local Alembic chain now includes **0014_mobile_oauth_state** for
the two PKCE tables previously only represented in shared model metadata:
`oauth_states`, `mobile_login_grants`. It creates missing tables, checks existing
columns/PK/grant ownership, preserves all user/progress rows and refuses conflicting
schemas. In-memory SQLite tests pass; real deployed PostgreSQL/whole migration
chain acceptance remains required. Chemistry/history publication migrations and
deletion lifecycle schema are **not supplied by this migration**.

Rehearsal must use a fresh **staging restore** target and an authorized, encrypted
backup. With preconfigured private libpq service/password files, operator commands
can omit credential values from command lines:

```powershell
# Operator verifies private service identities and destination first.
pg_dump --dbname='service=ilm-approved-backup-source' --format=custom `
  --no-owner --no-acl --file='<private-encrypted-backup-path>'
pg_restore --dbname='service=ilm-empty-staging-restore' --single-transaction `
  --no-owner --no-acl '<private-encrypted-backup-path>'
```

These commands have **not** been run. Do not use a production database as restore
target or add `--clean`. Validate backup restore, row counts, stable user IDs,
provider subject uniqueness, source/content hashes and per-user progress/reward
invariants in staging before applying a reviewed migration sequence. Use an
explicit staging process environment for Alembic, not implicit `.env` discovery.

Rollback is application deployment rollback to the recorded previous revision,
keeping additive PKCE tables and active sessions. 0014 intentionally refuses
destructive downgrade. Do not restore an old whole database over new learner
progress; replay/restore requires a separate incident plan. Do not rotate session
secrets or change user/lesson keys during this update.

## Five-subject production publication is still engineering work

All five runtimes are tested in Beta. Four v2 engines explicitly authorize only
owned local/staging databases and development/test environments; Flutter's
integrated Beta deliberately rejects release builds. These guards remain.

A production path needs an explicit reviewed publication policy and schema,
source-hash validation for each lesson/assessment, owner-scoped attempts and
server-authoritative grading/rewards. It must reuse the existing engines through
an audited production authorization boundary, preserving their preview entry
guards, rather than toggling `BIOLOGY_ONLY=false`, spoofing ENVIRONMENT or using a
staging-named production database. Then adapt normal mobile release navigation to
that contract and test all catalogue/grade states5–11. Existing science/source
validators and original subject branches remain untouched by this patch.

Old-client strategy is an unresolved prerequisite: identify the actual deployed
1.0.2 OAuth protocol, preserve existing refresh sessions/IDs, and rehearse a
capability-aware transition. New clients must not downgrade to token-bearing
deep links. Do not claim older fresh login remains compatible without testing it.

## Other gates not closed by an AAB or keys

- Owner-verified account deletion/request: authenticated in-app and external web
  entry, reauthentication/replay protection, per-account personal-data inventory,
  requests/fulfilment/retention, all session revocation, uploads/external stores,
  shared curriculum and other accounts preserved, and end-to-end tests.
  No deletion workflow has been implemented by this patch.
- Reconcile Play Data safety and public privacy statements against deployed auth,
  progress, analytics/Firebase/SDKs and AI handling. No Console changes made.
- Google AI Studio is unsuitable for this school client's under-18 audience under
  its current terms; see `AI_PROVIDER_READINESS.md`. No exposed key was activated.
- Real new/returning/different Google accounts, expired/invalid sessions, offline
  recovery, cross-device and Play-signed internal-track upgrade with retained data.
- Measured optimized device startup/frame/memory acceptance, Android15/16
  edge-to-edge and16KB runtime, plus crash/ANR observation. Debug launch timeout
  alone is not an ANR diagnosis or a performance acceptance result.

Only after these gates pass should the reviewed five-subject release AAB be
rebuilt, signed with the existing key, checked for unused versionCode4, verified,
and presented for the user's **separate Play upload approval**. Existing artifacts
are prior Biology-only/local Beta candidates, not evidence these gates passed.
