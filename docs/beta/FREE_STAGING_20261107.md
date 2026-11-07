# Free HTTPS staging recovery — 2026-11-07

Owner confirmed a $0 Render build spend limit and authorized only separate Free
PostgreSQL and Free web staging. No production deployment, production database
migration/import, paid resource, or Play upload is authorized by that approval.

## Latest OAuth/device checkpoint — 2026-11-08

Real HTTPS staging on Samsung SM-A125F now accepts two owner-approved Google
accounts, independent onboarding, restart/session restoration, A→B→A logout/login,
MCQ/FRQ and saved progress. A returned to30 XP/two lessons/20-XP goal; B independently
started atzero and completed Chemistry7 at12/12,+20 XP/one lesson/10-XP goal.
A's Chemistry result was11/12 and Physics5/6; correct/incorrect feedback and
optional reviewed explanations were observed. No identities or tokens are reported.

Three real fixes are accepted: route-extra restoration (`e3571d3`), reviewed
profile404 (`d587f9b`) and native FRQ semantics (`23f696f`, following470313d).
Current Flutter source23f696f: **1375 full tests passed** (serial38:33),105 default
targeted/10 reviewed contracts passed, full analyze **No issues found**.
Backend Live d587f9b: **5334 passed,65 skipped,21 warnings**, import/Docker passed
in CI42395951490. Awake exact-Live public preflight9/9 passed. Counts overlap and
must not be summed; the earlier interrupted Flutter attempt is retained separately.

Current installed artifact: `ILM-AI-Staging-1.0.3-code4-23f696f.apk`,180506516 bytes
(172.14 MiB), SHA2560268df56e4bee55d097dbb885a3b46c0ade13dd04322eda463257419c430abe2.
Separate staging package, install-r Success, no clear/uninstall, bounded credential
scan zero matches. Private OAuth file still has the doubled.json.json extension
and matches active staging. Free hosting/DB, auto-deploy off, deletion/test-auth/
preview flags off; no external AI key. Verified fallback works.

**Production NO-GO**: Live e97c029/main remains unchanged. Production baseline/
verified backup restore/migration/import/deploy approval, actual deletion sender/
policy/storage acceptance, Play-signed1.0.2 update/OAuth compatibility, provider
audience/configuration, exposed operator-key rotation and stable performance/
final production artifact acceptance remain. Free idle wake/timeouts are retained
as failures; no current cold-start SLA or artificial keepalive is claimed.
See backend `docs/beta/GOOGLE_STAGING_ACCEPTANCE_20261107.md` and
`docs/beta/PRODUCTION_READINESS_20261108.md` for current evidence and release gates.


## Source and hosting evidence

Authenticated Render reads confirm production service `srv-d99id4mcjfls738a8l80`
tracks `main`, with commit-triggered automatic deployment. Live commit is
`e97c029f341da172fc753ab07b44b783cdf13b5f`; failed deployment is
`e881930708fb04022dfa97a496167d8abf779bb2`. The latter changes README only.
The Live source predates the mobile routers, explaining their real HTTP404s.
This does not establish the historical failed-build cause (logs have expired).
Production uses a Neon PostgreSQL connection; it is not the new Render staging
database. Existing Google credentials are present, not accepted in a live test.

Release branch `release/ilm-ai-1.0.3-recovery-20261107` was safely pushed at
`186a096fd6a74695473b424148ece868b94dd0ee`, including the README-only main merge.
Production's linked branch and Live deployment were unchanged after that push.
No PR preview, force push, or main push was used. Outgoing objects were checked
for source PDFs, private database/credential artifacts and known secret formats;
only synthetic deterministic synthetic fixture literals were accepted.

## OAuth setup pending is not authentication acceptance

Default staging validation still requires a dedicated Google client. The explicit
`STAGING_AUTH_SETUP_PENDING=true` mode is allowed only in staging with **both**
Google credential values empty, test/preview login disabled, and deletion off.
All HTTPS, isolated database identity, signing secret and publication checks stay.
Missing/partial credentials are not filled with dummy or production values.

In this mode Google login returns503, auth config says `google_configured:false`,
and health reports `oauth_setup_pending:true`, `authentication_ready:false`.
No test login, fabricated user, or private-endpoint authorization is added. Public
catalogue, TLS, deployed revision and unauthorized route behavior can be tested.
Passing infrastructure checks never means Google/session/progress/deletion user
journeys were accepted. Enabling OAuth requires a dedicated client, setting this
flag false, redeploying only staging, and performing real test-account journeys.

Free resources must stay explicitly `plan:free`, automatic deploy/previews off,
no autoscaling, HA, replicas, paid disk or automatic paid fallback. Free PostgreSQL
expires after30 days; Free web sleeps when idle. Record the actual expiry and URL
from Render, and retain only synthetic staging accounts. Do not treat it as
durable production hosting or backup/recovery evidence.

Private Render credentials are entered with hidden terminal input and used only
in memory against the official API. API/DB secrets are never persisted in receipt
files. The owner deferred rotation of the chat-exposed key; rotation remains a
release gate, without stopping unrelated authorized staging preparation.

Actual resource IDs, URL, expiry, revision, tests and remaining external actions
must be appended after the corresponding operation succeeds; no live staging is
claimed merely by committing this document.

## Local configuration regression

71 staging-config/OAuth/preflight tests passed (one existing httpx deprecation
warning). After converting the imported pytest fixture into an explicit plugin,
all5 redirect tests passed again. These counts overlap. Changed-file Ruff checks
and Git whitespace validation pass. Docker build failure is no longer masked by
`continue-on-error` in CI. Full GitHub CI is tracked separately; pending is not
success.

New isolated Free database: `dpg-dbnib9dg1s2s73cpgab0-a`, PostgreSQL16, Oregon,
name `ilm-ai-103-staging-8b0727`, expires `2026-12-07T13:20:37Z`. Autoscaling and
HA are off; external access is restricted to the operator's single IPv4 address.
Creation succeeded; schema/import acceptance is recorded only after completion.

`scripts/initialize_fresh_render_staging.py` is an explicit one-time staging build
action bound to the new internal `dpg-*` identity, staging-only Render service,
empty users/content and strict pending-auth config. It refuses the production
service, external/other URLs, existing learner content and unknown schema; errors
never echo credentials. It reuses actual Alembic and source-validated importer,
without weakening the existing local-only import CLI. Remove this one-time action
from the new staging Build Command after it completes. Normal app startup still
does not migrate or import.13 offline target-guard cases passed. The external
operator run completed Alembic0017, then was interrupted during source validation
before import writes; its import must not be reported as passed.

## Hosted outcome (supersedes unprovisioned staging notes)

Free service `srv-dbniform8hqs73caemig` is live at
`https://ilm-ai-103-stage-8b0727.onrender.com`, initially deployed from
`686bf921c62c0f0d332ba9b401e8936e82805a23`. Auto deploy and previews are off.
Its one-time initialization completed Alembic0017 and imported Biology406,
Physics316, Chemistry268, Uzbekistan History172, World History219:1381 lessons.
Users0; progress rows modified0. The completed initialization action was removed
from future Build Commands. No production DB or user data was copied or written.

Real TLS chain/hostname verification succeeded with TLS1.3, certificate valid
through2026-12-20. Read-only hosted checks: health200 with exact SHA/contract2;
five subjects visible and correctly locked at every grade5–11; all subject grade
routes200; profile/tree without credentials401; unknown exchange grant400;
test-login404/no such route;46 mobile paths registered. Warm catalogue responses
were1.47–2.13s from this workstation, not device benchmarks.

The first catalogue request timed out after120s, although server logs later show
its200 completion. Local source-cache profile49s under cProfile identified the
strict whole-source validators as expensive. The fix prepares the SAME existing
process-local validated caches before reviewed startup accepts traffic. Validation
failure blocks startup; no source/DB/auth check is removed.13 startup/warmup tests
passed. This prevents early successful health before source preparation, **not**
the Free plan's idle spin-up latency. Cold hosted reacceptance is recorded only
after the corrected commit is deployed and probed.

Google remains unconfigured: config says false, login503, health explicitly says
authentication_ready:false. Normal release preflight correctly exits1/NO-GO on
that check, while its other8 checks pass. Dedicated staging client/test-account
journeys, deletion/mailbox, device/profile/signed upgrade and live NVIDIA remain
unaccepted. The owner has been given the exact Google Web OAuth redirect:
`https://ilm-ai-103-stage-8b0727.onrender.com/auth/google-callback-mobile`.
Only a private local credential-file path is requested, never secret chat text.

One additional synthetic legacy-format session test passed: old HS256 access and
stored refresh restore the same profile, cross-account access stays403, refresh
rotates once, logout revokes replacement,137 XP/progress remain and onboarding
is not repeated. This is not a Play-signed1.0.2 binary acceptance test. The old
Flutter main source expects tokens in callback URI; hardened backend requires
PKCE. The local code3 APK contains PKCE/exchange strings and was rebuilt after
the published release, so it cannot prove the actual Play1.0.2 auth contract.
Do not reintroduce bearer tokens in callback URLs to hide this rollout gate.

Production schema was inventoried in a TLS client connection with PostgreSQL
default_transaction_read_only=on, statement/lock timeouts and no user-row reads.
46 public tables, existing users/refresh columns, no Alembic version table and
no new curriculum/OAuth-grant/deletion tables. This is an existing unversioned
schema: **do not run initial CREATE migrations or blindly stamp head**. A verified
backup/restore, baseline reconciliation and additive migration rehearsal against
a structural clone are required before the owner can approve production rollout.
No production schema/data mutation was performed.

## Corrected startup deployment acceptance

`23d9ed355d916586e6cebf7fb2de3613348b4935` is confirmed Live on staging,
deploy `dep-dbnip9s9v7es73cstifg`, observed2026-11-07T13:54:46Z. The first
requests after that new process became ready: health200/exact SHA/contract2 in
0.80s; grade5 catalogue200 in4.06s; grade7 catalogue200 in2.52s; all five subjects
and correct locks; unauthorized tree401 in1.22s; Google configfalse in1.31s.
No initialization/import was rerun in this deployment. Normal source/DB guards
still execute, caches remain process-local, and idle wake/startup may still take
minutes on Free compute. This is not a device/startup SLA or production GO.

Local8930 Beta still responds200. Fresh read-only digest of all46 account/progress
tables exactly matches both prior `production-focus-beta-preservation` and
`blockers-beta-preservation-current` snapshots. ADB is empty. Central CLAUDE and
production audit handoffs were updated; no new APK/AAB was necessary for these
backend-only changes.

The observed46-table production structural clone was then rehearsed on loopback
PG with synthetic data: a0012 baseline hypothesis followed by additive0013–0017,
1381-lesson import/reimport, unchanged user42/137 XP/progress and0 reimport inserts.
No production rows were read/copied or changed. See the precise scope and remaining
baseline/backup gates in [the unversioned schema report](PRODUCTION_UNVERSIONED_SCHEMA_20261107.md).
Dedicated Google client setup steps: [operator guide](GOOGLE_STAGING_OPERATOR_SETUP.md).

After initialization, the new staging database's temporary operator IPv4 rule
was removed: external access is now disabled; the same-region staging service
uses its private internal TLS connection. Plans remain Free, HA/autoscaling off,
auto deploy off, Google credentials absent. Final hosted receipt records actual
Live hashes for staging and production without credential values.

Free staging shares this workspace's750 monthly instance hours with its existing
Free service. No artificial keepalive or repeated monitoring loop is left running;
idle staging can sleep. Build spend limit $0 was confirmed by the owner, not a
universal bandwidth/billing guarantee. No paid compute/database/HA/disk was enabled.
See [Render Free usage limits](https://render.com/docs/free#monthly-usage-limits).

## Later cold-host / full-CI evidence (supersedes pending-only notes)

After idle, a real HTTPS health request took188.41s before returning the exact
23d9ed3/contract2 response; catalogue then returned200 in5.81s with external DB
access closed. Local Beta stayed200 and the owned test PG was confirmed stopped.
This is a measured Free cold-wake limitation, not a resolved production startup
SLA. No keepalive is left running to consume shared Free instance hours.

The oldest full Linux CI finished:5224 passed,2 failed,64 skipped,77 fixture errors,
4481.79s. Its two frozen-file failures and fixture-root causes were diagnosed;
see [the exact runtime review and fixture corrections](SHARED_RUNTIME_INTEGRATION_REVIEW_20261107.md).
Known-obsolete three runs were canceled (202 accepted) before starting a corrected
run. The first failure remains recorded; no full-suite pass is claimed.
