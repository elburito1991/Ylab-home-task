import uuid

from sqlalchemy import func, select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker

from .models import Submenus


class SubmenusDAO(BaseDAO):
    model = Submenus

    @classmethod
    async def update_counters(cls, item_id: uuid.UUID, dishes=0, addition=True) -> None:
        async with async_session_maker() as session:
            if addition:
                query = update(cls.model) \
                    .filter_by(id=item_id). \
                    values(
                    {'dishes_count': cls.model.dishes_count + dishes}
                )
                await session.execute(query)
                await session.commit()
            else:
                query = update(cls.model) \
                    .filter_by(id=item_id). \
                    values(
                    {'dishes_count': cls.model.dishes_count - dishes}
                )
                await session.execute(query)
                await session.commit()

    @classmethod
    async def get_count_of_children(cls, item_id: uuid.UUID, child_model) -> int:
        async with async_session_maker() as session:
            query = (
                select(func.count(child_model.id))
                .select_from(cls.model)
                .join(child_model, item_id == child_model.submenu_id)
                .where(item_id == child_model.submenu_id)
            )

            children_count = await session.execute(query)
            children_count = children_count.scalar()

            return children_count
