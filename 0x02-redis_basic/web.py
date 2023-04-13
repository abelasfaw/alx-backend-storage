#!/usr/bin/env python3
'''expiring web cache and tracker'''
import redis
import requests
from typing import Callable


_redis = redis.Redis()


def count_access(func: Callable) -> Callable:
    """counts page access"""
    def wrapper(*args, **kwargs):
        """wrapper"""
        key = "count:{}".format(args[0])
        _redis.incr(key)
        return func(*args, **kwargs)
    return wrapper


def get_cached_page(func: Callable) -> Callable:
    """returns cached page content"""
    def wrapper(*args, **kwargs):
        """wrapper"""
        key = "result:{}".format(args[0])
        if _redis.exists(key):
            data = _redis.get(key)
            return data.decode('utf-8')
        return func(*args, **kwargs)
    return wrapper


@get_cached_page
@count_access
def get_page(url: str) -> str:
    '''obtains the HTML content of a particular URL and returns it'''
    key = "count:{}".format(url)
    page_content = requests.get(url)
    _redis.set(key, page_content.text, ex=10)
    return response.text
