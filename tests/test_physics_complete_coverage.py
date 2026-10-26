"""316-section coverage is imported content, never learner/release approval."""

import pytest
from test_physics_v2 import PREFIX
from test_physics_v2 import preview as preview  # noqa: PLC0414
from test_release_hardening import setup as setup  # noqa: PLC0414

from scripts.audit_physics_course import report
from services.assessment_models import CurriculumAssessment, CurriculumLessonV2
from services.physics_curriculum import import_batch, load_course


def test_all_six_source_ranges_have_exact_nonduplicated_interactive_coverage():
    data = report()
    assert data["authored"] == data["source_total"] == 316
    assert data["remaining"] == 0
    assert [r["authored"] for r in data["grades"]] == [61, 46, 60, 59, 45, 45]
    keys = []
    for document in load_course():
        for lesson in document["lessons"]:
            keys.append(lesson["key"])
            assert lesson["cards"] and lesson["examples"] and lesson["assessments"]
    assert len(keys) == len(set(keys)) == 316
    assert data["publication"] == "local_test_preview_only"
    assert data["independent_expert"] == "not_claimed"


@pytest.mark.parametrize("missing_grade,missing_section", [(11, 45), (11, 23), (8, 30)])
def test_missing_import_cannot_report_complete_course(
    preview, missing_grade, missing_section
):
    client, factory = preview
    with factory.begin() as db:
        for document in load_course():
            import_batch(db, document)
    before = client.get(f"{PREFIX}/catalog?grade=11").json()
    assert before["course_complete"] and before["grade_content_complete"]
    assert before["publication"] == "local_test_preview_only"
    # The learner has not completed 316 lessons: this is content availability.
    assert before["lessons"][0]["state"] == "available"
    assert before["lessons"][1]["state"] == "locked"
    with factory.begin() as db:
        missing = (
            db.query(CurriculumLessonV2)
            .filter_by(subject="fizika", grade=missing_grade, sequence=missing_section)
            .one()
        )
        db.query(CurriculumAssessment).filter_by(lesson_key=missing.key).delete()
        db.delete(missing)
    after = client.get(f"{PREFIX}/catalog?grade=11").json()
    assert not after["course_complete"]
    assert after["grade_content_complete"] == (missing_grade != 11)
    assert not client.get(f"{PREFIX}/catalog?grade={missing_grade}").json()[
        "grade_content_complete"
    ]
