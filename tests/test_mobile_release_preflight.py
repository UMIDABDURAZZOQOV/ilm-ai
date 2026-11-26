from types import SimpleNamespace

import pytest
import requests

from scripts.mobile_release_preflight import SUBJECTS, check, origin


@pytest.mark.parametrize("fault", [
    None, "missing_lesson", "short_summary", "wrong_grade", "duplicate_grade",
    "duplicate_subject", "no_availability",
])
def test_release_103_checks_the_reviewed_counts_in_both_views(fault):
    counts = dict(biologiya=355, fizika=280, kimyo=204, jahon_tarixi=219, ozbekiston_tarixi=172)

    def get(url, **kwargs):
        if url.endswith("/subjects"):
            rows = [dict(slug=s, available=True, grades=[7, 8], ready_lessons=n)
                    for s, n in counts.items()]
            if fault == "duplicate_subject":
                rows.append(rows[0].copy())
            if fault == "no_availability":
                del rows[0]["available"]
            if fault == "short_summary":
                rows[0]["ready_lessons"] -= 1
            return response(200, rows)
        if url.endswith("/grades"):
            slug = url.split("/")[-2]
            grades = [dict(grade=7, ready_lessons=1), dict(grade=8, ready_lessons=counts[slug]-1)]
            if slug == "biologiya":
                if fault == "wrong_grade":
                    grades[1]["grade"] = 9
                if fault == "duplicate_grade":
                    grades[1]["grade"] = 7
                if fault == "missing_lesson":
                    grades[1]["ready_lessons"] -= 1
            return response(200, {"grades": grades})
        return good_get(url, **kwargs)

    assert check("https://example.test", get, require_103_publication=True)["contract_ready"] is (fault is None)


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


def response(status, body, headers=None):
    return SimpleNamespace(status_code=status, json=lambda: body, headers=headers or {})


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
    if url.endswith("/readyz"):
        return response(200, {"status": "ready"})
    if url.endswith("/account/deletion/config"):
        return response(200, {"available": True, "web_path": "/account-deletion"})
    if url.endswith(("/mobile/subject-chat", "/mobile/study-help")):
        return response(405, None, {"Allow": "POST"})
    return response(200, [dict(slug=s, grades=[7], available=True) for s in SUBJECTS])


def test_passing_contract_is_not_production_signoff():
    result = check("https://example.test", good_get)
    assert len(result["checks"]) == 8 and result["contract_ready"]
    assert result["decision"] == "FURTHER_ACCEPTANCE_REQUIRED"
    assert result["production_signoff"] is False


def test_ai_reporting_option_checks_route_without_submitting_a_report():
    def get(url, **kwargs):
        if url.endswith('/ai-answer-report'):
            return response(405, None, {'Allow': 'POST'})
        return good_get(url, **kwargs)

    result = check('https://example.test', get, require_ai_reporting=True)
    assert result['checks'][-1]['name'] == 'ai_answer_report_route'
    assert result['contract_ready'] and not result['production_signoff']
    assert 'authenticated_ai_answer_reporting' in result['not_tested']
    assert not check('https://example.test', good_get, require_ai_reporting=True)['contract_ready']


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


@pytest.mark.parametrize('ready,deletion_available,expected', [
    (True, True, True),
    (False, True, False),
    (True, False, False),
])
def test_release_operations_require_ready_database_and_available_deletion(ready, deletion_available, expected):
    def get(url, **kwargs):
        if url.endswith('/readyz'):
            return response(200 if ready else 503, {'status': 'ready' if ready else 'not_ready'})
        if url.endswith('/account/deletion/config'):
            return response(200, {'available': deletion_available, 'web_path': '/account-deletion'})
        return good_get(url, **kwargs)

    result = check('https://example.test', get, require_release_operations=True)
    assert len(result['checks']) == 12
    assert result['contract_ready'] is expected
    assert result['production_signoff'] is False


@pytest.mark.parametrize("path", ["/mobile/subject-chat", "/mobile/study-help"])
@pytest.mark.parametrize("status,allow", [(404, ""), (405, ""), (405, "GET"), (200, "POST")])
def test_release_operations_fail_for_missing_or_wrong_ai_route(path, status, allow):
    def get(url, **kwargs):
        if url.endswith(path):
            return response(status, "PRIVATE-BODY", {"Allow": allow})
        return good_get(url, **kwargs)

    result = check("https://example.test", get, require_release_operations=True)
    failed = [item for item in result["checks"] if not item["passed"]]
    assert [item["path"] for item in failed] == [path]
    assert result["decision"] == "NO-GO"
    assert "real_hosted_ai_generation" in result["not_tested"]
    assert "PRIVATE" not in str(result)


@pytest.mark.parametrize("methods,expected", [(["password"], False), ("google", False), (["google", "password"], True)])
def test_email_free_release_requires_google_deletion_method(methods, expected):
    def get(url, **kwargs):
        if url.endswith("/account/deletion/config"):
            return response(200, {
                "web_path": "/account-deletion", "available": True,
                "email_required": False, "reauthentication_methods": methods,
            })
        return good_get(url, **kwargs)

    result = check("https://example.test", get, require_release_operations=True)
    assert result["contract_ready"] is expected
    assert result["production_signoff"] is False


@pytest.mark.parametrize(
    "capability, expected",
    [
        ({}, False),
        ({"email_required": True, "reauthentication_methods": ["google"]}, False),
        ({"email_required": False, "reauthentication_methods": ["password"]}, False),
        ({"email_required": False, "reauthentication_methods": ["google"]}, True),
    ],
)
def test_google_account_deletion_gate_rejects_legacy_email_only_mode(capability, expected):
    def get(url, **kwargs):
        if url.endswith("/account/deletion/config"):
            return response(200, {
                "available": True,
                "web_path": "/account-deletion",
                **capability,
            })
        return good_get(url, **kwargs)

    result = check("https://example.test", get, require_google_account_deletion=True)
    assert len(result["checks"]) == 12
    assert result["contract_ready"] is expected
    assert result["production_signoff"] is False


@pytest.mark.parametrize("revision", ["short", "A" * 40, "private-token", "f" * 41])
def test_revision_input_is_strict_and_not_reflected(revision):
    with pytest.raises(ValueError) as error:
        check("https://example.test", good_get, expected_revision=revision)
    assert str(error.value) == "expected_revision_must_be_full_lowercase_git_sha"


@pytest.mark.parametrize(
    "identity,accepted",
    [
        ({"revision": "a" * 40, "mobile_contract_version": 2}, True),
        ({"revision": "b" * 40, "mobile_contract_version": 2}, False),
        ({"revision": "a" * 7, "mobile_contract_version": 2}, False),
        ({"revision": "a" * 40, "mobile_contract_version": 1}, False),
        ({"revision": "a" * 40, "mobile_contract_version": True}, False),
        ({"revision": "PRIVATE-VALUE", "mobile_contract_version": "PRIVATE"}, False),
        ({}, False),
    ],
)
def test_expected_deployment_requires_exact_public_identity(identity, accepted):
    calls = []

    def get(url, **kwargs):
        calls.append(url)
        if url.endswith("/health"):
            return response(200, {"status": "ok", **identity})
        return good_get(url, **kwargs)

    result = check("https://example.test", get, expected_revision="a" * 40)
    assert result["contract_ready"] is accepted
    assert result["production_signoff"] is False
    assert len(calls) == 8  # One health request, never authenticated or mutating.
    assert "PRIVATE" not in str(result)
