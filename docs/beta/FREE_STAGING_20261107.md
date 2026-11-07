# Free HTTPS staging recovery — 2026-11-07

Owner confirmed a $0 Render build spend limit and authorized only separate Free
PostgreSQL and Free web staging. No production deployment, production database
migration/import, paid resource, or Play upload is authorized by that approval.

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
only synthetic `nvapi-synthetic-test-only-*` fixture literals were accepted.

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
