"""Real reviewed catalogue/graders, synthetic HTTP. Never a live model claim."""

from copy import deepcopy
import hashlib
import json
import os
import secrets
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from tests.test_integrated_beta import beta_api, correct_answer  # noqa: F401
from tests.test_nvidia_explanations import (  # noqa: F401
    KEY, explanation_transport, generated_plan,
)


@pytest.fixture
def learner(beta_api):  # noqa: F811
    client, factory, _, _ = beta_api
    original = client.headers.get("Authorization")
    result = client.post("/beta/auth/test-login", json={"installation_secret": secrets.token_urlsafe(32)})
    assert result.status_code == 200
    account = result.json()
    client.headers["Authorization"] = "Bearer " + account["access_token"]
    from services.models import User
    with factory() as db:
        db.get(User, account["user_id"]).age = 20  # Synthetic profile, not a real person's age.
        db.commit()
    yield client, factory, account["user_id"]
    if original:
        client.headers["Authorization"] = original


def state_snapshot(factory, uid):
    from services.models import User, StudySession, StudyEvent
    with factory() as db:
        rows = [(s.id, s.scope, s.questions, s.response, str(s.completed_at))
                for s in db.query(StudySession).filter_by(user_id=uid).order_by(StudySession.id)]
        return (db.get(User, uid).xp_total, db.query(StudyEvent).count(),
                hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode()).hexdigest())


def ask_unchanged(client, factory, uid, body):
    before = state_snapshot(factory, uid)
    result = client.post("/beta/study-help", json=body,
                         headers={'X-ILM-Study-Help': 'reviewed-text-v2'})
    assert result.status_code == 200, result.text
    assert state_snapshot(factory, uid) == before
    return result.json()


def record_subject(subject, grade, lessons, records, frq):
    filename = os.getenv("ILM_NVIDIA_TEST_MATRIX_PATH")
    if filename:
        data = dict(subject=subject, grade=grade,
                    checked_utc=datetime.now(timezone.utc).isoformat(),
                    run_id=os.getenv('ILM_NVIDIA_TEST_RUN_ID'),
                    source="actual owned reviewed app catalogue",
                    lessons=lessons, questions=records, synthetic_transport=True,
                    real_provider_requests=False, MCQ_live="BLOCKED", FRQ_live="BLOCKED" if frq else "N/A",
                    wrong_answer_live="BLOCKED", fallback="PASS", Android_E2E="BLOCKED")
        with Path(filename).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(data, ensure_ascii=False) + "\n")


@pytest.mark.parametrize('provider_name', ['nvidia', 'gemini'])
@pytest.mark.parametrize("subject,grade", [
    ("biologiya", 5), ("fizika", 7), ("kimyo", 7),
    ("ozbekiston_tarixi", 7), ("jahon_tarixi", 6),
])
def test_actual_five_subject_catalogue_post_answer_generation_and_failure_preserve_grading(
    learner, explanation_transport, monkeypatch, subject, grade, provider_name,  # noqa: F811
):
    from services import study_help
    from services.models import StudySession
    from services.nvidia_explanations import NvidiaExplanationProvider
    client, factory, uid = learner
    study_help._requests.clear()
    provider = NvidiaExplanationProvider(KEY)
    if provider_name == 'gemini':
        from services.gemini_explanations import GeminiExplanationProvider, GEMINI_MODEL
        provider = GeminiExplanationProvider('AQ.' + 'synthetic-only-' * 3)
        explanation_transport.envelope_change = {'model': GEMINI_MODEL}
    monkeypatch.setattr(study_help, "_provider", provider)
    observed_pool = []
    explanation_transport.observe = lambda: observed_pool.append(factory.kw["bind"].pool.checkedout())
    questions, lessons = [], []

    def check_help(body, prompt, kind, is_correct):
        body = dict(body, language="uz", message="PRIVATE-IGNORE-SYSTEM-LEARNER-TEXT")
        result = ask_unchanged(client, factory, uid, body)
        assert result["provider_status"] == "generated" and result["mode"] == "generated_explanation"
        assert result["is_correct"] is is_correct and result["source_refs"]
        assert result["generation"]["is_correct"] is is_correct
        assert result['generation']['provider'] == provider_name
        assert result["generation"]["paragraphs"]
        assert result["evidence"] and all(e["source_refs"] for e in result["evidence"])
        assert "PRIVATE-" not in json.dumps(explanation_transport.calls[-1][1]["json"])
        assert "external_ai_eligible" not in result
        # Old Android has no generation capability header. Even when the new
        # provider is configured it must receive its original reviewed schema.
        if not questions:
            count = len(explanation_transport.calls)
            before = state_snapshot(factory, uid)
            legacy = client.post('/beta/study-help', json=body)
            assert legacy.status_code == 200
            assert legacy.json()['mode'] == 'reviewed_evidence'
            assert legacy.json()['provider_status'] == 'client_upgrade_required'
            assert 'generation' not in legacy.json()
            assert len(explanation_transport.calls) == count
            assert state_snapshot(factory, uid) == before
            older_nvidia_client = client.post('/beta/study-help', json=body,
                headers={'X-ILM-Study-Help': 'nvidia-text-v1'})
            assert older_nvidia_client.status_code == 200
            if provider_name == 'gemini':
                assert older_nvidia_client.json()['provider_status'] == 'client_upgrade_required'
                assert len(explanation_transport.calls) == count
            else:
                assert older_nvidia_client.json()['generation']['provider'] == 'nvidia'
        questions.append(dict(question_key=body["question_key"], prompt=prompt, kind=kind,
                              is_correct=is_correct, source_refs=result["source_refs"],
                              request_sha256=result["generation"]["request_sha256"],
                              response_sha256=result["generation"]["response_sha256"],
                              generated_text=result["generation"]["paragraphs"],
                              backend_response=result,
                              real_model=False))
        return result

    if subject == "biologiya":
        outline = client.get(f"/beta/skills/{uid}/curriculum", params={"subject": subject, "grade": grade}).json()
        lesson = outline["chapters"][0]["topics"][0]["lesson_ids"][0]
        issued = client.post(f"/beta/skills/lessons/{lesson}/start", json={"user_id": uid, "language": "uz"}).json()
        assert len(issued["questions"]) >= 2
        from services.models import SkillLesson
        with factory() as db:
            title = db.get(SkillLesson, lesson).title_uz
        lessons.append(dict(lesson_id=lesson, title=title, actual_catalogue=True))
        first = issued["questions"][0]
        base = dict(subject=subject, grade=grade, attempt_id=f"lesson:{issued['attempt_id']}", question_key=str(first["id"]))
        pre = ask_unchanged(client, factory, uid, dict(base, language="uz"))
        assert pre["provider_status"] == "answer_required" and not explanation_transport.calls
        for index, correct in [(0, False), (1, True)]:
            q = issued["questions"][index]
            selected = q["correct_answer"] if correct else next(o for o in q["options"] if o != q["correct_answer"])
            body = dict(base, question_key=str(q["id"]), checked=True, selected_answer=selected)
            check_help(body, q["question_text"], "concept_selection", correct)
        # Biology v1 has MCQ options, not FRQ; do not manufacture an FRQ.
        last_body = body
        frq = False
        completion = f'/beta/skills/lessons/{lesson}/complete'
        results = dict(user_id=uid, attempt_id=issued['attempt_id'], results=[
            dict(question_id=q['id'], answer_index=(
                next(i for i, option in enumerate(q['options']) if option != q['correct_answer'])
                if index == 0 else q['options'].index(q['correct_answer'])), is_correct=False)
            for index, q in enumerate(issued['questions'])])
        completed = client.post(completion, json=results)
        assert completed.status_code == 200, completed.text
        xp_after = state_snapshot(factory, uid)[0]
        assert client.post(completion, json=results).json() == completed.json()
        assert state_snapshot(factory, uid)[0] == xp_after

    else:
        root = f"/beta/v2/{subject}"
        catalog = client.get(root + "/catalog", params={"grade": grade}).json()
        key = catalog["lessons"][0]["key"]
        issued = client.post(root + f"/lessons/{key}/start", json={"assessment_version": 2, "request_id": str(uuid4())}).json()
        lessons.append(dict(lesson_key=key, title=issued['title'], actual_catalogue=True))
        with factory() as db:
            raw_questions = deepcopy(db.get(StudySession, issued["attempt_id"]).questions["assessments"])
            from services.beta_curriculum import adapter
            _, model, _, _ = adapter(db, subject)
            actual_lesson = db.get(model, key)
            lesson_metadata = dict(topic_id=actual_lesson.topic_id, sequence=actual_lesson.sequence)
        first = raw_questions[0]
        base = dict(subject=subject, grade=grade, lesson_key=key, attempt_id=issued["attempt_id"], question_key=first["key"])
        pre = ask_unchanged(client, factory, uid, dict(base, language="uz"))
        assert pre["provider_status"] == "answer_required" and not explanation_transport.calls
        wrong_done = right_done = frq = False
        written_kinds = {'short_text', 'numeric_quantity', 'numeric_value', 'chemical_formula', 'chemical_equation', 'formula'}
        for raw in raw_questions:
            if subject == 'fizika':
                from tests.test_physics_course import new_answer
                answer = new_answer(lesson_metadata, raw)
            else:
                answer = correct_answer(raw)
            correct = True
            if raw["kind"] == "concept_selection" and not wrong_done:
                answer["choice_id"] = next(o["id"] for o in raw["public"]["options"] if o["id"] != answer["choice_id"])
                correct = False
                wrong_done = True
            submitted = client.post(root + f"/attempts/{issued['attempt_id']}/answers", json={
                "assessment_version": 2, "assessment_key": raw["key"], "answer": answer})
            assert submitted.status_code == 200 and submitted.json()["is_correct"] is correct, submitted.text
            body = dict(base, question_key=raw["key"])
            if (not correct or (raw['kind'] == 'concept_selection' and not right_done)
                    or (raw['kind'] in written_kinds and not frq)):
                result = check_help(body, raw["public"]["prompt"], raw["kind"], correct)
                assert [e["text"] for e in result["evidence"] if e["kind"] == "solution"] == [s["body"] for s in submitted.json()["solution"]]
            right_done |= correct and raw["kind"] == "concept_selection"
            frq |= raw["kind"] in written_kinds
        assert wrong_done and right_done and frq
        last_body = body
        # Help does not complete a session; normal completion alone awards XP.
        completion = root + f"/attempts/{issued['attempt_id']}/complete"
        completed = client.post(completion, json={"assessment_version": 2})
        assert completed.status_code == 200
        xp_after = state_snapshot(factory, uid)[0]
        assert client.post(completion, json={"assessment_version": 2}).json() == completed.json()
        assert state_snapshot(factory, uid)[0] == xp_after

        # The source-authored written question also receives a valid but wrong
        # response in a separate owned attempt (immutable answers stay intact).
        retry = client.post(root + f"/lessons/{key}/start", json={
            "assessment_version": 2, "request_id": str(uuid4())}).json()
        with factory() as db:
            retry_questions = deepcopy(db.get(StudySession, retry['attempt_id']).questions['assessments'])
        for raw in retry_questions:
            if subject == 'fizika':
                answer = new_answer(lesson_metadata, raw)
            else:
                answer = correct_answer(raw)
            written = raw['kind'] in written_kinds
            if written:
                answer['value'] = '99999999' if raw['kind'] in {'numeric_quantity','numeric_value'} else 'PRIVATE-WRITTEN-ANSWER'
            submitted = client.post(root + f"/attempts/{retry['attempt_id']}/answers", json={
                'assessment_version': 2, 'assessment_key': raw['key'], 'answer': answer})
            assert submitted.status_code == 200, submitted.text
            if written:
                assert submitted.json()['is_correct'] is False
                body = dict(base, attempt_id=retry['attempt_id'], question_key=raw['key'])
                check_help(body, raw['public']['prompt'], raw['kind'], False)
                break
        else:
            raise AssertionError('No real source-authored written question in the selected lesson')

    # A controlled upstream outage does not erase an already checked answer,
    # change its grade, complete a lesson, or award XP again.
    explanation_transport.statuses = [429]
    outage = ask_unchanged(client, factory, uid, dict(last_body, language="uz"))
    assert outage["provider_status"] == "unavailable" and outage["mode"] == "reviewed_evidence"
    assert "generation" not in outage and outage["evidence"] and outage["answered"]
    count = len(explanation_transport.calls)
    repeat = ask_unchanged(client, factory, uid, dict(last_body, language="uz"))
    assert repeat == outage and len(explanation_transport.calls) == count
    assert observed_pool and set(observed_pool) == {0}
    record_subject(subject, grade, lessons, questions, frq)


@pytest.mark.parametrize("age", [None, 12, 17])
def test_unknown_or_child_profile_keeps_verified_help_without_upstream(learner, explanation_transport, monkeypatch, age):  # noqa: F811
    from services import study_help
    from services.models import User
    from services.nvidia_explanations import NvidiaExplanationProvider
    client, factory, uid = learner
    study_help._requests.clear()
    monkeypatch.setattr(study_help, "_provider", NvidiaExplanationProvider(KEY))
    with factory() as db:
        db.get(User, uid).age = age
        db.commit()
    outline = client.get(f"/beta/skills/{uid}/curriculum", params={"subject": "biologiya", "grade": 5}).json()
    lesson = outline["chapters"][0]["topics"][0]["lesson_ids"][0]
    issued = client.post(f"/beta/skills/lessons/{lesson}/start", json={"user_id": uid, "language": "uz"}).json()
    q = issued["questions"][0]
    result = ask_unchanged(client, factory, uid, dict(subject="biologiya", attempt_id=f"lesson:{issued['attempt_id']}",
                         question_key=str(q["id"]), checked=True, selected_answer=q["correct_answer"], language="uz"))
    assert result["provider_status"] == "audience_unavailable"
    assert result["mode"] == "reviewed_evidence" and result["is_correct"] is True
    assert not explanation_transport.calls


def test_normal_startup_hook_is_present_without_importing_or_booting_real_app():
    import ast
    tree = ast.parse(Path(__file__).resolve().parents[1].joinpath("main.py").read_text(encoding="utf-8"))
    hook = next(node for node in tree.body if isinstance(node, ast.AsyncFunctionDef) and node.name == "_study_help_startup")
    assert any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "configure_from_environment" for node in ast.walk(hook))


def test_route_deadline_returns_verified_help_while_transport_still_holds_bounded_slots(learner, monkeypatch):
    import threading
    import time
    import requests
    from routers import beta_mobile
    from services import study_help
    from services.nvidia_explanations import NvidiaExplanationProvider
    client, factory, uid = learner
    release = threading.Event()
    finished = threading.Event()
    calls, pool_counts = [], []

    class BlockedSession:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def post(self, *args, **kwargs):
            calls.append(1)
            pool_counts.append(factory.kw['bind'].pool.checkedout())
            try:
                assert release.wait(10), 'Synthetic blocked worker must be released'
                raise requests.Timeout('synthetic ignored socket timeout')
            finally:
                if len(calls) == 2:
                    finished.set()

    monkeypatch.setattr(requests, 'Session', BlockedSession)
    monkeypatch.setattr(beta_mobile, 'EXPLANATION_RESPONSE_DEADLINE_SECONDS', .08)
    provider = NvidiaExplanationProvider(KEY)
    monkeypatch.setattr(study_help, '_provider', provider)
    study_help._requests.clear()
    outline = client.get(f'/beta/skills/{uid}/curriculum', params={'subject': 'biologiya', 'grade': 5}).json()
    lesson = outline['chapters'][0]['topics'][0]['lesson_ids'][0]
    issued = client.post(f'/beta/skills/lessons/{lesson}/start', json={'user_id': uid, 'language': 'uz'}).json()
    question = issued['questions'][0]
    body = dict(subject='biologiya', grade=5, attempt_id=f"lesson:{issued['attempt_id']}",
                question_key=str(question['id']), checked=True,
                selected_answer=question['correct_answer'], language='uz')
    try:
        for _ in range(3):
            started = time.monotonic()
            result = ask_unchanged(client, factory, uid, body)
            assert time.monotonic() - started < 2
            assert result['provider_status'] == 'unavailable'
            assert result['answered'] and result['is_correct']
            assert 'generation' not in result and 'external_ai_eligible' not in result
        # Two stalled workers keep their slots; a third call never creates a
        # third upstream request and releases the DB before the wait.
        assert len(calls) == 2 and pool_counts == [0, 0]
    finally:
        release.set()
        assert finished.wait(3)
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if provider._slots.acquire(False):
                if provider._slots.acquire(False):
                    provider._slots.release()
                    provider._slots.release()
                    break
                provider._slots.release()
            time.sleep(.01)
        else:
            raise AssertionError('Synthetic provider workers did not release slots')
