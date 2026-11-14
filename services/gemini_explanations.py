"""Google-hosted Gemini explanations with the shared reviewed-evidence boundary.

This is separate from the legacy services.gemini OpenAI compatibility wrapper.
No key pool, automatic billing activation, or production opt-in is implicit.
"""
import re

from services.nvidia_explanations import NvidiaExplanationProvider


GEMINI_MODEL = 'gemini-3.1-flash-lite'
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions'


class GeminiExplanationProvider(NvidiaExplanationProvider):
    """Reuse transport deadlines, admission and grounding; pin Google's endpoint."""

    provider_name = 'gemini'
    explanation_model = GEMINI_MODEL
    explanation_url = GEMINI_URL
    capabilities = frozenset({'reviewed-text-v2'})
    read_timeout_seconds = 12
    system_suffix = (
        " JSON talabi: quotes[].text dagi HAR BIR iqtibos aynan o'sha paragrafning "
        "text satrida ham so'zma-so'z, tinish belgilari va harf kattaligigacha "
        "bir xil bo'lishi SHART. Faqat mazmunini qayta aytish yetarli emas. "
        "Avval qisqa izoh, so'ng text ichida aynan iqtibosni yozing. "
        "quotes alohida ro'yxati text ichidagi iqtibosning o'rnini bosmaydi. "
        "Javobni yuborishdan avval har bir quotes[].text text ichida borligini tekshiring."
    )
    # Gemini 3.1 does not support reasoning_effort=none. No tools/search enabled.
    request_options = dict(reasoning_effort='minimal', max_tokens=2000,
                           stream=False, response_format={'type': 'json_object'})


def from_reviewed_config(data):
    usage = data.get('usage')
    review_field = ('trial_review_reference' if usage == 'internal_evaluation'
                    else 'hosted_use_review_reference')
    fields = {'provider', 'model', 'api_key', 'usage', 'audience', 'free_only',
              review_field, 'audience_review_reference',
              'data_processing_review_reference', 'free_plan_review_reference'}
    if (set(data) != fields or data.get('provider') != 'gemini_explanation'
            or data.get('model') != GEMINI_MODEL
            or usage not in {'internal_evaluation', 'authorized_hosted_application'}
            or data.get('audience') != 'adults_only' or data.get('free_only') is not True
            or not isinstance(data.get('api_key'), str)
            # Both standard and authorization keys exist. Syntax is not proof
            # of validity, free-tier eligibility or audience authorization.
            or not re.fullmatch(r'(?:AIza|AQ\.)[A-Za-z0-9_.-]{16,500}', data['api_key'])):
        raise ValueError('invalid_private_explanation_config')
    if usage == 'internal_evaluation':
        from services.nvidia_study_help import trial_allowed
        if not trial_allowed():
            raise ValueError('internal_explanation_evaluation_only')
    for name in fields:
        if name.endswith('_reference') and (
                not isinstance(data[name], str) or not data[name].strip()
                or len(data[name]) > 500):
            raise ValueError('invalid_private_explanation_config')
    return GeminiExplanationProvider(data['api_key'], usage=usage)
