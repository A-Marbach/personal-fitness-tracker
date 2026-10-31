from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkoutEntry(Base):
    __tablename__ = "workout_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    recorded_on: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
    )

    pull_ups: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    push_ups: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
