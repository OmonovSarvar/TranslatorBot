import aiogram
import requests
import config
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Botni yaratamiz
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
# Apining url manzili
url = "https://google-translate1.p.rapidapi.com/language/translate/v2"


# 
#@dp.message_handler(commands=["start"])  # Start command
#async def echo_handler(message: Message):
#    first_name = message.from_user.first_name  # Get user's 
#    await message.reply(f"Assalomu Alekum {first_name}")



@dp.message_handler(commands=['start', 'translate'])
async def send_translation_menu(message: Message):
    keyboard = get_translation_buttons()
    await message.reply("Qaysi tarjimani tanlaysiz?", reply_markup=keyboard)


def get_translation_buttons():
    # Tugmalarni yaratamiz
    keyboard = InlineKeyboardMarkup(row_width=2)
    uz_to_en = InlineKeyboardButton("O‘zbek ➡ Ingliz", callback_data="uz_to_en")
    en_to_uz = InlineKeyboardButton("Ingliz ➡ O‘zbek", callback_data="en_to_uz")

    # Tugmalarni qo‘shamiz
    keyboard.add(uz_to_en, en_to_uz)
    return keyboard


@dp.message_handler()
def get_text_from_user(message: Message):
    user_text = message.text
    print(user_text)


payload = {
	"q": "Salom, dunyo!",
	"target": "en",
	"source": "uz"
}
headers = {
	"x-rapidapi-key": "707c9a7aeemsh5ffec9ad5b7ac26p1582a5jsn2dd2b6a6b87b",
	"x-rapidapi-host": "google-translate1.p.rapidapi.com",
	"Content-Type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())


# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    print("Bot ishga tushdi")
