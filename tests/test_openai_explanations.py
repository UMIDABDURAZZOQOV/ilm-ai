"""Synthetic transport tests for the OpenAI adapter; never live OpenAI inference."""
import json

import pytest

from services import study_help
from services.openai_explanations import (
    MINIMUM_AGE, OPENAI_URL, OpenAIExplanationProvider, from_reviewed_config,
)
from services.study_help_provider import SelectorUnavailable, load_provider
from tests.test_nvidia_explanations import context, explanation_transport  # noqa: F401

KEY = 'sk-' + 'synthetic-test-only-' * 3
MODEL = 'gpt-4.1-mini'


def config(**change):
    return dict(dict(provider='openai_explanation', model=MODEL, api_key=KEY,
                     audience='students_13_plus',
                     audience_review_reference='synthetic review',
                     data_processing_review_reference='synthetic review'), **change)


@pytest.fixture
def openai_transport(explanation_transport):  # noqa: F811
    explanation_transport.envelope_change = {'model': MODEL + '-2025-04-14'}
    return explanation_transport


@pytest.mark.parametrize('subject', ['biologiya', 'fizika', 'kimyo', 'jahon_tarixi', 'ozbekiston_tarixi'])
@pytest.mark.parametrize('correct', [False, True])
def test_openai_minimized_post_answer_request(openai_transport, subject, correct):
    result = OpenAIExplanationProvider(KEY, model=MODEL).explain(
        dict(context(), subject=subject, is_correct=correct))
    assert result['provider'] == 'openai' and result['is_correct'] is correct
    url, request = openai_transport.calls[0]
    assert url == OPENAI_URL and request['allow_redirects'] is False
    assert request['headers'] == {'Authorization': 'Bearer ' + KEY}
    body = request['json']
    assert body['model'] == MODEL and body['store'] is False
    assert body['response_format'] == {'type': 'json_object'}
    assert 'reasoning_effort' not in body and 'tools' not in body
    assert 'PRIVATE-' not in json.dumps(body)
    assert KEY not in json.dumps(result)
    assert openai_transport.sessions[0].trust_env is False


def test_dated_snapshot_accepted_but_foreign_model_fails_closed(openai_transport):
    provider = OpenAIExplanationProvider(KEY, model=MODEL)
    assert provider.model_matches(MODEL) and provider.model_matches(MODEL + '-2025-04-14')
    assert not provider.model_matches('gpt-4o') and not provider.model_matches(MODEL + '-evil')
    openai_transport.envelope_change = {'model': 'some-other-model'}
    with pytest.raises(SelectorUnavailable):
        provider.explain(context())


@pytest.mark.parametrize('deployment', [{'ENVIRONMENT': 'production'}, {'DEPLOYMENT_STAGE': 'staging'}])
def test_openai_starts_on_hosted_deployments(tmp_path, monkeypatch, deployment):
    path = tmp_path / 'openai.private.json'
    path.write_text(json.dumps(config()), encoding='utf-8')
    assert type(load_provider(path)) is OpenAIExplanationProvider
    monkeypatch.setattr(study_help, '_provider', None)
    study_help.configure_from_environment({**deployment, 'STUDY_HELP_CONFIG_FILE': str(path)})
    assert type(study_help._provider) is OpenAIExplanationProvider
    assert study_help.supports_generation('reviewed-text-v2')


@pytest.mark.parametrize('change', [
    {'model': 'gpt-5'}, {'model': 'gemini-3.1-flash-lite'}, {'api_key': 'AIza' + 'x' * 30},
    {'audience': 'adults_only'}, {'audience': 'all_ages'}, {'audience_review_reference': ''},
    {'extra': 'field'},
])
def test_private_config_rejects_wrong_or_unreviewed_values(change):
    with pytest.raises(ValueError, match='invalid_private_explanation_config'):
        from_reviewed_config(config(**change))


@pytest.mark.parametrize('age,eligible', [(None, False), (11, False), (12, False),
                                          (MINIMUM_AGE, True), (17, True), (35, True)])
def test_teen_age_gate(monkeypatch, age, eligible):
    class User:
        pass
    user = User()
    user.age = age

    class DB:
        def get(self, model, uid):
            return user
    monkeypatch.setattr(study_help, '_provider', OpenAIExplanationProvider(KEY, model=MODEL))
    ctx = {}
    study_help.attach_provider_eligibility(DB(), 1, ctx)
    assert ctx['external_ai_eligible'] is eligible


def test_gemini_still_adult_only(monkeypatch):
    from services.gemini_explanations import GeminiExplanationProvider

    class User:
        age = 17

    class DB:
        def get(self, model, uid):
            return User()
    monkeypatch.setattr(study_help, '_provider', GeminiExplanationProvider('AQ.' + 'x' * 40))
    ctx = {}
    study_help.attach_provider_eligibility(DB(), 1, ctx)
    assert ctx['external_ai_eligible'] is False
