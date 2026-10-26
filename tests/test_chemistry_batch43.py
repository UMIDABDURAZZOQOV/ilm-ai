"""Book-image reviewed acids/esters/fats/carbohydrates retain shared contracts."""
from collections import Counter
from copy import deepcopy
from decimal import Decimal
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import (
    DIRECTORY, load_catalog, load_lessons, read_json, validate_catalog, validate_lesson,
)
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import (
    reviewed_chemistry_documents, chemistry, PREFIX, send, finish, answer_for,
)

TOPICS = [f'ch10-paragraph{n:02}' for n in range(26, 31)]


def test_batch43_five_source_ordered_lessons_and_common_inputs(reviewed_chemistry_documents):
    lessons = reviewed_chemistry_documents[219:224]
    assert [l['topic_id'] for l in lessons] == TOPICS
    assert [l['sequence'] for l in lessons] == list(range(26, 31))
    assert sum(len(l['content']['cards']) for l in lessons) == 53
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments']) == {
        'concept_selection': 20, 'short_text': 11, 'numeric_value': 25,
        'chemical_formula': 5, 'chemical_equation': 18,
    }
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])


@pytest.mark.parametrize('topic', TOPICS)
def test_batch43_source_scope_is_required(topic):
    c = deepcopy(load_catalog())
    next(r for r in c['books'][3]['records'] if r['id'] == topic).pop('editorial_review_issues')
    with pytest.raises(ValueError, match='known_editorial_issue'):
        validate_catalog(c)


@pytest.mark.parametrize('n,fid,value,error', [
    (26, 'numbering', '2,2-metilbutan kislota', 'branched_acid_wrong_caption_is_withheld'),
    (27, 'pair', 'Dimetilefir va metilpropilefir izomer', 'different_carbon_ether_pair_cannot_be_isomers'),
    (28, 'base', 'Ishqorli gidrolizda faqat erkin kislota', 'alkaline_ester_hydrolysis_requires_source_salt_products'),
    (29, 'hydrogenation', 'Barcha o‘simlik yog‘lari suyuq', 'universal_fat_phase_claim_is_withheld'),
    (30, 'silver', 'Fruktoza kumush ko‘zguni hech qachon bermaydi', 'unverified_sugar_redox_exclusivity_is_withheld'),
])
def test_batch43_withheld_key_cannot_enter_scientific_answers(n, fid, value, error):
    l = deepcopy(read_json(DIRECTORY / f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError, match=error):
        validate_lesson(load_catalog(), l, read_json(DIRECTORY / f'grade10_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,fid,expected,value,code', [
    (26,'first','133.2','133,2','correct'),
    (26,'second','176','176','correct'),
    (26,'third','163.2','1.632e2','correct'),
    (26,'oxide','2C2H4O2+MgO=C4H6O4Mg+H2O','C2H4O2+MgO=C4H6O4Mg+H2O','atom_imbalance'),
    (27,'orbitals','3','3','correct'),
    (27,'worked','60','60','correct'),
    (27,'variant','68.182','68,182','correct'),
    (27,'variant','68.182','68.1818181818','incorrect'),
    (28,'amount','64','64','correct'),
    (28,'base','C4H8O2+NaOH=C2H3O2Na+C2H6O','C4H8O2+NaOH=C2H4O2+C2H6O','incorrect_species'),
    (29,'unknown','116','116','correct'),
    (29,'butyrin','528','528','correct'),
    (29,'propionin','199.8','199,8','correct'),
    (29,'palmitin','1251','1251','correct'),
    (29,'palmitin','C51H98O6+3NaOH=C3H8O3+3C16H31O2Na','C51H98O6+NaOH=C3H8O3+3C16H31O2Na','atom_imbalance'),
    (30,'glucose','5','5','correct'),
    (30,'reduction','6','6','correct'),
    (30,'amount','276','276','correct'),
    (30,'amount','134.4','1.344e2','correct'),
    (30,'hydrolysisatoms','C12H22O11+H2O=2C6H12O6','C12H22O11+H2O=C6H12O6','atom_imbalance'),
])
def test_batch43_exact_existing_grader(n, fid, expected, value, code, reviewed_chemistry_documents):
    l = next(l for l in reviewed_chemistry_documents if l['topic_id'] == f'ch10-paragraph{n:02}')
    q = next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected'] == expected)
    assert grade_answer(q['grading_spec'], {'value': value}) == code


def test_batch43_amounts_are_independently_recomputed():
    assert Decimal(120)*Decimal('.60')/40*74 == Decimal('133.2')
    assert Decimal(80)*Decimal('.80')/40*102 == Decimal('163.2')
    assert round(Decimal(60)/88*100, 3) == Decimal('68.182')
    assert Decimal(200)*Decimal('.40')/40*32 == 64
    assert (386-92+3*18)/3 == 116
    assert Decimal(604)/302*3*88 == 528
    assert Decimal(234)/260*3*74 == Decimal('199.8')
    assert Decimal(1209)/806*3*278 == 1251
    assert Decimal(3)*2*46 == 276
    assert Decimal(3)*2*Decimal('22.4') == Decimal('134.4')


def test_batch43_source_proofs_preserve_book_identity_and_model_scope(reviewed_chemistry_documents):
    rows = {l['topic_id']: l for l in reviewed_chemistry_documents}
    for n, fid, topic, page in [
        (26,'first','ch8-paragraph05',27),
        (27,'variant','ch8-paragraph01',7),
        (28,'amount','ch8-paragraph05',29),
        (29,'palmitin','ch8-paragraph05',27),
        (30,'amount','ch8-paragraph26',114),
    ]:
        proof = next(r for r in rows[f'ch10-paragraph{n:02}']['facts'][fid]['source_refs']
                     if r['topic_id'] == topic and r['printed_pages'] == [page])
        assert proof['file_name'] == 'kimyo_8_uzb.pdf'
        assert proof['printed_pages'] == proof['pdf_pages']
    # The undefined orbital/gram conversion and silver-mixture answer are not keys.
    l = rows['ch10-paragraph30']
    assert '450' not in {a for f in l['facts'].values() for a in f['verified_answers']}
    assert all('122' not in str(q['source_refs']) for q in l['assessments'] if q['response_kind'] == 'numeric_value')
    assert 'jami' in next(q['public']['prompt'] for q in l['assessments'] if q['response_kind'] == 'chemical_formula')


def test_batch43_preserves219_completions_and_adds100xp_once(chemistry):
    client, factory, _ = chemistry
    docs = load_lessons()
    with factory.begin() as db:
        for l in docs[:219]:
            db.add(ChemistryProgress(user_id=1, lesson_key=l['key'], best_score_pct=100,
                                    attempts=1, xp_earned=20, completed_at=utcnow()))
        db.get(User, 1).xp_total = 4380
    old = {g: client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10 = client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state'] == 'completed' for l in g10[:25])
    assert g10[25]['state'] == 'available'
    assert all(l['state'] == 'locked' for l in g10[26:])
    for l in docs[219:224]:
        response = client.post(f"{PREFIX}/lessons/{l['key']}/start", json={
            'assessment_version': 2, 'request_id': str(uuid4()),
        })
        assert response.status_code == 200, response.text
        a = response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r = send(client, a, q, answer_for(q))
            assert r.status_code == 200 and r.json()['is_correct'], r.text
        result = finish(client, a)
        assert result.status_code == 200 and result.json()['xp_awarded'] == 20
        assert finish(client, a).json() == result.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 4480
        assert db.query(ChemistryProgress).filter_by(user_id=1).count() == 224
        assert (db.get(User,42).xp_total, db.get(User,42).streak_days) == (137,3)
    current = client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state'] == 'completed' for l in current[:30])
    if len(current)>30:
        assert current[30]['state'] == 'available'
    for g,c in old.items():
        assert client.get(PREFIX+f'/catalog?grade={g}').json() == c
