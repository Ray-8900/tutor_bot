import asyncio

from aiogram import Bot, Dispatcher

from database.database import init_db
from bot.handlers.registration import router
from bot.handlers.student import router as student_router
from bot.handlers.teacher import router as teacher_router
from config import BOT_TOKEN


async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(student_router)
    dp.include_router(teacher_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())