#!/usr/bin/env python3
'''Redis using python'''
import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function
    """
    inputs = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """decorator wrapper"""
        self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(output))
        return output
    return wrapper


class Cache():
    ''' Redis cache class'''

    def __init__(self):
        '''stores instance of redis as client as private variable
        and flushes instance'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''stores data in redis using generated key'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        '''retreives data from redis in its original type'''
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        '''converts byte to string'''
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        '''converts byte to int'''
        return int(data)
