"""Grade9 original-page literal keys, combined paragraphs and real owned-schema QA."""

from uuid import uuid4

import pytest
import test_uzbekistan_history_course as g7

from services.models import User
from services.uzbekistan_history_grading import grade_answer
from services.uzbekistan_history_models import HistoryProgress
from services.uzbekistan_history_validation import load_course

P = g7.P
MCQ = {
    1: ["Zarafshon vodiysi", "Xiva", "Farg‘ona vodiysi", "Hazorasp"],
    2: ["Parvonachi", "Mirobboshi", "Mirshabboshi", "Minglar"],
    3: ["Yarmchi", "Solg‘ut", "Marg‘ilon", "Agrar"],
    4: ["Ogahiy", "Turdi Ali va Mirzo Mahmud", "Truppa"],
    5: ["Irtish", "Sirdaryo", "Oqmachit"],
}
FRQ = {
    1: ["Talash yerlar", "Noiblik"],
    2: ["Mushrif", "Mirzaboshi"],
    3: ["Chig'ir", "Mutavalli"],
    4: ["Zullisonayn", "Epos"],
    5: ["Semipalatinsk", "Chimkent"],
}
ORDER = {4: ["e1", "e2", "e3"], 5: ["e1", "e2", "e3", "e4"]}

MCQ.update(
    {
        6: ["Oqsoqol", "Niyozbek", "Aliquli"],
        7: ["Verniy", "Samarqand", "Ashxobod"],
        8: ["Erjar", "Xo‘jand", "Jizzax", "O‘ratepa"],
        9: ["Amir Muzaffar", "Bobobek", "Kogon"],
        10: ["Gandimiyon", "Muhammad Rahimxon II", "Kontributsiya"],
    }
)
FRQ.update(
    {
        6: ["Chimkent", "Ultimatum"],
        7: ["Kaufman", "Yangi Marg'ilon"],
        8: ["Romanovskiy", "Sirdaryo"],
        9: ["Protektorat", "Lessar"],
        10: ["Pristan", "Amudaryo"],
    }
)
ORDER.update(
    {
        6: ["e1", "e2"],
        7: ["e1", "e2", "e3", "e4", "e5"],
        9: ["e1", "e2"],
        10: ["e1", "e2"],
    }
)

MCQ.update(
    {
        11: ["Po‘latxon", "Nasriddinbek", "Farg‘ona viloyati"],
        12: ["Duma", "Volost", "Samarqand viloyati"],
        13: ["General-gubernator", "Kredit", "Madrasa", "Avliyoota"],
        14: [
            "Biy sudlari",
            "Apellatsiya",
            "Toshkent sud palatasi",
            "Uchastka mirovoy sudyalari",
        ],
        15: ["Samarqand", "Andijon", "Paxta tozalash"],
    }
)
FRQ.update(
    {
        11: ["Skobelev", "Go'ktepa"],
        12: ["Toshkent uyezdi", "Uyezd"],
        13: ["Bo'zsuv", "Ma’muriyat ruxsati"],
        14: ["Ispravnik", "Okrug sudlari"],
        15: ["Sirdaryo magistral kanali", "Samarqand"],
    }
)
ORDER.update({11: ["e1", "e2", "e3"], 12: ["e1", "e2"], 15: ["e1", "e2"]})

MCQ.update(
    {
        16: ["Mingtepa", "Namangan", "Darvishxon"],
        17: [
            "Toshotar voqeasi",
            "Putintsev",
            "Mardikor va hunarmand-kosiblar",
            "Mish-mish",
        ],
        18: ["Dukchi eshon", "Kazarma", "Korolkov", "Andijon"],
        19: ["Toshkent — Vabo isyoni", "Muhammad Ali"],
        20: [
            "Quyi Amudaryo",
            "Muhammad Rahimxon I",
            "Beklarbegi",
            "Yog‘och va suyak ishlash",
        ],
    }
)
FRQ.update(
    {
        16: ["Yetimxon", "Mingboshi"],
        17: ["Muhammad Yoqub", "1892"],
        18: ["Katorga", "Muhammad Ali"],
        19: ["Qurbonjon dodxoh"],
        20: ["Biylar sudi", "O'n to'rt urug'"],
    }
)
ORDER.update({16: ["e1", "e2", "e3", "e4"], 19: ["e2", "e3", "e1"]})


def lessons():
    return [l for d in load_course() if d["grade"] == 9 for l in d["lessons"]]


def answers(lesson):
    """Literal values checked on PDF5–23; never read grading_spec to derive a key."""
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


@pytest.mark.parametrize("sequence", range(1, 21))
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


def test_grade9_original_numbering_independent_progress_replay_and_old_grades(preview):
    client, factory = preview
    g7.complete_lesson(client, g7.course_lessons()[0])
    before7 = client.get(P + "/catalog?grade=7").json()
    before8 = client.get(P + "/catalog?grade=8").json()
    catalog = client.get(P + "/catalog?grade=9").json()
    assert catalog["source_sections"] == 39
    assert catalog["implemented_sections"] == len(lessons())
    assert not catalog["grade_content_complete"] and not catalog["course_ready"]
    assert catalog["lessons"][3]["source_numbers"] == [4, 5]
    assert start(client, lessons()[1]).status_code == 403
    for l in lessons():
        assert finish(client, l)["xp_awarded"] == 10
    assert finish(client, lessons()[0])["xp_awarded"] == 0
    assert client.get(P + "/catalog?grade=7").json() == before7
    assert client.get(P + "/catalog?grade=8").json() == before8
    done = client.get(P + "/catalog?grade=9").json()
    assert done["chapters"][0]["checkpoint_state"] == "completed"
    assert done["chapters"][1]["checkpoint_state"] == (
        "completed" if len(lessons()) >= 11 else "locked"
    )
    assert done["chapters"][2]["checkpoint_state"] == (
        "completed" if len(lessons()) >= 15 else "locked"
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 147 + 10 * len(lessons())
        assert db.get(HistoryProgress, (1, "uzh-7-1-r1")).completed_at is not None
        assert (
            db.query(HistoryProgress)
            .filter(HistoryProgress.lesson_key.like("uzh-8-%"))
            .count()
            == 0
        )


def test_postgres_grade9_owned_schema_replay_parallel_and_grade7_preserved(monkeypatch):
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
    schema = "uzbekistan_history_grade9_" + secrets.token_hex(8)
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        Base.metadata.create_all(engine)
        HistoryBase.metadata.create_all(engine)
        factory = sessionmaker(bind=engine, expire_on_commit=False)
        with factory.begin() as db:
            db.add(
                User(id=1, name="Local QA", email="uzh8-qa@example.test", xp_total=137)
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
            tokens, "JWT_SECRET", "grade9-local-pg-only-test-key-over-32-characters"
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
