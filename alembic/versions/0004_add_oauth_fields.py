"""add oauth fields

Revision ID: 0004_add_oauth_fields
Revises: 0003_sync_models
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0004_add_oauth_fields'
down_revision = '0003_sync_models'
branch_labels = None
depends_on = None


def upgrade():
    # Make password column nullable for OAuth users
    op.alter_column('users', 'password', nullable=True)
    
    # Add OAuth provider fields
    op.add_column('users', sa.Column('oauth_provider', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(length=200), nullable=True))


def downgrade():
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'oauth_provider')
    op.alter_column('users', 'password', nullable=False)