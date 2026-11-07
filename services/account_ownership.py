"""Reviewed ownership inventory, intentionally not guessed from similar names.

IELTS question.parent_id points to another question, not a parent account.
Shared textbooks/question seeds and other learners' progress are never erased.
"""

DELETED_PROVIDER = "__account_deleted__"

DIRECT_OWNERS = {
    "assistant_messages": ("user_id",),
    "flashcard_decks": ("user_id",),
    "share_links": ("user_id",),
    "streak_freezes": ("user_id",),
    "assistant_memories": ("user_id",),
    "vectors": ("user_id",),
    "quiz_sessions": ("user_id",),
    "learning_plans": ("user_id",),
    "user_courses": ("user_id",),
    "review_items": ("user_id",),
    "checkout_sessions": ("user_id",),
    "refresh_tokens": ("user_id",),
    "llm_logs": ("user_id",),
    "sat_ielts_questions": ("created_by",),
    "sat_ielts_sessions": ("user_id",),
    "sat_ielts_score_predictions": ("user_id",),
    "sat_ielts_user_prefs": ("user_id",),
    "ielts_writing_submissions": ("user_id",),
    "ielts_speaking_submissions": ("user_id",),
    "ielts_mock_tests": ("user_id",),
    "skilltree_user_lesson_progress": ("user_id",),
    "ielts_starred_words": ("user_id",),
    "skilltree_user_unit_exams": ("user_id",),
    "skilltree_user_language_levels": ("user_id",),
    "skilltree_mistakes": ("user_id",),
    "skilltree_daily_challenges": ("user_id",),
    "skilltree_lesson_attempts": ("user_id",),
    "study_sessions": ("user_id",),
    "study_events": ("user_id",),
    "mobile_login_grants": ("user_id",),
    "skilltree_mock_exams": ("user_id",),
    "skilltree_classes": ("teacher_id",),
    "skilltree_class_members": ("student_id",),
    "skilltree_family_codes": ("child_id",),
    "skilltree_parent_links": ("parent_id", "child_id"),
    "user_study_preferences": ("user_id",),
    "curriculum_progress_v2": ("user_id",),
    "chemistry_preview_progress": ("user_id",),
    "world_history_preview_progress": ("user_id",),
    "uzbekistan_history_preview_progress": ("user_id",),
    "beta_test_identities": ("user_id",),
}
ANSWER_TABLES = (
    "curriculum_answers_v2",
    "chemistry_preview_answers",
    "world_history_preview_answers",
    "uzbekistan_history_preview_answers",
)
USER_FILES = (
    "vectors",
    "data/chat_history",
    "data/plans",
    "data/quiz_history",
    "data/review_items",
)
