"""add email_verified flag and email_verification_codes table

Revision ID: 0007_add_email_verification
Revises: 0006_add_plans_and_checkout
Create Date: 2026-07-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0007_add_email_verification'
down_revision = '0006_add_plans_and_checkout'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    # Google/OAuth accounts don't need email verification — their address is
    # already verified by Google. Mark existing OAuth users as verified so
    # this migration doesn't lock anyone out.
    op.execute("UPDATE users SET email_verified = TRUE WHERE oauth_provider IS NOT NULL")

    op.create_table(
        'email_verification_codes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=200), nullable=False, index=True),
        sa.Column('code', sa.String(length=8), nullable=False),
        sa.Column('purpose', sa.String(length=32), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('email_verification_codes')
    op.drop_column('users', 'email_verified')
