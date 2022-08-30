from sqlalchemy import Column, Boolean, Integer, DateTime

# from cat_charity_fund.app.core.db import Base
from core.db import Base


class FinBase(Base):
    """Базовая модель с общими полями."""

    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
