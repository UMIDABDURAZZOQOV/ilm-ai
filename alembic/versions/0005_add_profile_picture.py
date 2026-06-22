"""add profile picture field

Revision ID: 0005_add_profile_picture
Revises: 0004_add_oauth_fields
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005_add_profile_picture'
down_revision = '0004_add_oauth_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Add profile picture column for OAuth users
    op.add_column('users', sa.Column('profile_picture', sa.String(length=500), nullable=True))


def downgrade():
    op.drop_column('users', 'profile_picture')
