import aiogram
import config
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Botni yaratamiz
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


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




# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    print("Bot ishga tushdi")
