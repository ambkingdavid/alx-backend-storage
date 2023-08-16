#!/usr/bin/env python3

"""Contains a web class"""

import requests
import redis
from functools import wraps


class WebCache:
    def __init__(self):
        self._redis: redis.Redis = redis.Redis()

    def count_url(self, url: str) -> str:
        return f"count:{url}"

    def cache_key(self, url: str) -> str:
        return f"cache:{url}"


def count_access(method):
    """
    Decorator to count the number of times a URL is accessed.
    """
    @wraps(method)
    def wrapper(self, url: str, *args, **kwargs) -> str:
        count_key: str = self.cache.count_url(url)
        self._redis.incr(count_key)
        return method(self, url, *args, **kwargs)

    return wrapper


def cache_result(expiration: int = 10):
    """
    Decorator to cache function results with an expiration time.
    """
    def decorator(method):
        @wraps(method)
        def wrapper(self, url: str, *args, **kwargs) -> str:
            cache_key: str = self.cache.cache_key(url)
            cached_result: bytes = self._redis.get(cache_key)
            if cached_result:
                return cached_result.decode("utf-8")

            result: str = method(self, url, *args, **kwargs)
            self._redis.setex(cache_key, expiration, result)
            return result

        return wrapper

    return decorator


class Web:
    def __init__(self):
        self._redis: redis.Redis = redis.Redis()
        self.cache: WebCache = WebCache()

    @count_access
    @cache_result()
    def get_page(self, url: str) -> str:
        response: requests.Response = requests.get(url)
        return response.text
