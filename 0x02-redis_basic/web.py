#!/usr/bin/env python3

"""Contains a web class"""

import requests
from functools import wraps
from datetime import datetime, timedelta
from typing import Callable, Any, Dict


cache = {}


def cache_decorator(expiration_time: int) -> Callable:
    """
    A decorator function that caches the results of a
    function for a specified amount of time.

    :param expiration_time: The amount of time in seconds
    to cache the results of the function.
    :return: A decorator that can be used to cache the results of a function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            url = args[0]
            now = datetime.now()
            if url in cache and cache[url]['expiration_time'] > now:
                cache[url]['count'] += 1
                return cache[url]['result']
            result = func(*args, **kwargs)
            cache[url] = {
                'result': result,
                'expiration_time': now + timedelta(seconds=expiration_time),
                'count': 1
            }
            return result
        return wrapper
    return decorator


@cache_decorator(expiration_time=10)
def get_page(url: str) -> str:
    """
    A function that uses the requests module to obtain the HTML
    content of a particular URL and returns it.

    :param url: The URL to get the HTML content from.
    :return: The HTML content of the specified URL.
    """
    response = requests.get(url)
    return response.text
