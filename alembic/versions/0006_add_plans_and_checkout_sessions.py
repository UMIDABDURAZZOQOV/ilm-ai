"""add learning_plans and checkout_sessions tables for persistence

Revision ID: 0006_add_plans_and_checkout
Revises: 0005_add_profile_picture
Create Date: 2026-07-08
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0006_add_plans_and_checkout'
down_revision = '0005_add_profile_picture'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'learning_plans',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('plan', sa.JSON(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'checkout_sessions',
        sa.Column('session_id', sa.String(length=64), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('data', sa.JSON(), nullable=False),
    )


def downgrade():
    op.drop_table('checkout_sessions')
    op.drop_table('learning_plans')
