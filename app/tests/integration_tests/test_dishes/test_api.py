from httpx import AsyncClient

from app.tests.base_const import Dish, Menu, Submenu


async def test_post_menu(ac: AsyncClient):
    response_post = await ac.post('/api/v1/menus', json={
        'title': 'My menu 1',
        'description': 'My menu description 1'
    })

    assert response_post.status_code == 201
    Menu.id = response_post.json()['id']


async def test_post_submenu(ac: AsyncClient):
    response_post_submenu = await ac.post(f'/api/v1/menus/{Menu.id}/submenus', json={
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    })
    assert response_post_submenu.status_code == 201
    Submenu.id = response_post_submenu.json()['id']


async def test_get_all_dishes_is_empty(ac: AsyncClient):
    response_get_all_dishes = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes')
    assert response_get_all_dishes.status_code == 200
    assert response_get_all_dishes.json() == []


async def test_post_dishes(ac: AsyncClient):
    response_post_dishes = await ac.post(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes', json={
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    })

    response_data = response_post_dishes.json()
    assert response_post_dishes.status_code == 201
    assert response_data['id']
    assert response_data['title']
    assert response_data['description']
    assert response_data['price']

    Dish.id, Dish.title, Dish.description, Dish.price = \
        response_data['id'], response_data['title'], response_data['description'], response_data['price']


async def test_get_all_dishes_after_post(ac: AsyncClient):
    response_get_all_dishes = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes')
    assert response_get_all_dishes.status_code == 200
    assert response_get_all_dishes.json() != []


async def test_get_exact_dish_after_post(ac: AsyncClient):
    response_get_dish = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes/{Dish.id}')

    response_data = response_get_dish.json()
    assert response_get_dish.status_code == 200
    assert response_data['id'] == Dish.id
    assert response_data['title'] == Dish.title
    assert response_data['description'] == Dish.description
    assert response_data['price'] == Dish.price


async def test_update_dish(ac: AsyncClient):
    response_patch_dish = await ac.patch(
        f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes/{Dish.id}',
        json={
            'title': 'My updated dish 1',
            'description': 'My updated dish description 1',
            'price': '14.50'
        })
    assert response_patch_dish.status_code == 200

    response_data = response_patch_dish.json()
    assert Dish.title != response_data['title']
    assert Dish.description != response_data['description']
    assert Dish.price != response_data['price']

    assert response_data['title'] == 'My updated dish 1'
    assert response_data['description'] == 'My updated dish description 1'
    assert response_data['price'] == '14.50'

    Dish.title, Dish.description, Dish.price = \
        response_data['title'], response_data['description'], response_data['price']


async def test_get_exact_dish_after_upd(ac: AsyncClient):
    response_get_dish = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes/{Dish.id}')

    response_data = response_get_dish.json()
    assert response_get_dish.status_code == 200
    assert response_data['id'] == Dish.id
    assert response_data['title'] == Dish.title
    assert response_data['description'] == Dish.description
    assert response_data['price'] == Dish.price


async def test_del_dish(ac: AsyncClient):
    response_delete_dish = await ac.delete(
        f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes/{Dish.id}'
    )
    assert response_delete_dish.status_code == 200


async def test_get_all_dishes_after_del(ac: AsyncClient):
    response_get_all_dishes = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes')
    assert response_get_all_dishes.status_code == 200
    assert response_get_all_dishes.json() == []


async def test_get_exact_dish_after_del(ac: AsyncClient):
    response_get_dish = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes/{Dish.id}')
    assert response_get_dish.status_code == 404
    assert response_get_dish.json()['detail'] == 'dish not found'


async def test_del_submenus(ac: AsyncClient):
    response_delete_submenu = await ac.delete(
        f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}'
    )
    assert response_delete_submenu.status_code == 200


async def test_get_all_submenus_after_del(ac: AsyncClient):
    response_get_all_submenus = await ac.get(f'/api/v1/menus/{Menu.id}/submenus')
    assert response_get_all_submenus.status_code == 200
    assert response_get_all_submenus.json() == []


async def test_delete_menu(ac: AsyncClient):
    response_delete_menu = await ac.delete(f'/api/v1/menus/{Menu.id}')
    assert response_delete_menu.status_code == 200


async def test_get_exact_menu_after_del(ac: AsyncClient):
    response_get_all_menus = await ac.get('/api/v1/menus')
    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() == []
