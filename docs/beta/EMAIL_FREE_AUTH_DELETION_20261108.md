# Email-free authentication and owner-verified deletion — staging acceptance

2026-11-08. This supersedes the earlier mandatory staging sender setup.
No Brevo/Resend account, paid resource, mailer credential or automatic email was
created.10,000 users is an operator review milestone, never an automatic toggle.
Production deployment, DB changes and Play upload remain separately gated.

## Latest corrective work (supersedes earlier pending artifact notes)

Android source7a2e37e registers both exact auth/deletion callback routes.
The corrected arm64 staging APK installed with `install -r` Success; native
resolution accepts both routes and rejects `/deletion/other`. Owner selection
returned to the app, but backend verification denied the response; no proof or
DELETE request was issued. The third disposable account remains intact.

The backend correction below uses fresh application OAuth issuance, not Google
Account session age.17 real-RSA/privacy regression tests passed; the broader
SQLite/PostgreSQL suite and new-source full CI are pending at this checkpoint.
Never reuse the parent's5356 CI pass as a result for this runtime correction.

Current production candidate `ILM-AI-1.0.3-code4-7a2e37e-NO-GO.aab` is77581578
bytes, SHA256 `0b34f08354eeeae7167478f998074f4a6bd5f52e39834ce2f006c9f47199b911`.
Bundletool/JAR signature, existing upload certificate, package/version, exact
callback filters,16KiB native alignment and bounded secret checks passed.
This is artifact verification, not production deployment or Google acceptance.
Flutter full suite is still running; targeted37 and analyze clean are observed.

## Runtime contracts

- `EMAIL_FREE_AUTHENTICATION=true` opts into password signup/login without email
  OTP. It does **not** pretend the mailbox was verified. Google login still uses
  its existing verified provider subject/PKCE exchange/session mechanism.
- An unverified password signup cannot silently claim/link another person's
  Google identity by email. Existing provider-subject matches continue normally.
- Password reset verification is retained. Without a configured delivery service,
  email-free mode returns the same503 for every reset-request address; it never
  says a code was sent or permits reset using only an email. Minimal transactional
  recovery delivery remains optional infrastructure for password users who lose
  their password. Google users use Google's own recovery.
- `EMAIL_FREE_ACCOUNT_DELETION=true` removes only the email-delivery prerequisite
  for the new flow. The existing deletion-enabled, DB, dedicated secret,
  policy-reference, storage and write-barrier checks remain.0018 must be applied.
- Original OTP routes remain compatible with older clients when a sender exists;
  the current app checks actual server capabilities and uses the new flow when
  offered. Network/configuration failure does not silently fall back to a weaker
  proof or show deletion success.

## New deletion authorization

1. Mobile starts with an authenticated, active owner. Password users re-enter
   their current password, checked with the existing server password verifier.
   Google users complete a separate OAuth authorization with state, nonce and
   account selection, through the already registered callback.
2. Google ID token RS256 signature, issuer, audience/azp, expiry, nonce and fresh
   signed issuance time (`iat`) are checked against the current five-minute
   window and this exact flow's creation time. Missing/stale required claims
   fail closed. Ownership uses only
   the exact linked provider subject. No account creation or email linking here.
3. The browser callback contains only a90-second one-use code, PKCE-bound to the
   initiating client. A deletion code never becomes a normal login/session grant.
   Web callback uses a fragment removed immediately; app callback uses the
   separate `/deletion/callback` purpose. Proofs are not put in URLs or logs.
4. Exchange produces a five-minute, purpose/owner-bound deletion proof. Password
   or identity changes invalidate it. The user then explicitly confirms permanent
   deletion. A fresh mobile confirmation still requires a valid owner session.
5. The existing transactional purge/revocation and durable file-cleanup path is
   reused. A lost response can be retried with the same narrow proof after
   revocation. Other-user proof use is denied. Partial cleanup/financial retention
   is reported honestly, never as completed deletion.

Google Account session `auth_time` is optional and is not the application's
reauthentication time. An existing Google browser session can authorize a new
application response; this flow does not claim fresh Google password/MFA entry.
Google does not support forcing Google Account reauthentication with `max_age`.
The new signed, nonce-bound response, exact linked subject, owner session, PKCE,
one-use grant and separate final consent establish recent application approval.
Old/cached ID tokens cannot substitute for that response. If optional `auth_time`
is present, malformed/future values are rejected. See the official distinction:
https://developers.google.com/identity/siwg/security-bundle .
Failures log only fixed allowlisted categories, never token/claim/exception text.

## Web and manual review

The external `/account-deletion` page supports Google, password and a separate
manual request when the account cannot be accessed. A manual request is an
encrypted review ticket, **not identity proof and not deletion authorization**.
Knowing an email cannot delete, block or change an account. No provider login,
password, verification code or identity document belongs in its reason field.

Operator procedure: inspect a ticket through an authorized private process,
establish ownership using independently verified evidence, document the result,
and preferably have the owner complete ordinary account recovery and the fresh
authenticated deletion flow. Never mint a deletion proof from the ticket/email
alone. No public ticket listing, admin bypass or automatic manual deletion exists.
Actual support staffing/contact and processing/retention commitments require the
owner's policy approval before claiming this pathway operational in production.

## Data retained and privacy review

Original identity, profile, password/provider subject, tokens, progress, answers
and owned data are purged through the existing inventory. Minimal non-reusable
UID tombstones remain to prevent stale requests recreating users. Pending cleanup
jobs retain the minimum retry data; completed jobs clear email hashes. Expired
reauth bindings are removed before their challenge rows by the existing cleanup
worker (one day after expiry). Manual ticket contact/reason is encrypted and
purged when a matching verified account is deleted; other pending tickets require
operator retention handling. These are actual implementation behaviors, not an
approved legal retention promise or a claim that provider backups are erased.

Financial retention, backups, external processors, tombstones and pending manual
ticket retention need explicit Privacy Policy/Data safety reconciliation. Do not
invent a statutory period or call a blocked account deleted.

## Staging acceptance boundary

Keep A30 XP/two lessons and B20 XP/one lesson unchanged. The owner has added a
third Google test account for an actual destructive staging test. Google account
selection/password/2FA/consent remains with the owner. Only a clearly identified
disposable third account may be deleted after explicit final consent.

Current baseline numbers1375 Flutter and5334 backend are historical parent-source
results. New-source test, deploy and APK evidence is recorded separately below.
Real third-account Google reauthentication/deletion remains pending; do not infer
it from the password/API acceptance.

## Current observed checkpoint

- Backend source `fd44385d40a5b0258ee0206c6daa64ef31408362` is actually Live on
  isolated Free staging, deploy `dep-dbnvte0u01pc73dt17rg`; auto-deploy remains off.
  Production remains `e97c029f341da172fc753ab07b44b783cdf13b5f`, with unchanged
  environment. No production database/deploy or Play action was performed.
- Before additive staging migration0018, a TLS-verified custom PostgreSQL backup
  was saved privately outside Git. All11 learner tables/39 rows compared unchanged
  across the migration. External DB access was closed again in a finally block.
  The backup was actually restored into a disposable loopback database: original
 0017 head and11 tables/39 learner rows verified; temporary restore DB dropped.
  This is staging-backup evidence, not a production-backup/restore acceptance.
- Exact-Live read-only mobile preflight: **9/9**. Real HTTPS disposable-password
  acceptance: **29/29**, including signup without email, same-account login,
  fresh password proof, other-owner403, invalid-session401, missing-consent400,
  actual app/web deletion, token/refresh revocation, safe idempotent retry and
  manual request not disabling an account. Both newly generated synthetic
  accounts were deleted; prior A/B accounts were not used in these HTTP tests.
  Password recovery honestly returns the same503 for known/unknown addresses.
- Local backend regression checkpoints:111 passed on SQLite/loopback PostgreSQL
  with migration-chain coverage; later69 passed for new guards/worker/auth cases;
  latest RSA identity/token checks11 passed. These overlap, so are not summed.
  Exact-source full Linux CI42446994077 succeeded: **5356 passed,75 skipped,
 21 warnings** in6150.04s; import and Docker build passed. Skips are not passes.
- Flutter source `984a825b3b39b2d0a5b316ff1f57d21309556850`: targeted43 passed;
  full analyze `No issues found`; **1390 full serial tests passed** in26:25.
  Current staging-flag regressions are running separately. Debug staging
  APK build passed in279.2s. Separate package `com.ilmai.app.staging`,1.0.3/code4,
  SHA256 `808876b2a197d953ee76999d063a047f14c336ac2cd6bfa073fb3351955dc0d3`,
 209859628 bytes/200.14MiB. Exact OAuth values/checked credential formats:0 hits
  across676 ZIP entries. `adb install -r` returned Success, no uninstall/clear.
- Samsung after update restored A's30 XP/two lessons and20-XP daily goal. The
  deploy-time catalogue timeout is retained as a failure sample; explicit retry
  loaded the catalogue. This is not a production startup/performance signoff.

### Later phone-discovered auth-expiry fix

The first third-account Google attempt returned after more than10 minutes. Bounded
staging logs showed a callback307 and no mobile exchange; the app incorrectly
labelled its browser timeout as a waking server. This was not accepted as login.
Fresh owner-completed Google login reached a separate new onboarding successfully.
Third-account age/profile completion and actual deletion remain in progress.

Flutter `b6f604aa510a5e25f2ca34b02f216b7efd495bd4` now distinguishes browser expiry
from a network/server timeout, with localized retry guidance. OAuth flow/grant TTL,
identity, state, callback scheme and PKCE guards are unchanged. Callback fixtures
now use the actual configured scheme and explicitly reject the other app scheme.
Full new-source **1392 tests passed** in11:05; targeted61 passed (overlap), full
analyze `No issues found` in91.3s. Final b6f604a staging-flag regressions **99/99**
passed in1:30. These counts overlap; the preceding98 pass remains historical.

New Samsung arm64 staging APK built in255.4s:1.0.3/code4,
`ILM-AI-Staging-1.0.3-code4-b6f604a-arm64.apk`,109715231 bytes/104.63MiB,
SHA256 `1210bfbf82e7807b1851b3e2e0a0489fa5754ef598daaadfa65cc1fad9abc1c1`.
674 ZIP entries checked;0 exact OAuth/checked credential-format hits. New APK
installation returned `Success` with `adb install -r` after the third-account
onboarding finished. No app data was cleared. Post-update native deletion
acceptance remains in progress.

An upload-key-signed984a825 AAB candidate was built/validated, but is superseded
by this app fix. The new b6f604a AAB build is running; neither artifact has been
uploaded or approved. Existing production package/version/signing stay fixed.

### Actual native reauthentication callback defect — active fix

During real third-account deletion reauth the owner selected Google, but the
browser remained open. Staging health200/0.8s and bounded logs proved prepare200
and Google callback307; no deletion exchange followed. The installed Android
resolver found auth/callback but returned `No activity found` for deletion/callback.
The manifest registered only the auth host. Dart/mock tests alone missed this
cross-layer defect; earlier b6f604a APK/AAB are therefore superseded, not release-ready.

Flutter `7a2e37e86f34f0cfb0cd5e95a62a5e853244f7b4` adds a separate exact
scheme/host/path filter for deletion/callback to the same CallbackActivity. The
auth filter is preserved; no wildcard/prefix/path broadening or state/PKCE bypass.
A new static native contract reproduced the failure before the fix;37 targeted
native/deletion/login tests then passed. Full current suite and new APK are running;
actual post-install resolver and fresh Google deletion acceptance are still pending.
The owner manually closed the Google window; no auth screen was automated.

New AAB verification also checks both exact intent filters in the built manifest,
not merely the scheme string. Actual browser visual acceptance of the external
web page was attempted but the browser access host is unavailable; only the real
HTTPS API/static-asset acceptance is claimed. Production remains NO-GO.

Receipts are outside Git in `ilm-ai-beta-artifacts`: staging-email-free operations,
backup-restore, live-preflight, hosted-api-acceptance and APK JSON files dated
20261108. Private backup/OAuth credentials, identities and tokens are not included.

## Official requirements reviewed

- [Google Play account deletion](https://support.google.com/googleplay/android-developer/answer/13327111)
- [Google OpenID Connect reference](https://developers.google.com/identity/openid-connect/reference)
- [Google session metadata and auth_time](https://developers.googleblog.com/enhance-security-and-trust-new-session-metadata-in-sign-in-with-google/)

An in-app option and a working external deletion-request path are both required;
deactivation alone is not deletion. Email OTP is not the only ownership mechanism.
This engineering implementation does not itself establish Play policy approval.
