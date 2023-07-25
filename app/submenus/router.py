import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError

from app.dishes import Dishes
from app.menus.dao import MenusDAO
from app.submenus.dao import SubmenusDAO
from app.submenus.exeptions import SubmenuDontExistsException
from app.submenus.shemas import SSubmenuAddIn, SSubmenuAddOut, SSubmenuUpdate

router = APIRouter(
    prefix="/menus",
    tags=["Подразделы меню"]
)


@router.get("/{menu_id}/submenus", response_model=list[SSubmenuAddOut], status_code=200)
@version(1)
async def get_submenus(menu_id: uuid.UUID):
    submenus = await SubmenusDAO.find_all(menu_id=menu_id)
    return jsonable_encoder(submenus)


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=SSubmenuAddOut, status_code=200)
@version(1)
async def get_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    submenu = await SubmenusDAO.find_one_or_none(menu_id=menu_id, id=submenu_id)
    if not submenu:
        raise SubmenuDontExistsException

    return jsonable_encoder(submenu)


@router.post("/{menu_id}/submenus", response_model=SSubmenuAddOut, status_code=201)
@version(1)
async def add_submenu(menu_id: uuid.UUID, menu: SSubmenuAddIn):
    try:
        new_submenu = await SubmenusDAO.add_item(menu_id=menu_id, **menu.model_dump())

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Title must be uniq"
        )
    else:
        await MenusDAO.update_counters(menu_id, submenu=1)
        return jsonable_encoder(new_submenu)


@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SSubmenuAddOut, status_code=200)
@version(1)
async def update_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, item: SSubmenuUpdate):
    submenu = await SubmenusDAO.find_one_or_none(menu_id=menu_id, id=submenu_id)
    if not submenu:
        raise SubmenuDontExistsException

    update_data = item.model_dump(exclude_unset=True)
    filters = {"id": submenu_id, "menu_id": menu_id}

    try:
        updated_submenu = await SubmenusDAO.update_item(filters, **update_data)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Title already exist, must be uniq"
        )
    else:
        return jsonable_encoder(updated_submenu)


@router.delete("/{menu_id}/submenus/{submenu_id}", status_code=200)
@version(1)
async def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    submenu = await SubmenusDAO.find_one_or_none(menu_id=menu_id, id=submenu_id)
    if not submenu:
        raise SubmenuDontExistsException

    dishes_count = await SubmenusDAO.get_count_of_children(submenu_id, Dishes)
    await MenusDAO.update_counters(menu_id, submenu=1, dishes=dishes_count, addition=False)

    filters = {"id": submenu_id, "menu_id": menu_id}
    await SubmenusDAO.delete_item(filters)

    return {
        "status": True,
        "message": "The submenu has been deleted"
    }
