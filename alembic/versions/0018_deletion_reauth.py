"""Add purpose-bound deletion reauthentication; never delete users or send mail."""

from alembic import op
import sqlalchemy as sa

revision = "0018_deletion_reauth"
down_revision = "0017_runtime_foundation"
branch_labels = depends_on = None


def upgrade():
    op.create_table(
        "account_deletion_manual_requests",
        sa.Column("id", sa.String(43), primary_key=True),
        sa.Column("account_hash", sa.String(64), nullable=False),
        sa.Column("contact_hash", sa.String(64), nullable=False),
        sa.Column("encrypted_details", sa.Text, nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "account_deletion_reauth",
        sa.Column("state_hash", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("method", sa.String(16), nullable=False),
        sa.Column("surface", sa.String(16), nullable=False),
        sa.Column("phase", sa.String(16), nullable=False),
        sa.Column("nonce_hash", sa.String(64)),
        sa.Column("challenge", sa.String(43)),
        sa.Column("identity_hash", sa.String(64)),
        sa.Column("grant_hash", sa.String(64), unique=True),
        sa.Column(
            "challenge_id",
            sa.String(64),
            sa.ForeignKey("account_deletion_challenges.id"),
            unique=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("exchange_expires_at", sa.DateTime(timezone=True)),
    )


def downgrade():
    raise RuntimeError("deletion_proofs_require_reviewed_retention_not_automatic_drop")
