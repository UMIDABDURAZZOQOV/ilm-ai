"""add skill sub-domain column to sat_ielts_questions

Revision ID: 0011_add_question_skill
Revises: 0010_add_review_items
Create Date: 2026-07-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0011_add_question_skill'
down_revision = '0010_add_review_items'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sat_ielts_questions', sa.Column('skill', sa.String(length=120), nullable=True))
    op.create_index('ix_sat_ielts_questions_skill', 'sat_ielts_questions', ['skill'])


def downgrade():
    op.drop_index('ix_sat_ielts_questions_skill', table_name='sat_ielts_questions')
    op.drop_column('sat_ielts_questions', 'skill')
