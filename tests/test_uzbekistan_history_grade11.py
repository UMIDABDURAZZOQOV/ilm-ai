"""Grade11 literal source answers, separate progress and owned PostgreSQL schema."""

from uuid import uuid4

import pytest
import test_uzbekistan_history_course as g7

from services.models import User
from services.uzbekistan_history_grading import grade_answer
from services.uzbekistan_history_models import HistoryProgress
from services.uzbekistan_history_validation import load_course

P = g7.P
MCQ = {
    1: ["Abdulla Oripov", "Davlat gerbi", "1-sentabr"],
    2: ["Senat", "Vazirlar Mahkamasi", "Yurisdiksiya"],
    3: ["Sessiya", "Ko‘ppartiyaviylik", "Markaziy saylov komissiyasi"],
    4: ["Harakatlar strategiyasi", "Xalq qabulxonalari", "Konsepsiya"],
    5: ["So‘m-kupon", "Asaka", "Magistral"],
}
FRQ = {
    1: ["Mutal Burhonov", "8-dekabr"],
    2: ["Vatan himoyachilari kuni", "Qonunchilik palatasi"],
    3: ["Fuqarolar yig‘ini", "O‘zLiDeP"],
    4: ["Virtual qabulxona", "Davlat dasturi"],
    5: ["Afrosiyob", "Qamchiq tunneli"],
}
ORDER = {1: ["e1", "e2", "e3"], 3: ["e1", "e2", "e3"], 5: ["e1", "e2", "e3"]}

# Independent original-page oracles for the reviewed drafts; registration below
# determines which batches can enter the preview. No key is derived from a rubric.
MCQ.update(
    {
        6: ["Konvertatsiya", "Logistika", "Angren"],
        7: ["Skrining", "Nuroniy", "Infratuzilma"],
        8: ["Milliy-madaniy markazlar", "Baynalmilal", "21-fevral"],
        9: ["Seminariya", "Konfessiya", "Toshkent"],
        10: [
            "Kadrlar tayyorlash milliy dasturi",
            "11 yillik ta’lim",
            "Maktabgacha ta’lim vazirligi",
        ],
        11: ["Bakalavr", "Davlat test markazi", "Sirtqi ta’lim"],
        12: ["Oliy attestatsiya komissiyasi", "Innovatsiya", "Integratsiya"],
        13: ["Universiada", "Futbol", "Boks"],
        14: ["O‘zbekiston yoshlar ittifoqi", "Umid", "Muhammad al-Xorazmiy"],
        15: ["Temuriylar tarixi davlat muzeyi", "O‘zbek palovi", "Jizzax"],
        16: ["Samarqand", "Hunarmand", "Moziydan sado"],
        17: [
            "Afg‘oniston",
            "Tashqi ishlar vazirligi",
            "Nizolarni tinch yo‘l bilan hal qilish",
        ],
        18: ["Tojikiston", "Delimitatsiya", "Sammit"],
        19: ["Rossiya", "Bill Klinton", "Moskva"],
        20: ["Alisher Navoiy", "Ikki tomonlama aloqalar", "Toshkent"],
        21: ["Birlashgan Millatlar Tashkiloti", "6+2", "Transchegaraviy"],
        22: ["Pekin", "Shanxay beshligi", "Pokiston"],
    }
)
FRQ.update(
    {
        6: ["Erkin iqtisodiy zona", "Konvertatsiya"],
        7: ["Fuqarolar yig‘ini", "Keksalarni e’zozlash yili"],
        8: ["16 noyabr", "Baynalmilal"],
        9: ["Tolerantlik", "Samarqand"],
        10: ["1 oktabr", "Maktabgacha ta’lim"],
        11: ["Magistr", "PhD"],
        12: ["OAK", "Xorazm Ma’mun akademiyasi"],
        13: ["Umid nihollari", "Ravshan Ermatov"],
        14: ["30 iyun", "Zulfiya davlat mukofoti"],
        15: ["21 mart", "Mirzo Ulug‘bek"],
        16: ["O‘zbekkino", "Ijod"],
        17: ["Tashqi siyosiy faoliyat konsepsiyasi", "Orol muammosi"],
        18: ["Dushanbe", "Sammit"],
        19: ["Bill Klinton", "Xitoy"],
        20: ["Tokio", "Narasimxa Rao"],
        21: ["Toshkent", "Orolni qutqarish xalqaro jamg‘armasi"],
        22: ["MDH", "Hindiston"],
    }
)
ORDER.update(
    {
        15: ["e1", "e2", "e3"],
        19: ["e1", "e2", "e3"],
        21: ["e1", "e2", "e3"],
        22: ["e1", "e2", "e3"],
    }
)


def lessons():
    return [l for d in load_course() if d["grade"] == 11 for l in d["lessons"]]


def answers(lesson):
    """Literal values checked on PDF5–46; never read grading_spec to derive a key."""
    mc = short = 0
    result = []
    for q in lesson["assessments"]:
        if q["response_kind"] == "concept_selection":
            value = MCQ[lesson["sequence"]][mc]
            result.append(
                {
                    "choice_id": next(
                        o["id"] for o in q["public"]["options"] if o["label"] == value
                    )
                }
            )
            mc += 1
        elif q["response_kind"] == "short_text":
            result.append({"value": FRQ[lesson["sequence"]][short]})
            short += 1
        else:
            result.append({"order": ORDER[lesson["sequence"]]})
    return result


@pytest.mark.parametrize("sequence", range(1, 23))
def test_literal_original_page_answer_keys_and_wrong_answers(sequence):
    lesson = lessons()[sequence - 1]
    for q, value in zip(lesson["assessments"], answers(lesson)):
        assert grade_answer(q["grading_spec"], value) == "correct"
        if "choice_id" in value:
            wrong = next(
                o["id"] for o in q["public"]["options"] if o["id"] != value["choice_id"]
            )
            assert grade_answer(q["grading_spec"], {"choice_id": wrong}) == "incorrect"
        elif "value" in value:
            assert (
                grade_answer(q["grading_spec"], {"value": "bu javob emas"})
                == "incorrect"
            )
        else:
            assert (
                grade_answer(q["grading_spec"], {"order": value["order"][::-1]})
                == "incorrect"
            )


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from g7.preview.__wrapped__(tmp_path, monkeypatch)


def start(client, lesson):
    r = client.post(
        f"{P}/lessons/{lesson['key']}/start",
        json={"assessment_version": 2, "request_id": str(uuid4())},
    )
    return r


def finish(client, lesson):
    r = start(client, lesson)
    assert r.status_code == 200, r.text
    a = r.json()
    assert "grading_spec" not in str(a) and "accepted_answers" not in str(a)
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        payload = {
            "assessment_version": 2,
            "assessment_key": q["key"],
            "answer": answer,
        }
        url = f"{P}/attempts/{a['attempt_id']}/answers"
        first = client.post(url, json=payload)
        assert first.status_code == 200 and first.json()["is_correct"], first.text
        assert client.post(url, json=payload).json() == first.json()
    url = f"{P}/attempts/{a['attempt_id']}/complete"
    first = client.post(url, json={"assessment_version": 2})
    assert first.status_code == 200 and first.json()["score_pct"] == 100
    assert client.post(url, json={"assessment_version": 2}).json() == first.json()
    return first.json()


def test_grade11_progress_replay_and_previous_grades(preview):
    client, factory = preview
    g7.complete_lesson(client, g7.course_lessons()[0])
    before = {g: client.get(P + f"/catalog?grade={g}").json() for g in [7, 8, 9, 10]}
    catalog = client.get(P + "/catalog?grade=11").json()
    assert catalog["source_sections"] == 22
    assert catalog["implemented_sections"] == len(lessons())
    assert catalog["grade_content_complete"] is (len(lessons()) == 22)
    assert not catalog["course_ready"]
    assert start(client, lessons()[1]).status_code == 403
    for l in lessons():
        assert finish(client, l)["xp_awarded"] == 10
    assert finish(client, lessons()[0])["xp_awarded"] == 0
    for g, c in before.items():
        assert client.get(P + f"/catalog?grade={g}").json() == c
    if len(lessons()) == 22:
        done = client.get(P + "/catalog?grade=11").json()
        assert len(done["chapters"]) == 9
        assert all(c["checkpoint_state"] == "completed" for c in done["chapters"])
    with factory() as db:
        assert db.get(User, 1).xp_total == 147 + 10 * len(lessons())
        assert db.get(HistoryProgress, (1, "uzh-7-1-r1")).completed_at is not None


def test_postgres_grade11_owned_schema_replay_parallel_and_grade7_preserved(
    monkeypatch,
):
    import os
    import secrets
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import make_url
    from sqlalchemy.orm import sessionmaker

    from routers.uzbekistan_history_preview import router
    from services import db as database
    from services import tokens
    from services.database_url import normalize_database_url
    from services.models import Base
    from services.uzbekistan_history_curriculum import import_course, safe_staging_url
    from services.uzbekistan_history_models import HistoryBase

    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("opt-in local PostgreSQL URL file not supplied")
    url = normalize_database_url(Path(filename).read_text().strip())
    safe_staging_url(make_url(url))
    admin = create_engine(url)
    schema = "uzbekistan_history_grade11_" + secrets.token_hex(8)
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        Base.metadata.create_all(engine)
        HistoryBase.metadata.create_all(engine)
        factory = sessionmaker(bind=engine, expire_on_commit=False)
        with factory.begin() as db:
            db.add(
                User(id=1, name="Local QA", email="uzh11-qa@example.test", xp_total=137)
            )
            db.flush()
            assert import_course(db)["created"] == sum(
                len(d["lessons"]) for d in load_course()
            )
            assert import_course(db) == {
                "created": 0,
                "skipped": sum(len(d["lessons"]) for d in load_course()),
            }
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("UZBEKISTAN_HISTORY_PREVIEW_ENABLED", "true")
        monkeypatch.setattr(
            tokens, "JWT_SECRET", "grade11-local-pg-only-test-key-over-32-characters"
        )
        app = FastAPI()
        app.include_router(router)

        def get_db():
            with factory() as db:
                yield db

        app.dependency_overrides[database.get_db] = get_db
        with TestClient(
            app, headers={"Authorization": "Bearer " + tokens.create_access_token(1)}
        ) as client:
            g7.complete_lesson(client, g7.course_lessons()[0])
            for lesson in lessons()[:-1]:
                result = finish(client, lesson)
                assert result["xp_awarded"] == 10
            last = lessons()[-1]
            attempts = [start(client, last).json() for _ in range(2)]
            for attempt in attempts:
                for q, answer in zip(last["assessments"], answers(last)):
                    response = client.post(
                        f"{P}/attempts/{attempt['attempt_id']}/answers",
                        json={
                            "assessment_version": 2,
                            "assessment_key": q["key"],
                            "answer": answer,
                        },
                    )
                    assert response.status_code == 200 and response.json()["is_correct"]
            with ThreadPoolExecutor(max_workers=2) as pool:
                responses = list(
                    pool.map(
                        lambda a: client.post(
                            f"{P}/attempts/{a['attempt_id']}/complete",
                            json={"assessment_version": 2},
                        ),
                        attempts,
                    )
                )
            assert all(r.status_code == 200 for r in responses)
            assert sorted(r.json()["xp_awarded"] for r in responses) == [0, 10]
            result = finish(client, lessons()[0])
            assert result["xp_awarded"] == 0
        with factory() as db:
            assert db.get(User, 1).xp_total == 147 + 10 * len(lessons())
            assert db.get(HistoryProgress, (1, "uzh-7-1-r1")).completed_at is not None
            assert db.query(HistoryProgress).count() == 1 + len(lessons())
    finally:
        engine.dispose()
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()
