from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
from fastapi import HTTPException
import jwt
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from services import ai_answer_reports as reports, tokens
from services.account_deletion import _purge_owned_rows
from services.ai_answer_report_models import AiAnswerReport
from services.db import Base
from services.models import User


def install_report_table(engine):
    spec = importlib.util.spec_from_file_location(
        'ai_report_migration', Path(__file__).parents[1] / 'alembic/versions/0019_ai_answer_reports.py',
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    with engine.begin() as connection, Operations.context(MigrationContext.configure(connection)):
        if engine.dialect.name == 'postgresql':
            from tests.test_account_deletion import migration as account_migration
            account_migration.install_barriers(connection)
        migration.upgrade()


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(tokens, 'JWT_SECRET', 'synthetic-ai-report-fixture-secret-only')
    engine = create_engine(f"sqlite:///{tmp_path / 'reports.db'}")
    Base.metadata.create_all(engine)
    install_report_table(engine)
    with Session(engine) as session:
        session.add_all([
            User(id=12, email="one@example.invalid", name="One", xp_total=25),
            User(id=34, email="two@example.invalid", name="Two", xp_total=55),
        ])
        session.commit()
        yield session
    engine.dispose()


def reply(surface="subject_chat", status="answered"):
    return dict(mode=surface, subject="kimyo", status=status, request_id="chat-turn",
                generation=dict(model="synthetic-model", request_id="explanation-turn",
                                http_status=200, paragraphs=[{"text": "Example answer."}]))


@pytest.mark.parametrize("surface", ["subject_chat", "generated_explanation"])
def test_owned_answer_is_reportable_once_without_changing_progress(db, surface):
    issued = reports.reportable(reply(surface), 12, "v1")
    second = reports.reportable(reply(surface), 12, "v1")
    for result in (issued, second):
        assert reports.save(db, 12, reports.AnswerReport(
            receipt=result["report_receipt"], paragraphs=["Example answer."]
        )) == {"reported": True}
    row = db.query(AiAnswerReport).one()
    assert (row.user_id, row.surface, row.paragraphs) == (12, surface, ["Example answer."])
    assert db.get(User, 12).xp_total == 25


def test_rejects_modified_content_different_account_expiry_and_session_tokens(db):
    receipt = reports.reportable(reply(), 12, "v1")["report_receipt"]
    expired = jwt.decode(receipt, reports._key(), algorithms=["HS256"], audience=reports.AUDIENCE)
    expired["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    expired = jwt.encode(expired, reports._key(), algorithm="HS256")
    for owner, proof, text in [
        (34, receipt, "Example answer."),
        (12, receipt, "Replaced answer."),
        (12, expired, "Example answer."),
        (12, tokens.create_access_token(12), "Example answer."),
    ]:
        with pytest.raises(HTTPException) as error:
            reports.save(db, owner, reports.AnswerReport(receipt=proof, paragraphs=[text]))
        assert error.value.detail == "invalid_ai_report"
    assert db.query(AiAnswerReport).count() == 0


@pytest.mark.parametrize("surface", ["subject_chat", "generated_explanation"])
def test_two_displayed_answers_with_same_transport_id_can_both_be_reported(db, surface):
    for text in ["The first answer.", "The revised answer.", "The revised answer."]:
        answer = reply(surface)
        answer["generation"]["paragraphs"] = [{"text": text}]
        issued = reports.reportable(answer, 12, "v1")
        reports.save(db, 12, reports.AnswerReport(receipt=issued["report_receipt"], paragraphs=[text]))
    assert sorted(row.paragraphs for row in db.query(AiAnswerReport)) == [
        ["The first answer."], ["The revised answer."],
    ]


def test_account_purge_removes_only_its_reports_and_contact_data_is_redacted(db):
    answer = reply()
    text = "Generated text with contact student@example.invalid."
    answer["generation"]["paragraphs"][0]["text"] = text
    for owner in (12, 34):
        issued = reports.reportable(answer, owner, "v1")
        reports.save(db, owner, reports.AnswerReport(receipt=issued["report_receipt"], paragraphs=[text]))
    _purge_owned_rows(db, db.get(User, 12))
    db.commit()
    row = db.query(AiAnswerReport).one()
    assert row.user_id == 34
    assert "student@example.invalid" not in row.paragraphs[0]


def test_unavailable_reviewed_and_legacy_replies_have_no_report_proof():
    assert "report_receipt" not in reports.reportable(reply(status="unavailable"), 12, "v1")
    assert "report_receipt" not in reports.reportable(reply("reviewed_evidence"), 12, "v1")
    assert "report_receipt" not in reports.reportable(reply(), 12, None)


def test_deleted_account_cannot_receive_a_report_even_with_direct_database_write(db):
    from services.account_ownership import DELETED_PROVIDER

    issued = reports.reportable(reply(), 12, "v1")
    db.get(User, 12).oauth_provider = DELETED_PROVIDER
    db.commit()
    with pytest.raises(HTTPException) as error:
        reports.save(db, 12, reports.AnswerReport(receipt=issued["report_receipt"], paragraphs=["Example answer."]))
    assert error.value.status_code == 401
    db.rollback()
    db.add(AiAnswerReport(id="attempted-write", user_id=12, subject="kimyo", surface="subject_chat",
                          model="synthetic", paragraphs=["Test"], created_at=datetime.now(timezone.utc)))
    with pytest.raises(IntegrityError, match="account_deleted"):
        db.commit()
