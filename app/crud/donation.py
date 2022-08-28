from .base import CRUDBase
from models import Donation


donation_crud = CRUDBase(Donation)
