from httpx import AsyncClient

from app.tests.base_const import Menu, Submenu


async def test_post_menu(ac: AsyncClient):
    response_post_menu = await ac.post('/api/v1/menus', json={
        'title': 'My menu 1',
        'description': 'My menu description 1'
    })
    Menu.id = response_post_menu.json()['id']

    assert response_post_menu.status_code == 201


async def test_get_all_submenu_is_empty(ac: AsyncClient):
    response_get_all_submenus = await ac.get(f'/api/v1/menus/{Menu.id}/submenus')
    assert response_get_all_submenus.status_code == 200
    assert response_get_all_submenus.json() == []


async def test_post_submenu(ac: AsyncClient):
    response_post_submenu = await ac.post(f'/api/v1/menus/{Menu.id}/submenus', json={
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    })
    response_data = response_post_submenu.json()

    assert response_data['id']
    assert response_data['title']
    assert response_data['description']
    Submenu.id, Submenu.title, Submenu.description = \
        response_data['id'], response_data['title'], response_data['description']


async def test_get_all_submenus_after_post(ac: AsyncClient):
    response_get_all_submenus = await ac.get(f'/api/v1/menus/{Menu.id}/submenus')
    assert response_get_all_submenus.status_code == 200
    assert response_get_all_submenus.json() != []


async def test_get_exact_submenu_after_post(ac: AsyncClient):
    response_get_exact_submenu = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}')
    response_data = response_get_exact_submenu.json()
    assert response_data['id']
    assert response_data['title']
    assert response_data['description']


async def test_update_submenu(ac: AsyncClient):
    response_patch_submenu = await ac.patch(
        f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}',
        json={
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1'
        })
    assert response_patch_submenu.status_code == 200

    submenu_obj_new = response_patch_submenu.json()
    assert Submenu.title != submenu_obj_new['title']
    assert Submenu.description != submenu_obj_new['description']

    assert submenu_obj_new['title'] == 'My updated submenu 1'
    assert submenu_obj_new['description'] == 'My updated submenu description 1'


async def test_get_exact_submenu_after_upd(ac: AsyncClient):
    response_get_exact_submenu = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}')
    response_data = response_get_exact_submenu.json()
    assert response_data['id']
    assert response_data['title']
    assert response_data['description']


async def test_del_submenus(ac: AsyncClient):
    response_delete_submenu = await ac.delete(
        f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}'
    )
    assert response_delete_submenu.status_code == 200


async def test_get_all_submenus_after_del(ac: AsyncClient):
    response_get_all_submenus = await ac.get(f'/api/v1/menus/{Menu.id}/submenus')
    assert response_get_all_submenus.status_code == 200
    assert response_get_all_submenus.json() == []


async def test_get_exact_submenu_after_del(ac: AsyncClient):
    response_get_exact_submenu = await ac.get(f'/api/v1/menus/{Menu.id}/submenus/{Submenu.id}')
    assert response_get_exact_submenu.json()['detail'] == 'submenu not found'


async def test_delete_menu(ac: AsyncClient):
    response_delete_menu = await ac.delete(f'/api/v1/menus/{Menu.id}')
    assert response_delete_menu.status_code == 200


async def test_get_exact_menu_after_del(ac: AsyncClient):
    response_get_all_menus = await ac.get('/api/v1/menus')
    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() == []
