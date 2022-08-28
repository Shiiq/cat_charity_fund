from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from .fin_base import FinBaseSchema


class CharityProjectCreate(BaseModel):
    """POST - все поля обязательные."""
    name: str = Field(..., title='Проект', min_length=1, max_length=100)
    description: str = Field(..., title='Описание', min_length=1)
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    """PATCH - все поля опциональные."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectFromDB(FinBaseSchema, CharityProjectCreate):

    class Config:
        orm_mode = True
