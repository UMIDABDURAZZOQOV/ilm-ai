"""Read-only public API contract probe. No login, secrets, DB access or deployment.

This is one readiness gate, never a production signoff. Output includes only
fixed check names, statuses and booleans, not response bodies or OAuth values.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

import requests


SUBJECTS = {"biologiya", "fizika", "kimyo", "ozbekiston_tarixi", "jahon_tarixi"}


def origin(value):
    try:
        uri = urlsplit(value)
        if (
            uri.username
            or uri.password
            or uri.path not in {"", "/"}
            or uri.query
            or uri.fragment
            or not uri.hostname
            or uri.port not in {None, 443, 8930}
        ):
            raise ValueError
        if uri.scheme != "https" and value.rstrip("/") != "http://127.0.0.1:8930":
            raise ValueError
    except ValueError:
        raise ValueError(
            "expected_https_origin_without_credentials_path_or_query"
        ) from None
    return value.rstrip("/")


def check(
    base,
    get=requests.get,
    *,
    expected_revision=None,
    require_release_operations=False,
    require_google_account_deletion=False,
    require_ai_reporting=False,
):
    if expected_revision is not None and not re.fullmatch(
        r"[0-9a-f]{40}", expected_revision
    ):
        raise ValueError("expected_revision_must_be_full_lowercase_git_sha")
    base = origin(base)
    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "origin": base,
        "read_only": True,
        "checks": [],
        "production_signoff": False,
    }

    def probe(name, path, validator=None, *, expect_post_route=False):
        item = dict(name=name, path=path, status=None, passed=False)
        try:
            response = get(base + path, timeout=(5, 15), allow_redirects=False)
            item["status"] = response.status_code
            if expect_post_route:
                # Inspect the router without using credentials or generating AI output.
                methods = response.headers.get("Allow", "").upper().split(",")
                item["passed"] = response.status_code == 405 and "POST" in {
                    method.strip() for method in methods
                }
            elif response.status_code == 200:
                item["passed"] = bool(validator(response.json()))
        except (
            requests.RequestException,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
        ):
            # No provider/server error bodies or URLs from redirects in logs.
            pass
        report["checks"].append(item)

    identity = {}

    def health(data):
        if not isinstance(data, dict):
            return False
        revision = data.get("revision")
        identity["revision"] = (
            revision
            if isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}", revision)
            else "unknown"
        )
        identity["mobile_contract_version"] = (
            data.get("mobile_contract_version")
            if type(data.get("mobile_contract_version")) is int
            else None
        )
        return data.get("status") == "ok"

    probe("health", "/health", health)
    report["observed_revision"] = identity.get("revision", "unknown")
    report["observed_mobile_contract_version"] = identity.get(
        "mobile_contract_version"
    )
    if expected_revision is not None:
        report["expected_revision"] = expected_revision
        report["checks"].append(
            dict(
                name="deployed_revision_and_contract",
                path="/health",
                status=report["checks"][0]["status"],
                passed=(
                    report["checks"][0]["passed"]
                    and identity.get("revision") == expected_revision
                    and identity.get("mobile_contract_version") == 2
                ),
            )
        )
    probe(
        "mobile_pkce_v2_google",
        "/auth/mobile/config",
        lambda d: (
            isinstance(d, dict)
            and d.get("mobile_auth_version") == 2
            and d.get("pkce_method") == "S256"
            and d.get("code_exchange_path") == "/auth/mobile/exchange"
            and d.get("google_configured") is True
            and d.get("redirect_uri") == base + "/auth/google-callback-mobile"
        ),
    )

    def catalogue(data):
        if not isinstance(data, list):
            return False
        rows = {
            s["slug"]: s
            for s in data
            if isinstance(s, dict) and s.get("slug") in SUBJECTS
        }
        return set(rows) == SUBJECTS and all(
            row.get("available", True) is True
            and isinstance(row.get("grades"), list)
            and row["grades"]
            and all(type(g) is int and 5 <= g <= 11 for g in row["grades"])
            for row in rows.values()
        )

    probe("five_subject_mobile_catalogue", "/mobile/skills/subjects", catalogue)
    # Verify read-only grade availability across the full range. Never ask for
    # personal tree/profile/progress endpoints without an owned test identity.
    for slug in sorted(SUBJECTS):
        probe(
            "grades_" + slug,
            "/mobile/skills/subjects/" + slug + "/grades",
            lambda d: (
                isinstance(d, dict)
                and isinstance(d.get("grades"), list)
                and bool(d["grades"])
                and all(
                    isinstance(g, dict)
                    and type(g.get("grade")) is int
                    and 5 <= g["grade"] <= 11
                    and type(g.get("ready_lessons")) is int
                    and g["ready_lessons"] > 0
                    for g in d["grades"]
                )
            ),
        )
    if require_release_operations or require_google_account_deletion:
        def deletion_available(data):
            if (
                not isinstance(data, dict)
                or data.get("available") is not True
                or data.get("web_path") != "/account-deletion"
            ):
                return False
            email_required = data.get("email_required")
            if require_google_account_deletion and email_required is not False:
                return False
            if email_required is False:
                methods = data.get("reauthentication_methods")
                return isinstance(methods, list) and "google" in methods
            return True

        probe(
            "database_readiness",
            "/readyz",
            lambda data: isinstance(data, dict) and data.get("status") == "ready",
        )
        probe(
            "account_deletion_available",
            "/account/deletion/config",
            deletion_available,
        )
        probe("subject_chat_route", "/mobile/subject-chat", expect_post_route=True)
        probe("lesson_study_help_route", "/mobile/study-help", expect_post_route=True)
    if require_ai_reporting:
        probe("ai_answer_report_route", "/mobile/ai-answer-report", expect_post_route=True)
    report["contract_ready"] = all(c["passed"] for c in report["checks"])
    report["decision"] = (
        "FURTHER_ACCEPTANCE_REQUIRED" if report["contract_ready"] else "NO-GO"
    )
    report["not_tested"] = [
        "real_google_login",
        "account_deletion",
        "data_safety",
        "signed_upgrade",
        "user_progress",
        "real_hosted_ai_generation",
        "authenticated_ai_answer_reporting",
        "provider_audience_approval",
        "device_performance",
    ]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--expected-revision",
        help="Require the exact approved40-character deployed SHA and mobile contract2",
    )
    parser.add_argument(
        "--require-release-operations",
        action="store_true",
        help="Also require database readiness, account deletion and both mobile AI routes",
    )
    parser.add_argument(
        "--require-google-account-deletion",
        action="store_true",
        help="Require release operations and Google reauthentication without email OTP",
    )
    parser.add_argument(
        "--require-ai-reporting", action="store_true", help="Check the AI answer report route",
    )
    args = parser.parse_args()
    try:
        report = check(
            args.origin,
            expected_revision=args.expected_revision,
            require_release_operations=args.require_release_operations,
            require_google_account_deletion=args.require_google_account_deletion,
            require_ai_reporting=args.require_ai_reporting,
        )
    except ValueError as error:
        # Fixed validation messages only; never echo a malformed URL/credential.
        parser.exit(2, str(error) + "\n")
    encoded = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf8")
    print(encoded)
    return 0 if report["contract_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
