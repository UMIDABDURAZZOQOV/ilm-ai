import datetime
import logging
import os
import re
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from services.quiz_engine import check_answer, generate_quiz
from services.users import (
    find_user_by_chat_id,
    link_telegram,
    record_study_activity,
    set_reminder_time,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TZ = ZoneInfo("Asia/Tashkent")
LINK_EMAIL, LINK_PASSWORD = range(2)
quiz_sessions: dict[int, dict] = {}

# SAT/IELTS pending questions: {chat_id: {session_id, question, user_id}}
sat_pending: dict[int, dict] = {}


def _linked_user(update: Update):
    return find_user_by_chat_id(update.effective_chat.id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to *Ilm AI* — your personal learning companion.\n\n"
        "I can:\n"
        "• Send daily study reminders\n"
        "• Run a quick 5-question quiz\n"
        "• Track your learning streak\n"
        "• Send daily SAT/IELTS practice questions\n\n"
        "*First step:* link your web account with `/link`\n\n"
        "*Commands:*\n"
        "/quiz — 5-question quiz\n"
        "/satpractice — toggle daily SAT question (07:00 Tashkent)\n"
        "/satquiz — instant SAT/IELTS question\n"
        "/reminder 09:00 — daily reminder (Tashkent time)\n"
        "/streak — your streak\n"
        "/help — all commands",
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📚 *Ilm AI Bot Commands*\n\n"
        "/link — connect your web account\n"
        "/quiz — 5 questions from your materials\n"
        "/satpractice — toggle daily SAT/IELTS question at 07:00 Tashkent\n"
        "/satquiz — get an instant SAT/IELTS practice question\n"
        "/reminder 18:30 — set daily reminder\n"
        "/streak — consecutive study days\n"
        "/cancel — cancel linking\n\n"
        "Sign up on the website, upload a PDF, then use /link here.",
        parse_mode="Markdown",
    )


async def link_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Send your *website account email*:\n"
        "(e.g. learner@example.com)",
        parse_mode="Markdown",
    )
    return LINK_EMAIL


async def link_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["link_email"] = update.message.text.strip().lower()
    await update.message.reply_text("Now send your password:")
    return LINK_PASSWORD


async def link_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = context.user_data.get("link_email", "")
    password = update.message.text.strip()
    result = link_telegram(email, password, update.effective_chat.id)

    if not result["ok"]:
        await update.message.reply_text(
            f"❌ {result['error']}\nTry again with /link"
        )
        return ConversationHandler.END

    user = result["user"]
    await update.message.reply_text(
        f"✅ Linked! Hello, {user['name']}!\n\n"
        f"Reminder time: {user.get('reminder_time', '09:00')}\n"
        "Change it: /reminder 09:00\n"
        "Start a quiz: /quiz"
    )
    return ConversationHandler.END


async def link_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Linking cancelled.")
    return ConversationHandler.END


async def streak_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = _linked_user(update)
    if not user:
        await update.message.reply_text("Link your account first with /link")
        return

    days = user.get("streak_days", 0)
    last = user.get("last_study_date") or "none yet"
    if days >= 7:
        msg = f"🔥 Amazing! {days}-day streak! Keep going!"
    elif days >= 3:
        msg = f"⭐ Great! {days} days in a row!"
    else:
        msg = f"📈 Streak: {days} days\nLast activity: {last}"

    await update.message.reply_text(msg)


async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = _linked_user(update)
    if not user:
        await update.message.reply_text("Link your account first with /link")
        return

    if not context.args:
        current = user.get("reminder_time", "09:00")
        await update.message.reply_text(
            f"Current reminder: *{current}* (Asia/Tashkent)\n"
            "Change: `/reminder 18:30`",
            parse_mode="Markdown",
        )
        return

    time_str = context.args[0]
    if not re.match(r"^\d{1,2}:\d{2}$", time_str):
        await update.message.reply_text("Use format HH:MM — e.g. 09:00 or 18:30")
        return

    hour, minute = map(int, time_str.split(":"))
    if hour > 23 or minute > 59:
        await update.message.reply_text("Invalid time. Example: 09:00")
        return

    normalized = f"{hour:02d}:{minute:02d}"
    set_reminder_time(user["id"], normalized)
    await update.message.reply_text(
        f"✅ Daily reminder set to *{normalized}* (Asia/Tashkent)",
        parse_mode="Markdown",
    )


async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = _linked_user(update)
    if not user:
        await update.message.reply_text("Link your account first with /link")
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("⏳ Preparing your quiz...")

    data = generate_quiz(user["id"], num_questions=5, difficulty="solid understanding")
    if "error" in data:
        await update.message.reply_text(f"❌ {data['error']}")
        return

    questions = data.get("questions", [])
    if not questions:
        await update.message.reply_text("No questions generated. Upload more materials.")
        return

    quiz_sessions[chat_id] = {
        "user_id": user["id"],
        "questions": questions,
        "index": 0,
        "score": 0,
        "context": data.get("_context", ""),
    }
    await send_question(chat_id, context)


async def send_question(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = quiz_sessions.get(chat_id)
    if not session:
        return

    idx = session["index"]
    questions = session["questions"]
    if idx >= len(questions):
        await finish_quiz(chat_id, context)
        return

    q = questions[idx]
    text = f"📝 Question {idx + 1}/{len(questions)}\n\n{q['question']}"
    options = q.get("options", [])

    if options:
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"ans:{idx}:{i}")]
            for i, opt in enumerate(options)
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        session["awaiting_text"] = True
        await context.bot.send_message(
            chat_id=chat_id,
            text=text + "\n\nType your answer as a message.",
        )


async def on_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id
    session = quiz_sessions.get(chat_id)
    if not session:
        await query.edit_message_text("Session ended. Start again with /quiz")
        return

    _, q_idx, opt_idx = query.data.split(":")
    q_idx, opt_idx = int(q_idx), int(opt_idx)
    if q_idx != session["index"]:
        return

    q = session["questions"][q_idx]
    await evaluate_and_next(query, session, q, q["options"][opt_idx], context)


async def on_text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    session = quiz_sessions.get(chat_id)
    if not session or not session.get("awaiting_text"):
        return

    session["awaiting_text"] = False
    q = session["questions"][session["index"]]
    result = check_answer(
        q["question"],
        update.message.text.strip(),
        q.get("correct_answer", ""),
        session["context"],
        user_id=session["user_id"],
    )
    if result.get("is_correct"):
        session["score"] += 1

    await update.message.reply_text(
        f"{'✅' if result.get('is_correct') else '❌'} {result.get('feedback', '')}\n\n"
        f"💡 {result.get('explanation', q.get('explanation', ''))}"
    )
    session["index"] += 1
    await send_question(chat_id, context)


async def evaluate_and_next(query, session, q, user_answer, context) -> None:
    result = check_answer(
        q["question"],
        user_answer,
        q.get("correct_answer", ""),
        session["context"],
        user_id=session["user_id"],
    )
    if result.get("is_correct"):
        session["score"] += 1

    icon = "✅" if result.get("is_correct") else "❌"
    await query.edit_message_text(
        f"{icon} {result.get('feedback', '')}\n\n💡 {result.get('explanation', q.get('explanation', ''))}"
    )
    session["index"] += 1
    await send_question(query.message.chat_id, context)


async def finish_quiz(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = quiz_sessions.pop(chat_id, None)
    if not session:
        return

    total = len(session["questions"])
    score = session["score"]
    streak_info = record_study_activity(session["user_id"])
    streak_days = streak_info["streak_days"]
    pct = int((score / total) * 100) if total else 0

    # Save quiz session to history (for gap detection)
    try:
        from services.quiz_history import add_session
        results = [
            {
                "question": q.get("question", ""),
                "user_answer": session.get("answers", {}).get(str(i), ""),
                "correct_answer": q.get("correct_answer", ""),
                "is_correct": session.get("answers", {}).get(str(i), "") == q.get("correct_answer", ""),
                "topic": q.get("topic", "general"),
                "explanation": q.get("explanation", ""),
            }
            for i, q in enumerate(session["questions"])
        ]
        add_session(session["user_id"], score, total, "medium", results)
    except Exception as e:
        logger.warning("Failed to save telegram quiz session: %s", e)

    if pct >= 80:
        praise = "🌟 Excellent work!"
    elif pct >= 50:
        praise = "👍 Good effort — review your materials and try again."
    else:
        praise = "📖 Review your uploaded materials and try again."

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"🏁 Quiz complete!\n\n"
            f"Score: {score}/{total} ({pct}%)\n"
            f"{praise}\n\n"
            f"🔥 Streak: {streak_days} days\n"
            "Another quiz: /quiz"
        ),
    )

    if streak_days in (3, 7, 14, 30):
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🎉 Congrats! {streak_days} days in a row — keep it up!",
        )


async def send_daily_reminders(context: ContextTypes.DEFAULT_TYPE) -> None:
    from services.users import users_with_reminder_at

    now = datetime.datetime.now(TZ)
    for user in users_with_reminder_at(now.hour, now.minute):
        chat_id = user["telegram_chat_id"]
        streak = user.get("streak_days", 0)
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"📚 Hi {user['name']}! Time to study.\n\n"
                    f"🔥 Streak: {streak} days\n"
                    "Quick quiz: /quiz"
                ),
            )
        except Exception as e:
            logger.warning("Reminder failed for %s: %s", chat_id, e)


# ===========================================================================
# SAT/IELTS Telegram helpers (Tasks 13.1, 13.2, 13.3)
# ===========================================================================


async def _send_sat_question_to_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Select one SAT question for user_id and send it to chat_id as an inline keyboard.

    Returns True on success, False if no question is available or limit reached.
    """
    from services.db import SessionLocal
    from services.question_bank import select_questions_for_session
    from services.sat_session_engine import create_session
    from services.sat_subscription import can_attempt_sat_ielts, record_sat_ielts_attempt
    from services.models import SatIeltsSession
    from services.sat_session_engine import compute_domain_accuracy

    db = SessionLocal()
    try:
        ok, msg = can_attempt_sat_ielts(user_id, db)
        if not ok:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ {msg}")
            return False

        # Prefer weak domains for this user
        sessions = (
            db.query(SatIeltsSession)
            .filter(
                SatIeltsSession.user_id == user_id,
                SatIeltsSession.exam_type == "SAT",
                SatIeltsSession.status == "completed",
            )
            .order_by(SatIeltsSession.started_at.desc())
            .limit(10)
            .all()
        )
        domain_acc = compute_domain_accuracy(sessions) if sessions else {}
        weak_domains = [d for d, acc in domain_acc.items() if acc < 0.70]
        target_domain = weak_domains[0] if weak_domains else None

        questions = select_questions_for_session(
            db, exam_type="SAT", domain=target_domain, difficulty="medium", count=1
        )
        if not questions:
            questions = select_questions_for_session(
                db, exam_type="SAT", domain=None, difficulty="medium", count=1
            )
        if not questions:
            await context.bot.send_message(
                chat_id=chat_id,
                text="📚 No SAT questions available yet. Seed the question bank first.",
            )
            return False

        q = questions[0]
        session = create_session(
            db=db,
            user_id=user_id,
            exam_type="SAT",
            questions=questions,
            timed=False,
            session_type="practice",
        )
        record_sat_ielts_attempt(user_id, 1, db)

        # Store pending state
        sat_pending[chat_id] = {
            "session_id": session.id,
            "question": {
                "id": q.id,
                "text": q.question_text,
                "options": q.options or [],
                "correct_answer": q.correct_answer,
                "question_type": q.question_type,
                "domain": q.domain,
            },
            "user_id": user_id,
        }

        domain_label = f"[{q.domain}]" if q.domain else ""
        diff_label = q.difficulty.capitalize()
        header = f"🎯 SAT Practice {domain_label} ({diff_label})\n\n{q.question_text}"

        if q.question_type == "mcq" and q.options:
            keyboard = [
                [InlineKeyboardButton(opt, callback_data=f"sat_ans:{i}")]
                for i, opt in enumerate(q.options)
            ]
            await context.bot.send_message(
                chat_id=chat_id,
                text=header,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=header + "\n\n✏️ Type your answer as a message.",
            )
        return True
    except Exception as e:
        logger.error("SAT question send failed for chat_id=%s: %s", chat_id, e)
        return False
    finally:
        db.close()


async def send_daily_sat_question(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Scheduled daily job: send one SAT question to each opted-in user at 07:00 Tashkent."""
    from services.db import SessionLocal
    from services.models import SatIeltsUserPrefs, User

    db = SessionLocal()
    try:
        opted_in = (
            db.query(SatIeltsUserPrefs, User)
            .join(User, User.id == SatIeltsUserPrefs.user_id)
            .filter(
                SatIeltsUserPrefs.telegram_sat_enabled == True,
                User.telegram_chat_id.isnot(None),
            )
            .all()
        )
    finally:
        db.close()

    for prefs, user in opted_in:
        chat_id_str = user.telegram_chat_id
        if not chat_id_str:
            continue
        try:
            chat_id = int(chat_id_str)
        except (ValueError, TypeError):
            continue
        try:
            await _send_sat_question_to_user(chat_id, user.id, context)
        except Exception as e:
            logger.warning("Daily SAT question failed for user_id=%s: %s", user.id, e)


async def satpractice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/satpractice — toggle daily SAT question subscription."""
    user = _linked_user(update)
    if not user:
        await update.message.reply_text("Link your account first with /link")
        return

    from services.db import SessionLocal
    from services.models import SatIeltsUserPrefs

    db = SessionLocal()
    try:
        prefs = db.query(SatIeltsUserPrefs).filter(
            SatIeltsUserPrefs.user_id == user["id"]
        ).first()
        if not prefs:
            prefs = SatIeltsUserPrefs(user_id=user["id"], telegram_sat_enabled=False)
            db.add(prefs)
            db.commit()
            db.refresh(prefs)

        prefs.telegram_sat_enabled = not prefs.telegram_sat_enabled
        db.commit()
        status = "enabled ✅" if prefs.telegram_sat_enabled else "disabled ❌"
        await update.message.reply_text(
            f"Daily SAT practice question {status}.\n"
            + ("You'll receive a question every day at 07:00 Tashkent time." if prefs.telegram_sat_enabled else "Use /satpractice again to re-enable.")
        )
    finally:
        db.close()


async def satquiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/satquiz — immediately send one SAT question."""
    user = _linked_user(update)
    if not user:
        await update.message.reply_text("Link your account first with /link")
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("⏳ Fetching a SAT question...")
    await _send_sat_question_to_user(chat_id, user["id"], context)


async def on_sat_tg_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback query from SAT inline keyboard answer buttons."""
    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id
    pending = sat_pending.get(chat_id)
    if not pending:
        await query.edit_message_text("⏱ Session expired. Use /satquiz for a new question.")
        return

    # Extract the chosen option index from callback data: "sat_ans:<index>"
    data = query.data  # e.g. "sat_ans:2"
    try:
        opt_idx = int(data.split(":")[1])
    except (IndexError, ValueError):
        await query.edit_message_text("Invalid answer. Use /satquiz to try again.")
        sat_pending.pop(chat_id, None)
        return

    q_info = pending["question"]
    options = q_info.get("options", [])
    if opt_idx < 0 or opt_idx >= len(options):
        await query.edit_message_text("Invalid option. Use /satquiz to try again.")
        sat_pending.pop(chat_id, None)
        return

    chosen_answer = options[opt_idx]
    correct_answer = q_info.get("correct_answer", "")
    is_correct = chosen_answer.strip() == correct_answer.strip()

    # Record answer and finalise session
    from services.db import SessionLocal
    from services.sat_session_engine import record_answer, finalise_session

    db = SessionLocal()
    try:
        record_answer(
            db,
            session_id=pending["session_id"],
            question_id=q_info["id"],
            answer=chosen_answer,
            elapsed_ms=0,
        )
        finalise_session(db, pending["session_id"])
    except Exception as e:
        logger.warning("SAT answer record failed: %s", e)
    finally:
        db.close()

    # Clear pending state
    sat_pending.pop(chat_id, None)

    icon = "✅" if is_correct else "❌"
    feedback = (
        f"{icon} {'Correct!' if is_correct else 'Incorrect.'}\n\n"
        f"Your answer: *{chosen_answer}*\n"
    )
    if not is_correct:
        feedback += f"Correct answer: *{correct_answer}*\n"
    feedback += "\nUse /satquiz for another question."

    await query.edit_message_text(feedback, parse_mode="Markdown")


def build_application() -> Application:
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from .env")

    app = Application.builder().token(token).build()
    link_conv = ConversationHandler(
        entry_points=[CommandHandler("link", link_start)],
        states={
            LINK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, link_email)],
            LINK_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, link_password)
            ],
        },
        fallbacks=[CommandHandler("cancel", link_cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(link_conv)
    app.add_handler(CommandHandler("quiz", quiz_cmd))
    app.add_handler(CommandHandler("streak", streak_cmd))
    app.add_handler(CommandHandler("reminder", reminder_cmd))
    app.add_handler(CommandHandler("satpractice", satpractice_cmd))
    app.add_handler(CommandHandler("satquiz", satquiz_cmd))
    app.add_handler(CallbackQueryHandler(on_sat_tg_answer, pattern=r"^sat_ans:"))
    app.add_handler(CallbackQueryHandler(on_quiz_answer, pattern=r"^ans:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text_answer))

    if app.job_queue:
        app.job_queue.run_repeating(send_daily_reminders, interval=60, first=10)
        app.job_queue.run_daily(
            send_daily_sat_question,
            time=datetime.time(7, 0, tzinfo=TZ),
        )

    return app


def main() -> None:
    app = build_application()
    logger.info("Ilm AI Telegram bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
