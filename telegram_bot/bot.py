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

token = os.getenv("TELEGRAM_BOT_TOKEN", "")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TZ = ZoneInfo("Asia/Tashkent")
LINK_EMAIL, LINK_PASSWORD = range(2)
quiz_sessions: dict[int, dict] = {}
sat_pending: dict[int, dict] = {}

# Per-chat language store: {chat_id: "uz"|"ru"|"en"}
chat_languages: dict[int, str] = {}


# ── Multilingual strings ──────────────────────────────────────────────────────

STRINGS = {
    "choose_lang": {
        "uz": "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇬🇧 Choose language",
        "ru": "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇬🇧 Choose language",
        "en": "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇬🇧 Choose language",
    },
    "lang_set": {
        "uz": "✅ Til o'rnatildi: O'zbek tili 🇺🇿",
        "ru": "✅ Язык установлен: Русский 🇷🇺",
        "en": "✅ Language set: English 🇬🇧",
    },
    "welcome": {
        "uz": (
            "Xush kelibsiz *Ilm AI* ga — shaxsiy o'quv yordamchingiz! 📚\n\n"
            "Men quyidagilarni qila olaman:\n"
            "• Kunlik o'qish eslatmalarini yuborish\n"
            "• 5 savollik tezkor quiz o'tkazish\n"
            "• O'quv seriyangizni kuzatish\n"
            "• Kunlik SAT/IELTS mashq savollari\n\n"
            "*Birinchi qadam:* /link bilan veb akkauntingizni ulang\n\n"
            "*Buyruqlar:*\n"
            "/quiz — 5 savollik quiz\n"
            "/satpractice — kunlik SAT savolini yoqish/o'chirish\n"
            "/satquiz — tezkor SAT/IELTS savoli\n"
            "/reminder 09:00 — kunlik eslatma vaqti\n"
            "/streak — seriyangiz\n"
            "/language — tilni o'zgartirish\n"
            "/help — barcha buyruqlar"
        ),
        "ru": (
            "Добро пожаловать в *Ilm AI* — ваш личный помощник в учёбе! 📚\n\n"
            "Я умею:\n"
            "• Отправлять ежедневные напоминания\n"
            "• Проводить быстрый квиз из 5 вопросов\n"
            "• Отслеживать вашу серию дней\n"
            "• Присылать ежедневные вопросы SAT/IELTS\n\n"
            "*Первый шаг:* свяжите аккаунт командой /link\n\n"
            "*Команды:*\n"
            "/quiz — квиз из 5 вопросов\n"
            "/satpractice — вкл/выкл ежедневный SAT вопрос\n"
            "/satquiz — мгновенный вопрос SAT/IELTS\n"
            "/reminder 09:00 — время напоминания\n"
            "/streak — ваша серия дней\n"
            "/language — сменить язык\n"
            "/help — все команды"
        ),
        "en": (
            "Welcome to *Ilm AI* — your personal learning companion! 📚\n\n"
            "I can:\n"
            "• Send daily study reminders\n"
            "• Run a quick 5-question quiz\n"
            "• Track your learning streak\n"
            "• Send daily SAT/IELTS practice questions\n\n"
            "*First step:* link your web account with /link\n\n"
            "*Commands:*\n"
            "/quiz — 5-question quiz\n"
            "/satpractice — toggle daily SAT question\n"
            "/satquiz — instant SAT/IELTS question\n"
            "/reminder 09:00 — daily reminder time\n"
            "/streak — your streak\n"
            "/language — change language\n"
            "/help — all commands"
        ),
    },
    "help": {
        "uz": (
            "📚 *Ilm AI Bot Buyruqlari*\n\n"
            "/link — veb akkauntingizni ulash\n"
            "/quiz — materiallaringizdan 5 ta savol\n"
            "/satpractice — kunlik SAT/IELTS savolini yoq/o'chir (07:00 Toshkent)\n"
            "/satquiz — tezkor SAT/IELTS savoli\n"
            "/reminder 18:30 — kunlik eslatma vaqtini o'rnatish\n"
            "/streak — ketma-ket o'qish kunlari\n"
            "/language — tilni o'zgartirish\n"
            "/cancel — bekor qilish\n\n"
            "Veb saytda ro'yxatdan o'ting, PDF yuklang, so'ng /link buyrug'ini ishlating."
        ),
        "ru": (
            "📚 *Команды Ilm AI Bot*\n\n"
            "/link — подключить веб-аккаунт\n"
            "/quiz — 5 вопросов из ваших материалов\n"
            "/satpractice — вкл/выкл ежедневный SAT/IELTS вопрос (07:00 Ташкент)\n"
            "/satquiz — мгновенный SAT/IELTS вопрос\n"
            "/reminder 18:30 — установить время напоминания\n"
            "/streak — дни подряд\n"
            "/language — сменить язык\n"
            "/cancel — отмена\n\n"
            "Зарегистрируйтесь на сайте, загрузите PDF, затем используйте /link."
        ),
        "en": (
            "📚 *Ilm AI Bot Commands*\n\n"
            "/link — connect your web account\n"
            "/quiz — 5 questions from your materials\n"
            "/satpractice — toggle daily SAT/IELTS question at 07:00 Tashkent\n"
            "/satquiz — instant SAT/IELTS practice question\n"
            "/reminder 18:30 — set daily reminder\n"
            "/streak — consecutive study days\n"
            "/language — change language\n"
            "/cancel — cancel linking\n\n"
            "Sign up on the website, upload a PDF, then use /link here."
        ),
    },
    "link_ask_email": {
        "uz": "Veb akkaunt *email manzilingizni* yuboring:\n(masalan: learner@example.com)",
        "ru": "Отправьте *email вашего веб-аккаунта*:\n(например: learner@example.com)",
        "en": "Send your *website account email*:\n(e.g. learner@example.com)",
    },
    "link_ask_password": {
        "uz": "Endi parolingizni yuboring:",
        "ru": "Теперь отправьте ваш пароль:",
        "en": "Now send your password:",
    },
    "link_success": {
        "uz": "✅ Ulandi! Salom, {name}!\n\nEslatma vaqti: {time}\nO'zgartirish: /reminder 09:00\nQuiz boshlash: /quiz",
        "ru": "✅ Подключено! Привет, {name}!\n\nВремя напоминания: {time}\nИзменить: /reminder 09:00\nНачать квиз: /quiz",
        "en": "✅ Linked! Hello, {name}!\n\nReminder time: {time}\nChange it: /reminder 09:00\nStart a quiz: /quiz",
    },
    "link_fail": {
        "uz": "❌ {error}\n/link bilan qayta urinib ko'ring",
        "ru": "❌ {error}\nПопробуйте снова с /link",
        "en": "❌ {error}\nTry again with /link",
    },
    "link_cancel": {
        "uz": "Bekor qilindi.",
        "ru": "Отменено.",
        "en": "Linking cancelled.",
    },
    "not_linked": {
        "uz": "Avval /link bilan akkauntingizni ulang",
        "ru": "Сначала подключите аккаунт командой /link",
        "en": "Link your account first with /link",
    },
    "quiz_preparing": {
        "uz": "⏳ Quiz tayyorlanmoqda...",
        "ru": "⏳ Квиз готовится...",
        "en": "⏳ Preparing your quiz...",
    },
    "quiz_no_questions": {
        "uz": "Savol topilmadi. Ko'proq material yuklang.",
        "ru": "Вопросы не найдены. Загрузите больше материалов.",
        "en": "No questions generated. Upload more materials.",
    },
    "quiz_complete": {
        "uz": "🏁 Quiz tugadi!\n\nNatija: {score}/{total} ({pct}%)\n{praise}\n\n🔥 Seriya: {streak} kun\nYana quiz: /quiz",
        "ru": "🏁 Квиз завершён!\n\nРезультат: {score}/{total} ({pct}%)\n{praise}\n\n🔥 Серия: {streak} дней\nЕщё квиз: /quiz",
        "en": "🏁 Quiz complete!\n\nScore: {score}/{total} ({pct}%)\n{praise}\n\n🔥 Streak: {streak} days\nAnother quiz: /quiz",
    },
    "praise_high": {
        "uz": "🌟 Ajoyib natija!",
        "ru": "🌟 Отличный результат!",
        "en": "🌟 Excellent work!",
    },
    "praise_mid": {
        "uz": "👍 Yaxshi urinish — materiallarni ko'rib qayta sinab ko'ring.",
        "ru": "👍 Хорошая попытка — повторите материалы и попробуйте снова.",
        "en": "👍 Good effort — review your materials and try again.",
    },
    "praise_low": {
        "uz": "📖 Yuklangan materiallaringizni ko'rib chiqing va qayta sinab ko'ring.",
        "ru": "📖 Повторите загруженные материалы и попробуйте снова.",
        "en": "📖 Review your uploaded materials and try again.",
    },
    "streak_amazing": {
        "uz": "🔥 Ajoyib! {days} kunlik seriya! Davom eting!",
        "ru": "🔥 Потрясающе! {days}-дневная серия! Продолжайте!",
        "en": "🔥 Amazing! {days}-day streak! Keep going!",
    },
    "streak_good": {
        "uz": "⭐ Zo'r! {days} kun ketma-ket!",
        "ru": "⭐ Отлично! {days} дней подряд!",
        "en": "⭐ Great! {days} days in a row!",
    },
    "streak_basic": {
        "uz": "📈 Seriya: {days} kun\nOxirgi faollik: {last}",
        "ru": "📈 Серия: {days} дней\nПоследняя активность: {last}",
        "en": "📈 Streak: {days} days\nLast activity: {last}",
    },
    "reminder_current": {
        "uz": "Joriy eslatma: *{time}* (Asia/Tashkent)\nO'zgartirish: `/reminder 18:30`",
        "ru": "Текущее напоминание: *{time}* (Asia/Tashkent)\nИзменить: `/reminder 18:30`",
        "en": "Current reminder: *{time}* (Asia/Tashkent)\nChange: `/reminder 18:30`",
    },
    "reminder_format_err": {
        "uz": "HH:MM formatini ishlating — masalan 09:00 yoki 18:30",
        "ru": "Используйте формат ЧЧ:ММ — например 09:00 или 18:30",
        "en": "Use format HH:MM — e.g. 09:00 or 18:30",
    },
    "reminder_invalid": {
        "uz": "Noto'g'ri vaqt. Masalan: 09:00",
        "ru": "Неверное время. Пример: 09:00",
        "en": "Invalid time. Example: 09:00",
    },
    "reminder_set": {
        "uz": "✅ Kunlik eslatma *{time}* ga o'rnatildi (Asia/Tashkent)",
        "ru": "✅ Ежедневное напоминание установлено на *{time}* (Asia/Tashkent)",
        "en": "✅ Daily reminder set to *{time}* (Asia/Tashkent)",
    },
    "daily_reminder": {
        "uz": "📚 Salom {name}! O'qish vaqti.\n\n🔥 Seriya: {streak} kun\nTezkor quiz: /quiz",
        "ru": "📚 Привет {name}! Время учиться.\n\n🔥 Серия: {streak} дней\nБыстрый квиз: /quiz",
        "en": "📚 Hi {name}! Time to study.\n\n🔥 Streak: {streak} days\nQuick quiz: /quiz",
    },
    "streak_milestone": {
        "uz": "🎉 Tabriklar! {days} kun ketma-ket — shunday davom eting!",
        "ru": "🎉 Поздравляем! {days} дней подряд — продолжайте в том же духе!",
        "en": "🎉 Congrats! {days} days in a row — keep it up!",
    },
    "satpractice_on": {
        "uz": "Kunlik SAT mashq savoli *yoqildi* ✅\nHar kuni soat 07:00 da (Toshkent vaqti) savol keladi.",
        "ru": "Ежедневный SAT вопрос *включён* ✅\nВопрос будет приходить каждый день в 07:00 (Ташкент).",
        "en": "Daily SAT practice question *enabled* ✅\nYou'll receive a question every day at 07:00 Tashkent time.",
    },
    "satpractice_off": {
        "uz": "Kunlik SAT mashq savoli *o'chirildi* ❌\nQayta yoqish: /satpractice",
        "ru": "Ежедневный SAT вопрос *отключён* ❌\nВключить снова: /satpractice",
        "en": "Daily SAT practice question *disabled* ❌\nUse /satpractice to re-enable.",
    },
    "sat_fetching": {
        "uz": "⏳ SAT savoli tayyorlanmoqda...",
        "ru": "⏳ Получаю SAT вопрос...",
        "en": "⏳ Fetching a SAT question...",
    },
    "sat_expired": {
        "uz": "⏱ Sessiya tugadi. Yangi savol: /satquiz",
        "ru": "⏱ Сессия истекла. Новый вопрос: /satquiz",
        "en": "⏱ Session expired. Use /satquiz for a new question.",
    },
    "sat_correct": {
        "uz": "✅ To'g'ri!\n\nJavobingiz: *{answer}*\n\nYana savol: /satquiz",
        "ru": "✅ Правильно!\n\nВаш ответ: *{answer}*\n\nЕщё вопрос: /satquiz",
        "en": "✅ Correct!\n\nYour answer: *{answer}*\n\nAnother question: /satquiz",
    },
    "sat_wrong": {
        "uz": "❌ Noto'g'ri.\n\nJavobingiz: *{user_answer}*\nTo'g'ri javob: *{correct}*\n\nYana savol: /satquiz",
        "ru": "❌ Неверно.\n\nВаш ответ: *{user_answer}*\nПравильный ответ: *{correct}*\n\nЕщё вопрос: /satquiz",
        "en": "❌ Incorrect.\n\nYour answer: *{user_answer}*\nCorrect answer: *{correct}*\n\nAnother question: /satquiz",
    },
    "q_label": {
        "uz": "📝 Savol {n}/{total}",
        "ru": "📝 Вопрос {n}/{total}",
        "en": "📝 Question {n}/{total}",
    },
    "q_type_text": {
        "uz": "\n\n✏️ Javobingizni xabar sifatida yuboring.",
        "ru": "\n\n✏️ Отправьте ваш ответ как сообщение.",
        "en": "\n\nType your answer as a message.",
    },
    "correct_feedback": {
        "uz": "✅ {feedback}\n\n💡 {explanation}",
        "ru": "✅ {feedback}\n\n💡 {explanation}",
        "en": "✅ {feedback}\n\n💡 {explanation}",
    },
    "wrong_feedback": {
        "uz": "❌ {feedback}\n\n💡 {explanation}",
        "ru": "❌ {feedback}\n\n💡 {explanation}",
        "en": "❌ {feedback}\n\n💡 {explanation}",
    },
}


def lang(chat_id: int) -> str:
    """Get language for a chat_id, default to 'uz' (most users are Uzbek)."""
    return chat_languages.get(chat_id, "uz")


def s(key: str, chat_id: int, **kwargs) -> str:
    """Get localized string. Falls back to 'en'."""
    lg = lang(chat_id)
    text = STRINGS.get(key, {}).get(lg) or STRINGS.get(key, {}).get("en", key)
    return text.format(**kwargs) if kwargs else text


# ── Helpers ───────────────────────────────────────────────────────────────────

def _linked_user(update: Update):
    return find_user_by_chat_id(update.effective_chat.id)


# ── /start — language selection ───────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show language selector first, then welcome in chosen language."""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="setlang:uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="setlang:en"),
        ]
    ]
    await update.message.reply_text(
        s("choose_lang", update.effective_chat.id),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def on_lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback, then show welcome message."""
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    chosen = query.data.split(":")[1]  # "uz", "ru", or "en"
    chat_languages[chat_id] = chosen
    await query.edit_message_text(s("lang_set", chat_id))
    await context.bot.send_message(
        chat_id=chat_id,
        text=s("welcome", chat_id),
        parse_mode="Markdown",
    )


async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/language — change language at any time."""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="setlang:uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="setlang:en"),
        ]
    ]
    await update.message.reply_text(
        s("choose_lang", update.effective_chat.id),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text(s("help", chat_id), parse_mode="Markdown")


# ── /link ─────────────────────────────────────────────────────────────────────

async def link_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    await update.message.reply_text(s("link_ask_email", chat_id), parse_mode="Markdown")
    return LINK_EMAIL


async def link_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["link_email"] = update.message.text.strip().lower()
    await update.message.reply_text(s("link_ask_password", update.effective_chat.id))
    return LINK_PASSWORD


async def link_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    email = context.user_data.get("link_email", "")
    password = update.message.text.strip()
    result = link_telegram(email, password, chat_id)

    if not result["ok"]:
        await update.message.reply_text(s("link_fail", chat_id, error=result["error"]))
        return ConversationHandler.END

    user = result["user"]
    await update.message.reply_text(
        s("link_success", chat_id, name=user["name"], time=user.get("reminder_time", "09:00"))
    )
    return ConversationHandler.END


async def link_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(s("link_cancel", update.effective_chat.id))
    return ConversationHandler.END


# ── /streak ───────────────────────────────────────────────────────────────────

async def streak_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = _linked_user(update)
    if not user:
        await update.message.reply_text(s("not_linked", chat_id))
        return

    days = user.get("streak_days", 0)
    last = user.get("last_study_date") or (
        "yo'q" if lang(chat_id) == "uz" else "нет" if lang(chat_id) == "ru" else "none yet"
    )
    if days >= 7:
        msg = s("streak_amazing", chat_id, days=days)
    elif days >= 3:
        msg = s("streak_good", chat_id, days=days)
    else:
        msg = s("streak_basic", chat_id, days=days, last=last)
    await update.message.reply_text(msg)


# ── /reminder ─────────────────────────────────────────────────────────────────

async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = _linked_user(update)
    if not user:
        await update.message.reply_text(s("not_linked", chat_id))
        return

    if not context.args:
        current = user.get("reminder_time", "09:00")
        await update.message.reply_text(
            s("reminder_current", chat_id, time=current), parse_mode="Markdown"
        )
        return

    time_str = context.args[0]
    if not re.match(r"^\d{1,2}:\d{2}$", time_str):
        await update.message.reply_text(s("reminder_format_err", chat_id))
        return

    hour, minute = map(int, time_str.split(":"))
    if hour > 23 or minute > 59:
        await update.message.reply_text(s("reminder_invalid", chat_id))
        return

    normalized = f"{hour:02d}:{minute:02d}"
    set_reminder_time(user["id"], normalized)
    await update.message.reply_text(
        s("reminder_set", chat_id, time=normalized), parse_mode="Markdown"
    )


# ── /quiz ─────────────────────────────────────────────────────────────────────

async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = _linked_user(update)
    if not user:
        await update.message.reply_text(s("not_linked", chat_id))
        return

    await update.message.reply_text(s("quiz_preparing", chat_id))

    data = generate_quiz(user["id"], num_questions=5, difficulty="solid understanding")
    if "error" in data:
        await update.message.reply_text(f"❌ {data['error']}")
        return

    questions = data.get("questions", [])
    if not questions:
        await update.message.reply_text(s("quiz_no_questions", chat_id))
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
    label = s("q_label", chat_id, n=idx + 1, total=len(questions))
    text = f"{label}\n\n{q['question']}"
    options = q.get("options", [])

    if options:
        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"ans:{idx}:{i}")]
            for i, opt in enumerate(options)
        ]
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        session["awaiting_text"] = True
        await context.bot.send_message(
            chat_id=chat_id, text=text + s("q_type_text", chat_id)
        )


async def on_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    session = quiz_sessions.get(chat_id)
    if not session:
        await query.edit_message_text(s("quiz_preparing", chat_id))
        return

    _, q_idx, opt_idx = query.data.split(":")
    q_idx, opt_idx = int(q_idx), int(opt_idx)
    if q_idx != session["index"]:
        return

    q = session["questions"][q_idx]
    await evaluate_and_next(query, session, q, q["options"][opt_idx], context, chat_id)


async def on_text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    session = quiz_sessions.get(chat_id)
    if not session or not session.get("awaiting_text"):
        return

    session["awaiting_text"] = False
    q = session["questions"][session["index"]]
    result = check_answer(
        q["question"], update.message.text.strip(),
        q.get("correct_answer", ""), session["context"], user_id=session["user_id"],
    )
    if result.get("is_correct"):
        session["score"] += 1

    icon = "correct_feedback" if result.get("is_correct") else "wrong_feedback"
    await update.message.reply_text(
        s(icon, chat_id,
          feedback=result.get("feedback", ""),
          explanation=result.get("explanation", q.get("explanation", "")))
    )
    session["index"] += 1
    await send_question(chat_id, context)


async def evaluate_and_next(query, session, q, user_answer, context, chat_id) -> None:
    result = check_answer(
        q["question"], user_answer, q.get("correct_answer", ""),
        session["context"], user_id=session["user_id"],
    )
    if result.get("is_correct"):
        session["score"] += 1

    icon = "correct_feedback" if result.get("is_correct") else "wrong_feedback"
    await query.edit_message_text(
        s(icon, chat_id,
          feedback=result.get("feedback", ""),
          explanation=result.get("explanation", q.get("explanation", "")))
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

    praise_key = "praise_high" if pct >= 80 else "praise_mid" if pct >= 50 else "praise_low"
    await context.bot.send_message(
        chat_id=chat_id,
        text=s("quiz_complete", chat_id,
               score=score, total=total, pct=pct,
               praise=s(praise_key, chat_id),
               streak=streak_days),
    )

    if streak_days in (3, 7, 14, 30):
        await context.bot.send_message(
            chat_id=chat_id,
            text=s("streak_milestone", chat_id, days=streak_days),
        )


# ── Daily reminders ───────────────────────────────────────────────────────────

async def send_daily_reminders(context: ContextTypes.DEFAULT_TYPE) -> None:
    from services.users import users_with_reminder_at
    now = datetime.datetime.now(TZ)
    for user in users_with_reminder_at(now.hour, now.minute):
        chat_id_val = user["telegram_chat_id"]
        if not chat_id_val:
            continue
        try:
            cid = int(chat_id_val)
            await context.bot.send_message(
                chat_id=cid,
                text=s("daily_reminder", cid,
                       name=user["name"], streak=user.get("streak_days", 0)),
            )
        except Exception as e:
            logger.warning("Reminder failed for %s: %s", chat_id_val, e)


# ── SAT/IELTS helpers ─────────────────────────────────────────────────────────

async def _send_sat_question_to_user(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    from services.db import SessionLocal
    from services.question_bank import select_questions_for_session
    from services.sat_session_engine import create_session, compute_domain_accuracy
    from services.sat_subscription import can_attempt_sat_ielts, record_sat_ielts_attempt
    from services.models import SatIeltsSession

    db = SessionLocal()
    try:
        ok, msg = can_attempt_sat_ielts(user_id, db)
        if not ok:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ {msg}")
            return False

        sessions = (
            db.query(SatIeltsSession)
            .filter(SatIeltsSession.user_id == user_id, SatIeltsSession.exam_type == "SAT", SatIeltsSession.status == "completed")
            .order_by(SatIeltsSession.started_at.desc()).limit(10).all()
        )
        domain_acc = compute_domain_accuracy(sessions) if sessions else {}
        weak_domains = [d for d, acc in domain_acc.items() if acc < 0.70]
        target_domain = weak_domains[0] if weak_domains else None

        questions = select_questions_for_session(db, exam_type="SAT", domain=target_domain, difficulty="medium", count=1)
        if not questions:
            questions = select_questions_for_session(db, exam_type="SAT", domain=None, difficulty="medium", count=1)
        if not questions:
            await context.bot.send_message(chat_id=chat_id, text="📚 No SAT questions available yet.")
            return False

        q = questions[0]
        session = create_session(db=db, user_id=user_id, exam_type="SAT", questions=questions, timed=False, session_type="practice")
        record_sat_ielts_attempt(user_id, 1, db)

        sat_pending[chat_id] = {
            "session_id": session.id,
            "question": {"id": q.id, "text": q.question_text, "options": q.options or [], "correct_answer": q.correct_answer, "question_type": q.question_type, "domain": q.domain},
            "user_id": user_id,
        }

        domain_label = f"[{q.domain}]" if q.domain else ""
        header = f"🎯 SAT {domain_label} ({q.difficulty.capitalize()})\n\n{q.question_text}"

        if q.question_type == "mcq" and q.options:
            keyboard = [[InlineKeyboardButton(opt, callback_data=f"sat_ans:{i}")] for i, opt in enumerate(q.options)]
            await context.bot.send_message(chat_id=chat_id, text=header, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await context.bot.send_message(chat_id=chat_id, text=header + s("q_type_text", chat_id))
        return True
    except Exception as e:
        logger.error("SAT question send failed for chat_id=%s: %s", chat_id, e)
        return False
    finally:
        db.close()


async def send_daily_sat_question(context: ContextTypes.DEFAULT_TYPE) -> None:
    from services.db import SessionLocal
    from services.models import SatIeltsUserPrefs, User
    db = SessionLocal()
    try:
        opted_in = (
            db.query(SatIeltsUserPrefs, User)
            .join(User, User.id == SatIeltsUserPrefs.user_id)
            .filter(SatIeltsUserPrefs.telegram_sat_enabled == True, User.telegram_chat_id.isnot(None))
            .all()
        )
    finally:
        db.close()

    for prefs, user in opted_in:
        chat_id_str = user.telegram_chat_id
        if not chat_id_str:
            continue
        try:
            cid = int(chat_id_str)
            await _send_sat_question_to_user(cid, user.id, context)
        except Exception as e:
            logger.warning("Daily SAT question failed for user_id=%s: %s", user.id, e)


async def satpractice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = _linked_user(update)
    if not user:
        await update.message.reply_text(s("not_linked", chat_id))
        return

    from services.db import SessionLocal
    from services.models import SatIeltsUserPrefs
    db = SessionLocal()
    try:
        prefs = db.query(SatIeltsUserPrefs).filter(SatIeltsUserPrefs.user_id == user["id"]).first()
        if not prefs:
            prefs = SatIeltsUserPrefs(user_id=user["id"], telegram_sat_enabled=False)
            db.add(prefs)
            db.commit()
            db.refresh(prefs)
        prefs.telegram_sat_enabled = not prefs.telegram_sat_enabled
        db.commit()
        key = "satpractice_on" if prefs.telegram_sat_enabled else "satpractice_off"
        await update.message.reply_text(s(key, chat_id), parse_mode="Markdown")
    finally:
        db.close()


async def satquiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = _linked_user(update)
    if not user:
        await update.message.reply_text(s("not_linked", chat_id))
        return
    await update.message.reply_text(s("sat_fetching", chat_id))
    await _send_sat_question_to_user(chat_id, user["id"], context)


async def on_sat_tg_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    pending = sat_pending.get(chat_id)
    if not pending:
        await query.edit_message_text(s("sat_expired", chat_id))
        return

    data = query.data
    try:
        opt_idx = int(data.split(":")[1])
    except (IndexError, ValueError):
        sat_pending.pop(chat_id, None)
        return

    q_info = pending["question"]
    options = q_info.get("options", [])
    if opt_idx < 0 or opt_idx >= len(options):
        sat_pending.pop(chat_id, None)
        return

    chosen_answer = options[opt_idx]
    correct_answer = q_info.get("correct_answer", "")
    is_correct = chosen_answer.strip() == correct_answer.strip()

    from services.db import SessionLocal
    from services.sat_session_engine import record_answer, finalise_session
    db = SessionLocal()
    try:
        record_answer(db, session_id=pending["session_id"], question_id=q_info["id"], answer=chosen_answer, elapsed_ms=0)
        finalise_session(db, pending["session_id"])
    except Exception as e:
        logger.warning("SAT answer record failed: %s", e)
    finally:
        db.close()

    sat_pending.pop(chat_id, None)

    if is_correct:
        msg = s("sat_correct", chat_id, answer=chosen_answer)
    else:
        msg = s("sat_wrong", chat_id, user_answer=chosen_answer, correct=correct_answer)
    await query.edit_message_text(msg, parse_mode="Markdown")


# ── Application builder ───────────────────────────────────────────────────────

def build_application() -> Application:
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from .env")

    app = Application.builder().token(token).build()

    link_conv = ConversationHandler(
        entry_points=[CommandHandler("link", link_start)],
        states={
            LINK_EMAIL:    [MessageHandler(filters.TEXT & ~filters.COMMAND, link_email)],
            LINK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, link_password)],
        },
        fallbacks=[CommandHandler("cancel", link_cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("language", language_cmd))
    app.add_handler(link_conv)
    app.add_handler(CommandHandler("quiz", quiz_cmd))
    app.add_handler(CommandHandler("streak", streak_cmd))
    app.add_handler(CommandHandler("reminder", reminder_cmd))
    app.add_handler(CommandHandler("satpractice", satpractice_cmd))
    app.add_handler(CommandHandler("satquiz", satquiz_cmd))
    app.add_handler(CallbackQueryHandler(on_lang_select, pattern=r"^setlang:"))
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
