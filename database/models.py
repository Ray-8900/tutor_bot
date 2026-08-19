from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="student"
    )

    lessons_as_student: Mapped[list["Lesson"]] = relationship(
        foreign_keys="Lesson.student_id",
        back_populates="student"
    )

    lessons_as_teacher: Mapped[list["Lesson"]] = relationship(
        foreign_keys="Lesson.teacher_id",
        back_populates="teacher"
    )


class InvitationCode(Base):
    __tablename__ = "invitation_codes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime
    )

    duration: Mapped[int] = mapped_column(
        default=60
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled"
    )

    student: Mapped["User"] = relationship(
        foreign_keys=[student_id],
        back_populates="lessons_as_student"
    )

    teacher: Mapped["User"] = relationship(
        foreign_keys=[teacher_id],
        back_populates="lessons_as_teacher"
    )