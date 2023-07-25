import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version
from sqlalchemy.exc import IntegrityError

from app.menus.dao import MenusDAO
from app.menus.exeptions import MenuDontExistsException
from app.menus.shemas import SMenuAddIn, SMenuAddOut, SMenuUpdate

router = APIRouter(
    prefix="/menus",
    tags=["Меню"]
)


@router.get("", response_model=list[SMenuAddOut], status_code=200)
@version(1)
async def get_menus():
    menus = await MenusDAO.find_all()
    return jsonable_encoder(menus)


@router.get("/{menu_id}", response_model=SMenuAddOut, status_code=200)
@version(1)
async def get_menu(menu_id: uuid.UUID):
    menu = await MenusDAO.find_one_or_none(id=menu_id)
    if not menu:
        raise MenuDontExistsException

    return jsonable_encoder(menu)


@router.post("", response_model=SMenuAddOut, status_code=201)
@version(1)
async def add_menu(menu: SMenuAddIn):
    try:
        new_menu = await MenusDAO.add_item(**menu.model_dump())

    except IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Title must be uniq"
        )
    else:
        return jsonable_encoder(new_menu)


@router.patch("/{menu_id}", response_model=SMenuAddOut)
@version(1)
async def update_menu(menu_id: uuid.UUID, item: SMenuUpdate):
    menu = await MenusDAO.find_one_or_none(id=menu_id)
    if not menu:
        raise MenuDontExistsException

    update_data = item.model_dump(exclude_unset=True)
    filters = {"id": menu_id}

    try:
        updated_menu = await MenusDAO.update_item(filters, **update_data)
    except IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="Title already exist, must be uniq"
        )
    else:
        return jsonable_encoder(updated_menu)


@router.delete("/{menu_id}", status_code=200)
@version(1)
async def delete_menu(menu_id: uuid.UUID):
    menu = await MenusDAO.find_one_or_none(id=menu_id)
    if not menu:
        raise MenuDontExistsException

    filters = {"id": menu_id}
    await MenusDAO.delete_item(filters)

    return {
        "status": True,
        "message": "The menu has been deleted"
    }
