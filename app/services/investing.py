from sqlalchemy import select
from sqlalchemy.sql.expression import false, true
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import CharityProject, Donation

# full_amount — требуемая сумма, целочисленное поле; больше 0;
# invested_amount — внесённая сумма, целочисленное поле; значение по умолчанию — 0;
# fully_invested — булево значение, указывающее на то, собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False;
async def check_active_projects(session):
    """Возвращает список незакрытых проектов."""
    active_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == false()
        )
    )
    return active_projects.scalars().all()


# full_amount — сумма пожертвования, целочисленное поле; больше 0;
# invested_amount — сумма из пожертвования, которая распределена по проектам; значение по умолчанию равно 0;
# fully_invested — булево значение, указывающее на то, все ли деньги из пожертвования были переведены в тот или иной проект; по умолчанию равно False;
async def check_remaining_donations(session):
    """Возвращает список оставшихся пожертвований."""
    remaining_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == false()
        )
    )
    return remaining_donations.scalars().all()


def investing():

    pass
