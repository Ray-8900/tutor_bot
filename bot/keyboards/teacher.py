from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

teacher_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Добавить занятие"),
            KeyboardButton(text="Расписание на неделю"),
            KeyboardButton(text="Создать код")
        ],
    ],
    resize_keyboard=True
)


def students_keyboard(students):
    keyboard = []

    for student in students:
        keyboard.append([
            InlineKeyboardButton(
                text=student.name,
                callback_data=f"student_{student.id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)