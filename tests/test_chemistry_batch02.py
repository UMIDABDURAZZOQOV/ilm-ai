"""Reviewed second batch: numerical FRQ, sequence, safety and evidence."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer, canonical_number
from services.chemistry_validation import DIRECTORY, load_catalog, load_lessons, read_json, validate_lesson
from services.models import User
from services.chemistry_models import ChemistryProgress
from test_chemistry_lesson import chemistry, PREFIX, send, finish, answer_for


@pytest.mark.parametrize('value,code',[
    ('0.1','correct'),('0,10','correct'),('1e-1','correct'),('+0.100','correct'),
    ('1','incorrect'),('-0.1','incorrect'),('0.1 nm','invalid_answer'),
    ('1/10','invalid_answer'),('NaN','invalid_answer'),('Infinity','invalid_answer'),
    ('1e999','invalid_answer'),('1e51','invalid_answer'),('1e-51','invalid_answer'),
    ('1,2.3','invalid_answer'),('٠.١','invalid_answer'),('__import__("os")','invalid_answer'),
    ('','answer_required'),(' '*3,'answer_required'),(0.1,'invalid_answer'),(True,'invalid_answer')])
def test_numeric_frq_is_exact_bounded_and_not_a_formula_evaluator(value,code):
    assert grade_answer({'kind':'numeric_value','expected':'0.1','unit':'nm'}, {'value':value})==code


def test_numeric_canonicalisation_is_exact_beyond_decimal_context_precision():
    assert canonical_number('1.66e-27')==canonical_number('0,000000000000000000000000001660')
    assert canonical_number('-0.000')=='0'
    assert canonical_number('1.00000000000000000000000000001')!=canonical_number('1.00000000000000000000000000002')


def test_second_batch_preserves_first_lesson_and_reviews_source_order():
    lessons=load_lessons()
    first=read_json(DIRECTORY/'grade7_paragraph01.json')
    assert lessons[0]==first and len(first['content']['cards'])==8
    batch=lessons[1:6]
    assert [l['topic_id'] for l in batch]==['ch7-paragraph02','ch7-practical01','ch7-practical02','ch7-paragraph03','ch7-paragraph04']
    for l in batch:
        assert any(q['response_kind']=='concept_selection' for q in l['assessments'])
        assert any(q['response_kind']!='concept_selection' for q in l['assessments'])
        assert l['prerequisite_ids']==[lessons[l['sequence']-2]['topic_id']]
    assert any(q['response_kind']=='numeric_value' for l in batch for q in l['assessments'])
    assert batch[-1]['content']['formulas'] and batch[-1]['content']['examples']
    for l in batch[1:3]:
        review=read_json(DIRECTORY/f"grade7_{'practical01' if l['sequence']==3 else 'practical02'}_review.json")
        assert any('Guided digital analysis only' in s for s in review['scientific_review_notes'])


def test_numeric_unit_or_derived_formula_cannot_lose_source_evidence():
    catalog=load_catalog();l=deepcopy(load_lessons()[5])
    review=read_json(DIRECTORY/'grade7_paragraph04_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='numeric_value')
    q['public']['unit']='unreviewed unit'
    with pytest.raises(ValueError,match='explicit_numeric_unit'):validate_lesson(catalog,l,review)
    l=deepcopy(load_lessons()[5]);l['content']['examples'][0]['source_refs']=[]
    with pytest.raises(ValueError):validate_lesson(catalog,l,review)


def test_all_six_lessons_unlock_in_order_numeric_replay_awards_once(chemistry):
    client,factory,_=chemistry
    documents=[l for l in load_lessons() if l['grade']==7 and l['sequence']<=6]
    for i,l in enumerate(documents):
        rows=client.get(PREFIX+'/catalog').json()['lessons']
        assert next(r for r in rows if r['key']==l['key'])['state']=='available'
        if i+1<len(documents):
            denied=client.post(f"{PREFIX}/lessons/{documents[i+1]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
            assert denied.status_code==403
        r=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert r.status_code==200,r.text
        attempt=r.json()
        assert 'grading_spec' not in str(attempt)
        submitted={}
        import os,json
        if os.getenv('CHEMISTRY_BATCH02_FIXTURES') and l['sequence']==6:
            from pathlib import Path
            target=Path(os.environ['CHEMISTRY_BATCH02_FIXTURES'])
            target.mkdir(parents=True,exist_ok=True)
            public=deepcopy(attempt)
            public['attempt_id']='chv2:900003:22222222-2222-4222-8222-222222222222'
            public['expires_at']='2099-01-01T00:00:00+00:00'
            (target/'chemistry_numeric_lesson.json').write_bytes((json.dumps(public,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
        for q in l['assessments']:
            if q['response_kind']=='numeric_value':
                invalid=send(client,attempt,q,{'value':'1/0'})
                assert invalid.status_code==422 and 'solution' not in invalid.text
            answer=answer_for(q)
            checked=send(client,attempt,q,answer)
            assert checked.status_code==200,checked.text
            assert checked.json()['is_correct']
            submitted[q['key']]=checked.json()
            if q['response_kind']=='numeric_value':
                # Equivalent decimal/scientific spelling must replay identically.
                from decimal import Decimal
                alias={'value':format(Decimal(q['grading_spec']['expected']),'f').replace('.',',')}
                assert send(client,attempt,q,alias).json()==checked.json()
                assert send(client,attempt,q,{'value':'999999'}).status_code==409
        result=finish(client,attempt)
        assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
        if os.getenv('CHEMISTRY_BATCH02_FIXTURES') and l['sequence']==6:
            result_public=result.json()
            result_public['attempt_id']='chv2:900003:22222222-2222-4222-8222-222222222222'
            result_public['elapsed_seconds']=180
            (target/'chemistry_numeric_results.json').write_bytes((json.dumps({'answers':submitted,'result':result_public},ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    with factory() as db:
        assert db.get(User,1).xp_total==120
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==6
        old=db.get(User,42)
        assert (old.xp_total,old.streak_days)==(137,3)
