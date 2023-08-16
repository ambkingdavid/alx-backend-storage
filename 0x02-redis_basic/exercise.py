#!/usr/bin/env python3

"""Contains a cache class"""

from typing import Union, Callable
from uuid import uuid4
from functools import wraps

import redis


def replay(method):
    """
    Display the history of calls for a particular function.
    """
    # Get the qualified name of the method using __qualname__
    method_name = method.__qualname__

    # Create input and output list keys
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    # Get the input and output lists from Redis
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    # Display the history of calls
    print(f"{method_name} was called {len(inputs)} times:")
    for input_str, output_str in zip(inputs, outputs):
        input_args = tuple(eval(input_str.decode('utf-8')))
        output_value = output_str.decode('utf-8')
        print(f"{method_name}{input_args} -> {output_value}")


def count_calls(fn: Callable) -> Callable:
    """
    Decorator to count the number of times
    a method is called

    Args:
        fn (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        increment count
        """
        if isinstance(self._redis, redis.Redis):
            key = method.__qualname__
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Get the qualified name of the method using __qualname__
        method_name = method.__qualname__

        # Create input and output list keys
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"

        # Append input arguments to the input list
        input_str = str(args)
        self._redis.rpush(inputs_key, input_str)

        # Call the original method and retrieve its output
        output = method(self, *args, **kwargs)

        # Store the output in the output list
        self._redis.rpush(outputs_key, output)

        return output

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
