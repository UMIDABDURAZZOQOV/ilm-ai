"""Add explicit mobile PKCE state/grant migration without changing user data.

Revision ID: 0014_mobile_oauth_state
Revises: 0013_add_assessment_v2
"""

from alembic import op
import sqlalchemy as sa

revision = "0014_mobile_oauth_state"
down_revision = "0013_add_assessment_v2"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    names = set(inspector.get_table_names())
    definitions = {
        "oauth_states": {
            "state_hash": (sa.String, False),
            "challenge": (sa.String, True),
            "redirect_uri": (sa.String, False),
            "expires_at": (sa.DateTime, False),
            "consumed": (sa.Boolean, False),
        },
        "mobile_login_grants": {
            "code_hash": (sa.String, False),
            "challenge": (sa.String, False),
            "user_id": (sa.Integer, False),
            "expires_at": (sa.DateTime, False),
            "consumed": (sa.Boolean, False),
        },
    }
    if "users" not in names:
        raise RuntimeError("mobile_oauth_migration_requires_existing_users")
    # Some installations used create_all. Validate both tables before any DDL;
    # never drop/recreate a live grant/state table to hide incompatible schemas.
    for name, required in definitions.items():
        if name not in names:
            continue
        columns = {c["name"]: c for c in inspector.get_columns(name)}
        if any(
            key not in columns
            or not isinstance(columns[key]["type"], kind)
            or columns[key]["nullable"] != nullable
            for key, (kind, nullable) in required.items()
        ):
            raise RuntimeError("mobile_oauth_existing_schema_requires_review")
        primary = "state_hash" if name == "oauth_states" else "code_hash"
        if inspector.get_pk_constraint(name)["constrained_columns"] != [primary]:
            raise RuntimeError("mobile_oauth_existing_primary_key_requires_review")
        if name == "mobile_login_grants" and not any(
            f["constrained_columns"] == ["user_id"]
            and f["referred_table"] == "users"
            and f["referred_columns"] == ["id"]
            for f in inspector.get_foreign_keys(name)
        ):
            raise RuntimeError("mobile_oauth_existing_ownership_requires_review")
    if "oauth_states" not in names:
        op.create_table(
            "oauth_states",
            sa.Column("state_hash", sa.String(64), primary_key=True),
            sa.Column("challenge", sa.String(128), nullable=True),
            sa.Column("redirect_uri", sa.String(1000), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column(
                "consumed", sa.Boolean, nullable=False, server_default=sa.false()
            ),
        )
    if "mobile_login_grants" not in names:
        op.create_table(
            "mobile_login_grants",
            sa.Column("code_hash", sa.String(64), primary_key=True),
            sa.Column("challenge", sa.String(128), nullable=False),
            sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column(
                "consumed", sa.Boolean, nullable=False, server_default=sa.false()
            ),
        )


def downgrade():
    raise RuntimeError("rollback_application_only_keep_pkce_tables_and_active_sessions")
