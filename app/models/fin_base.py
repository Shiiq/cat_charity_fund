import datetime as dt

from sqlalchemy import Column, Boolean, Integer, DateTime

# from cat_charity_fund.app.core.db import Base
from core.db import Base


class FinBase(Base):
    """Базовая модель."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.datetime.now())
    close_date = Column(DateTime)
