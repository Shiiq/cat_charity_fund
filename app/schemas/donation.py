from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from .fin_base import FinBaseSchema


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
    comment: Optional[str] = Field(None, title='Комментарий к пожертвованию')

    class Config:
        extra = Extra.forbid


# class DonationResponse(DonationCreate):
#     id: int
#     create_date: datetime = Field(...)
#
#
# class DonationDB(BaseModel):
#     user_id: Optional[int]
#     pass