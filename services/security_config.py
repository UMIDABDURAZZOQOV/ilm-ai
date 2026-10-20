"""Validate configuration without changing keys or persisted user credentials."""

import os


def require_production_secret(name: str, value: str, placeholder: str) -> None:
    if os.environ.get("ENVIRONMENT") == "production" and (
        not value.strip() or value == placeholder
    ):
        raise RuntimeError(
            f"{name} must be configured in production; empty/default signing keys are unsafe."
        )
