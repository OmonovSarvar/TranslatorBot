import aiogram
import config
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def echo_handler(message: Message):
    await message.reply(f"Salom {message.from_user.first_name}")







# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    print("Bot ishga tushdi")
