#!/usr/bin/env python3
""" Redis """

import redis
import requests

cache = redis.Redis()


def get_page(url: str) -> str:
    """ obtain the HTML content of a particular URL and returns it """
    count = f"count:{url}"
    result = f"result:{url}"

    cache.incr(count)

    cached_result = cache.get(result)
    if (cached_result):
        return cached_result.decode('utf-8')

    response = requests.get(url).text
    cache.set(result, response, ex=10)
    return response
