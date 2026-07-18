from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean, Float, ForeignKey, CheckConstraint, UniqueConstraint
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
    # Skill-tree gamification (Milliy Sertifikat)
    xp_total = Column(Integer, default=0, nullable=False)
    referral_code = Column(String(16), unique=True, nullable=True)
    referred_by = Column(Integer, nullable=True)  # user_id of the inviter (set once)


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
    image_url      = Column(Text, nullable=True)                      # URL or base64 data URI for question images (graphs, triangles, etc.)
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


# ─── IELTS-specific tables ─────────────────────────────────────────────────────

class IeltsListening(Base):
    """IELTS Listening passages with audio and questions."""
    __tablename__ = "ielts_listening"
    id              = Column(Integer, primary_key=True, index=True)
    section         = Column(Integer, nullable=False)                # 1-4
    title           = Column(String(300), nullable=False)
    audio_url       = Column(Text, nullable=True)                    # URL to audio file
    transcript      = Column(Text, nullable=True)                     # Full transcript
    difficulty      = Column(String(8), nullable=False)               # easy|medium|hard
    duration_seconds = Column(Integer, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class IeltsReading(Base):
    """IELTS Reading passages with questions."""
    __tablename__ = "ielts_reading"
    id              = Column(Integer, primary_key=True, index=True)
    section         = Column(Integer, nullable=False)                # 1-3
    title           = Column(String(300), nullable=False)
    passage_text    = Column(Text, nullable=False)                    # Full passage
    difficulty      = Column(String(8), nullable=False)               # easy|medium|hard
    word_count      = Column(Integer, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class IeltsWriting(Base):
    """IELTS Writing tasks (Task 1 and Task 2)."""
    __tablename__ = "ielts_writing"
    id              = Column(Integer, primary_key=True, index=True)
    task_type       = Column(String(8), nullable=False)              # Task1|Task2
    category        = Column(String(100), nullable=False)             # e.g., "Technology", "Education"
    prompt          = Column(Text, nullable=False)
    image_url       = Column(Text, nullable=True)                     # For Task 1 charts/graphs
    min_words       = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    difficulty      = Column(String(8), nullable=False)               # easy|medium|hard
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class IeltsSpeaking(Base):
    """IELTS Speaking topics and cue cards."""
    __tablename__ = "ielts_speaking"
    id              = Column(Integer, primary_key=True, index=True)
    part            = Column(Integer, nullable=False)                # 1-3
    topic           = Column(String(300), nullable=False)
    questions       = Column(JSON, nullable=False)                    # List of questions
    cue_card        = Column(Text, nullable=True)                     # For Part 2
    prep_seconds    = Column(Integer, nullable=True)                  # Preparation time
    speak_seconds   = Column(Integer, nullable=True)                  # Speaking time
    difficulty      = Column(String(8), nullable=False)               # easy|medium|hard
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class IeltsQuestion(Base):
    """Unified question table for IELTS (can be linked to Listening/Reading)."""
    __tablename__ = "ielts_questions"
    id              = Column(Integer, primary_key=True, index=True)
    skill           = Column(String(20), nullable=False)              # Listening|Reading
    parent_id       = Column(Integer, nullable=True)                  # FK to ielts_listening or ielts_reading
    question_type   = Column(String(20), nullable=False)              # mcq|tfng|completion|matching|heading
    question_text   = Column(Text, nullable=False)
    options         = Column(JSON, nullable=True)                     # For MCQ
    correct_answer  = Column(Text, nullable=False)
    hint            = Column(Text, nullable=True)                     # e.g., "ONE WORD ONLY"
    order_index     = Column(Integer, nullable=False)                # Question order in section
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class IeltsWritingSubmission(Base):
    """User writing submissions with AI grading."""
    __tablename__ = "ielts_writing_submissions"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    task_id         = Column(Integer, ForeignKey("ielts_writing.id"), nullable=False)
    essay_text      = Column(Text, nullable=False)
    word_count      = Column(Integer, nullable=True)
    band_score      = Column(Float, nullable=True)                   # AI-graded 0-9
    feedback        = Column(Text, nullable=True)                     # AI feedback
    task_response   = Column(Text, nullable=True)                     # TR score
    coherence       = Column(Text, nullable=True)                     # CC score
    lexical         = Column(Text, nullable=True)                     # LR score
    grammar         = Column(Text, nullable=True)                     # GRA score
    submitted_at    = Column(DateTime(timezone=True), server_default=func.now())


class IeltsSpeakingSubmission(Base):
    """User speaking recordings with AI grading."""
    __tablename__ = "ielts_speaking_submissions"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    topic_id        = Column(Integer, ForeignKey("ielts_speaking.id"), nullable=False)
    audio_url       = Column(Text, nullable=False)                    # Recording URL
    duration_seconds = Column(Integer, nullable=True)
    band_score      = Column(Float, nullable=True)                   # AI-graded 0-9
    feedback        = Column(Text, nullable=True)                     # AI feedback
    fluency         = Column(Text, nullable=True)                     # FC score
    lexical         = Column(Text, nullable=True)                     # LR score
    grammar         = Column(Text, nullable=True)                     # GRA score
    pronunciation   = Column(Text, nullable=True)                     # P score
    submitted_at    = Column(DateTime(timezone=True), server_default=func.now())


class IeltsMockTest(Base):
    """Full IELTS computer-based mock test."""
    __tablename__ = "ielts_mock_tests"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    test_type       = Column(String(20), nullable=False)              # academic|general_training
    status          = Column(String(20), default="in_progress")       # in_progress|completed
    listening_score = Column(Float, nullable=True)
    reading_score   = Column(Float, nullable=True)
    writing_score   = Column(Float, nullable=True)
    speaking_score  = Column(Float, nullable=True)
    overall_band    = Column(Float, nullable=True)
    started_at      = Column(DateTime(timezone=True), server_default=func.now())
    completed_at    = Column(DateTime(timezone=True), nullable=True)


# ─── Skill Tree (Milliy Sertifikat, Duolingo-style) ────────────────────────────

class SkillSubject(Base):
    """A top-level subject (Ona tili, Tarix, ...). Generalized so more subjects
    can be added later without a schema change — only new seed data."""
    __tablename__ = "skilltree_subjects"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(40), unique=True, nullable=False)      # "ona_tili" | "tarix"
    name_uz = Column(String(120), nullable=False)
    name_ru = Column(String(120), nullable=False)
    name_en = Column(String(120), nullable=False)
    icon = Column(String(40), nullable=True)
    color = Column(String(16), nullable=True)                   # hex accent for path theming
    order_index = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)


class SkillUnit(Base):
    __tablename__ = "skilltree_units"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("skilltree_subjects.id"), nullable=False, index=True)
    slug = Column(String(60), nullable=False)
    title_uz = Column(String(160), nullable=False)
    title_ru = Column(String(160), nullable=False)
    title_en = Column(String(160), nullable=False)
    order_index = Column(Integer, nullable=False)               # unit position within subject
    __table_args__ = (UniqueConstraint("subject_id", "order_index", name="uq_unit_order"),)


class SkillLesson(Base):
    __tablename__ = "skilltree_lessons"
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("skilltree_units.id"), nullable=False, index=True)
    slug = Column(String(60), nullable=False)
    title_uz = Column(String(160), nullable=False)
    title_ru = Column(String(160), nullable=False)
    title_en = Column(String(160), nullable=False)
    order_index = Column(Integer, nullable=False)               # position within unit == path node order
    xp_reward = Column(Integer, default=10)
    # Duolingo-style teaching phase shown BEFORE the questions: a JSON list of
    # cards [{"title": ..., "body": ..., "example": ...}] in Uzbek, generated
    # by the seed script. Nullable so structure can exist before content does.
    theory = Column(JSON, nullable=True)
    __table_args__ = (UniqueConstraint("unit_id", "order_index", name="uq_lesson_order"),)


class SkillLessonPrerequisite(Base):
    """Explicit prereq edges (many-to-many) instead of a single 'previous lesson'
    pointer, so future subjects can branch/merge paths without a schema change.
    v1 seed data is a straight line: every lesson requires the lesson immediately
    before it (a unit's first lesson requires the previous unit's last lesson);
    a subject's very first lesson has no row here -> always unlocked."""
    __tablename__ = "skilltree_lesson_prerequisites"
    lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), primary_key=True)
    requires_lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), primary_key=True)


class SkillQuestion(Base):
    __tablename__ = "skilltree_questions"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)               # stable order within the lesson session
    language = Column(String(4), nullable=False)                # 'uz' | 'ru' | 'en'
    question_type = Column(String(16), nullable=False, default="mcq")
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)                       # list[str], len==4 for mcq
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)                   # shown on the immediate-feedback card
    difficulty = Column(String(8), default="medium")
    __table_args__ = (CheckConstraint("question_type IN ('mcq')", name="chk_skill_qtype"),)


class UserLessonProgress(Base):
    """One row per (user, lesson) once attempted at least once. Absence of a row
    means 'not yet completed' -- combined with SkillLessonPrerequisite to compute
    locked/unlocked/completed status at read time (no stored 'locked' state)."""
    __tablename__ = "skilltree_user_lesson_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), nullable=False, index=True)
    stars = Column(Integer, default=0)                          # 0-3, best-ever
    best_score_pct = Column(Float, nullable=True)
    xp_earned = Column(Integer, default=0)                      # cumulative xp earned from this lesson
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)   # first completion
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),)


class SkillMistake(Base):
    """Mistakes notebook: a question the user answered wrong and hasn't yet
    answered correctly in a mistakes-practice run. Upserted on lesson complete;
    resolved_at set when the user finally gets it right."""
    __tablename__ = "skilltree_mistakes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("skilltree_questions.id"), nullable=False, index=True)
    wrong_count = Column(Integer, default=1)
    last_wrong_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("user_id", "question_id", name="uq_user_mistake"),)


class SkillDailyChallenge(Base):
    """One row per (user, date): enforces the once-a-day bonus and records the score."""
    __tablename__ = "skilltree_daily_challenges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(String(20), nullable=False)                   # YYYY-MM-DD
    score = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    xp_awarded = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_user_daily"),)


class SkillLessonAttempt(Base):
    """Per-session log (mirrors QuizSession) -- powers idempotent XP awarding
    for idempotent XP awarding."""
    __tablename__ = "skilltree_lesson_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    score = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    xp_awarded = Column(Integer, default=0)
    results = Column(JSON, nullable=True)                       # [{question_id, user_answer, is_correct}]


# ─── Mock exam + score prediction (Sinov imtihoni) ─────────────────────────────

class SkillMockExam(Base):
    """A full Milliy Sertifikat-style mock exam for one subject: a timed block
    of questions pulled from that subject's committed bank. On completion we
    grade it (percentage -> DTM-style certificate grade A+..C / no certificate)
    and store a predicted real-exam grade blended from the user's lesson mastery."""
    __tablename__ = "skilltree_mock_exams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subject_slug = Column(String(40), nullable=False, index=True)
    status = Column(String(16), default="in_progress")          # in_progress | completed
    question_ids = Column(JSON, nullable=False)                  # ordered list[int]
    duration_seconds = Column(Integer, nullable=False, default=1800)
    score = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    percentage = Column(Float, nullable=True)
    grade = Column(String(20), nullable=True)                   # "A+" | "A" | ... | "Sertifikatsiz"
    predicted_grade = Column(String(20), nullable=True)
    predicted_pct = Column(Float, nullable=True)
    results = Column(JSON, nullable=True)                        # [{question_id, is_correct}]
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


# ─── Teacher / class mode (Sinf rejimi) ────────────────────────────────────────

class SkillClass(Base):
    """A class a teacher opens. Any user can create one (becomes its teacher);
    students join with the 6-char join_code. No global 'teacher' role needed."""
    __tablename__ = "skilltree_classes"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(160), nullable=False)
    subject_slug = Column(String(40), nullable=True)            # optional focus subject
    join_code = Column(String(12), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    archived = Column(Boolean, default=False)


class SkillClassMember(Base):
    __tablename__ = "skilltree_class_members"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("skilltree_classes.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("class_id", "student_id", name="uq_class_member"),)


class SkillClassAssignment(Base):
    """Homework a teacher assigns to a class: a whole subject or a specific
    lesson, optionally due by a date. Progress is derived from each student's
    existing lesson progress -- no per-assignment submission row needed."""
    __tablename__ = "skilltree_class_assignments"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("skilltree_classes.id"), nullable=False, index=True)
    subject_slug = Column(String(40), nullable=True)
    lesson_id = Column(Integer, ForeignKey("skilltree_lessons.id"), nullable=True)
    title = Column(String(200), nullable=False)
    due_date = Column(String(20), nullable=True)                # YYYY-MM-DD
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Parent dashboard (Ota-ona paneli) ─────────────────────────────────────────

class FamilyCode(Base):
    """A stable code a student generates once and shares with a parent so the
    parent can link to their account and view (read-only) their progress."""
    __tablename__ = "skilltree_family_codes"
    child_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    code = Column(String(12), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ParentChildLink(Base):
    """A confirmed parent -> child link (parent redeemed the child's FamilyCode).
    Grants the parent read-only access to that child's stats."""
    __tablename__ = "skilltree_parent_links"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    child_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("parent_id", "child_id", name="uq_parent_child"),)
