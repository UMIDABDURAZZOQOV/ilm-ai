from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from services.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=True)  # Made nullable for OAuth users
    oauth_provider = Column(String(50), nullable=True)  # 'google', etc.
    oauth_provider_id = Column(String(200), nullable=True)  # Provider's user ID
    profile_picture = Column(String(500), nullable=True)  # Profile picture URL from OAuth
    telegram_chat_id = Column(String(64), nullable=True)
    reminder_time = Column(String(8), default="09:00")
    streak_days = Column(Integer, default=0)
    last_study_date = Column(String(20), nullable=True)
    subscription_tier = Column(String(32), default="free")
    uploads_count = Column(Integer, default=0)
    quiz_count_today = Column(Integer, default=0)
    quiz_count_date = Column(String(20), nullable=True)
    chat_count_today = Column(Integer, default=0)
    chat_count_date = Column(String(20), nullable=True)
    learning_goal = Column(Text, nullable=True)
    target_date = Column(String(20), nullable=True)


class VectorEntry(Base):
    __tablename__ = "vectors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    filename = Column(String(300))
    topic = Column(String(200), default="General")
    chunk_id = Column(String(300))
    text = Column(Text)
    embedding = Column(JSON)  # stored as JSON array; later can be migrated to pgvector column


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    score = Column(Integer)
    total = Column(Integer)
    difficulty = Column(String(32))
    results = Column(JSON)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    token = Column(String(128), primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    exp = Column(Integer, nullable=False)


class LLMLog(Base):
    __tablename__ = "llm_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    prompt = Column(Text)
    response = Column(Text)
    latency_ms = Column(Integer)
    token_count = Column(Integer, nullable=True)
    model = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # For evaluation rubric
    rating = Column(Integer, nullable=True)  # 1-5 general
    accuracy = Column(Integer, nullable=True)  # 1-5
    groundedness = Column(Integer, nullable=True)  # 1-5
    helpfulness = Column(Integer, nullable=True)  # 1-5
    tone = Column(Integer, nullable=True)  # 1-5
    eval_comment = Column(Text, nullable=True)
