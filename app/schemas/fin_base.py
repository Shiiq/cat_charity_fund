from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class FinBaseSchema(BaseModel):
    id: int
    create_date: datetime = Field(...)
    close_date: Optional[datetime] = Field(...)
    invested_amount: Optional[int] = Field(..., ge=0)
    fully_invested: bool
