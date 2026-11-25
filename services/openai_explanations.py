"""OpenAI-hosted explanations and subject chat for ILM AI's school audience.

Same reviewed-evidence boundary, grounding validator, subject scope, quota,
deadline and circuit breaker as the Gemini adapter; only the endpoint, model
and audience rule differ. OpenAI's under-18 API guidance permits teen use with
safeguards; under-13 use needs verified guardian consent, which ILM AI does not
yet collect, so under-13 profiles keep the reviewed textbook explanations.
"""
import re

from services.gemini_explanations import GeminiExplanationProvider

OPENAI_URL = 'https://api.openai.com/v1/chat/completions'
# Chat-completions models that accept temperature, max_tokens and JSON mode.
OPENAI_MODELS = frozenset({'gpt-4.1-mini', 'gpt-4o-mini'})
MINIMUM_AGE = 13


class OpenAIExplanationProvider(GeminiExplanationProvider):
    provider_name = 'openai'
    explanation_url = OPENAI_URL
    requires_adult_profile = True  # keep the age gate on; the age is MINIMUM_AGE
    minimum_age = MINIMUM_AGE
    fallback_models = ()  # never fall back to a Google model
    read_timeout_seconds = 12
    # store=False: requests are not kept for OpenAI's stored-completions
    # features. No tools, no web search, JSON-only output.
    request_options = dict(temperature=0.3, max_tokens=2000, stream=False,
                           store=False, response_format={'type': 'json_object'})

    def __init__(self, key, *, model, usage='authorized_hosted_application', **kwargs):
        self.explanation_model = model
        super().__init__(key, usage=usage, **kwargs)

    def model_matches(self, returned, requested=None):
        # OpenAI answers with a dated snapshot, e.g. gpt-4.1-mini-2025-04-14.
        model = requested or self.explanation_model
        return isinstance(returned, str) and (
            returned == model
            or re.fullmatch(re.escape(model) + r'-\d{4}-\d{2}-\d{2}', returned) is not None)


def from_reviewed_config(data):
    fields = {'provider', 'model', 'api_key', 'audience', 'audience_review_reference',
              'data_processing_review_reference'}
    if (set(data) != fields or data.get('provider') != 'openai_explanation'
            or data.get('model') not in OPENAI_MODELS
            or data.get('audience') != 'students_13_plus'
            or not isinstance(data.get('api_key'), str)
            or not re.fullmatch(r'sk-[A-Za-z0-9_-]{20,300}', data['api_key'])):
        raise ValueError('invalid_private_explanation_config')
    for name in ('audience_review_reference', 'data_processing_review_reference'):
        if not isinstance(data[name], str) or not data[name].strip() or len(data[name]) > 500:
            raise ValueError('invalid_private_explanation_config')
    return OpenAIExplanationProvider(data['api_key'], model=data['model'])
