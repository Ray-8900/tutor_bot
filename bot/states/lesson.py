from aiogram.fsm.state import StatesGroup, State


class AddLessonState(StatesGroup):
    waiting_for_student = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_duration = State()