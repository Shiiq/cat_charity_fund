from sqlalchemy import Column, String, Text

from .fin_base import FinBase


class CharityProject(FinBase):
    """Модель благотворительного проекта."""

    __abstract__ = False
    __table_args__ = {'extend_existing': True}
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
