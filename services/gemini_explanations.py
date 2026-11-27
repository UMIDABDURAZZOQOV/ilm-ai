"""Google-hosted Gemini explanations with the shared reviewed-evidence boundary.

This is separate from the legacy services.gemini OpenAI compatibility wrapper.
No key pool, automatic billing activation, or production opt-in is implicit.
"""
import re

from services.nvidia_explanations import NvidiaExplanationProvider


GEMINI_MODEL = 'gemini-3.1-flash-lite'
GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions'
OWNER_ACCEPTED_AUDIENCE = 'owner_accepted_mixed_audience'
AUDIENCES = frozenset({'adults_only', OWNER_ACCEPTED_AUDIENCE})


class GeminiExplanationProvider(NvidiaExplanationProvider):
    """Reuse transport deadlines, admission and grounding; pin Google's endpoint."""

    provider_name = 'gemini'
    explanation_model = GEMINI_MODEL
    # gemini-3.1-flash-lite intermittently answers 503 "high demand". Retry
    # the SAME model after a short pause: the released 1.0.3 app accepts only
    # gemini-3.1-flash-lite answers, so a different fallback model's reply was
    # always shown to learners as "No answer arrived".
    fallback_models = (GEMINI_MODEL,)
    busy_retry_delay = 1.5
    explanation_url = GEMINI_URL
    capabilities = frozenset({'reviewed-text-v2'})
    read_timeout_seconds = 12
    system_suffix = (
        " JSON talabi: quotes[].text dagi HAR BIR iqtibos aynan o'sha paragrafning "
        "text satrida ham so'zma-so'z, tinish belgilari va harf kattaligigacha "
        "bir xil bo'lishi SHART. Faqat mazmunini qayta aytish yetarli emas. "
        "Avval qisqa izoh, so'ng text ichida aynan iqtibosni yozing. "
        "quotes alohida ro'yxati text ichidagi iqtibosning o'rnini bosmaydi. "
        "Javobni yuborishdan avval har bir quotes[].text text ichida borligini tekshiring. "
        "EXCEPTION: subject-chat allows {{quote:0}} placeholders explicitly. "
        "For subject-chat prefer those placeholders instead of duplicating quote text."
    )
    # Gemini 3.1 does not support reasoning_effort=none. No tools/search enabled.
    request_options = dict(reasoning_effort='minimal', max_tokens=2000,
                           stream=False, response_format={'type': 'json_object'})

    def chat(self, context):
        # The same instance owns admission, quota and circuit state for chat
        # and explanations. Chat is never a second budget or a key pool.
        return self.explain(dict(context, mode='subject_chat'))

    def generation_options(self, context):
        if context.get('mode') == 'subject_chat':
            # Short conversational turns leave time for a bounded format repair.
            # Truncated output still fails closed; no deadline is extended.
            return dict(self.request_options, max_tokens=1200)
        return super().generation_options(context)

    def prepare_payload(self, context):
        if context.get('mode') == 'subject_chat':
            from services.subject_tutor import provider_payload
            return provider_payload(context)
        return super().prepare_payload(context)

    def system_prompt(self, context):
        if context.get('mode') == 'subject_chat':
            from services.subject_tutor import SYSTEM_PROMPT
            return SYSTEM_PROMPT + (
                '\nPrefer explicit {{quote:0}} slots. Each evidence includes exact '
                'quote_options. Prefer quotes:[{"evidence_id":"e1","quote_id":"q1"}] '
                'using an option from that SAME evidence instead of copying text. '
                'The server resolves only known options and validates the entire answer. '
                'Do not repeat the selected quote after its slot. If no option fits, '
                'the original exact quotes[].text format remains available.'
            )
        return super().system_prompt(context)

    def validate_content(self, raw, context):
        if context.get('mode') == 'subject_chat':
            from services.subject_tutor import validate_reply
            return validate_reply(raw, context)
        return super().validate_content(raw, context)

    def format_retry_instruction(self, raw, context):
        if context.get('mode') == 'subject_chat':
            from services.subject_tutor import grounding_reason
            reason = grounding_reason(raw, context)
            if reason in {'quote_typography', 'quote_not_in_source', 'quote_not_in_paragraph'}:
                return (
                    '\nQUOTE CORRECTION: Generate a fresh answer. For each paragraph, '
                    'use a real evidence_id and a quote_id from that same evidence '
                    'item’s quote_options. Return only those two keys in each quote '
                    'object. Include the matching {{quote:0}} placeholder in '
                    'paragraph.text and let the server insert the exact source text. '
                    'All evidence and numeric validation still applies.'
                )
            if reason == 'unsupported_numbers':
                return (
                    '\nGROUNDING CORRECTION: Your answer contained a number absent '
                    'from its cited evidence. Generate a fresh answer using only '
                    'facts and quantities in the cited evidence. Do not number '
                    'paragraphs or invent numeric examples. Do not merely remove '
                    'digits from an unsupported claim. All validation still applies.'
                )
        return None

    def content_fields(self, content, context):
        if context.get('mode') == 'subject_chat':
            return dict(language='uz', status=content['status'],
                        grounding='citations_and_quotes_checked_not_semantic_verification',
                        paragraphs=content['paragraphs'])
        return super().content_fields(content, context)


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
            or data.get('audience') not in AUDIENCES or data.get('free_only') is not True
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
    provider = GeminiExplanationProvider(data['api_key'], usage=usage)
    if data['audience'] == OWNER_ACCEPTED_AUDIENCE:
        if usage != 'authorized_hosted_application':
            raise ValueError('invalid_private_explanation_config')
        # The owner explicitly accepted Google's audience terms risk for the
        # school app (2026-11-25). Any learner with a recorded age may use the
        # source-bound tutor; grounding, subject scope and quotas are unchanged.
        provider.minimum_age = 1
        provider.owner_accepted_mixed_audience = True
    return provider
