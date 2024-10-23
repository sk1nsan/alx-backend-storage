#!/usr/bin/env python3
""" Redis """

import redis
import requests

cache = redis.Redis()


def get_page(url: str) -> str:
    """ obtain the HTML content of a particular URL and returns it """
    key = f"count{url}"
    if (not cache.get(key)):
        cache.set(url, 1, ex=10)
    else:
        cache.incr(url)
    return requests.get(url).text
