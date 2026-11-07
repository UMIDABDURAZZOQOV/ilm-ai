# Isolated HTTPS/OAuth staging — prepared, not deployed

Updated: 2026-11-07. **NO-GO for production.** No hosting service, domain, HTTPS
certificate, Google client or fresh staging database was created in this task.
No production account/database/deployment/Play release was modified.

## Existing infrastructure

- `render.yaml` describes a Render Python web service (`uvicorn main:app`) and
  a PostgreSQL database. Its existence does not establish the live deploy commit,
  dashboard access, free-plan availability or a separate staging allocation.
- Production app: `com.ilmai.app`, 1.0.2/code3; owner confirms code4 is unused.
- Local Beta: loopback port8930, test identity, not HTTPS/OAuth acceptance.
- Fresh read-only probe on 2026-11-07: health200; `/auth/mobile/config`,
  `/mobile/skills/subjects`, five mobile grade routes404. Receipt:
  `ilm-ai-beta-artifacts/final-readiness-production-contract-network-20261107.json`.
- No hosting/domain administrator access was established. No paid resource was
  activated. Production Render blueprint remains unchanged.

## Prepared configuration

`deploy/staging.env.example` lists actual server environment variable names.
It contains placeholders and intentionally fails the offline validator.
Copy it **outside all Git checkouts**, e.g. to a private local configuration
directory; protect the file with the Windows account ACL. Never add it to Git,
chat, Flutter defines, APKs or AABs. `.env.*` and `*.private.env` are ignored.

Set a dedicated PostgreSQL database **and role** ending `_staging`, restricted
to that database; declare their exact host/name/role in the template. The guard
checks these identities, but cannot prove that an operator did not mislabel a
production resource. Record that independent check in
`STAGING_ISOLATION_REVIEW_REFERENCE`. Start with synthetic accounts; do not copy
production learner data. Backups used for rollback rehearsals must also be
synthetic/sanitized and restored into an empty isolated destination.

Set `ENVIRONMENT=production` to retain production persistence/secret/CORS checks;
`DEPLOYMENT_STAGE=staging` activates additional isolation checks before router/DB
imports. `PYTHON_DOTENV_DISABLED=1` prevents implicit production `.env` discovery
(requires python-dotenv>=1.2; locally verified1.2.2). Use distinct strong
`SECRET_KEY` and `JWT_SECRET`; never reuse existing production secrets. Keep
`AUTH_STORAGE=database`, test-login/preview flags disabled and payment test mode
enabled. Optional external AI/bot/monitoring integrations stay unset. The reviewed
lesson explanation fallback does not require an AI token. NVIDIA trial is not
enabled for production/staging; quota exhaustion stops provider use.

`MOBILE_PUBLICATION_REVIEW_REFERENCE` records operator provenance for pinned
source publication, **not** independent scientific/pedagogical signoff. Four v2
engines are reused under the explicit publication dependency; old preview gates
remain closed. Missing schema, content or private-grader drift returns503.
Production startup no longer creates tables, imports legacy seed content,
retags questions during import. Existing production reminders start through the
application lifecycle and are disabled in staging. Reviewed migrations/imports
must be completed explicitly before acceptance. Pinned additive migration
`0015_reviewed_subject_schemas` now creates the12 existing Chemistry/history
engine tables and rejects conflicting schemas before any DDL; its SQLite tests
passed. Actual PostgreSQL migration acceptance, reviewed publication import
tooling and account deletion are still outstanding at this
checkpoint; a new empty database is not yet a complete working staging service.

Offline check (does not connect to any database/server):

```powershell
Set-Location 'C:\Users\Page\Desktop\Projects\ilm-ai-beta'
python -X utf8 scripts/check_staging_config.py --env-file '<private-file-path>'
python -X utf8 scripts/run_staging.py --env-file '<private-file-path>'
```

Only after the operator has provisioned and reviewed the dedicated database,
schema/import and HTTPS reverse proxy can this start a local backend on8931:

```powershell
python -X utf8 scripts/run_staging.py --env-file '<private-file-path>' --serve
```

The launcher uses the explicit file and a minimal OS environment, so parent-shell
production credentials are not inherited. It does not run migrations/imports or
provision hosting. Port8930/local Beta is not stopped or repurposed.

## External operator steps

1. Choose an existing approved hosting allocation and separate staging hostname.
   Confirm any cost before activation; no new paid hosting is authorized.
2. Provision a fresh persistent PostgreSQL database and least-privilege staging
   role, separate secrets and synthetic test users. Check all ownership/grants.
3. Deploy only a reviewed committed branch/revision; run reviewed additive schema
   migrations and exact source imports explicitly. Record the deployed revision,
   schema revision and content hashes. Rehearse backup/rollback on staging.
4. Configure managed TLS or an approved reverse proxy for the staging hostname.
   Validate certificate chain, hostname, expiry, renewal and redirect behavior.
   No certificate has been issued or validated here. Do not bypass TLS checks.
5. Configure a **dedicated Google OAuth Web client** in an isolated test project
   or approved staging allocation. Consent screen: test audience/test accounts;
   scopes `openid email profile`. Put client ID/secret only in server secret
   configuration. Authorized redirect URI must exactly equal:
   `https://<staging-api-host>/auth/google-callback-mobile`.
   Backend uses state + S256 PKCE and single-use exchange grants, not tokens in
   deep-link URLs. Callback scheme is `ilmai-staging://auth/callback`.
6. Build the Android staging app with normal `main.dart`,
   `REVIEWED_MOBILE_RELEASE=true`, `MOBILE_STAGING=true`, and HTTPS `API_URL`.
   Gradle uses `com.ilmai.app.staging`/`ILM AI Staging`/`ilmai-staging` for staging;
   no Beta/test-login flag. Actual staging APK build/OAuth/device acceptance has
   not yet been completed. Production build keeps `com.ilmai.app`/`ilmai`.
   If adding native Google credentials, use the appropriate package and actual
   signing SHA; upload-key SHA does not prove Play App Signing certificate match.
7. Run read-only preflight against the staging origin. Exit0 only means API
   contract compatibility, never full acceptance. Keep the following matrix.

## Acceptance matrix — not yet hosted acceptance

| Area | Required evidence |
| --- | --- |
| Auth | New Google account, returning account, account switch, cancellation, network failure; no duplicate profile or cross-account data |
| Session | Relaunch, expired access/refresh, logout/relogin, revocation; saved progress retained |
| Catalogue | All five subjects visible for grades5–11; locks/labels from actual imported availability; no fabricated lessons |
| Lessons | Theory, MCQ/FRQ correct/incorrect, explanation only after checked feedback, retry/draft, idempotent completion/XP |
| Data | Preferences/progress isolation and restoration, no production data in staging |
| Deletion | Verified in-app and public web deletion, full data lifecycle/revocation, other users unaffected — implementation pending |
| Contract | All missing404 routes resolved by the intended deployed commit, old clients still compatible |
| Resilience | Timeout/offline, interrupted submit, retry, concurrent reward, source/grader drift rejected |
| Device | Real Android profile/release cold/warm startup, scrolling, large text, edge-to-edge, back navigation, signed upgrade |
| Store | Accurate privacy/Data safety/deletion URLs and Play signing/version evidence; no upload without owner permission |

Do not declare staging live, OAuth accepted, production fixed or release approved
until each corresponding real check has been performed and recorded.
