#!/usr/bin/env python3

"""Contains a cache class"""

from typing import Union, Callable
from uuid import uuid4
from functools import wraps

import redis


def replay(method):
    """
    Display the history of calls
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_str, output_str in zip(inputs, outputs):
        input_args = eval(input_str.decode('utf-8'))
        output_value = output_str.decode('utf-8')
        input_args_str = ", ".join(repr(arg) for arg in input_args)
        print(f"{method.__qualname__}(*({input_args_str},)) -> {output_value}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator function that takes in a callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """increment count"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Returns callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Invoke a function"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        ret = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, ret)
        return ret
    return wrapper


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

    @call_history
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


cache = Cache()

s1 = cache.store("foo")
s2 = cache.store("bar")
s3 = cache.store(42)

replay(cache.store)
