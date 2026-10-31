
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkoutCreate(BaseModel):
    recorded_on: date

    pull_ups: int = Field(ge=0)
    push_ups: int = Field(ge=0)


class WorkoutResponse(WorkoutCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
