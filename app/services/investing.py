import datetime as dt
from typing import Union

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.sql.expression import false
from sqlalchemy.ext.asyncio import AsyncSession

from models import CharityProject, Donation


async def get_invest_objects(
        model: Union[CharityProject, Donation],
        session: AsyncSession
):
    """
    Возвращает текущие незакрытые проекты/пожертвования в порядке их создания.
    """

    actual_data = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(
            model.create_date.asc()
        )
    )
    return actual_data.scalars().all()


async def close_obj(
        instance: Union[CharityProject, Donation],
):
    """Обновляет информацию о проекте/пожертвовании и закрывает его."""

    now = dt.datetime.now()
    instance.invested_amount = instance.full_amount
    instance.fully_invested = True
    instance.close_date = now
    return instance


async def investing_process(
        new_obj: Union[CharityProject, Donation],
        session: AsyncSession
):
    """
    Процесс инвестирования.
    :param new_obj: Создаваемый благотворительный проект или пожертвование.
    """

    # Если переданный объект - благотворительный проект
    # то вытаскиваем из БД незакрытые пожертвования для инвестирования в проект
    if isinstance(new_obj, CharityProject):
        objects_to_invest = await get_invest_objects(Donation, session)

    # Если переданный объект - пожертвование
    # то вытаскиваем из БД незакрытые проекты для распределения средств
    elif isinstance(new_obj, Donation):
        objects_to_invest = await get_invest_objects(CharityProject, session)

    else:
        raise HTTPException(
            status_code=422,
            detail='Предоставлены неверные данные.'
        )

    # Если нет незакрытых проектов/пожертвований
    # возвзращаем объект без изменений
    if not objects_to_invest:
        return new_obj

    for obj in objects_to_invest:

        # Необходимая сумма для закрытия проекта
        new_obj_remains = new_obj.full_amount - new_obj.invested_amount

        # Необходимая сумма для закрытия пожертвования
        obj_remains = obj.full_amount - obj.invested_amount

        if new_obj_remains == obj_remains:
            await close_obj(new_obj)
            await close_obj(obj)
            session.add(obj, new_obj)
            break

        elif new_obj_remains < obj_remains:
            obj.invested_amount += new_obj_remains
            await close_obj(new_obj)
            session.add(obj, new_obj)
            break

        elif new_obj_remains > obj_remains:
            new_obj.invested_amount += obj_remains
            await close_obj(obj)
            session.add(obj, new_obj)
            continue

    await session.commit()
    await session.refresh(new_obj)
    return new_obj
