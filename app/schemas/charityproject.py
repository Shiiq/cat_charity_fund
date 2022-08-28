from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt
# id — первичный ключ;
# name — уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 100 символов включительно;
# description — описание, обязательное поле, текст; не менее одного символа;
# full_amount — требуемая сумма, целочисленное поле; больше 0;
# invested_amount — внесённая сумма, целочисленное поле; значение по умолчанию — 0;
# fully_invested — булево значение, указывающее на то, собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False;
# create_date — дата создания проекта, тип DateTime, должно добавляться автоматически в момент создания проекта.
# close_date — дата закрытия проекта, DateTime, проставляется автоматически в момент набора нужной суммы.

# full_amount = Column(Integer)
# invested_amount = Column(Integer, default=0)
# fully_invested = Column(Boolean, default=False)
# create_date = Column(DateTime, default=dt.datetime.now())
# close_date = Column(DateTime)


# class CharityProjectBase(BaseModel):
#     name: str = Field(..., title='Проект', min_length=1, max_length=100)
#     description: str = Field(..., title='Описание', min_length=1)
#     full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
#
#     class Config:
#         extra = Extra.forbid


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


# class CharityProjectFromDB(CharityProjectCreate):
#     id: int
#
#     class Config:
#         orm_mode = True
