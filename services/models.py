from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean, Float, ForeignKey, CheckConstraint
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
    profile_picture = Column(Text, nullable=True)  # Avatar: OAuth URL, /avatars/*.svg preset path, or a base64 data URI
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
    assistant_count_today = Column(Integer, default=0)
    assistant_count_date = Column(String(20), nullable=True)
    learning_goal = Column(Text, nullable=True)
    target_date = Column(String(20), nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    push_token = Column(String(300), nullable=True)


class EmailVerificationCode(Base):
    __tablename__ = "email_verification_codes"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), index=True, nullable=False)
    code = Column(String(8), nullable=False)
    purpose = Column(String(32), nullable=False)  # 'signup' | 'password_reset'
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AssistantMessage(Base):
    """General-purpose AI assistant conversation history — separate from the
    materials-grounded chat (VectorEntry-backed). Not restricted to any topic."""
    __tablename__ = "assistant_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    role = Column(String(16), nullable=False)  # 'user' | 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


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


class LearningPlan(Base):
    __tablename__ = "learning_plans"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    plan = Column(JSON, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ReviewItem(Base):
    """A weak topic (from a Gaps Report) scheduled for spaced-repetition review."""
    __tablename__ = "review_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    topic = Column(String(200), nullable=False)
    source_material = Column(String(300), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    next_review_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    interval_stage = Column(Integer, default=0)  # index into REVIEW_INTERVALS
    last_result = Column(String(16), nullable=True)  # "correct" | "incorrect"
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)


class CheckoutSession(Base):
    __tablename__ = "checkout_sessions"
    session_id = Column(String(64), primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    data = Column(JSON, nullable=False)


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


class SatIeltsQuestion(Base):
    __tablename__ = "sat_ielts_questions"
    id             = Column(Integer, primary_key=True, index=True)
    exam_type      = Column(String(8), nullable=False, index=True)    # "SAT" | "IELTS"
    domain         = Column(String(100), nullable=False, index=True)
    skill          = Column(String(120), nullable=True, index=True)   # sub-domain skill, e.g. "Linear functions"
    difficulty     = Column(String(8), nullable=False)                # easy|medium|hard
    question_type  = Column(String(16), nullable=False)               # mcq|short_answer|essay
    question_text  = Column(Text, nullable=False)
    options        = Column(JSON, nullable=True)                      # list[str], len==4 for MCQ
    correct_answer = Column(Text, nullable=True)
    rubric         = Column(Text, nullable=True)
    source_filename = Column(String(300), nullable=True)              # set for AI-generated
    tags           = Column(JSON, default=list)
    created_by     = Column(Integer, nullable=True)                   # user_id, NULL = seed
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("exam_type IN ('SAT','IELTS')", name="chk_sat_exam_type"),
        CheckConstraint("difficulty IN ('easy','medium','hard')", name="chk_sat_difficulty"),
        CheckConstraint(
            "question_type IN ('mcq','short_answer','essay')",
            name="chk_sat_question_type"
        ),
    )


class SatIeltsSession(Base):
    __tablename__ = "sat_ielts_sessions"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    exam_type       = Column(String(8), nullable=False)
    domain          = Column(String(100), nullable=True)              # NULL = full test / multi-domain
    difficulty      = Column(String(8), nullable=False)
    session_type    = Column(String(16), nullable=False)              # "practice" | "full_test"
    status          = Column(String(16), default="in_progress")       # in_progress|completed|expired
    timed           = Column(Boolean, default=False)
    duration_seconds = Column(Integer, nullable=True)
    questions       = Column(JSON, nullable=False)                    # list of question IDs
    answers         = Column(JSON, default=dict)                      # {q_id: {answer, elapsed_ms}}
    score           = Column(Integer, nullable=True)
    total           = Column(Integer, nullable=True)
    score_pct       = Column(Float, nullable=True)
    analysis_status = Column(String(16), default="pending")           # pending|complete|failed
    analysis_result = Column(JSON, nullable=True)
    started_at      = Column(DateTime(timezone=True), server_default=func.now())
    completed_at    = Column(DateTime(timezone=True), nullable=True)


class SatIeltsScorePrediction(Base):
    __tablename__ = "sat_ielts_score_predictions"
    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    exam_type      = Column(String(8), nullable=False)
    predicted_score = Column(Float, nullable=True)
    domain_weights  = Column(JSON, nullable=True)                     # {"Algebra": 0.72, ...}
    sessions_used   = Column(Integer, nullable=False)
    computed_at     = Column(DateTime(timezone=True), server_default=func.now())


class SatIeltsUserPrefs(Base):
    """Per-user SAT/IELTS preferences and daily counters."""
    __tablename__ = "sat_ielts_user_prefs"
    user_id              = Column(Integer, ForeignKey("users.id"), primary_key=True)
    sat_target_score     = Column(Integer, nullable=True)             # 400–1600
    ielts_target_band    = Column(Float, nullable=True)               # 1.0–9.0
    telegram_sat_enabled = Column(Boolean, default=False)
    questions_today      = Column(Integer, default=0)
    questions_date       = Column(String(20), nullable=True)          # YYYY-MM-DD
    ai_generated_today   = Column(Integer, default=0)
    ai_generated_date    = Column(String(20), nullable=True)
