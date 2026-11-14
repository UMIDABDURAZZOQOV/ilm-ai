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
    assert request['timeout'][1] <= 12
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
