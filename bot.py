import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши описание, и я сгенерирую изображение по нему с помощью ИИ 🎨"
    )

# Обработка текстовых сообщений
async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("Создаю изображение... ⏳")

    try:
        response = openai.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        await update.message.reply_photo(photo=image_url, caption="Готово! 😊")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при создании изображения: {e}")

# Основной запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))
    app.run_polling()
