#!/usr/bin/env python3

"""Contains a cache class"""

from typing import Union
from uuid import uuid4

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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate random id, stes it as the key and use the data
        passed to the function as the value
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes]:
        """
        Retrieve data from Redis using the provided key and optionally apply the conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional): A conversion function to apply to the retrieved data.

        Returns:
            Union[str, bytes]: The retrieved data from Redis, optionally converted using fn.
        """
        data: bytes = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis using the provided key and return it as a string.

        Args:
            key (str): The key to retrieve the string from Redis.

        Returns:
            str: The retrieved string from Redis.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis using the provided key and return it as an integer.

        Args:
            key (str): The key to retrieve the integer from Redis.

        Returns:
            int: The retrieved integer from Redis.
        """
        return self.get(key, fn=int)
