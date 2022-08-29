from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.user import current_user, current_superuser
from crud.donation import donation_crud
from models import User
from schemas.donation import DonationCreate, DonationResponse, DonationFromDB

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFromDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Эндпоинт для просмотра пожертвований всех юзеров.
    Только для суперюзера.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationFromDB],
    response_model_exclude={'user_id'}
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для просмотра всех пожертвований текущего юзера."""
    user_donations = await donation_crud.get_donation_by_user(
        user=user,
        session=session
    )
    return user_donations


@router.post('/', response_model=DonationResponse)
async def create_new_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для создания пожертвования."""
    new_donation = await donation_crud.create(
        obj_in=donation,
        user=user,
        session=session
    )
    return new_donation
