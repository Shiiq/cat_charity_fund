from typing import List
#
from sqlalchemy import select
from sqlalchemy.sql.expression import false, true
from models import CharityProject, Donation
#
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.user import current_user, current_superuser
from crud.charityproject import charity_project_crud
from schemas.charityproject import (CharityProjectCreate,
                                    CharityProjectUpdate,
                                    CharityProjectFromDB)

router = APIRouter()


@router.get('/', response_model=List[CharityProjectFromDB])
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для просмотра списка проектов."""
    charity_projects = await charity_project_crud.get_multi(session)
    # active_projects = await session.execute(
    #     select(CharityProject).where(
    #         CharityProject.fully_invested == false()
    #     ).order_by(CharityProject.create_date.desc())
    # )
    # return active_projects.scalars().all()
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт для создания нового проекта. Только для суперюзера."""
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        charity_project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для редактирования проекта. Только для суперюзера."""
    charity_project = await charity_project_crud.get_by_attribute(
        attr_name='id',
        attr_value=project_id,
        session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=422,
            detail='Закрытый проект нельзя редактировать.'
        )
    if charity_project_data.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=charity_project_data,
        session=session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectFromDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для удаления проекта. Только для суперюзера."""
    charity_project = await charity_project_crud.get_by_attribute(
        attr_name='id',
        attr_value=project_id,
        session=session
    )
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект, '
                   'в который уже были инвестированы средства, '
                   'его можно только закрыть.'
        )
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project
