import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from smsactivate.api import SMSActivateAPI

from sms_activate import get_phone_number, get_status, set_status
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
SMS_API_KEY = os.getenv('SMS_API_KEY')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

sa = SMSActivateAPI(SMS_API_KEY)
sa.debug_mode = True


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Hello, I'm a bot!")


@dp.message(Command(commands=['rent']))
async def rent_number(message: types.Message):
    phone_number, activation_id = get_phone_number(SMS_API_KEY)
    if activation_id:
        await message.reply(f"Ваш номер: {phone_number}. Ожидаем код...")
        await asyncio.sleep(150)  # Ожидание 2 минут
        status = get_status(SMS_API_KEY, activation_id)
        if "STATUS_OK" in status:
            code = status.split(":")[1].strip()
            await message.reply(f"Ваш код: {code}")
        else:
            set_status(SMS_API_KEY, activation_id, '8')  # Отмена активации
            await message.reply("Код не получен. Попробуйте еще раз.")
    else:
        await message.reply("Не удалось получить номер. Попробуйте позже.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
