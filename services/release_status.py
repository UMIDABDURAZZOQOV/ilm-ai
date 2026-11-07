"""Public deployment identity, never database URLs or secrets."""

import os
import re


def public_status():
    revision = os.getenv("RENDER_GIT_COMMIT", os.getenv("APP_BUILD_REVISION", ""))
    if not re.fullmatch(r"[0-9a-f]{7,40}", revision):
        revision = "unknown"
    status = {
        "status": "ok",
        "revision": revision,
        "mobile_contract_version": 2
        if os.getenv("MOBILE_REVIEWED_RELEASE") == "true"
        else 1,
    }
    from services.deployment_config import staging_auth_setup_pending
    if staging_auth_setup_pending(os.environ):
        status.update(oauth_setup_pending=True, authentication_ready=False)
    return status
