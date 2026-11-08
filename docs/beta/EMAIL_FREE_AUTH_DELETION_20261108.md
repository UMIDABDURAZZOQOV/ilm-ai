# Email-free authentication and owner-verified deletion — active work

2026-11-08. This supersedes the earlier mandatory staging sender setup.
No Brevo/Resend account, paid resource, mailer credential or automatic email was
created.10,000 users is an operator review milestone, never an automatic toggle.
Production deployment, DB changes and Play upload remain separately gated.

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
   Google users complete a separate OAuth authorization with state, nonce,
   max_age=0 and requested auth_time, through the already registered callback.
2. Google ID token RS256 signature, issuer, audience/azp, expiry, nonce and fresh
   auth_time are checked. Missing/stale claims fail closed. Ownership uses only
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
results. New-source test, deploy and APK evidence must be recorded separately.
No new live deletion/Google reauth acceptance is claimed by this draft.

## Official requirements reviewed

- [Google Play account deletion](https://support.google.com/googleplay/android-developer/answer/13327111)
- [Google OpenID Connect reference](https://developers.google.com/identity/openid-connect/reference)
- [Google session metadata and auth_time](https://developers.googleblog.com/enhance-security-and-trust-new-session-metadata-in-sign-in-with-google/)

An in-app option and a working external deletion-request path are both required;
deactivation alone is not deletion. Email OTP is not the only ownership mechanism.
This engineering implementation does not itself establish Play policy approval.
