from app.dao.base import BaseDAO

from .models import Dishes


class DishesDAO(BaseDAO):
    model = Dishes
