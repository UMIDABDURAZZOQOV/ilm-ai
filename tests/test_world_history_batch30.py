"""Grade9§23–27: distinct leaders, political labels and mixed-date map layers."""
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
    return [d for d in load_lessons() if d['grade']==9 and 23<=d['sequence']<=27]


def test_batch30_source_order_scoped_facts_counts_and_finite_targets():
    ds=batch()
    assert [d['sequence'] for d in ds]==list(range(23,28))
    assert [len(d['facts']) for d in ds]==[9,13,11,13,13]
    assert [len(d['content']['cards']) for d in ds]==[6,7,7,8,7]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,ending',[(23,False),(24,False),(24,True),(25,False),(26,False),(26,True),(27,False),(27,True)])
def test_batch30_shared_source_pages_cannot_be_broadened(number,ending):
    d=deepcopy(batch()[number-23]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    index=(4 if number==26 else 3 if number==27 else -1) if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch30_person_ordinals_and_names_cannot_share_unreviewed_aliases():
    ds=batch()
    for i,index,wrong in [(0,9,'Ferdinand Koburg'),(1,7,'Fiat'),(2,8,'Aleksandr II'),(2,9,'Frans Ferdinand'),(3,7,'San-Stefano'),(4,7,'Konvensiya'),(4,8,'Intervensiya')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade9_paragraph23_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Ferdinand Koburg')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)
    king=ds[1]['assessments'][0]
    wrong=next(o['id'] for o in king['public']['options'] if o['label']=='Viktor Emmanuil III')
    assert grade_answer(king['grading_spec'],{'choice_id':wrong})=='incorrect'


def test_batch30_political_interpretations_and_unreviewed_precision_are_not_keys():
    ds=batch()
    for i,key in [(0,'rivalry'),(0,'preparation'),(1,'economy'),(1,'reforms'),(2,'bulgaria_status'),(2,'alliances'),(3,'reforms'),(3,'social'),(3,'policy'),(4,'economy'),(4,'vietnam'),(4,'outcomes')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    assert ds[1]['facts']['fiat']['verified_answers']==['Fiat']
    assert ds[0]['facts']['ferdinand']['verified_answers']==['Frans Ferdinand']
    assert all(83 not in r['pdf_pages'] for r in ds[0]['source_refs'])
    assert all(90 not in r['pdf_pages'] for r in ds[2]['source_refs'])
    d=deepcopy(ds[3]);r=read_json(DIRECTORY/'grade9_paragraph26_review.json')
    d['assessments'][0]['fact_ids']=['policy']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['policy']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_batch30_map156_requires_each_linked_source_digest_without_blanket_approval():
    catalog=load_catalog();appendix=next(r for r in catalog['books'][3]['ancillary_records'] if r['id']=='wh9-appendix')
    assert appendix['fact_review']=='not_reviewed'
    for n in [26,27]:
        d=batch()[n-23];refs=[r for r in d['source_refs'] if r['topic_id']=='wh9-appendix']
        assert len(refs)==1 and refs[0]['pdf_pages']==[156]
        assert not d['facts']['map']['automatic_assessment_allowed']
        r=read_json(DIRECTORY/f'grade9_paragraph{n:02d}_review.json')
        next(row for row in r['source_pages'] if row['pdf_page']==156)['page_image_sha256']='0'*64
        with pytest.raises(ValueError,match='exact_original_page_digest_required'):
            validate_lesson(catalog,d,r)


def test_all150_units3000_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:150]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3000
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==150
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:27])
    assert all(r['state']!='completed' for r in nine['lessons'][27:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
