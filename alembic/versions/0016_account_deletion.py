"""Verified deletion state and write barriers; no account is deleted by migration.

Revision ID: 0016_account_deletion
Revises: 0015_reviewed_subject_schemas
"""

from alembic import op
import sqlalchemy as sa

revision = "0016_account_deletion"
down_revision = "0015_reviewed_subject_schemas"
branch_labels = None
depends_on = None
MARKER = "__account_deleted__"
# Pinned ownership inventory. Update via a NEW migration if ownership changes.
OWNERS = {
    "assistant_messages": ("user_id",),
    "flashcard_decks": ("user_id",),
    "share_links": ("user_id",),
    "streak_freezes": ("user_id",),
    "assistant_memories": ("user_id",),
    "vectors": ("user_id",),
    "quiz_sessions": ("user_id",),
    "learning_plans": ("user_id",),
    "user_courses": ("user_id",),
    "review_items": ("user_id",),
    "checkout_sessions": ("user_id",),
    "refresh_tokens": ("user_id",),
    "llm_logs": ("user_id",),
    "sat_ielts_questions": ("created_by",),
    "sat_ielts_sessions": ("user_id",),
    "sat_ielts_score_predictions": ("user_id",),
    "sat_ielts_user_prefs": ("user_id",),
    "ielts_writing_submissions": ("user_id",),
    "ielts_speaking_submissions": ("user_id",),
    "ielts_mock_tests": ("user_id",),
    "skilltree_user_lesson_progress": ("user_id",),
    "ielts_starred_words": ("user_id",),
    "skilltree_user_unit_exams": ("user_id",),
    "skilltree_user_language_levels": ("user_id",),
    "skilltree_mistakes": ("user_id",),
    "skilltree_daily_challenges": ("user_id",),
    "skilltree_lesson_attempts": ("user_id",),
    "study_sessions": ("user_id",),
    "study_events": ("user_id",),
    "mobile_login_grants": ("user_id",),
    "skilltree_mock_exams": ("user_id",),
    "skilltree_classes": ("teacher_id",),
    "skilltree_class_members": ("student_id",),
    "skilltree_family_codes": ("child_id",),
    "skilltree_parent_links": ("parent_id", "child_id"),
    "user_study_preferences": ("user_id",),
    "curriculum_progress_v2": ("user_id",),
    "chemistry_preview_progress": ("user_id",),
    "world_history_preview_progress": ("user_id",),
    "uzbekistan_history_preview_progress": ("user_id",),
    "beta_test_identities": ("user_id",),
}
ANSWERS = (
    "curriculum_answers_v2",
    "chemistry_preview_answers",
    "world_history_preview_answers",
    "uzbekistan_history_preview_answers",
)


def tables():
    metadata = sa.MetaData()
    sa.Table("users", metadata, sa.Column("id", sa.Integer, primary_key=True))
    challenge = sa.Table(
        "account_deletion_challenges",
        metadata,
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("email_hash", sa.String(64), nullable=False, index=True),
        sa.Column("code_hash", sa.String(64), nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False),
        sa.Column("consumed", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    job = sa.Table(
        "account_deletion_jobs",
        metadata,
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("email_hash", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
    )
    bucket = sa.Table(
        "account_deletion_rate_buckets",
        metadata,
        sa.Column("key_hash", sa.String(64), primary_key=True),
        sa.Column("count", sa.Integer, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    return [challenge, job, bucket]


def ownership_rules():
    rules = [
        (table, column, "direct") for table, cols in OWNERS.items() for column in cols
    ]
    return (
        rules
        + [(table, "session_id", "session") for table in ANSWERS]
        + [
            ("skilltree_class_assignments", "class_id", "class"),
            ("skilltree_class_members", "class_id", "class"),
        ]
    )


def validate_ownership_columns(connection):
    inspector = sa.inspect(connection)
    names = set(inspector.get_table_names())
    for table, column, _ in ownership_rules():
        if table in names and column not in {
            c["name"] for c in inspector.get_columns(table)
        }:
            raise RuntimeError("account_ownership_schema_requires_review")


def install_barriers(connection):
    validate_ownership_columns(connection)
    names = set(sa.inspect(connection).get_table_names())
    dialect = connection.dialect.name
    if dialect not in {"sqlite", "postgresql"}:
        raise RuntimeError("account_deletion_database_not_supported")
    if dialect == "postgresql":
        connection.exec_driver_sql("""
        CREATE OR REPLACE FUNCTION account_owner_write_guard() RETURNS trigger
        LANGUAGE plpgsql AS $$ DECLARE owner_id integer; marker text; BEGIN
          IF TG_ARGV[1] = 'session' THEN
            SELECT user_id INTO owner_id FROM study_sessions WHERE id = to_jsonb(NEW)->>TG_ARGV[0];
          ELSIF TG_ARGV[1] = 'class' THEN
            SELECT teacher_id INTO owner_id FROM skilltree_classes WHERE id = (to_jsonb(NEW)->>TG_ARGV[0])::integer;
          ELSE owner_id := (to_jsonb(NEW)->>TG_ARGV[0])::integer;
          END IF;
          IF owner_id IS NULL AND TG_ARGV[1] = 'direct' THEN RETURN NEW; END IF;
          SELECT oauth_provider INTO marker FROM users WHERE id = owner_id FOR KEY SHARE;
          IF NOT FOUND OR marker = '__account_deleted__' THEN
            RAISE EXCEPTION USING ERRCODE = '23514', MESSAGE = 'account_deleted';
          END IF;
          RETURN NEW;
        END $$;
        CREATE OR REPLACE FUNCTION account_tombstone_guard() RETURNS trigger
        LANGUAGE plpgsql AS $$ BEGIN
          IF OLD.oauth_provider = '__account_deleted__' THEN
            RAISE EXCEPTION USING ERRCODE = '23514', MESSAGE = 'account_deleted';
          END IF;
          IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
          RETURN NEW;
        END $$;
        """)
        connection.exec_driver_sql(
            "DROP TRIGGER IF EXISTS account_guard_users ON users"
        )
        connection.exec_driver_sql(
            "CREATE TRIGGER account_guard_users BEFORE UPDATE OR DELETE ON users FOR EACH ROW EXECUTE FUNCTION account_tombstone_guard()"
        )
    else:
        for action in ("UPDATE", "DELETE"):
            connection.exec_driver_sql(
                f"CREATE TRIGGER IF NOT EXISTS account_guard_users_{action.lower()} BEFORE {action} ON users WHEN OLD.oauth_provider = '{MARKER}' BEGIN SELECT RAISE(ABORT, 'account_deleted'); END"
            )
    rules = ownership_rules()
    for table, column, kind in rules:
        if table not in names:
            continue
        if column not in {c["name"] for c in sa.inspect(connection).get_columns(table)}:
            raise RuntimeError("account_ownership_schema_requires_review")
        trigger = "account_guard_" + table + "_" + column
        if dialect == "postgresql":
            connection.exec_driver_sql(f"DROP TRIGGER IF EXISTS {trigger} ON {table}")
            connection.exec_driver_sql(
                f"CREATE TRIGGER {trigger} BEFORE INSERT OR UPDATE ON {table} FOR EACH ROW EXECUTE FUNCTION account_owner_write_guard('{column}', '{kind}')"
            )
        else:
            expression = f"NEW.{column}"
            if kind == "session":
                expression = (
                    f"(SELECT user_id FROM study_sessions WHERE id = NEW.{column})"
                )
            if kind == "class":
                expression = f"(SELECT teacher_id FROM skilltree_classes WHERE id = NEW.{column})"
            for action in ("INSERT", "UPDATE"):
                connection.exec_driver_sql(
                    f"CREATE TRIGGER IF NOT EXISTS {trigger}_{action.lower()} BEFORE {action} ON {table} WHEN NEW.{column} IS NOT NULL BEGIN SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM users WHERE id = {expression} AND COALESCE(oauth_provider, '') <> '{MARKER}') THEN RAISE(ABORT, 'account_deleted') END; END"
                )


def upgrade():
    connection = op.get_bind()
    names = set(sa.inspect(connection).get_table_names())
    if "users" not in names or "oauth_provider" not in {
        c["name"] for c in sa.inspect(connection).get_columns("users")
    }:
        raise RuntimeError("account_deletion_requires_user_identity_schema")
    # Existing installations are checked before creating any new table.
    import importlib.util
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "pinned_schema_check",
        Path(__file__).with_name("0015_reviewed_subject_schemas.py"),
    )
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    validate_ownership_columns(connection)
    for table in tables():
        if table.name in names:
            helper.validate_existing(sa.inspect(connection), table)
    for table in tables():
        if table.name not in names:
            table.create(connection)
    install_barriers(connection)


def downgrade():
    raise RuntimeError("account_deletion_revocation_barriers_must_not_be_dropped")
