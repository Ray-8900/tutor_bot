from aiogram import Router, F
from aiogram.types import Message

from database.queries import get_next_lesson, get_week_lessons


router = Router()


@router.message(F.text == "📅 Ближайшее занятие")
async def next_lesson_handler(message: Message):
    lesson = await get_next_lesson(message.from_user.id)

    if lesson is None:
        await message.answer(
            "📅 У тебя нет ближайших занятий."
        )
        return

    await message.answer(
        f"📅 Ближайшее занятие\n\n"
        f"🕐 Начало: {lesson.start_time}\n"
        f"⏱ Продолжительность: {lesson.duration} мин."
    )

@router.message(F.text == "🗓 Расписание на неделю")
async def week_schedule_handler(message: Message):
    lessons = await get_week_lessons(message.from_user.id)

    if not lessons:
        await message.answer(
            "🗓 На этой неделе занятий нет."
        )
        return

    text = "🗓 Расписание на неделю\n\n"

    for lesson in lessons:
        text += (
            f"📅 {lesson.start_time.strftime('%d.%m')}\n"
            f"🕐 {lesson.start_time.strftime('%H:%M')}\n"
            f"⏱ {lesson.duration} мин.\n\n"
        )

    await message.answer(text)