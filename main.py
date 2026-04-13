import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import register_handlers

TOKEN = "8357001490:AAHfcrxsJyCUM6NOAuCnmExJZguyVPJKQr0"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

register_handlers(dp)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())