"""Grade10 literal source answers, separate progress and owned PostgreSQL schema."""

from uuid import uuid4

import pytest
import test_uzbekistan_history_course as g7

from services.models import User
from services.uzbekistan_history_grading import grade_answer
from services.uzbekistan_history_models import HistoryProgress
from services.uzbekistan_history_validation import load_course

P = g7.P
MCQ = {
    1: ["Turkiston komiteti", "Mustafo Cho‘qay", "Sherali Lapin"],
    2: ["Petrograd", "Fyodor Kolesov", "Koalitsion hukumat"],
    3: ["Muhammadjon Tinishboyev", "Qo‘qon", "El bayrog‘i"],
    4: ["Turor Risqulov", "Oziq-ovqat solig‘i", "Yer maydoni"],
    5: ["Madaminbek", "Samarqand", "Skobelev"],
}
FRQ = {
    1: ["Sho‘roi Islomiya", "Aleksandr Kerenskiy"],
    2: ["Xalq Komissarlari Soveti", "Perfilev"],
    3: ["Mustafo Cho‘qay", "Obidjon Mahmudov"],
    4: ["Yangi iqtisodiy siyosat", "Pud"],
    5: ["Qo‘rboshi", "Madaminbek"],
}
MCQ.update(
    {
        6: ["Fayzulla Xo‘jayev", "Qiziltepa", "Konstitutsiya"],
        7: ["Bobooxun Salimov", "Polvonniyoz Yusupov", "Xalq dorilfununi"],
        8: ["Mulla Abdulqahhor", "Cho‘lpon", "Junaidxon"],
        9: ["Turor Risqulov", "O‘zbekiston SSR", "Qozoqlar"],
        10: ["Yo‘ldosh Oxunboboyev", "Toshkent", "Qo‘shchi"],
    }
)
FRQ.update(
    {
        6: ["Mirzo Salimbek", "Sitorai Mohi Xosa"],
        7: ["Junaidxon", "Polvonniyoz Yusupov"],
        8: ["Anvar Posho", "Afg‘oniston"],
        9: ["Fayzulla Xo‘jayev", "Tojikiston ASSR"],
        10: ["Fayzulla Xo‘jayev", "Qoraqalpog‘iston ASSR"],
    }
)
ORDER = {
    6: ["e1", "e2", "e3"],
    7: ["e1", "e2", "e3", "e4"],
    9: ["e1", "e2"],
    10: ["e1", "e2", "e3", "e4"],
}


def lessons():
    return [l for d in load_course() if d["grade"] == 10 for l in d["lessons"]]


MCQ.update(
    {
        11: ["Sovxoz", "Natsionalizatsiya", "Majburiy mehnat posyolkalari"],
        12: ["Industrlashtirish", "Bobon Mavlonbekov", "GESlar kaskadi"],
        13: ["Artel", "Kooperatsiya", "Jahon Obidova"],
        14: ["Otajon Hoshim", "Konservatoriya", "Lotin yozuvi"],
        15: ["Botu", "Mirkomil Mirsharopov", "Shahidlar xotirasi"],
    }
)
FRQ.update(
    {
        11: ["Kolxoz", "Ukraina"],
        12: ["Toshkent to‘qimachilik kombinati", "Bobon Mavlonbekov"],
        13: ["Hujum", "Ayollar klublari"],
        14: ["O‘zFAN", "Kirill yozuvi"],
        15: ["Mahmud Hodiyev", "31-avgust"],
    }
)
ORDER.update({12: ["e1", "e2", "e3"], 14: ["e1", "e2", "e3"], 15: ["e1", "e2"]})


def answers(lesson):
    """Literal original-page values; never read grading_spec to derive a key."""
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


MCQ.update(
    {
        16: ["Polsha", "Evakuatsiya", "Usmon Yusupov"],
        17: ["Bekobod", "Sanitar poyezd", "Kartochka tizimi"],
        18: ["Zebo G‘aniyeva", "Kavaleriya", "Motamsaro ona"],
        19: ["Hamid Olimjon", "Toshkent", "Anna Axmatova"],
        20: ["Monokultura", "Guliston", "Toshkent traktor zavodi"],
    }
)
FRQ.update(
    {
        16: ["Molotov-Ribbentrop pakti", "Toshkent aviatsiya zavodi"],
        17: ["Bahri Akramova", "Qrim tatarlari"],
        18: ["Qo‘chqor Turdiyev", "Xotira va Qadrlash kuni"],
        19: ["Toshmuhammad Qori-Niyoziy", "Biz g‘alaba qozonamiz"],
        20: ["Mirzacho‘l", "Kartochka tizimi"],
    }
)
ORDER.update({16: ["e1", "e2"], 18: ["e1", "e2", "e3"], 20: ["e1", "e2", "e3"]})


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


def test_grade10_progress_replay_and_previous_grades(preview):
    client, factory = preview
    g7.complete_lesson(client, g7.course_lessons()[0])
    before = {g: client.get(P + f"/catalog?grade={g}").json() for g in [7, 8, 9]}
    catalog = client.get(P + "/catalog?grade=10").json()
    assert catalog["source_sections"] == 28
    assert catalog["implemented_sections"] == len(lessons())
    assert catalog["grade_content_complete"] is (len(lessons()) == 28)
    assert not catalog["course_ready"]
    assert start(client, lessons()[1]).status_code == 403
    for l in lessons():
        assert finish(client, l)["xp_awarded"] == 10
    assert finish(client, lessons()[0])["xp_awarded"] == 0
    for g, c in before.items():
        assert client.get(P + f"/catalog?grade={g}").json() == c
    if len(lessons()) == 28:
        done = client.get(P + "/catalog?grade=10").json()
        assert len(done["chapters"]) == 6
        assert all(c["checkpoint_state"] == "completed" for c in done["chapters"])
    with factory() as db:
        assert db.get(User, 1).xp_total == 147 + 10 * len(lessons())
        assert db.get(HistoryProgress, (1, "uzh-7-1-r1")).completed_at is not None


def test_postgres_grade10_owned_schema_replay_parallel_and_grade7_preserved(
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
    schema = "uzbekistan_history_grade10_" + secrets.token_hex(8)
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
            tokens, "JWT_SECRET", "grade10-local-pg-only-test-key-over-32-characters"
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
