"""Grade8 paragraphs16–20: exact source regions, terms and reviewed limits."""
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
    return [d for d in load_lessons() if d['grade']==8 and 16<=d['sequence']<=20]


def test_batch22_original_order_counts_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[16,17,18,19,20]
    assert [len(d['facts']) for d in ds]==[14,11,15,12,13]
    assert [len(d['content']['cards']) for d in ds]==[8,7,8,8,8]
    assert [len(d['assessments']) for d in ds]==[12,11,12,12,12]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,key in [(0,'isolation'),(0,'culture'),(1,'economy'),(1,'science'),(2,'economy'),(2,'writers'),(3,'competition'),(3,'racism'),(4,'completion'),(4,'society'),(4,'colonies')]:
        assert not ds[n]['facts'][key]['automatic_assessment_allowed']
    assert ds[0]['facts']['offices']['verified_answers']==['Daimyo','Samuray','Syogun']
    assert ds[4]['facts']['railway']['claim']=='1825-yil Buyuk Britaniyada temiryo‘l qurilishi bilan berilgan.'


@pytest.mark.parametrize('number,ending',[(16,False),(17,False),(18,False),(19,False),(20,False),(16,True),(17,True),(18,True),(20,True)])
def test_batch22_exact_shared_original_regions(number,ending):
    d=deepcopy(batch()[number-16]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_full_names_offices_and_dominion_are_not_broad_aliases():
    ds=batch()
    for n,index,wrong in [(0,8,'Ieyasu'),(0,9,'Li'),(1,8,'Sanjoqbey'),(1,9,'Chalabiy'),(2,8,'Xatoiy'),(2,10,'Ismoil I Safaviy'),(3,11,'Qohira'),(4,9,'Mustaqillik'),(4,11,'Chartistlar')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade8_paragraph20_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Mustaqillik')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_racist_ideology_cannot_be_an_automatic_fact_key():
    d=deepcopy(batch()[3]);r=read_json(DIRECTORY/'grade8_paragraph19_review.json')
    d['assessments'][0]['fact_ids']=['racism']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['racism']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_ottoman_map_page_requires_exact_original_image_digest():
    d=batch()[1];r=read_json(DIRECTORY/'grade8_paragraph17_review.json')
    next(p for p in r['source_pages'] if p['pdf_page']==85)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


def test_all110_units2200_xp_once_and_existing_grade_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:110]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2200
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==110
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:20])
    assert all(r['state']!='completed' for r in eight['lessons'][20:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
