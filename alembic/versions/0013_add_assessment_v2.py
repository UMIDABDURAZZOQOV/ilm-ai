"""Add opt-in assessment v2; preserve shared study/account/legacy content.

Revision ID: 0013_add_assessment_v2
Revises: 0012_add_skilltree_gamification
"""

import sqlalchemy as sa

from alembic import op

revision = "0013_add_assessment_v2"
down_revision = "0012_add_skilltree_gamification"
branch_labels = None
depends_on = None


def upgrade():
    # Older installs created these additive shared tables through Base.create_all.
    # A migration-only install needs the same definitions, without startup seeds.
    names = set(sa.inspect(op.get_bind()).get_table_names())
    if "study_sessions" not in names:
        op.create_table(
            "study_sessions",
            sa.Column("id", sa.String(96), primary_key=True),
            sa.Column(
                "user_id",
                sa.Integer,
                sa.ForeignKey("users.id"),
                nullable=False,
                index=True,
            ),
            sa.Column("kind", sa.String(24), nullable=False, index=True),
            sa.Column("scope", sa.String(100), nullable=False),
            sa.Column("questions", sa.JSON, nullable=False),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("completed_at", sa.DateTime(timezone=True)),
            sa.Column("response", sa.JSON),
            sa.Column("fingerprint", sa.String(64)),
        )
    if "study_events" not in names:
        op.create_table(
            "study_events",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("source_key", sa.String(140), nullable=False, unique=True),
            sa.Column(
                "user_id",
                sa.Integer,
                sa.ForeignKey("users.id"),
                nullable=False,
                index=True,
            ),
            sa.Column("kind", sa.String(24), nullable=False),
            sa.Column("xp", sa.Integer, nullable=False, default=0),
            sa.Column(
                "created_at", sa.DateTime(timezone=True), nullable=False, index=True
            ),
        )
    op.create_table(
        "curriculum_v2_lessons",
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
            "subject", "grade", "sequence", name="uq_v2_lesson_sequence"
        ),
    )
    op.create_table(
        "curriculum_assessments_v2",
        sa.Column("key", sa.String(140), primary_key=True),
        sa.Column(
            "lesson_key",
            sa.String(96),
            sa.ForeignKey("curriculum_v2_lessons.key"),
            nullable=False,
        ),
        sa.Column("order_index", sa.Integer, nullable=False),
        sa.Column("response_kind", sa.String(32), nullable=False),
        sa.Column("public_prompt", sa.JSON, nullable=False),
        sa.Column("grading_spec", sa.JSON, nullable=False),
        sa.Column("source_refs", sa.JSON, nullable=False),
        sa.UniqueConstraint("lesson_key", "order_index", name="uq_v2_assessment_order"),
    )
    op.create_index(
        "ix_curriculum_assessments_v2_lesson_key",
        "curriculum_assessments_v2",
        ["lesson_key"],
    )
    op.create_table(
        "curriculum_progress_v2",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column(
            "lesson_key",
            sa.String(96),
            sa.ForeignKey("curriculum_v2_lessons.key"),
            primary_key=True,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("best_score_pct", sa.Float, nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False),
        sa.Column("xp_earned", sa.Integer, nullable=False),
    )
    op.create_table(
        "curriculum_answers_v2",
        sa.Column(
            "session_id",
            sa.String(96),
            sa.ForeignKey("study_sessions.id"),
            primary_key=True,
        ),
        sa.Column(
            "assessment_key",
            sa.String(140),
            sa.ForeignKey("curriculum_assessments_v2.key"),
            primary_key=True,
        ),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("response", sa.JSON, nullable=False),
    )


def downgrade():
    # Intentional: shared study tables may hold Biology history; never drop them.
    for table in (
        "curriculum_answers_v2",
        "curriculum_progress_v2",
        "curriculum_assessments_v2",
        "curriculum_v2_lessons",
    ):
        op.drop_table(table)
