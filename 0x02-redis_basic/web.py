#!/usr/bin/env python3
'''expiring web cache and tracker'''
import redis
import requests
from functools import wraps


_redis = redis.Redis()


def count_page_access(method):
    """counts page access """
    @wraps(method)
    def wrapper(url):
        cache_key = "cache:" + url
        cached_data = _redis.get(cache_key)
        if cached_data:
            return cached_data.decode("utf-8")

        key = "count:{}".format(url)
        html = method(url)
        _redis.incr(key)
        _redis.set(cache_key, html)
        _redis.expire(cache_key, 10)
        return html
    return wrapper


@count_page_access
def get_page(url: str) -> str:
    '''obtains the HTML content of a particular URL and returns it'''
    page_content = requests.get(url)
    return page_content.text
