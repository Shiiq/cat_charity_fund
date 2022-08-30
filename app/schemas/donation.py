from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from schemas.fin_base import FinBaseSchema


class DonationCreate(BaseModel):
    """Схема для создания пожертвования."""

    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
    comment: Optional[str] = Field(None, title='Комментарий к пожертвованию')

    class Config:
        extra = Extra.forbid


class DonationResponse(DonationCreate):
    """Схема для ответного сообщения на создание пожертвования."""

    create_date: datetime = Field(...)

    class Config:
        orm_mode = True


class DonationFromDB(FinBaseSchema, DonationCreate):
    """Схема для отображения полной информации о пожертвовании из БД."""

    class Config:
        orm_mode = True
