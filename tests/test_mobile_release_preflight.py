from types import SimpleNamespace

import pytest
import requests

from scripts.mobile_release_preflight import SUBJECTS, check, origin


@pytest.mark.parametrize(
    "value",
    [
        "http://example.test",
        "https://user:secret@example.test",
        "https://example.test?api_key=secret",
        "https://example.test/a",
        "https://example.test#secret",
        "https://example.test:bad",
        "https://example.test:8931",
    ],
)
def test_unsafe_origin_is_rejected(value):
    with pytest.raises(ValueError) as error:
        origin(value)
    assert "secret" not in str(error.value)


def response(status, body):
    return SimpleNamespace(status_code=status, json=lambda: body)


def good_get(url, **kwargs):
    assert kwargs["allow_redirects"] is False
    if url.endswith("/health"):
        return response(200, {"status": "ok"})
    if url.endswith("/auth/mobile/config"):
        return response(
            200,
            dict(
                mobile_auth_version=2,
                pkce_method="S256",
                code_exchange_path="/auth/mobile/exchange",
                google_configured=True,
                redirect_uri="https://example.test/auth/google-callback-mobile",
            ),
        )
    if url.endswith("/grades"):
        return response(200, {"grades": [{"grade": 7, "ready_lessons": 1}]})
    return response(200, [dict(slug=s, grades=[7], available=True) for s in SUBJECTS])


def test_passing_contract_is_not_production_signoff():
    result = check("https://example.test", good_get)
    assert len(result["checks"]) == 8 and result["contract_ready"]
    assert result["decision"] == "FURTHER_ACCEPTANCE_REQUIRED"
    assert result["production_signoff"] is False


@pytest.mark.parametrize("status", [301, 302, 401, 403, 404, 429, 500])
def test_missing_or_redirected_contract_fails_closed_without_body(status):
    result = check(
        "https://example.test", lambda *a, **k: response(status, "PRIVATE-RESPONSE")
    )
    assert result["decision"] == "NO-GO"
    assert "PRIVATE" not in str(result)


def test_network_error_does_not_reveal_url_or_exception():
    def fail(*args, **kwargs):
        raise requests.ConnectionError("PRIVATE-ERROR")

    result = check("https://example.test", fail)
    assert result["decision"] == "NO-GO" and "PRIVATE" not in str(result)


def test_legacy_biology_only_catalogue_does_not_pass():
    def get(url, **kwargs):
        if url.endswith("/subjects"):
            return response(200, [dict(slug="biologiya", grades=[7])])
        return good_get(url, **kwargs)

    assert check("https://example.test", get)["decision"] == "NO-GO"
