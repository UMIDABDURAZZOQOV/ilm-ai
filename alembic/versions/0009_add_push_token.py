"""add push_token column for Expo push notifications

Revision ID: 0009_add_push_token
Revises: 0008_add_assistant_messages
Create Date: 2026-07-09
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0009_add_push_token'
down_revision = '0008_add_assistant_messages'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('push_token', sa.String(length=300), nullable=True))


def downgrade():
    op.drop_column('users', 'push_token')
