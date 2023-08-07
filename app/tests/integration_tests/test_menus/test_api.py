from httpx import AsyncClient

from app.tests.base_const import Menu


async def test_get_all_menus(ac: AsyncClient):
    response = await ac.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


async def test_post_menu(ac: AsyncClient):
    response_post = await ac.post('/api/v1/menus', json={
        'title': 'My menu 1',
        'description': 'My menu description 1'
    })
    response_data = response_post.json()
    Menu.id, Menu.title, Menu.description \
        = response_data['id'], response_data['title'], response_data['description']

    assert response_post.status_code == 201
    assert response_data['id']
    assert response_data['title']
    assert response_data['description']


async def test_get_all_menus_after_post(ac: AsyncClient):
    response_get_all_menus = await ac.get('/api/v1/menus')

    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() != []


async def test_get_exact_menu_after_post(ac: AsyncClient):
    response_get_by_id = await ac.get(f'/api/v1/menus/{Menu.id}')
    response_data = response_get_by_id.json()

    assert response_get_by_id.status_code == 200
    assert response_data['id'] == Menu.id
    assert response_data['title'] == Menu.title
    assert response_data['description'] == Menu.description


async def test_update_menu(ac: AsyncClient):
    response_patch_menu = await ac.patch(f'/api/v1/menus/{Menu.id}', json={
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    })
    assert response_patch_menu.status_code == 200

    menu_obj_new = response_patch_menu.json()
    assert Menu.title != menu_obj_new['title']
    assert Menu.description != menu_obj_new['description']

    assert menu_obj_new['title'] == 'My updated menu 1'
    assert menu_obj_new['description'] == 'My updated menu description 1'


async def test_delete_menu(ac: AsyncClient):
    menus_li = await ac.get('/api/v1/menus')
    menu_obj_id = menus_li.json()[0]['id']

    response_delete_menu = await ac.delete(f'/api/v1/menus/{menu_obj_id}')
    assert response_delete_menu.status_code == 200


async def test_get_all_menus_after_del(ac: AsyncClient):
    response_get_all_menus = await ac.get('/api/v1/menus')
    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() == []


async def test_get_exact_menu_after_del(ac: AsyncClient):
    response_get_menu_by_id = await ac.get(f'/api/v1/menus/{Menu.id}')
    assert response_get_menu_by_id.json()['detail'] == 'menu not found'
