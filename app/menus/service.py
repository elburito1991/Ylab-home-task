import uuid

from fastapi import Depends
from sqlalchemy import RowMapping

from app.cache.cache import CacheItems
from app.menus import Menus
from app.menus.repo import MenuRepository
from app.menus.shemas import SMenuAddIn, SMenuUpdate


class MenuService:

    def __init__(self, dao: MenuRepository = Depends(), cache: CacheItems = Depends()):
        self.dao = dao
        self.cache = cache

    async def get_menu(self, menu_id: uuid.UUID) -> RowMapping:
        menu = await self.cache.get_cache(f'menu.get_menu.{menu_id}')
        if not menu:
            menu = await self.dao.get_menu(menu_id)
            await self.cache.set_cache(f'menu.get_menu.{menu_id}', menu)
        return menu

    async def get_menus(self) -> list[RowMapping]:
        menus = await self.cache.get_cache('menu.get_menus')
        if not menus:
            menus = await self.dao.get_all_menus()
            await self.cache.set_cache('menu.get_menus', menus)
        return menus

    async def add_menu(self, menu: SMenuAddIn) -> Menus:
        await self.cache.delete_cache(['menu.get_menus'])
        menu = await self.dao.add_menu(menu)
        return menu

    async def update_menu(self, menu_id: uuid.UUID, data: SMenuUpdate) -> Menus:
        await self.cache.delete_cache(['menu.get_menus', f'menu.get_menu.{menu_id}'])
        updated_menu = await self.dao.update_menu(menu_id, data)
        return updated_menu

    async def delete_menu(self, menu_id: uuid.UUID) -> dict[str, str | bool]:
        await self.cache.flush_redis()
        deleted_menu = await self.dao.delete_menu(menu_id)
        return deleted_menu
