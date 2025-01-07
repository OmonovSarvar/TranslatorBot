import http.client
import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config
import json

# Botni yaratamiz
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Apining url manzili
url = "deep-translate1.p.rapidapi.com"
path = "/language/translate/v2"

# API key
RAPIDAPI_KEY = config.RAPIDAPI_KEY

# Result nomli dict yaratamiz
answer = {}

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
    conn = http.client.HTTPSConnection(url)
    conn.request("POST", path, json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # JSON'ni dict formatiga o‘zgartirish
    try:
        answer = json.loads(data)
        print(type(answer))
        print(answer)
        # translatedText ni olish
        translated_text = answer['data']['translations']['translatedText']
        await message.answer(translated_text)
    except json.JSONDecodeError:
        print("Error decoding JSON. Response might not be valid.")
    except KeyError as e:
        print(f"KeyError: {e} - Response structure might be different.")


# Botni ishga tushirish
if __name__ == '__main__':
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
    print("Bot to'xtatildi")
