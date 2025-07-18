import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ChatType
import asyncio

API_TOKEN = "8007934043:AAEESCCrou1Ldr63cQ_BBurZNYIVP4mvQR4"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# נשמור את המשתמשים שדיברו עם הבוט
user_ids = set()

@dp.message(CommandStart())
async def start_command(message: Message):
    user_ids.add(message.chat.id)
    await message.answer("✅ עודכנת! כשתתפרסם הודעה בערוץ – תקבל אותה כאן.")

# מאזין לכל ההודעות מהערוץ
@dp.channel_post()
async def channel_listener(message: Message):
    if message.chat.username != "mivzakimplus":
        return  # לא הערוץ שלנו

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=message.text or "📢 (הודעה לא טקסטואלית)")
        except Exception as e:
            logging.warning(f"שגיאה בשליחה ל-{user_id}: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
