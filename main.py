import http.client
import json
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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

text = ""
answer = {}
source = ""
target = ""

# Boshlang'ich tilni belgilash
source = "uz"
target = "en"

@dp.message_handler(commands=['start'])    
async def send_translation_menu(message: Message):
    keyboard = get_translation_buttons()
    await message.reply("Qaysi tarjimani tanlaysiz?", reply_markup=keyboard)

def get_translation_buttons():
    # Tugmalarni yaratamiz
    keyboard = InlineKeyboardMarkup(row_width=2)
    uz_to_en = InlineKeyboardButton("O‘zbek ➡ Ingliz", callback_data="uz_to_en")
    en_to_uz = InlineKeyboardButton("Ingliz ➡ O‘zbek", callback_data="en_to_uz")
    change_lang = InlineKeyboardButton("Tilni o'zgartirish", callback_data="change_lang")

    # Tugmalarni qo‘shamiz
    keyboard.add(uz_to_en, en_to_uz, change_lang)

    return keyboard

# Tilni o'zgartirish
@dp.callback_query_handler(lambda c: c.data == 'change_lang')
async def change_language(callback_query: CallbackQuery):
    keyboard = get_translation_buttons()  # Yangi tarjima tugmalari
    await callback_query.message.answer("Qaysi tildan qaysi tilga tarjima qilishni xohlaysiz?", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "uz_to_en")
async def set_uz_to_en(callback_query: CallbackQuery):
    global source, target
    source = "uz"
    target = "en"
    await callback_query.message.answer("O‘zbek tilidan Ingliz tiliga tarjima qilishga tayyormiz!")

@dp.callback_query_handler(lambda c: c.data == "en_to_uz")
async def set_en_to_uz(callback_query: CallbackQuery):
    global source, target
    source = "en"
    target = "uz"
    await callback_query.message.answer("Ingliz tilidan O‘zbek tiliga tarjima qilishga tayyormiz!")

# Foydalanuvchidan matn so'rash
@dp.message_handler(commands=['change'])
async def prompt_for_change(message: Message):
    keyboard = get_translation_buttons()
    await message.reply("Tilni o'zgartirish uchun quyidagi tugmalarni tanlang:", reply_markup=keyboard)

@dp.message_handler()
async def translate_text(message: Message):
    await message.reply("Matn kiriting:")
    text = message.text

    payload = {
        "q": text,
        "target": target,  # Qaysi tilga tarjima qilish
        "source": source   # Qaysi tildan tarjima qilish
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
        # translatedText ni olish
        translated_text = answer['data']['translations']['translatedText']

        # Nusxa olish tugmasini qo'shish
        keyboard = InlineKeyboardMarkup()
        copy_button = InlineKeyboardButton("Nusxa olish", callback_data="copy_text")
        keyboard.add(copy_button)

        await message.answer(f"Tarjima: {translated_text}", reply_markup=keyboard)

    except json.JSONDecodeError:
        print("Error decoding JSON. Response might not be valid.")
    except KeyError as e:
        print(f"KeyError: {e} - Response structure might be different.")

# Nusxa olish tugmasi
@dp.callback_query_handler(lambda c: c.data == "copy_text")
async def copy_text(callback_query: CallbackQuery):
    await callback_query.message.answer("Matn clipboard'ga nusxalandi!")

# Botni ishga tushirish 
if __name__ == '__main__':
    print("Bot ishga tushirildi")
    executor.start_polling(dp, skip_updates=True)
    print("Bot to'xtatildi")
