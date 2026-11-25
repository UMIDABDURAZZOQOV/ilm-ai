"""Synthetic transport tests, never evidence of live Google inference."""
import json

import pytest
import requests

from services import study_help
from services.gemini_explanations import (
    GEMINI_MODEL, GEMINI_URL, GeminiExplanationProvider, from_reviewed_config,
)
from services.study_help_provider import SelectorUnavailable, load_provider
from tests.test_nvidia_explanations import context, explanation_transport  # noqa: F401

KEY = 'AQ.' + 'synthetic-test-only-' * 3


def config():
    return dict(provider='gemini_explanation', model=GEMINI_MODEL, api_key=KEY,
                usage='authorized_hosted_application', audience='adults_only', free_only=True,
                hosted_use_review_reference='synthetic review, not real authorization',
                audience_review_reference='synthetic review',
                data_processing_review_reference='synthetic review',
                free_plan_review_reference='synthetic review')


@pytest.fixture
def google_transport(explanation_transport):  # noqa: F811
    explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    return explanation_transport


@pytest.mark.parametrize('subject', ['biologiya', 'fizika', 'kimyo', 'jahon_tarixi', 'ozbekiston_tarixi'])
@pytest.mark.parametrize('correct', [False, True])
def test_google_only_minimized_post_answer_request(google_transport, subject, correct):
    result = GeminiExplanationProvider(KEY).explain(dict(context(), subject=subject, is_correct=correct))
    assert result['provider'] == 'gemini' and result['model'] == GEMINI_MODEL
    assert result['http_status'] == 200 and result['is_correct'] is correct
    url, request = google_transport.calls[0]
    assert url == GEMINI_URL and request['allow_redirects'] is False
    assert request['headers'] == {'Authorization': 'Bearer ' + KEY}
    assert request['json']['reasoning_effort'] == 'minimal'
    assert request['json']['response_format'] == {'type': 'json_object'}
    assert request['json']['max_tokens'] == 2000
    assert request['timeout'][1] <= 12
    assert request['timeout'][1] <= 8
    assert 'quotes[].text' in request['json']['messages'][0]['content']
    assert 'tools' not in request['json']
    assert 'PRIVATE-' not in json.dumps(request['json'])
    assert KEY not in json.dumps(result)
    assert google_transport.sessions[0].trust_env is False


@pytest.mark.parametrize('key', [KEY, 'AIza' + 'synthetic-test-only-' * 3])
def test_private_config_supports_google_key_types_and_normal_startup(tmp_path, monkeypatch, key):
    path = tmp_path / 'gemini.private.json'
    path.write_text(json.dumps(dict(config(), api_key=key)), encoding='utf-8')
    assert type(load_provider(path)) is GeminiExplanationProvider
    monkeypatch.setattr(study_help, '_provider', None)
    study_help.configure_from_environment({'STUDY_HELP_CONFIG_FILE': str(path)})
    assert type(study_help._provider) is GeminiExplanationProvider
    assert study_help.supports_generation('reviewed-text-v2')
    assert not study_help.supports_generation('nvidia-text-v1')
    assert not study_help.supports_generation(None)


@pytest.mark.parametrize('deployment', [
    {'ENVIRONMENT': 'production'},
    {'DEPLOYMENT_STAGE': 'staging'},
])
def test_hosted_mixed_audience_disables_gemini_and_keeps_reviewed_feedback(
    tmp_path, monkeypatch, deployment, google_transport,
):
    from services.study_help import HelpRequest

    path = tmp_path / 'gemini.private.json'
    path.write_text(json.dumps(config()), encoding='utf-8')
    monkeypatch.setattr(study_help, '_provider', None)
    with pytest.raises(ValueError, match='gemini_not_available_for_hosted_mixed_audience_app'):
        study_help.configure_from_environment({**deployment, 'STUDY_HELP_CONFIG_FILE': str(path)})

    assert study_help._provider is None
    data = HelpRequest(subject='kimyo', grade=7, attempt_id='attempt', question_key='question')
    evidence = context()['evidence']
    response = study_help.respond(
        dict(source_refs=evidence[0]['source_refs'], evidence=evidence, is_correct=True),
        data,
        allow_generation=True,
    )
    assert response['mode'] == 'reviewed_evidence'
    assert response['provider_status'] == 'unconfigured'
    assert response['is_correct'] is True
    assert not google_transport.calls


@pytest.mark.parametrize('change', [
    {'base_url': 'https://untrusted.invalid'}, {'api_keys': [KEY]},
    {'api_key': 'nvapi-not-a-google-key'}, {'model': 'other-model'},
    {'free_only': False}, {'free_only': 1}, {'audience': 'all_ages'},
    {'usage': 'unknown'}, {'audience_review_reference': ''},
])
def test_private_config_rejects_wrong_destination_or_unreviewed_options(change):
    with pytest.raises(ValueError):
        from_reviewed_config(dict(config(), **change))


@pytest.mark.parametrize('status', [401, 402, 403, 429])
def test_auth_or_quota_failure_stops_without_rotation(google_transport, status):
    google_transport.statuses = [status]
    provider = GeminiExplanationProvider(KEY)
    for _ in range(2):
        with pytest.raises(SelectorUnavailable):
            provider.explain(context())
    assert len(google_transport.calls) == 1


@pytest.mark.parametrize('change', [{'answered': False}, {'external_ai_eligible': False}, {'external_ai_eligible': None}])
def test_unchecked_or_ineligible_questions_never_go_upstream(google_transport, change):
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider(KEY).explain(dict(context(), **change))
    assert not google_transport.calls


def test_timeout_and_non_google_model_fail_closed(google_transport):
    google_transport.exception = requests.Timeout('synthetic confidential detail')
    with pytest.raises(SelectorUnavailable) as error:
        GeminiExplanationProvider(KEY).explain(context())
    assert not str(error.value)
    google_transport.exception = None
    google_transport.envelope_change = {'model': 'other-model'}
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider(KEY).explain(context())


def test_paraphrased_quote_without_literal_text_still_fails(google_transport):
    # Actual live-probe failure shape. Keep the strict evidence check rather than
    # accepting prose which silently omits its purported supporting quote.
    google_transport.plan = dict(language='uz', is_correct=False, paragraphs=[dict(
        text='Bu yerda model dalilni faqat qayta ifodalagan.',
        quotes=[dict(evidence_id='e1', text=context()['evidence'][0]['text'])])])
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider(KEY).explain(context())


def test_evaluation_cannot_follow_environment_into_production(monkeypatch, google_transport):
    data = config()
    data.pop('hosted_use_review_reference')
    data.update(usage='internal_evaluation', trial_review_reference='synthetic internal test')
    monkeypatch.setenv('ENVIRONMENT', 'test')
    monkeypatch.setenv('ILM_BETA_ENABLED', 'true')
    provider = from_reviewed_config(data)
    assert provider.explain(context())['usage'] == 'internal_evaluation'
    monkeypatch.setenv('ENVIRONMENT', 'production')
    with pytest.raises(SelectorUnavailable):
        provider.explain(context())
    with pytest.raises(ValueError):
        from_reviewed_config(data)
    assert len(google_transport.calls) == 1


def test_failure_diagnostics_never_log_provider_body_or_credential(google_transport, caplog):
    google_transport.statuses=[403]
    google_transport.raw=json.dumps({'error':{'message':KEY+' PRIVATE-DETAIL'}}).encode()
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider(KEY).explain(context())
    assert 'provider=gemini status=403' in caplog.text
    assert KEY not in caplog.text and 'PRIVATE-' not in caplog.text


def test_transient_timeout_recovers_once_on_same_key(google_transport):
    attempts = []
    def transient():
        attempts.append(1)
        google_transport.exception = requests.Timeout('synthetic') if len(attempts) == 1 else None
    google_transport.observe = transient
    # The recovered second attempt is served by the fallback model.
    google_transport.envelope_change = {'model': 'gemini-2.5-flash'}
    assert GeminiExplanationProvider(KEY).explain(context())['http_status'] == 200
    assert len(google_transport.calls) == 2
    assert all(call[1]['headers']['Authorization'] == 'Bearer ' + KEY for call in google_transport.calls)


def test_timeout_does_not_retry_without_remaining_budget(google_transport, monkeypatch):
    from services import nvidia_explanations
    clock = [100.0]
    monkeypatch.setattr(nvidia_explanations.time, 'monotonic', lambda: clock[0])
    def expired():
        clock[0] = 114.0
        google_transport.exception = requests.Timeout('synthetic')
    google_transport.observe = expired
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider(KEY).explain(context())
    assert len(google_transport.calls) == 1


def test_retry_connect_and_read_fit_remaining_deadline(google_transport, monkeypatch):
    from services import nvidia_explanations
    clock = [100.0]
    monkeypatch.setattr(nvidia_explanations.time, 'monotonic', lambda: clock[0])
    google_transport.statuses = [503, 200]
    google_transport.observe = lambda: clock.__setitem__(0, 113.0)
    google_transport.envelope_change = {'model': 'gemini-2.5-flash'}
    assert GeminiExplanationProvider(KEY).explain(context())['http_status'] == 200
    connect, read = google_transport.calls[1][1]['timeout']
    assert connect > 0 and read > 0 and connect + read <= 3


def owner_accepted_config():
    data = dict(config(), audience='owner_accepted_mixed_audience')
    return data


@pytest.mark.parametrize('deployment', [{'ENVIRONMENT': 'production'}, {'DEPLOYMENT_STAGE': 'staging'}])
def test_owner_accepted_audience_runs_hosted_for_all_recorded_ages(tmp_path, monkeypatch, deployment):
    path = tmp_path / 'gemini.private.json'
    path.write_text(json.dumps(owner_accepted_config()), encoding='utf-8')
    monkeypatch.setattr(study_help, '_provider', None)
    study_help.configure_from_environment({**deployment, 'STUDY_HELP_CONFIG_FILE': str(path)})
    assert type(study_help._provider) is GeminiExplanationProvider

    class User:
        age = 11

    class DB:
        def get(self, model, uid):
            return User()
    ctx = {}
    study_help.attach_provider_eligibility(DB(), 1, ctx)
    assert ctx['external_ai_eligible'] is True
    User.age = None
    ctx = {}
    study_help.attach_provider_eligibility(DB(), 1, ctx)
    assert ctx['external_ai_eligible'] is False


def test_owner_accepted_audience_requires_hosted_usage():
    data = dict(owner_accepted_config(), usage='internal_evaluation')
    data['trial_review_reference'] = data.pop('hosted_use_review_reference')
    with pytest.raises(ValueError):
        from_reviewed_config(data)


def test_second_attempt_uses_fallback_model_after_high_demand(google_transport):
    google_transport.statuses = [503, 200]
    google_transport.envelope_change = {'model': 'gemini-2.5-flash'}
    result = GeminiExplanationProvider(KEY).explain(dict(context(), subject='kimyo', is_correct=False))
    assert [call[1]['json']['model'] for call in google_transport.calls] == [GEMINI_MODEL, 'gemini-2.5-flash']
    assert result['model'] == 'gemini-2.5-flash'
    assert google_transport.calls[1][1]['json']['reasoning_effort'] == 'none'
    assert google_transport.calls[0][1]['json']['reasoning_effort'] == 'minimal'


def test_busy_primary_with_retry_after_still_tries_fallback(google_transport):
    google_transport.statuses = [503, 200]
    google_transport.headers = {'Retry-After': '30'}
    google_transport.envelope_change = {'model': 'gemini-2.5-flash'}
    provider = GeminiExplanationProvider(KEY)
    assert provider.explain(dict(context(), subject='kimyo', is_correct=True))['model'] == 'gemini-2.5-flash'
    assert provider._paused_until == 0 or provider._paused_until <= provider._clock()
