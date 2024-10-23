#!/usr/bin/env python3
""" Redis """

import redis
import requests

cache = redis.Redis()


def get_page(url: str) -> str:
    """ obtain the HTML content of a particular URL and returns it """
    key = f"count{url}"
    result = requests.get(url).text

    cache.incr(key)
    cache.set(url, result, ex=10)

    return requests.get(url).text
