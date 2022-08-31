from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from .fin_base import FinBaseSchema


class CharityProjectCreate(BaseModel):
    """Схема для POST запроса. Все поля обязательные."""

    name: str = Field(..., title='Благотворительный проект', min_length=1, max_length=100)
    description: str = Field(..., title='Описание проекта', min_length=1)
    full_amount: PositiveInt = Field(..., title='Необходимая сумма пожертвования')

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    """Схема для PATCH запроса. Все поля опциональные."""

    name: Optional[str] = Field(None, title='Благотворительный проект', min_length=1, max_length=100)
    description: Optional[str] = Field(None, title='Описание проекта', min_length=1)
    full_amount: Optional[PositiveInt] = Field(None, title='Необходимая сумма пожертвования')

    class Config:
        extra = Extra.forbid


class CharityProjectFromDB(FinBaseSchema, CharityProjectCreate):
    """Схема для отображения полной информации о проекте из БД."""

    class Config:
        orm_mode = True
