"""sync models

Revision ID: 0003_sync_models
Revises: 0002_add_llm_logs
Create Date: 2026-06-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_sync_models'
down_revision = '0002_add_llm_logs'
branch_labels = None
depends_on = None


def upgrade():
    # Update users table
    op.add_column('users', sa.Column('learning_goal', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('target_date', sa.String(length=20), nullable=True))

    # Update vectors table
    op.add_column('vectors', sa.Column('topic', sa.String(length=200), nullable=True, server_default='General'))

    # Update llm_logs table
    op.add_column('llm_logs', sa.Column('accuracy', sa.Integer(), nullable=True))
    op.add_column('llm_logs', sa.Column('groundedness', sa.Integer(), nullable=True))
    op.add_column('llm_logs', sa.Column('helpfulness', sa.Integer(), nullable=True))
    op.add_column('llm_logs', sa.Column('tone', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('llm_logs', 'tone')
    op.drop_column('llm_logs', 'helpfulness')
    op.drop_column('llm_logs', 'groundedness')
    op.drop_column('llm_logs', 'accuracy')
    op.drop_column('vectors', 'topic')
    op.drop_column('users', 'target_date')
    op.drop_column('users', 'learning_goal')
