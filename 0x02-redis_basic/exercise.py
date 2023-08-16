#!/usr/bin/env python3

"""Contains a cache class"""

from typing import Union, Callable
from uuid import uuid4
from functool import wraps

import redis


class Cache:
    """
    A cache class
    """
    def __init__(self):
        """
        Initializes the cache class
        Args:
            redis: Instance of the redis class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(fn: Callable) -> Callable:
        """
        Decorator to count the number of times
        a method is called

        Args:
            fn (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method.
        """
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            key = "{}".format(fn.__qualname__)
            self._redis.incr(key)
            return fn(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate random id, stes it as the key and use the data
        passed to the function as the value
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> [int, bytes, float, str]:
        """
        convert to any desired format
        """

        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        REtrieves a string from redis using the provided key and
        returns it as a sring
        Args:
            key: str retrieved from redis
        Return:
                str
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: int) -> int:
        """
           REtrieves a int from redis using the provided key and
        returns it as an integer
        Args:
            key: int retrieved from redis
        Return:
                int
        """

        return self.get(key, fn=int)
