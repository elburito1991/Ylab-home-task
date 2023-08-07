import uuid

from fastapi import HTTPException
from sqlalchemy import RowMapping
from sqlalchemy.exc import IntegrityError

from app.menus import Menus
from app.menus.dao import MenusDAO
from app.menus.exeptions import MenuDontExistsException
from app.menus.shemas import SMenuAddIn, SMenuUpdate


class MenuRepository:

    @staticmethod
    async def get_menu(menu_id: uuid.UUID) -> RowMapping:
        menu = await MenusDAO.find_one_or_none(id=menu_id)
        if not menu:
            raise MenuDontExistsException
        return menu

    @staticmethod
    async def get_all_menus() -> list[RowMapping]:
        menus = await MenusDAO.find_all()
        return menus

    @staticmethod
    async def add_menu(menu: SMenuAddIn) -> Menus:
        try:
            new_menu = await MenusDAO.add_item(**menu.model_dump())

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Title must be uniq"
            )
        else:
            return new_menu

    @staticmethod
    async def update_menu(menu_id: uuid.UUID, data: SMenuUpdate) -> Menus:
        menu = await MenusDAO.find_one_or_none(id=menu_id)
        if not menu:
            raise MenuDontExistsException

        update_data = data.model_dump(exclude_unset=True)
        filters = {"id": menu_id}

        try:
            updated_menu = await MenusDAO.update_item(filters, **update_data)

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Title already exist, must be uniq"
            )
        else:
            return updated_menu

    @staticmethod
    async def delete_menu(menu_id: uuid.UUID) -> dict[str, str | bool]:
        menu = await MenusDAO.find_one_or_none(id=menu_id)
        if not menu:
            raise MenuDontExistsException

        filters = {"id": menu_id}
        await MenusDAO.delete_item(filters)

        return {
            "status": True,
            "message": "The menu has been deleted"
        }
