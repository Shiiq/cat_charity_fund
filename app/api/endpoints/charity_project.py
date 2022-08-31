from typing import List

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_unique_name,
                                check_project_exists,
                                check_project_free_to_update,
                                check_project_free_to_delete)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate,
                                         CharityProjectFromDB)
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectFromDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для просмотра списка проектов."""

    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectFromDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт для создания нового проекта. Только для суперюзера."""

    # Проверка уникальности имени
    project_name = charity_project.name
    await check_unique_name(project_name, session)

    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session
    )
    # Процесс инвестирования
    char_proj = await investing_process(new_charity_project, session)
    return char_proj


@router.patch(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: PositiveInt,
        charity_project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для редактирования проекта. Только для суперюзера."""

    # Проверяем существует ли проект
    charity_project = await check_project_exists(
        project_id=project_id,
        session=session
    )
    # Если в запросе передано новое имя - проверяем уникальность
    if charity_project_data.name is not None:
        project_name = charity_project_data.name
        await check_unique_name(project_name, session)
    # Если в запросе передана новая сумма - проверяем условия
    # 1. Закрыт ли проект?
    # 2. Новая сумма меньше уже внесенной в проект?
    if charity_project_data.full_amount is not None:
        full_amount = charity_project_data.full_amount
        charity_project = await check_project_free_to_update(
            project=charity_project,
            full_amount=full_amount
        )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=charity_project_data,
        session=session
    )
    # Процесс инвестирования
    char_proj = await investing_process(charity_project, session)
    return char_proj


@router.delete(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: PositiveInt,
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для удаления проекта. Только для суперюзера."""

    # Проверяем существует ли проект
    charity_project = await check_project_exists(
        project_id=project_id,
        session=session
    )
    charity_project = await check_project_free_to_delete(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project
