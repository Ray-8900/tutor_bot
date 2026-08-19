from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.registration import RegistrationState
from database.queries import get_user, register_student
from bot.keyboards.student import student_keyboard
from bot.keyboards.teacher import teacher_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    telegram_id = message.from_user.id

    user = await get_user(telegram_id)

    if user is not None:

        if user.role == "teacher":
            await message.answer(
                f"С возвращением, {user.name}! 👨‍🏫",
                reply_markup=teacher_keyboard
            )

        else:
            await message.answer(
                f"С возвращением, {user.name}! 👋",
                reply_markup=student_keyboard
            )

        return

    await message.answer(
        "👋 Привет!\n\n"
        "Ты ещё не зарегистрирован.\n"
        "Введи код приглашения, который выдал тебе репетитор:"
    )

    await state.set_state(RegistrationState.waiting_for_code)


@router.message(RegistrationState.waiting_for_code)
async def registration_handler(
    message: Message,
    state: FSMContext
):
    telegram_id = message.from_user.id
    name = message.from_user.first_name
    code = message.text.strip()

    user = await register_student(
        telegram_id=telegram_id,
        name=name,
        code=code
    )

    if user is None:
        await message.answer(
            "❌ Код недействителен.\n"
            "Проверь его и попробуй ещё раз."
        )
        return

    await state.clear()

    await message.answer(
        f"✅ Регистрация успешна!\n\n"
        f"Добро пожаловать, {user.name}!",
        reply_markup=student_keyboard
    )

