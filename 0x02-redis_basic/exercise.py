#!/usr/bin/env python3
""" Redis """

import redis
from uuid import uuid4
from typing import Callable, Union, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
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


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function"""
        name = method.__qualname__
        self._redis.rpush(name + ":inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(name + ":outputs", str(result))
        return result
    return wrapper


def replay(method: Callable):
    """ display the history of calls of a particular function """
    name = method.__qualname__
    cache = method.__self__._redis
    nums_called = int(cache.get(name))
    calls = dict(zip(cache.lrange(name + ":inputs", 0, -1),
                     cache.lrange(name + ":outputs", 0, -1)))
    print(f"{name} was called {nums_called} times:")
    for input, output in calls.items():
        print(f"{name}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """ cache class """

    def __init__(self):
        """ initalize a cache instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ stores data with a random key """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[None, Callable] = None) -> Any:
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
        return result.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ return data as an int """
        result = self._redis.get(key)
        if not result:
            return result
        return int(result)
