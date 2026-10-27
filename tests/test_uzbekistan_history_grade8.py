"""Scanned-source keys, cross-grade ownership and progress preservation."""

from copy import deepcopy
from uuid import uuid4

import pytest
import test_uzbekistan_history_course as grade7_tests
from test_uzbekistan_history_course import P, complete_lesson, course_lessons

from services.models import User
from services.uzbekistan_history_grading import grade_answer
from services.uzbekistan_history_models import HistoryProgress
from services.uzbekistan_history_validation import load_course, validate_batch

# Literal keys independently checked on original PDF5–19; never extracted from grading_spec.
MCQ = {
    1: ["Abulxayrxon", "Tura", "Oltin O‘rda"],
    2: ["Hirot", "Abu Said Mirzo", "Andijon"],
    3: ["Umarshayx Mirzo", "Kobul", "Gulbadanbegim"],
    4: ["Samarqand", "Farg‘ona", "Marv"],
    5: ["Ubaydullaxon", "Buxoro", "Mir Arab"],
}
FRQ = {
    1: ["Sig'noq", "Buxoro"],
    2: ["Sirdaryo", "Husayn Boyqaro"],
    3: ["Qutlug' Nigorxonim", "Humoyunnoma"],
    4: ["Ismoil Safaviy", "To'lg'ama"],
    5: ["Abdullatifxon", "Navro'z Ahmadxon"],
}
ORDER = {
    1: ["e1", "e2", "e3"],
    2: ["e1", "e2", "e3", "e4"],
    3: ["e1", "e2", "e3"],
    4: ["e1", "e2", "e3", "e4"],
    5: ["e1", "e2", "e3"],
}

MCQ.update(
    {
        6: ["Muhammad Islom", "Abdulmo‘min", "Boqi Muhammad"],
        7: ["Boqi Muhammad", "Balx", "Subhonqulixon"],
        8: ["Farg‘ona vodiysi", "Abulfayzxon", "Parokandalik"],
        9: ["Devonbegi", "Parvonachi", "Amlok", "Qozikalon"],
        10: ["Qalb", "Jevachi", "Sadoq", "Yalovbardor"],
    }
)
FRQ.update(
    {
        6: ["1583", "Iskandar Sulton"],
        7: ["Zuhrabegim", "Toshkent"],
        8: ["1708", "Muhammad Hakimbiy"],
        9: ["Dodxoh", "Mirob"],
        10: ["Tavochi", "To'fandoz"],
    }
)
ORDER.update(
    {6: ["e1", "e2", "e3", "e4"], 7: ["e1", "e2", "e3", "e4"], 8: ["e1", "e2", "e3"]}
)

MCQ.update(
    {
        11: ["Mulki xos", "Tanho", "Tim"],
        12: ["Antoniy Jenkinson", "Xuroson", "Beneveni"],
        13: ["Muhammad Solih", "Subhonqulixon", "Sayido Nasafiy", "Samarqand"],
        14: ["Nodirshoh", "Mang‘itlar", "Muhammad Rahim"],
        15: ["Amir Haydar", "Miyonqol", "Qo‘qon"],
    }
)
FRQ.update(
    {
        11: ["Xiroj", "Yasoq"],
        12: ["Xoxlov", "Akbarshoh"],
        13: ["Qul Ubaydiy", "Otinoyi"],
        14: ["Shohmurod", "Doniyolbiy"],
        15: ["Din Nosirbek", "Nasrullo"],
    }
)
ORDER.update(
    {
        11: ["e1", "e2"],
        12: ["e1", "e2", "e3"],
        14: ["e1", "e2", "e3"],
        15: ["e1", "e2", "e3", "e4"],
    }
)

MCQ.update(
    {
        16: ["Qo‘shbegi", "Kitobdor", "Sadr", "Tanob"],
        17: ["Qora cherik", "Sarboz", "Vaziri harb", "Navkariya"],
        18: ["Chig‘ir", "Mutavalli", "Tanobona", "Qishloq xo‘jaligi"],
        19: ["Karvonboshi", "Orenburg", "To‘qimachilik", "Tashqi savdo davom etgan"],
        20: ["Ignatyev", "Aleksandr Byorns", "Ernazarbiy"],
    }
)
FRQ.update(
    {
        16: ["Mirob", "Kichik inoq"],
        17: ["1837", "Sarbozxona"],
        18: ["Xiroj", "Zakot"],
        19: ["Samarqand", "Buxoro olachasi"],
        20: ["Murkford", "Ashtarxon"],
    }
)
ORDER[20] = ["e2", "e3", "e1"]

MCQ.update({21:['Muhammadniyoz Nishotiy','Ahmad Donish','Shahrisabz'],22:['Elbarsxon','Urganch','Arabshohiylar','Shahar nomi'],23:['Arab Muhammadxon','Anushaxon','Nodirshoh'],24:['Muhammad Amin','Eltuzar','Talash yerlar'],25:['Mehtar','Shig‘ovul','Yasovulboshi','Oliy Kengash']})
FRQ.update({21:['Shashmaqom','Juvayniy'],22:['Umar','Amudaryo'],23:['Inoq','Bekovich-Cherkasskiy'],24:['Muhammad Rahimxon 1','Toshhovli'],25:['Muftiy','Xon navkarlari']})
ORDER.update({21:['e1','e2','e3'],23:['e1','e2','e3'],24:['e1','e2','e3','e4']})

MCQ.update({26:['Bevatan','Dishan qal’a','Otliq','Begar'],27:['V. Perovskiy','Majburiyatlar akti','Marv'],28:['Munis','Abulg‘oziy Bahodirxon','Xattot','Munis'],29:['Arxiv hujjatlari','Toshkent','Vamberi'],30:['Abdullaxon II','Oydosbiy','Ovul']})
FRQ.update({26:["Ichan qal'a","Salg'ut"],27:['Danilevskiy','Bojxona'],28:['Ogahiy','Vaqf'],29:['Muravyov','Peterburg'],30:['Biylarog‘asi','Janadaryo']})
ORDER.update({27:['e2','e3','e1'],29:['e3','e1','e2'],30:['e1','e2']})

MCQ.update({31:['Ajiniyoz','Jiyen Jirov','Xo‘jayli','Og‘zaki ijod'],32:['Shohruxbiy','Abdurahimbiy','Abdulkarimbiy'],33:['Olimxon','Madalixon','Sheralixon'],34:['Mingboshi','Devonbegi','Mirza','Ulamo'],35:['Olimxon','Sipoh','Yovar','Qo‘rboshi']})
FRQ.update({31:['Berdaq','Bo‘zatov'],32:['Tepa qo‘rg‘on','1776'],33:['1805','Musulmonqul'],34:['Dasturxonchi','Umaro'],35:['Miltiq puli','Botmon']})
ORDER.update({32:['e1','e2'],33:['e1','e2','e3','e4']})


def lessons():
    return [l for d in load_course() if d["grade"] == 8 for l in d["lessons"]]


def answers(lesson):
    result = []
    mc = fr = 0
    seq = lesson["sequence"]
    for q in lesson["assessments"]:
        if q["response_kind"] == "concept_selection":
            result.append(
                {
                    "choice_id": next(
                        o["id"]
                        for o in q["public"]["options"]
                        if o["label"] == MCQ[seq][mc]
                    )
                }
            )
            mc += 1
        elif q["response_kind"] == "short_text":
            result.append({"value": FRQ[seq][fr]})
            fr += 1
        else:
            result.append({"order": ORDER[seq]})
    return result


@pytest.mark.parametrize("seq", range(1, 36))
def test_image_checked_independent_keys_wrong_choices_and_aliases(seq):
    lesson = lessons()[seq - 1]
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        assert grade_answer(q["grading_spec"], answer) == "correct"
        if q["response_kind"] == "concept_selection":
            for option in q["public"]["options"]:
                assert grade_answer(q["grading_spec"], {"choice_id": option["id"]}) == (
                    "correct" if option["id"] == answer["choice_id"] else "incorrect"
                )
        elif q["response_kind"] == "short_text":
            assert (
                grade_answer(q["grading_spec"], {"value": "boshqa javob"})
                == "incorrect"
            )
        else:
            assert (
                grade_answer(q["grading_spec"], {"order": answer["order"][::-1]})
                == "incorrect"
            )
        for ref in q["source_refs"]:
            assert ref["verification"] == "original_image_checked_ocr_locator_only"
            assert len(ref["page_image_sha256"]) == len(ref["pdf_pages"])


@pytest.mark.parametrize("case", ["missing_pixels", "native_only", "unverified_pixels"])
def test_watermark_or_ocr_cannot_substitute_for_scanned_image_evidence(case):
    d = deepcopy(next(d for d in load_course() if d["grade"] == 8))
    ref = d["lessons"][0]["facts"][next(iter(d["lessons"][0]["facts"]))]["source_refs"][
        0
    ]
    if case == "missing_pixels":
        ref.pop("page_image_sha256")
    elif case == "native_only":
        ref["verification"] = "original_text_and_image_checked"
    else:
        ref["page_image_sha256"] = ["0" * 64] * len(ref["pdf_pages"])
    with pytest.raises(ValueError):
        validate_batch(d)


def start(client, seq, request=None):
    return client.post(
        f"{P}/lessons/uzh-8-{seq}-r1/start",
        json={"assessment_version": 2, "request_id": request or str(uuid4())},
    )


def finish(client, lesson):
    a = start(client, lesson["sequence"])
    assert a.status_code == 200, a.text
    a = a.json()
    encoded = str(a)
    assert "grading_spec" not in encoded and "accepted_answers" not in encoded
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        body = {"assessment_version": 2, "assessment_key": q["key"], "answer": answer}
        response = client.post(f"{P}/attempts/{a['attempt_id']}/answers", json=body)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(f"{P}/attempts/{a['attempt_id']}/answers", json=body).json()
            == response.json()
        )
    response = client.post(
        f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}
    )
    assert response.status_code == 200, response.text
    assert (
        client.post(
            f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}
        ).json()
        == response.json()
    )
    return a, response.json()


@pytest.fixture
def history_preview(tmp_path, monkeypatch):
    yield from grade7_tests.preview.__wrapped__(tmp_path, monkeypatch)


def test_grade8_catalogue_and_separate_prerequisites_preserve_grade7(history_preview):
    client, factory = history_preview
    # Existing first grade7 completion must survive import, grade selection and grade8 XP.
    complete_lesson(client, course_lessons()[0])
    g7_before = client.get(P + "/catalog?grade=7").json()
    catalog = client.get(P + "/catalog?grade=8").json()
    assert catalog["book"]["isbn"] == "978-9943-22-371-4"
    assert catalog["source_sections"] == 41 and catalog["implemented_sections"] == len(
        lessons()
    )
    assert catalog["blocked_grades"] == [] and not catalog["grade_content_complete"]
    assert start(client, 2).status_code == 403
    for lesson in lessons():
        _, r = finish(client, lesson)
        assert r["xp_awarded"] == 10
    _, r = finish(client, lessons()[0])
    assert r["xp_awarded"] == 0
    g7_after = client.get(P + "/catalog?grade=7").json()
    assert [
        (l["key"], l["state"], l["best_score_pct"]) for l in g7_after["lessons"]
    ] == [(l["key"], l["state"], l["best_score_pct"]) for l in g7_before["lessons"]]
    with factory() as db:
        assert db.get(User, 1).xp_total == 147 + 10 * len(lessons())
        assert db.get(HistoryProgress, (1, "uzh-7-1-r1")) is not None


def test_postgres_grade8_owned_schema_replay_parallel_and_grade7_preserved(monkeypatch):
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
    schema = "uzbekistan_history_grade8_" + secrets.token_hex(8)
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
            assert import_course(db)["created"] == 42 + len(lessons())
            assert import_course(db) == {"created": 0, "skipped": 42 + len(lessons())}
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("UZBEKISTAN_HISTORY_PREVIEW_ENABLED", "true")
        monkeypatch.setattr(
            tokens, "JWT_SECRET", "grade8-local-pg-only-test-key-over-32-characters"
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
            complete_lesson(client, course_lessons()[0])
            for lesson in lessons()[:-1]:
                _, result = finish(client, lesson)
                assert result["xp_awarded"] == 10
            last = lessons()[-1]
            attempts = [start(client, last["sequence"]).json() for _ in range(2)]
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
            _, result = finish(client, lessons()[0])
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


def test_mixed_script_ocr_lookalike_is_blocked_but_cyrillic_word_is_not_mislabelled():
    from services.uzbekistan_history_validation import reviewed_text_scripts

    assert reviewed_text_scripts("O‘zbekiston Кирилл")
    assert not reviewed_text_scripts(
        "Florо"
    )  # Last character is Cyrillic, not Latin o.
    d = deepcopy(next(d for d in load_course() if d["grade"] == 8))
    d["lessons"][0]["cards"][0]["body"] += " Florо"
    with pytest.raises(ValueError, match="mixed_script_word_requires_review"):
        validate_batch(d)


@pytest.mark.parametrize(
    "case", ["content", "different_person", "source", "unverified"]
)
def test_spelling_reviews_cannot_add_new_historical_keys(case):
    from services.uzbekistan_history_spelling import load_reviews, validate_reviews

    reviews = deepcopy(load_reviews())
    validate_reviews(load_course(), reviews)
    if case == "content":
        reviews[0]["lesson_content_sha256"] = "0" * 64
    elif case == "different_person":
        reviews[0]["aliases"] = ["Amir Haydar"]
    elif case == "source":
        reviews[0]["source_refs"] = []
    else:
        reviews[0]["verification"] = "ocr_only"
    with pytest.raises(ValueError):
        validate_reviews(load_course(), reviews)


def test_original_joined_name_is_accepted_only_in_new_reviewed_snapshots(
    history_preview,
):
    from services.models import StudySession

    client, factory = history_preview
    for lesson in lessons()[:14]:
        finish(client, lesson)
    lesson = lessons()[14]
    old = start(client, 15).json()
    with factory.begin() as db:
        row = db.get(StudySession, old["attempt_id"])
        snapshot = deepcopy(row.questions)
        for q in snapshot["assessments"]:
            if q["key"] == lesson["assessments"][3]["key"]:
                q["grading_spec"]["aliases"] = ["Din Nosirbek"]
                q["grading_spec"].pop("spelling_review_sha256", None)
        row.questions = snapshot
    old_response = None
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        if q == lesson["assessments"][3]:
            answer = {"value": "Dinnosirbek"}
        response = client.post(
            f"{P}/attempts/{old['attempt_id']}/answers",
            json={
                "assessment_version": 2,
                "assessment_key": q["key"],
                "answer": answer,
            },
        )
        assert response.status_code == 200
        if q == lesson["assessments"][3]:
            old_response = response.json()
            assert not old_response["is_correct"]
    r = client.post(
        f"{P}/attempts/{old['attempt_id']}/complete", json={"assessment_version": 2}
    ).json()
    assert r["score"] == 5 and r["xp_awarded"] == 10
    fresh = start(client, 15).json()
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        if q == lesson["assessments"][3]:
            answer = {"value": "Dinnosirbek"}
        response = client.post(
            f"{P}/attempts/{fresh['attempt_id']}/answers",
            json={
                "assessment_version": 2,
                "assessment_key": q["key"],
                "answer": answer,
            },
        )
        assert response.status_code == 200 and response.json()["is_correct"]
    r = client.post(
        f"{P}/attempts/{fresh['attempt_id']}/complete", json={"assessment_version": 2}
    ).json()
    assert r["score"] == 6 and r["xp_awarded"] == 0
    replay = client.post(
        f"{P}/attempts/{old['attempt_id']}/answers",
        json={
            "assessment_version": 2,
            "assessment_key": lesson["assessments"][3]["key"],
            "answer": {"value": "Dinnosirbek"},
        },
    )
    assert replay.json() == old_response
    with factory() as db:
        assert db.get(User, 1).xp_total == 287


@pytest.mark.parametrize('case',['content','source'])
def test_new_snapshot_spelling_review_is_bound_to_imported_question(case):
    from services.uzbekistan_history_sources import digest
    from services.uzbekistan_history_spelling import new_attempt_spec
    lesson=lessons()[14];question=lesson['assessments'][3]
    with pytest.raises(ValueError):
        new_attempt_spec(lesson['key'],'0'*64 if case=='content' else digest(lesson),question['key'],question['grading_spec'],[] if case=='source' else question['source_refs'])
