"""Add existing Chemistry/history engine tables; never replace content/progress.

Revision ID: 0015_reviewed_subject_schemas
Revises: 0014_mobile_oauth_state
Definitions are pinned here rather than importing mutable runtime ORM metadata.
"""

from alembic import op
import sqlalchemy as sa

revision = "0015_reviewed_subject_schemas"
down_revision = "0014_mobile_oauth_state"
branch_labels = None
depends_on = None


def definitions():
    metadata = sa.MetaData()
    sa.Table("users", metadata, sa.Column("id", sa.Integer, primary_key=True))
    sa.Table(
        "study_sessions", metadata, sa.Column("id", sa.String(96), primary_key=True)
    )
    tables = []
    for subject in ("chemistry", "world_history", "uzbekistan_history"):
        prefix = subject + "_preview"
        lesson = sa.Table(
            prefix + "_lessons",
            metadata,
            sa.Column("key", sa.String(96), primary_key=True),
            sa.Column("subject", sa.String(40), nullable=False),
            sa.Column("grade", sa.Integer, nullable=False),
            sa.Column("sequence", sa.Integer, nullable=False),
            sa.Column("revision", sa.Integer, nullable=False),
            sa.Column("topic_id", sa.String(80), nullable=False, unique=True),
            sa.Column("content_sha256", sa.String(64), nullable=False),
            sa.Column("title", sa.Text, nullable=False),
            sa.Column("content", sa.JSON, nullable=False),
            sa.UniqueConstraint(
                "subject", "grade", "sequence", name="uq_" + prefix + "_sequence"
            ),
        )
        assessment = sa.Table(
            prefix + "_assessments",
            metadata,
            sa.Column("key", sa.String(140), primary_key=True),
            sa.Column(
                "lesson_key",
                sa.String(96),
                sa.ForeignKey(lesson.c.key),
                nullable=False,
                index=True,
            ),
            sa.Column("order_index", sa.Integer, nullable=False),
            sa.Column("response_kind", sa.String(32), nullable=False),
            sa.Column("public_prompt", sa.JSON, nullable=False),
            sa.Column("grading_spec", sa.JSON, nullable=False),
            sa.Column("source_refs", sa.JSON, nullable=False),
            sa.UniqueConstraint(
                "lesson_key", "order_index", name="uq_" + prefix + "_question_order"
            ),
        )
        progress = sa.Table(
            prefix + "_progress",
            metadata,
            sa.Column(
                "user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True
            ),
            sa.Column(
                "lesson_key",
                sa.String(96),
                sa.ForeignKey(lesson.c.key),
                primary_key=True,
            ),
            sa.Column("completed_at", sa.DateTime(timezone=True)),
            sa.Column("best_score_pct", sa.Float, nullable=False),
            sa.Column("attempts", sa.Integer, nullable=False),
            sa.Column("xp_earned", sa.Integer, nullable=False),
        )
        answer = sa.Table(
            prefix + "_answers",
            metadata,
            sa.Column(
                "session_id",
                sa.String(96),
                sa.ForeignKey("study_sessions.id"),
                primary_key=True,
            ),
            sa.Column(
                "assessment_key",
                sa.String(140),
                sa.ForeignKey(assessment.c.key),
                primary_key=True,
            ),
            sa.Column("fingerprint", sa.String(64), nullable=False),
            sa.Column("response", sa.JSON, nullable=False),
        )
        tables.extend([lesson, assessment, progress, answer])
    return tables


def validate_existing(inspector, table):
    columns = {c["name"]: c for c in inspector.get_columns(table.name)}
    for column in table.columns:
        existing = columns.get(column.name)
        if (
            existing is None
            or existing["type"]._type_affinity != column.type._type_affinity
            or existing["nullable"] != column.nullable
            or (
                getattr(column.type, "length", None) is not None
                and getattr(existing["type"], "length", None) != column.type.length
            )
        ):
            raise RuntimeError("reviewed_subject_existing_columns_require_review")
    if inspector.get_pk_constraint(table.name)["constrained_columns"] != [
        c.name for c in table.primary_key
    ]:
        raise RuntimeError("reviewed_subject_existing_primary_key_requires_review")
    foreign = {
        (
            tuple(f["constrained_columns"]),
            f["referred_table"],
            tuple(f["referred_columns"]),
        )
        for f in inspector.get_foreign_keys(table.name)
    }
    for key in table.foreign_key_constraints:
        targets = list(key.elements)
        wanted = (
            tuple(c.parent.name for c in targets),
            targets[0].column.table.name,
            tuple(c.column.name for c in targets),
        )
        if wanted not in foreign:
            raise RuntimeError("reviewed_subject_existing_ownership_requires_review")
    unique = {
        tuple(c["column_names"]) for c in inspector.get_unique_constraints(table.name)
    }
    unique |= {
        tuple(i["column_names"])
        for i in inspector.get_indexes(table.name)
        if i.get("unique")
    }
    if any(
        tuple(c.name for c in constraint.columns) not in unique
        for constraint in table.constraints
        if isinstance(constraint, sa.UniqueConstraint)
    ):
        raise RuntimeError("reviewed_subject_existing_uniqueness_requires_review")


def upgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    names = set(inspector.get_table_names())
    if not {"users", "study_sessions"} <= names:
        raise RuntimeError("reviewed_subject_migration_requires_shared_schema")
    tables = definitions()
    # Validate every existing table before any DDL. Never drop/recreate an
    # incompatible table or silently discard immutable source/progress rows.
    for table in tables:
        if table.name in names:
            validate_existing(inspector, table)
    for table in tables:
        if table.name not in names:
            table.create(connection)


def downgrade():
    raise RuntimeError("rollback_application_only_keep_reviewed_content_and_progress")
