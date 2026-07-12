"""add review_items table for spaced-repetition review of weak topics

Revision ID: 0010_add_review_items
Revises: 0009_add_push_token
Create Date: 2026-07-09
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0010_add_review_items'
down_revision = '0009_add_push_token'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'review_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('topic', sa.String(length=200), nullable=False),
        sa.Column('source_material', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('next_review_date', sa.String(length=20), nullable=False),
        sa.Column('interval_stage', sa.Integer(), server_default='0'),
        sa.Column('last_result', sa.String(length=16), nullable=True),
        sa.Column('last_reviewed_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table('review_items')
