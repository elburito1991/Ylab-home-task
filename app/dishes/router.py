import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version

from app.dishes.service import DishService
from app.dishes.shemas import SDishAddIn, SDishAddOut, SDishUpdate

router = APIRouter(
    prefix="/menus",
    tags=["Блюда"]
)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes",
            response_model=list[SDishAddOut], status_code=200)
@version(1)
async def get_dishes(submenu_id: uuid.UUID, dish_service: DishService = Depends()) -> list[SDishAddOut]:
    result = await dish_service.get_dishes(submenu_id)
    return jsonable_encoder(result)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            response_model=SDishAddOut, status_code=200)
@version(1)
async def get_dish(submenu_id: uuid.UUID, dish_id: uuid.UUID, dish_service: DishService = Depends()) -> SDishAddOut:
    result = await dish_service.get_dish(dish_id, submenu_id)
    return jsonable_encoder(result)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=SDishAddOut, status_code=201)
@version(1)
async def add_dish(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, dish: SDishAddIn,
        dish_service: DishService = Depends()
) -> SDishAddOut:
    result = await dish_service.add_dish(menu_id, submenu_id, dish)
    return jsonable_encoder(result)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=SDishAddOut, status_code=200)
@version(1)
async def update_dish(
        submenu_id: uuid.UUID, dish_id: uuid.UUID, dish: SDishUpdate,
        dish_service: DishService = Depends()
) -> SDishAddOut:
    result = await dish_service.update_dish(submenu_id, dish_id, dish)
    return jsonable_encoder(result)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200)
@version(1)
async def delete_dish(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID,
        dish_service: DishService = Depends()
) -> dict[str, str | bool]:
    result = await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    return result
