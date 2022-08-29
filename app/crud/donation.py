from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models import Donation, User


class DonationCRUD(CRUDBase):
    async def get_donation_by_user(
            self,
            user: User,
            session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDBase(Donation)
