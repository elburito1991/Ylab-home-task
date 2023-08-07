import pickle
from typing import Any

import aioredis
from sqlalchemy import RowMapping

from app.config import settings


class CacheItems:
    redis_conf = aioredis.from_url(f'redis://{settings.REDIS_HOST}', decode_responses=False)

    @classmethod
    async def set_cache(cls, request: str, response: Any) -> None:
        response = pickle.dumps(response)
        async with cls.redis_conf as redis:
            await redis.set(request, response)

    @classmethod
    async def get_cache(cls, request: str) -> list[RowMapping] | RowMapping:
        async with cls.redis_conf as redis:
            byte_request = bytes(request, 'utf-8')
            cache = await redis.get(byte_request)
            if cache:
                cache = pickle.loads(cache)
            return cache

    @classmethod
    async def delete_cache(cls, request: list[str]) -> None:
        async with cls.redis_conf as redis:
            await redis.delete(*request)

    @classmethod
    async def flush_redis(cls) -> None:
        async with cls.redis_conf as redis:
            await redis.flushdb(asynchronous=True)
