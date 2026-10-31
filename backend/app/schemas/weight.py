from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WeightCreate(BaseModel):
    recorded_on: date
    weight_kg: Decimal = Field(gt=0, le=999.99, decimal_places=2)


class WeightResponse(WeightCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
