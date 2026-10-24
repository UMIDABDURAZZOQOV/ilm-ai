"""Source-reviewed formula, amount, change, equation and composition lessons."""
from copy import deepcopy
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY, load_catalog, load_lessons, read_json, validate_lesson, validate_catalog
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry, PREFIX, send, finish, answer_for


def test_batch04_notation_keys_are_taught_source_reviewed_and_balanced():
    docs=load_lessons()[11:16]
    assert [l['topic_id'] for l in docs]==[f'ch7-paragraph{n:02}' for n in range(9,14)]
    assert sum(len(l['content']['cards']) for l in docs)==30
    assert sum(len(l['assessments']) for l in docs)==56
    assert all(l['content']['formulas'] for l in docs if l['topic_id']!='ch7-paragraph11')
    review=read_json(DIRECTORY/'grade7_paragraph13_review.json')
    assert any('discrepancy' in n and '42.88' in n and '42.86' in n for n in review['scientific_review_notes'])
    # No conflicting CO/CO2 percentage becomes a learner's answer key.
    assert not {'42.88','42.86','57.12','57.14','27.29','27.27','72.71','72.73'} & {
        q['grading_spec']['verified_answer'] for q in docs[-1]['assessments']}


def test_notation_validation_rejects_bad_alias_or_unbalanced_private_key():
    catalog=load_catalog();l=deepcopy(load_lessons()[11]);r=read_json(DIRECTORY/'grade7_paragraph09_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='chemical_formula')
    q['grading_spec']['aliases']=['H2O']
    with pytest.raises(ValueError,match='formula_alias_composition'):validate_lesson(catalog,l,r)
    l=deepcopy(load_lessons()[14]);r=read_json(DIRECTORY/'grade7_paragraph12_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='chemical_equation')
    q['grading_spec'].update(expected='Mg+O2=MgO',verified_answer='Mg+O2=MgO')
    l['facts'][q['fact_ids'][0]]['verified_answers'].append('Mg+O2=MgO')
    with pytest.raises(ValueError,match='unbalanced_reviewed_equation'):validate_lesson(catalog,l,r)


def test_editorial_percentage_conflict_cannot_be_hidden_or_used_as_a_key():
    catalog=deepcopy(load_catalog())
    row=next(r for r in catalog['books'][0]['records'] if r['id']=='ch7-paragraph13')
    row.pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)
    l=deepcopy(load_lessons()[15]);r=read_json(DIRECTORY/'grade7_paragraph13_review.json')
    l['facts']['ratio']['verified_answers'].append('42,86%')
    with pytest.raises(ValueError,match='unresolved_source_percentage'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('broken',['o?simlik','\ufffd'])
def test_corrupted_lesson_copy_fails_closed(broken):
    l=deepcopy(load_lessons()[11]);l['content']['cards'][0]['body']=broken
    with pytest.raises(ValueError,match='corrupted_utf8_lesson_copy'):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/'grade7_paragraph09_review.json'))


def test_batch04_all_questions_wrong_balance_feedback_and_equivalent_replay(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:11]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,
                                     attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=220
    for l in docs[11:16]:
        r=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert r.status_code==200,r.text
        attempt=r.json();public=deepcopy(attempt);submitted={}
        assert 'grading_spec' not in json.dumps(attempt)
        for q in l['assessments']:
            spec=q['grading_spec']
            if q['response_kind']=='chemical_equation':
                bad=send(client,attempt,q,{'value':'<script>'})
                assert bad.status_code==422 and 'solution' not in bad.text
            response=send(client,attempt,q,answer_for(q))
            assert response.status_code==200,response.text
            assert response.json()['is_correct']
            submitted[q['key']]=response.json()
            if q['response_kind']=='chemical_formula':
                unicode_value=spec['expected'].translate(str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉'))
                assert send(client,attempt,q,{'value':unicode_value}).json()==response.json()
            if q['response_kind']=='chemical_equation':
                # Whitespace, arrow and term order changes are the same answer.
                sides=spec['expected'].split('=')
                equivalent=' + '.join(reversed(sides[0].split('+')))+' → '+' + '.join(reversed(sides[1].split('+')))
                assert send(client,attempt,q,{'value':equivalent}).json()==response.json()
        done=finish(client,attempt)
        assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,attempt).json()==done.json()
        target=os.getenv('CHEMISTRY_BATCH04_FIXTURES')
        if target and l['sequence'] in {12,15}:
            directory=Path(target);directory.mkdir(parents=True,exist_ok=True)
            name='formula' if l['sequence']==12 else 'equation'
            sid=f"chv2:900003:{'3' if name=='formula' else '4'}3333333-3333-4333-8333-333333333333"
            public['attempt_id']=sid;public['expires_at']='2099-01-01T00:00:00+00:00'
            result=done.json();result['attempt_id']=sid;result['elapsed_seconds']=180
            for suffix,payload in [('lesson',public),('results',{'answers':submitted,'result':result})]:
                (directory/f'chemistry_{name}_{suffix}.json').write_bytes((json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    with factory() as db:
        assert db.get(User,1).xp_total==320
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==16
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)

    # A fresh replay can be wrong without awarding another20XP. It reports the
    # source-backed reason and solution only after submission, then locks answer.
    l=docs[14]
    attempt=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).json()
    for q in l['assessments'][:6]:assert send(client,attempt,q,answer_for(q)).status_code==200
    q=l['assessments'][6]
    wrong=send(client,attempt,q,{'value':'Mg+O2=MgO'})
    assert wrong.status_code==200 and wrong.json()['code']=='atom_imbalance'
    assert wrong.json()['is_correct'] is False and wrong.json()['solution']
    assert send(client,attempt,q,answer_for(q)).status_code==409
