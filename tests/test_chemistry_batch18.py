"""Exact chapter prefixes and supplied electronic/bonding models;no new graders."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_next_five_source_order_counts_and_exact_chapter_prefix_identity():
    docs=load_lessons()[84:89]
    assert [l['topic_id'] for l in docs]==[f'ch8-paragraph{n:02}' for n in range(11,16)]
    assert [l['sequence'] for l in docs]==list(range(11,16))
    assert sum(len(l['content']['cards']) for l in docs)==39
    assert sum(len(l['assessments']) for l in docs)==61
    l=docs[3];assert l['source_context_ids']==['ch8-chapter03']
    refs=[r for r in l['source_refs'] if r['topic_id']=='ch8-chapter03']
    assert [r['printed_pages'] for r in refs]==[[63],[64]]
    assert all(r['paragraph'] is None and r['topic_title']=='Kimyoviy bog‘lanishlar' for r in refs)
    assert refs[1]['page_scope']=='before_first_teaching_heading'
    assert l['facts']['nucleus']['source_refs'][0]['topic_id']=='ch8-chapter03'
    q=docs[4]['assessments'][3]
    assert q['response_kind']=='concept_selection' and any(o['label']=='NH4+' for o in q['public']['options'])


@pytest.mark.parametrize('rid',[f'ch8-paragraph{n:02}' for n in range(11,16)]+['ch8-chapter03'])
def test_new_source_scope_issues_remain_pinned(rid):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==rid).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('mode,error',[
 ('future_page','claim_outside_chapter_prefix'),
 ('heading_page_without_scope','claim_outside_chapter_prefix'),
 ('false_paragraph','claim_source_identity_mismatch'),
 ('other_chapter','source_chapter_prefix_must_precede_lesson'),
 ('chapter_as_activity','same_chapter_review_anchor_required')])
def test_chapter_context_cannot_escape_prefix_or_mislabel_a_paragraph(mode,error):
    l=deepcopy(load_lessons()[87]);r=read_json(DIRECTORY/'grade8_paragraph14_review.json')
    if mode=='other_chapter':l['source_context_ids']=['ch8-chapter04']
    elif mode=='chapter_as_activity':l['source_activity_ids']=l.pop('source_context_ids')
    else:
        def mutate(v):
            if isinstance(v,dict):
                if v.get('topic_id')=='ch8-chapter03':
                    if mode=='false_paragraph' and 'paragraph' in v:v['paragraph']=3
                    if mode=='future_page' and v.get('printed_pages')==[63]:v.update(printed_pages=[65],pdf_pages=[65])
                    if mode=='future_page' and v.get('printed_page')==63:v.update(printed_page=65,pdf_page=65)
                    if mode=='heading_page_without_scope':v.pop('page_scope',None)
                for x in v.values():mutate(x)
            elif isinstance(v,list):
                for x in v:mutate(x)
        mutate(l);mutate(r)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,fid,text,error',[
 (12,'scandium','Ce4f2','unresolved_la_ce_configuration'),
 (12,'scandium','La f','unresolved_la_ce_configuration'),
 (13,'test','35.4846','unresolved_natural_chlorine_average'),
 (13,'test','35,543','unresolved_natural_chlorine_average'),
 (15,'polar','CH4 molekulasi qutbli','unreviewed_molecule_geometry')])
def test_held_configuration_average_or_geometry_is_not_an_answer(n,fid,text,error):
    l=deepcopy(load_lessons()[73+n]);r=read_json(DIRECTORY/f'grade8_paragraph{n:02}_review.json')
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
 (11,5,'P','correct'),(11,8,'10','correct'),(11,10,'0','correct'),
 (12,6,'9','correct'),(12,7,'10','correct'),(12,10,'1','correct'),
 (13,8,'SrO','correct'),(13,9,'AsH₃','correct'),(13,10,'50','correct'),
 (13,11,'72,6','correct'),(13,12,'42','correct'),(13,14,'81','correct'),
 (14,4,'yadro','correct'),(14,8,'10','correct'),(14,10,'3,16','correct'),(14,11,'1.8','correct'),
 (15,6,'xlor','correct'),(15,7,'donor','correct'),(15,10,'H₂','correct'),
 (15,11,'N2','correct'),(15,14,'3','correct'),(15,16,'1','correct')])
def test_existing_mcq_frq_contract_covers_reviewed_examples(n,qn,value,code,reviewed_chemistry_documents):
    q=reviewed_chemistry_documents[73+n]['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve84_and_chapter_refs_reach_public_api(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:84]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1680
    before=client.get(PREFIX+'/catalog?grade=7').json()
    for l in docs[84:89]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a)
        if l['topic_id']=='ch8-paragraph14':
            refs=a['content']['cards'][0]['source_refs']
            assert refs[0]['topic_id']=='ch8-chapter03' and refs[0]['paragraph'] is None and refs[0]['printed_pages']==[63]
        for q in l['assessments']:
            result=send(client,a,q,answer_for(q));assert result.status_code==200 and result.json()['is_correct'],result.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1780
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==89
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==before
