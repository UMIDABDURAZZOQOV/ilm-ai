"""Accept a report only for the generated answer originally shown to its owner."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
import hmac
import json
from typing import Annotated

from fastapi import HTTPException
import jwt
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError

from services import tokens
from services.account_ownership import DELETED_PROVIDER
from services.ai_answer_report_models import AiAnswerReport
from services.models import User


AUDIENCE = "ilm-ai-answer-report"
Paragraph = Annotated[str, Field(min_length=1, max_length=1500)]


class AnswerReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    receipt: str = Field(min_length=1, max_length=1400)
    paragraphs: list[Paragraph] = Field(min_length=1, max_length=4)


def _key():
    return hmac.digest(tokens.JWT_SECRET.encode(), AUDIENCE.encode(), "sha256")


def _hash(value):
    return sha256(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def reportable(reply, uid, capability):
    if capability != "v1":
        return reply
    surface = reply.get("mode")
    if surface != "generated_explanation" and not (
        surface == "subject_chat" and reply.get("status") == "answered"
    ):
        return reply
    generation = reply.get("generation") or {}
    model = generation.get("model")
    request_id = reply.get("request_id") if surface == "subject_chat" else generation.get("request_id")
    paragraphs = generation.get("paragraphs")
    if (not isinstance(model, str) or not 1 <= len(model) <= 120 or not request_id
            or generation.get("http_status") != 200 or not isinstance(paragraphs, list)
            or not 1 <= len(paragraphs) <= 4):
        return reply
    text = [item.get("text") for item in paragraphs if isinstance(item, dict)]
    if len(text) != len(paragraphs) or any(not isinstance(value, str) or not 1 <= len(value) <= 1500
                                           for value in text):
        return reply
    now = datetime.now(timezone.utc)
    content_digest = _hash(text)
    receipt = jwt.encode({
        "sub": str(uid), "aud": AUDIENCE, "exp": now + timedelta(hours=24),
        # Transport request IDs can recur in another conversation or after a retry.
        "jti": _hash([uid, surface, reply["subject"], reply.get("conversation_id"),
                      request_id, model, content_digest]), "digest": content_digest,
        "subject": reply["subject"], "surface": surface, "model": model,
    }, _key(), algorithm="HS256")
    return {**reply, "report_receipt": receipt}


def save(db, uid, data):
    try:
        claim = jwt.decode(data.receipt, _key(), algorithms=["HS256"], audience=AUDIENCE,
                           options={"require": ["sub", "aud", "exp", "jti", "digest"]})
    except jwt.InvalidTokenError:
        raise HTTPException(400, "invalid_ai_report") from None
    if claim["sub"] != str(uid) or not hmac.compare_digest(claim["digest"], _hash(data.paragraphs)):
        raise HTTPException(400, "invalid_ai_report")
    if not inspect(db.connection()).has_table(AiAnswerReport.__tablename__):
        raise HTTPException(503, "ai_reporting_unavailable")
    if db.get_bind().dialect.name == "sqlite":
        db.connection().exec_driver_sql("BEGIN IMMEDIATE")
    owner = db.scalar(select(User).where(User.id == uid).with_for_update())
    if owner is None or owner.oauth_provider == DELETED_PROVIDER:
        raise HTTPException(401, "account_deleted")
    if db.get(AiAnswerReport, claim["jti"]) is None:
        # Persist only the reported answer. Never include the learner prompt,
        # conversation, raw written answer, or signed token in the review queue.
        from services.subject_tutor import sanitized

        db.add(AiAnswerReport(id=claim["jti"], user_id=uid, subject=claim["subject"],
                              surface=claim["surface"], model=claim["model"],
                              paragraphs=[sanitized(text) for text in data.paragraphs],
                              created_at=datetime.now(timezone.utc)))
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            if db.get(AiAnswerReport, claim["jti"]) is None:
                raise
    db.commit()
    return {"reported": True}
