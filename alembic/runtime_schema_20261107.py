"""Pinned 2026-11-07 runtime DDL. No application imports, user rows or seeds."""

import sqlalchemy as sa


def definitions():
    metadata = sa.MetaData()
    table = sa.Table(
        "assistant_memories",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_assistant_memories_id", table.c["id"], unique=False)
    sa.Index("ix_assistant_memories_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "assistant_messages",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_assistant_messages_id", table.c["id"], unique=False)
    sa.Index("ix_assistant_messages_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "checkout_sessions",
        metadata,
        sa.Column("session_id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
    )
    sa.Index("ix_checkout_sessions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "email_verification_codes",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("code", sa.String(length=8), nullable=False),
        sa.Column("purpose", sa.String(length=32), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_email_verification_codes_email", table.c["email"], unique=False)
    sa.Index("ix_email_verification_codes_id", table.c["id"], unique=False)
    table = sa.Table(
        "flashcard_decks",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("cards", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_flashcard_decks_id", table.c["id"], unique=False)
    sa.Index("ix_flashcard_decks_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "ielts_listening",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("section", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("audio_parts", sa.JSON(), nullable=True),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.Column("tables", sa.JSON(), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_listening_id", table.c["id"], unique=False)
    table = sa.Table(
        "ielts_questions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("skill", sa.String(length=20), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("question_type", sa.String(length=20), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("correct_answer", sa.Text(), nullable=False),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_questions_id", table.c["id"], unique=False)
    table = sa.Table(
        "ielts_reading",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("section", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("passage_text", sa.Text(), nullable=False),
        sa.Column("tables", sa.JSON(), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_reading_id", table.c["id"], unique=False)
    table = sa.Table(
        "ielts_speaking",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("part", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(length=300), nullable=False),
        sa.Column("questions", sa.JSON(), nullable=False),
        sa.Column("cue_card", sa.Text(), nullable=True),
        sa.Column("prep_seconds", sa.Integer(), nullable=True),
        sa.Column("speak_seconds", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_speaking_id", table.c["id"], unique=False)
    table = sa.Table(
        "ielts_writing",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("task_type", sa.String(length=8), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("min_words", sa.Integer(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_writing_id", table.c["id"], unique=False)
    table = sa.Table(
        "llm_logs",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("prompt", sa.Text(), nullable=True),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("model", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("accuracy", sa.Integer(), nullable=True),
        sa.Column("groundedness", sa.Integer(), nullable=True),
        sa.Column("helpfulness", sa.Integer(), nullable=True),
        sa.Column("tone", sa.Integer(), nullable=True),
        sa.Column("eval_comment", sa.Text(), nullable=True),
    )
    sa.Index("ix_llm_logs_id", table.c["id"], unique=False)
    sa.Index("ix_llm_logs_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "oauth_states",
        metadata,
        sa.Column("state_hash", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("challenge", sa.String(length=128), nullable=True),
        sa.Column("redirect_uri", sa.String(length=1000), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed", sa.Boolean(), nullable=False),
    )
    table = sa.Table(
        "quiz_sessions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("difficulty", sa.String(length=32), nullable=True),
        sa.Column("results", sa.JSON(), nullable=True),
    )
    sa.Index("ix_quiz_sessions_id", table.c["id"], unique=False)
    sa.Index("ix_quiz_sessions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "refresh_tokens",
        metadata,
        sa.Column("token", sa.String(length=128), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exp", sa.Integer(), nullable=False),
    )
    sa.Index("ix_refresh_tokens_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "sat_ielts_questions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("exam_type", sa.String(length=8), nullable=False),
        sa.Column("domain", sa.String(length=100), nullable=False),
        sa.Column("skill", sa.String(length=120), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column("question_type", sa.String(length=16), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("correct_answer", sa.Text(), nullable=True),
        sa.Column("rubric", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("source_filename", sa.String(length=300), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "difficulty IN ('easy','medium','hard')", name="chk_sat_difficulty"
        ),
        sa.CheckConstraint("exam_type IN ('SAT','IELTS')", name="chk_sat_exam_type"),
        sa.CheckConstraint(
            "question_type IN ('mcq','short_answer','essay')",
            name="chk_sat_question_type",
        ),
    )
    sa.Index("ix_sat_ielts_questions_domain", table.c["domain"], unique=False)
    sa.Index("ix_sat_ielts_questions_exam_type", table.c["exam_type"], unique=False)
    sa.Index("ix_sat_ielts_questions_id", table.c["id"], unique=False)
    sa.Index("ix_sat_ielts_questions_skill", table.c["skill"], unique=False)
    table = sa.Table(
        "share_links",
        metadata,
        sa.Column("token", sa.String(length=24), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_share_links_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "skilltree_placement_questions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("subject_slug", sa.String(length=40), nullable=False),
        sa.Column("level", sa.String(length=12), nullable=False),
        sa.Column("skill", sa.String(length=40), nullable=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.String(length=500), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_skilltree_placement_questions_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_placement_questions_level", table.c["level"], unique=False)
    sa.Index(
        "ix_skilltree_placement_questions_subject_slug",
        table.c["subject_slug"],
        unique=False,
    )
    table = sa.Table(
        "skilltree_subjects",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("slug", sa.String(length=40), nullable=False),
        sa.Column("name_uz", sa.String(length=120), nullable=False),
        sa.Column("name_ru", sa.String(length=120), nullable=False),
        sa.Column("name_en", sa.String(length=120), nullable=False),
        sa.Column("icon", sa.String(length=40), nullable=True),
        sa.Column("color", sa.String(length=16), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.UniqueConstraint("slug"),
    )
    sa.Index("ix_skilltree_subjects_id", table.c["id"], unique=False)
    table = sa.Table(
        "streak_freezes",
        metadata,
        sa.Column("user_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    table = sa.Table(
        "users",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=True),
        sa.Column("oauth_provider", sa.String(length=50), nullable=True),
        sa.Column("oauth_provider_id", sa.String(length=200), nullable=True),
        sa.Column("profile_picture", sa.Text(), nullable=True),
        sa.Column("telegram_chat_id", sa.String(length=64), nullable=True),
        sa.Column("reminder_time", sa.String(length=8), nullable=True),
        sa.Column("streak_days", sa.Integer(), nullable=True),
        sa.Column("last_study_date", sa.String(length=20), nullable=True),
        sa.Column("subscription_tier", sa.String(length=32), nullable=True),
        sa.Column("uploads_count", sa.Integer(), nullable=True),
        sa.Column("quiz_count_today", sa.Integer(), nullable=True),
        sa.Column("quiz_count_date", sa.String(length=20), nullable=True),
        sa.Column("chat_count_today", sa.Integer(), nullable=True),
        sa.Column("chat_count_date", sa.String(length=20), nullable=True),
        sa.Column("assistant_count_today", sa.Integer(), nullable=True),
        sa.Column("assistant_count_date", sa.String(length=20), nullable=True),
        sa.Column("learning_goal", sa.Text(), nullable=True),
        sa.Column("target_date", sa.String(length=20), nullable=True),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("push_token", sa.String(length=300), nullable=True),
        sa.Column("xp_total", sa.Integer(), nullable=False),
        sa.Column("referral_code", sa.String(length=16), nullable=True),
        sa.Column("referred_by", sa.Integer(), nullable=True),
        sa.UniqueConstraint("referral_code"),
    )
    sa.Index("ix_users_email", table.c["email"], unique=True)
    sa.Index("ix_users_id", table.c["id"], unique=False)
    table = sa.Table(
        "vectors",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=300), nullable=True),
        sa.Column("topic", sa.String(length=200), nullable=True),
        sa.Column("chunk_id", sa.String(length=300), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("embedding", sa.JSON(), nullable=True),
    )
    sa.Index("ix_vectors_id", table.c["id"], unique=False)
    sa.Index("ix_vectors_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "curriculum_courses",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "subject_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_subjects.id"),
            nullable=False,
        ),
        sa.Column("grade", sa.Integer(), nullable=False),
        sa.Column("title_uz", sa.Text(), nullable=False),
        sa.Column("source_book_id", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=48), nullable=False),
        sa.Column("catalog", sa.JSON(), nullable=False),
        sa.UniqueConstraint("subject_id", "grade", name="uq_curriculum_subject_grade"),
    )
    table = sa.Table(
        "ielts_mock_tests",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("test_type", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("listening_score", sa.Float(), nullable=True),
        sa.Column("reading_score", sa.Float(), nullable=True),
        sa.Column("writing_score", sa.Float(), nullable=True),
        sa.Column("speaking_score", sa.Float(), nullable=True),
        sa.Column("overall_band", sa.Float(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    sa.Index("ix_ielts_mock_tests_id", table.c["id"], unique=False)
    sa.Index("ix_ielts_mock_tests_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "ielts_speaking_submissions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "topic_id", sa.Integer(), sa.ForeignKey("ielts_speaking.id"), nullable=False
        ),
        sa.Column("audio_url", sa.Text(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("band_score", sa.Float(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("fluency", sa.Text(), nullable=True),
        sa.Column("lexical", sa.Text(), nullable=True),
        sa.Column("grammar", sa.Text(), nullable=True),
        sa.Column("pronunciation", sa.Text(), nullable=True),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_speaking_submissions_id", table.c["id"], unique=False)
    sa.Index("ix_ielts_speaking_submissions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "ielts_starred_words",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("word", sa.String(length=64), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "word", name="uq_user_starred_word"),
    )
    sa.Index("ix_ielts_starred_words_id", table.c["id"], unique=False)
    sa.Index("ix_ielts_starred_words_user_id", table.c["user_id"], unique=False)
    sa.Index("ix_ielts_starred_words_word", table.c["word"], unique=False)
    table = sa.Table(
        "ielts_writing_submissions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "task_id", sa.Integer(), sa.ForeignKey("ielts_writing.id"), nullable=False
        ),
        sa.Column("essay_text", sa.Text(), nullable=False),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column("band_score", sa.Float(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("task_response", sa.Text(), nullable=True),
        sa.Column("coherence", sa.Text(), nullable=True),
        sa.Column("lexical", sa.Text(), nullable=True),
        sa.Column("grammar", sa.Text(), nullable=True),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_ielts_writing_submissions_id", table.c["id"], unique=False)
    sa.Index("ix_ielts_writing_submissions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "learning_plans",
        metadata,
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("plan", sa.JSON(), nullable=False),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    table = sa.Table(
        "mobile_login_grants",
        metadata,
        sa.Column("code_hash", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("challenge", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed", sa.Boolean(), nullable=False),
    )
    table = sa.Table(
        "review_items",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("source_material", sa.String(length=300), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("next_review_date", sa.String(length=20), nullable=False),
        sa.Column("interval_stage", sa.Integer(), nullable=True),
        sa.Column("last_result", sa.String(length=16), nullable=True),
        sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    sa.Index("ix_review_items_id", table.c["id"], unique=False)
    sa.Index("ix_review_items_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "sat_ielts_score_predictions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exam_type", sa.String(length=8), nullable=False),
        sa.Column("predicted_score", sa.Float(), nullable=True),
        sa.Column("domain_weights", sa.JSON(), nullable=True),
        sa.Column("sessions_used", sa.Integer(), nullable=False),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_sat_ielts_score_predictions_id", table.c["id"], unique=False)
    sa.Index("ix_sat_ielts_score_predictions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "sat_ielts_sessions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exam_type", sa.String(length=8), nullable=False),
        sa.Column("domain", sa.String(length=100), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=False),
        sa.Column("session_type", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=True),
        sa.Column("timed", sa.Boolean(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("questions", sa.JSON(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("score_pct", sa.Float(), nullable=True),
        sa.Column("analysis_status", sa.String(length=16), nullable=True),
        sa.Column("analysis_result", sa.JSON(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    sa.Index("ix_sat_ielts_sessions_id", table.c["id"], unique=False)
    sa.Index("ix_sat_ielts_sessions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "sat_ielts_user_prefs",
        metadata,
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("sat_target_score", sa.Integer(), nullable=True),
        sa.Column("ielts_target_band", sa.Float(), nullable=True),
        sa.Column("telegram_sat_enabled", sa.Boolean(), nullable=True),
        sa.Column("questions_today", sa.Integer(), nullable=True),
        sa.Column("questions_date", sa.String(length=20), nullable=True),
        sa.Column("ai_generated_today", sa.Integer(), nullable=True),
        sa.Column("ai_generated_date", sa.String(length=20), nullable=True),
    )
    table = sa.Table(
        "skilltree_classes",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "teacher_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("subject_slug", sa.String(length=40), nullable=True),
        sa.Column("join_code", sa.String(length=12), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("archived", sa.Boolean(), nullable=True),
    )
    sa.Index("ix_skilltree_classes_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_classes_join_code", table.c["join_code"], unique=True)
    sa.Index("ix_skilltree_classes_teacher_id", table.c["teacher_id"], unique=False)
    table = sa.Table(
        "skilltree_daily_challenges",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("date", sa.String(length=20), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("xp_awarded", sa.Integer(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "date", name="uq_user_daily"),
    )
    sa.Index("ix_skilltree_daily_challenges_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_daily_challenges_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "skilltree_family_codes",
        metadata,
        sa.Column(
            "child_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("code", sa.String(length=12), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index("ix_skilltree_family_codes_code", table.c["code"], unique=True)
    table = sa.Table(
        "skilltree_mock_exams",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("subject_slug", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=True),
        sa.Column("question_ids", sa.JSON(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("percentage", sa.Float(), nullable=True),
        sa.Column("grade", sa.String(length=20), nullable=True),
        sa.Column("predicted_grade", sa.String(length=20), nullable=True),
        sa.Column("predicted_pct", sa.Float(), nullable=True),
        sa.Column("results", sa.JSON(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    sa.Index("ix_skilltree_mock_exams_id", table.c["id"], unique=False)
    sa.Index(
        "ix_skilltree_mock_exams_subject_slug", table.c["subject_slug"], unique=False
    )
    sa.Index("ix_skilltree_mock_exams_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "skilltree_parent_links",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("child_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("parent_id", "child_id", name="uq_parent_child"),
    )
    sa.Index("ix_skilltree_parent_links_child_id", table.c["child_id"], unique=False)
    sa.Index("ix_skilltree_parent_links_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_parent_links_parent_id", table.c["parent_id"], unique=False)
    table = sa.Table(
        "skilltree_units",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "subject_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_subjects.id"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(length=60), nullable=False),
        sa.Column("title_uz", sa.String(length=160), nullable=False),
        sa.Column("title_ru", sa.String(length=160), nullable=False),
        sa.Column("title_en", sa.String(length=160), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.UniqueConstraint("subject_id", "order_index", name="uq_unit_order"),
    )
    sa.Index("ix_skilltree_units_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_units_subject_id", table.c["subject_id"], unique=False)
    table = sa.Table(
        "skilltree_user_language_levels",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("subject_slug", sa.String(length=40), nullable=False),
        sa.Column("level", sa.String(length=8), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("score_pct", sa.Float(), nullable=True),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "subject_slug", name="uq_user_language_level"),
    )
    sa.Index("ix_skilltree_user_language_levels_id", table.c["id"], unique=False)
    sa.Index(
        "ix_skilltree_user_language_levels_subject_slug",
        table.c["subject_slug"],
        unique=False,
    )
    sa.Index(
        "ix_skilltree_user_language_levels_user_id", table.c["user_id"], unique=False
    )
    table = sa.Table(
        "study_events",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("source_key", sa.String(length=140), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("xp", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_key"),
    )
    sa.Index("ix_study_events_created_at", table.c["created_at"], unique=False)
    sa.Index("ix_study_events_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "study_sessions",
        metadata,
        sa.Column("id", sa.String(length=96), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("kind", sa.String(length=24), nullable=False),
        sa.Column("scope", sa.String(length=100), nullable=False),
        sa.Column("questions", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response", sa.JSON(), nullable=True),
        sa.Column("fingerprint", sa.String(length=64), nullable=True),
    )
    sa.Index("ix_study_sessions_kind", table.c["kind"], unique=False)
    sa.Index("ix_study_sessions_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "user_courses",
        metadata,
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("course", sa.JSON(), nullable=False),
        sa.Column("progress", sa.JSON(), nullable=True),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    table = sa.Table(
        "user_study_preferences",
        metadata,
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("daily_goal_xp", sa.Integer(), nullable=False),
        sa.Column("subject", sa.String(length=100), nullable=True),
        sa.Column("grade", sa.String(length=8), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("reason", sa.String(length=500), nullable=True),
    )
    table = sa.Table(
        "curriculum_chapters",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("curriculum_courses.id"),
            nullable=False,
        ),
        sa.Column("source_key", sa.String(length=80), nullable=False),
        sa.Column(
            "unit_id", sa.Integer(), sa.ForeignKey("skilltree_units.id"), nullable=False
        ),
        sa.UniqueConstraint("unit_id"),
        sa.UniqueConstraint("course_id", "source_key", name="uq_curriculum_chapter"),
    )
    sa.Index("ix_curriculum_chapters_course_id", table.c["course_id"], unique=False)
    table = sa.Table(
        "skilltree_class_members",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "class_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_classes.id"),
            nullable=False,
        ),
        sa.Column(
            "student_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("class_id", "student_id", name="uq_class_member"),
    )
    sa.Index("ix_skilltree_class_members_class_id", table.c["class_id"], unique=False)
    sa.Index("ix_skilltree_class_members_id", table.c["id"], unique=False)
    sa.Index(
        "ix_skilltree_class_members_student_id", table.c["student_id"], unique=False
    )
    table = sa.Table(
        "skilltree_lessons",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "unit_id", sa.Integer(), sa.ForeignKey("skilltree_units.id"), nullable=False
        ),
        sa.Column("slug", sa.String(length=60), nullable=False),
        sa.Column("title_uz", sa.String(length=160), nullable=False),
        sa.Column("title_ru", sa.String(length=160), nullable=False),
        sa.Column("title_en", sa.String(length=160), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("xp_reward", sa.Integer(), nullable=True),
        sa.Column("theory", sa.JSON(), nullable=True),
        sa.UniqueConstraint("unit_id", "order_index", name="uq_lesson_order"),
    )
    sa.Index("ix_skilltree_lessons_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_lessons_unit_id", table.c["unit_id"], unique=False)
    table = sa.Table(
        "skilltree_user_unit_exams",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "unit_id", sa.Integer(), sa.ForeignKey("skilltree_units.id"), nullable=False
        ),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("best_score_pct", sa.Float(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=True),
        sa.Column("passed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "unit_id", name="uq_user_unit_exam"),
    )
    sa.Index("ix_skilltree_user_unit_exams_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_user_unit_exams_unit_id", table.c["unit_id"], unique=False)
    sa.Index("ix_skilltree_user_unit_exams_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "curriculum_topics",
        metadata,
        sa.Column("id", sa.String(length=80), primary_key=True, nullable=False),
        sa.Column(
            "chapter_id",
            sa.Integer(),
            sa.ForeignKey("curriculum_chapters.id"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("title_uz", sa.Text(), nullable=False),
        sa.Column("source", sa.JSON(), nullable=False),
    )
    sa.Index("ix_curriculum_topics_chapter_id", table.c["chapter_id"], unique=False)
    table = sa.Table(
        "skilltree_class_assignments",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "class_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_classes.id"),
            nullable=False,
        ),
        sa.Column("subject_slug", sa.String(length=40), nullable=True),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            nullable=True,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("due_date", sa.String(length=20), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )
    sa.Index(
        "ix_skilltree_class_assignments_class_id", table.c["class_id"], unique=False
    )
    sa.Index("ix_skilltree_class_assignments_id", table.c["id"], unique=False)
    table = sa.Table(
        "skilltree_lesson_attempts",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("total", sa.Integer(), nullable=True),
        sa.Column("xp_awarded", sa.Integer(), nullable=True),
        sa.Column("results", sa.JSON(), nullable=True),
    )
    sa.Index("ix_skilltree_lesson_attempts_id", table.c["id"], unique=False)
    sa.Index(
        "ix_skilltree_lesson_attempts_lesson_id", table.c["lesson_id"], unique=False
    )
    sa.Index("ix_skilltree_lesson_attempts_user_id", table.c["user_id"], unique=False)
    table = sa.Table(
        "skilltree_lesson_prerequisites",
        metadata,
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "requires_lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            primary_key=True,
            nullable=False,
        ),
    )
    table = sa.Table(
        "skilltree_questions",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            nullable=False,
        ),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(length=4), nullable=False),
        sa.Column("question_type", sa.String(length=16), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("correct_answer", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("difficulty", sa.String(length=8), nullable=True),
        sa.CheckConstraint("question_type IN ('mcq')", name="chk_skill_qtype"),
    )
    sa.Index("ix_skilltree_questions_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_questions_lesson_id", table.c["lesson_id"], unique=False)
    table = sa.Table(
        "skilltree_user_lesson_progress",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            nullable=False,
        ),
        sa.Column("stars", sa.Integer(), nullable=True),
        sa.Column("best_score_pct", sa.Float(), nullable=True),
        sa.Column("xp_earned", sa.Integer(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),
    )
    sa.Index("ix_skilltree_user_lesson_progress_id", table.c["id"], unique=False)
    sa.Index(
        "ix_skilltree_user_lesson_progress_lesson_id",
        table.c["lesson_id"],
        unique=False,
    )
    sa.Index(
        "ix_skilltree_user_lesson_progress_user_id", table.c["user_id"], unique=False
    )
    table = sa.Table(
        "curriculum_lesson_sources",
        metadata,
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_lessons.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "topic_id",
            sa.String(length=80),
            sa.ForeignKey("curriculum_topics.id"),
            nullable=False,
        ),
        sa.Column("content_key", sa.String(length=100), nullable=False),
        sa.Column("content_sha256", sa.String(length=64), nullable=False),
        sa.Column("references", sa.JSON(), nullable=False),
        sa.Column("question_references", sa.JSON(), nullable=False),
        sa.UniqueConstraint("content_key"),
    )
    sa.Index("ix_curriculum_lesson_sources_topic_id", table.c["topic_id"], unique=False)
    table = sa.Table(
        "skilltree_mistakes",
        metadata,
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "question_id",
            sa.Integer(),
            sa.ForeignKey("skilltree_questions.id"),
            nullable=False,
        ),
        sa.Column("wrong_count", sa.Integer(), nullable=True),
        sa.Column(
            "last_wrong_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("review_stage", sa.Integer(), nullable=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "question_id", name="uq_user_mistake"),
    )
    sa.Index("ix_skilltree_mistakes_id", table.c["id"], unique=False)
    sa.Index("ix_skilltree_mistakes_question_id", table.c["question_id"], unique=False)
    sa.Index("ix_skilltree_mistakes_user_id", table.c["user_id"], unique=False)
    return metadata
