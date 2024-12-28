import http.client
import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config

# Botni yaratamiz
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Apining url manzili
url = "deep-translate1.p.rapidapi.com"
path = "/language/translate/v2"

# API key
RAPIDAPI_KEY = config.RAPIDAPI_KEY

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
async def get_text_from_user(message: Message):
    user_text = message.text

    payload = {
        "q": f"{user_text}",
        "target": "en",  # Qaysi tilga tarjima qilish
        "source": "uz"   # Qaysi tildan tarjima qilish
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    # http.client bilan so'rov yuborish
    try:
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", path, json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        result = json.loads(data)

        # API javobini tekshirish
        if 'data' in result and 'translations' in result['data']:
            translated_text = result['data']['translations'][0]['translatedText']
            await message.reply(translated_text)
        else:
            await message.reply("Xatolik yuz berdi yoki tarjima topilmadi. Iltimos, keyinroq urinib ko'ring.")

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        await message.reply("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")


# Botni ishga tushirish
if __name__ == '__main__':
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
    print("Bot to'xtatildi")
