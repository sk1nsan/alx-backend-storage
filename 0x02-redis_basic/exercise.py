#!/usr/bin/env python3
""" Redis """

import redis
from uuid import uuid4
from typing import Callable, TypeVar, Any, Union
from functools import wraps

T = TypeVar("T")


def count_calls(method: Callable[..., Any]) -> Callable[..., Any]:
    """ keep track of the number of calls """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ keep track of the number of calls """
        name = method.__qualname__
        if (self._redis.get(name)):
            self._redis.incr(name)
        else:
            self._redis.set(name, 1)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ cache class """

    def __init__(self):
        """ initalize a cache instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ stores data with a random key """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[None, Callable[[bytes], T]] = None) -> T:
        """ return data """
        result = self._redis.get(key)
        if not result or not fn:
            return result
        return fn(result)

    def get_str(self, key: str) -> str:
        """ return data as a string """
        result = self._redis.get(key)
        if not result:
            return result
        return str(result)

    def get_int(self, key: str) -> int:
        """ return data as an int """
        result = self._redis.get(key)
        if not result:
            return result
        return int(result)
