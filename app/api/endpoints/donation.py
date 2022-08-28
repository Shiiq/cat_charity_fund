# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from core.db import get_async_session
# from core.user import current_user, current_superuser
# from crud.donation import donation_crud
# from schemas.charityproject import CharityProjectCreate, CharityProjectUpdate
#
# router = APIRouter()
#
#
# @router.get('/')
# async def get_all_charity_project(
#         session: AsyncSession = Depends(get_async_session)
# ):
#     charity_projects = await charity_project_crud.get_multi(session)
#     return charity_projects