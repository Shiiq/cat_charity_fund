from sqlalchemy import Column, String, Text

# from fin_base import FinBase
from models.fin_base import FinBase


class CharityProject(FinBase):
    """Модель благотворительного проекта."""

    __abstract__ = False

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
