from telegram import Update
from telegram.ext import ContextTypes
from briefgen import generate_brief
from config import MAKE_WEBHOOK_URL
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 *BriefBot v1.0 активирован.*\n"
        "Добро пожаловать в интерфейс системного ассистента.\n\n"
        "📨 _Перешлите мне текст клиентской заявки — и я трансформирую её в логически структурированное техническое задание._",
        parse_mode="Markdown"
    )

async def handle_brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text

    await update.message.reply_text("🧩 Анализирую входной текст...\n📡 Инициализация языковой модели...")

    try:
        structured = generate_brief(raw_text)
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка генерации ТЗ. Обратитесь к оператору.")
        print("Ошибка генерации:", e)
        return

    await update.message.reply_text("✅ Техническое задание готово:\n\n" + structured)

    # Отправка в Make
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json={
            "source_text": raw_text,
            "structured_brief": structured,
            "username": update.effective_user.username or "unknown"
        })

        if response.status_code == 200:
            await update.message.reply_text("☁️ Задание успешно сохранено в облачной системе.")
        else:
            await update.message.reply_text("⚠️ Не удалось сохранить ТЗ. Код ответа от сервера: " + str(response.status_code))

    except Exception as e:
        print("Ошибка при отправке в Make:", e)
        await update.message.reply_text("⚠️ Ошибка отправки в облачную систему.")
