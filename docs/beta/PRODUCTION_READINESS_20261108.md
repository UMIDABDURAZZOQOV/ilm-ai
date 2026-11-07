# ILM AI1.0.3 — current production release gates (2026-11-08)

This is a readiness record for updating existing `com.ilmai.app`, not a first
publication and not permission to deploy or upload. Preserve1.0.3/code4 and the
existing verified signing identity. **Production remains NO-GO.**

## Confirmed current backend

- Recovery branch: `release/ilm-ai-1.0.3-recovery-20261107`.
- Staging Live source: `d587f9b56cb9aa54fb35f6bbf92af9dcf7a285f9`.
- Staging service: `srv-dbniform8hqs73caemig`; deploy
  `dep-dbnlssm417fc73e49rn0`; Free, auto-deploy off.
- Production service: `srv-d99id4mcjfls738a8l80`, still Live
  `e97c029f341da172fc753ab07b44b783cdf13b5f`, linked to `main` with auto-deploy on.
- New source full Linux CI42395951490: **5334 passed,65 skipped,21 warnings**,
  5731.06s; import and Docker build successful. Skipped cases are not passes.
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
| Account deletion | SQLite/PostgreSQL local tests; stage flag remains off | Public staging HTML/config200 with available=false; real OTP sender/mailbox, retention/privacy/storage/worker acceptance and owned deletion journey still required |
| Performance | Free HTTPS service resumed only after timeout/retry; app did not falsely report success | Stable hosting/cold-start acceptance and real release/profile measurement; no paid resource is authorized |
| External AI | Verified lesson fallback works on phone; no provider credential in APK | Valid private provider config plus audience/privacy/limits acceptance; no quota circumvention |
| Signing/update | Existing package/signing and latest Play code3 previously checked; targetcode4 | Actual Play-signed1.0.2→1.0.3 update, data preservation and final candidate artifact scan |
| Operator credentials | Values not in code/reports/APK; exact and format scans performed | Rotate previously chat-disclosed Render credential before production; owner deferred rotation |

## Production mutation approval packet — not yet approved

The backend candidate is `d587f9b...`, not the old `main`. Do not push/merge
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
