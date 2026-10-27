"""Opt-in mathematics tables; never registered with legacy Base/create_all.

Explicit local/test setup owns these tables. Other subjects keep their models.
"""

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base

from services.models import User

MathBase = declarative_base()


class MathLesson(MathBase):
    __tablename__ = "mathematics_preview_lessons"
    key = Column(String(96), primary_key=True)
    grade = Column(Integer, nullable=False)
    part = Column(Integer, nullable=False)
    sequence = Column(Integer, nullable=False)
    sha256 = Column(String(64), nullable=False)
    document = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint("grade", "part", "sequence", name="uq_math_preview_sequence"),
    )


class MathAttempt(MathBase):
    __tablename__ = "mathematics_preview_attempts"
    id = Column(String(96), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    lesson_key = Column(String(96), ForeignKey(MathLesson.key), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    snapshot = Column(JSON, nullable=False)
    result = Column(JSON, nullable=True)


class MathAnswer(MathBase):
    __tablename__ = "mathematics_preview_answers"
    attempt_id = Column(String(96), ForeignKey(MathAttempt.id), primary_key=True)
    request_id = Column(String(36), primary_key=True)
    question_id = Column(String(96), nullable=False)
    sequence = Column(Integer, nullable=False)
    fingerprint = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    response = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint("attempt_id", "sequence", name="uq_math_answer_sequence"),
    )


class MathProgress(MathBase):
    __tablename__ = "mathematics_preview_progress"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    lesson_key = Column(String(96), ForeignKey(MathLesson.key), primary_key=True)
    completed_at = Column(DateTime(timezone=True), nullable=False)
    xp_earned = Column(Integer, nullable=False)
