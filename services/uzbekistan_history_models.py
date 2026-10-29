"""History opt-in v2 tables adapted from the existing isolated assessment v2 contract, intentionally outside legacy Base.metadata/create_all.

Only an explicit migration/import creates them. No legacy content/progress table
or MCQ constraint is altered. Shared account/session/ledger foreign keys remain.
"""

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base

from services.models import StudySession, User

HistoryBase = declarative_base()


class HistoryLesson(HistoryBase):
    __tablename__ = "uzbekistan_history_preview_lessons"
    key = Column(String(96), primary_key=True)
    subject = Column(String(40), nullable=False)
    grade = Column(Integer, nullable=False)
    sequence = Column(Integer, nullable=False)
    revision = Column(Integer, nullable=False)
    topic_id = Column(String(80), nullable=False, unique=True)
    content_sha256 = Column(String(64), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "subject",
            "grade",
            "sequence",
            name="uq_uzbekistan_history_preview_sequence",
        ),
    )


class HistoryAssessment(HistoryBase):
    __tablename__ = "uzbekistan_history_preview_assessments"
    key = Column(String(140), primary_key=True)
    lesson_key = Column(
        String(96), ForeignKey(HistoryLesson.key), nullable=False, index=True
    )
    order_index = Column(Integer, nullable=False)
    response_kind = Column(String(32), nullable=False)
    public_prompt = Column(JSON, nullable=False)
    grading_spec = Column(JSON, nullable=False)
    source_refs = Column(JSON, nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "lesson_key",
            "order_index",
            name="uq_uzbekistan_history_preview_question_order",
        ),
    )


class HistoryProgress(HistoryBase):
    __tablename__ = "uzbekistan_history_preview_progress"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    lesson_key = Column(String(96), ForeignKey(HistoryLesson.key), primary_key=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    best_score_pct = Column(Float, nullable=False, default=0)
    attempts = Column(Integer, nullable=False, default=0)
    xp_earned = Column(Integer, nullable=False, default=0)


class HistoryAnswer(HistoryBase):
    __tablename__ = "uzbekistan_history_preview_answers"
    session_id = Column(String(96), ForeignKey(StudySession.id), primary_key=True)
    assessment_key = Column(
        String(140), ForeignKey(HistoryAssessment.key), primary_key=True
    )
    fingerprint = Column(String(64), nullable=False)
    response = Column(JSON, nullable=False)
