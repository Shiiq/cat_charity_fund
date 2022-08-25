from sqlalchemy import Column, ForeignKey, Integer, Text

# from fin_base import FinBase
from .fin_base import FinBase


class Donation(FinBase):
    """Модель пожертвования."""
    __abstract__ = False

    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'), nullable=False)
    comment = Column(Text)
