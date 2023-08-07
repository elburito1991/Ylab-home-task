import uuid

from fastapi import Depends
from sqlalchemy import RowMapping

from app.cache.cache import CacheItems
from app.dishes import Dishes
from app.dishes.repo import DishRepository
from app.dishes.shemas import SDishAddIn, SDishUpdate


class DishService:
    def __init__(self, dao: DishRepository = Depends(), cache: CacheItems = Depends()):
        self.dao = dao
        self.cache = cache

    async def get_dish(self, dish_id: uuid.UUID, submenu_id: uuid.UUID) -> RowMapping:
        dish = await self.cache.get_cache(f"dish.get_dish.{dish_id}")
        if not dish:
            dish = await self.dao.get_dish(dish_id, submenu_id)
            await self.cache.set_cache(f"dish.get_dish.{dish_id}", dish)
        return dish

    async def get_dishes(self, submenu_id: uuid.UUID) -> list[RowMapping]:
        dishes = await self.cache.get_cache("dish.get_dishes")
        if not dishes:
            dishes = await self.dao.get_all_dishes(submenu_id=submenu_id)
            await self.cache.set_cache("dish.get_dishes", dishes)
        return dishes

    async def add_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish: SDishAddIn) -> Dishes:
        await self.cache.delete_cache(
            [
                "menu.get_menus",
                f"menu.get_menu.{menu_id}",
                "submenu.get_submenus",
                f"submenu.get_submenu.{submenu_id}",
                "dish.get_dishes"
            ]
        )
        dish = await self.dao.add_dish(menu_id, submenu_id, dish)
        return dish

    async def update_dish(self, submenu_id: uuid.UUID, dish_id: uuid.UUID, data: SDishUpdate) -> Dishes:
        await self.cache.delete_cache(
            [
                "dish.get_dishes", f"dish.get_dish.{dish_id}"
            ]
        )
        updated_dish = await self.dao.update_dish(submenu_id, dish_id, data)
        return updated_dish

    async def delete_dish(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> dict[str, str | bool]:
        await self.cache.flush_redis()
        deleted_dish = await self.dao.delete_dish(menu_id, submenu_id, dish_id)
        return deleted_dish
