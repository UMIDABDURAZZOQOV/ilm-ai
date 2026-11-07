# Verified account deletion — implementation and deployment gate

Local implementation, 2026-11-07. **Not enabled on production or the running
8930 Beta. No real account has been deleted for testing.**

## Contract

- Settings → Delete account → permanent-deletion consent → email code → explicit
  submit. Password and Google accounts both prove current mailbox possession.
- Authenticated `POST /account/deletion/me/request` resolves identity from the
  bearer token. There is no caller-supplied account ID.
- Public `/account-deletion` works without installing the app. Its request and
  confirmation endpoints use JSON bodies, never URL credentials. Unknown-address
  responses do not disclose account existence. Email delivery timing is not
  claimed to be indistinguishable.
- Ten-minute HMAC-protected, one-use code; five verification attempts; persistent
  per-peer hourly request limit and per-address cooldown. Trusted proxy/IP limits
  and production abuse monitoring still require operator acceptance.
- Verification, owned DB rows, progress/answers and session revocation are one
  transaction. Shared curriculum and unrelated learners' own progress remain.
- An immutable, scrubbed account-ID tombstone prevents ID reuse and stale-token
  resurrection. Original email, Google subject, password, name, age, push token,
  profile picture and learning totals are removed from that row.
- Per-account files use a durable pending-cleanup job. Locked, unsafe or unknown
  file layouts return `pending_cleanup`, never false success. The app clears only
  the deleted UID's preferences/drafts and secure session, and blocks queued cache
  writes. A receipt cannot log out a new session to the same/different account.
- Re-registration creates a fresh ID/profile with zero progress. It cannot recover
  the deleted profile. Ordinary logout preserves progress as before.
- Financial records/non-free accounts enter `retention_review`: **not deleted or
  revoked**. An operator must establish the actual legal retention and response
  process. Do not advertise automated paid-account deletion as complete.

## Deployment prerequisites

1. Approved staging isolation and an owned persistent PostgreSQL DB. Run the full
   Alembic chain through `0017_runtime_foundation` there first. Existing deployments
   need schema/revision inventory and backup/restore rehearsal; never blindly
   stamp an unversioned DB. No production migration permission is implied.
2. `ACCOUNT_DELETION_ENABLED=true` only after acceptance;
   `ACCOUNT_DELETION_SECRET` is a new, private, random secret of at least 32 chars;
   `ACCOUNT_DELETION_POLICY_REFERENCE` identifies the approved policy/review.
   Never reuse JWT secrets or print/store keys in Git, APKs or reports.
3. `ACCOUNT_DELETION_STORAGE_ROOT` is an absolute real directory. Production
   runtime requires it to equal the backend working directory, since legacy
   writers use relative paths. Symlinks/reparse points are rejected. Persistent
   storage and worker access must survive deployment/restart.
4. Configure a dedicated verified test sender using existing Brevo, Resend or Gmail
   support. Use only owned staging inboxes. A configured key is not proof of email
   delivery; test real delivery, expiry, retry and provider failure.
5. Check `GET /account/deletion/config` (`available=true`) and the external web page
   through the actual HTTPS origin. Add that deployed URL in Play Console only
   after real acceptance. The page is now hosted on isolated HTTPS staging (200), but its capability
   config returns available=false. Production still runs old code. No real OTP
   delivery or account deletion acceptance is implied.
6. Cleanup retry is scheduled every minute when enabled on the normal runtime.
   Staging intentionally disables general scheduling: invoke
   `services.account_deletion_worker.process_pending(db)` from an isolated operator
   job with the same private configuration. It only retries verified existing jobs.
7. Confirm all personal-data stores, external processors, backups and legal
   retention periods against the actual deployment. Security tombstones and job
   receipts retain identifiers/timestamps, not original identity. Set and publish
   their approved retention periods; no invented legal duration is supplied here.

## Privacy/Data safety reconciliation — owner review required

This is an implementation inventory, not an approved legal policy or a submitted
Play declaration. The app's existing privacy link remains unchanged. Before GO,
update its published policy to match this flow, public deletion URL, operator
contact, deadlines, backup lifecycle, financial review and minimal security
retention. Do not claim immediate physical erasure from provider backups.

Review at least: Google identity/name/email/profile; age and learning preferences;
answers, progress/XP and lesson activity; optional FCM token/device delivery;
support/feedback; any enabled media/upload, purchase and AI services. Presence of
a Flutter SDK dependency does not alone prove that it transmits data: inspect
the actual release configuration and network behavior. NVIDIA trial is backend
only and is not enabled/accepted for production here. Include real enabled
processors and children's/audience requirements; do not infer approval from mocks.

Official review references:
- https://support.google.com/googleplay/android-developer/answer/13327111
- https://support.google.com/googleplay/android-developer/answer/10787469

## Evidence boundaries

Synthetic SQLite/PostgreSQL tests cover password/Google deletion, OTP/consent,
expiry, invalid attempts, isolation, revocation, rollback, re-registration, stale
writes, missing barriers, file retries and cleanup worker. Flutter tests cover
consent/OTP, honest result states, failure handling, UID-scoped cache cleanup and
session generation protection. These are not real Google, mailbox, phone,
hosted HTTPS, backup-erasure or legal-policy acceptance.

Final receipts: backend lifecycle32 passed on SQLite/PostgreSQL, plus2 additional
cached-file-auth rejection cases; Flutter20 final targeted cases passed, including
the reproduced/fixed Uzbek200% text/keyboard dialog overflow, exact-UID cleanup and
same-UID new-session generation protection. Configuration/startup/email42 passed.
Full Flutter1359 passed before the final responsive dialog fix, followed by the
targeted20 and clean final analyze. Code commits: backend `b4e138a`, Flutter
`ac168c3`. Full report: `FINAL_FIX_PROGRESS_20261107.md`.
