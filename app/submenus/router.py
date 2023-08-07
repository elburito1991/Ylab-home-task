import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version

from app.submenus.service import SubmenuService
from app.submenus.shemas import SSubmenuAddIn, SSubmenuAddOut, SSubmenuUpdate

router = APIRouter(
    prefix="/menus",
    tags=["Подразделы меню"]
)


@router.get("/{menu_id}/submenus", response_model=list[SSubmenuAddOut], status_code=200)
@version(1)
async def get_submenus(menu_id: uuid.UUID, submenu_service: SubmenuService = Depends()) -> list[SSubmenuAddOut]:
    result = await submenu_service.get_submenus(menu_id)
    return jsonable_encoder(result)


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=SSubmenuAddOut, status_code=200)
@version(1)
async def get_submenu(
        menu_id: uuid.UUID, submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends()
) -> SSubmenuAddOut:
    result = await submenu_service.get_submenu(menu_id, submenu_id)
    return jsonable_encoder(result)


@router.post("/{menu_id}/submenus", response_model=SSubmenuAddOut, status_code=201)
@version(1)
async def add_submenu(
        menu_id: uuid.UUID, submenu: SSubmenuAddIn,
        submenu_service: SubmenuService = Depends()
) -> SSubmenuAddOut:
    result = await submenu_service.add_submenu(menu_id, submenu)
    return jsonable_encoder(result)


@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SSubmenuAddOut, status_code=200)
@version(1)
async def update_submenu(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, item: SSubmenuUpdate,
        submenu_service: SubmenuService = Depends()
) -> SSubmenuAddOut:
    result = await submenu_service.update_submenu(menu_id, submenu_id, item)
    return jsonable_encoder(result)


@router.delete("/{menu_id}/submenus/{submenu_id}", status_code=200)
@version(1)
async def delete_submenu(
        menu_id: uuid.UUID, submenu_id: uuid.UUID,
        submenu_service: SubmenuService = Depends()
) -> dict[str, str | bool]:
    # TODO исправить аннотацию
    result = await submenu_service.delete_submenu(menu_id, submenu_id)
    return result
