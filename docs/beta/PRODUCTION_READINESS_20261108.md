# ILM AI1.0.3 — current production release gates (2026-11-08)

## Latest accepted deletion correction

Staging Live597b5ac8a989d2c177ee22403f34ea36d7f6918e,
deploy dep-dboabch5efls73da7sj0: exact-source9/9 public contracts passed after
an honestly retained deploy-time timeout. No env/schema/DB change in deployment.
Owner-controlled Google reauth, separate final third-account deletion and same
Google relogin passed on Samsung with app source7a2e37e. A TLS read-only staging
DB check confirmed completed cleanup, personal-field scrubbing, zero owned rows
across40 tables/old refresh tokens, a distinct new zero-XP/zero-progress account,
and protected A30 XP/two lessons/B20 XP/one lesson preserved. ACL closed again.
Minimal immutable ID tombstone remains by design; no original provider subject.

New-source local backend110 regressions plus14 OAuth/migration tests passed.
Full CI42500888563 is still running; parent5356 pass is not its result.
Flutter1393 full tests passed in44:00, targeted37, analyze clean384.7s.
Native7a2e37e APK installed-r Success; matching AAB77581578 bytes passed signing,
package/version/callback/16KiB/secret checks. Earlier pending Google-deletion and
native-build notes below are historical. Production remains NO-GO: existing
production API/DB baseline/backup/migration/import/deploy approvals, privacy and
manual-support/retention/storage operations, signed-upgrade, provider and stable
performance gates remain. Production Livee97c029/main/Play are unchanged.

This is a readiness record for updating existing `com.ilmai.app`, not a first
publication and not permission to deploy or upload. Preserve1.0.3/code4 and the
existing verified signing identity. **Production remains NO-GO.**

## Confirmed current backend

- Recovery branch: `release/ilm-ai-1.0.3-recovery-20261107`.
- Staging Live source: `fd44385d40a5b0258ee0206c6daa64ef31408362` (email-free
  deletion update; see dedicated acceptance report).
- Staging service: `srv-dbniform8hqs73caemig`; deploy
  `dep-dbnvte0u01pc73dt17rg`; Free, auto-deploy off.
- Production service: `srv-d99id4mcjfls738a8l80`, still Live
  `e97c029f341da172fc753ab07b44b783cdf13b5f`, linked to `main` with auto-deploy on.
- Parent-source full Linux CI42395951490: **5334 passed,65 skipped,21 warnings**,
  5731.06s; import and Docker build successful. Skipped cases are not passes.
  Current fd44385 CI42446994077 succeeded:5356 passed,75 skipped,21 warnings
  in6150.04s; import and Docker build passed. This is separately observed evidence.
- Final awake-server preflight9/9 passes at the exact Live source. Earlier
  resume-timeout preflight is retained separately as a failed performance sample.
- Dedicated Google Web client, isolated Free PostgreSQL and strict staging config
  are verified; no production OAuth/env/database/deploy change was made.

CI: https://github.com/UMIDABDURAZZOQOV/ilm-ai/actions/runs/42395951490

Actual public catalogue read contains seven metadata rows: five published
subjects plus unavailable legacy `matematika`/`ona_tili` (no grades). The latter
are not claimed to have lesson content. Verified published grade availability:
Biology5–11, Physics6–11, Chemistry7–11, Uzbekistan History7–11, World History6–11.
No opening grade was guessed from the user's illustrative examples.

## Acceptance and remaining gates

| Area | Evidence | Remaining action before production |
| --- | --- | --- |
| Google identity/session | Two real owned Google accounts, A→B→A restoration; A30 XP/two lessons, B20 XP/one; no repeated onboarding | Old Play-signed client OAuth compatibility and broader concurrent-device acceptance |
| Learning/progress | Five-subject locks; both accounts complete MCQ/FRQ; correct/incorrect fallback and native semantics accepted; current Flutter1375 full tests/analyze clean | Actual production configuration and Play-signed update acceptance; see dedicated report |
| New routers | Full CI and exact staging contracts pass; real profile404 fixed without preview bypass | Production still old404; final separately authorized service update only after other gates |
| Existing production database | Read-only inventory:46 unversioned tables; isolated fresh-chain/import and synthetic structural rehearsal already tested | Reconcile actual baseline, verified backup/restore and explicit migration/import approval; never blanket stamp/create_all |
| Account deletion | New email-free staging enabled after additive0018/verified staging backup restore; HTTPS password/web acceptance29/29, two synthetic accounts actually deleted | Real third-account Google fresh reauth/deletion/relogin, support/retention/privacy/storage/worker acceptance still required; email sender is no longer a mandatory deletion prerequisite |
| Performance | Free HTTPS service resumed only after timeout/retry; app did not falsely report success | Stable hosting/cold-start acceptance and real release/profile measurement; no paid resource is authorized |
| External AI | Verified lesson fallback works on phone; no provider credential in APK | Valid private provider config plus audience/privacy/limits acceptance; no quota circumvention |
| Signing/update | Existing package/signing and latest Play code3 previously checked; targetcode4 | Actual Play-signed1.0.2→1.0.3 update, data preservation and final candidate artifact scan |
| Operator credentials | Values not in code/reports/APK; exact and format scans performed | Rotate previously chat-disclosed Render credential before production; owner deferred rotation |

## Production mutation approval packet — not yet approved

The backend candidate is `fd44385...`, not the old `main`. Do not push/merge
`main` merely to publish code: its linked production auto-deploy would run.
The final packet must identify exact source/service, reviewed DB baseline and
backup restore point, additive migration/import transaction, preserved secrets,
legacy/current API smoke commands and rollback. An old-code rollback must not
blindly downgrade/delete new tables or remove learner progress. Prepare a PR or
separate fix branch; do not force-push protected branches.

Required operator approvals remain production service update, production DB
mutation/import, any paid resource, and Google Play upload. Staging-only consent
does not authorize those actions. A locally built APK/AAB is not a GO decision.

Current actual phone/source/artifact details belong in
[Google staging acceptance](GOOGLE_STAGING_ACCEPTANCE_20261107.md). Earlier audit
sections that say hosting/OAuth are absent or the new-source CI is pending are
historical and superseded by this checkpoint.

Current email-free runtime/app checkpoints are in
[email-free authentication/deletion](EMAIL_FREE_AUTH_DELETION_20261108.md).
Flutter b6f604a full serial1392 passed in11:05, analyze clean; targeted61 and exact
staging-flag99 passed (counts overlap). The phone-discovered browser-expiry message
now distinguishes Google interaction expiry from a network/server timeout; OAuth,
state, identity and PKCE lifetime guards are unchanged. Parent984a825 is historical.
New separate
staging APK installed Success with A30 XP/two lessons preserved. A new production
AAB candidate is being built locally and is not approved for upload. The verified restore relates to the isolated staging backup,
not the unversioned production database. No mandatory Brevo/Resend setup is pending
under the owner's revised policy; secure lost-password delivery remains an honest
optional-infrastructure limitation.
