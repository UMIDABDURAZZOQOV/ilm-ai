"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-01
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(200), nullable=False, unique=True),
        sa.Column('password', sa.String(256), nullable=False),
        sa.Column('telegram_chat_id', sa.String(64), nullable=True),
        sa.Column('reminder_time', sa.String(8), nullable=True, server_default='09:00'),
        sa.Column('streak_days', sa.Integer, nullable=True, server_default='0'),
        sa.Column('last_study_date', sa.String(20), nullable=True),
        sa.Column('subscription_tier', sa.String(32), nullable=True, server_default='free'),
        sa.Column('uploads_count', sa.Integer, nullable=True, server_default='0'),
        sa.Column('quiz_count_today', sa.Integer, nullable=True, server_default='0'),
        sa.Column('quiz_count_date', sa.String(20), nullable=True),
        sa.Column('chat_count_today', sa.Integer, nullable=True, server_default='0'),
        sa.Column('chat_count_date', sa.String(20), nullable=True),
    )

    op.create_table(
        'vectors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False, index=True),
        sa.Column('filename', sa.String(300)),
        sa.Column('chunk_id', sa.String(300)),
        sa.Column('text', sa.Text),
        sa.Column('embedding', sa.JSON),
    )

    op.create_table(
        'quiz_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False, index=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('score', sa.Integer),
        sa.Column('total', sa.Integer),
        sa.Column('difficulty', sa.String(32)),
        sa.Column('results', sa.JSON),
    )

    op.create_table(
        'refresh_tokens',
        sa.Column('token', sa.String(128), primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False, index=True),
        sa.Column('exp', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('refresh_tokens')
    op.drop_table('quiz_sessions')
    op.drop_table('vectors')
    op.drop_table('users')
