#!/usr/bin/env python3
"""contains a Cache class"""

import redis
import uuid
from typing import Union, Callable
import functools


class Cache:
    def __init__(self) -> None:
        """
        Initialize the Cache class by creating a Redis client
        instance and flushing the database.
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(fn: Callable) -> Callable:
        """
        Decorator to count the number of times a method is
        called and store the count in Redis.

        Args:
            fn (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method.
        """
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            key = "{}".format(fn.__qualname__)
            self._redis.incr(key)
            return fn(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key
        and return the key.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored
            in the cache.

        Returns:
            str: The generated random key used to store the data in Redis.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes]:
        """
        Retrieve data from Redis using the provided key and
        optionally apply the conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional): A conversion function to
            apply to the retrieved data.

        Returns:
            Union[str, bytes]: The retrieved data from Redis,
            optionally converted using fn.
        """
        data: bytes = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis using the provided key
        and return it as a string.

        Args:
            key (str): The key to retrieve the string from Redis.

        Returns:
            str: The retrieved string from Redis.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis using the provided key
        and return it as an integer.

        Args:
            key (str): The key to retrieve the integer from Redis.

        Returns:
            int: The retrieved integer from Redis.
        """
        return self.get(key, fn=int)
