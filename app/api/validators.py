from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_unique_name(
        project_name: str,
        session: AsyncSession
):
    """Проверка уникальности имени."""

    is_exists = await session.execute(
        select(CharityProject.id).where(CharityProject.name == project_name)
    )
    if is_exists.scalars().first() is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: PositiveInt,
        session: AsyncSession
):
    """Проверка существует ли проект."""

    charity_project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_free_to_update(
        project: CharityProject,
        full_amount: int
):
    """
    Проверка условий для редактирования параметров проекта.
    1. Проект не должен быть закрыт;
    2. Требуемая сумма не может быть меньше уже вложенной суммы.
    """

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )
    return project


async def check_project_free_to_delete(
        project: CharityProject
):
    """
    Проверка условий для удаления проекта.
    1. Проект не должен быть закрыт;
    2. В проекте еще не было инвестиций.
    """

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project
