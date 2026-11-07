"""Guard tests never connect to a hosted or local database."""
import pytest
from scripts.initialize_fresh_render_staging import require_fresh_staging_target

pytest_plugins = ["test_deployment_config"]
DATABASE = "dpg-" + "a" * 20 + "-a"


@pytest.fixture
def fresh(config):
    config.update(STAGING_AUTH_SETUP_PENDING="true", GOOGLE_CLIENT_ID="", GOOGLE_CLIENT_SECRET="",
                  STAGING_DATABASE_HOST=DATABASE,
                  DATABASE_URL=f"postgresql://ilm_staging:test-only@{DATABASE}/ilm_staging?sslmode=require",
                  RENDER_SERVICE_ID="srv-" + "b" * 20)
    return config


def test_exact_isolated_target_is_required(fresh):
    require_fresh_staging_target(fresh, DATABASE)


@pytest.mark.parametrize("key,value", [
    ("RENDER_SERVICE_ID", "srv-d99id4mcjfls738a8l80"),
    ("RENDER_SERVICE_ID", ""),
    ("DEPLOYMENT_STAGE", "production"),
    ("STAGING_AUTH_SETUP_PENDING", "false"),
    ("STAGING_DATABASE_HOST", "production.neon.tech"),
    ("DATABASE_URL", "postgresql://ilm_staging:test-only@localhost/ilm_staging"),
    ("BETA_TEST_AUTH_ENABLED", "true"),
    ("GOOGLE_CLIENT_SECRET", "synthetic-only"),
])
def test_unsafe_target_never_reaches_database(fresh, key, value):
    fresh[key] = value
    with pytest.raises(ValueError):
        require_fresh_staging_target(fresh, DATABASE)


@pytest.mark.parametrize("database_id", ["", "production", DATABASE + ".render.com", "dpg-other-a"])
def test_arbitrary_database_ids_are_rejected(fresh, database_id):
    with pytest.raises(ValueError):
        require_fresh_staging_target(fresh, database_id)
