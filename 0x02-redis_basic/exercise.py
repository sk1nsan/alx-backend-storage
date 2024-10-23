#!/usr/bin/env python3
""" Redis """

import redis
from uuid import uuid4


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        key = str(uuid4())
        self._redis.set(key, data)
        return key
