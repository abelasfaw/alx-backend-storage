#!/usr/bin/env python3
'''Redis using python'''
import uuid
import redis
from typing import Union


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
