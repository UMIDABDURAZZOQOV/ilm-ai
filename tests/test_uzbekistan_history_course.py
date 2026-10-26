"""Independent source meaning, objective aliases and isolated API/XP regression."""

from copy import deepcopy
from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from routers.uzbekistan_history_preview import router
from services import db as database
from services import tokens
from services.models import Base, StudySession, User
from services.study import utcnow
from services.uzbekistan_history_curriculum import import_course
from services.uzbekistan_history_grading import grade_answer, normalized_text
from services.uzbekistan_history_models import (
    HistoryBase,
    HistoryProgress,
)
from services.uzbekistan_history_validation import (
    chronology_bounds,
    load_course,
    validate_batch,
    validate_ref,
)

P = "/preview/uzbekistan-history/v2"
MCQ = {
    1: [
        "Dehqon",
        "Kashovar",
        "Hunarmandchilik va savdo",
        "Sug‘orma dehqonchilik maydonlarining kengayishi",
    ],
    2: ["Afrig‘iylar", "Zarafshon vohasi", "Kidar", "Ichki va tashqi savdo aloqalari"],
    3: [
        "Ipak yo‘li",
        "Sosoniylarning kumush tangalari",
        "Sosoniylarning eftallarga boj to‘lashi",
        "Sug‘d tili",
    ],
    4: ["552-yil", "Qabilalar ittifoqi", "Eron sosoniylari", "G‘arbga"],
    5: ["Buxoro", "618–630-yillar", "Tudunlar", "Sug‘d savdogarlari"],
}
FRQ = {
    1: ["kadivar", "CHOKAR."],
    2: ["Kat shahri", "Balx"],
    3: ["Pero'z", "Sug'd tili"],
    4: ["Bumin", "Yabg'u xoqon"],
    5: ["Abruy", "El Arslon"],
}
ORDER = {2: ["e1", "e2"], 3: ["e1", "e2", "e3"], 4: ["e1", "e2", "e3"], 5: ["e2", "e1"]}

MCQ.update({
    6: ["Boj to‘lash va ichki boshqaruvning saqlanishi", "Zarafshon va Qashqadaryo", "Koson, Axsikat, Quva", "Ko‘handiz yoki ark"],
    7: ["Sug‘d va xorazm yozuvlari", "Charm, yog‘och va sopol", "Varaxsha", "Bir nechta diniy an’ana mavjud bo‘lgan"],
    8: ["Daryoning narigi tomoni", "Marv", "Buxoro", "Iqto"],
    9: ["Jizya", "Xiroj", "Dastlabki yillarda", "Quva va Afrosiyob"],
    10: ["G‘urak va Divashtich", "Oq libos", "Niqobdor", "Rofe ibn Lays"],
})
FRQ.update({6: ["Tunkat", "Rabot"], 7: ["Mug' qal'asi", "Choch raqsi"],
    8: ["Qutayba ibn Muslim", "G'urak"], 9: ["Zakot", "Jizya"],
    10: ["Hoshim ibn Hakim", "Som qal'asi"]})
ORDER.update({8: ["e1", "e2", "e3"], 10: ["e1", "e2", "e3"]})

MCQ.update({
    11: ["Abu Muslim", "Abbosiylar", "Talos vodiysi", "Vazir ul-vuzaro"],
    12: ["Suyob", "Yangikent", "Tohir ibn Husayn", "Nishopur"],
    13: ["Samarqand", "Ismoil Somoniy", "Buxoro", "Farjak madrasasi"],
    14: ["Samarqand", "Chek", "Mulki sultoniy", "Vaqf yerlari"],
    15: ["G‘azna", "Xorazm", "Firdavsiy", "Rais"],
})
FRQ.update({11: ["Amirul-umaro", "Devon al mashriq"], 12: ["Xutba", "Ya'qub ibn Lays"],
    13: ["Vazir", "Hojib"], 14: ["Falslar", "Qo'shchi"], 15: ["Alptegin", "Abu Rayhon Beruniy"]})
ORDER.update({n: ["e1", "e2", "e3"] for n in [11, 12, 13, 15]})

MCQ.update({
    16: ["Horun Bug‘roxon", "Nasr Eloqxon", "Bolasog‘un va Samarqand", "Qatvon"],
    17: ["Ma’mun ibn Muhammad", "Otsiz", "Takash", "Xorazmshoh"],
    18: ["Temuchin", "Bahouddin Roziy", "Buxoro", "Inolchiq"],
    19: ["Kuchlarni turli shaharlarga bo‘lish", "O‘tror", "Temur Malik", "Urganch"],
    20: ["Jaloliddin Manguberdi", "Valiyon qal’asi", "Parvon", "Sultonband"],
})
FRQ.update({16: ["Iqto", "Dehqon"], 17: ["Urganch", "Anushtegin"],
    18: ["Mahmud Yalavoch", "O'tror"], 19: ["Temur Malik", "Najmiddin Kubro"],
    20: ["Hind daryosi", "Ashura oroli"]})
ORDER.update({n: ["e1", "e2", "e3"] for n in [16, 17, 18, 19]})
ORDER[20] = ["e1", "e2"]

MCQ.update({
    21: ["Tabriz", "Garni", "Isfahon", "Arzinjon"],
    22: ["Nasaviy", "Maqsud Shayxzoda", "Ibn al-Asir", "Tarixiy drama"],
    23: ["Xo‘jand", "Qopchur", "Kalon", "Torob"],
    24: ["Ma’sudbek", "Kebek", "Mulki devon", "Suyurg‘ol"],
    25: ["Movarounnahr, Xorazm va Yettisuv", "Qovunchi madaniyati", "Sug‘d va turk tillari", "Etnik jarayon"],
})
FRQ.update({21: ["Xalifa Nosir", "G'iyosiddin Pirshoh"], 22: ["Juvayniy", "Jaloliddin Manguberdi ordeni"],
    23: ["Mahmud Torobiy", "Barot"], 24: ["Yomlar", "Qarshi"], 25: ["Turkiston"]})
ORDER.update({21: ["e1", "e2", "e3", "e4"], 22: ["e1", "e2", "e3", "e4"],
    23: ["e1", "e2"], 24: ["e1", "e2", "e3"]})

MCQ.update({
    26: ["Bag‘dod", "Al-Xorazmiy", "Ahmad al-Farg‘oniy", "Abu Nasr Farobiy"],
    27: ["Mahmud az-Zamaxshariy", "Yusuf Xos Hojib", "Mahmud Koshg‘ariy", "Ahmad Yugnakiy"],
    28: ["Imom al-Buxoriy", "Abu Mansur al-Moturidiy", "Burhoniddin al-Marg‘inoniy", "Fiqh"],
    29: ["Xonbandi", "Xattotlik", "Olti maqom", "Yog‘och sinch"],
    30: ["Xoja Ilg‘or", "Dorug‘a", "Loy jangi", "Samarqand"],
})
FRQ.update({26: ["Ibn Sino", "Beruniy"], 27: ["Xos Hojib", "Koshg'ar"],
    28: ["Ahmad Yassaviy", "Bahouddin Naqshband"], 29: ["Ismoil Somoniy", "12 asr"],
    30: ["Mavlonozoda", "Abu Bakr Kalaviy"]})
ORDER[30] = ["e1", "e2", "e3", "e4"]

MCQ.update({
    31: ["Movarounnahr amiri", "Samarqand", "1372-yil", "Hirot"],
    32: ["Devonbegi", "Tavochi", "Tuman", "Suyurg‘ol"],
    33: ["Barquq", "Klavixo", "Mironshoh", "Samarqand"],
    34: ["I.M. Mo‘minov", "Xristofor Marlo", "Toshkent", "1995-yil"],
    35: ["Pirmuhammad", "Xalil Sulton", "Hirot", "Samarqand"],
})
FRQ.update({31: ["Sayyid Baraka", "Bayroq va nog'ora"], 32: ["Hazora", "Qo'shun"],
    33: ["Muhammad Qozi", "Karl VI"], 34: ["Perondino", "Sevilya"], 35: ["Qora Yusuf", "Xudoydod"]})
ORDER.update({31: ["e1", "e2", "e3"], 32: ["e1", "e2", "e3"],
    33: ["e1", "e2", "e3", "e4"], 34: ["e1", "e2", "e3", "e4", "e5"],
    35: ["e1", "e2", "e3", "e4"]})

MCQ.update({
    36: ["Shohrux", "1412-yil", "Tarnob", "Issiqko‘l"],
    37: ["Abulxayrxon", "Abu Said", "Sulton Husayn Boyqaro", "Muhrdorlik"],
    38: ["Banno", "Ustoz", "Tarxonlik yorlig‘i", "Hudud va savdo yo‘li alohida belgilangan"],
    39: ["Saroymulkxonim", "Geometriya", "Shamsiddin Muhammad Xavofiy", "Buxoro"],
    40: ["Samarqand", "Ziji jadidi Ko‘ragoniy", "G‘iyosiddin Jamshid", "Rasadxona"],
})
FRQ.update({36: ["Abdullatif", "Muhammad Miskin"], 37: ["Ubaydulloh Ahror", "Fayzulloh Abullays"],
    38: ["Fulusi adliya", "Begor"], 39: ["Sanad", "Qozizoda Rumiy"],
    40: ["Alouddin Ali Qushchi", "To'rt ulus tarixi"]})
ORDER.update({36: ["e1", "e2", "e3", "e4", "e5", "e6"], 37: ["e1", "e2", "e3"],
    39: ["e1", "e2", "e3"]})


MCQ.update({
    41: ["Durbek", "Alisher Navoiy", "Mirxond", "Xondamir"],
    42: ["Lavvohlik", "Sahhoflik", "Nasta’liq", "Kamoliddin Behzod"],
})
FRQ.update({41: ["Abdurahmon Jomiy", "Lutfiy"],
    42: ["Mahmud Muzahhib", "Sultonali Mashhadiy"]})
ORDER[42] = ["e1", "e2", "e3"]


def course_lessons():
    return [l for d in load_course() for l in d["lessons"]]


def answers(lesson):
    result = []
    mc = fr = 0
    for q in lesson["assessments"]:
        kind = q["response_kind"]
        seq = lesson["sequence"]
        if kind == "concept_selection":
            label = MCQ[seq][mc]
            mc += 1
            result.append(
                {
                    "choice_id": next(
                        o["id"] for o in q["public"]["options"] if o["label"] == label
                    )
                }
            )
        elif kind == "short_text":
            result.append({"value": FRQ[seq][fr]})
            fr += 1
        else:
            result.append({"order": ORDER[seq]})
    return result


@pytest.mark.parametrize("seq", range(1, 43))
def test_independent_source_answer_keys(seq):
    l = course_lessons()[seq - 1]
    for q, a in zip(l["assessments"], answers(l)):
        assert grade_answer(q["grading_spec"], a) == "correct"
        if q["response_kind"] == "concept_selection":
            for o in q["public"]["options"]:
                assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                    "correct" if o["id"] == a["choice_id"] else "incorrect"
                )
        elif q["response_kind"] == "short_text":
            assert (
                grade_answer(q["grading_spec"], {"value": "boshqa javob"})
                == "incorrect"
            )
        else:
            assert (
                grade_answer(q["grading_spec"], {"order": a["order"][::-1]})
                == "incorrect"
            )


@pytest.mark.parametrize(
    "text", ["__import__('os')", "kat\u200b", "kat/2", "x" * 121, "<script>"]
)
def test_bounded_alias_input_never_evaluates(text):
    with pytest.raises(ValueError):
        normalized_text(text)


def test_reviewed_spelling_is_not_fuzzy_or_essay_grading():
    assert normalized_text(" SUG‘D TILI. ") == normalized_text("sug'd tili")
    assert normalized_text("To‘ng") != normalized_text("Tong")
    q = load_course()[0]["lessons"][4]["assessments"][5]
    assert grade_answer(q["grading_spec"], {"value": "El Arslon"}) == "correct"
    assert grade_answer(q["grading_spec"], {"value": "Sheri Kishvar"}) == "correct"
    assert grade_answer(q["grading_spec"], {"value": "Sheri Kishva"}) == "incorrect"
    assert all(
        r["evaluation"] == "self_or_teacher_review_only"
        for l in load_course()[0]["lessons"]
        for r in l["reflections"]
    )


def test_century_notation_has_frozen_legacy_and_bounded_new_normalization():
    spec = deepcopy(course_lessons()[28]["assessments"][-1]["grading_spec"])
    assert grade_answer(spec, {"value": "12"}) == "incorrect"  # frozen legacy
    spec["normalization_revision"] = 2
    for value in ["12", "XII", "Ⅻ", "12 asr", "XII-asr"]:
        assert grade_answer(spec, {"value": value}) == "correct"
    for value in ["13", "IIIIIIIIIIII", "120", "0", "XII yil"]:
        assert grade_answer(spec, {"value": value}) == "incorrect"
    name = deepcopy(course_lessons()[0]["assessments"][4]["grading_spec"])
    name["normalization_revision"] = 2
    assert grade_answer(name, {"value": "12"}) == "incorrect"


def test_legacy_century_answer_replay_survives_new_attempt_normalization(preview):
    c, factory = preview
    for lesson in course_lessons()[:28]:
        complete_lesson(c, lesson)
    lesson = course_lessons()[28]
    old = start(c, 29).json()
    with factory.begin() as db:
        row = db.get(StudySession, old["attempt_id"])
        snapshot = deepcopy(row.questions)
        for q in snapshot["assessments"]:
            q["grading_spec"].pop("normalization_revision", None)
        row.questions = snapshot
    saved = None
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        if q == lesson["assessments"][-1]:
            answer = {"value": "12"}
        body = {"assessment_version": 2, "assessment_key": q["key"], "answer": answer}
        r = c.post(f"{P}/attempts/{old['attempt_id']}/answers", json=body)
        assert r.status_code == 200
        saved = r.json()
    assert saved is not None and not saved["is_correct"]
    old_result = c.post(f"{P}/attempts/{old['attempt_id']}/complete", json={"assessment_version": 2}).json()
    assert old_result["score"] == 5 and old_result["xp_awarded"] == 10
    fresh = start(c, 29).json()
    for q, answer in zip(lesson["assessments"], answers(lesson)):
        if q == lesson["assessments"][-1]:
            answer = {"value": "XII"}
        r = c.post(f"{P}/attempts/{fresh['attempt_id']}/answers", json={
            "assessment_version": 2, "assessment_key": q["key"], "answer": answer,
        })
        assert r.status_code == 200 and r.json()["is_correct"]
    new_result = c.post(f"{P}/attempts/{fresh['attempt_id']}/complete", json={"assessment_version": 2}).json()
    assert new_result["score"] == 6 and new_result["xp_awarded"] == 0
    q = lesson["assessments"][-1]
    replay = c.post(f"{P}/attempts/{old['attempt_id']}/answers", json={
        "assessment_version": 2, "assessment_key": q["key"], "answer": {"value": "12"},
    })
    assert replay.status_code == 200 and replay.json() == saved
    with factory() as db:
        assert db.get(StudySession, old["attempt_id"]).response == old_result
        assert db.get(User, 1).xp_total == 427


def test_chronology_intervals_no_display_year_zero_or_elapsed_year_claim():
    assert chronology_bounds({"era": "BCE", "start_year": 2, "end_year": 1}) == (-2, -1)
    assert chronology_bounds({"era": "CE", "start_year": 1, "end_year": 1}) == (1, 1)
    for t in [
        {"era": "CE", "start_year": 0, "end_year": 1},
        {"era": "BCE", "start_year": 1, "end_year": 2},
    ]:
        with pytest.raises(ValueError):
            chronology_bounds(t)


@pytest.mark.parametrize("case", ["hash", "marker", "title", "future"])
def test_prior_context_is_pinned_and_future_context_stays_blocked(case):
    from services.uzbekistan_history_sources import digest, load_catalog

    book = load_catalog()["books"][0]
    lesson = course_lessons()[39]
    topic = book["topics"][39]
    ref = deepcopy(next(r for r in lesson["source_refs"] if r["topic_id"] != topic["id"]))
    validate_ref(ref, book, topic, lesson["facts"])
    if case == "hash":
        ref["source_topic_sha256"] = "0" * 64
    elif case == "marker":
        ref["cross_topic_reference"] = "not_reviewed"
    elif case == "title":
        ref["source_title"] = "incorrect source paragraph"
    else:
        future = book["topics"][40]
        ref.update(topic_id=future["id"], chapter_id=future["chapter_id"],
                   source_topic_sha256=digest(future), source_title=future["title"],
                   pdf_pages=[151], printed_pages=[151],
                   native_text_sha256=[book["pages"][150]["native_text_sha256"]])
    with pytest.raises(ValueError, match="unreviewed_or_future_context"):
        validate_ref(ref, book, topic, lesson["facts"])


@pytest.mark.parametrize(
    "case",
    [
        "unverified_alias",
        "untaught",
        "cross_boundary",
        "future_page",
        "wrong_order",
        "wrong_source_hash",
        "interpretation_key",
        "interpreted_chronology",
        "duplicate_label",
        "feedback_key",
        "missing_card_refs",
        "missing_example_refs",
        "missing_root_refs",
        "mislinked_example",
    ],
)
def test_source_tamper_fails_closed(case):
    d = deepcopy(load_course()[0])
    l = d["lessons"][0]
    q = l["assessments"][4]
    if case == "unverified_alias":
        q["grading_spec"]["aliases"].append("yangi taxmin")
    elif case == "untaught":
        q["fact_ids"] = ["not_taught"]
    elif case == "cross_boundary":
        q["source_refs"][0]["end_before_y"] = 0
    elif case == "future_page":
        q["source_refs"][0]["pdf_pages"] = [9]
    elif case == "wrong_order":
        d["lessons"][1]["assessments"][-1]["grading_spec"]["expected"] = ["e2", "e1"]
    elif case == "wrong_source_hash":
        q["source_refs"][0]["sha256"] = "0" * 64
    elif case == "interpretation_key":
        next(
            f
            for f in l["facts"].values()
            if f["assertion_kind"] == "source_interpretation"
        )["accepted_answers"] = ["one opinion"]
    elif case == "interpreted_chronology":
        dated = next(f for f in d["lessons"][1]["facts"].values() if f.get("time", {}).get("start_year") == 456)
        dated["assertion_kind"] = "source_interpretation"
        dated["accepted_answers"] = []
    elif case == "missing_card_refs":
        l["cards"][0]["source_refs"] = []
    elif case == "missing_example_refs":
        l["examples"][0]["source_refs"] = []
    elif case == "missing_root_refs":
        l["source_refs"] = []
    elif case == "mislinked_example":
        example = l["examples"][0]
        unrelated = next(f for fid, f in l["facts"].items() if fid not in example["fact_ids"])
        example["source_refs"] = deepcopy(unrelated["source_refs"])
    elif case == "feedback_key":
        l["assessments"][0]["grading_spec"]["verified_answer"] = "unverified claim"
    elif case == "duplicate_label":
        options = l["assessments"][0]["public"]["options"]
        options[1]["label"] = options[0]["label"]
    with pytest.raises(ValueError):
        validate_batch(d)


@pytest.fixture
def preview(tmp_path, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("UZBEKISTAN_HISTORY_PREVIEW_ENABLED", "true")
    engine = create_engine(
        f"sqlite:///{tmp_path / 'uzbekistan_history_staging.db'}",
        connect_args={"check_same_thread": False, "timeout": 30},
    )

    @event.listens_for(engine, "connect")
    def fk(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    HistoryBase.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory.begin() as db:
        db.add_all(
            [
                User(
                    id=1,
                    name="QA",
                    email="uzh-qa@example.test",
                    xp_total=137,
                    streak_days=3,
                ),
                User(id=2, name="QA2", email="uzh-qa2@example.test", xp_total=0),
            ]
        )
        assert import_course(db) == {"created": 42, "skipped": 0}
        assert import_course(db) == {"created": 0, "skipped": 42}
    app = FastAPI()
    app.include_router(router)

    def db_override():
        with factory() as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise

    app.dependency_overrides[database.get_db] = db_override
    monkeypatch.setattr(
        tokens, "JWT_SECRET", "history-tests-only-key-longer-than-32-characters"
    )
    client = TestClient(app)
    client.headers["Authorization"] = "Bearer " + tokens.create_access_token(1)
    yield client, factory
    engine.dispose()


def start(client, seq=1, request=None):
    return client.post(
        f"{P}/lessons/uzh-7-{seq}-r1/start",
        json={"assessment_version": 2, "request_id": request or str(uuid4())},
    )


def complete_lesson(client, l, request=None):
    response = start(client, l["sequence"], request)
    assert response.status_code == 200, response.text
    a = response.json()
    payload = str(a)
    for secret in ["grading_spec", "aliases", "accepted_answers", "expected", "facts"]:
        assert secret not in payload
    for q, answer in zip(l["assessments"], answers(l)):
        body = {"assessment_version": 2, "assessment_key": q["key"], "answer": answer}
        r = client.post(f"{P}/attempts/{a['attempt_id']}/answers", json=body)
        assert r.status_code == 200 and r.json()["is_correct"], r.text
        assert (
            client.post(f"{P}/attempts/{a['attempt_id']}/answers", json=body).json()
            == r.json()
        )
    r = client.post(
        f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}
    )
    assert r.status_code == 200, r.text
    assert (
        client.post(
            f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}
        ).json()
        == r.json()
    )
    return a, r.json()


def test_real_api_all_forty_two_sources_xp_replay_and_legacy_preservation(preview):
    c, f = preview
    catalog = c.get(P + "/catalog").json()
    assert catalog["subject"] == "ozbekiston_tarixi" and catalog["book"]["grade"] == 7
    assert catalog["lessons"][0]["source_numbers"] == [1]
    assert catalog["book"]["isbn"] == "978-9943-26-656-8"
    assert catalog["source_sections"] == 42 and catalog["implemented_sections"] == 42
    assert catalog["available_grades"] == [7] and catalog["blocked_grades"] == [8]
    assert [r["state"] for r in catalog["lessons"]] == ["available"] + ["locked"] * 41
    assert start(c, 2).status_code == 403
    for l in course_lessons():
        _, result = complete_lesson(c, l)
        assert result["xp_awarded"] == 10
    _, again = complete_lesson(c, load_course()[0]["lessons"][0])
    assert again["xp_awarded"] == 0 and again["xp_total"] == 557
    cat = c.get(P + "/catalog").json()
    assert not cat["course_complete"] and cat["grade_content_complete"]
    assert not cat["course_ready"]
    assert cat["chapters"][0]["checkpoint_state"] == "completed"
    assert cat["chapters"][1]["checkpoint_state"] == "completed"
    assert cat["chapters"][2]["checkpoint_state"] == "completed"
    assert cat["chapters"][3]["checkpoint_state"] == "completed"
    assert cat["chapters"][4]["checkpoint_state"] == "completed"
    assert cat["chapters"][5]["checkpoint_state"] == "completed"
    with f() as db:
        assert (
            db.get(User, 1).xp_total == 557 and db.query(HistoryProgress).count() == 42
        )


def test_account_isolation_request_identity_and_expiry(preview):
    c, f = preview
    request = str(uuid4())
    a = start(c, 1, request).json()
    assert start(c, 1, request).json() == a
    assert start(c, 2, request).status_code == 409
    old = c.headers["Authorization"]
    c.headers["Authorization"] = "Bearer " + tokens.create_access_token(2)
    assert (
        c.post(
            f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}
        ).status_code
        == 404
    )
    c.headers["Authorization"] = old
    with f.begin() as db:
        db.get(StudySession, a["attempt_id"]).started_at = utcnow() - timedelta(
            hours=25
        )
    assert start(c, 1, request).status_code == 409


def test_format_retry_alias_replay_and_order_enforced(preview):
    c, _ = preview
    a = start(c).json()
    qs = load_course()[0]["lessons"][0]["assessments"]

    def send(q, answer):
        return c.post(
            f"{P}/attempts/{a['attempt_id']}/answers",
            json={
                "assessment_version": 2,
                "assessment_key": q["key"],
                "answer": answer,
            },
        )

    assert send(qs[1], answers(load_course()[0]["lessons"][0])[1]).status_code == 409
    assert send(qs[0], {"choice_id": "forged"}).status_code == 422
    for q, ans in zip(qs[:4], answers(load_course()[0]["lessons"][0])[:4]):
        assert send(q, ans).json()["is_correct"]
    assert send(qs[4], {"value": "<script>"}).status_code == 422
    first = send(qs[4], {"value": "Kadivar"})
    assert first.json()["is_correct"]
    assert send(qs[4], {"value": "KADIVARLAR."}).json() == first.json()
    assert send(qs[4], {"value": "dehqon"}).status_code == 409


def test_gate_and_wrong_subject_keys(preview, monkeypatch):
    c, _ = preview
    assert (
        c.post(
            P + "/lessons/physics-6-section-1-r1/start",
            json={"assessment_version": 2, "request_id": str(uuid4())},
        ).status_code
        == 404
    )
    assert c.get(P + "/catalog?grade=6").status_code == 422
    assert c.get(P + "/catalog?grade=9").json()["lessons"] == []
    monkeypatch.setenv("ENVIRONMENT", "production")
    assert c.get(P + "/catalog").status_code == 404


def test_missing_grade8_is_not_an_empty_verified_book(preview):
    c, _ = preview
    d = c.get(P + "/catalog?grade=8").json()
    assert d["book"] is None and d["source_sections"] is None
    assert d["lessons"] == [] and d["source_status"] == "blocked_missing_source"
    assert not d["grade_content_complete"] and not d["course_ready"]


def test_failed_lesson_never_unlocks_or_awards_xp_and_client_cannot_claim_correctness(preview):
    c, factory = preview
    lesson = course_lessons()[0]
    a = start(c).json()
    q = lesson["assessments"][0]
    forged = c.post(f"{P}/attempts/{a['attempt_id']}/answers", json={
        "assessment_version": 2, "assessment_key": q["key"],
        "answer": {**answers(lesson)[0], "is_correct": True},
    })
    assert forged.status_code == 422
    for q, correct in zip(lesson["assessments"], answers(lesson)):
        wrong = {"choice_id": next(o["id"] for o in q["public"]["options"]
                                  if o["id"] != correct["choice_id"])} if q["response_kind"] == "concept_selection" else {"value": "boshqa atama"}
        r = c.post(f"{P}/attempts/{a['attempt_id']}/answers", json={
            "assessment_version": 2, "assessment_key": q["key"], "answer": wrong,
        })
        assert r.status_code == 200 and not r.json()["is_correct"]
        assert r.json()["feedback"] and r.json()["source_refs"]
    r = c.post(f"{P}/attempts/{a['attempt_id']}/complete", json={"assessment_version": 2}).json()
    assert not r["passed"] and r["score"] == 0 and r["xp_awarded"] == 0
    assert start(c, 2).status_code == 403
    with factory() as db:
        assert db.get(User, 1).xp_total == 137
    _, passed = complete_lesson(c, lesson)
    assert passed["passed"] and passed["xp_awarded"] == 10 and passed["xp_total"] == 147


def test_import_immutable_digest_and_local_only_gate(preview, monkeypatch):
    from sqlalchemy.engine import make_url

    from services.uzbekistan_history_curriculum import safe_staging_url
    from services.uzbekistan_history_models import HistoryLesson

    _, factory = preview
    with factory.begin() as db:
        db.get(HistoryLesson, "uzh-7-1-r1").content_sha256 = "0" * 64
    with factory() as db, pytest.raises(ValueError, match="changed_history_content"):
        import_course(db)
    for url in ["sqlite:///production.db", "postgresql://public.invalid/staging"]:
        with pytest.raises(ValueError):
            safe_staging_url(make_url(url))
    monkeypatch.setenv("ENVIRONMENT", "production")
    with pytest.raises(ValueError):
        safe_staging_url(make_url("sqlite:////tmp/uzbekistan_history_staging.db"))


@pytest.mark.parametrize("different_attempts", [False, True])
def test_parallel_completion_never_duplicates_xp(preview, different_attempts):
    from concurrent.futures import ThreadPoolExecutor

    c, factory = preview
    l = load_course()[0]["lessons"][0]
    a = start(c).json()
    attempts = [a, start(c).json()] if different_attempts else [a]
    for attempt in attempts:
        for q, answer in zip(l["assessments"], answers(l)):
            assert c.post(f"{P}/attempts/{attempt['attempt_id']}/answers", json={
                "assessment_version": 2, "assessment_key": q["key"], "answer": answer,
            }).status_code == 200
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda attempt: c.post(
            f"{P}/attempts/{attempt['attempt_id']}/complete", json={"assessment_version": 2}
        ), attempts if different_attempts else [a, a]))
    assert [r.status_code for r in responses] == [200, 200]
    if different_attempts:
        assert sorted(r.json()["xp_awarded"] for r in responses) == [0, 10]
    else:
        assert responses[0].json() == responses[1].json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 147


def test_postgres_opt_in_fresh_schema_all_forty_and_parallel_xp(monkeypatch):
    """Only an explicit loopback staging URL; never a production schema."""
    import os
    import secrets
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path

    from sqlalchemy import text
    from sqlalchemy.engine import make_url

    from services.database_url import normalize_database_url
    from services.uzbekistan_history_curriculum import safe_staging_url

    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("opt-in local PostgreSQL URL file not supplied")
    url = normalize_database_url(Path(filename).read_text().strip())
    safe_staging_url(make_url(url))
    admin = create_engine(url)
    schema = "uzbekistan_history_" + secrets.token_hex(8)
    with admin.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        Base.metadata.create_all(engine)
        HistoryBase.metadata.create_all(engine)
        factory = sessionmaker(bind=engine, expire_on_commit=False)
        with factory.begin() as db:
            db.add(User(id=1, name="QA", email="qa@example.test", xp_total=137))
            db.flush()
            assert import_course(db) == {"created": 42, "skipped": 0}
            assert import_course(db) == {"created": 0, "skipped": 42}
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("UZBEKISTAN_HISTORY_PREVIEW_ENABLED", "true")
        monkeypatch.setattr(tokens, "JWT_SECRET", "history-local-pg-test-only-key-over-32-characters")
        app = FastAPI()
        app.include_router(router)

        def get_db():
            with factory() as db:
                yield db

        app.dependency_overrides[database.get_db] = get_db
        with TestClient(app, headers={"Authorization": "Bearer " + tokens.create_access_token(1)}) as c:
            for l in course_lessons()[:-1]:
                _, r = complete_lesson(c, l)
                assert r["xp_awarded"] == 10
            l = course_lessons()[-1]
            attempts = [start(c, l["sequence"]).json() for _ in range(2)]
            for attempt in attempts:
                for q, answer in zip(l["assessments"], answers(l)):
                    assert c.post(f"{P}/attempts/{attempt['attempt_id']}/answers", json={
                        "assessment_version": 2, "assessment_key": q["key"], "answer": answer,
                    }).status_code == 200
            with ThreadPoolExecutor(max_workers=2) as pool:
                responses = list(pool.map(lambda attempt: c.post(
                    f"{P}/attempts/{attempt['attempt_id']}/complete", json={"assessment_version": 2}
                ), attempts))
            assert [r.status_code for r in responses] == [200, 200]
            assert sorted(r.json()["xp_awarded"] for r in responses) == [0, 10]
            _, r = complete_lesson(c, load_course()[0]["lessons"][0])
            assert r["xp_total"] == 557 and r["xp_awarded"] == 0
        with factory() as db:
            assert db.get(User, 1).xp_total == 557 and db.query(HistoryProgress).count() == 42
    finally:
        engine.dispose()
        with admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()
