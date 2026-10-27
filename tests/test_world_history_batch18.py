"""Grade7 completion: four remaining paragraphs and scoped chronology reference."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():
    return [d for d in load_lessons() if d['grade']==7 and 41<=d['sequence']<=44]


def test_batch18_counts_original_order_and_ungraded_interpretations():
    documents=batch()
    assert [d['sequence'] for d in documents]==[41,42,43,44]
    assert [len(d['facts']) for d in documents]==[17,18,16,19]
    assert [len(d['content']['cards']) for d in documents]==[7,7,8,9]
    assert [len(d['assessments']) for d in documents]==[12,12,12,16]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==16
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'reforms'),(0,'range'),(1,'belief'),(1,'community'),(2,'legend'),(2,'change'),(3,'instruments'),(3,'maya_writing'),(3,'reference')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']
    assert 151 not in [p for ref in documents[2]['source_refs'] for p in ref['pdf_pages']]
    assert documents[3]['source_context_ids']==['wh7-chronology']
    assert [ref['pdf_pages'] for ref in documents[3]['facts']['reference']['source_refs']]==[[155],[156]]
    assert not any('reference' in q['fact_ids'] for q in documents[3]['assessments'])


@pytest.mark.parametrize('number,ending',[(41,False),(42,False),(43,False),(44,False),(41,True),(42,True)])
def test_batch18_exact_shared_source_regions(number,ending):
    d=deepcopy(batch()[number-41]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_reference_original_image_digest_is_not_optional():
    d=batch()[-1];r=read_json(DIRECTORY/'grade7_paragraph44_review.json')
    r['source_pages'][-1]['page_image_sha256']='0'*64
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_names_roles_and_author_work_targets_remain_finite():
    documents=batch()
    for n,index,wrong in [(0,9,'Shamsiddin Eltutmish'),(1,11,'Tlatoani'),(2,9,'Muso II'),(3,12,'Bahriya'),(3,13,'Li Son Ge')]:
        assert grade_answer(documents[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(documents[3]);r=read_json(DIRECTORY/'grade7_paragraph44_review.json')
    d['assessments'][12]['grading_spec']['aliases'].append('Bahriya')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_reference_list_does_not_approve_uncertain_automatic_chronology():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph44_review.json')
    d['assessments'][0]['fact_ids']=['reference']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['reference']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all90_units1800_xp_once_grade7_content_complete_and_grade8_pending(history):
    client,factory,_=history;documents=load_lessons()[:90]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1800
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==90
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert six['grade_content_complete'] and seven['grade_content_complete']
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:44])
    assert seven['implemented_sections']==seven['source_sections']==44
    assert seven['source_review_issue_count']==0 and not seven['source_review_pending']
    assert eight['source_sections']==33
    assert eight['implemented_sections']==sum(d['grade']==8 for d in load_lessons())
    assert not six['course_complete'] and not seven['course_complete'] and not eight['course_complete']
