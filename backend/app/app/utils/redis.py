"""Services module."""

from aioredis import Redis


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self) -> str:
        await self._redis.set("my-key", "value")
        return await self._redis.get("my-key")

    def set_value(self, key: str, value: str, expire: int) -> str:
        self._redis.set(key, value, expire)
        result = self._redis.get(key)
        return result

    def get_value(self, key: str) -> str:
        return self._redis.get(key)

    def del_key(self, key: str) -> str:
        return self._redis.delete(key)
