from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.teacher import students_keyboard
from bot.states.lesson import AddLessonState
from database.queries import get_all_students
from datetime import datetime
from database.queries import create_lesson, get_user, get_week_lessons_teacher, create_invitation_code

router = Router()


@router.message(F.text == "➕ Добавить занятие")
async def add_lesson_handler(message: Message, state: FSMContext):
    students = await get_all_students()

    if not students:
        await message.answer(
            "❌ У тебя пока нет учеников."
        )
        return

    await message.answer(
        "👨‍🎓 Выбери ученика:",
        reply_markup=students_keyboard(students)
    )

    await state.set_state(AddLessonState.waiting_for_student)


@router.callback_query(
    AddLessonState.waiting_for_student,
    F.data.startswith("student_")
)
async def student_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    student_id = int(callback.data.split("_")[1])

    await state.update_data(student_id=student_id)

    await callback.message.answer(
        "📅 Введи дату занятия в формате:\n"
        "ДД.ММ.ГГГГ\n\n"
        "Например: 20.08.2026"
    )

    await state.set_state(AddLessonState.waiting_for_date)

    await callback.answer()

@router.message(AddLessonState.waiting_for_date)
async def date_entered(message: Message, state: FSMContext):
    try:
        lesson_date = datetime.strptime(
            message.text,
            "%d.%m.%Y"
        ).date()
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты.\n\n"
            "Введи дату в формате:\n"
            "ДД.ММ.ГГГГ\n\n"
            "Например: 20.08.2026"
        )
        return

    await state.update_data(
        lesson_date=lesson_date
    )

    await message.answer(
        "🕐 Теперь введи время занятия:\n\n"
        "Например: 15:30"
    )

    await state.set_state(
        AddLessonState.waiting_for_time
    )

@router.message(AddLessonState.waiting_for_time)
async def time_entered(message: Message, state: FSMContext):
    try:
        lesson_time = datetime.strptime(
            message.text,
            "%H:%M"
        ).time()
    except ValueError:
        await message.answer(
            "❌ Неверный формат времени.\n\n"
            "Введи время в формате:\n"
            "ЧЧ:ММ\n\n"
            "Например: 15:30"
        )
        return

    await state.update_data(
        lesson_time=lesson_time
    )

    await message.answer(
        "⏱ Введи продолжительность занятия в минутах.\n\n"
        "Например: 60"
    )

    await state.set_state(
        AddLessonState.waiting_for_duration
    )

@router.message(AddLessonState.waiting_for_duration)
async def duration_entered(message: Message, state: FSMContext):
    try:
        duration = int(message.text)

        if duration <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Неверная продолжительность.\n\n"
            "Введи количество минут числом.\n"
            "Например: 60"
        )
        return

    data = await state.get_data()

    student_id = data["student_id"]
    lesson_date = data["lesson_date"]
    lesson_time = data["lesson_time"]

    start_time = datetime.combine(
        lesson_date,
        lesson_time
    )

    teacher_id = (await get_user(message.from_user.id)).id

    lesson = await create_lesson(
        student_id=student_id,
        teacher_id=teacher_id,
        start_time=start_time,
        duration=duration
    )

    await state.clear()

    await message.answer(
        "✅ Занятие успешно добавлено!\n\n"
        f"📅 {start_time.strftime('%d.%m.%Y')}\n"
        f"🕐 {start_time.strftime('%H:%M')}\n"
        f"⏱ {duration} мин."
    )

@router.message(F.text == "Расписание на неделю")
async def week_schedule_handler(message: Message):
    lessons = await get_week_lessons_teacher(message.from_user.id)

    if not lessons:
        await message.answer(
            "На этой неделе занятий нет."
        )
        return

    text = "Расписание на неделю\n\n"

    for lesson in lessons:
        text += (
            f"📅 {lesson.start_time.strftime('%d.%m')}\n"
            f"🕐 {lesson.start_time.strftime('%H:%M')}\n"
            f"👤 {lesson.student.name}\n"
            f"⏱ {lesson.duration} мин.\n\n"
        )

    await message.answer(text)

@router.message(F.text == "Создать код")
async def prnt_code(message: Message, state: FSMContext):
    code = await create_invitation_code()
    print(code)

    await message.answer(code.code)

