"""No network, real credentials, database or student data used by this suite."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from types import SimpleNamespace
import sys
import threading

import pytest

from services.study_help_provider import (
    EvidenceSelector,
    SelectorUnavailable,
    load_provider,
)


CONTEXT = dict(
    subject="kimyo",
    grade=7,
    title="Reviewed topic",
    question="Reviewed question",
    user_id="PRIVATE-USER",
    attempt_id="PRIVATE-ATTEMPT",
    selected_answer="PRIVATE-ANSWER",
    message="PRIVATE-MESSAGE",
    evidence=[
        dict(
            id="e1",
            kind="cards",
            text="Reviewed explanation",
            source_refs=[{"private_path": "PRIVATE-PATH"}],
        ),
        dict(id="e2", kind="feedback", text="PRIVATE-FEEDBACK"),
    ],
)


class UpstreamError(Exception):
    def __init__(self, status, headers=None):
        super().__init__("PRIVATE-KEY PRIVATE-UPSTREAM-BODY")
        self.status_code = status
        self.response = SimpleNamespace(headers=headers or {})


@pytest.fixture
def fake_sdk(monkeypatch):
    state = SimpleNamespace(calls=[], results=[], configs=[])

    class ConnectionError(Exception):
        pass

    class APITimeoutError(ConnectionError):
        pass

    class Client:
        def __init__(self, **config):
            state.configs.append(config)
            self.chat = SimpleNamespace(completions=self)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def create(self, **kwargs):
            state.calls.append(kwargs)
            result = state.results.pop(0) if state.results else {"ids": ["e1"]}
            if callable(result):
                result = result()
            if isinstance(result, Exception):
                raise result
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(message=SimpleNamespace(content=json.dumps(result)))
                ]
            )

    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(
            OpenAI=Client,
            APIConnectionError=ConnectionError,
            APITimeoutError=APITimeoutError,
        ),
    )
    state.connection_error = ConnectionError
    state.timeout_error = APITimeoutError
    return state


def config():
    return dict(
        provider="openai",
        model="configured-model",
        api_keys=["unit-test-key-a", "unit-test-key-b"],
        audience_review_reference="Operator review artifact; not a legal approval",
    )


def test_config_is_explicit_and_keys_are_not_in_repr(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEYS", "environment-must-not-be-read")
    path = tmp_path / "private.json"
    path.write_text(json.dumps(config()), encoding="utf8")
    provider = load_provider(path)
    assert "unit-test-key" not in repr(provider)
    assert len(provider._keys) == 2


@pytest.mark.parametrize(
    "change",
    [
        {"provider": "gemini"},
        {"api_keys": ["AQ.synthetic-not-a-credential"]},
        {"api_keys": ["AIza-synthetic-not-a-credential"]},
        {"api_keys": []},
        {"api_keys": ["duplicate-test-key"] * 2},
        {"api_keys": ["unit-test-key"] * 9},
        {"api_keys": ["with whitespace"]},
        {"api_keys": "not-a-list"},
        {"audience_review_reference": ""},
        {"model": None},
        {"base_url": "https://evil.invalid"},
    ],
)
def test_invalid_config_is_rejected_without_secret_text(tmp_path, change):
    data = dict(config(), **change)
    path = tmp_path / "private.json"
    path.write_text(json.dumps(data), encoding="utf8")
    with pytest.raises(ValueError) as caught:
        load_provider(path)
    assert "unit-test-key" not in str(caught.value)
    assert "AQ." not in str(caught.value)


def test_unreviewed_legacy_config_and_malformed_json_fail_closed(tmp_path):
    path = tmp_path / "private.json"
    for text in [
        '{"api_key":"private-placeholder","model":"m"}',
        "{private-placeholder",
    ]:
        path.write_text(text)
        with pytest.raises(ValueError, match="invalid_private_ai_config"):
            load_provider(path)


def test_checkout_config_rejected():
    with pytest.raises(ValueError, match="outside_checkout"):
        load_provider(__file__)


@pytest.mark.parametrize("worktree", [False, True])
def test_config_in_another_git_checkout_is_rejected(tmp_path, worktree):
    root = tmp_path / "other-repository"
    root.mkdir()
    marker = root / ".git"
    if worktree:
        marker.write_text("gitdir: synthetic-worktree-metadata")
    else:
        marker.mkdir()
    path = root / "private.json"
    path.write_text(json.dumps(config()))
    with pytest.raises(ValueError, match="outside_checkout"):
        load_provider(path)


def test_payload_contains_reviewed_material_only_and_requests_do_not_store(fake_sdk):
    selector = EvidenceSelector(["unit-test-key"], "configured-model")
    assert selector.select(CONTEXT) == ["e1"]
    call = fake_sdk.calls[0]
    assert call["store"] is False and call["max_completion_tokens"] == 1024
    body = json.dumps(call)
    assert "PRIVATE-" not in body
    assert "Reviewed explanation" in body
    assert fake_sdk.configs[0]["base_url"] == "https://api.openai.com/v1"
    assert fake_sdk.configs[0]["max_retries"] == 0
    assert fake_sdk.configs[0]["timeout"] == 6.0


@pytest.mark.parametrize("status", [401, 500, 502, 503])
def test_authorized_failure_switches_to_next_key(fake_sdk, status):
    fake_sdk.results = [UpstreamError(status), {"ids": ["e1"]}]
    selector = EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m")
    assert selector.select(CONTEXT) == ["e1"]
    assert [c["api_key"] for c in fake_sdk.configs] == [
        "unit-test-key-a",
        "unit-test-key-b",
    ]
    assert selector.select(CONTEXT) == ["e1"]
    assert fake_sdk.configs[-1]["api_key"] == "unit-test-key-b"


@pytest.mark.parametrize("status", [400, 403, 404, 422, 429])
def test_request_permission_and_quota_errors_do_not_sweep_accounts(fake_sdk, status):
    fake_sdk.results = [UpstreamError(status)]
    selector = EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m")
    with pytest.raises(SelectorUnavailable) as caught:
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 1
    assert "PRIVATE" not in str(caught.value)


@pytest.mark.parametrize("status", [429, 503])
def test_retry_after_pauses_entire_pool_without_sleep(fake_sdk, status):
    now = [100.0]
    fake_sdk.results = [UpstreamError(status, {"retry-after": "180"})]
    selector = EvidenceSelector(
        ["unit-test-key-a", "unit-test-key-b"], "m", clock=lambda: now[0]
    )
    for t in [100.0, 200.0, 279.0]:
        now[0] = t
        with pytest.raises(SelectorUnavailable):
            selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 1
    now[0] = 280.0
    assert selector.select(CONTEXT) == ["e1"]


@pytest.mark.parametrize(
    "code",
    [
        "insufficient_quota",
        "credit_balance_exhausted",
        "organization_usage_limit_exceeded",
        "organization_spend_limit_exceeded",
        "project_spend_limit_exceeded",
    ],
)
def test_exhausted_budget_stops_all_keys_until_operator_reconfiguration(fake_sdk, code):
    error = UpstreamError(429)
    error.body = {"error": {"code": code}}
    fake_sdk.results = [error]
    clock = [100.0]
    selector = EvidenceSelector(
        ["unit-test-key-a", "unit-test-key-b"], "m", clock=lambda: clock[0]
    )
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    clock[0] += 86400
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 1


def test_no_unbounded_retry_with_eight_keys(fake_sdk):
    fake_sdk.results = [UpstreamError(500)] * 8
    selector = EvidenceSelector([f"unit-test-key-{i}" for i in range(8)], "m")
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 2


def test_timeout_does_not_duplicate_potentially_billed_request(fake_sdk):
    fake_sdk.results = [fake_sdk.timeout_error()]
    selector = EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m")
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 1


def test_connection_failure_can_use_second_key(fake_sdk):
    fake_sdk.results = [fake_sdk.connection_error()]
    selector = EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m")
    assert selector.select(CONTEXT) == ["e1"] and len(fake_sdk.calls) == 2


def test_budget_reserves_failed_attempts_and_resets_utc_day(fake_sdk):
    clock = [100.0]
    wall = [datetime(2026, 11, 6, tzinfo=timezone.utc).timestamp()]
    selector = EvidenceSelector(
        ["unit-test-key"], "m", clock=lambda: clock[0], wall=lambda: wall[0]
    )
    for _ in range(20):
        selector.select(CONTEXT)
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    clock[0] += 61
    selector._daily_calls = 1000
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    wall[0] += 86400
    assert selector.select(CONTEXT) == ["e1"]


def test_large_payload_never_calls_provider(fake_sdk):
    context = dict(CONTEXT, question="x" * 24001)
    with pytest.raises(SelectorUnavailable):
        EvidenceSelector(["unit-test-key"], "m").select(context)
    assert not fake_sdk.calls


@pytest.mark.parametrize("result", [{"ids": [], "text": "invented"}, ["e1"], None])
def test_invalid_model_shape_does_not_retry_other_keys(fake_sdk, result):
    fake_sdk.results = [result]
    with pytest.raises(SelectorUnavailable):
        EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m").select(CONTEXT)
    assert len(fake_sdk.calls) == 1


def test_busy_provider_uses_fallback_without_queueing(fake_sdk):
    entered = threading.Barrier(3)
    release = threading.Event()

    def wait():
        entered.wait(timeout=5)
        assert release.wait(timeout=5)
        return {"ids": ["e1"]}

    fake_sdk.results = [wait, wait]
    selector = EvidenceSelector(["unit-test-key"], "m")
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = [executor.submit(selector.select, CONTEXT) for _ in range(2)]
        entered.wait(timeout=5)
        try:
            with pytest.raises(SelectorUnavailable):
                selector.select(CONTEXT)
        finally:
            release.set()
        assert all(r.result(timeout=5) == ["e1"] for r in results)


def test_failed_attempts_count_toward_same_budget(fake_sdk):
    fake_sdk.results = [UpstreamError(500), UpstreamError(500)]
    selector = EvidenceSelector(["unit-test-key-a", "unit-test-key-b"], "m")
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    for _ in range(18):
        selector.select(CONTEXT)
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 20 and selector._daily_calls == 20


def test_retry_after_http_date_is_honored(fake_sdk, monkeypatch):
    from email.utils import format_datetime
    from services import study_help_provider

    wall = 1700000000.0
    monkeypatch.setattr(study_help_provider.time, "time", lambda: wall)
    header = format_datetime(
        datetime.fromtimestamp(wall + 180, timezone.utc), usegmt=True
    )
    fake_sdk.results = [UpstreamError(503, {"retry-after": header})]
    clock = [100.0]
    selector = EvidenceSelector(
        ["unit-test-key-a", "unit-test-key-b"], "m", clock=lambda: clock[0]
    )
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    clock[0] = 279
    with pytest.raises(SelectorUnavailable):
        selector.select(CONTEXT)
    assert len(fake_sdk.calls) == 1
    clock[0] = 280
    assert selector.select(CONTEXT) == ["e1"]
