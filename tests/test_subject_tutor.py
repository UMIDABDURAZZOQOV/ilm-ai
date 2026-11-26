"""Conversation boundaries; synthetic transport, not live AI acceptance."""
import json
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from services import subject_tutor as tutor, study_help
from services.gemini_explanations import GeminiExplanationProvider, GEMINI_MODEL
from services.study_help_provider import SelectorUnavailable
from tests.test_nvidia_explanations import explanation_transport  # noqa: F401


def request(**changes):
    return tutor.ChatRequest(**dict(dict(subject='kimyo', grade=7,
        conversation_id=str(uuid4()), request_id=str(uuid4()), message='Modda nima?'), **changes))


def context():
    return dict(subject='kimyo', grade=7, message='Modda nima?', question='Modda nima?',
                history=[], external_ai_eligible=True, evidence=[dict(id='e1',
                title='Test', text='Moddalar turli xossalarga ega.', source_refs=[{'page':1}])])


@pytest.mark.parametrize('message', ['Ilk o‘rta asrlarda dehqonlar kim bo‘lgan?',
                                    'Ilk orta asrlarda dehqonlar kim bolgan?'])
def test_history_definition_is_not_drowned_by_repeated_chapter_titles(monkeypatch, message):
    directory = Path(__file__).resolve().parents[1] / 'scripts/curriculum/uzbekistan_history'
    documents = [json.loads(source.read_text(encoding='utf-8'))
                 for source in directory.glob('grade*_batch*.json')
                 if 'review' not in source.name]
    chunks = []
    for document, lesson in ((d, l) for d in documents for l in d.get('lessons', [])):
        for section in ('cards', 'formulas', 'examples', 'reflections'):
            for card in lesson.get(section, []):
                text = '\n'.join(str(card[k]) for k in ('title', 'expression', 'body') if card.get(k))
                if text:
                    chunks.append(dict(text=text, title=lesson['title'], grade=document['grade'],
                        lesson_key=lesson['key'], source_refs=card.get('source_refs') or lesson['source_refs']))
    monkeypatch.setattr(tutor, 'teaching_chunks', lambda db, subject: iter(chunks))
    monkeypatch.setattr(study_help, 'attach_provider_eligibility', lambda *args: None)
    data = request(subject='ozbekiston_tarixi', message=message)
    row, _ = tutor.begin(1, data)
    result = tutor.retrieve(None, 1, data, row)
    assert any('dehqon — yer mulkiga ega' in e['text'] for e in result['evidence'])
    assert len(result['evidence']) <= 8
    assert sum(len(e['text'].encode('utf-8')) for e in result['evidence']) <= 12000
    assert all(e['source_refs'] for e in result['evidence'])


def plan(body):
    quote = body['evidence'][0]['text']
    return dict(status='answered', paragraphs=[dict(text='Sodda qilib aytganda: '+quote,
        quotes=[dict(evidence_id='e1', text=quote)])])


@pytest.fixture(autouse=True)
def isolated():
    tutor._conversations.clear()
    yield
    tutor._conversations.clear()


def test_actual_message_history_not_identity_are_sent(explanation_transport):  # noqa: F811
    explanation_transport.envelope_change = {'model':GEMINI_MODEL}
    explanation_transport.plan = plan
    data = dict(context(), message='Boshqacha tushuntir',
                history=[{'role':'user','text':'Modda nima?'}], email='PRIVATE-USER')
    result = GeminiExplanationProvider('synthetic-key').chat(data)
    payload = json.loads(explanation_transport.calls[0][1]['json']['messages'][1]['content'])
    assert payload['message'] == data['message'] and payload['history'] == data['history']
    assert 'PRIVATE-USER' not in json.dumps(payload)
    assert result['status'] == 'answered' and result['provider'] == 'gemini'
    assert 'is_correct' not in result
    assert explanation_transport.calls[0][1]['json']['max_tokens'] == 1200


@pytest.mark.parametrize('status', ['off_topic','clarify','insufficient_evidence'])
def test_nonanswer_has_no_invented_paragraphs(status):
    assert tutor.validate_reply(json.dumps(dict(status=status,paragraphs=[])),context())['status']==status
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(dict(status=status,paragraphs=[{'text':'Invented'}])),context())


def test_cross_subject_citation_rejected():
    reply=plan(context())
    reply['paragraphs'][0]['quotes'][0]['evidence_id']='other-subject'
    with pytest.raises(SelectorUnavailable): tutor.validate_reply(json.dumps(reply),context())


def test_invalid_quote_slot_reports_grounding_cause_not_generic_shape():
    reply = {'status': 'answered', 'paragraphs': [
        {'text': '{{quote:0}} Bu tushunchani tushuntiramiz.',
         'quotes': [{'evidence_id': 'e1', 'text': 'Unreviewed quote'}]}]}
    assert tutor.grounding_reason(json.dumps(reply), context()) == 'quote_not_in_source'
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(reply), context())


def test_owner_scope_busy_and_retry(monkeypatch):
    data=request()
    row,_=tutor.begin(1,data)
    for uid, changed, code in [(2,{},404),(1,{'subject':'fizika'},409),(1,{},409)]:
        with pytest.raises(HTTPException) as error:
            tutor.begin(uid,data.model_copy(update=changed))
        assert error.value.status_code==code
    class Provider:
        calls=0
        def chat(self, ctx):
            self.calls+=1
            return {'status':'answered','paragraphs':[{'text':'Moddalar turli xossalarga ega.'}]}
    provider=Provider()
    monkeypatch.setattr(study_help,'_provider',provider)
    reply=tutor.respond(row,data,context())
    assert tutor.begin(1,data)[1] == reply and provider.calls==1
    assert row.history[0]['text']==data.message and not row.busy
    with pytest.raises(HTTPException): tutor.begin(1,data.model_copy(update={'message':'Yangi savol'}))


def test_unconfigured_not_fabricated_or_audience_error(monkeypatch):
    monkeypatch.setattr(study_help,'_provider',None)
    data=request(); row,_=tutor.begin(1,data)
    result=tutor.respond(row,data,context())
    assert result['status']=='unavailable' and not result['paragraphs']
    assert not row.history and not row.busy
    assert tutor.begin(1,data)[1] is None


def test_age_restriction_never_calls_provider(monkeypatch):
    class Provider:
        def chat(self, ctx): pytest.fail('ineligible upstream request')
    monkeypatch.setattr(study_help,'_provider',Provider())
    data=request();row,_=tutor.begin(1,data)
    assert tutor.respond(row,data,dict(context(),external_ai_eligible=False))['status']=='audience_unavailable'


def test_bounded_per_owner_and_no_cross_owner_eviction():
    first=request();row,_=tutor.begin(2,first);tutor.release(row)
    for _ in range(8):
        row,_=tutor.begin(1,request());tutor.release(row)
    assert len(tutor._conversations)==5 and first.conversation_id in tutor._conversations


@pytest.mark.parametrize('change', [{'subject':'other'},{'grade':4},{'message':' '},
    {'conversation_id':'-'*36},{'request_id':'not-uuid'},{'message':'x'*1501}])
def test_invalid_request(change):
    with pytest.raises(ValidationError): request(**change)


def test_sensitive_input_redacted():
    result=tutor.sanitized('Mening test@example.com, AQ.'+'a'*30+' va modda savolim')
    assert 'test@example.com' not in result and 'AQ.' not in result and 'modda' in result


@pytest.mark.parametrize('prefix', ['ilm1_', 'ilmr1_', 'rnd_', 'napi_'])
def test_chat_does_not_forward_pasted_keys_in_messages_or_history(prefix):
    example = prefix + 'A' * 43
    question = f'Modda nima? ({example})'
    data = context()
    data.update(message=question, history=[{'role': 'assistant', 'text': question},
                                          {'role': 'user', 'text': 'NaCl formulasi to‘g‘rimi?'}])
    payload = json.loads(tutor.provider_payload(data))
    assert example not in json.dumps(payload)
    assert payload['message'] == payload['history'][0]['text'] == 'Modda nima? ([shaxsiy ma’lumot olib tashlandi])'
    assert payload['history'][1] == data['history'][1]
    assert payload['evidence'][0]['text'] == data['evidence'][0]['text']
    assert tutor.sanitized(question) == payload['message']


def test_question_context_cannot_change_inside_conversation():
    data=request(attempt_id='owned',question_key='first',checked=True)
    row,_=tutor.begin(1,data)
    tutor.release(row)
    with pytest.raises(HTTPException) as error:
        tutor.begin(1,data.model_copy(update={'question_key':'second'}))
    assert error.value.detail=='conversation_question_changed'


def test_grounding_diagnostic_is_precise_without_logging_content(caplog):
    bad=plan(context())
    bad['paragraphs'][0]['text']='PRIVATE-RESPONSE with no quoted evidence here.'
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(bad),context())
    assert 'quote_not_in_paragraph' in caplog.text
    assert 'PRIVATE-RESPONSE' not in caplog.text
    assert context()['evidence'][0]['text'] not in caplog.text


def test_unchecked_question_is_rejected_before_retrieval():
    data=request(attempt_id='owned',question_key='first',checked=False)
    row,_=tutor.begin(1,data)
    with pytest.raises(HTTPException) as error:
        tutor.retrieve(None,1,data,row)
    assert error.value.detail=='checked_question_required'


@pytest.mark.parametrize('repair', [True, False])
def test_format_retry_is_bounded_and_revalidated(explanation_transport, repair):
    explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    def output(body):
        result = plan(body)
        if len(explanation_transport.calls) == 1 or not repair:
            result['paragraphs'][0]['text'] = 'An explanation without its literal source quote.'
        return result
    explanation_transport.plan = output
    provider = GeminiExplanationProvider('synthetic-key')
    if repair:
        assert provider.chat(context())['status'] == 'answered'
    else:
        with pytest.raises(SelectorUnavailable):
            provider.chat(context())
    assert len(explanation_transport.calls) == 2
    sent = explanation_transport.calls[-1][1]['json']['messages']
    assert 'QUOTE CORRECTION' in sent[0]['content']
    assert 'An explanation without' not in json.dumps(sent)


def test_invented_source_is_rejected_after_bounded_repair(explanation_transport):
    explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    result = plan(context())
    result['paragraphs'][0]['quotes'][0]['text'] = 'Invented source fact'
    explanation_transport.plan = result
    with pytest.raises(SelectorUnavailable):
        GeminiExplanationProvider('synthetic-key').chat(context())
    assert len(explanation_transport.calls) == 2


def test_explicit_quote_slot_renders_only_verified_exact_source():
    value = plan(context())
    value['paragraphs'][0]['text'] = '{{quote:0}} Sodda tushuntirish.'
    reply = tutor.validate_reply(json.dumps(value), context())
    assert reply['paragraphs'][0]['text'] == context()['evidence'][0]['text'] + ' Sodda tushuntirish.'


def test_source_option_resolves_exact_quote_without_model_copying():
    value = plan(context())
    value['paragraphs'][0] = dict(text='{{quote:0}} Sodda tushuntirish.',
        quotes=[dict(evidence_id='e1', quote_id='q1')])
    reply = tutor.validate_reply(json.dumps(value), context())
    assert reply['paragraphs'][0]['text'] == context()['evidence'][0]['text'] + ' Sodda tushuntirish.'
    assert reply['paragraphs'][0]['evidence_ids'] == ['e1']


@pytest.mark.parametrize('case', ['unknown_evidence', 'unknown_option', 'extra_text', 'number', 'missing_slot'])
def test_source_options_cannot_bypass_final_validation(case):
    value = plan(context())
    paragraph = value['paragraphs'][0]
    paragraph.update(text='{{quote:0}} Sodda tushuntirish.',
                     quotes=[dict(evidence_id='e1', quote_id='q1')])
    if case == 'unknown_evidence': paragraph['quotes'][0]['evidence_id'] = 'e999'
    if case == 'unknown_option': paragraph['quotes'][0]['quote_id'] = 'q999'
    if case == 'extra_text': paragraph['quotes'][0]['text'] = 'Invented fact'
    if case == 'number': paragraph['text'] += ' 9999'
    if case == 'missing_slot': paragraph['text'] = 'An unrelated unsupported explanation.'
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(value), context())


def test_quote_menu_contains_only_bounded_exact_source_slices():
    evidence = dict(text='O‘simliklar o‘sadi. Suv zarur!\n' + 'a' * 301)
    options = tutor.quote_options(evidence)
    assert options == {'q1': 'O‘simliklar o‘sadi.', 'q2': 'Suv zarur!'}
    assert all(value in evidence['text'] for value in options.values())


def test_option_diagnostics_keep_numeric_repair_without_accepting_bad_reply():
    value = plan(context())
    value['paragraphs'][0] = dict(text='{{quote:0}} 9999 Sodda tushuntirish.',
        quotes=[dict(evidence_id='e1', quote_id='q1')])
    assert tutor.grounding_reason(json.dumps(value), context()) == 'unsupported_numbers'
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(value), context())


def test_adjacent_slot_and_literal_do_not_repeat_verified_quote():
    value = plan(context())
    quote = context()['evidence'][0]['text']
    value['paragraphs'][0]['text'] = '«{{quote:0}}» ' + quote + ' Sodda tushuntirish.'
    reply = tutor.validate_reply(json.dumps(value), context())
    assert reply['paragraphs'][0]['text'] == quote + ' Sodda tushuntirish.'


def test_duplicate_slot_does_not_hide_unsupported_claim():
    value = plan(context())
    quote = context()['evidence'][0]['text']
    value['paragraphs'][0]['text'] = '«{{quote:0}}» ' + quote + ' 9999'
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(value), context())


def test_nonadjacent_quote_repetition_is_not_rewritten():
    value = plan(context())
    quote = context()['evidence'][0]['text']
    value['paragraphs'][0]['text'] = '«{{quote:0}}» Sodda tushuntirish. ' + quote
    reply = tutor.validate_reply(json.dumps(value), context())
    assert reply['paragraphs'][0]['text'].count(quote) == 2


@pytest.mark.parametrize('change', ['invented', 'unknown_id', 'unknown_slot', 'number', 'too_long'])
def test_quote_slots_do_not_bypass_grounding(change):
    value = plan(context())
    paragraph = value['paragraphs'][0]
    paragraph['text'] = '{{quote:0}} Sodda tushuntirish.'
    if change == 'invented': paragraph['quotes'][0]['text'] = 'Manbada yoq fakt.'
    if change == 'unknown_id': paragraph['quotes'][0]['evidence_id'] = 'e999'
    if change == 'unknown_slot': paragraph['text'] += ' {{quote:3}}'
    if change == 'number': paragraph['text'] += ' 9999'
    if change == 'too_long': paragraph['text'] += 'a' * 1500
    with pytest.raises(SelectorUnavailable):
        tutor.validate_reply(json.dumps(value), context())


@pytest.mark.parametrize('repair', [True, False])
def test_numeric_repair_is_bounded_and_still_grounded(explanation_transport, repair):
    explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    def output(body):
        value = plan(body)
        value['paragraphs'][0]['text'] = '{{quote:0}} Sodda tushuntirish.'
        if len(explanation_transport.calls) == 1 or not repair:
            value['paragraphs'][0]['text'] += ' 9999'
        return value
    explanation_transport.plan = output
    if repair:
        assert GeminiExplanationProvider('synthetic').chat(context())['status'] == 'answered'
    else:
        with pytest.raises(SelectorUnavailable):
            GeminiExplanationProvider('synthetic').chat(context())
    assert len(explanation_transport.calls) == 2
    assert 'GROUNDING CORRECTION' in explanation_transport.calls[-1][1]['json']['messages'][0]['content']


def test_slot_indices_are_not_reported_as_invented_numbers():
    value = plan(context())
    value['paragraphs'][0]['text'] = '{{quote:0}} Sodda tushuntirish.'
    assert tutor.grounding_reason(json.dumps(value), context()) == 'other_validation'


@pytest.mark.parametrize('repair', [True, False])
@pytest.mark.parametrize('invalid_quote', ["O'simliklar o'sadi.", 'Bu matn manbada yo‘q.'])
def test_invalid_literal_quote_retry_uses_verified_options(explanation_transport, repair, invalid_quote):
    explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    ctx = context()
    ctx['evidence'][0]['text'] = 'O‘simliklar o‘sadi.'
    def output(body):
        value = plan(body)
        value['paragraphs'][0]['text'] = '{{quote:0}} Sodda tushuntirish.'
        if len(explanation_transport.calls) == 1 or not repair:
            value['paragraphs'][0]['quotes'][0]['text'] = invalid_quote
        else:
            value['paragraphs'][0]['quotes'] = [dict(evidence_id='e1', quote_id='q1')]
        return value
    explanation_transport.plan = output
    if repair:
        result = GeminiExplanationProvider('synthetic').chat(ctx)
        assert 'O‘simliklar o‘sadi.' in result['paragraphs'][0]['text']
    else:
        with pytest.raises(SelectorUnavailable):
            GeminiExplanationProvider('synthetic').chat(ctx)
    assert len(explanation_transport.calls) == 2
    instruction = explanation_transport.calls[-1][1]['json']['messages'][0]['content']
    assert 'QUOTE CORRECTION' in instruction and 'quote_options' in instruction
    assert invalid_quote not in instruction


def test_followup_retrieval_uses_prior_turn_without_other_subject(monkeypatch):
    calls=[]
    def chunks(db, subject):
        calls.append(subject)
        return iter([dict(text='Moddalar turli xossalarga ega.',title='Modda',grade=7,
                          lesson_key='first',source_refs=[{'page':1}])])
    monkeypatch.setattr(tutor,'teaching_chunks',chunks)
    monkeypatch.setattr(study_help,'attach_provider_eligibility',lambda *args: None)
    data=request(message='Yana sodda qilib tushuntir')
    row,_=tutor.begin(1,data)
    row.history=[{'role':'user','text':'Modda nima?'}]
    result=tutor.retrieve(None,1,data,row)
    assert calls==['kimyo'] and result['evidence'][0]['lesson_key']=='first'
    assert result['message']==data.message


def test_sentence_repeated_right_before_its_quote_is_dropped():
    value = plan(context())
    quote = context()['evidence'][0]['text']
    value['paragraphs'][0]['text'] = quote + ' «{{quote:0}}» Sodda tushuntirish.'
    reply = tutor.validate_reply(json.dumps(value), context())
    assert reply['paragraphs'][0]['text'] == '«' + quote + '» Sodda tushuntirish.'


@pytest.mark.parametrize('where', ['after', 'before'])
def test_quote_echo_with_other_apostrophe_glyphs_is_shown_once(where):
    ctx = context()
    ctx['evidence'][0]['text'] = 'Odamlar tabiatni o‘rganib, o‘z ishlarini yengillashtirgan.'
    quote = ctx['evidence'][0]['text']
    # Seen on a phone: the model repeated the cited sentence with ʻ instead of ‘.
    echo = quote.replace("'", 'ʻ').replace('‘', 'ʻ').replace('’', 'ʼ')
    value = plan(ctx)
    value['paragraphs'][0]['text'] = (
        '«{{quote:0}}» ' + echo + ' Sodda tushuntirish.' if where == 'after'
        else echo + ' «{{quote:0}}» Sodda tushuntirish.')
    reply = tutor.validate_reply(json.dumps(value), ctx)
    text = reply['paragraphs'][0]['text']
    assert text == '«' + quote + '» Sodda tushuntirish.'


def test_echo_pattern_only_relaxes_apostrophes_and_spacing():
    import re
    pattern = tutor._echo_pattern("o‘z ishlarini  yengillashtirgan.")
    assert re.fullmatch(pattern, "oʻz ishlarini yengillashtirgan.")
    assert re.fullmatch(pattern, "o'z ishlarini yengillashtirgan.")
    assert not re.fullmatch(pattern, "o‘z ishlarni yengillashtirgan.")


def test_quote_menu_prefers_sentences_over_headings():
    evidence = dict(id='e1', title='T', text=(
        'Nom va kuzatuv\n«Fizika» nomi tabiat ma’nosidagi yunoncha so‘z bilan bog‘liq. '
        'Odamlar tabiatni o‘rganib, usullar izlagan.'))
    options = list(tutor.quote_options(evidence).values())
    assert 'Nom va kuzatuv' not in options
    assert options[0].startswith('«Fizika» nomi') and options[0].endswith('.')
    # Evidence without any whole sentence still offers its exact slices.
    bare = dict(id='e2', title='T', text='Bosim birligi\nPaskal')
    assert list(tutor.quote_options(bare).values()) == ['Bosim birligi', 'Paskal']
