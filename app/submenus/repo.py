import uuid

from fastapi import HTTPException
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError

from app.dishes import Dishes
from app.menus.dao import MenusDAO
from app.submenus import Submenus
from app.submenus.dao import SubmenusDAO
from app.submenus.exeptions import SubmenuDontExistsException
from app.submenus.shemas import SSubmenuAddIn, SSubmenuUpdate


class SubmenuRepository:

    @staticmethod
    async def get_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID) -> RowMapping:
        submenu = await SubmenusDAO.find_one_or_none(id=submenu_id, menu_id=menu_id)
        if not submenu:
            raise SubmenuDontExistsException
        return submenu

    @staticmethod
    async def get_all_submenus(**filter_by) -> list[RowMapping]:
        submenus = await SubmenusDAO.find_all(**filter_by)
        return submenus

    @staticmethod
    async def add_submenu(menu_id: uuid.UUID, submenu: SSubmenuAddIn) -> Submenus:
        try:
            new_submenu = await SubmenusDAO.add_item(menu_id=menu_id, **submenu.model_dump())

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail='Title must be uniq'
            )
        else:
            await MenusDAO.update_counters(menu_id, submenu=1)
            return new_submenu

    @staticmethod
    async def update_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, data: SSubmenuUpdate) -> Submenus:
        submenu = await SubmenusDAO.find_one_or_none(id=submenu_id, menu_id=menu_id)
        if not submenu:
            raise SubmenuDontExistsException

        update_data = data.model_dump(exclude_unset=True)
        filters = {'id': submenu_id, 'menu_id': menu_id}

        try:
            updated_submenu = await SubmenusDAO.update_item(filters, **update_data)

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail='Title already exist, must be uniq'
            )
        else:
            return updated_submenu

    @staticmethod
    async def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID) -> dict[str, str | bool]:
        submenu = await SubmenusDAO.find_one_or_none(id=submenu_id, menu_id=menu_id)
        if not submenu:
            raise SubmenuDontExistsException

        dishes_count = await SubmenusDAO.get_count_of_children(submenu_id, Dishes)
        await MenusDAO.update_counters(menu_id, submenu=1, dishes=dishes_count, addition=False)

        filters = {'id': submenu_id, 'menu_id': menu_id}
        await SubmenusDAO.delete_item(filters)

        return {
            'status': True,
            'message': 'The submenu has been deleted'
        }
