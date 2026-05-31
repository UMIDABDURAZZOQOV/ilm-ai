import logging
import os
import re
from datetime import datetime
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


def _linked_user(update: Update):
    return find_user_by_chat_id(update.effective_chat.id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to *Ilm AI* — your personal learning companion.\n\n"
        "I can:\n"
        "• Send daily study reminders\n"
        "• Run a quick 5-question quiz\n"
        "• Track your learning streak\n\n"
        "*First step:* link your web account with `/link`\n\n"
        "*Commands:*\n"
        "/quiz — 5-question quiz\n"
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

    data = generate_quiz(user["id"], num_questions=5, difficulty="medium")
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

    now = datetime.now(TZ)
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


def build_application() -> Application:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
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
    app.add_handler(CallbackQueryHandler(on_quiz_answer, pattern=r"^ans:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text_answer))

    if app.job_queue:
        app.job_queue.run_repeating(send_daily_reminders, interval=60, first=10)

    return app


def main() -> None:
    app = build_application()
    logger.info("Ilm AI Telegram bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
