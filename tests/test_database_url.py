import pytest
from sqlalchemy import create_engine
from services.database_url import normalize_database_url


@pytest.mark.parametrize("prefix", ["postgres://", "postgresql://", "postgresql+psycopg2://"])
def test_postgres_uses_installed_driver_without_connecting_or_rewriting_credentials(prefix):
    url = normalize_database_url(prefix + "test:test@127.0.0.1/staging")
    assert url == "postgresql+psycopg2://test:test@127.0.0.1/staging"
    engine = create_engine(url)
    assert engine.dialect.driver == "psycopg2"
    engine.dispose()


def test_sqlite_configuration_is_unchanged():
    assert normalize_database_url("sqlite:////tmp/test.db") == "sqlite:////tmp/test.db"
