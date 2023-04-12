#!/usr/bin/env python3
'''Redis using python'''
import uuid
import redis
from typing import Union, Optional, Callable


class Cache():
    ''' Redis cache class'''

    def __init__(self):
        '''stores instance of redis as client as private variable
        and flushes instance'''
        self._redis = redis.Redis()
        self._redis.flushdb()

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
