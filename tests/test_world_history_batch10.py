"""First grade7 batch: independent grade progress and exact supplied-book claims."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_grade7_batch01_counts_original_order_and_scoped_answers():
    documents=load_lessons()[:51];assert len(documents)==51
    batch=[d for d in documents if d['grade']==7]
    assert [d['sequence'] for d in batch]==[1,2,3,4,5]
    assert [len(d['facts']) for d in batch]==[21,16,16,16,14]
    assert [len(d['content']['cards']) for d in batch]==[12,7,7,7,6]
    assert [len(d['assessments']) for d in batch]==[12,10,10,10,10]
    assert batch[0]['prerequisite_ids']==[]
    assert batch[0]['source_context_ids']==['wh7-authors','wh7-intro']
    assert all(d['book_id']=='world-history-7-uz-2017' for d in batch)
    for d in batch:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,identifier in [(0,'land_model'),(0,'outsider'),(1,'conversion'),(2,'saxons'),(3,'ambrosius'),(3,'raids'),(4,'gerbert'),(4,'church')]:
        assert not batch[n]['facts'][identifier]['automatic_assessment_allowed']
    assert batch[-1]['assessments'][5]['grading_spec']['verified_answer']=='Genrix I — Lex — Ioann XII'


@pytest.mark.parametrize('number',[2,3,4,5])
def test_grade7_shared_boundaries_cannot_be_expanded(number):
    d=deepcopy(next(d for d in load_lessons() if d['grade']==7 and d['sequence']==number))
    r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_otton_ordinals_and_benefice_allod_cannot_become_aliases():
    batch=[d for d in load_lessons() if d['grade']==7]
    spec=batch[4]['assessments'][-1]['grading_spec']
    assert grade_answer(spec,{'value':'Otton I'})=='correct'
    assert grade_answer(spec,{'value':'Otton III'})=='incorrect'
    assert grade_answer(batch[1]['assessments'][7]['grading_spec'],{'value':'Allod'})=='incorrect'
    d=deepcopy(batch[4]);r=read_json(DIRECTORY/'grade7_paragraph05_review.json')
    d['assessments'][-1]['grading_spec']['aliases'].append('Otton III')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_uncorroborated_pope_identity_cannot_be_automatically_assessed():
    d=deepcopy(next(d for d in load_lessons() if d['grade']==7 and d['sequence']==5))
    r=read_json(DIRECTORY/'grade7_paragraph05_review.json')
    d['assessments'][0]['fact_ids']=['gerbert']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['gerbert']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_grade7_first_lesson_is_independent_and_does_not_complete_grade6(history):
    client,factory,_=history;batch=[d for d in load_lessons() if d['grade']==7]
    catalogue=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert catalogue['implemented_sections']==len(batch) and catalogue['source_sections']==44
    assert catalogue['implemented_grades']==sorted({d['grade'] for d in load_lessons()})
    assert catalogue['lessons'][0]['state']=='available'
    assert all(r['state']=='locked' for r in catalogue['lessons'][1:])
    assert client.post(f"{PREFIX}/lessons/{batch[1]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
    response=client.post(f"{PREFIX}/lessons/{batch[0]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert response.status_code==200;attempt=response.json()
    assert all(ref['grade']==7 for ref in attempt['content']['source_refs'])
    for q in batch[0]['assessments']:assert send(client,attempt,q,answer_for(q)).json()['is_correct']
    assert finish(client,attempt).json()['xp_awarded']==20
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['lessons'][0]['state']=='available' and all(r['state']!='completed' for r in six['lessons'])
    assert seven['lessons'][0]['state']=='completed' and seven['lessons'][1]['state']=='available'
    with factory() as db:
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==1
        assert db.get(User,1).xp_total==20 and db.get(User,42).xp_total==137


def test_grade_transition_all51_units_once_only1020_xp(history):
    client,factory,_=history;documents=load_lessons()[:51]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1020
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==51
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:5])
    assert all(r['state']!='completed' for r in seven['lessons'][5:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
