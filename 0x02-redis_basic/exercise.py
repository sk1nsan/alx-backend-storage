#!/usr/bin/env python3
""" Redis """

import redis
from uuid import uuid4
from typing import Callable, TypeVar, Any
from functools import wraps

T = TypeVar("T")


def count_calls(method: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        name = method.__qualname__
        if (self._redis.get(name)):
            self._redis.incr(name)
        else:
            self._redis.set(name, 1)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: str | bytes | int | float) -> str:
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: None | Callable[[bytes], T] = None) -> T:
        result = self._redis.get(key)
        if not result or not fn:
            return result
        return fn(result)

    def get_str(self, key: str) -> str:
        result = self._redis.get(key)
        if not result:
            return result
        return str(result)

    def get_int(self, key: str) -> int:
        result = self._redis.get(key)
        if not result:
            return result
        return int(result)
