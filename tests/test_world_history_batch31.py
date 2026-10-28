"""Grade9 paragraphs28-32: finite names, source boundaries and political scope."""
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
    return [d for d in load_lessons() if d['grade']==9 and 28<=d['sequence']<=32]


def test_batch31_source_order_scoped_facts_counts_and_finite_targets():
    ds=batch()
    assert [d['sequence'] for d in ds]==list(range(28,33))
    assert [len(d['facts']) for d in ds]==[13,13,13,15,15]
    assert [len(d['content']['cards']) for d in ds]==[7,7,7,7,8]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,page',[(28,97),(28,101),(29,101),(30,105),(30,108),(31,108),(31,112),(32,112),(32,116)])
def test_batch31_shared_source_pages_cannot_be_broadened(number,page):
    d=deepcopy(batch()[number-28]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch31_aliases_cannot_cross_question_targets_or_distinct_organizations():
    ds=batch()
    for i,index,wrong in [(0,7,'Xitoy uyg‘onish jamiyati'),(0,8,'Xalq gazetasi'),(1,8,'Svadeshi'),(1,9,'Svaraj'),(2,8,'Tabriz'),(2,9,'Konvensiya'),(3,7,'Abdurahmon'),(3,8,'Rezidensiya'),(3,9,'Missiya'),(4,8,'Yosh turklar'),(4,9,'Birlik va taraqqiyot')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[1]);r=read_json(DIRECTORY/'grade9_paragraph29_review.json')
    d['assessments'][8]['grading_spec']['aliases'].append('Svadeshi')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_batch31_political_interpretation_and_unverified_precision_are_not_keys():
    ds=batch()
    for i,key in [(0,'economy'),(0,'programme'),(0,'constitutional'),(1,'economy'),(1,'press'),(1,'rights'),(2,'dependence'),(2,'rights'),(3,'rivalry'),(3,'governance'),(4,'economy'),(4,'counter'),(4,'ideologies')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    assert ds[3]['facts']['tarzi']['verified_answers']==['Tarziy']
    assert ds[3]['facts']['durand']['verified_answers']==['Dyurand']
    assert ds[4]['facts']['sultan']['verified_answers']==['Abdulhamid II']
    assert all(105 not in ref['pdf_pages'] for ref in ds[1]['source_refs'])
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade9_paragraph32_review.json')
    d['assessments'][0]['fact_ids']=['ideologies']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['ideologies']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_batch31_appendix_digest_per_link_without_whole_map_approval():
    c=load_catalog();appendix=next(r for r in c['books'][3]['ancillary_records'] if r['id']=='wh9-appendix')
    assert appendix['fact_review']=='not_reviewed'
    for n,d in zip(range(28,33),batch()):
        refs=[ref for ref in d['source_refs'] if ref['topic_id']=='wh9-appendix']
        assert len(refs)==1 and refs[0]['pdf_pages']==[156]
        assert not d['facts']['map']['automatic_assessment_allowed']
        r=read_json(DIRECTORY/f'grade9_paragraph{n:02d}_review.json')
        next(row for row in r['source_pages'] if row['pdf_page']==156)['page_image_sha256']='0'*64
        with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(c,d,r)


def test_all155_units3100_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:155]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3100
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==155
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:32])
    assert all(r['state']!='completed' for r in nine['lessons'][32:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
