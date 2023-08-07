import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version

from app.menus.service import MenuService
from app.menus.shemas import SMenuAddIn, SMenuAddOut, SMenuUpdate

router = APIRouter(
    prefix="/menus",
    tags=["Меню"]
)


@router.get("", response_model=list[SMenuAddOut], status_code=200)
@version(1)
async def get_menus(menu_service: MenuService = Depends()) -> list[SMenuAddOut]:
    result = await menu_service.get_menus()
    return jsonable_encoder(result)


@router.get("/{menu_id}", response_model=SMenuAddOut, status_code=200)
@version(1)
async def get_menu(menu_id: uuid.UUID, menu_service: MenuService = Depends()) -> SMenuAddOut:
    result = await menu_service.get_menu(menu_id)
    return jsonable_encoder(result)


@router.post("", response_model=SMenuAddOut, status_code=201)
@version(1)
async def add_menu(menu: SMenuAddIn, menu_service: MenuService = Depends()) -> SMenuAddOut:
    result = await menu_service.add_menu(menu)
    return jsonable_encoder(result)


@router.patch("/{menu_id}", response_model=SMenuAddOut)
@version(1)
async def update_menu(menu_id: uuid.UUID, item: SMenuUpdate, menu_service: MenuService = Depends()) -> SMenuAddOut:
    result = await menu_service.update_menu(menu_id, item)
    return jsonable_encoder(result)


@router.delete("/{menu_id}", status_code=200)
@version(1)
async def delete_menu(menu_id: uuid.UUID, menu_service: MenuService = Depends()) -> dict[str, str | bool]:
    # TODO исправить аннотацию
    result = await menu_service.delete_menu(menu_id)
    return result
