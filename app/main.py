from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis  # noqa

from app.cache.cache import CacheItems
from app.dishes.router import router as dish_router
from app.menus.router import router as menu_router
from app.submenus.router import router as submenu_router

app = FastAPI()

app.include_router(router=menu_router)
app.include_router(router=submenu_router)
app.include_router(router=dish_router)

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/api/v{major}',
                       )


async def shutdown() -> None:
    service = CacheItems()
    await service.flush_redis()
