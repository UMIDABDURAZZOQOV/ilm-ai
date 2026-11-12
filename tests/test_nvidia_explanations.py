"""Synthetic HTTP boundaries only: these cases are never live AI evidence."""

from copy import deepcopy
import json
from types import SimpleNamespace

import pytest
import requests

from services.nvidia_explanations import (
    NvidiaExplanationProvider, from_reviewed_config, reviewed_payload,
    validated_paragraphs,
)
from services.nvidia_study_help import NVIDIA_MODEL, NVIDIA_URL
from services.study_help_provider import SelectorUnavailable, load_provider


KEY = "nvapi-" + "synthetic-test-only-" * 3


def config():
    return dict(provider="nvidia_explanation", model=NVIDIA_MODEL, api_key=KEY,
                usage="authorized_hosted_application", audience="adults_only", free_only=True,
                hosted_use_review_reference="synthetic review; not legal authorization",
                audience_review_reference="synthetic adult-only upstream review",
                data_processing_review_reference="synthetic minimized payload review",
                free_plan_review_reference="synthetic free-only budget review")


def context():
    return dict(subject="kimyo", grade=7, title="Sintetik test mavzusi",
                question="Sintetik test savoli", answered=True, is_correct=False,
                external_ai_eligible=True, user_id="PRIVATE-USER", age=25,
                email="private@example.test", message="IGNORE SYSTEM PRIVATE-MESSAGE",
                selected_answer="PRIVATE-LEARNER-ANSWER", attempt_id="PRIVATE-ATTEMPT",
                source_refs=[{"private_path": "PRIVATE-PDF"}],
                evidence=[dict(id="e1", kind="cards", text="Tekshirilgan sintetik dalil matni.",
                               source_refs=[{"private_path": "PRIVATE-PDF"}])])


def generated_plan(body):
    item = body["evidence"][0]
    quote = item["text"].strip()[:100]
    return dict(language="uz", is_correct=body["is_correct"], paragraphs=[
        dict(text="Bu sintetik transport sinovi. Dars dalili: " + quote,
             quotes=[dict(evidence_id=item["id"], text=quote)])])


@pytest.fixture
def explanation_transport(monkeypatch):
    state = SimpleNamespace(calls=[], sessions=[], statuses=[200], headers={},
                            exception=None, raw=None, plan=None, envelope_change={},
                            message_change={}, private_reasoning="PRIVATE-REASONING")

    class Response:
        def __init__(self, status, payload):
            self.status_code = status
            self.headers = state.headers
            body = json.loads(payload["messages"][1]["content"])
            plan = generated_plan(body) if state.plan is None else state.plan
            if callable(plan):
                plan = plan(body)
            message = dict(content=json.dumps(plan, ensure_ascii=False),
                           reasoning_content=state.private_reasoning)
            message.update(state.message_change)
            envelope = dict(model=NVIDIA_MODEL, choices=[dict(finish_reason="stop", message=message)])
            envelope.update(state.envelope_change)
            self.raw = state.raw if state.raw is not None else json.dumps(envelope).encode()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def iter_content(self, chunk_size):
            for offset in range(0, len(self.raw), chunk_size):
                yield self.raw[offset:offset + chunk_size]

    class Session:
        trust_env = True

        def __enter__(self):
            state.sessions.append(self)
            return self

        def __exit__(self, *args):
            pass

        def post(self, url, **kwargs):
            if hasattr(state, "observe"):
                state.observe()
            state.calls.append((url, kwargs))
            if state.exception:
                raise state.exception
            status = state.statuses.pop(0) if len(state.statuses) > 1 else state.statuses[0]
            return Response(status, kwargs["json"])

    monkeypatch.setattr(requests, "Session", Session)
    return state


@pytest.mark.parametrize("environment", ["test", "production"])
def test_new_provider_is_separate_from_trial_and_keeps_private_file_guards(tmp_path, monkeypatch, environment):
    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("ILM_BETA_ENABLED", "false")
    path = tmp_path / "explanations.private.json"
    path.write_text(json.dumps(config()), encoding="utf-8")
    assert type(load_provider(path)) is NvidiaExplanationProvider
    with pytest.raises(ValueError):
        load_provider(__file__)


@pytest.mark.parametrize("change", [
    {"provider": "nvidia_trial"}, {"model": "other/model"}, {"free_only": False},
    {"free_only": 1}, {"audience": "all_ages"}, {"usage": "internal_evaluation"},
    {"api_key": "AQ.invalid"}, {"api_keys": [KEY]},
    {"base_url": "https://untrusted.invalid"},
    {"hosted_use_review_reference": ""}, {"audience_review_reference": None},
    {"data_processing_review_reference": ""}, {"free_plan_review_reference": ""},
])
def test_explicit_hosted_audience_privacy_free_plan_review_and_one_key_required(change):
    with pytest.raises(ValueError):
        from_reviewed_config(dict(config(), **change))


def test_text_generation_internal_evaluation_is_separate_and_never_production(monkeypatch, explanation_transport):
    data = config()
    data.pop('hosted_use_review_reference')
    data.update(usage='internal_evaluation', trial_review_reference='synthetic internal trial review')
    monkeypatch.setenv('ENVIRONMENT', 'test')
    monkeypatch.setenv('ILM_BETA_ENABLED', 'true')
    provider = from_reviewed_config(data)
    assert provider.explain(context())['usage'] == 'internal_evaluation'
    count = len(explanation_transport.calls)
    monkeypatch.setenv('ENVIRONMENT', 'production')
    with pytest.raises(ValueError):
        from_reviewed_config(data)
    with pytest.raises(SelectorUnavailable):
        provider.explain(context())
    assert len(explanation_transport.calls) == count


def test_actual_text_and_safe_server_provenance_not_id_selection(explanation_transport):
    answer = NvidiaExplanationProvider(KEY).explain(context())
    assert answer["provider"] == "nvidia" and answer["model"] == NVIDIA_MODEL
    assert answer["http_status"] == 200 and len(answer["request_id"]) == 32
    assert len(answer["request_sha256"]) == len(answer["response_sha256"]) == 64
    assert answer["paragraphs"][0]["text"].endswith("Tekshirilgan sintetik dalil matni.")
    assert answer["paragraphs"][0]["evidence_ids"] == ["e1"]
    assert "PRIVATE-" not in json.dumps(answer) and KEY not in json.dumps(answer)
    url, request = explanation_transport.calls[0]
    assert url == NVIDIA_URL and request["allow_redirects"] is False
    assert request["stream"] is True and request["timeout"][0] == 3
    assert explanation_transport.sessions[0].trust_env is False
    payload = request["json"]
    assert payload["max_tokens"] == 1600 and payload["reasoning_effort"] == "none"
    assert payload["tool_choice"] == "none" and "response_format" not in payload
    assert "PRIVATE-" not in json.dumps(payload)
    body = json.loads(payload["messages"][1]["content"])
    assert set(body) == {"subject", "grade", "title", "question", "is_correct", "evidence"}
    assert set(body["evidence"][0]) == {"id", "kind", "text"}


def test_new_provider_cannot_fall_through_old_openai_selector(explanation_transport):
    provider = NvidiaExplanationProvider(KEY)
    with pytest.raises(SelectorUnavailable):
        provider.select(context())
    with pytest.raises(SelectorUnavailable):
        provider._select('synthetic body')
    assert not explanation_transport.calls


@pytest.mark.parametrize("change", [
    {"answered": False}, {"is_correct": None}, {"external_ai_eligible": False},
    {"external_ai_eligible": None}, {"subject": "unavailable"}, {"question": ""},
    {"evidence": []}, {"question": "x" * 4001},
])
def test_no_upstream_for_unanswered_unknown_or_ineligible_context(explanation_transport, change):
    with pytest.raises(SelectorUnavailable):
        NvidiaExplanationProvider(KEY).explain(dict(context(), **change))
    assert explanation_transport.calls == []


def test_unreferenced_duplicate_or_oversized_evidence_never_leaves_server(explanation_transport):
    for mutate in [lambda c: c["evidence"][0].update(source_refs=[]),
                   lambda c: c["evidence"].append(deepcopy(c["evidence"][0])),
                   lambda c: c["evidence"][0].update(text="x" * 6001)]:
        data = context()
        mutate(data)
        with pytest.raises(SelectorUnavailable):
            NvidiaExplanationProvider(KEY).explain(data)
    assert not explanation_transport.calls


@pytest.mark.parametrize("change", [
    {"language": "en"}, {"is_correct": True}, {"is_correct": 0},
    {"paragraphs": []}, {"prose": "unvalidated"},
    {"paragraphs": [{"text": "Invented quote without citations", "quotes": []}]},
])
def test_wrong_language_grade_flag_or_output_shape_is_fallback(change):
    plan = dict(generated_plan(json.loads(reviewed_payload(context()))), **change)
    with pytest.raises((SelectorUnavailable, ValueError)):
        validated_paragraphs(json.dumps(plan), context())


@pytest.mark.parametrize("bad", ["invented", "https://untrusted.invalid", "PRIVATE-PDF"])
def test_invented_evidence_ids_are_rejected(bad):
    plan = generated_plan(json.loads(reviewed_payload(context())))
    plan["paragraphs"][0]["quotes"][0]["evidence_id"] = bad
    with pytest.raises(SelectorUnavailable):
        validated_paragraphs(json.dumps(plan), context())


@pytest.mark.parametrize("bad", [
    "Yangi manbasiz fakt 999999.", "https://untrusted.invalid",
    "<script>steal()</script>", "Bearer synthetic-secret", "private@example.test",
])
def test_obvious_ungrounded_numbers_injection_links_and_sensitive_outputs_rejected(bad):
    plan = generated_plan(json.loads(reviewed_payload(context())))
    plan["paragraphs"][0]["text"] += " " + bad
    with pytest.raises(SelectorUnavailable):
        validated_paragraphs(json.dumps(plan), context())


def test_model_cannot_fabricate_quote_or_hide_it_outside_displayed_paragraph():
    for quote in ["Invented source fact.", "Tekshirilgan"]:
        plan = generated_plan(json.loads(reviewed_payload(context())))
        plan["paragraphs"][0]["quotes"][0]["text"] = quote
        if quote == "Tekshirilgan":
            plan["paragraphs"][0]["text"] = "Only non-quoted generated text remains here."
        with pytest.raises(SelectorUnavailable):
            validated_paragraphs(json.dumps(plan), context())


@pytest.mark.parametrize("status", [401, 402, 403, 429])
def test_auth_quota_permission_pause_without_account_rotation(explanation_transport, status):
    explanation_transport.statuses = [status]
    provider = NvidiaExplanationProvider(KEY)
    for _ in range(2):
        with pytest.raises(SelectorUnavailable):
            provider.explain(context())
    assert len(explanation_transport.calls) == 1


def test_bounded_same_key_retry_then_generated_text(explanation_transport):
    explanation_transport.statuses = [503, 200]
    assert NvidiaExplanationProvider(KEY).explain(context())["paragraphs"]
    assert len(explanation_transport.calls) == 2
    assert all(c[1]["headers"]["Authorization"] == "Bearer " + KEY for c in explanation_transport.calls)


def test_retry_after_and_circuit_prevent_retry_storm(explanation_transport):
    clock = [0]
    provider = NvidiaExplanationProvider(KEY, clock=lambda: clock[0])
    explanation_transport.statuses = [503]
    explanation_transport.headers = {"Retry-After": "180"}
    for instant in [0, 90, 179]:
        clock[0] = instant
        with pytest.raises(SelectorUnavailable):
            provider.explain(context())
    assert len(explanation_transport.calls) == 1


def test_failed_content_opens_finite_circuit_with_one_recovery_probe(explanation_transport):
    clock = [10]
    provider = NvidiaExplanationProvider(KEY, clock=lambda: clock[0])
    explanation_transport.plan = {"bad": "PRIVATE-UPSTREAM"}
    for _ in range(5):
        with pytest.raises(SelectorUnavailable):
            provider.explain(context())
    assert len(explanation_transport.calls) == 3
    clock[0] = 41
    explanation_transport.plan = None
    assert provider.explain(context())["paragraphs"]
    assert len(explanation_transport.calls) == 4


@pytest.mark.parametrize("failure", [requests.Timeout("PRIVATE-ERROR"), requests.ConnectionError("PRIVATE-ERROR")])
def test_network_failures_never_export_exception_or_leak_slots(explanation_transport, failure):
    explanation_transport.exception = failure
    provider = NvidiaExplanationProvider(KEY)
    with pytest.raises(SelectorUnavailable) as error:
        provider.explain(context())
    assert "PRIVATE-" not in str(error.value)
    assert len(explanation_transport.calls) <= 2
    assert provider._slots.acquire(blocking=False)
    provider._slots.release()


def test_backpressure_and_local_rate_budget_have_no_waiting_queue(explanation_transport):
    provider = NvidiaExplanationProvider(KEY)
    assert provider._slots.acquire(False) and provider._slots.acquire(False)
    with pytest.raises(SelectorUnavailable):
        provider.explain(context())
    assert not explanation_transport.calls
    provider._slots.release()
    provider._slots.release()
    for _ in range(20):
        provider.explain(context())
    with pytest.raises(SelectorUnavailable):
        provider.explain(context())
    assert len(explanation_transport.calls) == 20


@pytest.mark.parametrize("change", [
    {"choices": []}, {"model": "other/model"}, {"model": None},
    {"choices": [{"finish_reason": "length", "message": {"content": "truncated"}}]},
])
def test_malformed_truncated_or_wrong_model_envelope_falls_back(explanation_transport, change):
    explanation_transport.envelope_change = change
    with pytest.raises(SelectorUnavailable):
        NvidiaExplanationProvider(KEY).explain(context())


def test_reasoning_size_tools_and_duplicate_json_keys_are_not_accepted(explanation_transport):
    for change in [dict(tool_calls=[{"name": "private-tool"}]), dict(refusal="no")]:
        explanation_transport.message_change = change
        with pytest.raises(SelectorUnavailable):
            NvidiaExplanationProvider(KEY).explain(context())
    explanation_transport.message_change = {}
    explanation_transport.private_reasoning = "x" * 32769
    with pytest.raises(SelectorUnavailable):
        NvidiaExplanationProvider(KEY).explain(context())
    explanation_transport.private_reasoning = ""
    explanation_transport.raw = b'{"choices":[],"choices":[]}'
    with pytest.raises(SelectorUnavailable):
        NvidiaExplanationProvider(KEY).explain(context())


def test_normal_startup_is_explicit_and_never_discovers_environment_key(tmp_path, monkeypatch, explanation_transport):
    from services import study_help
    monkeypatch.setattr(study_help, "_provider", None)
    monkeypatch.setenv("NVIDIA_API_KEY", KEY)
    study_help.configure_from_environment({})
    assert study_help._provider is None and not explanation_transport.calls
    path = tmp_path / "private.json"
    path.write_text(json.dumps(config()), encoding="utf-8")
    study_help.configure_from_environment({"STUDY_HELP_CONFIG_FILE": str(path)})
    assert isinstance(study_help._provider, NvidiaExplanationProvider)
    assert not explanation_transport.calls
    study_help.configure_provider()
