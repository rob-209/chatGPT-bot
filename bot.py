import os
import openai
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    Dispatcher,
)

# Получаем ключи
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например, https://your-app.onrender.com/webhook

# Инициализация
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)
bot = Bot(BOT_TOKEN)

# Telegram app с Dispatcher
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую изображение по нему 🎨")

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
        await update.message.reply_text(f"Ошибка при создании изображения: {e}")

# Обработчики
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))

# Flask Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

# Установка Webhook при запуске
@app.before_first_request
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
