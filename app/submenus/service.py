import uuid

from fastapi import Depends
from sqlalchemy import RowMapping

from app.cache.cache import CacheItems
from app.submenus import Submenus
from app.submenus.repo import SubmenuRepository
from app.submenus.shemas import SSubmenuAddIn, SSubmenuUpdate


class SubmenuService:
    def __init__(self, dao: SubmenuRepository = Depends(), cache: CacheItems = Depends()):
        self.dao = dao
        self.cache = cache

    async def get_submenu(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> RowMapping:
        submenu = await self.cache.get_cache(f'submenu.get_submenu.{submenu_id}')
        if not submenu:
            submenu = await self.dao.get_submenu(menu_id, submenu_id)
            await self.cache.set_cache(f'submenu.get_submenu.{submenu_id}', submenu)
        return submenu

    async def get_submenus(self, menu_id: uuid.UUID) -> list[RowMapping]:
        submenus = await self.cache.get_cache('submenu.get_submenus')
        if not submenus:
            submenus = await self.dao.get_all_submenus(menu_id=menu_id)
            await self.cache.set_cache('submenu.get_submenus', submenus)

        return submenus

    async def add_submenu(self, menu_id: uuid.UUID, submenu: SSubmenuAddIn) -> Submenus:
        await self.cache.delete_cache(
            [
                'menu.get_menus',
                f'menu.get_menu.{menu_id}',
                'submenu.get_submenus'
            ]
        )
        submenu = await self.dao.add_submenu(menu_id, submenu)
        return submenu

    async def update_submenu(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SSubmenuUpdate) -> Submenus:
        await self.cache.delete_cache(
            [
                'submenu.get_submenus',
                f'submenu.get_submenu.{submenu_id}'
            ]
        )
        updated_submenu = await self.dao.update_submenu(menu_id, submenu_id, submenu)
        return updated_submenu

    async def delete_submenu(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> dict[str, str | bool]:
        await self.cache.flush_redis()
        deleted_submenu = await self.dao.delete_submenu(menu_id, submenu_id)
        return deleted_submenu
