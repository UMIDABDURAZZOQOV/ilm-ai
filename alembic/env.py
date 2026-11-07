from logging.config import fileConfig
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from alembic import context
from services.db import engine, Base
from services.assessment_models import AssessmentBase
from services.chemistry_models import ChemistryBase
from services.world_history_models import WorldHistoryBase
from services.uzbekistan_history_models import HistoryBase
from services.account_models import AccountBase

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Provide the metadata for 'autogenerate'
target_metadata = [Base.metadata, AssessmentBase.metadata, ChemistryBase.metadata,
                   WorldHistoryBase.metadata, HistoryBase.metadata, AccountBase.metadata]


def run_migrations_offline():
    url = os.environ.get("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    supplied = config.attributes.get("connection")
    if supplied is not None:
        # Enables an actual Alembic-command rehearsal in an owned fresh schema
        # without changing global DB credentials or starting the application.
        context.configure(connection=supplied, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
        return
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.environ.get("DATABASE_URL", configuration.get("sqlalchemy.url"))
    connectable = engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
