"""Answer reports require the explicit migration and account write barrier."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import declarative_base

from services.models import User

AnswerReportBase = declarative_base()


class AiAnswerReport(AnswerReportBase):
    __tablename__ = "ai_answer_reports"

    id = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    subject = Column(String(40), nullable=False)
    surface = Column(String(24), nullable=False)
    model = Column(String(120), nullable=False)
    paragraphs = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
