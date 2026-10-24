"""Book-order second continuation: substance structure through phase changes."""
from hashlib import sha256
from uuid import uuid4

from services.chemistry_grading import grade_answer
from services.chemistry_validation import DIRECTORY, load_lessons, read_json
from services.models import User
from services.chemistry_models import ChemistryProgress
from test_chemistry_lesson import chemistry, PREFIX, send, finish, answer_for


def test_batch03_evidence_and_previously_reviewed_content_are_preserved():
    lessons=load_lessons()
    batch=lessons[6:11]
    assert [l['topic_id'] for l in batch]==['ch7-paragraph05','ch7-paragraph06','ch7-practical03','ch7-paragraph07','ch7-paragraph08']
    assert [l['sequence'] for l in batch]==list(range(7,12))
    # Pinned first lesson remains byte-identical to the prior reviewed index.
    assert sha256((DIRECTORY/'grade7_paragraph01.json').read_bytes()).hexdigest()==read_json(DIRECTORY/'grade7_paragraph01_review.json')['lesson_sha256']
    for lesson in batch:
        assert len(lesson['content']['cards'])>=5
        assert len(lesson['assessments'])>=10
        assert any(q['response_kind']=='short_text' for q in lesson['assessments'])
        for q in lesson['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            if q['response_kind']=='short_text':
                for alias in q['grading_spec']['aliases']:
                    assert grade_answer(q['grading_spec'],{'value':alias})=='correct'
    phase=next(l for l in batch if l['topic_id']=='ch7-paragraph08')
    assert {p for r in phase['source_refs'] for p in r['printed_pages']}=={28,29}
    review=read_json(DIRECTORY/'grade7_practical03_review.json')
    assert any('Digital-only' in n for n in review['scientific_review_notes'])
    assert any('101.3kPa' in n for n in read_json(DIRECTORY/'grade7_paragraph08_review.json')['scientific_review_notes'])


def test_batch03_unlock_and_all_new_assessments_complete_without_touching_other_user(chemistry):
    client,factory,_=chemistry
    docs=load_lessons()
    # Source prerequisites before this batch have already been completed by
    # this synthetic learner; do not recreate earlier attempts in every batch.
    with factory.begin() as db:
        from services.study import utcnow
        for l in docs[:6]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=120
    for l in docs[6:11]:
        rows=client.get(PREFIX+'/catalog').json()['lessons']
        assert next(r for r in rows if r['key']==l['key'])['state']=='available'
        r=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert r.status_code==200,r.text
        attempt=r.json()
        assert not {'facts','grading_spec','expected'} & attempt.keys()
        for q in l['assessments']:
            r=send(client,attempt,q,answer_for(q))
            assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,attempt)
        assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
        # A fully completed lesson can be replayed, never double-awarded.
        replay=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).json()
        for q in l['assessments']:
            assert send(client,replay,q,answer_for(q)).status_code==200
        assert finish(client,replay).json()['xp_awarded']==0
    with factory() as db:
        assert db.get(User,1).xp_total==220
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==11
        historical=db.get(User,42)
        assert (historical.xp_total,historical.streak_days)==(137,3)
