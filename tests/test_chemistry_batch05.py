"""Precise prior-topic and chapter-review provenance in the common lesson flow."""
from copy import deepcopy
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY, load_catalog, load_lessons, read_json, validate_lesson, readiness
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry, PREFIX, send, finish, answer_for


def test_batch05_counts_and_exact_context_review_identities():
    docs=load_lessons()
    batch=docs[16:21]
    assert [l['topic_id'] for l in batch]==[f'ch7-paragraph{n:02}' for n in range(14,19)]
    assert [l['sequence'] for l in batch]==list(range(17,22))
    assert sum(p['implemented_lessons'] for p in readiness(load_catalog(),docs[:21]))==21
    gas=batch[1]
    assert gas['source_context_ids']==['ch7-paragraph10']
    refs=gas['facts']['co2mass']['source_refs']
    assert refs[0]['paragraph']==10 and refs[0]['printed_pages']==[34]
    chapter=batch[2]
    assert set(chapter['source_activity_ids'])=={'ch7-1','ch7-2'}
    for ref in chapter['source_refs']:
        if ref['topic_id'] in {'ch7-1','ch7-2'}:
            assert ref['paragraph'] is None
        else:
            assert ref['paragraph']==16 and set(ref['printed_pages'])<={45,46,47}
    assert len(batch[2]['assessments'])==17


@pytest.mark.parametrize('mutation',['future','duplicate','unknown','wrong_identity','undeclared','early_review','wrong_kind'])
def test_context_or_review_cannot_bypass_source_order_or_page_identity(mutation):
    docs=load_lessons();l=deepcopy(docs[17]);r=read_json(DIRECTORY/'grade7_paragraph15_review.json')
    if mutation=='future':l['source_context_ids']=['ch7-paragraph18']
    if mutation=='duplicate':l['source_context_ids']*=2
    if mutation=='unknown':l['source_context_ids']=['unknown']
    if mutation=='wrong_identity':l['facts']['co2mass']['source_refs'][0]['topic_id']=l['topic_id']
    if mutation=='undeclared':l.pop('source_context_ids')
    if mutation=='early_review':l['source_activity_ids']=['ch7-1']
    if mutation=='wrong_kind':l['source_activity_ids']=['ch7-paragraph10']
    with pytest.raises(ValueError):validate_lesson(load_catalog(),l,r)


def test_context_does_not_bypass_the_known_editorial_key_hold():
    l=deepcopy(load_lessons()[18]);r=read_json(DIRECTORY/'grade7_paragraph16_review.json')
    l['source_context_ids']=['ch7-paragraph13']
    # Claim cannot acquire approval merely by being placed in another lesson.
    ref=deepcopy(read_json(DIRECTORY/'grade7_paragraph13.json')['facts']['ratio']['source_refs'][0])
    evidence=deepcopy(read_json(DIRECTORY/'grade7_paragraph13_review.json')['source_pages'][-1])
    r['source_pages'].append(evidence)
    l['facts']['mr_review']['source_refs']=[ref]
    l['facts']['mr_review']['verified_answers'].append('42.86')
    with pytest.raises(ValueError,match='unresolved_source_percentage'):validate_lesson(load_catalog(),l,r)


def test_open_source_issues_prevent_ready_even_if_all_topic_ids_are_present():
    catalog=load_catalog()
    synthetic=[{'topic_id':r['id']} for b in catalog['books'] for r in b['records']
               if r['kind'] in {'paragraph','laboratory','practical'}]
    states={p['grade']:p for p in readiness(catalog,synthetic)}
    assert states[7]['implemented_lessons']==74 and not states[7]['course_ready']
    assert len(states[7]['pending_source_review_ids'])>=2
    assert not states[9]['course_ready']
    assert not states[8]['course_ready']  # New original-page reviews remain open.
    assert all(states[g]['course_ready'] for g in [10,11])


@pytest.mark.parametrize('value',['0.00001','1e-5','1.0e-5'])
def test_unreviewed_ozone_exposure_number_cannot_become_an_answer(value):
    l=deepcopy(load_lessons()[20]);r=read_json(DIRECTORY/'grade7_paragraph18_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='numeric_value')
    q['public']['unit']='%'
    q['grading_spec'].update(unit='%',expected=value,verified_answer=value)
    l['facts'][q['fact_ids'][0]]['verified_answers'].append(value)
    with pytest.raises(ValueError,match='unresolved_ozone_context'):
        validate_lesson(load_catalog(),l,r)


def test_unreviewed_ozone_layer_thickness_is_not_a_numeric_task():
    l=deepcopy(load_lessons()[20]);r=read_json(DIRECTORY/'grade7_paragraph18_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='numeric_value')
    q['public']['unit']='mm'
    with pytest.raises(ValueError,match='unresolved_ozone_context'):
        validate_lesson(load_catalog(),l,r)


def test_all_batch05_questions_same_xp_and_optional_public_source_fixtures(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:16]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=320

    def exercise(l,export=None):
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json();public=deepcopy(attempt);answers={}
        assert 'grading_spec' not in json.dumps(attempt)
        for q in l['assessments']:
            result=send(client,attempt,q,answer_for(q))
            assert result.status_code==200 and result.json()['is_correct'],result.text
            answers[q['key']]=result.json()
        done=finish(client,attempt)
        assert done.status_code==200
        assert done.json()==finish(client,attempt).json()
        if export and os.getenv('CHEMISTRY_BATCH05_FIXTURES'):
            directory=Path(os.environ['CHEMISTRY_BATCH05_FIXTURES']);directory.mkdir(parents=True,exist_ok=True)
            sid='chv2:900003:55555555-5555-4555-8555-555555555555'
            public['attempt_id']=sid;public['expires_at']='2099-01-01T00:00:00+00:00'
            final=done.json();final['attempt_id']=sid;final['elapsed_seconds']=180
            for suffix,payload in [('lesson',public),('results',{'answers':answers,'result':final})]:
                (directory/f'chemistry_{export}_{suffix}.json').write_bytes((json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
        return done.json()

    for l in docs[16:21]:
        export={18:'context',19:'review'}.get(l['sequence'])
        assert exercise(l,export)['xp_awarded']==20
    # Export an actual practical payload, not a renamed theoretical fixture.
    assert exercise(docs[2],'practical')['xp_awarded']==0
    assert exercise(docs[18])['xp_awarded']==0
    with factory() as db:
        assert db.get(User,1).xp_total==420
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==21
        old=db.get(User,42)
        assert (old.xp_total,old.streak_days)==(137,3)
