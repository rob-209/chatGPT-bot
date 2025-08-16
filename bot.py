import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiohttp import ClientSession

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


async def generate_image(prompt: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json={"inputs": prompt}) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error from HuggingFace API: {text}")
            return await response.read()


@dp.message_handler(commands=["start"])
async def handle_start(message: Message):
    await message.reply("Привет! Отправь мне описание, и я сгенерирую изображение.")


@dp.message_handler()
async def handle_prompt(message: Message):
    prompt = message.text.strip()
    await message.reply("Генерирую изображение, подожди немного...")

    try:
        image_bytes = await generate_image(prompt)
        await bot.send_photo(message.chat.id, photo=image_bytes, caption="Вот твоё изображение!")
    except Exception as e:
        await message.reply(f"Произошла ошибка при генерации изображения:\n{e}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
