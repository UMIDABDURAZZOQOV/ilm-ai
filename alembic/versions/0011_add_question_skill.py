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
    # Historical installs had this table from create_all; a fresh migration-only
    # install must create the same pinned schema before adding its skill column.
    # Already-applied revisions are not rerun and existing rows are untouched.
    if not sa.inspect(op.get_bind()).has_table('sat_ielts_questions'):
        import runpy
        from pathlib import Path
        metadata = runpy.run_path(str(Path(__file__).parents[1] / 'runtime_schema_20261107.py'))['definitions']()
        metadata.tables['sat_ielts_questions'].create(op.get_bind())
        return
    op.add_column('sat_ielts_questions', sa.Column('skill', sa.String(length=120), nullable=True))
    op.create_index('ix_sat_ielts_questions_skill', 'sat_ielts_questions', ['skill'])


def downgrade():
    op.drop_index('ix_sat_ielts_questions_skill', table_name='sat_ielts_questions')
    op.drop_column('sat_ielts_questions', 'skill')
