import json
from typing import Union, Any

import redis.asyncio as redis
from loguru import logger

from bot.config import CONFIG


def redis_connect(func):
    async def wrapper(*args, **kwargs):
        async with redis.from_url(CONFIG.REDIS_URL, db=CONFIG.REDIS_DB) as r:
            return await func(*args, **kwargs, cache=r)
    return wrapper


class CacheController:
    @classmethod
    @redis_connect
    async def add(cls, key: str, data: Union[dict, list, Any], cache: redis.client.Redis):
        await cache.set(key, json.dumps(data))

    @classmethod
    @redis_connect
    async def get(cls, key: str, cache: redis.client.Redis):
        res = await cache.get(key)
        if res:
            return json.loads(res)
        return None

    @classmethod
    @redis_connect
    async def remove(cls, key: str, cache: redis.client.Redis):
        await cache.delete(key)

    @classmethod
    @redis_connect
    async def restart(cls, key: str, cache: redis.client.Redis):
        await cache.delete(key)
        await cache.set(key, json.dumps(dict()))

    @classmethod
    @redis_connect
    async def create_q_set(cls, user_id: str, new_data: dict, cache: redis.client.Redis):
        old_cache = await cache.get(user_id)
        if old_cache:
            old_cache = json.loads(old_cache)
            old_cache[user_id] = new_data
            await cache.set(user_id, json.dumps(old_cache))
            return old_cache
        return None

    @classmethod
    @redis_connect
    async def update_answer(cls, user_id: int, q_id: str, new_data: str, cache: redis.client.Redis):
        old_cache = await cache.get(user_id)
        logger.info(old_cache)
        if old_cache:
            old_cache = json.loads(old_cache)
            old_cache[user_id][q_id] = new_data
            await cache.set(user_id, json.dumps(old_cache))
            return old_cache
        return None
