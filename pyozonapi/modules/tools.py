import time
from typing import (
    Union,
    Protocol,
    Optional,
    Callable,
    Awaitable,
    Any
)
from math import ceil
from functools import wraps
from ..client import OzonClient


def list_division(_list: Union[list, str], divider: int) -> list:
    result = []

    if len(_list) == 0:
        return result

    for i in range(ceil(len(_list) / divider)):
        if (i + 1) * divider > len(_list):
            result.append(_list[i * divider:len(_list)])
        else:
            result.append(_list[i * divider:(i + 1) * divider])
    return result


class HasClient(Protocol):
    _client: OzonClient


def ttl_cache(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    cache = {}

    @wraps(func)
    async def wrapper(self: HasClient, *args, ttl: Optional[int] = None, **kwargs):
        client_id = id(self._client)
        cache_key = (client_id, func.__name__, args, tuple(kwargs.items()))
        current_time = time.time()

        ttl = ttl if ttl is not None else getattr(self._client, "ttl", None)

        if (ttl is not None) and (cache_key in cache):
            value, expiration = cache[cache_key]
            if (expiration is None) or (current_time < expiration):
                return value

        result = await func(self, *args, **kwargs)
        expiration = (current_time + ttl) if ttl else None
        cache[cache_key] = (result, expiration)

        return result

    return wrapper
