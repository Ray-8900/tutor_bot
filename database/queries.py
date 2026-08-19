from sqlalchemy import select

from database.database import async_session
from database.models import User, InvitationCode, Lesson
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import selectinload

# Users
async def get_user(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )

        return result.scalar_one_or_none()


async def create_user(
    telegram_id: int,
    name: str,
    role: str = "student"
):
    async with async_session() as session:
        user = User(
            telegram_id=telegram_id,
            name=name,
            role=role
        )

        session.add(user)
        await session.commit()

        return user

# Students

async def get_all_students():
    async with async_session() as session:
        result = await session.scalars(
            select(User).where(User.role == "student")
        )

        return list(result)



async def register_student(
    telegram_id: int,
    name: str,
    code: str
):
    async with async_session() as session:
        invitation_code = await session.scalars(
            select(InvitationCode).where(
                InvitationCode.code == code,
                InvitationCode.used.is_(False)
            )
        )

        cd = invitation_code.one_or_none()

        if cd is None:
            return None

        else:
            user = User(
                telegram_id=telegram_id,
                name=name,
                role="student"
            )

            session.add(user)
            cd.used = True

            await session.commit()
            return user

# Lessons

async def get_next_lesson(telegram_id):
    async with async_session() as session:
        user = await get_user(telegram_id)
        idd = user.id

        result = await session.execute(
            select(Lesson).where(Lesson.student_id == idd,
                                 Lesson.start_time > datetime.now()).order_by(Lesson.start_time).limit(1)
        )

        lesson = result.scalar_one_or_none()

        if lesson is None:
            return None

        return lesson

async def get_week_lessons(telegram_id: int):
    async with async_session() as session:
        user = await get_user(telegram_id)

        if user is None:
            return []

        today = datetime.now()

        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end_of_week = start_of_week + timedelta(days=7)

        result = await session.scalars(
            select(Lesson)
            .where(
                Lesson.student_id == user.id,
                Lesson.start_time >= start_of_week,
                Lesson.start_time < end_of_week
            )
            .order_by(Lesson.start_time)
        )

        return list(result)

async def create_lesson(
    student_id: int,
    teacher_id: int,
    start_time: datetime,
    duration: int = 60
):
    async with async_session() as session:
        lesson = Lesson(
            student_id=student_id,
            teacher_id=teacher_id,
            start_time=start_time,
            duration=duration
        )

        session.add(lesson)
        await session.commit()

        return lesson

# Teacher

async def make_teacher(telegram_id: int):
    async with async_session() as session:
        result = await session.scalars(
            select(User).where(User.telegram_id == telegram_id)
        )

        user = result.one_or_none()

        if user is None:
            return None

        user.role = "teacher"

        await session.commit()

        return user

async def get_week_lessons_teacher(telegram_id: int):
    async with async_session() as session:
        user = await get_user(telegram_id)

        if user is None:
            return []

        today = datetime.now()

        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        end_of_week = start_of_week + timedelta(days=7)

        result = await session.scalars(
            select(Lesson)
            .options(selectinload(Lesson.student))
            .where(
                Lesson.teacher_id == user.id,
                Lesson.start_time >= start_of_week,
                Lesson.start_time < end_of_week
            )
            .order_by(Lesson.start_time)
        )

        return list(result)

# Ivitation codes

async def create_invitation_code():
    async with async_session() as session:
        cod = secrets.token_hex(4)
        invitation_code = InvitationCode(
            code=cod,
        )
        session.add(invitation_code)
        await session.commit()

        return invitation_code

