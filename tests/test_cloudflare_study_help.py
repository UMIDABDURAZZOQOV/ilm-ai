"""Workers AI transport/config tests: no network, real token or database."""

import json
from types import SimpleNamespace

import pytest
import requests

from services.cloudflare_study_help import CloudflareEvidenceSelector, FREE_MODEL
from services.study_help_provider import SelectorUnavailable, load_provider
from test_study_help_provider import CONTEXT


@pytest.fixture
def transport(monkeypatch):
    state = SimpleNamespace(
        calls=[],
        status=200,
        headers={},
        sessions=[],
        envelope={
            "success": True,
            "errors": [],
            "result": {"response": {"ids": ["e1"]}},
        },
        exception=None,
        raw=None,
    )

    class Response:
        @property
        def status_code(self):
            return state.status

        @property
        def headers(self):
            return state.headers

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def iter_content(self, chunk_size):
            yield (
                state.raw
                if state.raw is not None
                else json.dumps(state.envelope).encode()
            )

    class Session:
        trust_env = True

        def __enter__(self):
            state.sessions.append(self)
            return self

        def __exit__(self, *args):
            pass

        def post(self, url, **kwargs):
            state.calls.append((url, kwargs))
            if state.exception:
                raise state.exception
            return Response()

    monkeypatch.setattr(requests, "Session", Session)
    return state


def config():
    return dict(
        provider="cloudflare",
        model=FREE_MODEL,
        api_keys=["unit-test-cloudflare-token"],
        audience_review_reference="technical review fixture",
        account_id="a" * 32,
        free_only=True,
        free_plan_review_reference="verified Workers Free fixture",
    )


def test_explicit_private_config_supports_free_cloudflare(tmp_path):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(config()))
    selector = load_provider(path)
    assert isinstance(selector, CloudflareEvidenceSelector)
    assert "unit-test-cloudflare-token" not in repr(selector)


@pytest.mark.parametrize(
    "change",
    [
        {"free_only": False},
        {"free_only": 1},
        {"free_plan_review_reference": ""},
        {"account_id": "../outside"},
        {"account_id": "a" * 31},
        {"model": "@cf/zai-org/glm-5.3"},
        {"model": "https://untrusted.invalid"},
        {"api_keys": ["unit-test-token-a", "unit-test-token-b"]},
        {"base_url": "https://untrusted.invalid"},
        {"api_keys": ["AQ.synthetic-not-a-credential"]},
    ],
)
def test_paid_unreviewed_or_arbitrary_config_is_rejected(tmp_path, change):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(dict(config(), **change)))
    with pytest.raises(ValueError) as error:
        load_provider(path)
    assert "unit-test" not in str(error.value)


def test_schema_and_source_only_payload_without_proxy_redirect_or_billing(transport):
    selector = CloudflareEvidenceSelector("unit-test-cloudflare-token", "a" * 32)
    assert selector.select(CONTEXT) == ["e1"]
    url, kwargs = transport.calls[0]
    assert (
        url
        == "https://api.cloudflare.com/client/v4/accounts/"
        + "a" * 32
        + "/ai/run/"
        + FREE_MODEL
    )
    assert kwargs["allow_redirects"] is False and kwargs["stream"] is True
    assert kwargs["timeout"] == (3, 6)
    assert transport.sessions[0].trust_env is False
    body = kwargs["json"]
    assert body["max_tokens"] == 256 and body["stream"] is False
    assert body["response_format"]["json_schema"]["additionalProperties"] is False
    assert "PRIVATE-" not in json.dumps(body)
    assert "unit-test-cloudflare-token" not in json.dumps(body)
    assert len(transport.calls) == 1


@pytest.mark.parametrize("value", [{"ids": ["e1"]}, '{"ids":["e1"]}'])
def test_structured_object_or_string_response_supported(transport, value):
    transport.envelope["result"]["response"] = value
    assert CloudflareEvidenceSelector("unit-test-token", "a" * 32).select(CONTEXT) == [
        "e1"
    ]


@pytest.mark.parametrize(
    "status", [301, 302, 400, 401, 403, 404, 408, 413, 429, 500, 503]
)
def test_upstream_errors_never_upgrade_rotate_or_retry(transport, status):
    transport.status = status
    with pytest.raises(SelectorUnavailable) as error:
        CloudflareEvidenceSelector("unit-test-token", "a" * 32).select(CONTEXT)
    assert str(error.value) == "" and len(transport.calls) == 1


def test_free_daily_quota_pauses_until_next_utc_day(transport):
    now, wall = [100.0], [86400.0 + 3600]
    transport.status = 429
    transport.envelope = {"success": False, "errors": [{"code": 3036}]}
    selector = CloudflareEvidenceSelector(
        "unit-test-token", "a" * 32, clock=lambda: now[0], wall=lambda: wall[0]
    )
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    now[0] += 60
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(transport.calls) == 1
    now[0] = 100 + 86400 - 3600
    wall[0] = 86400 * 2
    transport.status = 200
    transport.envelope = {
        "success": True,
        "errors": [],
        "result": {"response": {"ids": ["e1"]}},
    }
    assert selector.select(CONTEXT) == ["e1"]


@pytest.mark.parametrize("status", [429, 503])
def test_retry_after_is_global_and_nonblocking(transport, status):
    now = [100.0]
    transport.status = status
    transport.headers = {"retry-after": "180"}
    selector = CloudflareEvidenceSelector(
        "unit-test-token", "a" * 32, clock=lambda: now[0]
    )
    for instant in [100, 150, 279]:
        now[0] = instant
        with pytest.raises(SelectorUnavailable):
            selector.select(CONTEXT)
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "exception",
    [requests.Timeout("private upstream"), requests.ConnectionError("private token")],
)
def test_network_errors_are_sanitized_without_second_provider(transport, exception):
    transport.exception = exception
    with pytest.raises(SelectorUnavailable) as error:
        CloudflareEvidenceSelector("unit-test-token", "a" * 32).select(CONTEXT)
    assert str(error.value) == "" and len(transport.calls) == 1


@pytest.mark.parametrize(
    "value",
    [
        {"ids": ["e1"], "prose": "invented"},
        {"ids": ["e1", "e1"]},
        {"ids": [3]},
        {"ids": "e1"},
        {"ids": ["e1"] * 13},
        None,
        "not json",
    ],
)
def test_untrusted_model_output_falls_back(transport, value):
    transport.envelope["result"]["response"] = value
    with pytest.raises(SelectorUnavailable):
        CloudflareEvidenceSelector("unit-test-token", "a" * 32).select(CONTEXT)


def test_oversized_response_is_rejected(transport):
    transport.raw = b"x" * 32769
    with pytest.raises(SelectorUnavailable):
        CloudflareEvidenceSelector("unit-test-token", "a" * 32).select(CONTEXT)
