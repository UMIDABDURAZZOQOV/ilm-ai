"""Add missing runtime tables/columns after removing production create_all.

No seeding, user mutation, table rebuild, destructive downgrade or model import.
Pinned DDL is separate from evolving runtime metadata. Schema conflicts abort.
"""

import importlib.util
import hashlib
from pathlib import Path
import runpy
from alembic import op
import sqlalchemy as sa

revision = "0017_runtime_foundation"
down_revision = "0016_account_deletion"
branch_labels = depends_on = None


def definitions():
    return runpy.run_path(
        str(Path(__file__).parents[1] / "runtime_schema_20261107.py")
    )["definitions"]()


def upgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    metadata = definitions()
    additions = []
    missing_unique = []
    # Validate every existing type/key and every additive column BEFORE any DDL.
    for table in metadata.sorted_tables:
        if not inspector.has_table(table.name):
            continue
        columns = {c["name"]: c for c in inspector.get_columns(table.name)}
        if inspector.get_pk_constraint(table.name)["constrained_columns"] != [
            c.name for c in table.primary_key
        ]:
            raise RuntimeError("runtime_primary_key_requires_review")
        for column in table.columns:
            if column.name in columns:
                if (
                    columns[column.name]["type"]._type_affinity
                    != column.type._type_affinity
                ):
                    raise RuntimeError("runtime_column_type_requires_review")
                if not column.nullable and columns[column.name]["nullable"]:
                    raise RuntimeError("runtime_nullability_requires_review")
            else:
                if not column.nullable or column.primary_key or column.foreign_keys:
                    raise RuntimeError("runtime_required_column_requires_review")
                additions.append((table.name, column))
        existing_indexes = {
            index["name"]: index for index in inspector.get_indexes(table.name)
        }
        for index in table.indexes:
            existing = existing_indexes.get(index.name)
            if existing is not None and (
                existing["column_names"] != [c.name for c in index.columns]
                or bool(existing.get("unique")) != bool(index.unique)
            ):
                raise RuntimeError("runtime_index_requires_review")
        unique = {
            tuple(item["column_names"])
            for item in inspector.get_unique_constraints(table.name)
        }
        unique |= {
            tuple(item["column_names"])
            for item in existing_indexes.values()
            if item.get("unique")
        }
        for constraint in table.constraints:
            if not isinstance(constraint, sa.UniqueConstraint):
                continue
            keys = tuple(column.name for column in constraint.columns)
            if keys in unique:
                continue
            if set(keys) <= set(columns):
                selected = [table.c[key] for key in keys]
                duplicates = (
                    sa.select(*selected)
                    .where(*(column.is_not(None) for column in selected))
                    .group_by(*selected)
                    .having(sa.func.count() > 1)
                    .limit(1)
                )
                if connection.execute(duplicates).first() is not None:
                    raise RuntimeError("runtime_uniqueness_data_requires_review")
            missing_unique.append((table.name, keys))
    for name, column in additions:
        op.add_column(name, sa.Column(column.name, column.type, nullable=True))
    for table in metadata.sorted_tables:
        if not inspector.has_table(table.name):
            table.create(connection)
    for table in metadata.sorted_tables:
        for index in table.indexes:
            index.create(connection, checkfirst=True)
    for table, keys in missing_unique:
        identity = table + "_" + "_".join(keys)
        name = (
            "uq_runtime_"
            + identity[:40]
            + "_"
            + hashlib.sha256(identity.encode()).hexdigest()[:6]
        )
        op.create_index(name, table, list(keys), unique=True)
    # Apply ownership barriers also to tables created by this additive migration.
    spec = importlib.util.spec_from_file_location(
        "pinned_deletion_barriers", Path(__file__).with_name("0016_account_deletion.py")
    )
    barriers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(barriers)
    barriers.install_barriers(connection)


def downgrade():
    raise RuntimeError("rollback_application_only_keep_runtime_data_and_revocation")
