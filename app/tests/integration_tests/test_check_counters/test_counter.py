from httpx import AsyncClient

from app.tests.base_const import Menu, Submenu


class TestCounters:

    async def test_post_items(self, ac: AsyncClient):
        response_post_menu = await ac.post("/api/v1/menus", json={
            "title": "My menu 1",
            "description": "My menu description 1"
        })
        assert response_post_menu.status_code == 201
        response_data = response_post_menu.json()
        Menu.id = response_data["id"]

        response_post_submenu = await ac.post(f"/api/v1/menus/{Menu.id}/submenus", json={
            "title": "My submenu 1",
            "description": "My submenu description 1"
        })
        assert response_post_menu.status_code == 201
        response_data = response_post_submenu.json()
        Submenu.id = response_data["id"]

        for i in range(1, 3):
            response_post_dishes = await ac.post(f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes", json={
                "title": f"My dish {i}",
                "description": f"My dish description {i}",
                "price": "12.50"
            })
            assert response_post_dishes.status_code == 201

    async def test_check_items_counters_after_post(self, ac: AsyncClient):
        menu_obj = await ac.get(f"/api/v1/menus/{Menu.id}")
        menu_obj_data = menu_obj.json()
        assert menu_obj_data["submenus_count"] == 1
        assert menu_obj_data["dishes_count"] == 2

        submenu_obj = await ac.get(f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}")
        submenu_obj_data = submenu_obj.json()
        assert submenu_obj_data["dishes_count"] == 2

    async def test_del_submenu(self, ac: AsyncClient):
        response_del_submenu = await ac.delete(f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}")
        assert response_del_submenu.status_code == 200

    async def test_check_submenu_and_children_are_deleted(self, ac: AsyncClient):
        response_get_all_submenus = await ac.get(f"/api/v1/menus/{Menu.id}/submenus")
        assert response_get_all_submenus.status_code == 200
        assert response_get_all_submenus.json() == []

        response_get_all_dishes = await ac.get(f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes")
        assert response_get_all_dishes.status_code == 200
        assert response_get_all_dishes.json() == []

    async def test_check_menu_counters_after_submenu_del(self, ac: AsyncClient):
        menu_obj = await ac.get(f"/api/v1/menus/{Menu.id}")
        menu_obj_data = menu_obj.json()
        assert menu_obj_data["submenus_count"] == 0
        assert menu_obj_data["dishes_count"] == 0

    async def test_del_menu(self, ac: AsyncClient):
        response_delete_menu = await ac.delete(f"/api/v1/menus/{Menu.id}")
        assert response_delete_menu.status_code == 200

    async def test_menu_list_is_empty(self, ac: AsyncClient):
        response = await ac.get("/api/v1/menus")
        assert response.status_code == 200
        assert response.json() == []
