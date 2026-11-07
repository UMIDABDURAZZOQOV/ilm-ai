# Production mobile404 — source diagnosis and deployment gate

## Latest hosted checkpoint ? 2026-11-07

See [the current Free staging evidence](FREE_STAGING_20261107.md). Authenticated
Render reads now prove Live e97c029 on main lacks the mobile routers. Release
branch was safely pushed; isolated Free HTTPS staging is actually live with
Alembic0017/1381 lessons and no users. Google remains explicitly unconfigured;
normal preflight correctly stays NO-GO. Production's46-table Neon schema is
unversioned: no blind initial upgrade/stamp. No production mutation/deploy or
Play upload. This supersedes older unavailable-hosting/unknown-SHA/no-push notes.

2026-11-07. **NO-GO; no production deployment/migration or GitHub push performed.**
This is the focused successor to `FINAL_FIX_PROGRESS_20261107.md`.

## Confirmed source/deployment gap

Production API origin is configured in Flutter
`lib/core/network/dio_client.dart` as
`https://ilm-ai-backend-256x.onrender.com`; `API_URL` is its explicit build override.
Beta uses a separate guarded loopback override. No origin/path was renamed.

The public service is the Render hostname also referenced by this repository's
`render.yaml` and keep-alive workflows. Its responses include Uvicorn origin
metadata. That does not reveal Render dashboard settings or the deployed SHA.

Authenticated hosting inspection was unavailable: no local Render API credential
or service ID, GitHub CLI login check failed, and both browser/Windows control
initialization failed with `failed to write kernel assets`/path-not-found.
The Render integration is available but its connection was not confirmed.

Public GitHub inspection established:

- Repository `UMIDABDURAZZOQOV/ilm-ai`, public, default branch `main`.
- Queried current remote main: `e881930708fb04022dfa97a496167d8abf779bb2`.
- That exact source lacks `routers/mobile_skills.py`, `routers/reviewed_mobile.py`
  and `services/release_status.py`. Its `main.py` does not include a mobile router;
  `routers/auth.py` has legacy Google routes, no `/mobile/config` or exchange.
- Remote `qa/final-production-fixes-20261106` returned404: the working local
  feature branch has not been published there. It cannot be selected for a normal
  linked-branch deploy until publication is separately reviewed/authorized.
- Remote CI's `Deploy to Production` job only echoes a message. It does not send
  a deployment request. Local `render.yaml`/`railway.json` specify
  `uvicorn main:app --host 0.0.0.0 --port $PORT`; Docker starts the same module.
- The queried remote main is not an ancestor of the candidate: its only
  remote-only commit changes `README.md`, not Python/deployment behavior. No merge,
  force push or replacement of that remote documentation was performed.

Therefore a deployment of the inspected remote main cannot provide the new
mobile contracts: their source/registration is absent. The served OpenAPI also
lacks them, matching that legacy source family. **The exact live SHA/linked branch
is not proven.** `info.version=0.3.0` is unchanged across source revisions and is
not a Git identity. An env flag or another deploy of this old main cannot add
missing Python modules. No proxy rewrite/CORS/Google credential defect was proven
as the cause of these404s; the required routes are absent in the served contract.

Public-source evidence (fixed revision):

- [main.py](https://github.com/UMIDABDURAZZOQOV/ilm-ai/blob/e881930708fb04022dfa97a496167d8abf779bb2/main.py)
- [auth router](https://github.com/UMIDABDURAZZOQOV/ilm-ai/blob/e881930708fb04022dfa97a496167d8abf779bb2/routers/auth.py)
- [CI workflow](https://github.com/UMIDABDURAZZOQOV/ilm-ai/blob/e881930708fb04022dfa97a496167d8abf779bb2/.github/workflows/ci.yml)

## Endpoint evidence and expected correction

| Method/path | Expected after accepted deployment | Live result / cause | Local correction |
| --- | --- | --- | --- |
| GET `/health` |200, exact approved SHA, mobile contract2|200/status ok, no revision; legacy implementation|Existing `release_status.public_status` exposes only validated public build identity|
| GET `/auth/mobile/config` |200, PKCE/S256/v2; Google true only when actually configured|404; missing served and inspected-main route|Existing local auth router defines and registers it|
| POST `/auth/mobile/exchange` |Validated one-use PKCE exchange; reject missing/invalid proof|Absent in public OpenAPI; no mutating production probe performed|Existing local exchange/grant implementation; no test-login fallback|
| GET `/mobile/skills/config` |200/version2 after exact publication gate|Absent in public OpenAPI|Reviewed local router behind explicit publication configuration|
| GET `/mobile/skills/subjects` |200/all five, locks from real imported grades|404; no served mobile router|Reviewed router reuses existing source-bound engines|
| GET `/mobile/skills/subjects/{slug}/grades` (all five slugs) |200/actual ready grades|Each404; no served mobile router|Exact source-validated1381-lesson import; idempotent, no user/progress rewrite|
| GET `/account/deletion/config` and app/web flow |Capability honestly reflects policy/storage/mail/schema readiness|New deletion not accepted/enabled on production|Implemented/tested locally; keep off until its separate acceptance gates pass|

No synthetic200, route alias to a legacy grader or preview-guard bypass was added.
The five subjects remain source-bound; no PDFs/full textbooks are release inputs.

Final live read-only preflight at2026-11-07T12:22:31Z still reports health200,
auth/catalogue/five grade routes404 and observed revision `unknown`. Exact expected
`cd778f6`/contract2 check fails honestly; exit1/NO-GO. Local changes were not deployed.

## Changes in this focused task

- Removed echo-only deploy job from `.github/workflows/ci.yml`; test environment
  is explicitly isolated and its ephemeral DB name matches existing preview
  guards. No real production deployment job or secret was introduced.
- Added manual, read-only `mobile-contract-preflight.yml`: public GETs only,
  exact expected SHA, receipt saved on failure, read-only repository permissions.
  Dispatch itself does not deploy. It has not been run remotely.
- `scripts/mobile_release_preflight.py --expected-revision <full-sha>` now rejects
  unknown/wrong deployed revision or contract version even when health is200.
  It never authenticates, reads user data or logs response bodies/secret values.
- Added mismatch/redaction tests and real `main:app` contract acceptance to the
  existing disposable PostgreSQL whole-chain/import test. Pinned197 public legacy
  method/path pairs in a fixture; this checks route compatibility, not old-client
  authenticated payload semantics. Google/mail/scheduler/webhook are not called.
- Connection failure in the opt-in PG fixture now reports a fixed safe message,
  avoiding driver traceback locals with a private DSN. Test logs are sanitized.

Source/test/CI commit: `cd778f6c18c90f8e13cfe949856078829697ba2a` on
`qa/final-production-fixes-20261106`. No Flutter code change or APK rebuild is
required for these backend/CI diagnostics; Flutter remains functional `ac168c3`.

Final local evidence (commands overlap; do not add them as unique tests):

| Check | Actual result |
| --- | --- |
| Preflight/production startup unit checks |36 passed,2.46s|
| Auth/PKCE/progress/SQLite deletion/config/preflight/safe-error regression |140 passed,17 PG/full-chain cases deselected,275.17s|
| Actual main:app over freshly migrated/imported PostgreSQL |1 passed,144.63s;17 existing lifecycle/httpx deprecation warnings|
| Both workflow YAMLs |parsed; CI has only test job, new preflight is manual/read-only|
| Changed Python Ruff / staged git diff |passed|
| Existing8930 Beta health / account-progress preservation |200;46 table counts+hashes identical to prior checkpoint|

The PG command ran full Alembic0017, validated/imported1381 lessons, reimported
without overwrite, loaded the **actual** production entrypoint, retained all197
observed legacy method/path pairs, returned actual mobile config/catalogue/grade
responses for grades5–11 and retained synthetic137 XP. No lifespan/scheduler,
Google/email/webhook or hosted request was run by that test. New mobile private
requests without credentials returned401; no Beta test-login route was mounted.

The first regression invocation hit64 Windows temporary-directory permission
errors (76 tests still passed). Using a fresh, explicitly owned workspace
`--basetemp` fixed the runner configuration; final140 passed. An initial PG
invocation used the cluster's default port; it was restarted on its explicit
owned loopback55461 port. A second invocation omitted the project's Windows
UTF-8 switch and failed on Physics JSON decoding; `python -X utf8` rerun passed.
Neither source content nor preview guards were changed to obtain these passes.
The failed local connection log was sanitized; future connection failures use
fixed messages without private driver locals. Known private test credential scan
of the focused receipts found no matches. Old/new warnings and failed attempts
are not reported as successful tests.

Receipts in sibling `ilm-ai-beta-artifacts`:
`production-hosting-discovery-20261107.json`,
`production-remote-source-20261107.json`,
`production-legacy-storage-source-20261107.json`,
`production-entrypoint-postgres-contract-utf8-20261107.log`,
`production-deployment-auth-regression-final-20261107.log`,
`production-focus-beta-health-preservation-20261107.json`,
`production-revision-preflight-20261107.json`.
The owned test PG cluster was gracefully stopped; the existing8930 SQLite Beta
is left running. No real account/answer/XP or deployed database was changed.

## Required hosting inspection — stop before changing production

Connect the existing Render account or provide screenshots **without secret
values** of this exact service's Settings and latest Live deploy:

1. Service name/ID and external URL.
2. Linked repository, branch and Root Directory.
3. Build Command, Start Command and auto-deploy setting.
4. Latest Live deploy's full commit SHA and status; failed deploy event/log
   categories if any. Do not send raw logs containing environment/token values.
5. PostgreSQL persistence/backup availability and actual Alembic revision, only
   through an authorized operator; no learner rows need to be disclosed.

Do not press Deploy latest commit now: the inspected remote main lacks the fix.
Do not push/merge until the linked branch and auto-deploy behavior are confirmed.
Connecting Render authorizes inspection, not deployment/migration/config changes.

## Safe operator sequence after resources and separate authorization

1. Inventory current service and active database/auth store. Inspected remote
   `services/users.py` and `tokens.py` use DB only when `DATABASE_URL` exists;
   local default is database auth. Do not silently switch a JSON deployment to an
   empty DB. Preserve provider identities, currentJWT/SECRET values, DB identity,
   UID/lesson identifiers and persistent files. Never blindly apply the original
   Render Blueprint, which can create new resources/secrets.
2. Record current live code/env configuration and verify an actual backup/restore
   path. Export authorized production backups only into protected private storage,
   never this repo/APK. A backup file alone is not restore acceptance. For a
   manual operator dump, use private `PGSERVICEFILE`/`PGPASSFILE` and
   `pg_dump --dbname=service=ilm_production_backup --format=custom --no-owner
   --no-acl --file <protected-backup-path>`; no password-bearing URI in commands.
   Verify restore in a separate restricted destination and record its result.
3. Publish a reviewed candidate branch without triggering production; then create
   an approved isolated staging service/DB/role with dedicated secrets and HTTPS.
   No allocation/paid service was provisioned. Fill `deploy/staging.env.example`
   outside Git; run its offline validator. Do not copy production learner data.
4. Rehearse actual current-schema migration inventory and backup/restore on staging.
   Fresh-schema full-chain0017 evidence does not justify stamping an unversioned
   existing DB. Run explicit reviewed import, inspect its zero-overwrite result;
   do not create duplicate lessons or reset existing progress.
5. Configure Google Web client and test accounts for
   `https://<approved-staging-origin>/auth/google-callback-mobile`, app scheme
   `ilmai-staging`; verify TLS/redirect/secure cookies. Keep test-login/preview
   flags off. `MOBILE_REVIEWED_RELEASE=true` and publication reference must be
   accepted with exact imported content. Do not copy actual secrets into templates.
6. Accept real Google/session/five-subject/MCQ/FRQ/progress/deletion and old-client
   compatibility on staging. Deletion also needs policy, actual test mailbox,
   persistent storage, retry worker and financial/backup retention acceptance;
   see `ACCOUNT_DELETION.md`. Do not enable it merely to change a capability flag.
7. Obtain separate approval for production backup/migration/import/env/deployment.
   Deploy the exact accepted commit to the existing service/database; preserve
   `com.ilmai.app` and normal `ilmai` callback. Do not use Beta test identity.
8. Run read-only preflight with `--expected-revision` equal to that deployed SHA,
   then actual owned-account acceptance. A passing preflight is not GO by itself.

## Rollback boundaries

Record the previous live commit and compatible env before deployment. Roll back
the application only to a schema-compatible revision; pause writes/obtain operator
review if compatibility is uncertain. Keep additive schema/content changes and
current learner progress. Never run destructive downgrades or restore an old DB
over newer progress. Do not resurrect deleted account data from an old backup.
Deletion write barriers/tombstones must survive rollback, which can rule out a
legacy application revision. Backup recovery is a separate authorized incident
operation, not an automatic deploy script. No rollback was executed here.

Official operational references:
[Render deploys](https://render.com/docs/deploys),
[public build identity](https://render.com/docs/environment-variables),
[rollbacks](https://render.com/docs/rollbacks).

Read-only post-deployment command, **only after** an accepted exact commit has
actually been deployed (replace the SHA if a later candidate is approved):

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
python -X utf8 scripts/mobile_release_preflight.py `
  --origin 'https://ilm-ai-backend-256x.onrender.com' `
  --expected-revision cd778f6c18c90f8e13cfe949856078829697ba2a `
  --output 'C:\Users\Page\Desktop\Projects\ilm-ai-beta-artifacts\post-deploy-contract.json'
```

Running it now correctly returns NO-GO; it cannot deploy or migrate anything.

## Remaining external gates

Actual Render connection/service settings/live SHA and approved deployment;
hosted HTTPS/Google staging and backups; real deletion/privacy/Data safety;
old Play-client/signed upgrade and connected-phone benchmarks. No new AAB/Play
upload, provider activation, production data modification or live-account deletion.
