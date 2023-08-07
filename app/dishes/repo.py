import uuid

from fastapi import HTTPException
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError

from app.dishes import Dishes
from app.dishes.dao import DishesDAO
from app.dishes.exeptions import DishDontExistsException
from app.dishes.shemas import SDishAddIn, SDishUpdate
from app.menus.dao import MenusDAO
from app.submenus.dao import SubmenusDAO


class DishRepository:

    @staticmethod
    async def get_dish(dish_id: uuid.UUID, submenu_id: uuid.UUID) -> RowMapping:
        dish = await DishesDAO.find_one_or_none(id=dish_id, submenu_id=submenu_id)
        if not dish:
            raise DishDontExistsException
        return dish

    @staticmethod
    async def get_all_dishes(**filter_by) -> list[RowMapping]:
        dishes = await DishesDAO.find_all(**filter_by)
        return dishes

    @staticmethod
    async def add_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish: SDishAddIn) -> Dishes:
        try:
            new_dish = await DishesDAO.add_item(submenu_id=submenu_id, **dish.model_dump())

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Title must be uniq"
            )

        else:
            await SubmenusDAO.update_counters(item_id=submenu_id, dishes=1)
            await MenusDAO.update_counters(item_id=menu_id, dishes=1)
            return new_dish

    @staticmethod
    async def update_dish(submenu_id: uuid.UUID, dish_id: uuid.UUID, data: SDishUpdate) -> Dishes:
        submenu = await DishesDAO.find_one_or_none(id=dish_id, submenu_id=submenu_id)
        if not submenu:
            raise DishDontExistsException

        update_data = data.model_dump(exclude_unset=True)
        filters = {"id": dish_id, "submenu_id": submenu_id}

        try:
            updated_submenu = await DishesDAO.update_item(filters, **update_data)

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Title already exist, must be uniq"
            )
        else:
            return updated_submenu

    @staticmethod
    async def delete_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> dict[str, str | bool]:
        dish = await DishesDAO.find_one_or_none(id=dish_id, submenu_id=submenu_id)
        if not dish:
            raise DishDontExistsException

        await SubmenusDAO.update_counters(item_id=submenu_id, dishes=1, addition=False)
        await MenusDAO.update_counters(item_id=menu_id, dishes=1, addition=False)

        filters = {"id": dish_id, "submenu_id": submenu_id}
        await DishesDAO.delete_item(filters)

        return {
            "status": True,
            "message": "The dish has been deleted"
        }
