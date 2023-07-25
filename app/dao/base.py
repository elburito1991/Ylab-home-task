from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_item(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            new_obj = await session.execute(query)
            await session.commit()
            return new_obj.scalar()

    @classmethod
    async def update_item(cls, filters: dict, **data):
        async with async_session_maker() as session:
            query = update(cls.model) \
                .filter_by(**filters). \
                values(data).returning(cls.model)
            updated_obj = await session.execute(query)
            await session.commit()
            return updated_obj.scalar()

    @classmethod
    async def delete_item(cls, filters):
        async with async_session_maker() as session:
            query = delete(cls.model) \
                .filter_by(**filters) \
                .returning(cls.model.id)
            res = await session.execute(query)
            await session.commit()
            return res.scalar()

