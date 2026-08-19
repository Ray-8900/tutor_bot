from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


student_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📅 Ближайшее занятие"),
            KeyboardButton(text="🗓 Расписание на неделю")
        ]
    ],
    resize_keyboard=True
)