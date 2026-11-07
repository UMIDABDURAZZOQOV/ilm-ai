"""Pure staging configuration checks; never connect or echo secret values."""

import os
from pathlib import PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

PRODUCTION_HOST = "ilm-ai-backend-256x.onrender.com"


def staging_auth_setup_pending(env):
    """Explicit staging-only infrastructure mode, never authentication bypass."""
    return (
        env.get("DEPLOYMENT_STAGE") == "staging"
        and env.get("STAGING_AUTH_SETUP_PENDING") == "true"
    )


def https_origin(value):
    try:
        uri = urlsplit(value)
        return bool(
            uri.scheme == "https"
            and uri.hostname
            and uri.hostname != PRODUCTION_HOST
            and not uri.hostname.endswith(".invalid")
            and uri.hostname not in {"localhost", "127.0.0.1", "::1"}
            and not uri.username
            and not uri.password
            and uri.path in {"", "/"}
            and not uri.query
            and not uri.fragment
            and uri.port in {None, 443}
        )
    except ValueError:
        return False


def staging_errors(env):
    """Fixed check names only. Declared DB identities require operator review."""
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in env.items()):
        return ["configuration_values_must_be_strings"]
    errors = []

    def require(condition, name):
        if not condition:
            errors.append(name)

    require(env.get("DEPLOYMENT_STAGE") == "staging", "staging_stage_required")
    require(
        env.get("ENVIRONMENT") == "production", "production_runtime_guards_required"
    )
    require(
        env.get("PYTHON_DOTENV_DISABLED") == "1", "implicit_dotenv_must_be_disabled"
    )
    origin = env.get("STAGING_PUBLIC_ORIGIN", "").rstrip("/")
    require(https_origin(origin), "isolated_https_origin_required")
    require(
        env.get("MOBILE_OAUTH_REDIRECT_URI") == origin + "/auth/google-callback-mobile",
        "exact_mobile_callback_required",
    )
    require(
        env.get("MOBILE_RELEASE_APP_SCHEME") == "ilmai-staging",
        "isolated_app_scheme_required",
    )
    require(env.get("ALLOWED_ORIGINS") == origin, "exact_staging_cors_required")
    require(
        bool(env.get("STAGING_ISOLATION_REVIEW_REFERENCE", "").strip()),
        "operator_isolation_review_required",
    )
    try:
        db = urlsplit(env.get("DATABASE_URL", ""))
        name, role = (
            env.get("STAGING_DATABASE_NAME", ""),
            env.get("STAGING_DATABASE_USER", ""),
        )
        require(
            db.scheme in {"postgres", "postgresql", "postgresql+psycopg2"}
            and bool(db.hostname)
            and bool(db.password)
            and db.hostname == env.get("STAGING_DATABASE_HOST")
            and name.endswith("_staging")
            and role.endswith("_staging")
            and db.path == "/" + name
            and db.username == role
            and not db.fragment,
            "dedicated_postgres_identity_required",
        )
    except ValueError:
        errors.append("dedicated_postgres_identity_required")
    secrets = [env.get(k, "") for k in ("SECRET_KEY", "JWT_SECRET")]
    require(
        all(len(s) >= 32 and "CHANGE" not in s.upper() for s in secrets)
        and len(set(secrets)) == 2,
        "distinct_staging_signing_secrets_required",
    )
    require(
        env.get("STAGING_AUTH_SETUP_PENDING", "false") in {"true", "false"},
        "explicit_staging_auth_setup_mode_required",
    )
    if staging_auth_setup_pending(env):
        require(
            not env.get("GOOGLE_CLIENT_ID") and not env.get("GOOGLE_CLIENT_SECRET"),
            "pending_auth_credentials_must_be_empty",
        )
        require(
            env.get("ACCOUNT_DELETION_ENABLED", "false") == "false",
            "pending_auth_deletion_must_be_disabled",
        )
    else:
        require(
            bool(env.get("GOOGLE_CLIENT_ID", "").endswith(".apps.googleusercontent.com"))
            and bool(env.get("GOOGLE_CLIENT_SECRET")),
            "dedicated_google_client_required",
        )
    require(env.get("AUTH_STORAGE") == "database", "persistent_auth_storage_required")
    require(
        env.get("MOBILE_REVIEWED_RELEASE") == "true",
        "reviewed_mobile_contract_required",
    )
    require(
        bool(env.get("MOBILE_PUBLICATION_REVIEW_REFERENCE", "").strip()),
        "publication_review_reference_required",
    )
    flags = (
        "ILM_BETA_ENABLED",
        "BETA_TEST_AUTH_ENABLED",
        "PHYSICS_PREVIEW_ENABLED",
        "CHEMISTRY_PREVIEW_ENABLED",
        "WORLD_HISTORY_PREVIEW_ENABLED",
        "UZBEKISTAN_HISTORY_PREVIEW_ENABLED",
    )
    require(
        all(env.get(k, "").lower() in {"", "false", "0"} for k in flags),
        "test_and_preview_auth_must_be_disabled",
    )
    require(
        not any(
            env.get(k)
            for k in (
                "GEMINI_API_KEYS",
                "GEMINI_API_KEY",
                "GOOGLE_API_KEY",
                "NVIDIA_API_KEY",
                "NVIDIA_API_KEYS",
                "OPENAI_API_KEY",
                "OPENAI_API_KEYS",
                "ELEVENLABS_API_KEY",
                "TELEGRAM_BOT_TOKEN",
                "SENTRY_DSN",
            )
        ),
        "unreviewed_external_integrations_must_be_disabled",
    )
    require(env.get("PAYMENT_TEST_MODE") == "true", "payment_test_mode_required")
    if env.get("ACCOUNT_DELETION_ENABLED") == "true":
        deletion_secret = env.get("ACCOUNT_DELETION_SECRET", "")
        require(
            len(deletion_secret) >= 32 and deletion_secret not in secrets,
            "dedicated_account_deletion_secret_required",
        )
        require(
            bool(env.get("ACCOUNT_DELETION_POLICY_REFERENCE", "").strip()),
            "account_deletion_policy_review_required",
        )
        storage = env.get("ACCOUNT_DELETION_STORAGE_ROOT", "")
        require(
            PurePosixPath(storage).is_absolute()
            or PureWindowsPath(storage).is_absolute(),
            "absolute_account_deletion_storage_required",
        )
        require(
            bool(
                (env.get("BREVO_API_KEY") and env.get("BREVO_FROM_EMAIL"))
                or (env.get("RESEND_API_KEY") and env.get("RESEND_FROM"))
                or (env.get("GMAIL_ADDRESS") and env.get("GMAIL_APP_PASSWORD"))
            ),
            "dedicated_account_deletion_test_sender_required",
        )
    return errors


def require_staging_config(env=None):
    env = os.environ if env is None else env
    if env.get("STAGING_AUTH_SETUP_PENDING") == "true" and env.get("DEPLOYMENT_STAGE") != "staging":
        raise RuntimeError("pending_auth_mode_is_staging_only")
    if env.get("DEPLOYMENT_STAGE") == "staging":
        errors = staging_errors(env)
        if errors:
            raise RuntimeError("staging_configuration_rejected:" + ",".join(errors))


def mobile_app_scheme():
    scheme = os.getenv("MOBILE_RELEASE_APP_SCHEME", "ilmai")
    allowed = (
        {"ilmai-staging"} if os.getenv("DEPLOYMENT_STAGE") == "staging" else {"ilmai"}
    )
    if scheme not in allowed:
        raise RuntimeError("mobile_app_scheme_not_allowed")
    return scheme
