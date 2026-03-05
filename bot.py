import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "8706601049:AAGx0DYS2tz1KguqJn2U3gG6dPNS2h4mK98")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://zhanatbekkk.github.io/march8-invite/")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ── States ────────────────────────────────────────────────────────────────────
CHOOSE_LANG, QUIZ = range(2)

# ── Texts ─────────────────────────────────────────────────────────────────────
TEXTS = {
    "ru": {
        "welcome_title": "🌸 С праздником, 8 Марта! 🌸",
        "welcome": (
            "✨ <b>Дорогие, удивительные девушки департамента ДУМД!</b>\n\n"
            "В этот прекрасный весенний день хочется сказать вам самое главное:\n\n"
            "🌹 <i>Вы — сердце нашего коллектива.</i>\n"
            "Ваша теплота, мудрость и неиссякаемая энергия делают каждый рабочий день "
            "ярче и радостнее.\n\n"
            "💛 Пусть весна наполнит вашу жизнь цветами, улыбками и только приятными "
            "сюрпризами. Вы заслуживаете самого лучшего — каждый день!\n\n"
            "<b>С любовью и уважением, ваши коллеги 💐</b>\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "🎯 А теперь — небольшая весенняя викторина!\n"
            "5 вопросов, хорошее настроение и приятный сюрприз в конце 🎁"
        ),
        "start_quiz": "🌸 Начать викторину",
        "quiz_header": "Вопрос {num}/5",
        "prize_text": (
            "🎉 <b>Поздравляем! Вы прошли викторину!</b>\n\n"
            "{result_text}\n\n"
            "🎁 <b>Ваш подарок ждёт вас!</b>\n"
            "Нажмите кнопку ниже, чтобы открыть праздничное пригласительное 🌹"
        ),
        "open_invite": "🌸 Открыть пригласительное 🌸",
        "next": "Следующий вопрос ➡️",
    },
    "kz": {
        "welcome_title": "🌸 8 Наурыз мерекесімен! 🌸",
        "welcome": (
            "✨ <b>Қымбатты ДУМД департаментінің керемет қыздары!</b>\n\n"
            "Осы сәулелі көктем күнінде сіздерге ең маңызды сөздерді айтқым келеді:\n\n"
            "🌹 <i>Сіздер — ұжымымыздың жүрегісіз.</i>\n"
            "Сіздердің жылулығыңыз, даналығыңыз және таусылмас энергияңыз "
            "әр жұмыс күнін жарқын және қуанышты етеді.\n\n"
            "💛 Көктем өміріңізді гүлдермен, күлімдеумен және тек жағымды "
            "сюрпризбен толтырсын. Сіздер күн сайын ең жақсыға лайықсыз!\n\n"
            "<b>Сүйіспеншілік пен құрметпен, сіздердің әріптестеріңіз 💐</b>\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "🎯 Енді — шағын көктемгі викторина!\n"
            "5 сұрақ, жақсы көңіл-күй және соңында тәтті сюрприз 🎁"
        ),
        "start_quiz": "🌸 Викторинаны бастау",
        "quiz_header": "Сұрақ {num}/5",
        "prize_text": (
            "🎉 <b>Құттықтаймыз! Сіз викторинаны аяқтадыңыз!</b>\n\n"
            "{result_text}\n\n"
            "🎁 <b>Сіздің сыйлығыңыз күтіп тұр!</b>\n"
            "Мереке шақыруын ашу үшін төмендегі батырманы басыңыз 🌹"
        ),
        "open_invite": "🌸 Шақыруды ашу 🌸",
        "next": "Келесі сұрақ ➡️",
    }
}

# ── Quiz questions ─────────────────────────────────────────────────────────────
QUIZ_QUESTIONS = {
    "ru": [
        {
            "q": "🌸 Вопрос 1: Какое у вас настроение сегодня утром?",
            "options": ["🌞 Солнечное и бодрое!", "🌷 Нежное и весеннее", "☕ Только с кофе", "🦋 Порхаю от радости!"],
            "reactions": ["Отличное начало дня! ☀️", "Весна чувствуется! 🌸", "Кофе — лучший друг! ☕", "Вы заражаете всех радостью! 🦋"]
        },
        {
            "q": "🌿 Вопрос 2: Как ощущается весна за окном?",
            "options": ["🌱 Свежо и обновляюще", "🌼 Цветочный аромат везде!", "🌤️ Солнышко щекочет нос", "🎵 Птицы поют — душа поёт!"],
            "reactions": ["Свежесть весны — лучший заряд! 🌿", "Природа цветёт, как и вы! 🌼", "Весеннее солнце для вас! ☀️", "Ваша душа — музыка! 🎵"]
        },
        {
            "q": "💐 Вопрос 3: Если бы вы были цветком, то каким?",
            "options": ["🌹 Роза — королева", "🌷 Тюльпан — элегантность", "🌸 Сакура — нежность", "🌻 Подсолнух — солнечность"],
            "reactions": ["Истинная королева! 👑", "Элегантность во всём! 💫", "Нежность и красота! 🌸", "Вы освещаете всё вокруг! 🌻"]
        },
        {
            "q": "🎯 Вопрос 4: Какой ваш идеальный праздничный вечер?",
            "options": ["🍽️ Ужин с близкими", "🎭 Театр или концерт", "🌙 Уютный вечер дома", "💃 Танцы до утра!"],
            "reactions": ["Семья — главное богатство! 💛", "Вы цените прекрасное! 🎭", "Уют — ваша суперсила! 🏡", "Зажигаете! 🔥"]
        },
        {
            "q": "🌟 Вопрос 5: Ваше пожелание себе на этот год?",
            "options": ["💪 Сил и здоровья!", "❤️ Любви и тепла!", "🚀 Новых побед!", "😊 Просто счастья!"],
            "reactions": ["Пусть здоровье и силы всегда с вами! 💪", "Любовь наполняет мир! ❤️", "Победы уже впереди! 🏆", "Счастье — это вы! 😊"]
        },
    ],
    "kz": [
        {
            "q": "🌸 1-сұрақ: Бүгін таңертең көңіл-күйіңіз қандай?",
            "options": ["🌞 Күнді және серпінді!", "🌷 Нәзік және көктемгі", "☕ Тек кофемен ғана", "🦋 Қуаныштан ұшып жүрмін!"],
            "reactions": ["Тамаша күн басталуы! ☀️", "Көктем сезіледі! 🌸", "Кофе — ең жақсы дос! ☕", "Сіз бәріне қуаныш сыйлайсыз! 🦋"]
        },
        {
            "q": "🌿 2-сұрақ: Терезе сыртындағы көктем қандай сезіледі?",
            "options": ["🌱 Сергек және жаңарған", "🌼 Гүл иісі әрі жерде!", "🌤️ Күн мұрынды қытықтайды", "🎵 Құстар сайрайды — жан сайрайды!"],
            "reactions": ["Көктем сергектігі — ең жақсы заряд! 🌿", "Табиғат та, сіз де гүлдеп тұрсыз! 🌼", "Көктем күні сізге арналған! ☀️", "Жаныңыз — музыка! 🎵"]
        },
        {
            "q": "💐 3-сұрақ: Егер сіз гүл болсаңыз, қандай гүл болар едіңіз?",
            "options": ["🌹 Раушан — патшайым", "🌷 Қызғалдақ — талғамдылық", "🌸 Сакура — нәзіктік", "🌻 Күнбағыс — күнділік"],
            "reactions": ["Нағыз патшайым! 👑", "Барлығында талғамдылық! 💫", "Нәзіктік пен сұлулық! 🌸", "Сіз айналаны жарықтандырасыз! 🌻"]
        },
        {
            "q": "🎯 4-сұрақ: Мереке кешінің мінсіз нұсқасы қандай?",
            "options": ["🍽️ Жақындармен кеш ас", "🎭 Театр немесе концерт", "🌙 Үйдегі жайлы кеш", "💃 Таңға дейін би!"],
            "reactions": ["Отбасы — басты байлық! 💛", "Сіз сұлулықты бағалайсыз! 🎭", "Жайлылық — сіздің суперкүшіңіз! 🏡", "Жалын шашасыз! 🔥"]
        },
        {
            "q": "🌟 5-сұрақ: Осы жылға өзіңізге тілегіңіз қандай?",
            "options": ["💪 Күш пен денсаулық!", "❤️ Махаббат пен жылулық!", "🚀 Жаңа жеңістер!", "😊 Жай ғана бақыт!"],
            "reactions": ["Денсаулық пен күш әрқашан сізбен болсын! 💪", "Махаббат әлемді толтырады! ❤️", "Жеңістер алда! 🏆", "Бақыт — бұл сіз! 😊"]
        },
    ]
}

RESULT_TEXTS = {
    "ru": [
        "🌟 Вы — настоящая весенняя фея! Ваш позитив заряжает всех вокруг!",
        "💫 Ваша энергия и оптимизм — лучший подарок коллективу!",
        "🌸 Вы излучаете тепло и нежность — именно такие люди делают мир лучше!",
        "✨ Ваш характер — как весеннее солнце: тёплый, яркий и неотразимый!",
    ],
    "kz": [
        "🌟 Сіз — нағыз көктем пері! Позитивіңіз барлығын зарядтайды!",
        "💫 Сіздің энергияңыз бен оптимизміңіз — ұжымға ең жақсы сыйлық!",
        "🌸 Сіз жылу мен нәзіктік шығарасыз — дәл осындай адамдар әлемді жақсы етеді!",
        "✨ Сіздің мінезіңіз — көктем күні сияқты: жылы, жарқын және тартымды!",
    ]
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_lang(context):
    return context.user_data.get("lang", "ru")

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz"),
    ]])

def quiz_keyboard(lang, q_idx):
    q = QUIZ_QUESTIONS[lang][q_idx]
    buttons = [[InlineKeyboardButton(opt, callback_data=f"ans_{q_idx}_{i}")]
               for i, opt in enumerate(q["options"])]
    return InlineKeyboardMarkup(buttons)

# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🌸 <b>Выберите язык / Тілді таңдаңыз:</b>",
        reply_markup=lang_keyboard(),
        parse_mode="HTML"
    )
    return CHOOSE_LANG

async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    context.user_data["answers"] = []

    t = TEXTS[lang]
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(t["start_quiz"], callback_data="start_quiz")
    ]])

    await query.edit_message_text(
        f"{t['welcome_title']}\n\n{t['welcome']}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    return CHOOSE_LANG

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q_index"] = 0
    await send_question(query, context, edit=True)
    return QUIZ

async def send_question(query, context, edit=False):
    lang = get_lang(context)
    q_idx = context.user_data["q_index"]
    t = TEXTS[lang]
    q = QUIZ_QUESTIONS[lang][q_idx]
    text = f"<b>{t['quiz_header'].format(num=q_idx+1)}</b>\n\n{q['q']}"

    if edit:
        await query.edit_message_text(text, reply_markup=quiz_keyboard(lang, q_idx), parse_mode="HTML")
    else:
        await query.message.reply_text(text, reply_markup=quiz_keyboard(lang, q_idx), parse_mode="HTML")

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, q_idx_str, ans_idx_str = query.data.split("_")
    q_idx = int(q_idx_str)
    ans_idx = int(ans_idx_str)

    lang = get_lang(context)
    reaction = QUIZ_QUESTIONS[lang][q_idx]["reactions"][ans_idx]
    context.user_data.setdefault("answers", []).append(ans_idx)

    next_idx = q_idx + 1
    context.user_data["q_index"] = next_idx

    if next_idx >= 5:
        # Show prize
        import random
        result = random.choice(RESULT_TEXTS[lang])
        t = TEXTS[lang]
        prize_text = t["prize_text"].format(result_text=result)

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                t["open_invite"],
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
        await query.edit_message_text(
            f"<i>{reaction}</i>\n\n{prize_text}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return ConversationHandler.END
    else:
        # Show reaction + next question
        next_q = QUIZ_QUESTIONS[lang][next_idx]
        t = TEXTS[lang]
        text = (
            f"<i>{reaction}</i>\n\n"
            f"<b>{t['quiz_header'].format(num=next_idx+1)}</b>\n\n{next_q['q']}"
        )
        await query.edit_message_text(
            text,
            reply_markup=quiz_keyboard(lang, next_idx),
            parse_mode="HTML"
        )
        return QUIZ

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_LANG: [
                CallbackQueryHandler(choose_lang, pattern="^lang_"),
                CallbackQueryHandler(start_quiz, pattern="^start_quiz$"),
            ],
            QUIZ: [
                CallbackQueryHandler(handle_answer, pattern="^ans_"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv)
    logger.info("🌸 March 8 Bot started!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
