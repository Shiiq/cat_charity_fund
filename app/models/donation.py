from sqlalchemy import Column, ForeignKey, Integer, Text

from .fin_base import FinBase


class Donation(FinBase):
    """Модель пожертвования."""

    __abstract__ = False
    __table_args__ = {'extend_existing': True}
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )
    comment = Column(Text)
