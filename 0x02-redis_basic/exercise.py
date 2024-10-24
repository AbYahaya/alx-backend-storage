#!/usr/bin/env python3
"""
This module defines a Cache class and related utilities for tracking
method calls and displaying call history using Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a
    function in Redis. Input arguments are stored in a Redis list with
    key "<method_name>:inputs". Outputs are stored in a Redis list with
    key "<method_name>:outputs".
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores inputs and outputs in Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called. The count
    is stored in Redis with the method's qualified name as the key.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments call count and invokes the original method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls for a particular function.  
    Args:
        method (Callable): The function whose history is to be
        displayed.
    """
    method_name = method.__qualname__

    redis_instance = method.__self__._redis
    num_calls = int(redis_instance.get(method_name) or 0)

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {num_calls} times:")
    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """
    Cache class for storing data in Redis and tracking method calls.
    """

    def __init__(self) -> None:
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and apply an optional conversion
        function.

        Args:
            key (str): The key to retrieve.
            fn (Optional[Callable]): A function to apply to the
            retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to retrieve the data for.

        Returns:
            Optional[str]: The decoded string value from Redis or None.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to retrieve the data for.

        Returns:
            Optional[int]: The integer value from Redis or None.
        """
        return self.get(key, lambda d: int(d))
