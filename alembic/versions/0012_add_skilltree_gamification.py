"""add skill-tree gamification columns to users

Revision ID: 0012_add_skilltree_gamification
Revises: 0011_add_question_skill
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0012_add_skilltree_gamification'
down_revision = '0011_add_question_skill'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('xp_total', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('users', 'xp_total')
