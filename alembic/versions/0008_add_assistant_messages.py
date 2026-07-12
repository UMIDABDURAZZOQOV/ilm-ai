"""add assistant_messages table for general-purpose AI assistant

Revision ID: 0008_add_assistant_messages
Revises: 0007_add_email_verification
Create Date: 2026-07-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0008_add_assistant_messages'
down_revision = '0007_add_email_verification'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'assistant_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('role', sa.String(length=16), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.add_column('users', sa.Column('assistant_count_today', sa.Integer(), server_default='0'))
    op.add_column('users', sa.Column('assistant_count_date', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('users', 'assistant_count_date')
    op.drop_column('users', 'assistant_count_today')
    op.drop_table('assistant_messages')
