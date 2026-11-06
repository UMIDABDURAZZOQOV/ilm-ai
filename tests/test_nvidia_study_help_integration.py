"""Actual reviewed beta API with a fake NVIDIA transport, never real keys."""

import json
from uuid import uuid4

from tests.test_integrated_beta import beta_api, correct_answer  # noqa: F401
from tests.test_nvidia_study_help import nvidia_transport as transport  # noqa: F401


def test_reviewed_answer_feedback_survives_selection_quota_and_invented_ids(
    beta_api,  # noqa: F811
    transport,  # noqa: F811
    monkeypatch,
):
    # The beta fixture configures its disposable DB before application imports.
    from services import study_help
    from services.nvidia_study_help import NvidiaTrialEvidenceSelector
    from tests.test_nvidia_study_help import KEYS
    from services.models import StudySession

    client, factory, _, _ = beta_api
    study_help._requests.clear()
    key = client.get("/beta/v2/kimyo/catalog", params={"grade": 7}).json()["lessons"][
        0
    ]["key"]
    issued = client.post(
        f"/beta/v2/kimyo/lessons/{key}/start",
        json={"assessment_version": 2, "request_id": str(uuid4())},
    ).json()
    question = issued["questions"][0]
    with factory() as db:
        raw = db.get(StudySession, issued["attempt_id"]).questions["assessments"][0]
    submitted = client.post(
        f"/beta/v2/kimyo/attempts/{issued['attempt_id']}/answers",
        json={
            "assessment_version": 2,
            "assessment_key": question["key"],
            "answer": correct_answer(raw),
        },
    )
    assert submitted.status_code == 200 and submitted.json()["is_correct"] is True
    request = dict(
        subject="kimyo",
        grade=7,
        attempt_id=issued["attempt_id"],
        question_key=question["key"],
        language="uz",
        message="PRIVATE-follow-up",
    )
    monkeypatch.setattr(study_help, "_provider", NvidiaTrialEvidenceSelector(KEYS))
    transport.envelope["choices"][0]["message"]["content"] = json.dumps(
        {"ids": ["invented"]}
    )
    result = client.post("/beta/study-help", json=request)
    assert result.status_code == 200
    baseline = result.json()
    assert baseline["provider_status"] == "unavailable"
    assert baseline["is_correct"] is True
    assert baseline["source_refs"] and all(
        e["source_refs"] for e in baseline["evidence"]
    )
    feedback = [
        e
        for e in baseline["evidence"]
        if e["kind"] in {"answer", "feedback", "solution"}
    ]
    assert feedback
    teaching = next(
        e
        for e in baseline["evidence"]
        if e["kind"] not in {"answer", "feedback", "solution"}
    )
    transport.envelope["choices"][0]["message"]["content"] = json.dumps(
        {"ids": [teaching["id"]]}
    )
    selected = client.post("/beta/study-help", json=request).json()
    assert selected["provider_status"] == "selected"
    assert all(e in selected["evidence"] for e in feedback)
    assert all(e in baseline["evidence"] for e in selected["evidence"])
    assert "PRIVATE-" not in json.dumps(transport.calls[-1][1]["json"])
    transport.statuses = [429]
    transport.envelope = {}
    quota = client.post("/beta/study-help", json=request).json()
    assert quota["provider_status"] == "unavailable"
    assert quota["evidence"] == baseline["evidence"]
    calls = len(transport.calls)
    client.post("/beta/study-help", json=request)
    assert len(transport.calls) == calls
