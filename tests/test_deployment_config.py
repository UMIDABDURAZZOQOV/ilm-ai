"""Offline staging checks use synthetic credentials; never hosted resources."""

import pytest

from services.deployment_config import (
    mobile_app_scheme,
    require_staging_config,
    staging_errors,
)


@pytest.fixture
def config():
    return {
        "DEPLOYMENT_STAGE": "staging",
        "ENVIRONMENT": "production",
        "PYTHON_DOTENV_DISABLED": "1",
        "STAGING_PUBLIC_ORIGIN": "https://staging.example.test",
        "ALLOWED_ORIGINS": "https://staging.example.test",
        "MOBILE_OAUTH_REDIRECT_URI": "https://staging.example.test/auth/google-callback-mobile",
        "MOBILE_RELEASE_APP_SCHEME": "ilmai-staging",
        "STAGING_ISOLATION_REVIEW_REFERENCE": "synthetic fixture only",
        "STAGING_DATABASE_HOST": "localhost",
        "STAGING_DATABASE_NAME": "ilm_staging",
        "STAGING_DATABASE_USER": "ilm_staging",
        "DATABASE_URL": "postgresql://ilm_staging:test-only@localhost/ilm_staging",
        "SECRET_KEY": "a" * 40,
        "JWT_SECRET": "b" * 40,
        "GOOGLE_CLIENT_ID": "fixture.apps.googleusercontent.com",
        "GOOGLE_CLIENT_SECRET": "synthetic-only",
        "AUTH_STORAGE": "database",
        "MOBILE_REVIEWED_RELEASE": "true",
        "MOBILE_PUBLICATION_REVIEW_REFERENCE": "technical fixture, not expert approval",
        "PAYMENT_TEST_MODE": "true",
    }


def test_valid_configuration_is_offline_only(config):
    assert staging_errors(config) == []
    require_staging_config(config)


def test_explicit_pending_mode_keeps_auth_closed_and_isolated(config):
    config.update(
        STAGING_AUTH_SETUP_PENDING="true", GOOGLE_CLIENT_ID="", GOOGLE_CLIENT_SECRET=""
    )
    assert staging_errors(config) == []
    require_staging_config(config)
    config["BETA_TEST_AUTH_ENABLED"] = "true"
    assert "test_and_preview_auth_must_be_disabled" in staging_errors(config)


@pytest.mark.parametrize(
    "key,value",
    [
        ("GOOGLE_CLIENT_ID", "fixture.apps.googleusercontent.com"),
        ("GOOGLE_CLIENT_SECRET", "synthetic-only"),
        ("ACCOUNT_DELETION_ENABLED", "true"),
        ("STAGING_AUTH_SETUP_PENDING", "yes"),
    ],
)
def test_pending_mode_rejects_credentials_deletion_and_implicit_values(
    config, key, value
):
    config.update(
        STAGING_AUTH_SETUP_PENDING="true", GOOGLE_CLIENT_ID="", GOOGLE_CLIENT_SECRET=""
    )
    config[key] = value
    assert staging_errors(config)


def test_pending_mode_cannot_be_used_in_production(config):
    config.update(STAGING_AUTH_SETUP_PENDING="true", DEPLOYMENT_STAGE="production")
    with pytest.raises(RuntimeError, match="pending_auth_mode_is_staging_only"):
        require_staging_config(config)


def test_pending_health_does_not_claim_auth_readiness(monkeypatch):
    from services.release_status import public_status

    monkeypatch.setenv("DEPLOYMENT_STAGE", "staging")
    monkeypatch.setenv("STAGING_AUTH_SETUP_PENDING", "true")
    assert public_status()["authentication_ready"] is False
    assert public_status()["oauth_setup_pending"] is True
    monkeypatch.delenv("DEPLOYMENT_STAGE")
    assert "authentication_ready" not in public_status()


def test_enabled_deletion_requires_private_policy_storage_and_test_sender(config):
    config["ACCOUNT_DELETION_ENABLED"] = "true"
    assert {
        "dedicated_account_deletion_secret_required",
        "account_deletion_policy_review_required",
        "absolute_account_deletion_storage_required",
        "dedicated_account_deletion_test_sender_required",
    } <= set(staging_errors(config))
    config.update(
        ACCOUNT_DELETION_SECRET="c" * 40,
        ACCOUNT_DELETION_POLICY_REFERENCE="synthetic reviewed policy fixture",
        ACCOUNT_DELETION_STORAGE_ROOT="/isolated-staging",
        BREVO_API_KEY="synthetic-mail-key",
        BREVO_FROM_EMAIL="owned@example.test",
    )
    assert staging_errors(config) == []
    config["ACCOUNT_DELETION_SECRET"] = config["JWT_SECRET"]
    assert staging_errors(config) == ["dedicated_account_deletion_secret_required"]


def test_unassigned_env_value_is_rejected_without_traceback(config):
    config["DATABASE_URL"] = None
    assert staging_errors(config) == ["configuration_values_must_be_strings"]


def test_email_free_deletion_retains_all_other_deployment_guards(config):
    config.update(
        ACCOUNT_DELETION_ENABLED="true",
        EMAIL_FREE_ACCOUNT_DELETION="true",
        ACCOUNT_DELETION_SECRET="synthetic-separate-deletion-secret-32-chars",
        ACCOUNT_DELETION_POLICY_REFERENCE="owned staging acceptance only",
        ACCOUNT_DELETION_STORAGE_ROOT="/srv/owned-staging",
    )
    assert staging_errors(config) == []
    config["ACCOUNT_DELETION_POLICY_REFERENCE"] = ""
    assert "account_deletion_policy_review_required" in staging_errors(config)
    config["BETA_TEST_AUTH_ENABLED"] = "true"
    assert "test_and_preview_auth_must_be_disabled" in staging_errors(config)


@pytest.mark.parametrize(
    "key,value",
    [
        ("ENVIRONMENT", "test"),
        ("PYTHON_DOTENV_DISABLED", ""),
        ("STAGING_PUBLIC_ORIGIN", "https://ilm-ai-backend-256x.onrender.com"),
        ("STAGING_PUBLIC_ORIGIN", "https://x.invalid"),
        ("STAGING_PUBLIC_ORIGIN", "https://user:password@staging.example.test"),
        ("STAGING_PUBLIC_ORIGIN", "http://staging.example.test"),
        ("STAGING_PUBLIC_ORIGIN", "https://staging.example.test/path"),
        ("MOBILE_RELEASE_APP_SCHEME", "ilmai"),
        ("MOBILE_OAUTH_REDIRECT_URI", "https://wrong.test/callback"),
        ("ALLOWED_ORIGINS", "*"),
        ("STAGING_ISOLATION_REVIEW_REFERENCE", ""),
        ("STAGING_DATABASE_NAME", "production"),
        ("STAGING_DATABASE_HOST", "other-host"),
        ("STAGING_DATABASE_USER", "postgres"),
        ("DATABASE_URL", "sqlite:///test.db"),
        ("JWT_SECRET", "a" * 40),
        ("SECRET_KEY", "change-me"),
        ("GOOGLE_CLIENT_SECRET", ""),
        ("GOOGLE_CLIENT_ID", ""),
        ("AUTH_STORAGE", "legacy_json"),
        ("MOBILE_REVIEWED_RELEASE", "false"),
        ("MOBILE_PUBLICATION_REVIEW_REFERENCE", ""),
        ("BETA_TEST_AUTH_ENABLED", "true"),
        ("PHYSICS_PREVIEW_ENABLED", "true"),
        ("NVIDIA_API_KEY", "synthetic-sensitive-value"),
        ("TELEGRAM_BOT_TOKEN", "synthetic-sensitive-value"),
        ("PAYMENT_TEST_MODE", "false"),
    ],
)
def test_unsafe_configuration_fails_without_echoing_values(config, key, value):
    config[key] = value
    assert staging_errors(config)
    with pytest.raises(RuntimeError) as error:
        require_staging_config(config)
    assert config["DATABASE_URL"] not in str(error.value)
    assert config["SECRET_KEY"] not in str(error.value)
    assert "synthetic-sensitive-value" not in str(error.value)


def test_legacy_configuration_and_app_scheme_are_preserved(monkeypatch):
    require_staging_config({"ENVIRONMENT": "production"})
    monkeypatch.delenv("DEPLOYMENT_STAGE", raising=False)
    monkeypatch.delenv("MOBILE_RELEASE_APP_SCHEME", raising=False)
    # Local Beta's existing wrapper owns the final ilmai-beta URI. Its historic
    # configuration must not change the ordinary callback that wrapper validates.
    monkeypatch.setenv("MOBILE_APP_SCHEME", "ilmai-beta")
    assert mobile_app_scheme() == "ilmai"
    monkeypatch.setenv("DEPLOYMENT_STAGE", "staging")
    with pytest.raises(RuntimeError):
        mobile_app_scheme()
    monkeypatch.setenv("MOBILE_RELEASE_APP_SCHEME", "ilmai-staging")
    assert mobile_app_scheme() == "ilmai-staging"
    monkeypatch.setenv("MOBILE_RELEASE_APP_SCHEME", "https://attacker.test")
    with pytest.raises(RuntimeError):
        mobile_app_scheme()
