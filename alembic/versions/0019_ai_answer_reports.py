"""Store learner-submitted reports of generated answers for operator review."""

from alembic import op
import sqlalchemy as sa


revision = "0019_ai_answer_reports"
down_revision = "0018_deletion_reauth"
branch_labels = depends_on = None


def upgrade():
    op.create_table(
        "ai_answer_reports",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("subject", sa.String(40), nullable=False),
        sa.Column("surface", sa.String(24), nullable=False),
        sa.Column("model", sa.String(120), nullable=False),
        sa.Column("paragraphs", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ai_answer_reports_user_id", "ai_answer_reports", ["user_id"])
    if op.get_context().dialect.name == "postgresql":
        op.execute("""
            CREATE TRIGGER account_guard_ai_answer_reports_user_id
            BEFORE INSERT OR UPDATE ON ai_answer_reports
            FOR EACH ROW EXECUTE FUNCTION account_owner_write_guard('user_id', 'direct')
        """)
    else:
        for action in ('insert', 'update'):
            op.execute(f"""
                CREATE TRIGGER account_guard_ai_answer_reports_user_id_{action}
                BEFORE {action.upper()} ON ai_answer_reports
                WHEN NOT EXISTS (
                    SELECT 1 FROM users WHERE id = NEW.user_id
                    AND COALESCE(oauth_provider, '') <> '__account_deleted__'
                )
                BEGIN SELECT RAISE(ABORT, 'account_deleted'); END
            """)


def downgrade():
    raise RuntimeError("ai_answer_reports_require_reviewed_retention_not_automatic_drop")
