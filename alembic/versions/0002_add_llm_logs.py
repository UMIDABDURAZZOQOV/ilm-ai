"""add llm logs

Revision ID: 0002_add_llm_logs
Revises: 0001_initial
Create Date: 2026-06-11
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_llm_logs'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'llm_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=True, index=True),
        sa.Column('prompt', sa.Text),
        sa.Column('response', sa.Text),
        sa.Column('latency_ms', sa.Integer),
        sa.Column('token_count', sa.Integer, nullable=True),
        sa.Column('model', sa.String(64)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('eval_comment', sa.Text, nullable=True),
    )


def downgrade():
    op.drop_table('llm_logs')
