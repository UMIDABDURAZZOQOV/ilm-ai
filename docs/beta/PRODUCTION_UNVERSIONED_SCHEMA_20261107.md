# Existing production schema: rollout is blocked until reconciliation

## Verified read-only evidence

Authenticated hosting metadata points to Neon. Inspection used libpq verified
TLS1.3, `default_transaction_read_only=on`, statement/lock timeouts, and only
information_schema/pg_stat_ssl/Alembic metadata. No learner/account rows were read
and no DDL, import, backup restore or account mutation ran on production.

There are46 public tables and no `alembic_version`. Existing users and stored
refresh-token columns are present. These runtime-foundation tables are missing:

- curriculum_chapters, curriculum_courses, curriculum_lesson_sources,
  curriculum_topics
- mobile_login_grants, oauth_states
- study_events, study_sessions, user_study_preferences

Assessment-v2, Chemistry/history engine and deletion tables are also absent.
This list does not prove every existing column/index/constraint matches the
candidate. Read-only metadata is not a backup or data-integrity acceptance test.
Neon's server-side pg_stat_ssl can report false behind a TLS-terminating proxy;
the client's independently checked libpq TLS connection was true/TLS1.3.

## Required safe preparation before requesting production approval

1. Obtain and rehearse the owner's authorized backup/restore procedure. Do not
   copy production learner data into the public Free staging instance. Use an
   approved private recovery destination when real restore verification is needed.
2. Export **schema only** through a reviewed read-only connection. Compare all
   types, nullability, defaults, PK/FK/unique/index definitions and extensions.
   Create a structural clone on owned loopback PostgreSQL with synthetic users.
3. Reconcile the observed legacy baseline against each migration through0012.
   Version metadata may only be established after an explicit reviewed mapping
   proves those historical effects are already present. Do not blindly stamp
   head or run initial CREATE migrations over populated existing tables.
4. Rehearse the candidate additive0013–0017 path on that structural clone. Any
   type/nullability/key/uniqueness conflict must fail review before writes. Keep
   stable account/provider/lesson IDs, current JWT/session secrets and old rows.
5. Prove synthetic old-session refresh/logout, account isolation,137 XP/history
   preservation, additive import/reimport and idempotent completion. Existing
   fresh-schema rehearsals do not substitute for this clone acceptance.
6. Separately accept dedicated HTTPS/Google staging, real mailbox/deletion,
   actual Play1.0.2 signed upgrade/auth contract and device/profile performance.
   Record the completed full CI result; pending is not passed.
7. Present exact reviewed release SHA, migration/import SQL/diff, approved
   backup, affected service and rollback plan for the owner's final approval.
   No production command is authorized by this document.

Application rollback can restore the recorded previous code revision while
retaining compatible additive tables and newer learner progress. Never issue a
destructive downgrade or overwrite live progress with an older database restore.
The existing release signing/package/version4 reservation remains unchanged.

## Completed structural-clone rehearsal (14:08:30Z)

All46 actual public table definitions were reflected through the read-only TLS
connection, without user rows. A fresh random schema in owned loopback PG55461
recreated those columns/keys/defaults/indexes; serial PK sequences were rebound
to local clone sequences. Schema-only SQL stayed outside Git in local artifacts.
SHA256: `07552cd0a837194cd29b3281bc5a23234d7981b8c6bbcf75697c585507392fcc0`.

Only in that fresh local clone, the0012 historical-baseline **hypothesis** was
marked and additive0013–0017 applied successfully. A synthetic existing user42,
one legacy fixture lesson,137 XP and progress survived source-validated1381-lesson
import and idempotent reimport. Reimport inserted0 Biology/0 reviewed rows and
modified0 progress rows; total1382 includes the single legacy fixture. The owned
temporary schema was dropped after the run, not any production object.

Receipt: `ilm-ai-beta-artifacts/production-structural-clone-rehearsal-20261107.json`.
This proves additive path compatibility with the observed structure and synthetic
data. It does not prove actual legacy data uniqueness, backup/restore, historical
migration effects or authorize a production baseline/stamp. Those review gates
above remain. The first operator attempt stopped when its local test cluster
was unavailable; after restoring that owned cluster, the complete run passed.
