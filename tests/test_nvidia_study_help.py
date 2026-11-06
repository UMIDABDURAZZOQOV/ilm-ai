"""NVIDIA trial contract with fake transport: no actual token or network."""

import json
from types import SimpleNamespace

import pytest
import requests

from services.nvidia_study_help import (
    NVIDIA_MODEL,
    NVIDIA_URL,
    NvidiaTrialEvidenceSelector,
)
from services.study_help_provider import SelectorUnavailable, load_provider
from test_study_help_provider import CONTEXT


KEYS = ["nvapi-synthetic-test-only-" + str(i) for i in range(8)]


@pytest.fixture(autouse=True)
def trial_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("ILM_BETA_ENABLED", "true")


@pytest.fixture
def nvidia_transport(monkeypatch):
    state = SimpleNamespace(
        calls=[],
        sessions=[],
        statuses=[200],
        headers={},
        exception=None,
        raw=None,
        envelope={
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": '{"ids":["e1"]}',
                        "reasoning_content": "PRIVATE-REASONING",
                    },
                }
            ]
        },
    )

    class Response:
        def __init__(self, status):
            self.status_code, self.headers = status, state.headers

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
            return Response(
                state.statuses.pop(0) if len(state.statuses) > 1 else state.statuses[0]
            )

    monkeypatch.setattr(requests, "Session", Session)
    return state


def config():
    return dict(
        provider="nvidia_trial",
        model=NVIDIA_MODEL,
        api_keys=KEYS,
        audience_review_reference="synthetic technical review",
        free_only=True,
        usage="internal_evaluation",
        trial_review_reference="internal evaluation terms fixture",
    )


def test_eight_authorized_standby_keys_are_private_config_only(tmp_path):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(config()))
    assert isinstance(load_provider(path), NvidiaTrialEvidenceSelector)


@pytest.mark.parametrize(
    "change",
    [
        {"free_only": False},
        {"free_only": 1},
        {"usage": "production"},
        {"model": "other/model"},
        {"base_url": "https://untrusted.invalid"},
        {"trial_review_reference": ""},
        {"api_keys": ["AQ.synthetic-wrong-format"]},
        {"api_keys": ["hf_synthetic-wrong-format"]},
        {"api_keys": KEYS + ["nvapi-ninth-test-key"]},
    ],
)
def test_invalid_unreviewed_paid_or_foreign_provider_config_rejected(tmp_path, change):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(dict(config(), **change)))
    with pytest.raises(ValueError) as error:
        load_provider(path)
    assert not any(k in str(error.value) for k in KEYS)


@pytest.mark.parametrize(
    "environment,beta",
    [("production", "true"), ("development", "true"), ("test", "false"), ("", "")],
)
def test_not_allowed_outside_internal_test_beta(
    tmp_path, monkeypatch, nvidia_transport, environment, beta
):
    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("ILM_BETA_ENABLED", beta)
    path = tmp_path / "private.json"
    path.write_text(json.dumps(config()))
    with pytest.raises(ValueError):
        load_provider(path)
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert nvidia_transport.calls == []


def test_fixed_endpoint_source_only_payload_and_no_reasoning_exposed(nvidia_transport):
    assert NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT) == ["e1"]
    url, kwargs = nvidia_transport.calls[0]
    assert url == NVIDIA_URL
    assert kwargs["allow_redirects"] is False and kwargs["stream"] is True
    assert kwargs["timeout"] == (3, 6)
    assert nvidia_transport.sessions[0].trust_env is False
    payload = kwargs["json"]
    assert payload["model"] == NVIDIA_MODEL and payload["max_tokens"] == 256
    assert payload["reasoning_effort"] == "none" and payload["tool_choice"] == "none"
    assert payload["temperature"] == 0.95 and payload["stream"] is False
    assert "response_format" not in payload and "store" not in payload
    assert "PRIVATE-" not in json.dumps(payload)
    assert not any(key in json.dumps(payload) for key in KEYS)


def test_permission_failure_stops_pool(nvidia_transport):
    nvidia_transport.statuses = [403]
    selector = NvidiaTrialEvidenceSelector(KEYS)
    for _ in range(2):
        with pytest.raises(SelectorUnavailable):
            selector.select(CONTEXT)
    assert len(nvidia_transport.calls) == 1


@pytest.mark.parametrize("status", [402, 429])
def test_exhausted_or_throttled_key_automatically_uses_next(nvidia_transport, status):
    nvidia_transport.statuses = [status, 200]
    selector = NvidiaTrialEvidenceSelector(KEYS)
    assert selector.select(CONTEXT) == ["e1"]
    assert len(nvidia_transport.calls) == 2
    assert (
        nvidia_transport.calls[0][1]["headers"]["Authorization"] == "Bearer " + KEYS[0]
    )
    assert (
        nvidia_transport.calls[1][1]["headers"]["Authorization"] == "Bearer " + KEYS[1]
    )
    assert selector.select(CONTEXT) == ["e1"]
    assert (
        nvidia_transport.calls[2][1]["headers"]["Authorization"] == "Bearer " + KEYS[1]
    )


@pytest.mark.parametrize("status", [402, 429])
def test_all_eight_exhausted_or_throttled_stop_without_infinite_retries(
    nvidia_transport, status
):
    nvidia_transport.statuses = [status]
    selector = NvidiaTrialEvidenceSelector(KEYS)
    for _ in range(2):
        with pytest.raises(SelectorUnavailable):
            selector.select(CONTEXT)
    assert len(nvidia_transport.calls) == 8
    assert (
        len({kw["headers"]["Authorization"] for _, kw in nvidia_transport.calls}) == 8
    )


def test_key_retry_after_is_respected_and_later_recovers(nvidia_transport):
    now = [100.0]
    nvidia_transport.statuses = [429]
    nvidia_transport.headers = {"Retry-After": "180"}
    selector = NvidiaTrialEvidenceSelector(KEYS, clock=lambda: now[0])
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(nvidia_transport.calls) == 8
    now[0] = 279.0
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(nvidia_transport.calls) == 8
    now[0] = 280.0
    nvidia_transport.statuses = [200]
    assert selector.select(CONTEXT) == ["e1"]
    assert len(nvidia_transport.calls) == 9


def test_last_of_eight_keys_can_succeed_after_seven_quota_failures(nvidia_transport):
    nvidia_transport.statuses = [402] * 7 + [200]
    selector = NvidiaTrialEvidenceSelector(KEYS)
    assert selector.select(CONTEXT) == ["e1"]
    assert len(nvidia_transport.calls) == 8
    assert (
        nvidia_transport.calls[-1][1]["headers"]["Authorization"] == "Bearer " + KEYS[7]
    )


def test_no_new_attempt_after_admission_deadline(nvidia_transport, monkeypatch):
    from services import nvidia_study_help

    ticks = iter([100.0, 113.0])
    monkeypatch.setattr(nvidia_study_help.time, "monotonic", lambda: next(ticks))
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert nvidia_transport.calls == []


@pytest.mark.parametrize("status", [401, 500, 503])
def test_bounded_authorized_standby_for_invalid_key_or_service_error(
    nvidia_transport, status
):
    nvidia_transport.statuses = [status, 200]
    assert NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT) == ["e1"]
    assert len(nvidia_transport.calls) == 2
    assert (
        nvidia_transport.calls[0][1]["headers"]["Authorization"] == "Bearer " + KEYS[0]
    )
    assert (
        nvidia_transport.calls[1][1]["headers"]["Authorization"] == "Bearer " + KEYS[1]
    )


@pytest.mark.parametrize("status", [401, 500])
def test_at_most_two_attempts_with_eight_keys(nvidia_transport, status):
    nvidia_transport.statuses = [status]
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert len(nvidia_transport.calls) == 2


def test_retry_after_pauses_whole_pool_without_sleep(nvidia_transport):
    nvidia_transport.statuses = [503]
    nvidia_transport.headers = {"Retry-After": "180"}
    now = [10]
    selector = NvidiaTrialEvidenceSelector(KEYS, clock=lambda: now[0])
    for instant in [10, 80, 189]:
        now[0] = instant
        with pytest.raises(SelectorUnavailable):
            selector.select(CONTEXT)
    assert len(nvidia_transport.calls) == 1


@pytest.mark.parametrize("status", [202, 301, 302, 400, 404, 408, 422])
def test_no_polling_redirect_or_retry_for_other_responses(nvidia_transport, status):
    nvidia_transport.statuses = [status]
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert len(nvidia_transport.calls) == 1


@pytest.mark.parametrize(
    "change",
    [
        {"finish_reason": "length"},
        {"finish_reason": "tool_calls"},
        {"message": {"content": '{"ids":["e1"]}', "tool_calls": [{"name": "bad"}]}},
        {"message": {"content": "invented prose"}},
        {"message": {"content": '{"ids":["e1"],"prose":"invented"}'}},
        {"message": {"content": '{"ids":["e1","e1"]}'}},
        {"message": {"content": '{"ids":[1]}'}},
        {"message": {"content": None}},
        {"message": {"content": '{"ids":"e1"}'}},
        {"message": {"content": json.dumps({"ids": [str(i) for i in range(13)]})}},
    ],
)
def test_malformed_truncated_prose_and_tool_outputs_rejected(nvidia_transport, change):
    nvidia_transport.envelope["choices"][0].update(change)
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert len(nvidia_transport.calls) == 1


def test_response_size_cap_includes_ignored_reasoning(nvidia_transport):
    nvidia_transport.envelope["choices"][0]["message"]["reasoning_content"] = (
        "x" * 32769
    )
    with pytest.raises(SelectorUnavailable):
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)


@pytest.mark.parametrize(
    "exception,count",
    [
        (requests.Timeout("private token"), 1),
        (requests.ConnectionError("private token"), 2),
    ],
)
def test_transport_errors_sanitized(nvidia_transport, exception, count):
    nvidia_transport.exception = exception
    with pytest.raises(SelectorUnavailable) as error:
        NvidiaTrialEvidenceSelector(KEYS).select(CONTEXT)
    assert str(error.value) == "" and len(nvidia_transport.calls) == count
