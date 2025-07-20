import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_brief
from config import TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_brief))

    print("🤖 BriefBot активирован. Ожидаю запросы...")
    app.run_polling()

if __name__ == "__main__":
    main()
