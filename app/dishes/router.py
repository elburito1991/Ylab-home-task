import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError

from app.dishes.dao import DishesDAO
from app.dishes.exeptions import DishDontExistsException
from app.dishes.shemas import SDishAddIn, SDishAddOut, SDishUpdate
from app.menus.dao import MenusDAO
from app.submenus.dao import SubmenusDAO

router = APIRouter(
    prefix="/menus",
    tags=["Блюда"]
)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes",
            response_model=list[SDishAddOut], status_code=200)
@version(1)
async def get_dishes(submenu_id: uuid.UUID):
    dishes = await DishesDAO.find_all(submenu_id=submenu_id)
    return jsonable_encoder(dishes)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            response_model=SDishAddOut, status_code=200)
@version(1)
async def get_dish(submenu_id: uuid.UUID, dish_id: uuid.UUID):
    dish = await DishesDAO.find_one_or_none(submenu_id=submenu_id, id=dish_id)
    if not dish:
        raise DishDontExistsException

    return jsonable_encoder(dish)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=SDishAddOut, status_code=201)
@version(1)
async def add_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, menu: SDishAddIn):
    try:
        new_dish = await DishesDAO.add_item(submenu_id=submenu_id, **menu.model_dump())

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Title must be uniq"
        )
    else:
        await SubmenusDAO.update_counters(item_id=submenu_id, dishes=1)
        await MenusDAO.update_counters(item_id=menu_id, dishes=1)
        return jsonable_encoder(new_dish)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=SDishAddOut, status_code=200)
@version(1)
async def update_dish(submenu_id: uuid.UUID, dish_id: uuid.UUID, item: SDishUpdate):
    dish = await DishesDAO.find_one_or_none(submenu_id=submenu_id, id=dish_id)
    if not dish:
        raise DishDontExistsException

    update_data = item.model_dump(exclude_unset=True)
    filters = {"id": dish_id, "submenu_id": submenu_id}

    try:
        updated_dish = await DishesDAO.update_item(filters, **update_data)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Title already exist, must be uniq"
        )
    else:
        return jsonable_encoder(updated_dish)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=200)
@version(1)
async def delete_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID):
    dish = await DishesDAO.find_one_or_none(submenu_id=submenu_id, id=dish_id)
    if not dish:
        raise DishDontExistsException

    await SubmenusDAO.update_counters(item_id=submenu_id, dishes=1, addition=False)
    await MenusDAO.update_counters(item_id=menu_id, dishes=1, addition=False)

    filters = {"id": dish_id, "submenu_id": submenu_id}
    await DishesDAO.delete_item(filters)

    return {
        "status": True,
        "message": "The menu has been deleted"
    }
