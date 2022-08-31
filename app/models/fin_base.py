from sqlalchemy import Column, Boolean, Integer, DateTime

from app.core.db import Base


class FinBase(Base):
    """Базовая модель с общими полями."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
