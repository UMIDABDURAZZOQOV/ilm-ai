"""Grade9§13–17: scanned source scopes, political labels and appendix context."""
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
    return [d for d in load_lessons() if d['grade']==9 and 13<=d['sequence']<=17]


def test_batch28_source_order_counts_and_reviewed_answer_targets():
    ds=batch()
    assert [d['sequence'] for d in ds]==list(range(13,18))
    assert [len(d['facts']) for d in ds]==[11,12,9,14,14]
    assert [len(d['content']['cards']) for d in ds]==[7,8,6,7,8]
    assert [len(d['assessments']) for d in ds]==[10,10,10,10,14]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==22
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,ending',[(13,False),(14,False),(14,True),(15,False),(15,True),(16,False),(16,True),(17,False),(17,True)])
def test_batch28_shared_original_page_regions_cannot_be_broadened(number,ending):
    d=deepcopy(batch()[number-13]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    index=4 if number==17 and ending else -1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch28_names_policy_titles_and_terms_have_finite_distinct_targets():
    ds=batch()
    for i,index,wrong in [(0,7,'Suvaysh'),(1,6,'Morgan'),(2,7,'Adolatli yo‘l'),(2,9,'Teodor Ruzvelt'),(3,8,'Taft'),(4,10,'R. Dias'),(4,12,'P. Vilya')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade9_paragraph17_review.json')
    d['assessments'][12]['grading_spec']['aliases'].append('P. Vilya')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_batch28_colonial_racial_and_dictatorship_judgments_are_not_keys():
    ds=batch()
    for i,key in [(0,'colonial_model'),(0,'central_asia'),(1,'growth'),(1,'violence'),(2,'indigenous'),(2,'reforms'),(3,'model'),(3,'territories'),(3,'map'),(4,'development'),(4,'dictatorship'),(4,'map')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade9_paragraph17_review.json')
    d['assessments'][0]['fact_ids']=['dictatorship']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['dictatorship']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_batch28_appendix154_is_exact_lesson_context_without_whole_appendix_approval():
    catalog=load_catalog();appendix=next(r for r in catalog['books'][3]['ancillary_records'] if r['id']=='wh9-appendix')
    assert appendix['fact_review']=='not_reviewed'
    d=batch()[4];refs=[r for r in d['source_refs'] if r['topic_id']=='wh9-appendix']
    assert len(refs)==1 and refs[0]['pdf_pages']==[154]
    assert all(not {155,156}.intersection(r['pdf_pages']) for r in d['source_refs'])
    r=read_json(DIRECTORY/'grade9_paragraph17_review.json')
    next(p for p in r['source_pages'] if p['pdf_page']==154)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(catalog,d,r)


def test_all140_units2800_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:140]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2800
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==140
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:17])
    assert all(r['state']!='completed' for r in nine['lessons'][17:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
