"""Grade8 paragraphs21–25: exact names, genres, source regions and dates."""
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
    return [d for d in load_lessons() if d['grade']==8 and 21<=d['sequence']<=25]


def test_batch23_original_order_counts_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[21,22,23,24,25]
    assert [len(d['facts']) for d in ds]==[16,11,15,12,13]
    assert [len(d['content']['cards']) for d in ds]==[9,6,9,8,8]
    assert [len(d['assessments']) for d in ds]==[16,10,14,12,12]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==24
    for d in ds:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,key in [(0,'causes'),(1,'causes'),(1,'politics'),(2,'economy'),(2,'artists'),(3,'outcomes'),(4,'categories'),(4,'outcomes'),(4,'map_dates')]:
        assert not ds[n]['facts'][key]['automatic_assessment_allowed']
    assert all(126 not in ref['pdf_pages'] for ref in ds[4]['source_refs'])
    # Full names requested in FRQ must appear in original teaching, not only keys.
    assert 'Fyodor Mixaylovich Dostoyevskiy' in ' '.join(c['body'] for c in ds[2]['content']['cards'])
    assert 'Xose Morelos uning ishini davom ettirgan' in ' '.join(c['body'] for c in ds[4]['content']['cards'])


@pytest.mark.parametrize('number,ending',[(21,False),(22,False),(23,False),(24,False),(25,False),(21,True),(22,True),(23,True),(24,True)])
def test_batch23_exact_shared_original_regions(number,ending):
    d=deepcopy(batch()[number-21]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_full_names_genres_regnal_ordinals_and_unions_are_distinct():
    ds=batch()
    for n,index,wrong in [(0,15,'Napoleon I'),(1,9,'Bismark'),(2,10,'Aleksandr I'),(2,12,'Aleksandr Sergeyevich Pushkin'),(3,8,'Linkoln'),(3,11,'Melvill'),(4,9,'Kolumbiya'),(4,11,'Migel Idalgo')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[2]);r=read_json(DIRECTORY/'grade8_paragraph23_review.json')
    d['assessments'][12]['grading_spec']['aliases'].append('Aleksandr Sergeyevich Pushkin')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_colonial_social_labels_cannot_be_automatic_biological_truths():
    d=deepcopy(batch()[4]);r=read_json(DIRECTORY/'grade8_paragraph25_review.json')
    d['assessments'][0]['fact_ids']=['categories']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['categories']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_new_states_map_requires_exact_original_image_digest():
    d=batch()[4];r=read_json(DIRECTORY/'grade8_paragraph25_review.json')
    next(p for p in r['source_pages'] if p['pdf_page']==123)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


def test_all115_units2300_xp_once_and_existing_grade_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:115]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2300
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==115
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:25])
    assert all(r['state']!='completed' for r in eight['lessons'][25:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
