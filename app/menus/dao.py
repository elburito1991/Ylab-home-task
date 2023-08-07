import uuid

from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from .models import Menus


class MenusDAO(BaseDAO):
    model = Menus

    @classmethod
    async def update_counters(cls, item_id: uuid.UUID, submenu=0, dishes=0, addition=True) -> None:
        if addition:
            async with async_session_maker() as session:
                query = update(cls.model) \
                    .filter_by(id=item_id). \
                    values(
                    {
                        'submenus_count': cls.model.submenus_count + submenu,
                        'dishes_count': cls.model.dishes_count + dishes
                    }
                )
                await session.execute(query)
                await session.commit()

        else:
            async with async_session_maker() as session:
                query = update(cls.model).filter_by(id=item_id). \
                    values(
                    {
                        'submenus_count': cls.model.submenus_count - submenu,
                        'dishes_count': cls.model.dishes_count - dishes
                    }
                )
                await session.execute(query)
                await session.commit()
